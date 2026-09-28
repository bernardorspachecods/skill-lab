"""Build the authorized macOS exact-read collector."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


class ExactReadCaptureError(RuntimeError):
    """Raised when the exact-read collector cannot be prepared."""


def build_macos_interposer(output: Path) -> Path:
    """Compile the local exact-read adapter into an isolated output path."""

    if sys.platform != "darwin":
        raise ExactReadCaptureError("exact-read interposer currently requires macOS")
    clang = shutil.which("clang") or "/usr/bin/clang"
    source = Path(__file__).resolve().parents[2] / "scripts" / "exact_read_interposer.c"
    if not source.is_file():
        raise ExactReadCaptureError(f"collector source is missing: {source}")
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            clang,
            "-dynamiclib",
            "-fPIC",
            "-O2",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-o",
            str(output),
            str(source),
            "-framework",
            "Security",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    if not output.is_file():
        raise ExactReadCaptureError(f"clang produced no collector: {output}")
    return output
