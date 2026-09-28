import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from efficiency_validator.exact_read import parse_exact_read_trace
from efficiency_validator.exact_read_capture import build_macos_interposer


@pytest.mark.skipif(sys.platform != "darwin", reason="macOS collector")
def test_macos_interposer_captures_returned_bytes_and_snapshot(tmp_path: Path) -> None:
    clang = shutil.which("clang")
    if clang is None:
        pytest.skip("clang is unavailable")
    fixture_source = Path(__file__).parent / "fixtures" / "exact_read_fixture.c"
    parent_source = Path(__file__).parent / "fixtures" / "exact_read_exec_fixture.c"
    fixture = tmp_path / "fixture"
    parent = tmp_path / "parent"
    subprocess.run(
        [
            clang,
            "-O2",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-Wl,-flat_namespace",
            "-o",
            str(fixture),
            str(fixture_source),
        ],
        check=True,
    )
    subprocess.run(
        [
            clang,
            "-O2",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-Wl,-flat_namespace",
            "-o",
            str(parent),
            str(parent_source),
        ],
        check=True,
    )
    library = build_macos_interposer(tmp_path / "exact-read-interposer.dylib")
    sidecar = tmp_path / "exact-read.jsonl"
    sidecar_fd = os.open(sidecar, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    environment = os.environ.copy()
    environment.update(
        {
            "DYLD_INSERT_LIBRARIES": str(library),
            "DYLD_FORCE_FLAT_NAMESPACE": "1",
            "EFFICIENCY_EXACT_READ_FD": str(sidecar_fd),
            "EFFICIENCY_EXACT_READ_RUN_ID": "run-capture",
            "EFFICIENCY_EXACT_READ_CASE_ID": "case-capture",
            "EFFICIENCY_EXACT_READ_TRACE_ID": "trace-capture",
        }
    )
    try:
        subprocess.run(
            [str(parent), str(fixture)],
            check=True,
            env=environment,
            pass_fds=(sidecar_fd,),
        )
    finally:
        os.close(sidecar_fd)

    with sidecar.open("a", encoding="utf-8") as stream:
        stream.write(
            '{"type":"exact-read.trace.ended",'
            '"run_id":"run-capture","case_id":"case-capture",'
            '"trace_id":"trace-capture","status":"complete"}\n'
        )

    parsed = parse_exact_read_trace(
        sidecar.read_text(encoding="utf-8").splitlines(),
        expected_run_id="run-capture",
        expected_case_id="case-capture",
    )

    assert parsed.valid is True
    assert len(parsed.files) == 1
    assert len(parsed.events) == 1
    # The parent forks a real child and the child then execs the reader. Both
    # process identities are present, while the read belongs to the child.
    assert len(parsed.processes) == 2
    assert {process.process for process in parsed.processes} == {"parent", "fixture"}
    assert parsed.events[0].bytes == 32


@pytest.mark.skipif(sys.platform != "darwin", reason="macOS collector")
def test_macos_interposer_covers_positional_vectored_and_duplicate_reads(
    tmp_path: Path,
) -> None:
    clang = shutil.which("clang")
    if clang is None:
        pytest.skip("clang is unavailable")
    fixture_source = Path(__file__).parent / "fixtures" / "exact_read_api_fixture.c"
    fixture = tmp_path / "api-fixture"
    subprocess.run(
        [
            clang,
            "-O2",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-Wl,-flat_namespace",
            "-o",
            str(fixture),
            str(fixture_source),
        ],
        check=True,
    )
    library = build_macos_interposer(tmp_path / "exact-read-interposer.dylib")
    sidecar = tmp_path / "exact-read.jsonl"
    sidecar_fd = os.open(sidecar, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    environment = os.environ.copy()
    environment.update(
        {
            "DYLD_INSERT_LIBRARIES": str(library),
            "DYLD_FORCE_FLAT_NAMESPACE": "1",
            "EFFICIENCY_EXACT_READ_FD": str(sidecar_fd),
            "EFFICIENCY_EXACT_READ_RUN_ID": "run-api",
            "EFFICIENCY_EXACT_READ_CASE_ID": "case-api",
            "EFFICIENCY_EXACT_READ_TRACE_ID": "trace-api",
        }
    )
    try:
        subprocess.run(
            [str(fixture)],
            check=True,
            env=environment,
            pass_fds=(sidecar_fd,),
        )
    finally:
        os.close(sidecar_fd)

    with sidecar.open("a", encoding="utf-8") as stream:
        stream.write(
            '{"type":"exact-read.trace.ended",'
            '"run_id":"run-api","case_id":"case-api",'
            '"trace_id":"trace-api","status":"complete"}\n'
        )

    parsed = parse_exact_read_trace(
        sidecar.read_text(encoding="utf-8").splitlines(),
        expected_run_id="run-api",
        expected_case_id="case-api",
    )

    assert parsed.valid is True
    assert len(parsed.events) == 4
    assert {event.operation for event in parsed.events} == {"read"}
    assert [event.bytes for event in parsed.events] == [8, 8, 8, 8]
    assert all(event.content for event in parsed.events)
