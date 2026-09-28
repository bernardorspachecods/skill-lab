import json
from pathlib import Path

from scripts.compare_codex import generate_comparison_report


def test_comparison_cli_adapter_emits_versioned_report(tmp_path: Path) -> None:
    report = {
        "status": "complete",
        "manifest": {
            "run_id": "run-1",
            "case_id": "case-1",
            "task_hash": "task-1",
            "repo_revision": "target-1",
            "runtime_revision": "runtime-1",
            "model": "model-1",
            "codex_version": "codex-1",
            "observer_version": "observer-1",
            "sandbox": "read-only",
            "variation": "without-skill",
        },
        "parser": {"complete": True, "issues": []},
        "command_trace": {"command_count": 1},
        "observability": {
            "tokens": {"status": "available", "totals": {"total_tokens": 10}},
            "filesystem": {"status": "unavailable", "events": []},
        },
    }
    candidate = json.loads(json.dumps(report))
    candidate["manifest"]["run_id"] = "run-2"
    candidate["manifest"]["variation"] = "with-skill"
    candidate["observability"]["tokens"]["totals"]["total_tokens"] = 8
    quality = {"quality": {"status": "pass"}}
    config = {
        "baseline_variation": "without-skill",
        "candidate_variation": "with-skill",
        "primary_metric": "tokens",
    }
    paths = {
        "baseline": tmp_path / "baseline.json",
        "candidate": tmp_path / "candidate.json",
        "baseline_quality": tmp_path / "baseline-quality.json",
        "candidate_quality": tmp_path / "candidate-quality.json",
        "config": tmp_path / "config.json",
    }
    paths["baseline"].write_text(json.dumps(report))
    paths["candidate"].write_text(json.dumps(candidate))
    paths["baseline_quality"].write_text(json.dumps(quality))
    paths["candidate_quality"].write_text(json.dumps(quality))
    paths["config"].write_text(json.dumps(config))

    result = generate_comparison_report(
        paths["baseline"],
        paths["candidate"],
        paths["baseline_quality"],
        paths["candidate_quality"],
        paths["config"],
    )

    assert result["schema_version"] == "comparison-report-1"
    assert result["comparison"]["verdict"] == "inconclusive"
    assert result["comparison"]["evidence_status"] == "blocked"
