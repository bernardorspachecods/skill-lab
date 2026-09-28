"""Human-facing decision reports over saved efficiency-validator artefacts."""

from __future__ import annotations

from collections import Counter
from typing import Iterable


def build_decision_report(
    runs: Iterable[dict[str, object]],
    *,
    comparison: dict[str, object] | None = None,
    comparisons: Iterable[dict[str, object]] | None = None,
    aggregate: dict[str, object] | None = None,
    comparison_path: str | None = None,
    comparison_paths: Iterable[str] | None = None,
    aggregate_path: str | None = None,
) -> dict[str, object]:
    summaries = [_summarize_run(run) for run in runs]
    comparison_values = list(comparisons or ())
    if comparison is not None:
        comparison_values.insert(0, comparison)
    comparison_summaries = [
        _summarize_comparison(value) for value in comparison_values
    ]
    comparison_summaries = [
        value for value in comparison_summaries if value is not None
    ]
    comparison_summary = comparison_summaries[0] if comparison_summaries else None
    aggregate_summary = _summarize_aggregate(aggregate)
    source = aggregate_summary or comparison_summary
    decision = _decision_summary(source)
    limitations = _limitations(
        summaries, comparison_summaries, aggregate_summary
    )
    artifacts = [
        artifact
        for run in runs
        for artifact in _run_artifacts(run)
    ]
    all_comparison_paths = list(comparison_paths or ())
    if comparison_path:
        all_comparison_paths.insert(0, comparison_path)
    artifacts.extend(
        {"label": f"comparison report {index}", "path": path}
        for index, path in enumerate(all_comparison_paths, start=1)
    )
    if aggregate_path:
        artifacts.append({"label": "aggregate report", "path": aggregate_path})
    case_ids = sorted(
        {
            str(run["case_id"])
            for run in summaries
            if run.get("case_id") is not None
        }
    )
    return {
        "schema_version": "decision-report-1",
        "task": {"case_ids": case_ids, "run_count": len(summaries)},
        "decision": decision,
        "runs": summaries,
        "comparison": comparison_summary,
        "comparisons": comparison_summaries,
        "aggregate": aggregate_summary,
        "limitations": limitations,
        "artifacts": artifacts,
    }


