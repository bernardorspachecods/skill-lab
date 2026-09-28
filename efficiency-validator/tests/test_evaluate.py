from efficiency_validator.codex_events import CodexEvent, ParsedCodexEvents
from efficiency_validator.evaluate import evaluate_command_trace, evaluate_trace
from efficiency_validator.schema import TraceEvent


def test_evaluator_reports_route_and_retrieval_cost_from_trace() -> None:
    events = [
        TraceEvent(
            run_id="run-1",
            case_id="001-create-task",
            event_index=1,
            operation="search",
            paths=["docs/product/rules.md"],
            scanned_paths=["docs/product/rules.md", "docs/operations/local-development.md"],
            result_count=1,
            tokens=0,
        ),
        TraceEvent(
            run_id="run-1",
            case_id="001-create-task",
            event_index=2,
            operation="read",
            paths=["docs/product/rules.md"],
            tokens=30,
        ),
        TraceEvent(
            run_id="run-1",
            case_id="001-create-task",
            event_index=3,
            operation="read",
            paths=["apps/api/src/context_lab_api/app.py"],
            tokens=20,
        ),
        TraceEvent(
            run_id="run-1",
            case_id="001-create-task",
            event_index=4,
            operation="read",
            paths=["README.md"],
            tokens=10,
        ),
    ]
    oracle = {
        "authoritative_paths": ["docs/product/rules.md"],
        "implementation_paths": ["apps/api/src/context_lab_api/app.py"],
        "supporting_tests": [],
    }

    report = evaluate_trace(events, oracle)

    assert report.first_authoritative_path == "docs/product/rules.md"
    assert report.unique_paths_requested == 3
    assert report.unique_paths_read == 3
    assert report.relevant_paths_read == 2
    assert report.irrelevant_paths_read == 1
    assert report.scanned_paths == 2
    assert report.tokens_read == 60
    assert report.searches_without_results == 0


def test_command_evaluator_reports_observable_actions_and_claim_coverage() -> None:
    events = [
        CodexEvent(
            event_index=1,
            kind="command_execution",
            item_id="item-1",
            command="sed -n '1,80p' docs/product/rules.md",
            text="# Product Rules",
            exit_code=0,
            status="completed",
        ),
        CodexEvent(
            event_index=2,
            kind="agent_message",
            item_id="item-2",
            text="The membership rule is required.",
        ),
    ]
    parsed = ParsedCodexEvents(events=tuple(events), issues=())
    oracle = {
        "required_claims": [
            {"id": "membership", "description": "Membership is required."},
            {"id": "api-delegation", "description": "The API delegates."},
        ]
    }

    report = evaluate_command_trace(
        parsed,
        oracle,
        identified_claim_ids=["membership"],
    )

    assert report.command_count == 1
    assert report.agent_message_count == 1
    assert report.final_agent_message == "The membership rule is required."
    assert report.file_level_metrics == "unavailable"
    assert report.claim_coverage.identified_claim_ids == ("membership",)
    assert report.claim_coverage.missing_claim_ids == ("api-delegation",)


def test_first_authoritative_path_requires_a_structured_read() -> None:
    events = [
        TraceEvent(
            run_id="run-1",
            case_id="case-1",
            event_index=1,
            operation="search",
            paths=["docs/product/rules.md"],
            result_count=1,
            tokens=0,
        ),
        TraceEvent(
            run_id="run-1",
            case_id="case-1",
            event_index=2,
            operation="read",
            paths=["docs/operations/local-development.md"],
            tokens=10,
        ),
    ]

    report = evaluate_trace(
        events,
        {"authoritative_paths": ["docs/product/rules.md"]},
    )

    assert report.first_authoritative_path is None
