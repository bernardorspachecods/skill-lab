from dataclasses import dataclass
from typing import Iterable

from .codex_events import CodexEvent, ParsedCodexEvents
from .schema import TraceEvent


@dataclass(frozen=True)
class TraceReport:
    first_authoritative_path: str | None
    unique_paths_requested: int
    unique_paths_read: int
    relevant_paths_read: int
    irrelevant_paths_read: int
    scanned_paths: int
    tokens_read: int | None
    searches_without_results: int


@dataclass(frozen=True)
class ClaimCoverage:
    required_claim_ids: tuple[str, ...]
    identified_claim_ids: tuple[str, ...]
    missing_claim_ids: tuple[str, ...]
    coverage_ratio: float


@dataclass(frozen=True)
class CommandTraceReport:
    stream_complete: bool
    parser_issue_count: int
    command_count: int
    failed_command_count: int
    agent_message_count: int
    final_agent_message: str | None
    file_level_metrics: str
    claim_coverage: ClaimCoverage


def evaluate_command_trace(
    parsed: ParsedCodexEvents,
    oracle: dict[str, object],
    *,
    identified_claim_ids: Iterable[str] = (),
) -> CommandTraceReport:
    """Evaluate only evidence the Codex JSONL adapter actually exposes.

    The command-level report deliberately does not infer file reads, search
    results, scanned paths, or tokens from shell commands. Answer claims are
    supplied as normalized claim ids by a separate review step, then compared
    deterministically with the oracle's required claims.
    """

    events = sorted(parsed.events, key=lambda event: event.event_index)
    commands = [event for event in events if event.kind == "command_execution"]
    messages = [event for event in events if event.kind == "agent_message"]
    identified = tuple(
        dict.fromkeys(
            claim_id
            for claim_id in identified_claim_ids
            if claim_id in _required_claim_ids(oracle)
        )
    )
    required = _required_claim_ids(oracle)
    missing = tuple(claim_id for claim_id in required if claim_id not in identified)
    coverage_ratio = len(identified) / len(required) if required else 1.0
    return CommandTraceReport(
        stream_complete=parsed.complete,
        parser_issue_count=len(parsed.issues),
        command_count=len(commands),
        failed_command_count=sum(_command_failed(event) for event in commands),
        agent_message_count=len(messages),
        final_agent_message=messages[-1].text if messages else None,
        file_level_metrics="unavailable",
        claim_coverage=ClaimCoverage(
            required_claim_ids=required,
            identified_claim_ids=identified,
            missing_claim_ids=missing,
            coverage_ratio=coverage_ratio,
        ),
    )


def evaluate_trace(
    events: Iterable[TraceEvent], oracle: dict[str, object]
) -> TraceReport:
    ordered_events = sorted(events, key=lambda event: event.event_index)
    authoritative = _paths_from_oracle(oracle, "authoritative_paths")
    expected = (
        authoritative
        | _paths_from_oracle(oracle, "implementation_paths")
        | _paths_from_oracle(oracle, "allowed_implementation_paths")
        | _paths_from_oracle(oracle, "supporting_tests")
    )
    requested = {path for event in ordered_events for path in event.paths}
    read = {
        path
        for event in ordered_events
        if event.operation == "read"
        for path in event.paths
    }
    scanned = {
        path for event in ordered_events for path in event.scanned_paths
    }
    first_authoritative = next(
        (
            path
            for event in ordered_events
            if event.operation == "read"
            for path in event.paths
            if path in authoritative
        ),
        None,
    )
    return TraceReport(
        first_authoritative_path=first_authoritative,
        unique_paths_requested=len(requested),
        unique_paths_read=len(read),
        relevant_paths_read=len(read & expected),
        irrelevant_paths_read=len(read - expected),
        scanned_paths=len(scanned),
        tokens_read=(
            None
            if any(event.tokens is None for event in ordered_events)
            else sum(event.tokens or 0 for event in ordered_events)
        ),
        searches_without_results=sum(
            event.operation == "search" and event.result_count == 0
            for event in ordered_events
        ),
    )


def _command_failed(event: CodexEvent) -> bool:
    return (event.exit_code is not None and event.exit_code != 0) or (
        event.status in {"failed", "error"}
    )


def _required_claim_ids(oracle: dict[str, object]) -> tuple[str, ...]:
    raw_claims = oracle.get("required_claims", [])
    claim_ids: list[str] = []
    if not isinstance(raw_claims, list):
        return ()
    for claim in raw_claims:
        if isinstance(claim, str):
            claim_ids.append(claim)
        elif isinstance(claim, dict) and "id" in claim:
            claim_ids.append(str(claim["id"]))
    return tuple(dict.fromkeys(claim_ids))


def _paths_from_oracle(oracle: dict[str, object], key: str) -> set[str]:
    value = oracle.get(key, [])
    if not isinstance(value, list):
        return set()
    return {str(path) for path in value}
