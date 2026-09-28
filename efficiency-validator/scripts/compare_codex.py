#!/usr/bin/env python3
"""Compare two quality-gated Codex run reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from efficiency_validator.comparison import compare_runs
except ModuleNotFoundError:  # direct execution from the repository checkout
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from efficiency_validator.comparison import compare_runs


def generate_comparison_report(
    baseline_report_path: Path,
    candidate_report_path: Path,
    baseline_quality_path: Path,
    candidate_quality_path: Path,
    config_path: Path,
) -> dict[str, object]:
    baseline_report = json.loads(baseline_report_path.read_text(encoding="utf-8"))
    candidate_report = json.loads(candidate_report_path.read_text(encoding="utf-8"))
    baseline_quality = json.loads(
        baseline_quality_path.read_text(encoding="utf-8")
    )
    candidate_quality = json.loads(
        candidate_quality_path.read_text(encoding="utf-8")
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    result = compare_runs(
        baseline_report,
        candidate_report,
        baseline_quality,
        candidate_quality,
        config,
    )
    return {
        "schema_version": "comparison-report-1",
        "baseline_run_id": _run_id(baseline_report),
        "candidate_run_id": _run_id(candidate_report),
        "comparison": result.to_dict(),
    }


def _run_id(report: dict[str, object]) -> object:
    manifest = report.get("manifest")
    return manifest.get("run_id") if isinstance(manifest, dict) else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-report", type=Path, required=True)
    parser.add_argument("--candidate-report", type=Path, required=True)
    parser.add_argument("--baseline-quality", type=Path, required=True)
    parser.add_argument("--candidate-quality", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = generate_comparison_report(
        args.baseline_report,
        args.candidate_report,
        args.baseline_quality,
        args.candidate_quality,
        args.config,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    comparison = result["comparison"]
    print(json.dumps(comparison, sort_keys=True))
    return 0 if comparison["verdict"] != "inconclusive" else 1


if __name__ == "__main__":
    raise SystemExit(main())
