"""Exact returned-byte filesystem evidence and line reconstruction.

The legacy filesystem trace answers whether an operating-system access was
observed.  This module answers the stricter question needed by a file-efficiency
verdict: which bytes reached a measured process, from which immutable file
version, and which text lines those bytes touch.
"""

from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class ExactReadFile:
    path: str
    file_size: int
    content: bytes
    content_sha256: str
    content_kind: str

    @property
    def line_count(self) -> int:
        if self.content_kind != "text" or not self.content:
            return 0
        return len(self.content.splitlines())


@dataclass(frozen=True)
class ExactReadProcess:
    pid: int
    process: str


@dataclass(frozen=True)
class ExactReadEvent:
    event_index: int
    pid: int
    process: str
    path: str
    operation: str
    evidence_kind: str
    offset: int
    bytes: int
    content: bytes
    content_sha256: str
    file_sha256: str
    line_start: int | None = None
    line_end: int | None = None


@dataclass(frozen=True)
class ExactReadTrace:
    schema_version: str | None
    run_id: str | None
    case_id: str | None
    trace_id: str | None
    source: str | None
    authority: str | None
    status: str
    events: tuple[ExactReadEvent, ...] = ()
    files: tuple[ExactReadFile, ...] = ()
    processes: tuple[ExactReadProcess, ...] = ()
    invalid_reasons: tuple[str, ...] = ()

    @property
    def valid(self) -> bool:
        return self.status == "available" and not self.invalid_reasons

    @property
    def read_analysis(self) -> dict[str, int]:
        """Expose repetition, overlap, and unique-byte facts without guessing."""

        signatures: set[tuple[str, int, int, str]] = set()
        repeated = 0
        intervals: dict[str, list[tuple[int, int]]] = {}
        for event in self.events:
            signature = (
                event.path,
                event.offset,
                event.bytes,
                event.content_sha256,
            )
            if signature in signatures:
                repeated += 1
            signatures.add(signature)
            intervals.setdefault(event.path, []).append(
                (event.offset, event.offset + event.bytes)
            )

        overlap = 0
        unique_bytes = 0
        for spans in intervals.values():
            active_end = -1
            merged_start = -1
            merged_end = -1
            for start, end in sorted(spans):
                if start < active_end:
                    overlap += 1
                active_end = max(active_end, end)
                if merged_start < 0:
                    merged_start, merged_end = start, end
                elif start <= merged_end:
                    merged_end = max(merged_end, end)
                else:
                    unique_bytes += merged_end - merged_start
                    merged_start, merged_end = start, end
            if merged_start >= 0:
                unique_bytes += merged_end - merged_start
        return {
            "repeated_read_count": repeated,
            "overlapping_read_count": overlap,
            "unique_bytes": unique_bytes,
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "case_id": self.case_id,
            "trace_id": self.trace_id,
            "source": self.source,
            "authority": self.authority,
            "status": self.status,
            "valid": self.valid,
            "events": [
                {
                    "event_index": event.event_index,
                    "pid": event.pid,
                    "process": event.process,
                    "path": event.path,
                    "operation": event.operation,
                    "evidence_kind": event.evidence_kind,
                    "offset": event.offset,
                    "bytes": event.bytes,
                    "content_base64": base64.b64encode(event.content).decode(
                        "ascii"
                    ),
                    "content_sha256": event.content_sha256,
                    "file_sha256": event.file_sha256,
                    "line_start": event.line_start,
                    "line_end": event.line_end,
                }
                for event in self.events
            ],
            "files": [
                {
                    "path": file.path,
                    "file_size": file.file_size,
                    "content_sha256": file.content_sha256,
                    "content_kind": file.content_kind,
                    "line_count": file.line_count,
                }
                for file in self.files
            ],
            "processes": [
                {"pid": process.pid, "process": process.process}
                for process in self.processes
            ],
            "invalid_reasons": list(self.invalid_reasons),
            "analysis": self.read_analysis,
        }


