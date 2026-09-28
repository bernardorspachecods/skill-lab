import json
from pathlib import Path

from scripts.aggregate_codex import generate_aggregate_report


def test_aggregate_cli_adapter_preserves_mixed_verdicts(tmp_path: Path) -> None:
    better = {
        "comparison": {
            "verdict": "better",
            "evidence_status": "exploratory",
            "pair": {"valid": True},
            "quality": {"baseline": "pass", "candidate": "pass"},
            "deltas": {"tokens": {"absolute": -10}},
        }
    }
    worse = {
        "comparison": {
            "verdict": "worse",
            "evidence_status": "exploratory",
            "pair": {"valid": True},
            "quality": {"baseline": "pass", "candidate": "pass"},
            "deltas": {"tokens": {"absolute": 20}},
        }
    }
    paths = []
    for index, payload in enumerate((better, worse), start=1):
        path = tmp_path / f"comparison-{index}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        paths.append(path)

    report = generate_aggregate_report(paths)

    assert report["schema_version"] == "aggregate-report-1"
    assert report["verdict"] == "inconclusive"
    assert report["verdict_counts"] == {"better": 1, "worse": 1}
    assert report["tokens_delta"]["median"] == 5.0
