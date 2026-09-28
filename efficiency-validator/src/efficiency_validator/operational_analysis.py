"""Quality-aware comparison of operational-1 run bundles."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .operational_report import report


@dataclass(frozen=True)
class Metric:
    name: str
    baseline: float | None
    candidate: float | None
    delta: float | None
    relative: float | None
    lower_is_better: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline": self.baseline,
            "candidate": self.candidate,
            "delta": self.delta,
            "relative": self.relative,
            "status": "available" if self.baseline is not None and self.candidate is not None else "unavailable",
            "lower_is_better": self.lower_is_better,
        }


def _metric(name: str, baseline: Any, candidate: Any, lower_is_better: bool = True) -> Metric:
    left = float(baseline) if isinstance(baseline, (int, float)) and not isinstance(baseline, bool) else None
    right = float(candidate) if isinstance(candidate, (int, float)) and not isinstance(candidate, bool) else None
    delta = right - left if left is not None and right is not None else None
    relative = delta / left if delta is not None and left else None
    return Metric(name, left, right, delta, relative, lower_is_better)


def compare(baseline_bundle: Path, candidate_bundle: Path, *, tolerance: float = 0.05) -> dict[str, Any]:
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    baseline = report(baseline_bundle)
    candidate = report(candidate_bundle)
    bm, cm = baseline["manifest"], candidate["manifest"]
    reasons: list[str] = []
    for field, label in (("prompt_sha256", "prompt"), ("sandbox", "sandbox"),
                         ("model_requested", "requested model"), ("reasoning", "reasoning")):
        if bm.get(field) != cm.get(field):
            reasons.append(f"{label} differs")
    if bm.get("base_sha256") != cm.get("base_sha256"):
        reasons.append("starting target differs")
    if bm.get("input_sha256") == cm.get("input_sha256") and bm.get("overlay_paths") != cm.get("overlay_paths"):
        pass
    if baseline["execution_status"] != "completed":
        reasons.append("baseline execution is not completed")
    if candidate["execution_status"] != "completed":
        reasons.append("candidate execution is not completed")
    if baseline["collection_status"] != "available":
        reasons.append("baseline collection is incomplete")
    if candidate["collection_status"] != "available":
        reasons.append("candidate collection is incomplete")
    if baseline["quality"]["status"] != "pass":
        reasons.append("baseline evaluator checks did not pass")
    if candidate["quality"]["status"] != "pass":
        reasons.append("candidate evaluator checks did not pass")
    metrics = {
        "total_tokens": _metric("total_tokens", baseline["usage"]["total_tokens"], candidate["usage"]["total_tokens"]),
        "input_tokens": _metric("input_tokens", baseline["usage"]["input_tokens"], candidate["usage"]["input_tokens"]),
        "output_tokens": _metric("output_tokens", baseline["usage"]["output_tokens"], candidate["usage"]["output_tokens"]),
        "task_seconds": _metric("task_seconds", baseline["timing"]["task_seconds"], candidate["timing"]["task_seconds"]),
        "observed_commands": _metric("observed_commands", baseline["metrics"]["observed_commands"], candidate["metrics"]["observed_commands"]),
        "observed_tool_items": _metric("observed_tool_items", baseline["metrics"]["observed_tool_items"], candidate["metrics"]["observed_tool_items"]),
        "returned_command_output_bytes": _metric("returned_command_output_bytes", baseline["metrics"]["returned_command_output_bytes"], candidate["metrics"]["returned_command_output_bytes"]),
    }
    if reasons:
        verdict = "inconclusive"
        evidence_status = "blocked"
    else:
        verdict = "exploratory"
        evidence_status = "exploratory"
    available = [metric for metric in metrics.values() if metric.delta is not None]
    improvements = [metric.name for metric in available if metric.delta < 0 and metric.lower_is_better]
    regressions = [metric.name for metric in available if metric.delta > 0 and metric.lower_is_better]
    return {
        "schema": "operational-comparison-1",
        "evidence_status": evidence_status,
        "verdict": verdict,
        "reasons": reasons,
        "pair": {"baseline": str(baseline_bundle), "candidate": str(candidate_bundle),
                 "same_task_prompt": bm.get("prompt_sha256") == cm.get("prompt_sha256"),
                 "same_requested_model": bm.get("model_requested") == cm.get("model_requested"),
                 "same_sandbox": bm.get("sandbox") == cm.get("sandbox"),
                 "quality": {"baseline": baseline["quality"], "candidate": candidate["quality"]}},
        "metrics": {name: metric.to_dict() for name, metric in metrics.items()},
        "interpretation": {"lower_cost_metrics": improvements, "higher_cost_metrics": regressions,
                           "tolerance": tolerance,
                           "scope": "one completed pair; exploratory case observation, not a general improvement claim",
                           "quality_gate": "both explicit evaluator checks passed",
                           "reading_scope": "observed CLI tool inputs/results only; not complete filesystem reads"},
        "reports": {"baseline": baseline, "candidate": candidate},
    }


def save_comparison(baseline_bundle: Path, candidate_bundle: Path, output: Path, *, tolerance: float = 0.05) -> dict[str, Any]:
    result = compare(baseline_bundle, candidate_bundle, tolerance=tolerance)
    output.mkdir(parents=True, exist_ok=True)
    (output / "comparison.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    (output / "comparison.md").write_text(render_comparison(result))
    return result


def render_comparison(result: dict[str, Any]) -> str:
    pair = result["pair"]
    lines = ["# Operational comparison", "", f"Evidence status: **{result['evidence_status']}**",
             f"Verdict: **{result['verdict']}**", "", "## Pair", "",
             f"- Baseline: `{pair['baseline']}`", f"- Candidate: `{pair['candidate']}`",
             f"- Same prompt: `{pair['same_task_prompt']}`",
             f"- Same requested model: `{pair['same_requested_model']}`",
             f"- Same sandbox: `{pair['same_sandbox']}`", "",
             "## Metrics", "", "| Metric | Baseline | Candidate | Delta | Relative |", "| --- | ---: | ---: | ---: | ---: |"]
    for name, metric in result["metrics"].items():
        if metric["status"] == "available":
            relative = "unavailable" if metric["relative"] is None else f"{metric['relative']:.2%}"
            lines.append(f"| {name} | {metric['baseline']:.3f} | {metric['candidate']:.3f} | {metric['delta']:.3f} | {relative} |")
        else:
            lines.append(f"| {name} | unavailable | unavailable | unavailable | unavailable |")
    interpretation = result["interpretation"]
    lines.extend(["", "## Interpretation", "", f"- Lower-cost dimensions: {', '.join(interpretation['lower_cost_metrics']) or 'none'}",
                  f"- Higher-cost dimensions: {', '.join(interpretation['higher_cost_metrics']) or 'none'}",
                  f"- Quality gate: {interpretation['quality_gate']}",
                  f"- Reading scope: {interpretation['reading_scope']}",
                  f"- Scope: {interpretation['scope']}", "", "## Reasons", ""])
    lines.extend(["- " + reason for reason in result["reasons"]] or ["- none"])
    return "\n".join(lines) + "\n"
