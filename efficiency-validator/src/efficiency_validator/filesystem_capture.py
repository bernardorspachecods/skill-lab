"""Lifecycle control for an authorized macOS fs_usage sidecar.

The helper delegates authorization to macOS through osascript. The
harness never receives, prompts for, or stores the administrator password.
The privileged shell writes a raw capture and watches a user-owned stop file;
the normal parser later filters the raw stream to the staged target or the
sampled measured process tree.
"""

from __future__ import annotations

import os
import base64
import json
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import time
from typing import Callable, Protocol


class FilesystemCaptureError(RuntimeError):
    """Raised when the requested privileged capture cannot be established."""


class _Process(Protocol):
    pid: int

    def poll(self) -> int | None: ...

    def wait(self, timeout: float | None = None) -> int: ...

    def terminate(self) -> None: ...


PopenFactory = Callable[..., _Process]


class MacOSFsUsageCapture:
    """Start and stop one target-correlated privileged fs_usage capture."""

    def __init__(
        self,
        *,
        run_id: str,
        case_id: str,
        raw_path: Path,
        target_prefix: Path,
        additional_prefixes: tuple[Path, ...] = (),
        capture_all_paths: bool = False,
        timeout_seconds: int = 1800,
        authorization_timeout_seconds: float = 60.0,
        popen_factory: PopenFactory = subprocess.Popen,
    ) -> None:
        self.run_id = run_id
        self.case_id = case_id
        self.raw_path = raw_path.resolve()
        self.target_prefix = target_prefix.resolve()
        self.additional_prefixes = tuple(
            prefix.resolve() for prefix in additional_prefixes
        )
        self.capture_all_paths = capture_all_paths
        self.timeout_seconds = timeout_seconds
        self.authorization_timeout_seconds = authorization_timeout_seconds
        self._popen = popen_factory
        self._process: _Process | None = None
        self._ready_path = self.raw_path.parent / "capture.ready"
        self._stop_path = self.raw_path.parent / "capture.stop"
        self._error_path = self.raw_path.parent / "capture.error"

    def start(self) -> None:
        if sys.platform != "darwin":
            raise FilesystemCaptureError(
                "automatic fs_usage capture requires macOS"
            )
        self.raw_path.parent.mkdir(parents=True, exist_ok=True)
        for path in (
            self.raw_path,
            self._ready_path,
            self._stop_path,
            self._error_path,
        ):
            path.unlink(missing_ok=True)

        command = [
            "/usr/bin/osascript",
            "-e",
            self._privileged_script(),
        ]
        self._process = self._popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        deadline = time.monotonic() + self.authorization_timeout_seconds
        while not self._ready_path.exists():
            if self._process.poll() is not None:
                detail = self._error_detail()
                self._cleanup_control_files()
                raise FilesystemCaptureError(
                    "macOS fs_usage authorization failed" + detail
                )
            if time.monotonic() >= deadline:
                self._terminate_process()
                self._cleanup_control_files()
                raise FilesystemCaptureError(
                    "timed out waiting for macOS fs_usage authorization"
                )
            time.sleep(0.05)

    def stop(self, *, timeout_seconds: float = 10.0) -> Path:
        if self._process is None:
            raise FilesystemCaptureError("fs_usage capture was not started")
        self._stop_path.touch()
        try:
            self._process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            self._terminate_process()
            raise FilesystemCaptureError(
                "timed out stopping macOS fs_usage capture"
            ) from None
        finally:
            self._cleanup_control_files()
        if not self.raw_path.exists():
            raise FilesystemCaptureError(
                "fs_usage exited without producing a raw capture"
            )
        return self.raw_path

    def _privileged_script(self) -> str:
        raw = shlex.quote(str(self.raw_path))
        ready = shlex.quote(str(self._ready_path))
        stop = shlex.quote(str(self._stop_path))
        error = shlex.quote(str(self._error_path))
        prefixes = (self.target_prefix, *self.additional_prefixes)
        prefix_assignments = "\n".join(
            f"prefix_{index}={shlex.quote(str(prefix))}"
            for index, prefix in enumerate(prefixes)
        )
        prefix_cases = "\n".join(
            f'  *"$prefix_{index}"/*|*"$prefix_{index}") matches_prefix=1 ;;'
            for index in range(len(prefixes))
        )
        match_block = (
            "matches_prefix=1"
            if self.capture_all_paths
            else f"case \"$line\" in\n{prefix_cases}\n  esac"
        )
        run_id = shlex.quote(self.run_id)
        case_id = shlex.quote(self.case_id)
        shell = f"""#!/bin/sh
set -eu
raw={raw}
ready={ready}
stop={stop}
error={error}
{prefix_assignments}
run_id={run_id}
case_id={case_id}
umask 022
: > "$ready"
: > "$raw"
/usr/bin/fs_usage -w -F -f pathname -t {int(self.timeout_seconds)} 2> "$error" |
while IFS= read -r line; do
  matches_prefix=0
  {match_block}
  if [ "$matches_prefix" -eq 1 ]; then
    printf '%s\\n' "$line" >> "$raw"
  fi
  if [ -f "$stop" ]; then
    break
  fi
done &
tracer=$!
natural_exit=1
while /bin/kill -0 "$tracer" 2>/dev/null; do
  if [ -f "$stop" ]; then
    natural_exit=0
    /bin/kill "$tracer" 2>/dev/null || true
    break
  fi
  /bin/sleep 0.1
done
/bin/wait "$tracer" 2>/dev/null || true
/bin/chmod 0644 "$raw" "$error" 2>/dev/null || true
if [ "$natural_exit" -eq 1 ] && [ -s "$error" ]; then
  exit 1
fi
exit 0
"""
        encoded_shell = base64.b64encode(shell.encode("utf-8")).decode("ascii")
        shell_command = (
            f"/usr/bin/printf %s {encoded_shell} | "
            "/usr/bin/base64 -D | /bin/sh"
        )
        return (
            "do shell script "
            + json.dumps(shell_command)
            + " with administrator privileges"
        )

    def _terminate_process(self) -> None:
        if self._process is None:
            return
        try:
            os.killpg(self._process.pid, signal.SIGTERM)
        except (AttributeError, ProcessLookupError, PermissionError):
            self._process.terminate()

    def _error_detail(self) -> str:
        if not self._error_path.exists():
            return ""
        detail = self._error_path.read_text(
            encoding="utf-8", errors="replace"
        ).strip()
        return f": {detail}" if detail else ""

    def _cleanup_control_files(self) -> None:
        for path in (self._ready_path, self._stop_path, self._error_path):
            path.unlink(missing_ok=True)
