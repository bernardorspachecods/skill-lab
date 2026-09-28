import json
from pathlib import Path

import pytest

from efficiency_validator.operational import capture
from efficiency_validator.operational_analysis import compare, save_comparison


def _cli(tmp_path: Path, value: str) -> str:
    import sys
    path = tmp_path / f"cli-{value}"
    path.write_text(f"#!{sys.executable}\nimport json\nprint(json.dumps({{'type':'turn.started'}}))\nprint(json.dumps({{'type':'turn.completed','usage':{{'input_tokens':10,'cached_input_tokens':0,'cache_write_input_tokens':0,'output_tokens':2,'reasoning_output_tokens':0}}}}))\n")
    path.chmod(0o700)
    return str(path)


def _bundle(tmp_path: Path, name: str, variant: str, *, failed=False) -> Path:
    source = tmp_path / f"source-{name}"
    source.mkdir()
    path = Path(_cli(tmp_path, name))
    bundle = tmp_path / name
    checks = [["python3", "-c", "raise SystemExit(1)" if failed else "pass"]]
    capture(source, bundle, prompt="same", variant=variant, codex=path, checks=checks)
    from efficiency_validator.operational_report import save_report
    save_report(bundle)
    return bundle


def test_compare_reports_deltas_and_exploratory_scope(tmp_path):
    baseline = _bundle(tmp_path, "base", "base")
    candidate = _bundle(tmp_path, "candidate", "context")
    result = compare(baseline, candidate)
    assert result["verdict"] == "exploratory"
    assert result["evidence_status"] == "exploratory"
    assert result["metrics"]["total_tokens"]["delta"] == 0
    assert "observed CLI tool inputs/results" in result["interpretation"]["reading_scope"]


def test_quality_failure_blocks_comparison(tmp_path):
    baseline = _bundle(tmp_path, "base", "base")
    candidate = _bundle(tmp_path, "candidate", "context", failed=True)
    result = compare(baseline, candidate)
    assert result["verdict"] == "inconclusive"
    assert result["evidence_status"] == "blocked"
    assert "candidate evaluator checks did not pass" in result["reasons"]


def test_mismatched_prompt_blocks_pair(tmp_path):
    baseline = _bundle(tmp_path, "base", "base")
    source = tmp_path / "other-source"
    source.mkdir()
    candidate = tmp_path / "candidate"
    capture(source, candidate, prompt="different", variant="context", codex=_cli(tmp_path, "other"))
    from efficiency_validator.operational_report import save_report
    save_report(candidate)
    result = compare(baseline, candidate)
    assert result["evidence_status"] == "blocked"
    assert "prompt differs" in result["reasons"]


def test_comparison_is_regenerable(tmp_path):
    baseline = _bundle(tmp_path, "base", "base")
    candidate = _bundle(tmp_path, "candidate", "context")
    output = tmp_path / "comparison"
    first = save_comparison(baseline, candidate, output)
    second = json.loads((output / "comparison.json").read_text())
    assert second["schema"] == "operational-comparison-1"
    assert second["metrics"] == first["metrics"]