def parse_exact_read_trace(
    lines: Iterable[str],
    *,
    expected_run_id: str | None = None,
    expected_case_id: str | None = None,
) -> ExactReadTrace:
    """Parse and validate an ``exact-read-1`` JSONL sidecar.

    A returned read is valid only when its bytes are present, its file snapshot
    exists, its declared hash matches that snapshot, and the returned bytes
    equal the declared offset within that snapshot.  Any gap is a hard
    invalidation, never an estimate.
    """

    metadata: dict[str, object] | None = None
    ended_metadata: dict[str, object] | None = None
    raw_events: list[dict[str, object]] = []
    snapshots: list[dict[str, object]] = []
    process_records: list[dict[str, object]] = []
    reasons: list[str] = []

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            reasons.append(f"line {line_number}: malformed JSON: {exc.msg}")
            continue
        if not isinstance(payload, dict):
            reasons.append(f"line {line_number}: record is not an object")
            continue
        record_type = payload.get("type")
        if record_type == "exact-read.trace.started":
            if metadata is not None:
                for field in (
                    "schema_version",
                    "run_id",
                    "case_id",
                    "trace_id",
                    "source",
                    "authority",
                    "status",
                    "capture_mode",
                ):
                    if payload.get(field) != metadata.get(field):
                        reasons.append(
                            f"line {line_number}: duplicate metadata differs in {field}"
                        )
            else:
                metadata = payload
        elif record_type == "exact-read.access":
            raw_events.append(payload)
        elif record_type == "exact-read.file.snapshot":
            snapshots.append(payload)
        elif record_type == "exact-read.process.started":
            process_records.append(payload)
        elif record_type == "exact-read.process.ended":
            continue
        elif record_type == "exact-read.trace.ended":
            if ended_metadata is not None:
                reasons.append(f"line {line_number}: duplicate trace end metadata")
            else:
                ended_metadata = payload
        elif record_type == "exact-read.gap":
            reason = payload.get("reason")
            reasons.append(f"capture gap: {reason}")
        else:
            reasons.append(f"line {line_number}: unsupported record {record_type!r}")

    if metadata is None:
        reasons.append("missing exact-read.trace.started metadata")
        return ExactReadTrace(
            schema_version=None,
            run_id=None,
            case_id=None,
            trace_id=None,
            source=None,
            authority=None,
            status="malformed",
            invalid_reasons=tuple(dict.fromkeys(reasons)),
        )

    schema_version = _required_string(metadata, "schema_version", reasons)
    run_id = _required_string(metadata, "run_id", reasons)
    case_id = _required_string(metadata, "case_id", reasons)
    trace_id = _required_string(metadata, "trace_id", reasons)
    source = _required_string(metadata, "source", reasons)
    authority = _required_string(metadata, "authority", reasons)
    declared_status = _required_string(metadata, "status", reasons)
    if schema_version != "exact-read-1":
        reasons.append(f"unsupported exact-read schema: {schema_version!r}")
    if metadata.get("capture_mode") != "exact":
        reasons.append("trace is not declared capture_mode='exact'")
    if declared_status != "available":
        reasons.append(f"trace status is not available: {declared_status!r}")
    if ended_metadata is None:
        reasons.append("missing exact-read.trace.ended metadata")
    else:
        _check_identity(ended_metadata, run_id, case_id, trace_id, reasons)
        if ended_metadata.get("status") != "complete":
            reasons.append(
                "trace end status is not complete: "
                f"{ended_metadata.get('status')!r}"
            )
    for name, actual, expected in (
        ("run_id", run_id, expected_run_id),
        ("case_id", case_id, expected_case_id),
    ):
        if expected is not None and actual != expected:
            reasons.append(f"{name} {actual!r} does not match expected {expected!r}")

    files: dict[str, ExactReadFile] = {}
    for snapshot in snapshots:
        _check_identity(snapshot, run_id, case_id, trace_id, reasons)
        path = _required_string(snapshot, "path", reasons)
        raw_content = _decode_content(snapshot, "content_base64", reasons)
        if path is None or raw_content is None:
            continue
        try:
            file_size = int(snapshot["file_size"])
        except (KeyError, TypeError, ValueError):
            reasons.append(f"snapshot {path!r} has invalid file_size")
            continue
        declared_hash = _required_string(snapshot, "content_sha256", reasons)
        actual_hash = hashlib.sha256(raw_content).hexdigest()
        if declared_hash != actual_hash:
            reasons.append(f"snapshot {path!r} content hash does not match")
        if file_size != len(raw_content):
            reasons.append(f"snapshot {path!r} file_size does not match content")
        if path in files and files[path].content_sha256 != actual_hash:
            reasons.append(f"file {path!r} has conflicting snapshots")
        files[path] = ExactReadFile(
            path,
            file_size,
            raw_content,
            actual_hash,
            _content_kind(raw_content),
        )

    processes: dict[int, ExactReadProcess] = {}
    for process in process_records:
        _check_identity(process, run_id, case_id, trace_id, reasons)
        try:
            pid = int(process["pid"])
            name = str(process["process"])
        except (KeyError, TypeError, ValueError):
            reasons.append("process record has invalid pid or process")
            continue
        if pid < 1 or not name:
            reasons.append("process record has invalid identity")
            continue
        processes[pid] = ExactReadProcess(pid, name)

    events: list[ExactReadEvent] = []
    for raw in raw_events:
        _check_identity(raw, run_id, case_id, trace_id, reasons)
        event = _parse_event(raw, reasons)
        if event is None:
            continue
        file = files.get(event.path)
        if file is None:
            reasons.append(f"read {event.path!r} has no immutable snapshot")
            events.append(event)
            continue
        if event.file_sha256 != file.content_sha256:
            reasons.append(f"read {event.path!r} does not match snapshot version")
        end = event.offset + event.bytes
        if end > len(file.content):
            reasons.append(f"read {event.path!r} exceeds snapshot bounds")
        elif file.content[event.offset:end] != event.content:
            reasons.append(f"read {event.path!r} returned bytes do not match snapshot")
        line_start, line_end = (
            _line_span(file.content, event.offset, event.bytes)
            if file.content_kind == "text"
            else (None, None)
        )
        events.append(
            ExactReadEvent(
                **{**event.__dict__, "line_start": line_start, "line_end": line_end}
            )
        )
        if event.pid not in processes:
            reasons.append(f"read {event.path!r} belongs to unregistered process {event.pid}")

    status = "available" if not reasons else "partial"
    return ExactReadTrace(
        schema_version=schema_version,
        run_id=run_id,
        case_id=case_id,
        trace_id=trace_id,
        source=source,
        authority=authority,
        status=status,
        events=tuple(events),
        files=tuple(files.values()),
        processes=tuple(processes.values()),
        invalid_reasons=tuple(dict.fromkeys(reasons)),
    )


