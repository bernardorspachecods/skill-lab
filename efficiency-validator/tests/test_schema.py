import pytest

from efficiency_validator.schema import TraceEvent


def test_trace_event_keeps_missing_measurements_distinct_from_zero() -> None:
    event = TraceEvent.from_dict(
        {
            "run_id": "run-1",
            "case_id": "001-create-task",
            "event_index": 1,
            "operation": "read",
            "paths": ["docs/product/rules.md"],
        }
    )

    assert event.tokens is None
    assert event.result_count is None


def test_trace_event_rejects_invalid_operations_and_counts() -> None:
    with pytest.raises(ValueError, match="operation"):
        TraceEvent.from_dict(
            {
                "run_id": "run-1",
                "case_id": "case-1",
                "event_index": 1,
                "operation": "shell",
            }
        )

    with pytest.raises(ValueError, match="tokens"):
        TraceEvent.from_dict(
            {
                "run_id": "run-1",
                "case_id": "case-1",
                "event_index": 1,
                "operation": "read",
                "tokens": -1,
            }
        )
