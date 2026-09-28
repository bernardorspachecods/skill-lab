from pathlib import Path

import pytest

from efficiency_validator.staging import (
    RUNTIME_TEMP_DIR,
    StagingManifest,
    tree_hash,
    validate_staged_target,
)


def test_staging_manifest_round_trips_and_tree_hash_is_content_sensitive(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target"
    (target / "docs").mkdir(parents=True)
    (target / "CONTEXT.md").write_text("# Target\n", encoding="utf-8")
    (target / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
    (target / "apps").mkdir()
    (target / "packages").mkdir()
    (target / "docs" / "rules.md").write_text("v1\n", encoding="utf-8")
    validate_staged_target(target)
    first_hash = tree_hash(target)
    (target / RUNTIME_TEMP_DIR / "pytest-temp").mkdir(parents=True)
    (target / RUNTIME_TEMP_DIR / "pytest-temp" / "capture").write_text(
        "ephemeral\n", encoding="utf-8"
    )
    assert tree_hash(target) == first_hash

    manifest = StagingManifest(
        source_revision="abc123",
        staged_root=str(target.resolve()),
        tree_hash=first_hash,
    )

    (target / "docs" / "rules.md").write_text("v2\n", encoding="utf-8")

    assert StagingManifest.from_dict(manifest.to_dict()) == manifest
    assert tree_hash(target) != first_hash


def test_staged_target_rejects_harness_entries(tmp_path: Path) -> None:
    target = tmp_path / "target"
    for name in ("apps", "packages", "docs"):
        (target / name).mkdir(parents=True, exist_ok=True)
    (target / "CONTEXT.md").write_text("# Target\n", encoding="utf-8")
    (target / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
    (target / "observer").mkdir()

    with pytest.raises(ValueError, match="forbidden"):
        validate_staged_target(target)
