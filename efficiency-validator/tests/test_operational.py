import json
from pathlib import Path

from efficiency_validator.operational import capture


def fake_codex(tmp_path: Path, body: str) -> str:
    import sys
    script = tmp_path / "codex-fixture"
    script.write_text(
        f"#!{sys.executable}\nimport sys, json, pathlib, time\n"
        "if '--version' in sys.argv:\n print('fixture 1'); sys.exit()\n"
        "prompt = sys.stdin.read()\n" + body
    )
    script.chmod(0o700)
    return str(script)


def test_capture_preserves_inputs_and_outputs_without_changing_source(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "task.txt").write_text("before\n")
    executable = fake_codex(tmp_path, '''
print(json.dumps({"type":"turn.started"}), flush=True)
pathlib.Path("task.txt").write_text("after\\n")
print(json.dumps({"type":"item.completed","item":{"id":"a","type":"agent_message","text":"done"}}))
print(json.dumps({"type":"turn.completed","usage":{"input_tokens":12,"cached_input_tokens":4,"output_tokens":3}}))
''')
    bundle = tmp_path / "run"
    result = capture(source, bundle, prompt="change task", variant="base", codex=executable)
    assert result["termination"] == "completed"
    assert (source / "task.txt").read_text() == "before\n"
    assert (bundle / "inputs/target/task.txt").read_text() == "before\n"
    assert (bundle / "outputs/target/task.txt").read_text() == "after\n"
    assert json.loads((bundle / "changes.json").read_text())[0]["kind"] == "modified"
    assert (bundle / "events.jsonl").read_text().count("turn.completed") == 1


def test_timeout_keeps_partial_evidence_and_report_is_offline(tmp_path):
    from efficiency_validator.operational_report import report
    source = tmp_path / "source"
    source.mkdir()
    (source / "file").write_text("original")
    executable = fake_codex(tmp_path, '''
print(json.dumps({"type":"turn.started"}), flush=True)
print(json.dumps({"type":"future.event","payload":"retain me"}), flush=True)
time.sleep(20)
''')
    bundle = tmp_path / "run"
    result = capture(source, bundle, prompt="wait", variant="base", codex=executable, timeout=0.3)
    assert result["termination"] == "timeout"
    raw = (bundle / "events.jsonl").read_bytes()
    executable_path = Path(executable)
    executable_path.unlink()
    (source / "file").unlink()
    first = report(bundle)
    assert first["usage"]["input_tokens"] is None
    assert first["execution_status"] == "timeout"
    assert first["timeline"][1]["event"]["payload"] == "retain me"
    assert report(bundle) == first
    assert (bundle / "events.jsonl").read_bytes() == raw


def test_regeneration_detects_modified_evidence(tmp_path):
    from efficiency_validator.operational_report import report
    import pytest
    source = tmp_path / "source"
    source.mkdir()
    executable = fake_codex(tmp_path, "print('{}')\n")
    bundle = tmp_path / "run"
    capture(source, bundle, prompt="wait", variant="base", codex=executable)
    (bundle / "events.jsonl").write_text('{"type":"turn.completed"}\n')
    with pytest.raises(ValueError, match="integrity"):
        report(bundle)


def test_abandoned_run_can_be_recovered_without_launching_agent(tmp_path):
    from efficiency_validator.operational import recover
    from efficiency_validator.operational_report import report
    bundle = tmp_path / "run"
    bundle.mkdir()
    (bundle / "manifest.json").write_text(json.dumps({
        "schema": "operational-1", "run_id": "abandoned", "variant": "a",
        "termination": "running", "collector_pid": 2147483647,
        "versions": {"collector": "operational-1"}}))
    (bundle / "events.jsonl").write_text('{"type":"turn.started"}\n')
    result = recover(bundle)
    assert result["termination"] == "interrupted"
    assert report(bundle)["collection_status"] == "partial"


def test_overlay_is_preserved_and_repeated_runs_start_fresh(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "original.txt").write_text("initial")
    skill = tmp_path / "skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("Use the local helper")
    (skill / "helper.txt").write_text("resource")
    executable = fake_codex(tmp_path, '''
assert pathlib.Path("original.txt").read_text() == "initial"
pathlib.Path("original.txt").write_text("modified")
print(json.dumps({"type":"turn.started"}))
print(json.dumps({"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}))
''')
    first = tmp_path / "first"
    capture(source, first, prompt="work", variant="skill", codex=executable,
            overlays={".agents/skills/example": skill})
    (skill / "helper.txt").write_text("changed after capture")
    second = capture(source, tmp_path / "second", prompt="work", variant="base", codex=executable)
    assert second["termination"] == "completed"
    assert (first / "inputs/target/.agents/skills/example/helper.txt").read_text() == "resource"


