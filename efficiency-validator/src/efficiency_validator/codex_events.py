import json
from dataclasses import dataclass
from typing import Iterable, Literal


EventKind = Literal["command_execution", "agent_message"]
TurnStatus = Literal["completed", "failed", "incomplete"]


@dataclass(frozen=True)
class TokenUsage:
    """Provider-reported usage from one completed Codex turn.

    ``input_tokens`` already includes the cached portion in the Codex JSONL
    contract.  ``cached_input_tokens`` and ``cache_write_input_tokens`` are
    dimensions of that input total, not additional tokens to add to it.
    """

    input_tokens: int
    cached_input_tokens: int
    cache_write_input_tokens: int
    output_tokens: int
    reasoning_output_tokens: int

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def to_dict(self) -> dict[str, int]:
        return {
            "input_tokens": self.input_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "cache_write_input_tokens": self.cache_write_input_tokens,
            "output_tokens": self.output_tokens,
            "reasoning_output_tokens": self.reasoning_output_tokens,
            "total_tokens": self.total_tokens,
        }


@dataclass(frozen=True)
class TokenUsageRecord:
    """An authoritative usage observation and its JSONL source location."""

    turn_index: int
    event_index: int
    usage: TokenUsage
    source: Literal["codex-exec-json"] = "codex-exec-json"

    def to_dict(self) -> dict[str, object]:
        return {
            "turn_index": self.turn_index,
            "event_index": self.event_index,
            "source": self.source,
            "usage": self.usage.to_dict(),
        }


@dataclass(frozen=True)
class TurnObservation:
    """Lifecycle evidence for a turn, including failed/incomplete turns."""

    turn_index: int
    started_event_index: int | None
    terminal_event_index: int | None
    status: TurnStatus
    usage: TokenUsageRecord | None = None


@dataclass(frozen=True)
class CodexEvent:
    event_index: int
    kind: EventKind
    item_id: str
    command: str | None = None
    text: str | None = None
    exit_code: int | None = None
    status: str | None = None


@dataclass(frozen=True)
class ParseIssue:
    line_number: int
    kind: Literal[
        "non_json",
        "malformed_json",
        "invalid_payload",
        "missing_field",
        "invalid_usage",
    ]
    detail: str


@dataclass(frozen=True)
class RawCodexEvent:
    """Lossless JSON evidence retained for every valid protocol event."""

    event_index: int
    event_type: str
    item_type: str | None
    payload: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "event_index": self.event_index,
            "event_type": self.event_type,
            "item_type": self.item_type,
            "payload": self.payload,
        }


@dataclass(frozen=True)
class ParsedCodexEvents:
    events: tuple[CodexEvent, ...]
    issues: tuple[ParseIssue, ...]
    thread_id: str | None = None
    turns: tuple[TurnObservation, ...] = ()
    token_usage: tuple[TokenUsageRecord, ...] = ()
    raw_events: tuple[RawCodexEvent, ...] = ()

    @property
    def complete(self) -> bool:
        """Whether the input was syntactically clean and fully parseable.

        Process completion still belongs to the run manifest. This property
        only describes the JSONL stream passed to the parser.
        """

        return not self.issues and all(
            turn.status == "completed" and turn.usage is not None
            for turn in self.turns
        )


