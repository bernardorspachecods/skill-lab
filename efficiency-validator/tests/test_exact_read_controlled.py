import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from efficiency_validator.codex_events import parse_codex_stream
from efficiency_validator.comparison import compare_runs
from efficiency_validator.exact_read import parse_exact_read_trace
from efficiency_validator.exact_read_capture import build_macos_interposer
from efficiency_validator.reporting import build_observability_report


def _capture_fixture(
    *, binary: Path, library: Path, root: Path, run_id: str, arguments: tuple[str, ...] = ()
):
    sidecar = root / f"{run_id}.jsonl"
    sidecar_fd = os.open(sidecar, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    environment = os.environ.copy()
    environment.update(
        {
            "DYLD_INSERT_LIBRARIES": str(library),
            "DYLD_FORCE_FLAT_NAMESPACE": "1",
            "EFFICIENCY_EXACT_READ_FD": str(sidecar_fd),
            "EFFICIENCY_EXACT_READ_RUN_ID": run_id,
            "EFFICIENCY_EXACT_READ_CASE_ID": "case-controlled",
            "EFFICIENCY_EXACT_READ_TRACE_ID": f"trace-{run_id}",
        }
    )
    try:
        completed = subprocess.run(
            [str(binary), *arguments],
            check=False,
            env=environment,
            pass_fds=(sidecar_fd,),
        )
    finally:
        os.close(sidecar_fd)
    assert completed.returncode == 0
    with sidecar.open("a", encoding="utf-8") as stream:
        stream.write(
            json.dumps(
                {
                    "type": "exact-read.trace.ended",
                    "run_id": run_id,
                    "case_id": "case-controlled",
                    "trace_id": f"trace-{run_id}",
                    "status": "complete",
                }
            )
            + "\n"
        )
    return parse_exact_read_trace(
        sidecar.read_text(encoding="utf-8").splitlines(),
        expected_run_id=run_id,
        expected_case_id="case-controlled",
    )


def _report(
    trace,
    *,
    run_id: str,
    variation: str,
    prompt: str,
    path_roots: dict[str, tuple[str, ...]] | None = None,
) -> dict[str, object]:
    prompt_hash = f"sha256:{hashlib.sha256(prompt.encode()).hexdigest()}"
    manifest = {
        "run_id": run_id,
        "case_id": "case-controlled",
        "task_hash": "task-controlled",
        "repo_revision": "target-controlled",
        "runtime_revision": "runtime-controlled",
        "model": "codex-controlled",
        "codex_version": "codex-controlled",
        "observer_version": "observer-controlled",
        "sandbox": "read-only",
        "sidecar_revision": "sidecar-controlled",
        "variation": variation,
        "prompt": prompt,
        "prompt_hash": prompt_hash,
        "oracle": {
            "case_id": "case-controlled",
            "path": "oracles/case-controlled.json",
            "sha256": "sha256:oracle-controlled",
            "status": "available",
        },
        "controlled_variation": {
            "label": variation,
            "prompt_hash": prompt_hash,
            "status": "declared",
            "task_hash": "task-controlled",
        },
        "provenance_status": "complete",
    }
    observed_pids = [process.pid for process in trace.processes]
    observability = build_observability_report(
        parse_codex_stream([]),
        exact_read_trace=trace,
        exact_read_process_tree_pids=observed_pids,
        path_roots=path_roots,
    )
    return {
        "status": "complete",
        "manifest": manifest,
        "observability": observability,
        "command_trace": {"command_count": 1},
    }


@pytest.mark.skipif(sys.platform != "darwin", reason="macOS collector")
def test_controlled_paired_exact_runs_produce_a_file_efficiency_verdict(
    tmp_path: Path,
) -> None:
    clang = shutil.which("clang")
    if clang is None:
        pytest.skip("clang is unavailable")
    fixture_dir = Path(__file__).parent / "fixtures"
    baseline_source = fixture_dir / "exact_read_fixture.c"
    candidate_source = fixture_dir / "exact_read_small_fixture.c"
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    for source, output in (
        (baseline_source, baseline),
        (candidate_source, candidate),
    ):
        subprocess.run(
            [
                clang,
                "-O2",
                "-Wall",
                "-Wextra",
                "-Werror",
                "-Wl,-flat_namespace",
                "-o",
                str(output),
                str(source),
            ],
            check=True,
        )
    library = build_macos_interposer(tmp_path / "exact-read-interposer.dylib")
    baseline_trace = _capture_fixture(
        binary=baseline,
        library=library,
        root=tmp_path,
        run_id="run-controlled-baseline",
    )
    candidate_trace = _capture_fixture(
        binary=candidate,
        library=library,
        root=tmp_path,
        run_id="run-controlled-candidate",
    )
    assert baseline_trace.valid is True
    assert candidate_trace.valid is True

    result = compare_runs(
        _report(
            baseline_trace,
            run_id="run-controlled-baseline",
            variation="baseline",
            prompt="Read the file.",
        ),
        _report(
            candidate_trace,
            run_id="run-controlled-candidate",
            variation="candidate",
            prompt="Read the file.",
        ),
        {"quality": {"status": "pass"}},
        {"quality": {"status": "pass"}},
        {
            "baseline_variation": "baseline",
            "candidate_variation": "candidate",
            "primary_metric": "exact_read_bytes",
            "require_exact_read": True,
        },
    )

    assert result.verdict == "better"
    assert result.evidence_status == "exploratory"
    assert result.deltas["exact_read_bytes"].absolute == -24


@pytest.mark.skipif(sys.platform != "darwin", reason="macOS collector")
def test_controlled_exact_trace_classifies_all_local_path_categories(
    tmp_path: Path,
) -> None:
    clang = shutil.which("clang")
    if clang is None:
        pytest.skip("clang is unavailable")
    fixture_source = Path(__file__).parent / "fixtures" / "exact_read_paths_fixture.c"
    fixture = tmp_path / "paths-fixture"
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
    roots: dict[str, tuple[str, ...]] = {}
    paths: list[str] = []
    for category in (
        "target",
        "skill",
        "other-repository",
        "external-context",
        "cache-dependency",
        "evaluator",
    ):
        directory = tmp_path / category
        directory.mkdir()
        path = directory / "one-byte.txt"
        path.write_text(category, encoding="utf-8")
        roots[category] = (str(directory),)
        paths.append(str(path))
    paths.append("/etc/hosts")

    library = build_macos_interposer(tmp_path / "exact-read-interposer.dylib")
    trace = _capture_fixture(
        binary=fixture,
        library=library,
        root=tmp_path,
        run_id="run-controlled-paths",
        arguments=tuple(paths),
    )
    assert trace.valid is True

    report = _report(
        trace,
        run_id="run-controlled-paths",
        variation="paths",
        prompt="Read the paths.",
        path_roots=roots,
    )
    categories = report["observability"]["exact_read"]["path_categories"]

    assert categories["counts"] == {
        "cache-dependency": 1,
        "evaluator": 1,
        "external-context": 1,
        "other-repository": 1,
        "skill": 1,
        "system": 1,
        "target": 1,
    }
