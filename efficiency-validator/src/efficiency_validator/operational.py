"""Capture a real CLI run into a self-contained operational evidence bundle.

The workspace is disposable; inputs, raw streams and outputs are retained.
No host credentials or user configuration are copied into the bundle.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import math
import os
import platform
from pathlib import Path
import selectors
import shutil
import signal
import stat
import subprocess
import tempfile
import time
from datetime import datetime, timezone

VERSION = "operational-1"
DEFAULT_EXCLUDES = (".git", ".venv", "node_modules", "__pycache__", ".pytest_cache")


def write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def inventory(root: Path) -> dict:
    result = {}
    for path in sorted(root.rglob("*")):
        name = path.relative_to(root).as_posix()
        info = path.lstat()
        if path.is_symlink():
            result[name] = {"link": os.readlink(path)}
        elif stat.S_ISREG(info.st_mode):
            result[name] = {"sha256": digest(path.read_bytes()), "mode": stat.S_IMODE(info.st_mode)}
    return result


def snapshot(source: Path, destination: Path, excludes=()) -> dict:
    """Copy only regular files/directories and nonescaping relative symlinks."""
    destination.mkdir(parents=True, exist_ok=False)
    for directory, dirs, files in os.walk(source, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in excludes)
        for name in sorted(dirs + files):
            if name in excludes:
                continue
            path = Path(directory) / name
            target = destination / path.relative_to(source)
            info = path.lstat()
            if path.is_symlink():
                link = os.readlink(path)
                if os.path.isabs(link) or not path.resolve().is_relative_to(source.resolve()):
                    raise ValueError(f"External symlink must be materialized or excluded: {path}")
                target.symlink_to(link)
            elif stat.S_ISDIR(info.st_mode):
                target.mkdir(exist_ok=True)
            elif stat.S_ISREG(info.st_mode):
                shutil.copy2(path, target)
            else:
                raise ValueError(f"Unsupported special file: {path}")
    return inventory(destination)


def _run(command: list[str], cwd: Path, prefix: Path, *, timeout: float,
         stdin: Path | None = None, cancel: Path | None = None) -> dict:
    started = time.monotonic()
    result = {"command": command, "started_at": datetime.now(timezone.utc).isoformat(),
              "termination": "launch_failed", "exit_code": None,
              "cleanup": "not_needed", "timing_source": "host-monotonic"}
    process = None
    selector = selectors.DefaultSelector()
    handlers = {}
    interrupted = []
    try:
        for sig in (signal.SIGINT, signal.SIGTERM):
            handlers[sig] = signal.signal(sig, lambda signum, frame: interrupted.append(signum))
        with (stdin.open("rb") if stdin else open(os.devnull, "rb")) as incoming, \
                prefix.with_suffix(".jsonl").open("xb", buffering=0) as stdout, \
                prefix.with_suffix(".stderr").open("xb", buffering=0) as stderr, \
                prefix.with_suffix(".arrivals.jsonl").open("x", buffering=1) as arrivals:
            process = subprocess.Popen(command, cwd=cwd, stdin=incoming,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       start_new_session=True)
            result["pid"] = process.pid
            write_json(prefix.with_suffix(".process.json"), {"pid": process.pid, "started_at": result["started_at"]})
            for stream, output in ((process.stdout, stdout), (process.stderr, stderr)):
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, output)
            result["termination"] = "exited"
            stop_at = None
            line_number = 0
            pending = b""
            while selector.get_map() or process.poll() is None:
                elapsed = time.monotonic() - started
                if stop_at is None and (interrupted or (cancel and cancel.exists()) or elapsed >= timeout):
                    result["termination"] = "cancelled" if interrupted or (cancel and cancel.exists()) else "timeout"
                    stop_at = time.monotonic()
                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                if stop_at is not None and time.monotonic() - stop_at >= 2:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    if time.monotonic() - stop_at >= 3:
                        break
                for key, _ in selector.select(0.05):
                    chunk = os.read(key.fileobj.fileno(), 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    key.data.write(chunk)
                    if key.data is stdout:
                        pending += chunk
                        while b"\n" in pending:
                            _, pending = pending.split(b"\n", 1)
                            line_number += 1
                            arrivals.write(json.dumps({"line": line_number, "elapsed_seconds": elapsed}) + "\n")
            if pending:
                arrivals.write(json.dumps({"line": line_number + 1, "elapsed_seconds": time.monotonic() - started,
                                          "unterminated": True}) + "\n")
            result["exit_code"] = process.wait(timeout=3)
    except (OSError, subprocess.SubprocessError) as exc:
        result["error"] = str(exc)
        result["termination"] = "capture_failed" if process else "launch_failed"
    finally:
        if process:
            # Clean up the process group even when a parent exits before its children.
            try:
                os.killpg(process.pid, signal.SIGKILL)
                result["cleanup"] = "group_signalled; escaped descendants unobservable"
            except ProcessLookupError:
                result["cleanup"] = "group_exited; escaped descendants unobservable"
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                result["cleanup"] = "incomplete"
            for stream in (process.stdout, process.stderr):
                if stream:
                    stream.close()
        selector.close()
        for sig, handler in handlers.items():
            signal.signal(sig, handler)
        result["duration_seconds"] = time.monotonic() - started
    return result


def capture(source: Path, bundle: Path, *, prompt: str, variant: str,
            model: str | None = None, reasoning: str | None = None,
            sandbox: str = "workspace-write", timeout: float = 300,
            codex: str = "codex", overlays: dict[str, Path] | None = None,
            checks: list[list[str]] | None = None, excludes=DEFAULT_EXCLUDES) -> dict:
    """Run a fresh task. A reserved bundle is never overwritten, even on failure."""
    source, bundle = source.resolve(), bundle.resolve()
    codex = str(codex)
    if not source.is_dir() or bundle.is_relative_to(source) or source.is_relative_to(bundle):
        raise ValueError("Source must be a directory disjoint from the bundle")
    if sandbox not in {"read-only", "workspace-write"}:
        raise ValueError("Only read-only and workspace-write sandboxes are supported")
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be positive and finite")
    if not prompt.strip() or not variant.strip():
        raise ValueError("prompt and variant must be nonempty")
    bundle.mkdir(parents=True, exist_ok=False, mode=0o700)
    began = time.monotonic()
    manifest = {"schema": VERSION, "run_id": bundle.name, "variant": variant,
                "collector_pid": os.getpid(),
                "runtime_environment": {"platform": platform.platform(), "python": platform.python_version(),
                                        "path_sha256": digest(os.environ.get("PATH", "").encode()),
                                        "dependencies": "copied inputs plus inherited host executables; no automatic installation"},
                "prompt_sha256": digest(prompt.encode()), "model_requested": model,
                "model_resolved": None, "reasoning": reasoning, "sandbox": sandbox,
                "fresh_session": True, "cache_state": "unavailable",
                "user_config": "ignored; host authentication retained in place",
                "ambient_context": "global instructions/skills and system policy may still apply; not fully isolated",
                "excludes": list(excludes), "source": str(source), "termination": "preparing",
                "budget_support": {"wall_clock_seconds": timeout, "tokens": None, "money": None},
                "versions": {"collector": VERSION, "collector_sha256": digest(Path(__file__).read_bytes())},
                "checks_requested": checks or []}
    write_json(bundle / "manifest.json", manifest)
    workspace = None
    try:
        inputs = bundle / "inputs"
        inputs.mkdir()
        (inputs / "prompt.txt").write_text(prompt)
        before = snapshot(source, inputs / "target", excludes)
        manifest["base_inventory"] = before
        manifest["base_sha256"] = digest(json.dumps(before, sort_keys=True).encode())
        for relative, origin in (overlays or {}).items():
            destination = inputs / "target" / relative
            if Path(relative).is_absolute() or ".." in Path(relative).parts or not relative:
                raise ValueError("Overlay destination must be a nonempty relative path without '..'")
            if not destination.resolve().is_relative_to(inputs / "target"):
                raise ValueError("Overlay destination escapes target")
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.is_dir() or destination.is_symlink():
                raise ValueError("Overlay destination must be absent or a regular file")
            if origin.is_dir():
                snapshot(origin.resolve(), destination)
            elif origin.is_file():
                shutil.copy2(origin, destination)
            else:
                raise ValueError(f"Missing overlay resource: {origin}")
        before = inventory(inputs / "target")
        manifest["input_inventory"] = before
        manifest["input_sha256"] = digest(json.dumps(before, sort_keys=True).encode())
        manifest["overlay_paths"] = sorted((overlays or {}).keys())
        workspace = Path(tempfile.mkdtemp(prefix="efficiency-workspace-"))
        snapshot(inputs / "target", workspace / "target")
        command = [codex, "exec", "--ignore-user-config", "--ephemeral", "--json",
                   "--skip-git-repo-check", "--sandbox", sandbox, "--cd", str(workspace / "target")]
        if model:
            command.extend(["--model", model])
        if reasoning:
            command.extend(["-c", f"model_reasoning_effort={json.dumps(reasoning)}"])
        command.append("-")
        version = subprocess.run([codex, "--version"], capture_output=True, text=True, timeout=10)
        manifest["versions"]["codex"] = version.stdout.strip() if version.returncode == 0 else None
        manifest["setup_seconds"] = time.monotonic() - began
        manifest["workspace"] = str(workspace / "target")
        manifest["termination"] = "running"
        write_json(bundle / "manifest.json", manifest)
        run = _run(command, workspace / "target", bundle / "events", timeout=timeout,
                   stdin=inputs / "prompt.txt", cancel=bundle / "cancel.request")
        manifest["execution"] = run
        manifest["termination"] = run["termination"]
        outputs = bundle / "outputs"
        outputs.mkdir()
        after = snapshot(workspace / "target", outputs / "target")
        changes, patches = [], []
        for name in sorted(before.keys() | after.keys()):
            if before.get(name) == after.get(name):
                continue
            changes.append({"path": name, "kind": "created" if name not in before else "deleted" if name not in after else "modified",
                            "before": before.get(name), "after": after.get(name)})
            old, new = inputs / "target" / name, outputs / "target" / name
            try:
                a = old.read_text().splitlines(keepends=True) if old.is_file() and not old.is_symlink() else []
                b = new.read_text().splitlines(keepends=True) if new.is_file() and not new.is_symlink() else []
                patches.extend(difflib.unified_diff(a, b, fromfile="before/" + name, tofile="after/" + name))
            except UnicodeError:
                patches.append(f"Binary change: {name}\n")
        write_json(bundle / "changes.json", changes)
        (bundle / "changes.patch").write_text("".join(patches))
        manifest["output_inventory"] = after
        check_results = []
        if checks and run["termination"] == "exited" and run["exit_code"] == 0:
            for index, check in enumerate(checks):
                check_results.append(_run(check, workspace / "target", bundle / f"check-{index}",
                                          timeout=timeout, cancel=bundle / "cancel.request"))
        write_json(bundle / "checks.json", check_results)
        # Keep runtime checks separate from the agent's own result and task duration.
        from .codex_events import parse_codex_stream
        parsed = parse_codex_stream((bundle / "events.jsonl").read_text(errors="replace").splitlines())
        if manifest["termination"] == "exited":
            manifest["termination"] = "completed" if run["exit_code"] == 0 and parsed.turns and all(t.status == "completed" for t in parsed.turns) else "failed"
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        manifest["termination"] = "capture_failed"
        manifest["error"] = str(exc)
    finally:
        manifest["total_seconds"] = time.monotonic() - began
        if workspace:
            manifest["workspace_retained"] = True
        manifest["evidence_hashes"] = {
            p.relative_to(bundle).as_posix(): digest(p.read_bytes())
            for p in sorted(bundle.rglob("*"))
            if p.is_file() and not p.is_symlink() and p.name not in {"manifest.json", "cancel.request"}
        }
        write_json(bundle / "manifest.json", manifest)
    return manifest


def recover(bundle: Path, *, confirmed_stopped: bool = False) -> dict:
    """Finalize evidence after collector death; never relaunch or kill a PID."""
    manifest = json.loads((bundle / "manifest.json").read_text())
    if manifest.get("schema") != VERSION or manifest.get("termination") not in {"preparing", "running"}:
        raise ValueError("Only an unfinished operational-1 bundle can be recovered")
    pids = [manifest.get("collector_pid")]
    process_file = bundle / "events.process.json"
    if process_file.exists():
        pids.append(json.loads(process_file.read_text())["pid"])
    if pids[0] is None and not confirmed_stopped:
        raise ValueError("Collector identity missing; verify it stopped and use --confirm-stopped")
    for pid in pids:
        if pid is None:
            continue
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            continue
        raise ValueError(f"Process {pid} may still be alive; recovery refused")
    manifest["termination"] = "interrupted"
    manifest["recovery"] = "Retained received evidence; process cleanup and end time unavailable"
    workspace = manifest.get("workspace")
    if workspace and Path(workspace).is_dir() and not (bundle / "outputs").exists():
        try:
            after = snapshot(Path(workspace), bundle / "outputs/target")
            manifest["output_inventory"] = after
            before = manifest.get("input_inventory", {})
            write_json(bundle / "changes.json", [
                {"path": name, "kind": "created" if name not in before else "deleted" if name not in after else "modified",
                 "before": before.get(name), "after": after.get(name)}
                for name in sorted(before.keys() | after.keys()) if before.get(name) != after.get(name)])
        except (ValueError, OSError) as exc:
            manifest["recovery_output_error"] = str(exc)
    manifest["evidence_hashes"] = {
        p.relative_to(bundle).as_posix(): digest(p.read_bytes())
        for p in sorted(bundle.rglob("*"))
        if p.is_file() and not p.is_symlink() and p.name not in {"manifest.json", "cancel.request"}}
    write_json(bundle / "manifest.json", manifest)
    return manifest
