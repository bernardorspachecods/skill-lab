from __future__ import annotations

import hashlib
import io
import json
import subprocess
import tarfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


FORBIDDEN_TARGET_ENTRIES = frozenset(
    {"PLAN.md", "evaluation", "observer", "working", "traces"}
)
REQUIRED_TARGET_ENTRIES = frozenset(
    {"CONTEXT.md", "AGENTS.md", "apps", "packages", "docs"}
)
RUNTIME_TEMP_DIR = ".context-lab-tmp"


@dataclass(frozen=True)
class StagingManifest:
    source_revision: str
    staged_root: str
    tree_hash: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "StagingManifest":
        required = {"source_revision", "staged_root", "tree_hash"}
        missing = sorted(required - payload.keys())
        if missing:
            raise ValueError(f"Staging manifest is missing: {', '.join(missing)}")
        manifest = cls(
            source_revision=str(payload["source_revision"]),
            staged_root=str(payload["staged_root"]),
            tree_hash=str(payload["tree_hash"]),
        )
        if not all((manifest.source_revision, manifest.staged_root, manifest.tree_hash)):
            raise ValueError("Staging manifest values must not be empty")
        return manifest


def git_revision(repo: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def assert_clean_git_repository(repo: Path) -> None:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        raise ValueError(f"Source repository has uncommitted changes: {repo}")


def stage_target(source: Path, destination: Path) -> StagingManifest:
    source = source.resolve()
    destination = destination.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f"Staging destination is not empty: {destination}")

    assert_clean_git_repository(source)
    revision = git_revision(source)
    destination.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(
        ["git", "archive", "--format=tar", revision],
        cwd=source,
        check=True,
        capture_output=True,
    )
    with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as tar:
        tar.extractall(destination, filter="data")
    (destination / RUNTIME_TEMP_DIR).mkdir()
    validate_staged_target(destination)
    return StagingManifest(
        source_revision=revision,
        staged_root=str(destination),
        tree_hash=tree_hash(destination),
    )


def validate_staged_target(root: Path) -> None:
    root = root.resolve()
    if (root / ".git").exists():
        raise ValueError("Staged target must not contain .git")
    entries = {entry.name for entry in root.iterdir()}
    forbidden = sorted(entries & FORBIDDEN_TARGET_ENTRIES)
    if forbidden:
        raise ValueError(f"Staged target contains forbidden entries: {forbidden}")
    missing = sorted(REQUIRED_TARGET_ENTRIES - entries)
    if missing:
        raise ValueError(f"Staged target is missing required entries: {missing}")


def load_staging_manifest(path: Path, staged_root: Path) -> StagingManifest:
    manifest = StagingManifest.from_dict(
        json.loads(path.read_text(encoding="utf-8"))
    )
    root = staged_root.resolve()
    if Path(manifest.staged_root).resolve() != root:
        raise ValueError("Staging manifest does not describe the supplied repo")
    validate_staged_target(root)
    if tree_hash(root) != manifest.tree_hash:
        raise ValueError("Staged target content does not match its manifest")
    return manifest


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(
        (
            candidate
            for candidate in root.rglob("*")
            if candidate.is_file()
            and RUNTIME_TEMP_DIR not in candidate.relative_to(root).parts
        ),
        key=lambda candidate: candidate.relative_to(root).as_posix(),
    ):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def sidecar_revision(sidecar_root: Path) -> str:
    oracle_root = sidecar_root.resolve() / "oracles"
    if not oracle_root.is_dir():
        raise ValueError(f"Evaluator sidecar has no oracles directory: {oracle_root}")
    return tree_hash(oracle_root)
