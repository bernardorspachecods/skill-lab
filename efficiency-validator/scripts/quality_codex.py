#!/usr/bin/env python3
"""Apply the deterministic quality gate to one captured report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from efficiency_validator.quality import evaluate_quality
except ModuleNotFoundError:  # direct execution from the repository checkout
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from efficiency_validator.quality import evaluate_quality


def generate_quality_report(
    report_path: Path,
    oracle_path: Path,
    review_path: Path | None,
) -> dict[str, object]:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    review = (
        None
        if review_path is None
        else json.loads(review_path.read_text(encoding="utf-8"))
    )
    result = evaluate_quality(report, oracle, review)
    manifest = report.get("manifest", {})
    return {
        "schema_version": "quality-report-1",
        "run_id": manifest.get("run_id") if isinstance(manifest, dict) else None,
        "case_id": manifest.get("case_id") if isinstance(manifest, dict) else None,
        "quality": result.to_dict(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--review", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = generate_quality_report(args.report, args.oracle, args.review)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps(result["quality"], sort_keys=True))
    return 0 if result["quality"]["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
