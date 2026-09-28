import hashlib
import json

import pytest

from efficiency_validator.manifest import RunManifest, build_run_provenance


def test_manifest_round_trips_required_provenance() -> None:
    manifest = RunManifest(
        run_id="run-1",
        case_id="001-create-task",
        repo_revision="working-tree-1",
        runtime_revision="sha256:runtime",
        task_hash="sha256:abc",
        model="model-1",
        codex_version="codex-1",
        observer_version="0.5.0",
        launch_mode="host-runtime",
        sandbox="read-only",
        ephemeral=True,
        started_at="2026-09-24T10:00:00Z",
        finished_at="2026-09-24T10:01:00Z",
        exit_code=0,
        complete=True,
        sidecar_revision="sidecar-1",
        prompt="Review the task path.",
        prompt_hash="sha256:prompt",
        oracle={
            "case_id": "001-create-task",
            "path": "oracles/001-create-task.json",
            "sha256": "sha256:oracle",
            "status": "available",
        },
        controlled_variation={
            "label": "with-check-docs",
            "prompt_hash": "sha256:prompt",
            "status": "declared",
            "task_hash": "sha256:abc",
        },
    )

    assert RunManifest.from_dict(manifest.to_dict()) == manifest


def test_build_run_provenance_captures_prompt_oracle_and_variation(
    tmp_path,
) -> None:
    evaluator_root = tmp_path / "evaluator"
    oracle_path = evaluator_root / "oracles" / "case.json"
    oracle_path.parent.mkdir(parents=True)
    oracle_path.write_text(json.dumps({"case_id": "case-1"}), encoding="utf-8")

    provenance = build_run_provenance(
        prompt="Review the task path.",
        oracle_path=oracle_path,
        evaluator_root=evaluator_root,
        variation="with-check-docs",
        task_hash="sha256:task",
    )

    assert provenance["prompt"] == "Review the task path."
    assert provenance["prompt_hash"] == (
        "sha256:"
        + hashlib.sha256("Review the task path.".encode("utf-8")).hexdigest()
    )
    assert provenance["oracle"] == {
        "case_id": "case-1",
        "path": "oracles/case.json",
        "sha256": "sha256:"
        + hashlib.sha256(oracle_path.read_bytes()).hexdigest(),
        "status": "available",
    }
    assert provenance["controlled_variation"] == {
        "label": "with-check-docs",
        "prompt_hash": provenance["prompt_hash"],
        "status": "declared",
        "task_hash": "sha256:task",
    }


def test_manifest_rejects_missing_provenance() -> None:
    with pytest.raises(ValueError, match="sidecar_revision"):
        RunManifest.from_dict({"run_id": "run-1"})


def test_manifest_reads_old_bundle_as_legacy_without_inventing_provenance() -> None:
    legacy = RunManifest.from_dict(
        {
            "run_id": "run-legacy",
            "case_id": "case-1",
            "repo_revision": "target-1",
            "runtime_revision": "runtime-1",
            "task_hash": "sha256:task",
            "model": "model-1",
            "codex_version": "codex-1",
            "observer_version": "0.4.0",
            "launch_mode": "host-runtime-pty",
            "sandbox": "read-only",
            "ephemeral": True,
            "started_at": "2026-09-24T10:00:00Z",
            "finished_at": "2026-09-24T10:01:00Z",
            "exit_code": 0,
            "complete": True,
            "sidecar_revision": "sidecar-1",
        }
    )

    assert legacy.provenance_status == "legacy"
    assert legacy.prompt is None
    assert legacy.oracle is None
    assert legacy.controlled_variation is None
