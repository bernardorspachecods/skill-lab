import json
from pathlib import Path

from efficiency_validator.bundle import RunBundle


def _write_manifest(
    root: Path, *, run_id: str = "run-1", exact_read_required: bool = False
) -> None:
    (root / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "case_id": "case-1",
                "repo_revision": "target-1",
                "runtime_revision": "runtime-1",
                "task_hash": "task-1",
                "model": "model-1",
                "codex_version": "codex-1",
                "observer_version": "0.5.0",
                "launch_mode": "host-runtime-pty",
                "sandbox": "read-only",
                "ephemeral": True,
                "started_at": "2026-09-24T10:00:00Z",
                "finished_at": "2026-09-24T10:01:00Z",
                "exit_code": 0,
                "complete": True,
                "sidecar_revision": "sidecar-1",
                "observability_schema": "observability-1",
                "token_usage_source": "codex-exec-json",
                "filesystem_trace_source": "unavailable",
                "exact_read_required": exact_read_required,
                "exact_read_trace_source": (
                    "structured-read" if exact_read_required else "unavailable"
                ),
            }
        )
    )


def _write_report(root: Path, *, run_id: str = "run-1", filesystem: str = "unavailable") -> None:
    (root / "report.json").write_text(
        json.dumps(
            {
                "status": "complete",
                "manifest": {"run_id": run_id, "case_id": "case-1"},
                "observability": {
                    "filesystem": {
                        "status": filesystem,
                        "events": [],
                        "issues": [],
                    }
                },
            }
        )
    )


def test_bundle_accepts_complete_run_without_filesystem_sidecar(tmp_path: Path) -> None:
    _write_manifest(tmp_path)
    _write_report(tmp_path)
    (tmp_path / "events.jsonl").write_text("{}\n")

    validation = RunBundle.from_root(tmp_path).validate()

    assert validation.valid is True
    assert validation.filesystem_status == "unavailable"
    assert validation.issues == ()


def test_bundle_rejects_mismatched_filesystem_sidecar(tmp_path: Path) -> None:
    _write_manifest(tmp_path)
    _write_report(tmp_path, filesystem="available")
    (tmp_path / "events.jsonl").write_text("{}\n")
    (tmp_path / "filesystem.jsonl").write_text(
        json.dumps(
            {
                "type": "filesystem.trace.started",
                "schema_version": "filesystem-trace-1",
                "run_id": "different-run",
                "case_id": "case-1",
                "trace_id": "trace-1",
                "source": "macos-fs-usage",
                "authority": "os-kernel-observation",
                "status": "available",
            }
        )
        + "\n"
    )

    validation = RunBundle.from_root(tmp_path).validate()

    assert validation.valid is False
    assert validation.filesystem_status == "partial"
    assert any("filesystem" in issue for issue in validation.issues)


def test_bundle_rejects_missing_required_artifact(tmp_path: Path) -> None:
    _write_manifest(tmp_path)
    _write_report(tmp_path)

    validation = RunBundle.from_root(tmp_path).validate()

    assert validation.valid is False
    assert any("events.jsonl" in issue for issue in validation.issues)


def test_bundle_rejects_exact_mode_without_complete_read_evidence(tmp_path: Path) -> None:
    _write_manifest(tmp_path, exact_read_required=True)
    _write_report(tmp_path)
    (tmp_path / "events.jsonl").write_text("{}\n")
    (tmp_path / "exact-read.jsonl").write_text(
        json.dumps(
            {
                "type": "exact-read.trace.started",
                "schema_version": "exact-read-1",
                "run_id": "run-1",
                "case_id": "case-1",
                "trace_id": "trace-1",
                "source": "structured-read",
                "authority": "process-returned-bytes",
                "status": "available",
                "capture_mode": "exact",
            }
        )
        + "\n"
        + json.dumps(
            {
                "type": "exact-read.access",
                "run_id": "run-1",
                "case_id": "case-1",
                "trace_id": "trace-1",
                "event_index": 0,
                "pid": 7,
                "process": "reader",
                "path": "/repo/file.txt",
                "operation": "read",
                "evidence_kind": "returned",
                "offset": 0,
                "bytes": 1,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    validation = RunBundle.from_root(tmp_path).validate()

    assert validation.valid is False
    assert validation.exact_read_status == "partial"
    assert any("exact-read" in issue for issue in validation.issues)


def test_bundle_rejects_exact_process_escape(tmp_path: Path) -> None:
    _write_manifest(tmp_path, exact_read_required=True)
    _write_report(tmp_path)
    (tmp_path / "events.jsonl").write_text("{}\n")
    content = b"one\n"
    content_b64 = "b25lCg=="
    file_hash = "3f786850e387550fdab836ed7e6dc881de23001b"
    trace = [
        {
            "type": "exact-read.trace.started",
            "schema_version": "exact-read-1",
            "run_id": "run-1",
            "case_id": "case-1",
            "trace_id": "trace-1",
            "source": "structured-read",
            "authority": "process-returned-bytes",
            "status": "available",
            "capture_mode": "exact",
        },
        {
            "type": "exact-read.process.started",
            "run_id": "run-1",
            "case_id": "case-1",
            "trace_id": "trace-1",
            "pid": 7,
            "process": "reader",
        },
        {
            "type": "exact-read.file.snapshot",
            "run_id": "run-1",
            "case_id": "case-1",
            "trace_id": "trace-1",
            "path": "/repo/file.txt",
            "file_size": len(content),
            "content_base64": content_b64,
            "content_sha256": file_hash,
        },
        {
            "type": "exact-read.access",
            "run_id": "run-1",
            "case_id": "case-1",
            "trace_id": "trace-1",
            "event_index": 0,
            "pid": 7,
            "process": "reader",
            "path": "/repo/file.txt",
            "operation": "read",
            "evidence_kind": "returned",
            "offset": 0,
            "bytes": len(content),
            "content_base64": content_b64,
            "file_sha256": file_hash,
        },
        {
            "type": "exact-read.trace.ended",
            "run_id": "run-1",
            "case_id": "case-1",
            "trace_id": "trace-1",
            "status": "complete",
        },
    ]
    (tmp_path / "exact-read.jsonl").write_text(
        "".join(json.dumps(record) + "\n" for record in trace),
        encoding="utf-8",
    )
    (tmp_path / "process-tree.json").write_text(
        json.dumps(
            {
                "schema_version": "process-tree-1",
                "status": "available",
                "pids": [7, 8],
            }
        ),
        encoding="utf-8",
    )

    validation = RunBundle.from_root(tmp_path).validate()

    assert validation.valid is False
    assert any("missing pids: 8" in issue for issue in validation.issues)
