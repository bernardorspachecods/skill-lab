import base64
from pathlib import Path

import pytest

from efficiency_validator.filesystem_capture import MacOSFsUsageCapture
from efficiency_validator.filesystem_capture import FilesystemCaptureError


class _FakeProcess:
    def __init__(self) -> None:
        self.returncode = 0
        self.killed = False

    def poll(self) -> int | None:
        return None if not self.killed else self.returncode

    def wait(self, timeout: float | None = None) -> int:
        self.killed = True
        return self.returncode

    def terminate(self) -> None:
        self.killed = True


def test_capture_starts_and_stops_a_target_scoped_fs_usage_helper(
    tmp_path: Path,
) -> None:
    commands: list[list[str]] = []
    process = _FakeProcess()

    def fake_popen(command: list[str], **kwargs: object) -> _FakeProcess:
        commands.append(command)
        ready_path = tmp_path / "capture.ready"
        ready_path.touch()
        (tmp_path / "fs_usage.log").touch()
        return process

    capture = MacOSFsUsageCapture(
        run_id="run-1",
        case_id="case-1",
        raw_path=tmp_path / "fs_usage.log",
        target_prefix=tmp_path / "target",
        additional_prefixes=(tmp_path / "skills",),
        popen_factory=fake_popen,
        authorization_timeout_seconds=0.1,
    )

    capture.start()
    capture.stop()

    assert commands
    script = commands[0][2]
    encoded = script.split("/usr/bin/printf %s ", 1)[1].split(" |", 1)[0]
    shell = base64.b64decode(encoded).decode("utf-8")
    assert "/usr/bin/fs_usage" in shell
    assert "-F -f pathname" in shell
    assert str(tmp_path / "target") in shell
    assert str(tmp_path / "skills") in shell
    assert str(tmp_path / "capture.stop") in shell


def test_capture_can_retain_all_paths_for_later_process_tree_filtering(
    tmp_path: Path,
) -> None:
    commands: list[list[str]] = []
    process = _FakeProcess()

    def fake_popen(command: list[str], **kwargs: object) -> _FakeProcess:
        commands.append(command)
        (tmp_path / "capture.ready").touch()
        (tmp_path / "fs_usage.log").touch()
        return process

    capture = MacOSFsUsageCapture(
        run_id="run-1",
        case_id="case-1",
        raw_path=tmp_path / "fs_usage.log",
        target_prefix=tmp_path / "target",
        capture_all_paths=True,
        popen_factory=fake_popen,
        authorization_timeout_seconds=0.1,
    )

    capture.start()
    script = commands[0][2]
    shell = base64.b64decode(
        script.split("/usr/bin/printf %s ", 1)[1].split(" |", 1)[0]
    ).decode("utf-8")

    assert "matches_prefix=1" in shell
    assert 'case "$line" in' not in shell


def test_capture_rejects_authorization_that_exits_before_ready(
    tmp_path: Path,
) -> None:
    process = _FakeProcess()
    process.killed = True

    capture = MacOSFsUsageCapture(
        run_id="run-1",
        case_id="case-1",
        raw_path=tmp_path / "fs_usage.log",
        target_prefix=tmp_path / "target",
        popen_factory=lambda *args, **kwargs: process,
        authorization_timeout_seconds=0.1,
    )

    with pytest.raises(FilesystemCaptureError, match="authorization failed"):
        capture.start()
