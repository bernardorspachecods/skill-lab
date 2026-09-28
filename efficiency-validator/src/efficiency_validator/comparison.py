"""Quality-gated comparison of two captured Codex runs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import difflib
import hashlib
import json
import statistics
from typing import Literal


MetricStatus = Literal["available", "unavailable"]
Verdict = Literal["better", "same", "worse", "tradeoff", "inconclusive"]
EvidenceStatus = Literal["blocked", "exploratory", "supported"]


@dataclass(frozen=True)
class MetricMeasurement:
    value: float | None
    unit: str
    status: MetricStatus
    source: str


@dataclass(frozen=True)
class MetricPair:
    baseline: MetricMeasurement
    candidate: MetricMeasurement


@dataclass(frozen=True)
class MetricDelta:
    baseline: MetricMeasurement
    candidate: MetricMeasurement
    absolute: float | None
    relative: float | None
    within_tolerance: bool | None


@dataclass(frozen=True)
class PairValidation:
    valid: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class ComparisonResult:
    verdict: Verdict
    pair: PairValidation
    quality: dict[str, str]
    metrics: dict[str, MetricPair]
    deltas: dict[str, MetricDelta]
    reasons: tuple[str, ...]
    primary_metric: str
    prompt_diff: dict[str, object]
    evidence_status: EvidenceStatus

    def to_dict(self) -> dict[str, object]:
        return {
            "verdict": self.verdict,
            "pair": asdict(self.pair),
            "quality": self.quality,
            "metrics": {
                name: asdict(pair) for name, pair in self.metrics.items()
            },
            "deltas": {
                name: asdict(delta) for name, delta in self.deltas.items()
            },
            "reasons": list(self.reasons),
            "primary_metric": self.primary_metric,
            "prompt_diff": self.prompt_diff,
            "evidence_status": self.evidence_status,
        }


def compare_runs(
    baseline_report: dict[str, object],
    candidate_report: dict[str, object],
    baseline_quality: dict[str, object],
    candidate_quality: dict[str, object],
    config: dict[str, object],
) -> ComparisonResult:
    """Compare two reports after validating identity and quality gates."""

    primary_metric = _config_string(config, "primary_metric", "tokens")
    tolerance = _config_float(config, "relative_tolerance", 0.05)
    pair = _validate_pair(baseline_report, candidate_report, config)
    prompt_diff = _prompt_diff(baseline_report, candidate_report)
    metrics = _extract_metrics(baseline_report, candidate_report)
    deltas = _calculate_deltas(metrics, tolerance)
    quality = {
        "baseline": _quality_status(baseline_quality),
        "candidate": _quality_status(candidate_quality),
    }

    reasons = list(pair.reasons)
    if not pair.valid:
        return _result(
            "inconclusive", pair, quality, metrics, deltas, reasons,
            primary_metric, prompt_diff, "blocked"
        )

    if quality["baseline"] != "pass":
        reasons.append("baseline_quality_not_passed")
        return _result(
            "inconclusive", pair, quality, metrics, deltas, reasons,
            primary_metric, prompt_diff, "blocked"
        )
    if quality["candidate"] == "fail":
        reasons.append("candidate_quality_failed")
        return _result(
            "worse", pair, quality, metrics, deltas, reasons,
            primary_metric, prompt_diff, "blocked"
        )
    if quality["candidate"] != "pass":
        reasons.append("candidate_quality_indeterminate")
        return _result(
            "inconclusive", pair, quality, metrics, deltas, reasons,
            primary_metric, prompt_diff, "blocked"
        )

    primary = deltas.get(primary_metric)
    if primary is None or primary.within_tolerance is None:
        reasons.append("primary_metric_unavailable")
        return _result(
            "inconclusive", pair, quality, metrics, deltas, reasons,
            primary_metric, prompt_diff, "blocked"
        )

    regressions = _regressions(deltas, primary_metric)
    improvements = _improvements(deltas, primary_metric)
    reasons.extend(regressions)
    if primary.within_tolerance is False and primary.absolute is not None:
        if primary.absolute < 0:
            if regressions:
                verdict: Verdict = "tradeoff"
                reasons.append("primary_improved_with_secondary_regression")
            else:
                verdict = "better"
                reasons.append("primary_metric_decreased")
        else:
            verdict = "worse"
            reasons.append("primary_metric_increased")
    else:
        verdict = "same"
        if improvements:
            reasons.append("secondary_metric_improved")
        reasons.append("costs_within_tolerance")
    return _result(
        verdict, pair, quality, metrics, deltas, reasons,
        primary_metric, prompt_diff, "exploratory"
    )


def _result(
    verdict: Verdict,
    pair: PairValidation,
    quality: dict[str, str],
    metrics: dict[str, MetricPair],
    deltas: dict[str, MetricDelta],
    reasons: list[str],
    primary_metric: str,
    prompt_diff: dict[str, object],
    evidence_status: EvidenceStatus,
) -> ComparisonResult:
    return ComparisonResult(
        verdict=verdict,
        pair=pair,
        quality=quality,
        metrics=metrics,
        deltas=deltas,
        reasons=tuple(dict.fromkeys(reasons)),
        primary_metric=primary_metric,
        prompt_diff=prompt_diff,
        evidence_status=evidence_status,
    )


def _prompt_diff(
    baseline: dict[str, object], candidate: dict[str, object]
) -> dict[str, object]:
    baseline_manifest = _manifest(baseline)
    candidate_manifest = _manifest(candidate)
    baseline_prompt = baseline_manifest.get("prompt")
    candidate_prompt = candidate_manifest.get("prompt")
    result: dict[str, object] = {
        "status": "available"
        if isinstance(baseline_prompt, str) and isinstance(candidate_prompt, str)
        else "unavailable",
        "baseline_prompt": baseline_prompt,
        "candidate_prompt": candidate_prompt,
        "baseline_prompt_hash": baseline_manifest.get("prompt_hash"),
        "candidate_prompt_hash": candidate_manifest.get("prompt_hash"),
        "same_exact_prompt": (
            baseline_prompt == candidate_prompt
            if isinstance(baseline_prompt, str)
            and isinstance(candidate_prompt, str)
            else None
        ),
    }
    if isinstance(baseline_prompt, str) and isinstance(candidate_prompt, str):
        result["unified_diff"] = "".join(
            difflib.unified_diff(
                baseline_prompt.splitlines(keepends=True),
                candidate_prompt.splitlines(keepends=True),
                fromfile="baseline.prompt",
                tofile="candidate.prompt",
            )
        )
    else:
        result["unified_diff"] = None
    return result


def _validate_pair(
    baseline: dict[str, object],
    candidate: dict[str, object],
    config: dict[str, object],
) -> PairValidation:
    baseline_manifest = _manifest(baseline)
    candidate_manifest = _manifest(candidate)
    reasons: list[str] = []
    for field in (
        "case_id",
        "task_hash",
        "repo_revision",
        "runtime_revision",
        "model",
        "codex_version",
        "observer_version",
        "sandbox",
        "sidecar_revision",
    ):
        if baseline_manifest.get(field) != candidate_manifest.get(field):
            reasons.append(f"pair_{field}_mismatch")

    reasons.extend(_provenance_reasons(baseline_manifest, "baseline"))
    reasons.extend(_provenance_reasons(candidate_manifest, "candidate"))
    if baseline_manifest.get("oracle") != candidate_manifest.get("oracle"):
        reasons.append("pair_oracle_mismatch")

    primary_metric = _config_string(config, "primary_metric", "tokens")
    require_exact_read = bool(config.get("require_exact_read")) or primary_metric in {
        "exact_read_bytes",
        "exact_read_lines",
        "file_read_bytes",
        "file_read_lines",
    }
    if require_exact_read:
        for side, report in (("baseline", baseline), ("candidate", candidate)):
            exact_read = _observability_value(report, "exact_read")
            if (
                not isinstance(exact_read, dict)
                or exact_read.get("valid") is not True
                or exact_read.get("process_tree_covered") is not True
            ):
                reasons.append(f"{side}_exact_read_incomplete")

    baseline_text = json.dumps(baseline, sort_keys=True, ensure_ascii=False)
    for marker in _config_strings(config, "baseline_forbidden_markers"):
        if marker.lower() in baseline_text.lower():
            reasons.append("baseline_intervention_marker_detected")
            break

    baseline_variation = _config_string(config, "baseline_variation", "")
    candidate_variation = _config_string(config, "candidate_variation", "")
    if not baseline_variation or not candidate_variation:
        reasons.append("variation_not_declared")
    else:
        if baseline_manifest.get("variation") != baseline_variation:
            reasons.append("baseline_variation_mismatch")
        if candidate_manifest.get("variation") != candidate_variation:
            reasons.append("candidate_variation_mismatch")
        if baseline_variation == candidate_variation:
            reasons.append("variation_not_distinct")
    return PairValidation(valid=not reasons, reasons=tuple(dict.fromkeys(reasons)))


def _provenance_reasons(
    manifest: dict[str, object], side: str
) -> list[str]:
    reasons: list[str] = []
    if manifest.get("provenance_status") != "complete":
        reasons.append(f"{side}_provenance_incomplete")

    prompt = manifest.get("prompt")
    prompt_hash = manifest.get("prompt_hash")
    expected_prompt_hash = (
        f"sha256:{hashlib.sha256(prompt.encode('utf-8')).hexdigest()}"
        if isinstance(prompt, str)
        else None
    )
    if not isinstance(prompt, str) or not isinstance(prompt_hash, str):
        reasons.append(f"{side}_prompt_provenance_missing")
    elif prompt_hash != expected_prompt_hash:
        reasons.append(f"{side}_prompt_hash_mismatch")

    oracle = manifest.get("oracle")
    if (
        not isinstance(oracle, dict)
        or oracle.get("status") != "available"
        or not isinstance(oracle.get("sha256"), str)
        or not isinstance(oracle.get("path"), str)
    ):
        reasons.append(f"{side}_oracle_provenance_missing")

    variation = manifest.get("controlled_variation")
    if (
        not isinstance(variation, dict)
        or variation.get("status") != "declared"
        or variation.get("label") != manifest.get("variation")
        or variation.get("task_hash") != manifest.get("task_hash")
        or variation.get("prompt_hash") != manifest.get("prompt_hash")
    ):
        reasons.append(f"{side}_controlled_variation_invalid")
    return reasons


def _extract_metrics(
    baseline: dict[str, object], candidate: dict[str, object]
) -> dict[str, MetricMeasurement]:
    return {
        "tokens": _metric_pair(
            baseline,
            candidate,
            path=("observability", "tokens", "totals", "total_tokens"),
            status_path=("observability", "tokens", "status"),
            unit="tokens",
            source="codex-exec-json",
        ),
        "commands": _metric_pair(
            baseline,
            candidate,
            path=("command_trace", "command_count"),
            status_path=("status",),
            unit="commands",
            source="command-report",
        ),
        "filesystem_events": _metric_pair(
            baseline,
            candidate,
            path=("observability", "filesystem", "events"),
            status_path=("observability", "filesystem", "status"),
            unit="events",
            source="filesystem-sidecar",
        ),
        "exact_read_bytes": _metric_pair(
            baseline,
            candidate,
            path=("observability", "exact_read", "total_bytes"),
            status_path=("observability", "exact_read", "status"),
            unit="bytes",
            source="exact-read-1",
        ),
        "exact_read_lines": _metric_pair(
            baseline,
            candidate,
            path=("observability", "exact_read", "total_lines"),
            status_path=("observability", "exact_read", "status"),
            unit="lines",
            source="exact-read-1",
        ),
    }


def _metric_pair(
    baseline: dict[str, object],
    candidate: dict[str, object],
    *,
    path: tuple[str, ...],
    status_path: tuple[str, ...],
    unit: str,
    source: str,
) -> MetricPair:
    baseline_value, baseline_status = _metric_value(baseline, path, status_path)
    candidate_value, candidate_status = _metric_value(candidate, path, status_path)
    return MetricPair(
        baseline=MetricMeasurement(
            value=baseline_value,
            unit=unit,
            status=baseline_status,
            source=source,
        ),
        candidate=MetricMeasurement(
            value=candidate_value,
            unit=unit,
            status=candidate_status,
            source=source,
        ),
    )


def _calculate_deltas(
    metrics: dict[str, MetricPair], tolerance: float
) -> dict[str, MetricDelta]:
    deltas: dict[str, MetricDelta] = {}
    for name, pair in metrics.items():
        baseline = pair.baseline
        candidate = pair.candidate
        if (
            baseline.status != "available"
            or candidate.status != "available"
            or baseline.value is None
            or candidate.value is None
        ):
            deltas[name] = MetricDelta(baseline, candidate, None, None, None)
            continue
        absolute = candidate.value - baseline.value
        relative = None if baseline.value == 0 else absolute / baseline.value
        within = abs(relative) <= tolerance if relative is not None else absolute == 0
        deltas[name] = MetricDelta(baseline, candidate, absolute, relative, within)
    return deltas


def _regressions(
    deltas: dict[str, MetricDelta], primary_metric: str
) -> list[str]:
    return [
        f"{name}_increased"
        for name, delta in deltas.items()
        if name != primary_metric and delta.absolute is not None and delta.within_tolerance is False and delta.absolute > 0
    ]


def _improvements(
    deltas: dict[str, MetricDelta], primary_metric: str
) -> list[str]:
    return [
        f"{name}_decreased"
        for name, delta in deltas.items()
        if name != primary_metric and delta.absolute is not None and delta.within_tolerance is False and delta.absolute < 0
    ]


def _metric_value(
    report: dict[str, object],
    path: tuple[str, ...],
    status_path: tuple[str, ...],
) -> tuple[float | None, MetricStatus]:
    value: object = report
    for part in path:
        if not isinstance(value, dict):
            return None, "unavailable"
        value = value.get(part)
    status_value: object = report
    for part in status_path:
        if not isinstance(status_value, dict):
            return None, "unavailable"
        status_value = status_value.get(part)
    if path[-1] == "events":
        if status_value != "available" or not isinstance(value, list):
            return None, "unavailable"
        return float(len(value)), "available"
    if status_value not in {"available", "complete"} or not isinstance(value, (int, float)):
        return None, "unavailable"
    return float(value), "available"


def _manifest(report: dict[str, object]) -> dict[str, object]:
    value = report.get("manifest")
    return value if isinstance(value, dict) else {}


def _observability_value(report: dict[str, object], name: str) -> object:
    observability = report.get("observability")
    if not isinstance(observability, dict):
        return None
    return observability.get(name)


def _quality_status(report: dict[str, object]) -> str:
    value = report.get("quality")
    if not isinstance(value, dict):
        return "indeterminate"
    status = value.get("status")
    return status if status in {"pass", "fail", "indeterminate"} else "indeterminate"


def _config_string(config: dict[str, object], name: str, default: str) -> str:
    value = config.get(name, default)
    return value if isinstance(value, str) else default


def _config_float(config: dict[str, object], name: str, default: float) -> float:
    value = config.get(name, default)
    return float(value) if isinstance(value, (int, float)) else default


def _config_strings(config: dict[str, object], name: str) -> tuple[str, ...]:
    value = config.get(name, [])
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)


def aggregate_comparisons(
    comparisons: list[dict[str, object]],
    *,
    minimum_supported_replicates: int = 3,
) -> dict[str, object]:
    """Aggregate pair reports without hiding disagreement or weak evidence."""

    normalized = [
        value.get("comparison", value)
        for value in comparisons
        if isinstance(value, dict)
    ]
    if not normalized:
        return {
            "schema_version": "aggregate-report-1",
            "verdict": "inconclusive",
            "evidence_status": "blocked",
            "reason_codes": ["no_comparisons"],
            "verdict_counts": {},
            "pair_count": 0,
        }

    counts: dict[str, int] = {}
    for value in normalized:
        verdict = str(value.get("verdict", "inconclusive"))
        counts[verdict] = counts.get(verdict, 0) + 1

    valid_evidence = all(
        isinstance(value.get("pair"), dict)
        and value["pair"].get("valid") is True
        and value.get("evidence_status") == "exploratory"
        and isinstance(value.get("quality"), dict)
        and value["quality"].get("baseline") == "pass"
        and value["quality"].get("candidate") == "pass"
        for value in normalized
    )
    reasons: list[str] = []
    if "better" in counts and "worse" in counts:
        reasons.extend(["mixed_pair_verdicts", "high_run_to_run_variance"])
    if any(verdict in counts for verdict in ("tradeoff", "inconclusive")):
        reasons.append("unsupported_or_nonuniform_pair")

    verdict: Verdict = "inconclusive"
    if len(counts) == 1 and valid_evidence:
        only_verdict = next(iter(counts))
        if only_verdict in {"better", "same", "worse"}:
            verdict = only_verdict  # type: ignore[assignment]

    evidence_status: EvidenceStatus = "exploratory"
    if not valid_evidence:
        evidence_status = "blocked"
    elif verdict != "inconclusive" and len(normalized) >= minimum_supported_replicates:
        evidence_status = "supported"

    aggregate: dict[str, object] = {
        "schema_version": "aggregate-report-1",
        "verdict": verdict,
        "evidence_status": evidence_status,
        "reason_codes": list(dict.fromkeys(reasons)),
        "verdict_counts": counts,
        "pair_count": len(normalized),
    }
    for metric in ("tokens", "commands", "filesystem_events"):
        values = [
            value.get("deltas", {}).get(metric, {}).get("absolute")
            for value in normalized
        ]
        numeric = [float(value) for value in values if isinstance(value, (int, float))]
        aggregate[f"{metric}_delta"] = (
            {
                "mean": statistics.mean(numeric),
                "median": statistics.median(numeric),
                "min": min(numeric),
                "max": max(numeric),
            }
            if numeric
            else {"status": "unavailable"}
        )
    return aggregate
