#!/usr/bin/env python3
"""Collect raw JSONL events from a real Codex read-only session."""

from __future__ import annotations

import argparse
import errno
import hashlib
import json
import os
import pty
import select
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from efficiency_validator.manifest import (
        VALIDATOR_VERSION,
        RunManifest,
        build_run_provenance,
    )
    from efficiency_validator.staging import (
        load_staging_manifest,
        sidecar_revision,
    )
    from efficiency_validator.runtime import (
        load_runtime_manifest,
        runtime_environment,
    )
    from efficiency_validator.process_tree import snapshot_process_tree
except ModuleNotFoundError:  # direct execution from the repository checkout
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from efficiency_validator.manifest import (
        VALIDATOR_VERSION,
        RunManifest,
        build_run_provenance,
    )
    from efficiency_validator.staging import (
        load_staging_manifest,
        sidecar_revision,
    )
    from efficiency_validator.runtime import (
        load_runtime_manifest,
        runtime_environment,
    )
    from efficiency_validator.process_tree import snapshot_process_tree


def collect(
    repo: Path,
    prompt: str,
    output: Path,
    manifest_path: Path,
    *,
    run_id: str,
    case_id: str,
    model: str | None,
    staging_manifest: Path,
    runtime_manifest: Path,
    sidecar_root: Path,
    filesystem_trace_source: str = "unavailable",
    network_trace_source: str = "unavailable",
    exact_read_path: Path | None = None,
    exact_read_library: Path | None = None,
    exact_read_required: bool = False,
    variation: str = "unspecified",
    task_hash: str | None = None,
    oracle_path: Path | None = None,
    process_tree_path: Path | None = None,
    timeout_seconds: float = 1800,
) -> int:
    staged = load_staging_manifest(staging_manifest, repo)
    runtime = load_runtime_manifest(runtime_manifest, staged, repo)
    sidecar_digest = sidecar_revision(sidecar_root)
    codex_version = _codex_version()
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite capture: {output}")
    if manifest_path.exists():
        raise FileExistsError(f"Refusing to overwrite manifest: {manifest_path}")

    command_values = [
        "codex",
        "exec",
        "--cd",
        str(repo),
        "--skip-git-repo-check",
    ]
    if model:
        command_values.extend(("--model", model))
    command_values.extend(
        ("--sandbox", "read-only", "--ephemeral", "--json", prompt)
    )
    command_text = " ".join(shlex.quote(value) for value in command_values)
    command = ["/bin/zsh", "-lc", command_text]
    master_fd, slave_fd = pty.openpty()
    child_environment = runtime_environment(runtime, repo)
    exact_read_fd: int | None = None
    if exact_read_required:
        if exact_read_path is None or exact_read_library is None:
            raise ValueError(
                "exact_read_path and exact_read_library are required in exact mode"
            )
        exact_read_path.parent.mkdir(parents=True, exist_ok=True)
        exact_read_fd = os.open(
            exact_read_path,
            os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
            0o600,
        )
        child_environment.update(
            {
                "DYLD_INSERT_LIBRARIES": str(exact_read_library),
                "DYLD_FORCE_FLAT_NAMESPACE": "1",
                "EFFICIENCY_EXACT_READ_FD": str(exact_read_fd),
                "EFFICIENCY_EXACT_READ_RUN_ID": run_id,
                "EFFICIENCY_EXACT_READ_CASE_ID": case_id,
                "EFFICIENCY_EXACT_READ_TRACE_ID": f"trace-{run_id}",
            }
        )
    try:
        process = subprocess.Popen(
            command,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            close_fds=True,
            pass_fds=(() if exact_read_fd is None else (exact_read_fd,)),
            env=child_environment,
        )
    finally:
        if exact_read_fd is not None:
            os.close(exact_read_fd)
    os.close(slave_fd)

    process_pids: set[int] = {process.pid}
    process_names: set[str] = set()
    process_tree_errors: list[str] = []
    process_tree_sampled = False
    last_process_sample = 0.0

    def sample_process_tree() -> None:
        nonlocal process_tree_sampled, last_process_sample
        snapshot = snapshot_process_tree(process.pid)
        process_pids.update(snapshot.pids)
        process_names.update(snapshot.process_names)
        process_tree_sampled = process_tree_sampled or snapshot.status != "unavailable"
        if snapshot.error is not None and snapshot.error not in process_tree_errors:
            process_tree_errors.append(snapshot.error)
        last_process_sample = time.monotonic()

    sample_process_tree()

    output.parent.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now(timezone.utc)
    started_monotonic = time.monotonic()
    timed_out = False
    with output.open("x", encoding="utf-8") as stream:
        while True:
            if time.monotonic() - last_process_sample >= 0.25:
                sample_process_tree()
            remaining = timeout_seconds - (time.monotonic() - started_monotonic)
            if remaining <= 0:
                timed_out = True
                process.terminate()
                break
            try:
                ready, _, _ = select.select([master_fd], [], [], remaining)
                if not ready:
                    timed_out = True
                    process.terminate()
                    break
                chunk = os.read(master_fd, 4096)
            except OSError as exc:
                if exc.errno == errno.EIO:
                    break
                raise
            if not chunk:
                break
            stream.write(chunk.decode("utf-8", errors="replace"))
    os.close(master_fd)
    try:
        exit_code = process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        exit_code = process.wait()
    sample_process_tree()
    if exact_read_required and exact_read_path is not None:
        _append_exact_trace_end(
            exact_read_path,
            run_id=run_id,
            case_id=case_id,
            trace_id=f"trace-{run_id}",
            status="incomplete" if timed_out else "complete",
            exit_code=exit_code,
        )

    if process_tree_path is not None:
        process_tree_path.parent.mkdir(parents=True, exist_ok=True)
        process_tree_payload = {
            "schema_version": "process-tree-1",
            "root_pid": process.pid,
            "pids": sorted(process_pids),
            "process_names": sorted(process_names),
            "status": "available" if process_tree_sampled else "unavailable",
            "sampling": "periodic-process-table-snapshots",
            "errors": process_tree_errors,
        }
        with process_tree_path.open("x", encoding="utf-8") as stream:
            json.dump(process_tree_payload, stream, indent=2, sort_keys=True)
            stream.write("\n")

    finished_at = datetime.now(timezone.utc)
    effective_task_hash = task_hash or f"sha256:{hashlib.sha256(prompt.encode()).hexdigest()}"
    provenance = build_run_provenance(
        prompt=prompt,
        oracle_path=oracle_path,
        evaluator_root=sidecar_root,
        variation=variation,
        task_hash=effective_task_hash,
        case_id=case_id,
    )
    manifest = RunManifest(
        run_id=run_id,
        case_id=case_id,
        repo_revision=staged.source_revision,
        runtime_revision=runtime.runtime_revision,
        task_hash=effective_task_hash,
        model=model or "codex-default",
        codex_version=codex_version,
        observer_version=VALIDATOR_VERSION,
        launch_mode="host-runtime-pty",
        sandbox="read-only",
        ephemeral=True,
        started_at=started_at.isoformat(),
        finished_at=finished_at.isoformat(),
        exit_code=exit_code,
        complete=not timed_out and exit_code == 0,
        sidecar_revision=sidecar_digest,
        observability_schema="observability-1",
        token_usage_source="codex-exec-json",
        filesystem_trace_source=filesystem_trace_source,
        network_trace_source=network_trace_source,
        exact_read_required=exact_read_required,
        exact_read_trace_source=(
            "dyld-read-interposer" if exact_read_required else "unavailable"
        ),
        variation=variation,
        prompt=str(provenance["prompt"]),
        prompt_hash=str(provenance["prompt_hash"]),
        oracle=dict(provenance["oracle"]),
        controlled_variation=dict(provenance["controlled_variation"]),
        provenance_status=str(provenance["provenance_status"]),
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("x", encoding="utf-8") as stream:
        json.dump(manifest.to_dict(), stream, indent=2, sort_keys=True)
        stream.write("\n")
    return exit_code


def _codex_version() -> str:
    result = subprocess.run(
        ["codex", "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    version = (result.stdout or result.stderr).strip()
    if not version:
        raise RuntimeError("Codex did not report a version")
    return version


def _append_exact_trace_end(
    path: Path,
    *,
    run_id: str,
    case_id: str,
    trace_id: str,
    status: str,
    exit_code: int,
) -> None:
    """Close the sidecar only after the measured process has exited.

    A missing end record is treated as a truncated channel by the parser.  The
    parent writes this record after ``wait`` so a killed or still-running
    descendant cannot be mistaken for a complete trace.
    """

    with path.open("a", encoding="utf-8") as stream:
        json.dump(
            {
                "type": "exact-read.trace.ended",
                "run_id": run_id,
                "case_id": case_id,
                "trace_id": trace_id,
                "status": status,
                "exit_code": exit_code,
            },
            stream,
            sort_keys=True,
        )
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument(
        "--variation",
        default="unspecified",
        help="Declared experimental variation for paired comparisons",
    )
    parser.add_argument(
        "--task-hash",
        help="Canonical task identity shared by controlled prompt variations",
    )
    parser.add_argument(
        "--oracle",
        type=Path,
        help="Evaluator oracle used for this run, recorded by content digest",
    )
    parser.add_argument(
        "--model",
        help="Explicit Codex model; omit to use the account's configured default",
    )
    parser.add_argument("--staging-manifest", type=Path, required=True)
    parser.add_argument("--runtime-manifest", type=Path, required=True)
    parser.add_argument("--sidecar-root", type=Path, required=True)
    parser.add_argument(
        "--network-trace-source", default="unavailable"
    )
    parser.add_argument("--exact-read", action="store_true")
    parser.add_argument("--exact-read-path", type=Path)
    parser.add_argument("--exact-read-library", type=Path)
    parser.add_argument(
        "--process-tree",
        type=Path,
        help="Write sampled measured-process-tree metadata to this path",
    )
    parser.add_argument("--timeout-seconds", type=float, default=1800)
    args = parser.parse_args()
    return collect(
        args.repo,
        args.prompt,
        args.output,
        args.manifest,
        run_id=args.run_id,
        case_id=args.case_id,
        model=args.model,
        staging_manifest=args.staging_manifest,
        runtime_manifest=args.runtime_manifest,
        sidecar_root=args.sidecar_root,
        variation=args.variation,
        task_hash=args.task_hash,
        oracle_path=args.oracle,
        process_tree_path=args.process_tree,
        network_trace_source=args.network_trace_source,
        exact_read_path=args.exact_read_path,
        exact_read_library=args.exact_read_library,
        exact_read_required=args.exact_read,
        timeout_seconds=args.timeout_seconds,
    )


if __name__ == "__main__":
    raise SystemExit(main())
