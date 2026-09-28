from pathlib import Path

from efficiency_validator.filesystem import (
    macos_fs_usage_sidecar,
    parse_filesystem_trace,
    summarize_read_coverage,
)


FIXTURE = Path(__file__).parent / "fixtures" / "filesystem" / "available.jsonl"


def test_filesystem_sidecar_preserves_os_authority_and_run_correlation() -> None:
    parsed = parse_filesystem_trace(
        FIXTURE.read_text(encoding="utf-8").splitlines(),
        expected_run_id="run-fs-1",
        expected_case_id="case-fs-1",
    )

    assert parsed.status == "available"
    assert parsed.source == "macos-fs-usage"
    assert parsed.authority == "os-kernel-observation"
    assert parsed.events[0].operation == "open"
    assert parsed.events[0].evidence_kind == "opened"
    assert parsed.events[0].path.endswith("docs/rules.md")
    assert parsed.issues == ()


def test_filesystem_sidecar_mismatch_is_partial_not_silently_accepted() -> None:
    parsed = parse_filesystem_trace(
        FIXTURE.read_text(encoding="utf-8").splitlines(),
        expected_run_id="different-run",
        expected_case_id="case-fs-1",
    )

    assert parsed.status == "partial"
    assert parsed.events
    assert parsed.issues[0].kind == "mismatch"


def test_filesystem_sidecar_without_metadata_is_malformed() -> None:
    parsed = parse_filesystem_trace(
        [
            '{"type":"filesystem.access","run_id":"run-1"}',
        ]
    )

    assert parsed.status == "malformed"
    assert parsed.events == ()
    assert parsed.issues


def test_filesystem_sidecar_preserves_denied_and_truncated_statuses() -> None:
    denied = parse_filesystem_trace(
        [
            '{"type":"filesystem.trace.started",'
            '"schema_version":"filesystem-trace-1",'
            '"run_id":"run-1","case_id":"case-1","trace_id":"trace-1",'
            '"source":"macos-fs-usage",'
            '"authority":"os-kernel-observation","status":"denied"}'
        ]
    )
    truncated = parse_filesystem_trace(
        [
            '{"type":"filesystem.trace.started",'
            '"schema_version":"filesystem-trace-1",'
            '"run_id":"run-1","case_id":"case-1","trace_id":"trace-1",'
            '"source":"macos-fs-usage",'
            '"authority":"os-kernel-observation","status":"truncated"}'
        ]
    )

    assert denied.status == "denied"
    assert truncated.status == "truncated"


def test_macos_fs_usage_converter_filters_target_and_preserves_kernel_evidence() -> None:
    records = macos_fs_usage_sidecar(
        [
            "16:32:57.887492  lstat64  /private/tmp/run/target/docs/rules.md  0.000002  Python.123",
            "16:32:57.887500  read  B=4096 O=0  /private/tmp/run/target/docs/rules.md  0.000002  Python.123",
            "16:32:57.887501  open  /private/tmp/other/file  0.000002  Python.123",
        ],
        run_id="run-fs-1",
        case_id="case-fs-1",
        trace_id="trace-fs-1",
        target_prefix="/private/tmp/run/target",
    )

    assert len(records) == 3
    assert records[1]["evidence_kind"] == "requested"
    assert records[2]["evidence_kind"] == "requested"
    assert records[2]["thread_id"] == 123
    assert records[2]["process"] == "Python"
    assert records[2]["bytes"] == 4096
    assert records[2]["offset"] == 0


def test_macos_fs_usage_converter_can_include_an_explicit_skill_prefix() -> None:
    records = macos_fs_usage_sidecar(
        [
            "16:32:57.887492  open  /private/tmp/run/target/docs/rules.md  0.000002  Python.123",
            "16:32:57.887493  open  /Users/test/agent-skills/chat-start/SKILL.md  0.000002  Codex.456",
            "16:32:57.887494  open  /private/tmp/other/file  0.000002  Codex.456",
        ],
        run_id="run-fs-1",
        case_id="case-fs-1",
        trace_id="trace-fs-1",
        target_prefix="/private/tmp/run/target",
        additional_prefixes=("/Users/test/agent-skills",),
    )

    assert len(records) == 3
    assert records[0]["target_prefix"] == "/private/tmp/run/target"
    assert records[0]["capture_prefixes"] == [
        "/private/tmp/run/target",
        "/Users/test/agent-skills",
    ]
    assert records[2]["path"].endswith("chat-start/SKILL.md")


