#!/usr/bin/env python3
"""Generate a deterministic command-level report from one captured run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from efficiency_validator.codex_events import parse_codex_stream
    from efficiency_validator.exact_read import parse_exact_read_trace
    from efficiency_validator.filesystem import parse_filesystem_trace
    from efficiency_validator.network import parse_network_trace
    from efficiency_validator.manifest import RunManifest
    from efficiency_validator.reporting import build_command_report
except ModuleNotFoundError:  # direct execution from the repository checkout
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from efficiency_validator.codex_events import parse_codex_stream
    from efficiency_validator.exact_read import parse_exact_read_trace
    from efficiency_validator.filesystem import parse_filesystem_trace
    from efficiency_validator.network import parse_network_trace
    from efficiency_validator.manifest import RunManifest
    from efficiency_validator.reporting import build_command_report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--identified-claims", type=Path)
    parser.add_argument(
        "--filesystem-trace",
        type=Path,
        help="Optional authoritative JSONL filesystem sidecar",
    )
    parser.add_argument("--network-trace", type=Path)
    parser.add_argument("--exact-read-trace", type=Path)
    parser.add_argument("--process-tree", type=Path)
    parser.add_argument(
        "--path-root",
        action="append",
        default=[],
        metavar="CATEGORY=PATH",
        help="Path classification root, repeatable",
    )
    args = parser.parse_args()

    report = generate_report(
        args.events,
        args.manifest,
        args.oracle,
        identified_claims_path=args.identified_claims,
        filesystem_trace_path=args.filesystem_trace,
        network_trace_path=args.network_trace,
        exact_read_trace_path=args.exact_read_trace,
        process_tree_path=args.process_tree,
        path_roots=_parse_path_roots(args.path_root),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    return 0


def generate_report(
    events_path: Path,
    manifest_path: Path,
    oracle_path: Path,
    *,
    identified_claims_path: Path | None = None,
    filesystem_trace_path: Path | None = None,
    network_trace_path: Path | None = None,
    exact_read_trace_path: Path | None = None,
    process_tree_path: Path | None = None,
    path_roots: dict[str, tuple[str, ...]] | None = None,
) -> dict[str, object]:
    """Build one report from a captured run without owning its CLI process."""

    parsed = parse_codex_stream(
        events_path.read_text(encoding="utf-8", errors="replace").splitlines()
    )
    manifest = RunManifest.from_dict(
        json.loads(manifest_path.read_text(encoding="utf-8"))
    )
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    identified_claims = ()
    if identified_claims_path:
        identified_claims = json.loads(
            identified_claims_path.read_text(encoding="utf-8")
        )
    filesystem_trace = None
    if filesystem_trace_path:
        filesystem_trace = parse_filesystem_trace(
            filesystem_trace_path.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines(),
            expected_run_id=manifest.run_id,
            expected_case_id=manifest.case_id,
        )
    network_trace = None
    if network_trace_path:
        network_trace = parse_network_trace(
            network_trace_path.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines(),
            expected_run_id=manifest.run_id,
            expected_case_id=manifest.case_id,
        )
    exact_read_trace = None
    if exact_read_trace_path:
        exact_read_trace = parse_exact_read_trace(
            exact_read_trace_path.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines(),
            expected_run_id=manifest.run_id,
            expected_case_id=manifest.case_id,
        )
    process_tree_pids = None
    if process_tree_path:
        try:
            process_tree = json.loads(
                process_tree_path.read_text(encoding="utf-8")
            )
            raw_pids = process_tree.get("pids", [])
            if isinstance(raw_pids, list):
                process_tree_pids = tuple(
                    int(pid) for pid in raw_pids if isinstance(pid, int)
                )
        except (OSError, TypeError, ValueError, json.JSONDecodeError):
            process_tree_pids = None
    report = build_command_report(
        parsed,
        manifest,
        oracle,
        identified_claim_ids=identified_claims,
        filesystem_trace=filesystem_trace,
        network_trace=network_trace,
        exact_read_trace=exact_read_trace,
        exact_read_process_tree_pids=process_tree_pids,
        path_roots=path_roots,
    )
    return report


def _parse_path_roots(specs: list[str]) -> dict[str, tuple[str, ...]]:
    roots: dict[str, list[str]] = {}
    for spec in specs:
        if "=" not in spec:
            raise ValueError(f"path root must use CATEGORY=PATH: {spec!r}")
        category, path = spec.split("=", 1)
        if not category or not path:
            raise ValueError(f"path root must use CATEGORY=PATH: {spec!r}")
        roots.setdefault(category, []).append(path)
    return {category: tuple(paths) for category, paths in roots.items()}


if __name__ == "__main__":
    raise SystemExit(main())
