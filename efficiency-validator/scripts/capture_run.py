#!/usr/bin/env python3
"""Capture one staged Codex run into a reusable, validated run bundle."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any

try:
    from efficiency_validator.bundle import BundleValidation, RunBundle
    from efficiency_validator.filesystem import macos_fs_usage_sidecar
    from efficiency_validator.filesystem_capture import MacOSFsUsageCapture
    from efficiency_validator.exact_read_capture import build_macos_interposer
    from efficiency_validator.runtime import prepare_runtime
    from efficiency_validator.staging import stage_target
except ModuleNotFoundError:  # direct execution from the repository checkout
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from efficiency_validator.bundle import BundleValidation, RunBundle
    from efficiency_validator.filesystem import macos_fs_usage_sidecar
    from efficiency_validator.filesystem_capture import MacOSFsUsageCapture
    from efficiency_validator.exact_read_capture import build_macos_interposer
    from efficiency_validator.runtime import prepare_runtime
    from efficiency_validator.staging import stage_target

try:
    from scripts.collect_codex import collect
    from scripts.report_codex import generate_report
except ModuleNotFoundError:  # direct execution from the repository checkout
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from scripts.collect_codex import collect
    from scripts.report_codex import generate_report


@dataclass(frozen=True)
class CaptureResult:
    bundle: RunBundle
    collector_exit_code: int
    validation: BundleValidation

    @property
    def exit_code(self) -> int:
        if self.collector_exit_code != 0 or not self.validation.valid:
            return 1
        return 0


def capture_run(
    *,
    source: Path,
    bundle_root: Path,
    prompt: str,
    oracle: Path,
    evaluator_root: Path,
    run_id: str,
    case_id: str,
    variation: str = "unspecified",
    task_hash: str | None = None,
    model: str | None = None,
    identified_claims: Path | None = None,
    filesystem_raw: Path | None = None,
    filesystem_auto: bool = False,
    exact_read: bool = False,
    filesystem_prefixes: tuple[Path, ...] = (),
    network_trace: Path | None = None,
    path_roots: dict[str, tuple[str, ...]] | None = None,
    timeout_seconds: float = 1800,
) -> CaptureResult:
    """Run the staged collector and assemble its bundle without overwriting."""

    source = source.resolve()
    bundle_root = bundle_root.resolve()
    if bundle_root.exists() and any(bundle_root.iterdir()):
        raise FileExistsError(f"Bundle destination is not empty: {bundle_root}")
    bundle_root.mkdir(parents=True, exist_ok=True)

    target = bundle_root / "target"
    staging_manifest_path = bundle_root / "staging.json"
    runtime = bundle_root / "runtime"
    runtime_manifest_path = bundle_root / "runtime.json"
    events_path = bundle_root / "events.jsonl"
    manifest_path = bundle_root / "manifest.json"
    filesystem_path = bundle_root / "filesystem.jsonl"
    network_path = bundle_root / "network.jsonl"
    process_tree_path = bundle_root / "process-tree.json"
    exact_read_path = bundle_root / "exact-read.jsonl"
    exact_read_library = bundle_root / "exact-read-interposer.dylib"
    report_path = bundle_root / "report.json"
    if filesystem_raw is not None and filesystem_auto:
        raise ValueError("filesystem_raw and filesystem_auto are mutually exclusive")
    if exact_read:
        build_macos_interposer(exact_read_library)

    staging = stage_target(source, target)
    _write_json(staging_manifest_path, staging.to_dict())
    runtime_manifest = prepare_runtime(
        target,
        staging_manifest_path,
        runtime,
        runtime_manifest_path,
    )
    _write_json(runtime_manifest_path, runtime_manifest.to_dict())

    filesystem_trace_path: Path | None = None
    automatic_capture = None
    raw_filesystem_path = filesystem_raw
    if filesystem_auto:
        raw_filesystem_path = bundle_root / "fs_usage.log"
        automatic_capture = MacOSFsUsageCapture(
            run_id=run_id,
            case_id=case_id,
            raw_path=raw_filesystem_path,
            target_prefix=target,
            additional_prefixes=filesystem_prefixes,
            capture_all_paths=True,
            timeout_seconds=max(1, int(timeout_seconds)),
        )
        automatic_capture.start()

    try:
        collector_exit_code = collect(
            target,
            prompt,
            events_path,
            manifest_path,
            run_id=run_id,
            case_id=case_id,
            model=model,
            staging_manifest=staging_manifest_path,
            runtime_manifest=runtime_manifest_path,
            sidecar_root=evaluator_root,
            filesystem_trace_source=(
                "macos-fs-usage" if raw_filesystem_path is not None
                else "unavailable"
            ),
            network_trace_source=("external-sidecar" if network_trace else "unavailable"),
            exact_read_path=(exact_read_path if exact_read else None),
            exact_read_library=(exact_read_library if exact_read else None),
            exact_read_required=exact_read,
            variation=variation,
            task_hash=task_hash,
            oracle_path=oracle,
            process_tree_path=process_tree_path,
            timeout_seconds=timeout_seconds,
        )
    finally:
        if automatic_capture is not None:
            raw_filesystem_path = automatic_capture.stop()

    process_pids: tuple[int, ...] | None = None
    process_names: tuple[str, ...] | None = None
    if process_tree_path.is_file():
        try:
            process_tree_payload = json.loads(
                process_tree_path.read_text(encoding="utf-8")
            )
            raw_pids = process_tree_payload.get("pids", [])
            if isinstance(raw_pids, list):
                process_pids = tuple(
                    int(pid) for pid in raw_pids if isinstance(pid, int)
                )
            raw_names = process_tree_payload.get("process_names", [])
            if isinstance(raw_names, list):
                process_names = tuple(
                    str(name) for name in raw_names if isinstance(name, str)
                )
        except (OSError, TypeError, ValueError, json.JSONDecodeError):
            process_pids = None
            process_names = None

    if raw_filesystem_path is not None:
        filesystem_trace_path = filesystem_path
        records = macos_fs_usage_sidecar(
            raw_filesystem_path.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines(),
            run_id=run_id,
            case_id=case_id,
            trace_id=f"trace-{run_id}",
            target_prefix=str(target),
            additional_prefixes=tuple(
                str(prefix.resolve()) for prefix in filesystem_prefixes
            ),
            process_pids=process_pids,
            process_names=process_names,
            capture_all_paths=bool(process_names),
        )
        with filesystem_path.open("x", encoding="utf-8") as stream:
            for record in records:
                json.dump(record, stream, sort_keys=True)
                stream.write("\n")

    if network_trace is not None:
        network_path.write_text(
            network_trace.read_text(encoding="utf-8", errors="replace"),
            encoding="utf-8",
        )

    effective_path_roots = dict(path_roots or {})
    effective_path_roots.setdefault("target", (str(target),))
    if filesystem_prefixes:
        effective_path_roots.setdefault(
            "skill",
            tuple(
                str(prefix.resolve())
                for prefix in filesystem_prefixes
                if "skill" in str(prefix).lower()
            ),
        )

    report = generate_report(
        events_path,
        manifest_path,
        oracle,
        identified_claims_path=identified_claims,
        filesystem_trace_path=filesystem_trace_path,
        network_trace_path=(network_path if network_trace is not None else None),
        exact_read_trace_path=(exact_read_path if exact_read else None),
        process_tree_path=process_tree_path,
        path_roots=effective_path_roots,
    )
    _write_json(report_path, report)

    bundle = RunBundle.from_root(bundle_root)
    return CaptureResult(
        bundle=bundle,
        collector_exit_code=collector_exit_code,
        validation=bundle.validate(),
    )


def _write_json(path: Path, payload: Any) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--evaluator-root", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument(
        "--variation",
        default="unspecified",
        help="Declared experimental variation for paired comparisons",
    )
    parser.add_argument(
        "--task-hash",
        help="Canonical task identity shared by controlled prompt variations",
    )
    parser.add_argument("--model")
    parser.add_argument("--identified-claims", type=Path)
    parser.add_argument(
        "--filesystem-raw",
        type=Path,
        help="Optional raw macOS fs_usage capture collected around this run",
    )
    parser.add_argument(
        "--filesystem-auto",
        action="store_true",
        help="Authorize and capture macOS fs_usage automatically around the run",
    )
    parser.add_argument(
        "--exact-read",
        action="store_true",
        help="Require exact returned-byte file evidence for this run",
    )
    parser.add_argument(
        "--filesystem-prefix",
        type=Path,
        action="append",
        default=[],
        help="Additional path prefix to include in filesystem evidence",
    )
    parser.add_argument(
        "--network-trace",
        type=Path,
        help="Optional externally collected network metadata JSONL",
    )
    parser.add_argument("--timeout-seconds", type=float, default=1800)
    args = parser.parse_args()

    result = capture_run(
        source=args.source,
        bundle_root=args.bundle,
        prompt=args.prompt,
        oracle=args.oracle,
        evaluator_root=args.evaluator_root,
        run_id=args.run_id,
        case_id=args.case_id,
        variation=args.variation,
        task_hash=args.task_hash,
        model=args.model,
        identified_claims=args.identified_claims,
        filesystem_raw=args.filesystem_raw,
        filesystem_auto=args.filesystem_auto,
        exact_read=args.exact_read,
        filesystem_prefixes=tuple(args.filesystem_prefix),
        network_trace=args.network_trace,
        timeout_seconds=args.timeout_seconds,
    )
    print(json.dumps({
        "bundle": str(result.bundle.root),
        "collector_exit_code": result.collector_exit_code,
        "valid": result.validation.valid,
        "filesystem_status": result.validation.filesystem_status,
        "network_status": result.validation.network_status,
        "issues": list(result.validation.issues),
    }, sort_keys=True))
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