def _parse_event(
    raw: dict[str, object], reasons: list[str]
) -> ExactReadEvent | None:
    path = _required_string(raw, "path", reasons)
    process = _required_string(raw, "process", reasons)
    file_sha256 = _required_string(raw, "file_sha256", reasons)
    content = _decode_content(raw, "content_base64", reasons)
    if path is None or process is None or file_sha256 is None or content is None:
        return None
    try:
        event_index = int(raw["event_index"])
        pid = int(raw["pid"])
        offset = int(raw["offset"])
        byte_count = int(raw["bytes"])
    except (KeyError, TypeError, ValueError):
        reasons.append(f"read {path!r} has invalid event coordinates")
        return None
    operation = str(raw.get("operation", ""))
    evidence_kind = str(raw.get("evidence_kind", ""))
    if event_index < 0 or pid < 1 or offset < 0 or byte_count < 0:
        reasons.append(f"read {path!r} has negative coordinates")
    if evidence_kind != "returned":
        reasons.append(f"read {path!r} is not returned-byte evidence")
    if byte_count != len(content):
        reasons.append(f"read {path!r} byte count does not match content")
    content_sha256 = hashlib.sha256(content).hexdigest()
    declared_content_hash = raw.get("content_sha256")
    if declared_content_hash is not None and declared_content_hash != content_sha256:
        reasons.append(f"read {path!r} content hash does not match content")
    return ExactReadEvent(
        event_index=event_index,
        pid=pid,
        process=process,
        path=path,
        operation=operation,
        evidence_kind=evidence_kind,
        offset=offset,
        bytes=byte_count,
        content=content,
        content_sha256=content_sha256,
        file_sha256=file_sha256,
    )


def _decode_content(
    payload: dict[str, object], field: str, reasons: list[str]
) -> bytes | None:
    raw = payload.get(field)
    if not isinstance(raw, str):
        reasons.append(f"{payload.get('path', 'read')!r} missing {field}")
        return None
    try:
        return base64.b64decode(raw.encode("ascii"), validate=True)
    except (ValueError, UnicodeEncodeError):
        reasons.append(f"{payload.get('path', 'read')!r} has invalid {field}")
        return None


def _required_string(
    payload: dict[str, object], field: str, reasons: list[str]
) -> str | None:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        reasons.append(f"record missing non-empty {field}")
        return None
    return value


def _check_identity(
    payload: dict[str, object],
    run_id: str | None,
    case_id: str | None,
    trace_id: str | None,
    reasons: list[str],
) -> None:
    for field, expected in (
        ("run_id", run_id),
        ("case_id", case_id),
        ("trace_id", trace_id),
    ):
        if expected is not None and payload.get(field) != expected:
            reasons.append(
                f"record {field} {payload.get(field)!r} does not match trace metadata"
            )


def _line_span(content: bytes, offset: int, byte_count: int) -> tuple[int | None, int | None]:
    if byte_count == 0:
        return None, None
    start = content[:offset].count(b"\n") + 1
    end_position = offset + byte_count - 1
    end_prefix = (
        content[:end_position]
        if content[end_position : end_position + 1] == b"\n"
        else content[: end_position + 1]
    )
    end = end_prefix.count(b"\n") + 1
    return start, end


def _content_kind(content: bytes) -> str:
    """Conservatively classify bytes before exposing line coordinates.

    A line number is only meaningful for UTF-8 text without embedded NULs or
    other control bytes. Ambiguous content is kept byte-exact and treated as
    binary rather than receiving guessed line numbers.
    """

    if b"\x00" in content:
        return "binary"
    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError:
        return "binary"
    if any(
        ord(character) < 0x20 and character not in "\n\r\t\f\b"
        for character in decoded
    ):
        return "binary"
    return "text"
