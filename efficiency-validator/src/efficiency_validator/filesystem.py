"""Parsing for independently collected filesystem observations.

Codex ``exec --json`` exposes command text and aggregated output, not the
files opened by the processes behind a shell command.  This module therefore
accepts only an explicit sidecar trace whose producer and authority are named
in every capture.  It never promotes command paths or agent prose to file
access evidence.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from typing import Iterable, Literal


FilesystemSource = Literal[
    "macos-fs-usage",
    "linux-audit",
    "exec-server-rpc",
    "structured-read",
]
FilesystemStatus = Literal[
    "available",
    "unavailable",
    "denied",
    "partial",
    "malformed",
    "truncated",
]
FilesystemAuthority = Literal[
    "os-kernel-observation",
    "executor-rpc-observation",
    "structured-runtime-observation",
]
FilesystemEvidenceKind = Literal["requested", "returned", "opened", "scanned"]
ContentCapture = Literal["none", "hash", "full"]


_MACOS_FS_USAGE_TIMESTAMP = re.compile(
    r"^\s*(?P<timestamp>\d{2}:\d{2}:\d{2}\.\d+)\s+"
    r"(?P<operation>\S+)\s+"
)
_MACOS_PROCESS_PID = re.compile(r"^(?P<process>.+)\.(?P<pid>\d+)$")
_MACOS_BYTE_COUNT = re.compile(r"\bB=(?P<bytes>\d+)")
_MACOS_OFFSET = re.compile(r"\bO=(?P<offset>\d+)")


@dataclass(frozen=True)
class FilesystemEvent:
    run_id: str
    case_id: str
    trace_id: str
    event_index: int
    timestamp: str
    source: FilesystemSource
    authority: FilesystemAuthority
    evidence_kind: FilesystemEvidenceKind
    operation: str
    path: str
    pid: int | None = None
    process: str | None = None
    command_id: str | None = None
    bytes: int | None = None
    thread_id: int | None = None
    offset: int | None = None
    file_size: int | None = None
    line_start: int | None = None
    line_end: int | None = None
    file_line_count: int | None = None
    content_capture: ContentCapture = "none"
    content_hash: str | None = None
    content: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class FilesystemParseIssue:
    line_number: int
    kind: Literal["non_json", "malformed_json", "invalid_payload", "mismatch"]
    detail: str


@dataclass(frozen=True)
class ParsedFilesystemTrace:
    schema_version: str | None
    run_id: str | None
    case_id: str | None
    trace_id: str | None
    source: FilesystemSource | None
    authority: FilesystemAuthority | None
    status: FilesystemStatus
    events: tuple[FilesystemEvent, ...]
    issues: tuple[FilesystemParseIssue, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "case_id": self.case_id,
            "trace_id": self.trace_id,
            "source": self.source,
            "authority": self.authority,
            "status": self.status,
            "events": [event.to_dict() for event in self.events],
            "issues": [asdict(issue) for issue in self.issues],
        }


def macos_fs_usage_sidecar(
    lines: Iterable[str],
    *,
    run_id: str,
    case_id: str,
    trace_id: str,
    target_prefix: str,
    additional_prefixes: Iterable[str] = (),
    process_pids: Iterable[int] | None = None,
    process_names: Iterable[str] | None = None,
    capture_all_paths: bool = False,
) -> tuple[dict[str, object], ...]:
    """Convert macOS ``fs_usage -f pathname`` output to ``filesystem-trace-1``.

    ``fs_usage`` is a system-wide stream.  The converter keeps only records
    whose pathname starts with the immutable staged target, so unrelated host
    activity cannot be attributed to the measured run.  The source reports
    operations observed by the kernel; only ``open*`` operations are promoted
    to ``opened`` evidence.  Other operations remain ``requested`` evidence.
    """

    if not run_id or not case_id or not trace_id or not target_prefix:
        raise ValueError("run_id, case_id, trace_id, and target_prefix are required")
    prefixes = [target_prefix.rstrip("/")]
    prefixes.extend(
        prefix.rstrip("/")
        for prefix in additional_prefixes
        if prefix and prefix.rstrip("/") not in prefixes
    )
    allowed_pids = None if process_pids is None else set(process_pids)
    allowed_process_names = (
        None if process_names is None else {str(name) for name in process_names}
    )
    records: list[dict[str, object]] = [
        {
            "type": "filesystem.trace.started",
            "schema_version": "filesystem-trace-1",
            "run_id": run_id,
            "case_id": case_id,
            "trace_id": trace_id,
            "source": "macos-fs-usage",
            "authority": "os-kernel-observation",
            "status": "available",
            "capture_scope": (
                "measured-process-tree-by-process-name"
                if allowed_process_names is not None and capture_all_paths
                else "measured-process-tree"
                if allowed_pids is not None and capture_all_paths
                else "staged-target-and-explicit-prefixes"
                if len(prefixes) > 1
                else "staged-target-prefix"
            ),
            "target_prefix": prefixes[0],
            "capture_prefixes": prefixes,
            "process_pids": (
                sorted(allowed_pids) if allowed_pids is not None else None
            ),
            "process_names": (
                sorted(allowed_process_names)
                if allowed_process_names is not None
                else None
            ),
            "correlation_method": (
                "process-name"
                if allowed_process_names is not None and capture_all_paths
                else "process-thread-id"
                if allowed_pids is not None and capture_all_paths
                else "path-prefix"
            ),
            "correlation_confidence": (
                "partial"
                if allowed_process_names is not None and capture_all_paths
                else "high"
                if allowed_pids is not None and capture_all_paths
                else "high"
            ),
        }
    ]
    event_index = 0
    for line in lines:
        match = _MACOS_FS_USAGE_TIMESTAMP.match(line)
        if match is None:
            continue
        path_start, path = (
            _matching_any_path(line, match.end())
            if capture_all_paths
            else _matching_path(line, match.end(), prefixes)
        )
        if path_start is None or path is None:
            continue
        path_tail = line[path_start:].split()
        if not path_tail:
            continue
        process_token = path_tail[-1] if len(path_tail) > 1 else None
        process, thread_id = _split_macos_process(process_token)
        if allowed_process_names is not None and process not in allowed_process_names:
            continue
        if (
            allowed_process_names is None
            and allowed_pids is not None
            and thread_id not in allowed_pids
        ):
            continue
        operation = match.group("operation")
        records.append(
            {
                "type": "filesystem.access",
                "schema_version": "filesystem-trace-1",
                "run_id": run_id,
                "case_id": case_id,
                "trace_id": trace_id,
                "event_index": event_index,
                "timestamp": match.group("timestamp"),
                "source": "macos-fs-usage",
                "authority": "os-kernel-observation",
                "evidence_kind": (
                    "opened" if operation.lower().startswith("open") else "requested"
                ),
                "operation": operation,
                "path": path,
                "thread_id": thread_id,
                "process": process,
                "bytes": _marker_int(_MACOS_BYTE_COUNT, line),
                "offset": _marker_int(_MACOS_OFFSET, line),
            }
        )
        event_index += 1
    return tuple(records)


def _matching_path(
    line: str, start: int, prefixes: list[str]
) -> tuple[int | None, str | None]:
    for prefix in prefixes:
        path_start = line.find(prefix, start)
        if path_start < 0:
            continue
        tail = line[path_start:].split()
        if not tail:
            continue
        path = tail[0]
        if path == prefix or path.startswith(prefix + "/"):
            return path_start, path
    return None, None


def _marker_int(pattern: re.Pattern[str], line: str) -> int | None:
    match = pattern.search(line)
    return None if match is None else int(match.group(1))


def _matching_any_path(line: str, start: int) -> tuple[int | None, str | None]:
    match = re.search(r"(?P<path>/\S+)", line[start:])
    if match is None:
        return None, None
    path_start = start + match.start("path")
    return path_start, match.group("path")


def _split_macos_process(value: str | None) -> tuple[str | None, int | None]:
    if value is None:
        return None, None
    match = _MACOS_PROCESS_PID.match(value)
    if match is None:
        return value, None
    return match.group("process"), int(match.group("pid"))


def parse_filesystem_trace(
    lines: Iterable[str],
    *,
    expected_run_id: str | None = None,
    expected_case_id: str | None = None,
) -> ParsedFilesystemTrace:
    """Parse a versioned JSONL filesystem sidecar conservatively."""

    events: list[FilesystemEvent] = []
    issues: list[FilesystemParseIssue] = []
    metadata: dict[str, object] | None = None

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(
                FilesystemParseIssue(line_number, "malformed_json", str(exc))
            )
            continue
        if not isinstance(payload, dict):
            issues.append(
                FilesystemParseIssue(
                    line_number, "invalid_payload", "JSON value is not an object"
                )
            )
            continue

        if payload.get("type") == "filesystem.trace.started":
            if metadata is not None:
                issues.append(
                    FilesystemParseIssue(
                        line_number,
                        "invalid_payload",
                        "duplicate filesystem.trace.started record",
                    )
                )
                continue
            metadata = payload
            continue

        if payload.get("type") != "filesystem.access":
            issues.append(
                FilesystemParseIssue(
                    line_number,
                    "invalid_payload",
                    "expected filesystem.trace.started or filesystem.access",
                )
            )
            continue

        try:
            event = _event_from_dict(payload)
        except (KeyError, TypeError, ValueError) as exc:
            issues.append(
                FilesystemParseIssue(line_number, "invalid_payload", str(exc))
            )
            continue
        events.append(event)

    if metadata is None:
        issues.append(
            FilesystemParseIssue(
                0,
                "invalid_payload",
                "missing filesystem.trace.started metadata record",
            )
        )
        return ParsedFilesystemTrace(
            schema_version=None,
            run_id=None,
            case_id=None,
            trace_id=None,
            source=None,
            authority=None,
            status="malformed",
            events=tuple(events),
            issues=tuple(issues),
        )

    try:
        schema_version = _required_string(metadata, "schema_version")
        run_id = _required_string(metadata, "run_id")
        case_id = _required_string(metadata, "case_id")
        trace_id = _required_string(metadata, "trace_id")
        source = _literal_source(metadata.get("source"))
        authority = _literal_authority(metadata.get("authority"))
        status = _literal_status(metadata.get("status"))
    except (TypeError, ValueError) as exc:
        issues.append(FilesystemParseIssue(1, "invalid_payload", str(exc)))
        return ParsedFilesystemTrace(
            schema_version=(
                metadata.get("schema_version")
                if isinstance(metadata.get("schema_version"), str)
                else None
            ),
            run_id=(
                metadata.get("run_id")
                if isinstance(metadata.get("run_id"), str)
                else None
            ),
            case_id=(
                metadata.get("case_id")
                if isinstance(metadata.get("case_id"), str)
                else None
            ),
            trace_id=(
                metadata.get("trace_id")
                if isinstance(metadata.get("trace_id"), str)
                else None
            ),
            source=None,
            authority=None,
            status="malformed",
            events=tuple(events),
            issues=tuple(issues),
        )
    if schema_version != "filesystem-trace-1":
        issues.append(
            FilesystemParseIssue(
                1,
                "mismatch",
                f"unsupported filesystem trace schema: {schema_version!r}",
            )
        )
    for name, actual, expected in (
        ("run_id", run_id, expected_run_id),
        ("case_id", case_id, expected_case_id),
    ):
        if expected is not None and actual != expected:
            issues.append(
                FilesystemParseIssue(
                    1,
                    "mismatch",
                    f"{name} {actual!r} does not match expected {expected!r}",
                )
            )

    for event in events:
        for name, actual, expected in (
            ("run_id", event.run_id, run_id),
            ("case_id", event.case_id, case_id),
            ("trace_id", event.trace_id, trace_id),
            ("source", event.source, source),
            ("authority", event.authority, authority),
        ):
            if actual != expected:
                issues.append(
                    FilesystemParseIssue(
                        0,
                        "mismatch",
                        f"event {name} {actual!r} does not match metadata {expected!r}",
                    )
                )

    if issues and status == "available":
        status = "partial"
    return ParsedFilesystemTrace(
        schema_version=schema_version,
        run_id=run_id,
        case_id=case_id,
        trace_id=trace_id,
        source=source,
        authority=authority,
        status=status,
        events=tuple(events),
        issues=tuple(issues),
    )


def _event_from_dict(payload: dict[str, object]) -> FilesystemEvent:
    event_index = int(payload["event_index"])
    if event_index < 0:
        raise ValueError("event_index must be non-negative")
    raw_bytes = payload.get("bytes")
    byte_count = None if raw_bytes is None else int(raw_bytes)
    if byte_count is not None and byte_count < 0:
        raise ValueError("bytes must be non-negative")
    offset = _optional_non_negative_int(payload, "offset")
    file_size = _optional_non_negative_int(payload, "file_size")
    line_start = _optional_positive_int(payload, "line_start")
    line_end = _optional_positive_int(payload, "line_end")
    file_line_count = _optional_positive_int(payload, "file_line_count")
    if line_start is not None and line_end is not None and line_end < line_start:
        raise ValueError("line_end must be greater than or equal to line_start")
    if line_end is not None and file_line_count is not None:
        if line_end > file_line_count:
            raise ValueError("line_end cannot exceed file_line_count")
    content_capture = _literal_content_capture(
        payload.get("content_capture", "none")
    )
    content = payload.get("content")
    if content is not None and not isinstance(content, str):
        raise ValueError("content must be a string when present")
    if content_capture != "full" and content is not None:
        raise ValueError("content requires content_capture='full'")
    content_hash = payload.get("content_hash")
    if content_hash is not None and not isinstance(content_hash, str):
        raise ValueError("content_hash must be a string when present")
    if content is not None:
        calculated_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if content_hash is not None and content_hash != calculated_hash:
            raise ValueError("content_hash does not match captured content")
        content_hash = calculated_hash
    return FilesystemEvent(
        run_id=_required_string(payload, "run_id"),
        case_id=_required_string(payload, "case_id"),
        trace_id=_required_string(payload, "trace_id"),
        event_index=event_index,
        timestamp=_required_string(payload, "timestamp"),
        source=_literal_source(payload.get("source")),
        authority=_literal_authority(payload.get("authority")),
        evidence_kind=_literal_evidence_kind(payload.get("evidence_kind")),
        operation=_required_string(payload, "operation"),
        path=_required_string(payload, "path"),
        pid=None if payload.get("pid") is None else int(payload["pid"]),
        process=None
        if payload.get("process") is None
        else str(payload["process"]),
        command_id=None
        if payload.get("command_id") is None
        else str(payload["command_id"]),
        bytes=byte_count,
        thread_id=_optional_non_negative_int(payload, "thread_id"),
        offset=offset,
        file_size=file_size,
        line_start=line_start,
        line_end=line_end,
        file_line_count=file_line_count,
        content_capture=content_capture,
        content_hash=content_hash,
        content=content,
    )


def _optional_non_negative_int(
    payload: dict[str, object], name: str
) -> int | None:
    value = payload.get(name)
    if value is None:
        return None
    parsed = int(value)
    if parsed < 0:
        raise ValueError(f"{name} must be non-negative")
    return parsed


def _optional_positive_int(payload: dict[str, object], name: str) -> int | None:
    value = payload.get(name)
    if value is None:
        return None
    parsed = int(value)
    if parsed < 1:
        raise ValueError(f"{name} must be positive")
    return parsed


def _required_string(payload: dict[str, object], name: str) -> str:
    value = payload.get(name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _literal_source(value: object) -> FilesystemSource:
    if value not in {
        "macos-fs-usage",
        "linux-audit",
        "exec-server-rpc",
        "structured-read",
    }:
        raise ValueError(f"invalid filesystem source: {value!r}")
    return value  # type: ignore[return-value]


def _literal_authority(value: object) -> FilesystemAuthority:
    if value not in {
        "os-kernel-observation",
        "executor-rpc-observation",
        "structured-runtime-observation",
    }:
        raise ValueError(f"invalid filesystem authority: {value!r}")
    return value  # type: ignore[return-value]


def _literal_status(value: object) -> FilesystemStatus:
    if value not in {
        "available",
        "unavailable",
        "denied",
        "partial",
        "malformed",
        "truncated",
    }:
        raise ValueError(f"invalid filesystem status: {value!r}")
    return value  # type: ignore[return-value]


def _literal_evidence_kind(value: object) -> FilesystemEvidenceKind:
    if value not in {"requested", "returned", "opened", "scanned"}:
        raise ValueError(f"invalid filesystem evidence kind: {value!r}")
    return value  # type: ignore[return-value]


def _literal_content_capture(value: object) -> ContentCapture:
    if value not in {"none", "hash", "full"}:
        raise ValueError(f"invalid content capture mode: {value!r}")
    return value  # type: ignore[return-value]


def summarize_read_coverage(
    parsed: ParsedFilesystemTrace,
) -> dict[str, object]:
    """Summarize observable read coverage without treating unknown as zero.

    Coverage is calculated from line ranges when available, otherwise from
    byte intervals. The raw event still owns optional captured content; this
    summary deliberately stays compact so reports do not duplicate large file
    bodies.
    """

    grouped: dict[str, list[FilesystemEvent]] = {}
    for event in parsed.events:
        operation = event.operation.lower()
        if event.evidence_kind not in {"returned", "scanned"} and not (
            operation.startswith("read") or operation.startswith("pread")
        ):
            continue
        grouped.setdefault(event.path, []).append(event)

    files: list[dict[str, object]] = []
    for path, events in sorted(grouped.items()):
        file_size = next(
            (event.file_size for event in events if event.file_size is not None),
            None,
        )
        line_count = next(
            (
                event.file_line_count
                for event in events
                if event.file_line_count is not None
            ),
            None,
        )
        line_intervals = [
            (event.line_start, event.line_end)
            for event in events
            if event.line_start is not None and event.line_end is not None
        ]
        byte_intervals = [
            (event.offset, event.offset + event.bytes - 1)
            for event in events
            if event.offset is not None and event.bytes is not None and event.bytes > 0
        ]
        line_coverage = (
            _covered_units(line_intervals) / line_count
            if line_count is not None and line_count > 0 and line_intervals
            else None
        )
        byte_coverage = (
            _covered_units(byte_intervals) / file_size
            if file_size is not None and file_size > 0 and byte_intervals
            else (1.0 if file_size == 0 and not byte_intervals else None)
        )
        coverage = line_coverage if line_coverage is not None else byte_coverage
        coverage_status = (
            "full"
            if coverage is not None and coverage >= 1.0
            else "partial"
            if coverage is not None
            else "indeterminate"
        )
        observed_lines = (
            [
                min(start for start, _ in line_intervals),
                max(end for _, end in line_intervals),
            ]
            if line_intervals
            else None
        )
        capture_rank = max(
            (_content_capture_rank(event.content_capture) for event in events),
            default=0,
        )
        files.append(
            {
                "path": path,
                "file_size": file_size,
                "file_line_count": line_count,
                "observed_bytes": (
                    _covered_units(byte_intervals) if byte_intervals else None
                ),
                "observed_line_range": observed_lines,
                "line_coverage": line_coverage,
                "byte_coverage": byte_coverage,
                "coverage_status": coverage_status,
                "content_capture": ("none", "hash", "full")[capture_rank],
                "content_hashes": sorted(
                    {
                        event.content_hash
                        for event in events
                        if event.content_hash is not None
                    }
                ),
            }
        )
    return {
        "status": parsed.status,
        "file_count": len(files),
        "files": files,
    }


def _covered_units(intervals: list[tuple[int | None, int | None]]) -> int:
    normalized = sorted(
        (start, end)
        for start, end in intervals
        if start is not None and end is not None and end >= start
    )
    if not normalized:
        return 0
    total = 0
    current_start, current_end = normalized[0]
    for start, end in normalized[1:]:
        if start <= current_end + 1:
            current_end = max(current_end, end)
        else:
            total += current_end - current_start + 1
            current_start, current_end = start, end
    return total + current_end - current_start + 1


def _content_capture_rank(value: ContentCapture) -> int:
    return {"none": 0, "hash": 1, "full": 2}[value]
