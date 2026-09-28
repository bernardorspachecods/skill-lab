#!/usr/bin/env python3
"""Aggregate saved comparison reports without hiding disagreement."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from efficiency_validator.comparison import aggregate_comparisons
except ModuleNotFoundError:  # direct execution from the repository checkout
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from efficiency_validator.comparison import aggregate_comparisons


def generate_aggregate_report(
    comparison_paths: list[Path],
    *,
    minimum_supported_replicates: int = 3,
) -> dict[str, object]:
    comparisons = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in comparison_paths
    ]
    return aggregate_comparisons(
        comparisons,
        minimum_supported_replicates=minimum_supported_replicates,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--comparison",
        type=Path,
        action="append",
        required=True,
        help="Saved comparison report; repeat for each replicate",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--minimum-supported-replicates", type=int, default=3)
    args = parser.parse_args()

    report = generate_aggregate_report(
        args.comparison,
        minimum_supported_replicates=args.minimum_supported_replicates,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps(report, sort_keys=True))
    return 0 if report["verdict"] != "inconclusive" else 1


if __name__ == "__main__":
    raise SystemExit(main())