def parse_codex_stream(lines: Iterable[str]) -> ParsedCodexEvents:
    """Parse observable events while quarantining malformed input.

    Structural thread and turn events are retained as lifecycle and usage
    evidence. The result preserves command text and returned output but does
    not claim to know every filesystem access performed by a shell command.
    Non-JSON diagnostics and malformed records become issues instead of being
    mistaken for a complete capture.
    """

    events: list[CodexEvent] = []
    issues: list[ParseIssue] = []
    thread_id: str | None = None
    turns: list[TurnObservation] = []
    token_usage: list[TokenUsageRecord] = []
    raw_events: list[RawCodexEvent] = []
    active_turn: tuple[int, int | None] | None = None
    next_turn_index = 1
    for event_index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except UnicodeDecodeError as exc:
            issues.append(
                ParseIssue(event_index, "non_json", f"decode error: {exc}")
            )
            continue
        except json.JSONDecodeError as exc:
            kind: Literal["non_json", "malformed_json"] = "non_json"
            if line.lstrip().startswith(("{", "[")):
                kind = "malformed_json"
            issues.append(ParseIssue(event_index, kind, str(exc)))
            continue

        if not isinstance(payload, dict):
            issues.append(
                ParseIssue(
                    event_index,
                    "invalid_payload",
                    "JSON value is not an object",
                )
            )
            continue

        item = payload.get("item")
        raw_events.append(
            RawCodexEvent(
                event_index=event_index,
                event_type=str(payload.get("type", "unknown")),
                item_type=(
                    str(item.get("type"))
                    if isinstance(item, dict) and item.get("type") is not None
                    else None
                ),
                payload=payload,
            )
        )

        event_type = payload.get("type")
        if event_type == "thread.started":
            value = payload.get("thread_id")
            if value is None:
                issues.append(
                    ParseIssue(
                        event_index,
                        "missing_field",
                        "thread.started requires thread_id",
                    )
                )
            else:
                thread_id = str(value)
            continue

        if event_type == "turn.started":
            if active_turn is not None:
                turns.append(
                    TurnObservation(
                        turn_index=active_turn[0],
                        started_event_index=active_turn[1],
                        terminal_event_index=None,
                        status="incomplete",
                    )
                )
            active_turn = (next_turn_index, event_index)
            next_turn_index += 1
            continue

        if event_type in {"turn.completed", "turn.failed"}:
            if active_turn is None:
                active_turn = (next_turn_index, None)
                next_turn_index += 1
            turn_index, started_event_index = active_turn
            if event_type == "turn.failed":
                turns.append(
                    TurnObservation(
                        turn_index=turn_index,
                        started_event_index=started_event_index,
                        terminal_event_index=event_index,
                        status="failed",
                    )
                )
                active_turn = None
                continue

            raw_usage = payload.get("usage")
            usage = _parse_usage(raw_usage)
            if usage is None:
                issues.append(
                    ParseIssue(
                        event_index,
                        "missing_field" if raw_usage is None else "invalid_usage",
                        "turn.completed requires a non-negative usage object",
                    )
                )
                turns.append(
                    TurnObservation(
                        turn_index=turn_index,
                        started_event_index=started_event_index,
                        terminal_event_index=event_index,
                        status="completed",
                    )
                )
            else:
                record = TokenUsageRecord(
                    turn_index=turn_index,
                    event_index=event_index,
                    usage=usage,
                )
                token_usage.append(record)
                turns.append(
                    TurnObservation(
                        turn_index=turn_index,
                        started_event_index=started_event_index,
                        terminal_event_index=event_index,
                        status="completed",
                        usage=record,
                    )
                )
            active_turn = None
            continue

        if event_type != "item.completed":
            continue

        item = payload.get("item", {})
        if not isinstance(item, dict):
            issues.append(
                ParseIssue(
                    event_index,
                    "invalid_payload",
                    "completed item is not an object",
                )
            )
            continue
        item_type = item.get("type")
        if item_type == "command_execution":
            if "id" not in item or "command" not in item:
                issues.append(
                    ParseIssue(
                        event_index,
                        "missing_field",
                        "command_execution requires id and command",
                    )
                )
                continue
            events.append(
                CodexEvent(
                    event_index=event_index,
                    kind="command_execution",
                    item_id=str(item["id"]),
                    command=str(item["command"]),
                    text=str(item.get("aggregated_output", "")),
                    exit_code=(
                        None
                        if item.get("exit_code") is None
                        else int(item["exit_code"])
                    ),
                    status=(
                        None
                        if item.get("status") is None
                        else str(item["status"])
                    ),
                )
            )
        elif item_type == "agent_message":
            if "id" not in item:
                issues.append(
                    ParseIssue(
                        event_index,
                        "missing_field",
                        "agent_message requires id",
                    )
                )
                continue
            events.append(
                CodexEvent(
                    event_index=event_index,
                    kind="agent_message",
                    item_id=str(item["id"]),
                    text=str(item.get("text", "")),
                )
            )
    if active_turn is not None:
        turns.append(
            TurnObservation(
                turn_index=active_turn[0],
                started_event_index=active_turn[1],
                terminal_event_index=None,
                status="incomplete",
            )
        )

    return ParsedCodexEvents(
        events=tuple(events),
        issues=tuple(issues),
        thread_id=thread_id,
        turns=tuple(turns),
        token_usage=tuple(token_usage),
        raw_events=tuple(raw_events),
    )


def _parse_usage(payload: object) -> TokenUsage | None:
    if not isinstance(payload, dict):
        return None
    names = (
        "input_tokens",
        "cached_input_tokens",
        "output_tokens",
        "reasoning_output_tokens",
    )
    values: list[int] = []
    for name in names:
        value = payload.get(name)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            return None
        values.append(value)
    cache_write = payload.get("cache_write_input_tokens", 0)
    if (
        isinstance(cache_write, bool)
        or not isinstance(cache_write, int)
        or cache_write < 0
    ):
        return None
    return TokenUsage(
        input_tokens=values[0],
        cached_input_tokens=values[1],
        cache_write_input_tokens=cache_write,
        output_tokens=values[2],
        reasoning_output_tokens=values[3],
    )


def parse_codex_events(lines: Iterable[str]) -> list[CodexEvent]:
    """Compatibility wrapper returning only parsed actionable events.

    New collection code should use :func:`parse_codex_stream` so diagnostics
    and incomplete captures remain visible to the evaluator.
    """

    return list(parse_codex_stream(lines).events)
