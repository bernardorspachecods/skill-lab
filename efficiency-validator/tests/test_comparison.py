import hashlib

from efficiency_validator.comparison import aggregate_comparisons, compare_runs


def _manifest(run_id: str, *, variation: str) -> dict[str, object]:
    return {
        "run_id": run_id,
        "case_id": "case-1",
        "task_hash": "task-1",
        "repo_revision": "target-1",
        "runtime_revision": "runtime-1",
        "model": "model-1",
        "codex_version": "codex-1",
        "observer_version": "observer-1",
        "sandbox": "read-only",
        "sidecar_revision": "sidecar-1",
        "variation": variation,
        "prompt": "Review the task.",
        "prompt_hash": "hash:prompt",
        "oracle": {
            "case_id": "case-1",
            "path": "oracles/case.json",
            "sha256": "sha256:oracle",
            "status": "available",
        },
        "controlled_variation": {
            "label": variation,
            "prompt_hash": "hash:prompt",
            "status": "declared",
            "task_hash": "task-1",
        },
        "provenance_status": "complete",
    }


def _report(
    run_id: str,
    *,
    variation: str,
    tokens: int = 100,
    commands: int = 2,
    filesystem_events: int | None = None,
    prompt: str = "Review the task.",
) -> dict[str, object]:
    filesystem_status = "available" if filesystem_events is not None else "unavailable"
    return {
        "status": "complete",
        "manifest": {
            **_manifest(run_id, variation=variation),
            "prompt": prompt,
            "prompt_hash": f"sha256:{hashlib.sha256(prompt.encode()).hexdigest()}",
            "controlled_variation": {
                "label": variation,
                "prompt_hash": f"sha256:{hashlib.sha256(prompt.encode()).hexdigest()}",
                "status": "declared",
                "task_hash": "task-1",
            },
        },
        "parser": {"complete": True, "issues": []},
        "command_trace": {
            "command_count": commands,
            "final_agent_message": "answer",
        },
        "observability": {
            "tokens": {
                "status": "available",
                "totals": {"total_tokens": tokens},
            },
            "filesystem": {
                "status": filesystem_status,
                "events": [{}] * (filesystem_events or 0),
            },
        },
    }


def _quality(status: str = "pass") -> dict[str, object]:
    return {"schema_version": "quality-report-1", "quality": {"status": status}}


def _config() -> dict[str, object]:
    return {
        "baseline_variation": "without-skill",
        "candidate_variation": "with-skill",
        "primary_metric": "tokens",
        "relative_tolerance": 0.05,
    }


def test_comparison_reports_better_when_quality_holds_and_primary_cost_drops() -> None:
    result = compare_runs(
        _report("base", variation="without-skill", tokens=100),
        _report("candidate", variation="with-skill", tokens=80),
        _quality(),
        _quality(),
        _config(),
    )

    assert result.verdict == "better"
    assert result.pair.valid is True
    assert result.deltas["tokens"].absolute == -20


def test_comparison_reports_same_within_tolerance() -> None:
    config = _config()
    config["relative_tolerance"] = 0.10
    result = compare_runs(
        _report("base", variation="without-skill", tokens=100),
        _report("candidate", variation="with-skill", tokens=105),
        _quality(),
        _quality(),
        config,
    )

    assert result.verdict == "same"


def test_comparison_reports_worse_for_quality_failure() -> None:
    result = compare_runs(
        _report("base", variation="without-skill"),
        _report("candidate", variation="with-skill", tokens=50),
        _quality(),
        _quality("fail"),
        _config(),
    )

    assert result.verdict == "worse"
    assert "candidate_quality_failed" in result.reasons


def test_comparison_reports_tradeoff_for_primary_gain_and_secondary_regression() -> None:
    result = compare_runs(
        _report("base", variation="without-skill", tokens=100, commands=2),
        _report(
            "candidate",
            variation="with-skill",
            tokens=80,
            commands=4,
        ),
        _quality(),
        _quality(),
        _config(),
    )

    assert result.verdict == "tradeoff"
    assert "commands_increased" in result.reasons


def test_comparison_is_inconclusive_for_invalid_pair_or_missing_primary_cost() -> None:
    invalid = compare_runs(
        _report("base", variation="without-skill"),
        _report("candidate", variation="wrong-variation"),
        _quality(),
        _quality(),
        _config(),
    )
    missing = compare_runs(
        _report("base", variation="without-skill"),
        {**_report("candidate", variation="with-skill"),
         "observability": {"tokens": {"status": "unavailable", "totals": None}}},
        _quality(),
        _quality(),
        _config(),
    )

    assert invalid.verdict == "inconclusive"
    assert missing.verdict == "inconclusive"


