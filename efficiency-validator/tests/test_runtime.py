import json
from pathlib import Path

import pytest

from efficiency_validator.runtime import (
    RuntimeManifest,
    load_runtime_manifest,
    runtime_environment,
)
from efficiency_validator.staging import StagingManifest, tree_hash


def _staging_manifest(target: Path) -> StagingManifest:
    return StagingManifest(
        source_revision="target-commit",
        staged_root=str(target.resolve()),
        tree_hash=tree_hash(target),
    )


def test_runtime_manifest_round_trips_and_prepares_isolated_environment(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target"
    target.mkdir()
    (target / ".context-lab-tmp").mkdir()
    (target / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    (target / "uv.lock").write_text("lock\n", encoding="utf-8")
    staging = _staging_manifest(target)
    runtime_root = tmp_path / "runtime"
    (runtime_root / "bin").mkdir(parents=True)
    (runtime_root / "bin" / "python").write_text("", encoding="utf-8")
    manifest = RuntimeManifest(
        source_revision=staging.source_revision,
        target_tree_hash=staging.tree_hash,
        runtime_root=str(runtime_root.resolve()),
        runtime_revision="sha256:runtime",
        python_version="Python 3.13.7",
        uv_version="uv 0.9.0",
        extras=("test",),
    )

    restored = RuntimeManifest.from_dict(manifest.to_dict())
    environment = runtime_environment(restored, target)

    assert restored == manifest
    assert environment["VIRTUAL_ENV"] == str(runtime_root.resolve())
    assert environment["UV_PROJECT_ENVIRONMENT"] == str(runtime_root.resolve())
    assert environment["TMPDIR"] == str(target / ".context-lab-tmp")
    assert environment["PATH"].split(":", 1)[0] == str(runtime_root / "bin")
    assert environment["PYTHONNOUSERSITE"] == "1"


def test_runtime_manifest_must_match_the_staged_target(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    staging = _staging_manifest(target)
    runtime_root = tmp_path / "runtime"
    (runtime_root / "bin").mkdir(parents=True)
    (runtime_root / "bin" / "python").write_text("", encoding="utf-8")
    manifest_path = tmp_path / "runtime.json"
    manifest_path.write_text(
        json.dumps(
            RuntimeManifest(
                source_revision="different-commit",
                target_tree_hash=staging.tree_hash,
                runtime_root=str(runtime_root.resolve()),
                runtime_revision="sha256:runtime",
                python_version="Python 3.13.7",
                uv_version="uv 0.9.0",
                extras=("test",),
            ).to_dict()
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="source revision"):
        load_runtime_manifest(manifest_path, staging, target)