def test_cancel_retains_evidence_and_launch_failure_is_reportable(tmp_path):
    import threading
    import time
    from efficiency_validator.operational_report import report
    source = tmp_path / "source"
    source.mkdir()
    executable = fake_codex(tmp_path, 'print(\'{"type":"turn.started"}\', flush=True)\ntime.sleep(30)\n')
    bundle = tmp_path / "cancelled"

    def request_cancel():
        for _ in range(200):
            if (bundle / "events.jsonl").exists() and (bundle / "events.jsonl").stat().st_size:
                (bundle / "cancel.request").touch()
                return
            time.sleep(0.01)

    writer = threading.Thread(target=request_cancel)
    writer.start()
    result = capture(source, bundle, prompt="wait", variant="base", codex=executable)
    writer.join()
    assert result["termination"] == "cancelled"
    assert report(bundle)["timeline"][0]["event"]["type"] == "turn.started"
    broken = tmp_path / "broken"
    capture(source, broken, prompt="wait", variant="base", codex=str(tmp_path / "nonexistent"))
    assert report(broken)["execution_status"] == "capture_failed"


def test_manual_wait_intervals_are_unioned_and_missing_usage_is_not_zero(tmp_path):
    from efficiency_validator.operational_report import annotate, report
    source = tmp_path / "source"
    source.mkdir()
    executable = fake_codex(tmp_path, '''
print(json.dumps({"type":"turn.started"}))
print(json.dumps({"type":"turn.completed","usage":{"input_tokens":12,"output_tokens":3}}))
time.sleep(0.1)
''')
    bundle = tmp_path / "run"
    capture(source, bundle, prompt="work", variant="base", codex=executable)
    annotate(bundle, kind="hint", text="manual example", start=0.01, end=0.05)
    annotate(bundle, kind="approval", text="overlapping example", start=0.03, end=0.08)
    result = report(bundle)
    assert round(result["timing"]["recorded_user_wait_seconds"], 3) == 0.07
    assert result["usage"]["total_tokens"] == 15
    assert result["usage"]["cached_input_tokens"] is None
    assert result["interventions"]["total_count"] is None


def test_overwrite_and_escaping_symlink_are_rejected(tmp_path):
    import pytest
    source = tmp_path / "source"
    source.mkdir()
    outside = tmp_path / "outside"
    outside.write_text("not experiment input")
    (source / "escape").symlink_to(outside)
    bundle = tmp_path / "run"
    result = capture(source, bundle, prompt="work", variant="base")
    assert result["termination"] == "capture_failed"
    assert "symlink" in result["error"]
    with pytest.raises(FileExistsError):
        capture(source, bundle, prompt="again", variant="base")


def test_partial_message_is_not_presented_as_final_answer(tmp_path):
    from efficiency_validator.operational_report import report
    source = tmp_path / "source"
    source.mkdir()
    executable = fake_codex(tmp_path, '''
print(json.dumps({"type":"turn.started"}), flush=True)
print(json.dumps({"type":"item.completed","item":{"id":"m","type":"agent_message","text":"I will start"}}), flush=True)
time.sleep(20)
''')
    bundle = tmp_path / "run"
    capture(source, bundle, prompt="work", variant="base", codex=executable, timeout=0.2)
    assert report(bundle)["final_response"] is None
    assert report(bundle)["last_agent_message"] == "I will start"


def test_work_products_include_binary_creation_deletion_and_failed_checks(tmp_path):
    from efficiency_validator.operational_report import report
    import sys
    source = tmp_path / "source"
    source.mkdir()
    (source / "obsolete.txt").write_text("remove me")
    executable = fake_codex(tmp_path, '''
pathlib.Path("obsolete.txt").unlink()
pathlib.Path("new.bin").write_bytes(bytes([0, 255, 10]))
print(json.dumps({"type":"turn.started"}))
print(json.dumps({"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}))
''')
    bundle = tmp_path / "run"
    capture(source, bundle, prompt="modify", variant="base", codex=executable,
            checks=[[sys.executable, "-c", "print('failed criterion'); raise SystemExit(2)"]])
    result = report(bundle)
    assert {c["path"]: c["kind"] for c in result["changes"]} == {
        "new.bin": "created", "obsolete.txt": "deleted"}
    assert (bundle / "outputs/target/new.bin").read_bytes() == bytes([0, 255, 10])
    assert result["execution_status"] == "completed"
    assert result["quality"]["status"] == "fail"
    assert (bundle / "check-0.jsonl").read_text() == "failed criterion\n"


def test_offline_report_rejects_unknown_schema_and_added_input(tmp_path):
    from efficiency_validator.operational_report import report
    import pytest
    source = tmp_path / "source"
    source.mkdir()
    executable = fake_codex(tmp_path, "print('{}')\n")
    bundle = tmp_path / "run"
    capture(source, bundle, prompt="work", variant="base", codex=executable)
    (bundle / "inputs/target/extra").write_text("was not present")
    with pytest.raises(ValueError, match="integrity"):
        report(bundle)
    manifest = json.loads((bundle / "manifest.json").read_text())
    manifest["schema"] = "future-unsupported"
    (bundle / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="schema"):
        report(bundle)
