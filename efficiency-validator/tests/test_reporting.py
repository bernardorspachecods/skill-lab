from efficiency_validator.codex_events import (
    CodexEvent,
    ParsedCodexEvents,
    parse_codex_stream,
)
from efficiency_validator.manifest import RunManifest
from efficiency_validator.reporting import build_command_report
from efficiency_validator.network import parse_network_trace


def test_report_links_manifest_parser_status_and_claim_coverage() -> None:
    manifest = RunManifest(
        run_id="run-1",
        case_id="001-create-task",
        repo_revision="target-commit",
        runtime_revision="sha256:runtime",
        task_hash="sha256:task",
        model="model-1",
        codex_version="codex-1",
        observer_version="0.5.0",
        launch_mode="host-runtime-pty",
        sandbox="read-only",
        ephemeral=True,
        started_at="2026-09-24T10:00:00Z",
        finished_at="2026-09-24T10:01:00Z",
        exit_code=0,
        complete=True,
        sidecar_revision="sha256:sidecar",
    )
    parsed = ParsedCodexEvents(
        events=(
            CodexEvent(
                event_index=1,
                kind="command_execution",
                item_id="item-1",
                command="sed -n '1,20p' docs/product/rules.md",
                text="rules",
                exit_code=0,
                status="completed",
            ),
        ),
        issues=(),
    )

    report = build_command_report(
        parsed,
        manifest,
        {
            "required_claims": [
                {"id": "rule", "description": "The rule is identified."}
            ]
        },
        identified_claim_ids=["rule"],
    )

    assert report["status"] == "complete"
    assert report["manifest"]["repo_revision"] == "target-commit"
    assert report["parser"]["complete"] is True
    assert report["command_trace"]["claim_coverage"]["coverage_ratio"] == 1.0


def test_report_exposes_token_usage_and_unavailable_filesystem_signal() -> None:
    parsed = parse_codex_stream(
        [
            '{"type":"thread.started","thread_id":"thread-1"}',
            '{"type":"turn.started"}',
            (
                '{"type":"turn.completed","usage":{"input_tokens":10,'
                '"cached_input_tokens":2,"cache_write_input_tokens":0,'
                '"output_tokens":3,"reasoning_output_tokens":1}}'
            ),
        ]
    )
    report = build_command_report(
        parsed,
        RunManifest(
            run_id="run-1",
            case_id="case-1",
            repo_revision="target-commit",
            runtime_revision="sha256:runtime",
            task_hash="sha256:task",
            model="model-1",
            codex_version="codex-1",
            observer_version="0.5.0",
            launch_mode="host-runtime-pty",
            sandbox="read-only",
            ephemeral=True,
            started_at="2026-09-24T10:00:00Z",
            finished_at="2026-09-24T10:01:00Z",
            exit_code=0,
            complete=True,
            sidecar_revision="sha256:sidecar",
        ),
        {"required_claims": []},
    )

    observability = report["observability"]
    assert observability["raw_event_count"] == 3
    assert [event["event_type"] for event in observability["raw_events"]] == [
        "thread.started",
        "turn.started",
        "turn.completed",
    ]
    assert observability["tokens"]["status"] == "available"
    assert observability["tokens"]["totals"]["total_tokens"] == 13
    assert observability["filesystem"]["status"] == "unavailable"


def test_report_preserves_content_returned_by_a_command_without_calling_it_a_file_read() -> None:
    parsed = parse_codex_stream(
        [
            '{"type":"thread.started","thread_id":"thread-1"}',
            '{"type":"turn.started"}',
            '{"type":"item.completed","item":{'
            '"type":"command_execution","id":"cmd-1",'
            '"command":"sed -n \'1,10p\' docs/rules.md",'
            '"aggregated_output":"line one\\nline two\\n",'
            '"status":"completed","exit_code":0}}',
            (
                '{"type":"turn.completed","usage":{"input_tokens":10,'
                '"cached_input_tokens":2,"cache_write_input_tokens":0,'
                '"output_tokens":3,"reasoning_output_tokens":1}}'
            ),
        ]
    )
    report = build_command_report(
        parsed,
        RunManifest(
            run_id="run-1",
            case_id="case-1",
            repo_revision="target-commit",
            runtime_revision="sha256:runtime",
            task_hash="sha256:task",
            model="model-1",
            codex_version="codex-1",
            observer_version="0.5.0",
            launch_mode="host-runtime-pty",
            sandbox="read-only",
            ephemeral=True,
            started_at="2026-09-24T10:00:00Z",
            finished_at="2026-09-24T10:01:00Z",
            exit_code=0,
            complete=True,
            sidecar_revision="sha256:sidecar",
        ),
        {"required_claims": []},
    )

    returned = report["observability"]["returned_content"]
    assert returned[0]["source"] == "command_aggregated_output"
    assert returned[0]["content"] == "line one\nline two\n"
    assert report["observability"]["filesystem"]["read_coverage"]["status"] == (
        "unavailable"
    )


def test_report_keeps_network_metadata_separate_from_token_usage() -> None:
    parsed_network = parse_network_trace(
        [
            '{"type":"network.trace.started","schema_version":"network-trace-1",'
            '"run_id":"run-1","case_id":"case-1","trace_id":"trace-1",'
            '"source":"structured-runtime","authority":"structured-runtime-observation",'
            '"status":"available"}',
            '{"type":"network.access","schema_version":"network-trace-1",'
            '"run_id":"run-1","case_id":"case-1","trace_id":"trace-1",'
            '"event_index":0,"timestamp":"2026-09-25T10:00:00Z",'
            '"source":"structured-runtime","authority":"structured-runtime-observation",'
            '"destination":"api.example.test:443","bytes_sent":2,"bytes_received":3}',
        ]
    )
    report = build_command_report(
        parse_codex_stream([]),
        RunManifest(
            run_id="run-1",
            case_id="case-1",
            repo_revision="target-commit",
            runtime_revision="sha256:runtime",
            task_hash="sha256:task",
            model="model-1",
            codex_version="codex-1",
            observer_version="0.5.0",
            launch_mode="host-runtime-pty",
            sandbox="read-only",
            ephemeral=True,
            started_at="2026-09-24T10:00:00Z",
            finished_at="2026-09-24T10:01:00Z",
            exit_code=0,
            complete=True,
            sidecar_revision="sha256:sidecar",
        ),
        {"required_claims": []},
        network_trace=parsed_network,
    )

    assert report["observability"]["network"]["summary"]["total_bytes"] == 5
    assert report["observability"]["tokens"]["totals"] is None