def test_macos_fs_usage_converter_can_filter_all_paths_to_measured_process_tree() -> None:
    records = macos_fs_usage_sidecar(
        [
            "16:32:57.887492  open  /Users/test/agent-skills/chat-start/SKILL.md  0.000002  Codex.456",
            "16:32:57.887493  open  /Users/test/other/file  0.000002  Finder.999",
        ],
        run_id="run-fs-1",
        case_id="case-fs-1",
        trace_id="trace-fs-1",
        target_prefix="/private/tmp/run/target",
        process_pids=(456,),
        process_names=("Codex",),
        capture_all_paths=True,
    )

    assert len(records) == 2
    assert records[0]["capture_scope"] == "measured-process-tree-by-process-name"
    assert records[0]["correlation_confidence"] == "partial"
    assert records[1]["path"].endswith("agent-skills/chat-start/SKILL.md")


def test_structured_read_reports_partial_line_coverage_and_keeps_content() -> None:
    parsed = parse_filesystem_trace(
        [
            '{"type":"filesystem.trace.started",'
            '"schema_version":"filesystem-trace-1",'
            '"run_id":"run-content-1","case_id":"case-content-1",'
            '"trace_id":"trace-content-1","source":"structured-read",'
            '"authority":"structured-runtime-observation",'
            '"status":"available"}',
            '{"type":"filesystem.access",'
            '"schema_version":"filesystem-trace-1",'
            '"run_id":"run-content-1","case_id":"case-content-1",'
            '"trace_id":"trace-content-1","event_index":0,'
            '"timestamp":"2026-09-25T10:00:00Z",'
            '"source":"structured-read",'
            '"authority":"structured-runtime-observation",'
            '"evidence_kind":"returned","operation":"read",'
            '"path":"/repo/docs/large.md","offset":0,"bytes":120,'
            '"file_size":12000,"line_start":1,"line_end":10,'
            '"file_line_count":1000,"content_capture":"full",'
            '"content":"first ten lines"}',
        ],
        expected_run_id="run-content-1",
        expected_case_id="case-content-1",
    )

    assert parsed.status == "available"
    assert parsed.events[0].content == "first ten lines"
    summary = summarize_read_coverage(parsed)

    assert summary["files"][0]["coverage_status"] == "partial"
    assert summary["files"][0]["line_coverage"] == 0.01
    assert summary["files"][0]["observed_line_range"] == [1, 10]


def test_structured_read_reports_full_line_coverage() -> None:
    parsed = parse_filesystem_trace(
        [
            '{"type":"filesystem.trace.started",'
            '"schema_version":"filesystem-trace-1",'
            '"run_id":"run-content-2","case_id":"case-content-2",'
            '"trace_id":"trace-content-2","source":"structured-read",'
            '"authority":"structured-runtime-observation",'
            '"status":"available"}',
            '{"type":"filesystem.access",'
            '"schema_version":"filesystem-trace-1",'
            '"run_id":"run-content-2","case_id":"case-content-2",'
            '"trace_id":"trace-content-2","event_index":0,'
            '"timestamp":"2026-09-25T10:00:00Z",'
            '"source":"structured-read",'
            '"authority":"structured-runtime-observation",'
            '"evidence_kind":"returned","operation":"read",'
            '"path":"/repo/docs/small.md","offset":0,"bytes":100,'
            '"file_size":100,"line_start":1,"line_end":100,'
            '"file_line_count":100,"content_capture":"hash",'
            '"content_hash":"abc"}',
        ],
        expected_run_id="run-content-2",
        expected_case_id="case-content-2",
    )

    summary = summarize_read_coverage(parsed)

    assert summary["files"][0]["coverage_status"] == "full"
    assert summary["files"][0]["line_coverage"] == 1.0
