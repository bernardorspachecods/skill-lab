import json
from pathlib import Path

from scripts.decision_report_codex import generate_decision_report


def test_cli_adapter_accepts_multiple_pairs_and_quality_files(
    tmp_path: Path,
) -> None:
    report = {
        "manifest": {
            "run_id": "run-1",
            "case_id": "case-1",
            "variation": "baseline",
            "prompt": "Do the task.",
        },
        "observability": {
            "tokens": {"totals": {"total_tokens": 10}},
            "filesystem": {"status": "unavailable", "events": []},
        },
        "command_trace": {"command_count": 1, "failed_command_count": 0},
    }
    quality = {"quality": {"status": "pass"}}
    comparison = {
        "comparison": {
            "verdict": "same",
            "evidence_status": "exploratory",
            "primary_metric": "tokens",
            "deltas": {},
        }
    }
    aggregate = {
        "verdict": "inconclusive",
        "evidence_status": "exploratory",
        "pair_count": 2,
        "verdict_counts": {"same": 2},
    }
    paths = {}
    for name, value in (
        ("report.json", report),
        ("quality.json", quality),
        ("comparison-1.json", comparison),
        ("comparison-2.json", comparison),
        ("aggregate.json", aggregate),
    ):
        path = tmp_path / name
        path.write_text(json.dumps(value), encoding="utf-8")
        paths[name] = path

    summary = generate_decision_report(
        [f"baseline={paths['report.json']}"],
        [f"baseline={paths['quality.json']}"],
        [paths["comparison-1.json"], paths["comparison-2.json"]],
        paths["aggregate.json"],
    )

    assert summary["decision"]["verdict"] == "inconclusive"
    assert len(summary["comparisons"]) == 2
    assert summary["runs"][0]["quality"]["status"] == "pass"
