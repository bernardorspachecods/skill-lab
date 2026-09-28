from __future__ import annotations

import hashlib
from dataclasses import asdict
from typing import Iterable, Mapping

from .codex_events import ParsedCodexEvents
from .evaluate import evaluate_command_trace
from .filesystem import ParsedFilesystemTrace, summarize_read_coverage
from .exact_read import ExactReadTrace
from .network import ParsedNetworkTrace, summarize_network
from .path_categories import PathCategory, classify_path
from .manifest import RunManifest


def build_command_report(
    parsed: ParsedCodexEvents,
    manifest: RunManifest,
    oracle: dict[str, object],
    *,
    identified_claim_ids: Iterable[str] = (),
    filesystem_trace: ParsedFilesystemTrace | None = None,
    network_trace: ParsedNetworkTrace | None = None,
    exact_read_trace: ExactReadTrace | None = None,
    exact_read_process_tree_pids: Iterable[int] | None = None,
    path_roots: Mapping[str, Iterable[str]] | None = None,
) -> dict[str, object]:
    command_trace = evaluate_command_trace(
        parsed,
        oracle,
        identified_claim_ids=identified_claim_ids,
    )
    status = "complete" if manifest.complete and parsed.complete else "incomplete"
    return {
        "schema_version": "command-report-1",
        "status": status,
        "manifest": manifest.to_dict(),
        "parser": {
            "complete": parsed.complete,
            "issues": [asdict(issue) for issue in parsed.issues],
        },
        "observability": build_observability_report(
            parsed,
            filesystem_trace,
            network_trace=network_trace,
            exact_read_trace=exact_read_trace,
            exact_read_process_tree_pids=exact_read_process_tree_pids,
            path_roots=path_roots,
        ),
        "command_trace": asdict(command_trace),
    }


def build_observability_report(
    parsed: ParsedCodexEvents,
    filesystem_trace: ParsedFilesystemTrace | None = None,
    *,
    network_trace: ParsedNetworkTrace | None = None,
    exact_read_trace: ExactReadTrace | None = None,
    exact_read_process_tree_pids: Iterable[int] | None = None,
    path_roots: Mapping[str, Iterable[str]] | None = None,
) -> dict[str, object]:
    """Return E1 signals without guessing missing measurements."""

    if parsed.token_usage:
        token_status = "available" if parsed.complete else "partial"
    elif any(turn.status == "failed" for turn in parsed.turns):
        token_status = "failed"
    elif any(turn.status == "incomplete" for turn in parsed.turns):
        token_status = "incomplete"
    else:
        token_status = "unavailable"

    totals = {
        "input_tokens": sum(
            record.usage.input_tokens for record in parsed.token_usage
        ),
        "cached_input_tokens": sum(
            record.usage.cached_input_tokens for record in parsed.token_usage
        ),
        "cache_write_input_tokens": sum(
            record.usage.cache_write_input_tokens
            for record in parsed.token_usage
        ),
        "output_tokens": sum(
            record.usage.output_tokens for record in parsed.token_usage
        ),
        "reasoning_output_tokens": sum(
            record.usage.reasoning_output_tokens
            for record in parsed.token_usage
        ),
        "total_tokens": sum(
            record.usage.total_tokens for record in parsed.token_usage
        ),
    }
    if filesystem_trace is not None:
        filesystem = filesystem_trace.to_dict()
        filesystem["read_coverage"] = summarize_read_coverage(filesystem_trace)
        filesystem["path_categories"] = _path_category_summary(
            filesystem_trace, path_roots or {}
        )
    else:
        filesystem = {
            "status": "unavailable",
            "source": "none",
            "authority": None,
            "events": [],
            "issues": [],
            "read_coverage": {
                "status": "unavailable",
                "file_count": 0,
                "files": [],
            },
            "reason": "No authoritative filesystem sidecar was supplied",
        }
    if exact_read_trace is not None:
        exact_read = exact_read_trace.to_dict()
        exact_read.update(
            {
                "file_count": len(exact_read_trace.files),
                "read_count": len(exact_read_trace.events),
                "total_lines": sum(
                    (event.line_end - event.line_start + 1)
                    for event in exact_read_trace.events
                    if event.line_start is not None and event.line_end is not None
                ),
                "total_bytes": sum(
                    event.bytes for event in exact_read_trace.events
                ),
                "analysis": exact_read_trace.read_analysis,
            }
        )
        if exact_read_process_tree_pids is None:
            expected_process_pids: set[int] = set()
            missing_process_pids: list[int] = []
            process_tree_covered = False
        else:
            expected_process_pids = {
                int(pid) for pid in exact_read_process_tree_pids
            }
            observed_process_pids = {
                process.pid for process in exact_read_trace.processes
            }
            missing_process_pids = sorted(
                expected_process_pids - observed_process_pids
            )
            process_tree_covered = bool(expected_process_pids) and not missing_process_pids
        exact_read.update(
            {
                "process_tree_covered": process_tree_covered,
                "process_tree_pids": sorted(expected_process_pids),
                "missing_process_pids": missing_process_pids,
                "path_categories": _exact_path_category_summary(
                    exact_read_trace, path_roots or {}
                ),
            }
        )
    else:
        exact_read = {
            "status": "unavailable",
            "valid": False,
            "events": [],
            "files": [],
            "processes": [],
            "invalid_reasons": ["No exact-read sidecar was supplied"],
            "file_count": 0,
            "read_count": 0,
            "total_lines": 0,
            "total_bytes": 0,
            "analysis": {
                "repeated_read_count": 0,
                "overlapping_read_count": 0,
                "unique_bytes": 0,
            },
            "process_tree_covered": False,
            "process_tree_pids": [],
            "missing_process_pids": [],
            "path_categories": {"counts": {}, "paths": {}},
        }
    if network_trace is not None:
        network = network_trace.to_dict()
        network["summary"] = summarize_network(network_trace)
    else:
        network = {
            "status": "unavailable",
            "source": "none",
            "authority": None,
            "events": [],
            "issues": [],
            "summary": {
                "status": "unavailable",
                "event_count": 0,
                "destination_count": 0,
                "total_bytes_sent": 0,
                "total_bytes_received": 0,
                "total_bytes": 0,
                "destinations": [],
            },
            "reason": "No authoritative network metadata sidecar was supplied",
        }
    return {
        "schema_version": "observability-1",
        "thread_id": parsed.thread_id,
        "raw_event_count": len(parsed.raw_events),
        "raw_events": [event.to_dict() for event in parsed.raw_events],
        "turns": [
            {
                "turn_index": turn.turn_index,
                "started_event_index": turn.started_event_index,
                "terminal_event_index": turn.terminal_event_index,
                "status": turn.status,
                "has_usage": turn.usage is not None,
            }
            for turn in parsed.turns
        ],
        "tokens": {
            "status": token_status,
            "source": "codex-exec-json",
            "authoritative": bool(parsed.token_usage),
            "records": [record.to_dict() for record in parsed.token_usage],
            "totals": totals if parsed.token_usage else None,
        },
        "filesystem": filesystem,
        "exact_read": exact_read,
        "network": network,
        "returned_content": _returned_content(parsed),
    }


