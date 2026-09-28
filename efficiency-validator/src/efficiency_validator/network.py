"""Conservative network metadata evidence without retaining payloads."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from typing import Iterable, Literal


NetworkSource = Literal["macos-fs-usage", "nettop", "structured-runtime"]
NetworkAuthority = Literal[
    "os-kernel-observation",
    "structured-runtime-observation",
]
NetworkStatus = Literal[
    "available",
    "unavailable",
    "denied",
    "partial",
    "malformed",
    "truncated",
]


@dataclass(frozen=True)
class NetworkEvent:
    run_id: str
    case_id: str
    trace_id: str
    event_index: int
    timestamp: str
    source: NetworkSource
    authority: NetworkAuthority
    destination: str
    process: str | None = None
    pid: int | None = None
    protocol: str | None = None
    duration_ms: int | None = None
    bytes_sent: int | None = None
    bytes_received: int | None = None
    result: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class NetworkParseIssue:
    line_number: int
    kind: Literal["non_json", "malformed_json", "invalid_payload", "mismatch"]
    detail: str


@dataclass(frozen=True)
class ParsedNetworkTrace:
    schema_version: str | None
    run_id: str | None
    case_id: str | None
    trace_id: str | None
    source: NetworkSource | None
    authority: NetworkAuthority | None
    status: NetworkStatus
    events: tuple[NetworkEvent, ...]
    issues: tuple[NetworkParseIssue, ...]

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


def parse_network_trace(
    lines: Iterable[str],
    *,
    expected_run_id: str | None = None,
    expected_case_id: str | None = None,
) -> ParsedNetworkTrace:
    events: list[NetworkEvent] = []
    issues: list[NetworkParseIssue] = []
    metadata: dict[str, object] | None = None
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(NetworkParseIssue(line_number, "malformed_json", str(exc)))
            continue
        if not isinstance(payload, dict):
            issues.append(
                NetworkParseIssue(line_number, "invalid_payload", "JSON value is not an object")
            )
            continue
        if payload.get("type") == "network.trace.started":
            if metadata is not None:
                issues.append(NetworkParseIssue(line_number, "invalid_payload", "duplicate metadata"))
            else:
                metadata = payload
            continue
        if payload.get("type") != "network.access":
            issues.append(NetworkParseIssue(line_number, "invalid_payload", "expected network record"))
            continue
        try:
            events.append(_event_from_dict(payload))
        except (KeyError, TypeError, ValueError) as exc:
            issues.append(NetworkParseIssue(line_number, "invalid_payload", str(exc)))

    if metadata is None:
        issues.append(NetworkParseIssue(0, "invalid_payload", "missing network metadata"))
        return ParsedNetworkTrace(None, None, None, None, None, None, "malformed", tuple(events), tuple(issues))
    try:
        schema_version = _required_string(metadata, "schema_version")
        run_id = _required_string(metadata, "run_id")
        case_id = _required_string(metadata, "case_id")
        trace_id = _required_string(metadata, "trace_id")
        source = _literal_source(metadata.get("source"))
        authority = _literal_authority(metadata.get("authority"))
        status = _literal_status(metadata.get("status"))
    except (TypeError, ValueError) as exc:
        issues.append(NetworkParseIssue(1, "invalid_payload", str(exc)))
        return ParsedNetworkTrace(None, None, None, None, None, None, "malformed", tuple(events), tuple(issues))

    if schema_version != "network-trace-1":
        issues.append(NetworkParseIssue(1, "mismatch", f"unsupported schema: {schema_version!r}"))
    for name, actual, expected in (("run_id", run_id, expected_run_id), ("case_id", case_id, expected_case_id)):
        if expected is not None and actual != expected:
            issues.append(NetworkParseIssue(1, "mismatch", f"{name} does not match expected"))
    for event in events:
        for name, actual, expected in (
            ("run_id", event.run_id, run_id),
            ("case_id", event.case_id, case_id),
            ("trace_id", event.trace_id, trace_id),
            ("source", event.source, source),
            ("authority", event.authority, authority),
        ):
            if actual != expected:
                issues.append(NetworkParseIssue(0, "mismatch", f"event {name} mismatches metadata"))
    if issues and status == "available":
        status = "partial"
    return ParsedNetworkTrace(schema_version, run_id, case_id, trace_id, source, authority, status, tuple(events), tuple(issues))


def summarize_network(parsed: ParsedNetworkTrace) -> dict[str, object]:
    return {
        "status": parsed.status,
        "event_count": len(parsed.events),
        "destination_count": len({event.destination for event in parsed.events}),
        "total_bytes_sent": sum(event.bytes_sent or 0 for event in parsed.events),
        "total_bytes_received": sum(event.bytes_received or 0 for event in parsed.events),
        "total_bytes": sum(
            (event.bytes_sent or 0) + (event.bytes_received or 0)
            for event in parsed.events
        ),
        "destinations": sorted({event.destination for event in parsed.events}),
    }


def _event_from_dict(payload: dict[str, object]) -> NetworkEvent:
    return NetworkEvent(
        run_id=_required_string(payload, "run_id"),
        case_id=_required_string(payload, "case_id"),
        trace_id=_required_string(payload, "trace_id"),
        event_index=_non_negative_int(payload, "event_index"),
        timestamp=_required_string(payload, "timestamp"),
        source=_literal_source(payload.get("source")),
        authority=_literal_authority(payload.get("authority")),
        destination=_required_string(payload, "destination"),
        process=_optional_string(payload, "process"),
        pid=_optional_non_negative_int(payload, "pid"),
        protocol=_optional_string(payload, "protocol"),
        duration_ms=_optional_non_negative_int(payload, "duration_ms"),
        bytes_sent=_optional_non_negative_int(payload, "bytes_sent"),
        bytes_received=_optional_non_negative_int(payload, "bytes_received"),
        result=_optional_string(payload, "result"),
    )


def _required_string(payload: dict[str, object], name: str) -> str:
    value = payload.get(name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _optional_string(payload: dict[str, object], name: str) -> str | None:
    value = payload.get(name)
    return None if value is None else _required_string(payload, name)


def _non_negative_int(payload: dict[str, object], name: str) -> int:
    value = payload.get(name)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def _optional_non_negative_int(payload: dict[str, object], name: str) -> int | None:
    return None if payload.get(name) is None else _non_negative_int(payload, name)


def _literal_source(value: object) -> NetworkSource:
    if value not in {"macos-fs-usage", "nettop", "structured-runtime"}:
        raise ValueError(f"invalid network source: {value!r}")
    return value  # type: ignore[return-value]


def _literal_authority(value: object) -> NetworkAuthority:
    if value not in {"os-kernel-observation", "structured-runtime-observation"}:
        raise ValueError(f"invalid network authority: {value!r}")
    return value  # type: ignore[return-value]


def _literal_status(value: object) -> NetworkStatus:
    if value not in {"available", "unavailable", "denied", "partial", "malformed", "truncated"}:
        raise ValueError(f"invalid network status: {value!r}")
    return value  # type: ignore[return-value]
