from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .staging import RUNTIME_TEMP_DIR, StagingManifest, load_staging_manifest


@dataclass(frozen=True)
class RuntimeManifest:
    """Provenance for the host runtime made available to a measured run."""

    source_revision: str
    target_tree_hash: str
    runtime_root: str
    runtime_revision: str
    python_version: str
    uv_version: str
    extras: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_revision": self.source_revision,
            "target_tree_hash": self.target_tree_hash,
            "runtime_root": self.runtime_root,
            "runtime_revision": self.runtime_revision,
            "python_version": self.python_version,
            "uv_version": self.uv_version,
            "extras": list(self.extras),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RuntimeManifest":
        required = {
            "source_revision",
            "target_tree_hash",
            "runtime_root",
            "runtime_revision",
            "python_version",
            "uv_version",
            "extras",
        }
        missing = sorted(required - payload.keys())
        if missing:
            raise ValueError(
                f"Runtime manifest is missing: {', '.join(missing)}"
            )
        extras = payload["extras"]
        if not isinstance(extras, list) or not all(
            isinstance(extra, str) and extra for extra in extras
        ):
            raise ValueError("Runtime manifest extras must be a non-empty string list")
        manifest = cls(
            source_revision=str(payload["source_revision"]),
            target_tree_hash=str(payload["target_tree_hash"]),
            runtime_root=str(payload["runtime_root"]),
            runtime_revision=str(payload["runtime_revision"]),
            python_version=str(payload["python_version"]),
            uv_version=str(payload["uv_version"]),
            extras=tuple(extras),
        )
        if not all(
            (
                manifest.source_revision,
                manifest.target_tree_hash,
                manifest.runtime_root,
                manifest.runtime_revision,
                manifest.python_version,
                manifest.uv_version,
            )
        ):
            raise ValueError("Runtime manifest values must not be empty")
        return manifest


def prepare_runtime(
    target: Path,
    staging_manifest_path: Path,
    runtime_root: Path,
    manifest_path: Path,
    *,
    extras: tuple[str, ...] = ("test",),
) -> RuntimeManifest:
    """Create a locked runtime outside the staged target."""

    target = target.resolve()
    runtime_root = runtime_root.resolve()
    staging = load_staging_manifest(staging_manifest_path, target)
    if not (target / "pyproject.toml").is_file():
        raise ValueError(f"Target has no pyproject.toml: {target}")
    if not (target / "uv.lock").is_file():
        raise ValueError(f"Target has no uv.lock: {target}")
    if not extras:
        raise ValueError("At least one runtime extra is required")
    if runtime_root.exists() and any(runtime_root.iterdir()):
        raise FileExistsError(f"Runtime destination is not empty: {runtime_root}")

    uv = shutil.which("uv")
    if uv is None:
        raise FileNotFoundError("uv is required to prepare the target runtime")
    runtime_root.parent.mkdir(parents=True, exist_ok=True)
    uv_environment = os.environ.copy()
    uv_environment.setdefault(
        "UV_CACHE_DIR", str(runtime_root.parent / "uv-cache")
    )
    uv_environment["VIRTUAL_ENV"] = str(runtime_root)
    uv_environment["PATH"] = os.pathsep.join(
        (str(runtime_root / "bin"), uv_environment.get("PATH", ""))
    )
    subprocess.run(
        [uv, "venv", str(runtime_root)], check=True, env=uv_environment
    )
    runtime_python = runtime_root / "bin" / "python"
    if not runtime_python.is_file():
        raise RuntimeError(f"uv did not create a Python runtime: {runtime_python}")

    sync_command = [
        uv,
        "sync",
        "--project",
        str(target),
        "--active",
        "--locked",
    ]
    for extra in extras:
        sync_command.extend(("--extra", extra))
    subprocess.run(sync_command, check=True, env=uv_environment)

    python_version = _version(runtime_python)
    uv_version = _version(Path(uv), "--version")
    runtime_revision = _runtime_revision(
        target / "uv.lock", python_version, uv_version, extras
    )
    return RuntimeManifest(
        source_revision=staging.source_revision,
        target_tree_hash=staging.tree_hash,
        runtime_root=str(runtime_root),
        runtime_revision=runtime_revision,
        python_version=python_version,
        uv_version=uv_version,
        extras=extras,
    )


def load_runtime_manifest(
    path: Path,
    staging: StagingManifest,
    target: Path,
) -> RuntimeManifest:
    manifest = RuntimeManifest.from_dict(json.loads(path.read_text(encoding="utf-8")))
    if manifest.source_revision != staging.source_revision:
        raise ValueError("Runtime manifest source revision does not match staging")
    if manifest.target_tree_hash != staging.tree_hash:
        raise ValueError("Runtime manifest target hash does not match staging")
    if Path(manifest.runtime_root).resolve() == target.resolve():
        raise ValueError("Runtime must be outside the staged target")
    runtime_python = Path(manifest.runtime_root) / "bin" / "python"
    if not runtime_python.is_file():
        raise ValueError(f"Runtime Python is missing: {runtime_python}")
    return manifest


def runtime_environment(
    manifest: RuntimeManifest,
    workspace: Path,
) -> dict[str, str]:
    runtime_root = Path(manifest.runtime_root).resolve()
    runtime_bin = runtime_root / "bin"
    runtime_python = runtime_bin / "python"
    if not runtime_python.is_file():
        raise ValueError(f"Runtime Python is missing: {runtime_python}")
    environment = os.environ.copy()
    temp_root = workspace.resolve() / RUNTIME_TEMP_DIR
    temp_root.mkdir(parents=True, exist_ok=True)
    environment["VIRTUAL_ENV"] = str(runtime_root)
    environment["UV_PROJECT_ENVIRONMENT"] = str(runtime_root)
    environment["TMPDIR"] = str(temp_root)
    environment["TEMP"] = str(temp_root)
    environment["TMP"] = str(temp_root)
    environment["PATH"] = os.pathsep.join(
        (str(runtime_bin), environment.get("PATH", ""))
    )
    environment["PYTHONNOUSERSITE"] = "1"
    return environment


def _version(executable: Path, *arguments: str) -> str:
    result = subprocess.run(
        [str(executable), *arguments, "--version"]
        if not arguments
        else [str(executable), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    version = (result.stdout or result.stderr).strip()
    if not version:
        raise RuntimeError(f"Executable did not report a version: {executable}")
    return version


def _runtime_revision(
    lockfile: Path,
    python_version: str,
    uv_version: str,
    extras: tuple[str, ...],
) -> str:
    digest = hashlib.sha256()
    digest.update(lockfile.read_bytes())
    digest.update(b"\0")
    digest.update(python_version.encode("utf-8"))
    digest.update(b"\0")
    digest.update(uv_version.encode("utf-8"))
    digest.update(b"\0")
    digest.update(json.dumps(extras).encode("utf-8"))
    return f"sha256:{digest.hexdigest()}"
