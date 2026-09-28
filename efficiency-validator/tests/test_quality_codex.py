import json
from pathlib import Path

from scripts.quality_codex import generate_quality_report


def test_quality_cli_adapter_emits_versioned_indeterminate_report(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "report.json"
    oracle_path = tmp_path / "oracle.json"
    report_path.write_text(
        json.dumps(
            {
                "status": "complete",
                "manifest": {"run_id": "run-1", "case_id": "case-1"},
                "parser": {"complete": True, "issues": []},
                "command_trace": {"final_agent_message": "answer"},
            }
        )
    )
    oracle_path.write_text(json.dumps({"required_claims": []}))

    result = generate_quality_report(report_path, oracle_path, None)

    assert result["schema_version"] == "quality-report-1"
    assert result["run_id"] == "run-1"
    assert result["quality"]["status"] == "indeterminate"
