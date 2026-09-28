import json
from dataclasses import dataclass
from pathlib import Path

from efficiency_validator.manifest import RunManifest


@dataclass(frozen=True)
class _ManifestStub:
    payload: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return self.payload


def _manifest(run_id: str = "run-1") -> RunManifest:
    return RunManifest(
        run_id=run_id,
        case_id="case-1",
        repo_revision="target-1",
        runtime_revision="runtime-1",
        task_hash="task-1",
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
        sidecar_revision="sidecar-1",
    )


def test_capture_run_assembles_valid_bundle_without_filesystem_sidecar(
    tmp_path: Path, monkeypatch
) -> None:
    from scripts import capture_run

    captured: dict[str, object] = {}

    def fake_stage_target(source: Path, target: Path) -> _ManifestStub:
        target.mkdir()
        return _ManifestStub(
            {
                "source_revision": "target-1",
                "staged_root": str(target),
                "tree_hash": "tree-1",
            }
        )

    def fake_prepare_runtime(*args) -> _ManifestStub:
        runtime = args[2]
        runtime.mkdir()
        return _ManifestStub(
            {
                "source_revision": "target-1",
                "target_tree_hash": "tree-1",
                "runtime_root": str(runtime),
                "runtime_revision": "runtime-1",
                "python_version": "Python 3.13",
                "uv_version": "uv 0.1",
                "extras": ["test"],
            }
        )

    def fake_collect(repo, prompt, output, manifest_path, **kwargs) -> int:
        captured.update(kwargs)
        output.write_text("{}\n")
        manifest_path.write_text(json.dumps(_manifest().to_dict()))
        return 0

    monkeypatch.setattr(capture_run, "stage_target", fake_stage_target)
    monkeypatch.setattr(capture_run, "prepare_runtime", fake_prepare_runtime)
    monkeypatch.setattr(capture_run, "collect", fake_collect)
    monkeypatch.setattr(
        capture_run,
        "generate_report",
        lambda *args, **kwargs: {
            "status": "complete",
            "manifest": {"run_id": "run-1", "case_id": "case-1"},
            "observability": {
                "filesystem": {"status": "unavailable", "events": [], "issues": []}
            },
        },
    )

    result = capture_run.capture_run(
        source=tmp_path / "source",
        bundle_root=tmp_path / "bundle",
        prompt="task",
        oracle=tmp_path / "oracle.json",
        evaluator_root=tmp_path / "evaluator",
        run_id="run-1",
        case_id="case-1",
    )

    assert result.exit_code == 0
    assert result.validation.valid is True
    assert result.validation.filesystem_status == "unavailable"
    assert (tmp_path / "bundle" / "report.json").is_file()
    assert captured["oracle_path"] == tmp_path / "oracle.json"
    assert captured["process_tree_path"] == tmp_path / "bundle" / "process-tree.json"


def test_capture_run_wraps_collect_with_automatic_filesystem_capture(
    tmp_path: Path, monkeypatch
) -> None:
    from scripts import capture_run

    lifecycle: list[str] = []
    capture_kwargs: dict[str, object] = {}

    def fake_stage_target(source: Path, target: Path) -> _ManifestStub:
        target.mkdir()
        return _ManifestStub(
            {
                "source_revision": "target-1",
                "staged_root": str(target),
                "tree_hash": "tree-1",
            }
        )

    def fake_prepare_runtime(*args) -> _ManifestStub:
        runtime = args[2]
        runtime.mkdir()
        return _ManifestStub(
            {
                "source_revision": "target-1",
                "target_tree_hash": "tree-1",
                "runtime_root": str(runtime),
                "runtime_revision": "runtime-1",
                "python_version": "Python 3.13",
                "uv_version": "uv 0.1",
                "extras": [],
            }
        )

    class _AutoCapture:
        def __init__(self, **kwargs: object) -> None:
            lifecycle.append("init")
            self.raw_path = kwargs["raw_path"]
            capture_kwargs["filesystem_prefixes"] = kwargs["additional_prefixes"]

        def start(self) -> None:
            lifecycle.append("start")

        def stop(self) -> Path:
            lifecycle.append("stop")
            Path(self.raw_path).write_text("raw\n", encoding="utf-8")
            return Path(self.raw_path)

    def fake_collect(*args, **kwargs) -> int:
        lifecycle.append("collect")
        args[2].write_text("{}\n")
        args[3].write_text(json.dumps(_manifest().to_dict()))
        return 0

    captured_report_args: dict[str, object] = {}

    def fake_report(*args, **kwargs):
        captured_report_args.update(kwargs)
        return {
            "status": "complete",
            "manifest": {"run_id": "run-1", "case_id": "case-1"},
            "observability": {
                "filesystem": {"status": "available", "events": [], "issues": []}
            },
        }

    monkeypatch.setattr(capture_run, "stage_target", fake_stage_target)
    monkeypatch.setattr(capture_run, "prepare_runtime", fake_prepare_runtime)
    monkeypatch.setattr(capture_run, "collect", fake_collect)
    monkeypatch.setattr(capture_run, "MacOSFsUsageCapture", _AutoCapture)
    monkeypatch.setattr(
        capture_run,
        "macos_fs_usage_sidecar",
        lambda *args, **kwargs: (
            {
                "type": "filesystem.trace.started",
                "schema_version": "filesystem-trace-1",
                "run_id": "run-1",
                "case_id": "case-1",
                "trace_id": "trace-run-1",
                "source": "macos-fs-usage",
                "authority": "os-kernel-observation",
                "status": "available",
            },
        ),
    )
    monkeypatch.setattr(capture_run, "generate_report", fake_report)

    result = capture_run.capture_run(
        source=tmp_path / "source",
        bundle_root=tmp_path / "bundle",
        prompt="task",
        oracle=tmp_path / "oracle.json",
        evaluator_root=tmp_path / "evaluator",
        run_id="run-1",
        case_id="case-1",
        filesystem_auto=True,
        filesystem_prefixes=(tmp_path / "skills",),
    )

    assert result.exit_code == 0
    assert lifecycle == ["init", "start", "collect", "stop"]
    assert captured_report_args["filesystem_trace_path"] == (
        tmp_path / "bundle" / "filesystem.jsonl"
    )
    assert capture_kwargs["filesystem_prefixes"] == (tmp_path / "skills",)
