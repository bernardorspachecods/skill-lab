#!/usr/bin/env python3
"""Render compact human and machine decision reports from saved artefacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from efficiency_validator.decision_report import (
        build_decision_report,
        render_markdown,
    )
except ModuleNotFoundError:  # direct execution from the repository checkout
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from efficiency_validator.decision_report import (
        build_decision_report,
        render_markdown,
    )


def generate_decision_report(
    run_specs: list[str],
    quality_specs: list[str],
    comparison_paths: list[Path],
    aggregate_path: Path | None,
) -> dict[str, object]:
    qualities = dict(_parse_specs(quality_specs, "quality"))
    runs: list[dict[str, object]] = []
    for label, path_text in _parse_specs(run_specs, "run"):
        path = Path(path_text)
        item: dict[str, object] = {
            "label": label,
            "report_path": path_text,
            "report": _read_json(path),
        }
        quality_path = qualities.get(label)
        if quality_path:
            item["quality_path"] = quality_path
            item["quality"] = _read_json(Path(quality_path))
        runs.append(item)
    comparisons = [_read_json(path) for path in comparison_paths]
    aggregate = (
        _read_json(aggregate_path) if aggregate_path is not None else None
    )
    return build_decision_report(
        runs,
        comparisons=comparisons,
        aggregate=aggregate,
        comparison_paths=[str(path) for path in comparison_paths],
        aggregate_path=str(aggregate_path) if aggregate_path else None,
    )


def _parse_specs(specs: list[str], kind: str) -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for spec in specs:
        if "=" not in spec:
            raise ValueError(f"{kind} must use LABEL=PATH: {spec!r}")
        label, path = spec.split("=", 1)
        if not label or not path:
            raise ValueError(f"{kind} must use LABEL=PATH: {spec!r}")
        parsed.append((label, path))
    return parsed


def _read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run",
        action="append",
        required=True,
        metavar="LABEL=REPORT.json",
        help="Saved run report, repeat for baseline/candidate or more runs",
    )
    parser.add_argument(
        "--quality",
        action="append",
        default=[],
        metavar="LABEL=QUALITY.json",
        help="Optional quality report associated with a run label",
    )
    parser.add_argument(
        "--comparison",
        action="append",
        default=[],
        type=Path,
        help="Saved pair comparison report; repeat for each replicate",
    )
    parser.add_argument("--aggregate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Optional compact JSON output; defaults beside --output",
    )
    args = parser.parse_args()

    summary = generate_decision_report(
        args.run,
        args.quality,
        args.comparison,
        args.aggregate,
    )
    json_output = args.json_output or args.output.with_suffix(".json")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown(summary), encoding="utf-8")
    json_output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary["decision"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