def render_markdown(summary: dict[str, object]) -> str:
    decision = _dict(summary.get("decision"))
    task = _dict(summary.get("task"))
    run_list = summary.get("runs")
    runs = run_list if isinstance(run_list, list) else []
    lines = [
        "# Efficiency decision report",
        "",
        f"**Cases:** {_join_or_dash(task.get('case_ids'))}  ",
        f"**Runs:** {_value(task.get('run_count'))}",
        "",
        "## Decision",
        "",
        "| Verdict | Evidence status | Confidence |",
        "| --- | --- | --- |",
        (
            f"| {_value(decision.get('verdict'))} | "
            f"{_value(decision.get('evidence_status'))} | "
            f"{_value(decision.get('confidence'))} |"
        ),
        "",
        f"**Conclusion:** {_value(decision.get('conclusion'))}",
        "",
        "## What was tested",
        "",
    ]
    for run in runs:
        if not isinstance(run, dict):
            continue
        lines.extend(
            [
                f"### {_value(run.get('label'))}",
                "",
                f"- Variation: {_value(run.get('variation'))}",
                f"- Run: {_value(run.get('run_id'))}",
                "",
                "Prompt used:",
                "",
                "PROMPT START",
                str(run.get("prompt") or "(prompt unavailable)"),
                "PROMPT END",
                "",
            ]
        )

    lines.extend(
        [
            "## Run summary",
            "",
            "| Run | Tokens | Commands | Filesystem events | Exact reads | Quality |",
            "| --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for run in runs:
        if not isinstance(run, dict):
            continue
        costs = _dict(run.get("costs"))
        filesystem = _dict(run.get("filesystem"))
        exact_read = _dict(run.get("exact_read"))
        quality = _dict(run.get("quality"))
        lines.append(
            f"| {_value(run.get('label'))} | "
            f"{_value(costs.get('total_tokens'))} | "
            f"{_value(costs.get('commands'))} | "
            f"{_value(filesystem.get('event_count'))} | "
            f"{_value(exact_read.get('read_count'))} | "
            f"{_value(quality.get('status'))} |"
        )
    lines.append("")
    lines.extend(["## Filesystem summary", ""])
    for run in runs:
        if not isinstance(run, dict):
            continue
        filesystem = _dict(run.get("filesystem"))
        lines.extend(
            [
                f"### {_value(run.get('label'))}",
                "",
                (
                    f"Status: **{_value(filesystem.get('status'))}**; "
                    f"authority: {_value(filesystem.get('authority'))}; "
                    f"distinct paths: {_value(filesystem.get('distinct_paths'))}."
                ),
                "",
                "Top operations: "
                + _top_counts_text(filesystem.get("top_operations")),
                "",
                "Top paths:",
                "",
            ]
        )
        for path in filesystem.get("top_paths", []):
            if isinstance(path, dict):
                lines.append(
                    f"- {_value(path.get('path'))} "
                    f"({_value(path.get('count'))} events)"
                )
        if not filesystem.get("top_paths"):
            lines.append("- No paths recorded.")
        lines.append("")

    lines.extend(["## Exact file-read audit", ""])
    for run in runs:
        if not isinstance(run, dict):
            continue
        exact_read = _dict(run.get("exact_read"))
        lines.extend(
            [
                f"### {_value(run.get('label'))}",
                "",
                (
                    f"Status: **{_value(exact_read.get('status'))}**; "
                    f"valid: **{_value(exact_read.get('valid'))}**; "
                    f"files: {_value(exact_read.get('file_count'))}; "
                    f"reads: {_value(exact_read.get('read_count'))}; "
                    f"bytes: {_value(exact_read.get('total_bytes'))}; "
                    f"line spans: {_value(exact_read.get('total_lines'))}; "
                    f"unique bytes: "
                    f"{_value(_dict(exact_read.get('analysis')).get('unique_bytes'))}; "
                    f"repeated reads: "
                    f"{_value(_dict(exact_read.get('analysis')).get('repeated_read_count'))}; "
                    f"overlapping reads: "
                    f"{_value(_dict(exact_read.get('analysis')).get('overlapping_read_count'))}."
                ),
                "",
            ]
        )
        categories = _dict(exact_read.get("path_categories"))
        category_counts = categories.get("counts")
        if isinstance(category_counts, dict) and category_counts:
            lines.append(
                "Path categories: "
                + ", ".join(
                    f"{category} ({_value(count)})"
                    for category, count in sorted(category_counts.items())
                )
                + "."
            )
            lines.append("")
        invalid_reasons = exact_read.get("invalid_reasons")
        if isinstance(invalid_reasons, list) and invalid_reasons:
            lines.append("Why it is invalid:")
            lines.extend(f"- {reason}" for reason in invalid_reasons)
            lines.append("")
        files = exact_read.get("files")
        if isinstance(files, list) and files:
            lines.extend(
                [
                    "Files and immutable versions:",
                    "",
                    "| File | Size | Lines | SHA-256 |",
                    "| --- | ---: | ---: | --- |",
                ]
            )
            for file in files:
                if isinstance(file, dict):
                    lines.append(
                        f"| {_value(file.get('path'))} | "
                        f"{_value(file.get('file_size'))} | "
                        f"{_value(file.get('line_count'))} | "
                        f"`{_value(file.get('content_sha256'))}` |"
                    )
            lines.append("")
        reads = exact_read.get("reads")
        if isinstance(reads, list) and reads:
            lines.extend(
                [
                    "Returned-byte ledger:",
                    "",
                    "| Process | File | Byte span | Lines | Bytes | File SHA-256 |",
                    "| --- | --- | --- | --- | ---: | --- |",
                ]
            )
            for read in reads:
                if not isinstance(read, dict):
                    continue
                line_start = read.get("line_start")
                line_end = read.get("line_end")
                line_span = (
                    "binary/none"
                    if line_start is None or line_end is None
                    else f"{line_start}-{line_end}"
                )
                byte_start = read.get("offset")
                byte_count = read.get("bytes")
                byte_span = f"{_value(byte_start)}..{_value(byte_start)}+{_value(byte_count)}"
                lines.append(
                    f"| {_value(read.get('process'))} (PID {_value(read.get('pid'))}) | "
                    f"{_value(read.get('path'))} | {byte_span} | {line_span} | "
                    f"{_value(byte_count)} | `{_value(read.get('file_sha256'))}` |"
                )
            lines.append("")
        if not files and not reads and not invalid_reasons:
            lines.append("- No exact-read evidence recorded.")
            lines.append("")

    comparisons = summary.get("comparisons")
    comparison_list = (
        comparisons
        if isinstance(comparisons, list)
        else [_dict(summary.get("comparison"))]
    )
    comparison_list = [item for item in comparison_list if isinstance(item, dict) and item]
    if comparison_list:
        lines.extend(
            [
                "## Pair comparisons",
                "",
            ]
        )
        for index, comparison in enumerate(comparison_list, start=1):
            lines.extend(
                [
                    f"### Pair {index}",
                    "",
                    (
                        f"Verdict: **{_value(comparison.get('verdict'))}**; "
                        f"primary metric: {_value(comparison.get('primary_metric'))}."
                    ),
                    "",
                    "| Metric | Absolute delta | Relative delta |",
                    "| --- | ---: | ---: |",
                ]
            )
            for metric, delta in _dict(comparison.get("deltas")).items():
                if isinstance(delta, dict):
                    lines.append(
                        f"| {metric} | {_value(delta.get('absolute'))} | "
                        f"{_percentage(delta.get('relative'))} |"
                    )
            lines.extend(
                [
                    "",
                    "Reasons: " + _join_or_dash(comparison.get("reasons")),
                    "",
                ]
            )
            prompt_diff = _dict(comparison.get("prompt_diff"))
            if index == 1 and prompt_diff.get("unified_diff"):
                lines.extend(
                    [
                        "Prompt difference:",
                        "",
                        str(prompt_diff["unified_diff"]),
                        "",
                    ]
                )

    aggregate = _dict(summary.get("aggregate"))
    if aggregate:
        lines.extend(
            [
                "## Replicate aggregate",
                "",
                (
                    f"{_value(aggregate.get('pair_count'))} pairs; "
                    f"counts: {_value(aggregate.get('verdict_counts'))}; "
                    f"verdict: **{_value(aggregate.get('verdict'))}**."
                ),
                "",
                "Aggregate deltas:",
                "",
            ]
        )
        if aggregate.get("reason_codes"):
            lines.append(
                "Aggregate reasons: "
                + _join_or_dash(aggregate.get("reason_codes"))
            )
            lines.append("")
        for metric in ("tokens", "commands", "filesystem_events"):
            delta = _dict(aggregate.get(f"{metric}_delta"))
            if delta:
                lines.append(
                    f"- {metric}: mean {_value(delta.get('mean'))}, "
                    f"median {_value(delta.get('median'))}, "
                    f"range {_value(delta.get('min'))} to {_value(delta.get('max'))}"
                )
        lines.append("")

    lines.extend(["## Limitations", ""])
    limitations = summary.get("limitations")
    if isinstance(limitations, list) and limitations:
        lines.extend(f"- {item}" for item in limitations)
    else:
        lines.append("- None recorded.")
    lines.extend(["", "## Technical artefacts", ""])
    artifacts = summary.get("artifacts")
    if isinstance(artifacts, list) and artifacts:
        for artifact in artifacts:
            if isinstance(artifact, dict):
                lines.append(
                    f"- [{_value(artifact.get('label'))}]"
                    f"({_value(artifact.get('path'))})"
                )
    else:
        lines.append("- No source artefacts were supplied.")
    lines.append("")
    return "\n".join(lines)


def _summarize_run(item: dict[str, object]) -> dict[str, object]:
    report = _dict(item.get("report"))
    manifest = _dict(report.get("manifest"))
    observability = _dict(report.get("observability"))
    tokens = _dict(observability.get("tokens"))
    totals = _dict(tokens.get("totals"))
    command_trace = _dict(report.get("command_trace"))
    filesystem = _dict(observability.get("filesystem"))
    exact_read = _dict(observability.get("exact_read"))
    events = filesystem.get("events")
    event_list = events if isinstance(events, list) else []
    operations = Counter(
        str(event.get("operation"))
        for event in event_list
        if isinstance(event, dict) and event.get("operation")
    )
    paths = Counter(
        str(event.get("path"))
        for event in event_list
        if isinstance(event, dict) and event.get("path")
    )
    exact_events = [
        event for event in exact_read.get("events", [])
        if isinstance(event, dict)
    ]
    exact_paths = Counter(
        str(event.get("path"))
        for event in exact_events
        if event.get("path")
    )
    exact_files = [
        file for file in exact_read.get("files", [])
        if isinstance(file, dict)
    ]
    quality = _dict(item.get("quality"))
    if isinstance(quality.get("quality"), dict):
        quality = _dict(quality.get("quality"))
    return {
        "label": item.get("label") or manifest.get("variation") or "run",
        "run_id": manifest.get("run_id"),
        "case_id": manifest.get("case_id"),
        "variation": manifest.get("variation"),
        "prompt": manifest.get("prompt"),
        "model": manifest.get("model"),
        "status": report.get("status"),
        "costs": {
            "input_tokens": totals.get("input_tokens"),
            "cached_input_tokens": totals.get("cached_input_tokens"),
            "output_tokens": totals.get("output_tokens"),
            "reasoning_output_tokens": totals.get("reasoning_output_tokens"),
            "total_tokens": totals.get("total_tokens"),
            "commands": command_trace.get("command_count"),
            "failed_commands": command_trace.get("failed_command_count"),
            "agent_messages": command_trace.get("agent_message_count"),
        },
        "filesystem": {
            "status": filesystem.get("status", "unavailable"),
            "authority": filesystem.get("authority"),
            "event_count": len(event_list),
            "distinct_paths": len(paths),
            "top_operations": [
                {"operation": operation, "count": count}
                for operation, count in operations.most_common(8)
            ],
            "top_paths": [
                {"path": path, "count": count}
                for path, count in paths.most_common(8)
            ],
            "issues": filesystem.get("issues", []),
        },
        "exact_read": {
            "status": exact_read.get("status", "unavailable"),
            "valid": exact_read.get("valid", False),
            "file_count": exact_read.get("file_count", len(exact_files)),
            "read_count": exact_read.get("read_count", len(exact_events)),
            "total_bytes": exact_read.get("total_bytes", 0),
            "total_lines": exact_read.get("total_lines", 0),
            "analysis": _dict(exact_read.get("analysis")),
            "process_count": len(
                [
                    process for process in exact_read.get("processes", [])
                    if isinstance(process, dict)
                ]
            ),
            "invalid_reasons": exact_read.get("invalid_reasons", []),
            "path_categories": exact_read.get(
                "path_categories", {"counts": {}, "paths": {}}
            ),
            "files": [
                {
                    "path": file.get("path"),
                    "file_size": file.get("file_size"),
                    "content_sha256": file.get("content_sha256"),
                    "line_count": file.get("line_count"),
                }
                for file in exact_files
            ],
            "reads": [
                {
                    "event_index": event.get("event_index"),
                    "pid": event.get("pid"),
                    "process": event.get("process"),
                    "path": event.get("path"),
                    "operation": event.get("operation"),
                    "offset": event.get("offset"),
                    "bytes": event.get("bytes"),
                    "line_start": event.get("line_start"),
                    "line_end": event.get("line_end"),
                    "content_sha256": event.get("content_sha256"),
                    "file_sha256": event.get("file_sha256"),
                }
                for event in exact_events
            ],
            "top_paths": [
                {"path": path, "count": count}
                for path, count in exact_paths.most_common(8)
            ],
        },
        "quality": {
            "status": quality.get("status", "unavailable"),
            "missing_required_claim_ids": quality.get(
                "missing_required_claim_ids", []
            ),
            "disallowed_claims": quality.get("disallowed_claims", []),
        },
        "artifacts": _run_artifacts(item),
    }


def _summarize_comparison(
    value: dict[str, object] | None,
) -> dict[str, object] | None:
    if not value:
        return None
    comparison = _dict(value.get("comparison")) or value
    return {
        "verdict": comparison.get("verdict"),
        "evidence_status": comparison.get("evidence_status"),
        "primary_metric": comparison.get("primary_metric"),
        "reasons": comparison.get("reasons", []),
        "deltas": comparison.get("deltas", {}),
        "quality": comparison.get("quality", {}),
        "prompt_diff": comparison.get("prompt_diff", {}),
    }


def _summarize_aggregate(
    value: dict[str, object] | None,
) -> dict[str, object] | None:
    if not value:
        return None
    return {
        key: value.get(key)
        for key in (
            "verdict",
            "evidence_status",
            "pair_count",
            "verdict_counts",
            "reason_codes",
            "tokens_delta",
            "commands_delta",
            "filesystem_events_delta",
        )
        if key in value
    }


def _decision_summary(source: dict[str, object] | None) -> dict[str, object]:
    if not source:
        return {
            "verdict": "unavailable",
            "evidence_status": "blocked",
            "confidence": "none",
            "conclusion": "No comparison evidence was supplied.",
        }
    verdict = str(source.get("verdict") or "inconclusive")
    evidence_status = str(source.get("evidence_status") or "blocked")
    conclusions = {
        "better": "The candidate appears more efficient under the recorded evidence.",
        "worse": "The candidate appears less efficient under the recorded evidence.",
        "same": "No material efficiency difference was detected.",
        "tradeoff": "The candidate trades one cost dimension against another.",
        "inconclusive": "No safe efficiency conclusion can be made from this evidence.",
        "unavailable": "No efficiency conclusion is available.",
    }
    return {
        "verdict": verdict,
        "evidence_status": evidence_status,
        "confidence": {
            "supported": "supported",
            "exploratory": "exploratory",
            "blocked": "none",
        }.get(evidence_status, "unknown"),
        "conclusion": conclusions.get(verdict, conclusions["inconclusive"]),
    }


def _limitations(
    runs: list[dict[str, object]],
    comparisons: list[dict[str, object]],
    aggregate: dict[str, object] | None,
) -> list[str]:
    limitations: list[str] = []
    for run in runs:
        filesystem = _dict(run.get("filesystem"))
        if filesystem.get("status") != "available":
            limitations.append(
                f"{run.get('label')}: filesystem evidence is "
                f"{filesystem.get('status', 'unavailable')}."
            )
        exact_read = _dict(run.get("exact_read"))
        if exact_read.get("valid") is not True:
            limitations.append(
                f"{run.get('label')}: exact file-read evidence is "
                f"{exact_read.get('status', 'unavailable')}."
            )
        quality = _dict(run.get("quality"))
        if quality.get("status") not in {None, "pass"}:
            limitations.append(
                f"{run.get('label')}: quality gate is {quality.get('status')}."
            )
    if any(item.get("evidence_status") != "supported" for item in comparisons):
        limitations.append(
            "Pair evidence is not supported; the result remains exploratory "
            "or blocked."
        )
    if aggregate and aggregate.get("verdict") == "inconclusive":
        limitations.append("Replicate results do not support one stable verdict.")
    return limitations


def _run_artifacts(item: dict[str, object]) -> list[dict[str, str]]:
    artifacts: list[dict[str, str]] = []
    for key, label in (
        ("report_path", "run report"),
        ("quality_path", "quality report"),
    ):
        value = item.get(key)
        if value:
            artifacts.append(
                {
                    "label": f"{item.get('label', 'run')} {label}",
                    "path": str(value),
                }
            )
    return artifacts


def _dict(value: object) -> dict[str, object]:
    return value if isinstance(value, dict) else {}


def _value(value: object) -> str:
    if value is None or value == "":
        return "—"
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def _percentage(value: object) -> str:
    if value is None:
        return "—"
    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return _value(value)


def _join_or_dash(value: object) -> str:
    if isinstance(value, (list, tuple, set)):
        values = [_value(item) for item in value]
        return ", ".join(values) if values else "—"
    return _value(value)


def _top_counts_text(value: object) -> str:
    if not isinstance(value, list) or not value:
        return "—"
    return ", ".join(
        f"{_value(_dict(item).get('operation'))} "
        f"({_value(_dict(item).get('count'))})"
        for item in value
        if isinstance(item, dict)
    ) or "—"
