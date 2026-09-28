import base64
import hashlib
import json

from efficiency_validator.exact_read import parse_exact_read_trace


def _b64(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def test_exact_read_trace_reconstructs_returned_lines_from_snapshot() -> None:
    content = b"one\ntwo\nthree\nfour\n"
    returned = b"two\nthree\n"
    file_hash = hashlib.sha256(content).hexdigest()
    lines = [
        json.dumps(
            {
                "type": "exact-read.trace.started",
                "schema_version": "exact-read-1",
                "run_id": "run-exact-1",
                "case_id": "case-exact-1",
                "trace_id": "trace-exact-1",
                "source": "structured-read",
                "authority": "process-returned-bytes",
                "status": "available",
                "capture_mode": "exact",
            }
        ),
        json.dumps(
            {
                "type": "exact-read.process.started",
                "run_id": "run-exact-1",
                "case_id": "case-exact-1",
                "trace_id": "trace-exact-1",
                "pid": 123,
                "process": "fixture-reader",
            }
        ),
        json.dumps(
            {
                "type": "exact-read.file.snapshot",
                "run_id": "run-exact-1",
                "case_id": "case-exact-1",
                "trace_id": "trace-exact-1",
                "path": "/repo/docs/rules.md",
                "file_size": len(content),
                "content_base64": _b64(content),
                "content_sha256": file_hash,
            }
        ),
        json.dumps(
            {
                "type": "exact-read.access",
                "run_id": "run-exact-1",
                "case_id": "case-exact-1",
                "trace_id": "trace-exact-1",
                "event_index": 0,
                "pid": 123,
                "process": "fixture-reader",
                "path": "/repo/docs/rules.md",
                "operation": "read",
                "evidence_kind": "returned",
                "offset": 4,
                "bytes": len(returned),
                "content_base64": _b64(returned),
                "file_sha256": file_hash,
            }
        ),
        json.dumps(
            {
                "type": "exact-read.process.ended",
                "run_id": "run-exact-1",
                "case_id": "case-exact-1",
                "trace_id": "trace-exact-1",
                "pid": 123,
                "process": "fixture-reader",
            }
        ),
        json.dumps(
            {
                "type": "exact-read.trace.ended",
                "run_id": "run-exact-1",
                "case_id": "case-exact-1",
                "trace_id": "trace-exact-1",
                "status": "complete",
            }
        ),
    ]

    parsed = parse_exact_read_trace(
        lines,
        expected_run_id="run-exact-1",
        expected_case_id="case-exact-1",
    )

    assert parsed.status == "available"
    assert parsed.valid is True
    assert parsed.events[0].line_start == 2
    assert parsed.events[0].line_end == 3
    assert parsed.events[0].content == returned
    assert parsed.files[0].line_count == 4
    assert parsed.read_analysis == {
        "repeated_read_count": 0,
        "overlapping_read_count": 0,
        "unique_bytes": len(returned),
    }


def test_exact_read_trace_is_invalid_when_a_returned_read_has_no_content() -> None:
    lines = [
        json.dumps(
            {
                "type": "exact-read.trace.started",
                "schema_version": "exact-read-1",
                "run_id": "run-exact-2",
                "case_id": "case-exact-2",
                "trace_id": "trace-exact-2",
                "source": "structured-read",
                "authority": "process-returned-bytes",
                "status": "available",
                "capture_mode": "exact",
            }
        ),
        json.dumps(
            {
                "type": "exact-read.access",
                "run_id": "run-exact-2",
                "case_id": "case-exact-2",
                "trace_id": "trace-exact-2",
                "event_index": 0,
                "pid": 123,
                "process": "fixture-reader",
                "path": "/repo/docs/rules.md",
                "operation": "read",
                "evidence_kind": "returned",
                "offset": 0,
                "bytes": 10,
            }
        ),
    ]

    parsed = parse_exact_read_trace(
        lines,
        expected_run_id="run-exact-2",
        expected_case_id="case-exact-2",
    )

    assert parsed.valid is False
    assert parsed.status == "partial"
    assert any("content_base64" in reason for reason in parsed.invalid_reasons)


def test_exact_read_trace_rejects_changed_snapshot() -> None:
    content = b"original\n"
    returned = b"changed\n"
    lines = [
        json.dumps(
            {
                "type": "exact-read.trace.started",
                "schema_version": "exact-read-1",
                "run_id": "run-exact-3",
                "case_id": "case-exact-3",
                "trace_id": "trace-exact-3",
                "source": "structured-read",
                "authority": "process-returned-bytes",
                "status": "available",
                "capture_mode": "exact",
            }
        ),
        json.dumps(
            {
                "type": "exact-read.file.snapshot",
                "run_id": "run-exact-3",
                "case_id": "case-exact-3",
                "trace_id": "trace-exact-3",
                "path": "/repo/docs/rules.md",
                "file_size": len(content),
                "content_base64": _b64(content),
                "content_sha256": hashlib.sha256(content).hexdigest(),
            }
        ),
        json.dumps(
            {
                "type": "exact-read.access",
                "run_id": "run-exact-3",
                "case_id": "case-exact-3",
                "trace_id": "trace-exact-3",
                "event_index": 0,
                "pid": 123,
                "process": "fixture-reader",
                "path": "/repo/docs/rules.md",
                "operation": "read",
                "evidence_kind": "returned",
                "offset": 0,
                "bytes": len(returned),
                "content_base64": _b64(returned),
                "file_sha256": hashlib.sha256(content).hexdigest(),
            }
        ),
    ]

    parsed = parse_exact_read_trace(lines)

    assert parsed.valid is False
    assert any(
        "returned bytes do not match snapshot" in reason
        for reason in parsed.invalid_reasons
    )


def test_exact_read_trace_rejects_truncated_sidecar() -> None:
    lines = [
        json.dumps(
            {
                "type": "exact-read.trace.started",
                "schema_version": "exact-read-1",
                "run_id": "run-truncated",
                "case_id": "case-truncated",
                "trace_id": "trace-truncated",
                "source": "structured-read",
                "authority": "process-returned-bytes",
                "status": "available",
                "capture_mode": "exact",
            }
        )
    ]

    parsed = parse_exact_read_trace(lines)

    assert parsed.valid is False
    assert "missing exact-read.trace.ended metadata" in parsed.invalid_reasons


def test_exact_read_trace_keeps_binary_reads_byte_only() -> None:
    content = b"\x00binary\nwith\nnewlines"
    file_hash = hashlib.sha256(content).hexdigest()
    lines = [
        json.dumps(
            {
                "type": "exact-read.trace.started",
                "schema_version": "exact-read-1",
                "run_id": "run-binary",
                "case_id": "case-binary",
                "trace_id": "trace-binary",
                "source": "structured-read",
                "authority": "process-returned-bytes",
                "status": "available",
                "capture_mode": "exact",
            }
        ),
        json.dumps(
            {
                "type": "exact-read.process.started",
                "run_id": "run-binary",
                "case_id": "case-binary",
                "trace_id": "trace-binary",
                "pid": 7,
                "process": "binary-reader",
            }
        ),
        json.dumps(
            {
                "type": "exact-read.file.snapshot",
                "run_id": "run-binary",
                "case_id": "case-binary",
                "trace_id": "trace-binary",
                "path": "/repo/data.bin",
                "file_size": len(content),
                "content_base64": _b64(content),
                "content_sha256": file_hash,
            }
        ),
        json.dumps(
            {
                "type": "exact-read.access",
                "run_id": "run-binary",
                "case_id": "case-binary",
                "trace_id": "trace-binary",
                "event_index": 0,
                "pid": 7,
                "process": "binary-reader",
                "path": "/repo/data.bin",
                "operation": "read",
                "evidence_kind": "returned",
                "offset": 0,
                "bytes": len(content),
                "content_base64": _b64(content),
                "file_sha256": file_hash,
            }
        ),
        json.dumps(
            {
                "type": "exact-read.trace.ended",
                "run_id": "run-binary",
                "case_id": "case-binary",
                "trace_id": "trace-binary",
                "status": "complete",
            }
        ),
    ]

    parsed = parse_exact_read_trace(lines)

    assert parsed.valid is True
    assert parsed.files[0].content_kind == "binary"
    assert parsed.files[0].line_count == 0
    assert parsed.events[0].line_start is None
    assert parsed.events[0].line_end is None


def test_exact_read_trace_rejects_mapped_read_gap() -> None:
    lines = [
        json.dumps(
            {
                "type": "exact-read.trace.started",
                "schema_version": "exact-read-1",
                "run_id": "run-mmap",
                "case_id": "case-mmap",
                "trace_id": "trace-mmap",
                "source": "dyld-read-interposer",
                "authority": "process-returned-bytes",
                "status": "available",
                "capture_mode": "exact",
            }
        ),
        json.dumps(
            {
                "type": "exact-read.gap",
                "run_id": "run-mmap",
                "case_id": "case-mmap",
                "trace_id": "trace-mmap",
                "reason": "mmap-read-unsupported",
                "path": "/repo/data.bin",
            }
        ),
        json.dumps(
            {
                "type": "exact-read.trace.ended",
                "run_id": "run-mmap",
                "case_id": "case-mmap",
                "trace_id": "trace-mmap",
                "status": "complete",
            }
        ),
    ]

    parsed = parse_exact_read_trace(lines)

    assert parsed.valid is False
    assert any("mmap-read-unsupported" in reason for reason in parsed.invalid_reasons)


def test_exact_read_trace_rejects_each_declared_capture_gap() -> None:
    for gap_reason in (
        "file-write-unsupported",
        "read-from-unregistered-file-descriptor",
        "snapshot-read-failed",
        "openat-path-resolution-failed",
    ):
        lines = [
            json.dumps(
                {
                    "type": "exact-read.trace.started",
                    "schema_version": "exact-read-1",
                    "run_id": "run-gap",
                    "case_id": "case-gap",
                    "trace_id": "trace-gap",
                    "source": "dyld-read-interposer",
                    "authority": "process-returned-bytes",
                    "status": "available",
                    "capture_mode": "exact",
                }
            ),
            json.dumps(
                {
                    "type": "exact-read.gap",
                    "run_id": "run-gap",
                    "case_id": "case-gap",
                    "trace_id": "trace-gap",
                    "reason": gap_reason,
                }
            ),
            json.dumps(
                {
                    "type": "exact-read.trace.ended",
                    "run_id": "run-gap",
                    "case_id": "case-gap",
                    "trace_id": "trace-gap",
                    "status": "complete",
                }
            ),
        ]

        parsed = parse_exact_read_trace(lines)

        assert parsed.valid is False
        assert any(gap_reason in reason for reason in parsed.invalid_reasons)


def test_exact_read_trace_rejects_missing_snapshot_and_malformed_records() -> None:
    parsed = parse_exact_read_trace(
        [
            "not-json",
            json.dumps(
                {
                    "type": "exact-read.trace.started",
                    "schema_version": "exact-read-1",
                    "run_id": "run-missing-snapshot",
                    "case_id": "case-missing-snapshot",
                    "trace_id": "trace-missing-snapshot",
                    "source": "structured-read",
                    "authority": "process-returned-bytes",
                    "status": "available",
                    "capture_mode": "exact",
                }
            ),
            json.dumps(
                {
                    "type": "exact-read.process.started",
                    "run_id": "run-missing-snapshot",
                    "case_id": "case-missing-snapshot",
                    "trace_id": "trace-missing-snapshot",
                    "pid": 9,
                    "process": "reader",
                }
            ),
            json.dumps(
                {
                    "type": "exact-read.access",
                    "run_id": "run-missing-snapshot",
                    "case_id": "case-missing-snapshot",
                    "trace_id": "trace-missing-snapshot",
                    "event_index": 0,
                    "pid": 9,
                    "process": "reader",
                    "path": "/repo/missing.txt",
                    "operation": "read",
                    "evidence_kind": "returned",
                    "offset": 0,
                    "bytes": 1,
                    "content_base64": "YQ==",
                    "file_sha256": "file-hash",
                }
            ),
            json.dumps(
                {
                    "type": "exact-read.trace.ended",
                    "run_id": "run-missing-snapshot",
                    "case_id": "case-missing-snapshot",
                    "trace_id": "trace-missing-snapshot",
                    "status": "complete",
                }
            ),
        ]
    )

    assert parsed.valid is False
    assert any("malformed JSON" in reason for reason in parsed.invalid_reasons)
    assert any("no immutable snapshot" in reason for reason in parsed.invalid_reasons)