def _path_category_summary(
    filesystem_trace: ParsedFilesystemTrace,
    path_roots: Mapping[str, Iterable[str]],
) -> dict[str, object]:
    counts: dict[PathCategory, int] = {}
    paths: dict[PathCategory, set[str]] = {}
    for event in filesystem_trace.events:
        category = classify_path(event.path, path_roots)
        counts[category] = counts.get(category, 0) + 1
        paths.setdefault(category, set()).add(event.path)
    return {
        "counts": dict(sorted(counts.items())),
        "paths": {
            category: sorted(values) for category, values in sorted(paths.items())
        },
    }


def _exact_path_category_summary(
    trace: ExactReadTrace,
    path_roots: Mapping[str, Iterable[str]],
) -> dict[str, object]:
    counts: dict[PathCategory, int] = {}
    paths: dict[PathCategory, set[str]] = {}
    for event in trace.events:
        category = classify_path(event.path, path_roots)
        counts[category] = counts.get(category, 0) + 1
        paths.setdefault(category, set()).add(event.path)
    return {
        "counts": dict(sorted(counts.items())),
        "paths": {
            category: sorted(values) for category, values in sorted(paths.items())
        },
    }


def _returned_content(parsed: ParsedCodexEvents) -> list[dict[str, object]]:
    """Expose exact tool output without mislabelling it as a file read."""

    returned: list[dict[str, object]] = []
    for event in parsed.events:
        if event.kind != "command_execution" or not event.text:
            continue
        content_bytes = event.text.encode("utf-8")
        returned.append(
            {
                "event_index": event.event_index,
                "source": "command_aggregated_output",
                "command": event.command,
                "bytes": len(content_bytes),
                "content_hash": hashlib.sha256(content_bytes).hexdigest(),
                "content": event.text,
            }
        )
    return returned