def test_comparison_exposes_complete_prompt_diff() -> None:
    result = compare_runs(
        _report(
            "base",
            variation="without-skill",
            prompt="Read the task.\nReport the answer.",
        ),
        _report(
            "candidate",
            variation="with-skill",
            prompt="Read the docs first.\nRead the task.\nReport the answer.",
        ),
        _quality(),
        _quality(),
        _config(),
    )

    assert result.prompt_diff["same_exact_prompt"] is False
    assert result.prompt_diff["baseline_prompt"] == (
        "Read the task.\nReport the answer."
    )
    assert "+Read the docs first." in result.prompt_diff["unified_diff"]


def test_file_read_verdict_requires_valid_exact_read_evidence() -> None:
    baseline = _report("base", variation="without-skill")
    candidate = _report("candidate", variation="with-skill")
    for report in (baseline, candidate):
        report["manifest"]["exact_read_required"] = True
        report["observability"]["exact_read"] = {
            "status": "partial",
            "valid": False,
            "total_bytes": 10,
            "total_lines": 1,
        }
    config = _config()
    config["require_exact_read"] = True
    config["primary_metric"] = "exact_read_lines"

    result = compare_runs(
        baseline,
        candidate,
        _quality(),
        _quality(),
        config,
    )

    assert result.verdict == "inconclusive"
    assert result.evidence_status == "blocked"
    assert "baseline_exact_read_incomplete" in result.reasons


def test_file_read_verdict_requires_process_tree_coverage() -> None:
    baseline = _report("base", variation="without-skill")
    candidate = _report("candidate", variation="with-skill")
    for report in (baseline, candidate):
        report["observability"]["exact_read"] = {
            "status": "available",
            "valid": True,
            "process_tree_covered": False,
            "total_bytes": 10,
            "total_lines": 1,
        }
    config = _config()
    config["require_exact_read"] = True
    config["primary_metric"] = "exact_read_lines"

    result = compare_runs(
        baseline,
        candidate,
        _quality(),
        _quality(),
        config,
    )

    assert result.verdict == "inconclusive"
    assert result.evidence_status == "blocked"
    assert "candidate_exact_read_incomplete" in result.reasons
    assert "candidate_exact_read_incomplete" in result.reasons


def test_comparison_rejects_legacy_provenance() -> None:
    baseline = _report("base", variation="without-skill")
    baseline["manifest"] = {
        key: value
        for key, value in baseline["manifest"].items()
        if key not in {"provenance_status", "oracle", "controlled_variation"}
    }

    result = compare_runs(
        baseline,
        _report("candidate", variation="with-skill"),
        _quality(),
        _quality(),
        _config(),
    )

    assert result.verdict == "inconclusive"
    assert result.evidence_status == "blocked"
    assert "baseline_provenance_incomplete" in result.pair.reasons


def test_comparison_rejects_baseline_intervention_marker() -> None:
    baseline = _report("base", variation="without-skill")
    baseline["observability"] = {
        "raw_events": [
            {
                "event_type": "item.completed",
                "payload": {"item": {"text": "I used $check-docs."}},
            }
        ],
        "tokens": {
            "status": "available",
            "totals": {"total_tokens": 100},
        },
        "filesystem": {"status": "unavailable", "events": []},
    }
    config = _config()
    config["baseline_forbidden_markers"] = ["$check-docs"]

    result = compare_runs(
        baseline,
        _report("candidate", variation="with-skill"),
        _quality(),
        _quality(),
        config,
    )

    assert result.verdict == "inconclusive"
    assert "baseline_intervention_marker_detected" in result.pair.reasons


def test_aggregate_mixed_pairs_is_inconclusive() -> None:
    better = compare_runs(
        _report("base-1", variation="without-skill", tokens=100),
        _report("candidate-1", variation="with-skill", tokens=80),
        _quality(),
        _quality(),
        _config(),
    ).to_dict()
    worse = compare_runs(
        _report("base-2", variation="without-skill", tokens=100),
        _report("candidate-2", variation="with-skill", tokens=120),
        _quality(),
        _quality(),
        _config(),
    ).to_dict()

    aggregate = aggregate_comparisons([better, worse])

    assert aggregate["verdict"] == "inconclusive"
    assert aggregate["evidence_status"] == "exploratory"
    assert aggregate["verdict_counts"] == {"better": 1, "worse": 1}
