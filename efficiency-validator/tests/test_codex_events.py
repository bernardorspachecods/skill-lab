import json
from pathlib import Path

from efficiency_validator.codex_events import (
    parse_codex_events,
    parse_codex_stream,
)


FIXTURES = Path(__file__).parent / "fixtures" / "codex"


def _fixture(name: str) -> list[str]:
    return (FIXTURES / name).read_text(encoding="utf-8").splitlines()


def test_parser_keeps_observable_command_and_final_message_events() -> None:
    lines = [
        json.dumps({"type": "thread.started", "thread_id": "thread-1"}),
        json.dumps(
            {
                "type": "item.completed",
                "item": {
                    "id": "item-1",
                    "type": "command_execution",
                    "command": "sed -n '1,80p' docs/product/rules.md",
                    "aggregated_output": "# Product Rules",
                    "exit_code": 0,
                    "status": "completed",
                },
            }
        ),
        json.dumps(
            {
                "type": "item.completed",
                "item": {
                    "id": "item-2",
                    "type": "agent_message",
                    "text": "The task path is documented.",
                },
            }
        ),
        json.dumps({"type": "turn.completed"}),
    ]

    events = parse_codex_events(lines)

    assert len(events) == 2
    assert events[0].kind == "command_execution"
    assert events[0].command.startswith("sed -n")
    assert events[0].exit_code == 0
    assert events[1].kind == "agent_message"
    assert events[1].text == "The task path is documented."


def test_parser_quarantines_diagnostics_and_malformed_lines() -> None:
    result = parse_codex_stream(
        [
            "WARNING: runtime diagnostic",
            "{not-json}",
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {
                        "id": "item-1",
                        "type": "command_execution",
                        "command": "rg task",
                        "aggregated_output": "",
                        "exit_code": 1,
                        "status": "failed",
                    },
                }
            ),
        ]
    )

    assert len(result.events) == 1
    assert result.events[0].exit_code == 1
    assert [issue.kind for issue in result.issues] == [
        "non_json",
        "malformed_json",
    ]
    assert not result.complete


def test_legacy_parser_returns_events_without_hiding_stream_issues_api() -> None:
    events = parse_codex_events(["not-json"])

    assert events == []


def test_parser_records_authoritative_turn_usage_and_derived_total() -> None:
    parsed = parse_codex_stream(_fixture("complete-turn.jsonl"))

    assert parsed.complete is True
    assert parsed.thread_id == "thread-fixture-1"
    assert len(parsed.token_usage) == 1
    record = parsed.token_usage[0]
    assert record.event_index == 4
    assert record.usage.to_dict() == {
        "input_tokens": 120,
        "cached_input_tokens": 40,
        "cache_write_input_tokens": 0,
        "output_tokens": 18,
        "reasoning_output_tokens": 7,
        "total_tokens": 138,
    }


def test_parser_preserves_every_valid_json_event_as_raw_evidence() -> None:
    parsed = parse_codex_stream(
        [
            json.dumps({"type": "thread.started", "thread_id": "thread-1"}),
            json.dumps(
                {
                    "type": "item.started",
                    "item": {
                        "id": "item-1",
                        "type": "command_execution",
                        "command": "rg task",
                    },
                }
            ),
            json.dumps({"type": "future.event", "value": {"seen": True}}),
        ]
    )

    assert [event.event_type for event in parsed.raw_events] == [
        "thread.started",
        "item.started",
        "future.event",
    ]
    assert parsed.raw_events[1].item_type == "command_execution"
    assert parsed.raw_events[2].payload == {
        "type": "future.event",
        "value": {"seen": True},
    }


def test_failed_and_truncated_turns_are_not_reported_as_complete() -> None:
    failed = parse_codex_stream(_fixture("failed-turn.jsonl"))
    truncated = parse_codex_stream(_fixture("truncated-turn.jsonl"))

    assert failed.complete is False
    assert failed.turns[0].status == "failed"
    assert failed.token_usage == ()
    assert truncated.complete is False
    assert truncated.turns[0].status == "incomplete"


def test_completed_turn_with_invalid_usage_is_quarantined() -> None:
    parsed = parse_codex_stream(
        [
            '{"type":"turn.started"}',
            '{"type":"turn.completed","usage":{"input_tokens":-1}}',
        ]
    )

    assert parsed.complete is False
    assert parsed.token_usage == ()
    assert parsed.issues[0].kind == "invalid_usage"
