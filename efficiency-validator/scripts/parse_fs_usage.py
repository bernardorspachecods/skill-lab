#!/usr/bin/env python3
"""Convert a macOS fs_usage pathname capture into a filesystem sidecar."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from efficiency_validator.filesystem import macos_fs_usage_sidecar
except ModuleNotFoundError:  # direct execution from the repository checkout
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from efficiency_validator.filesystem import macos_fs_usage_sidecar


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--trace-id", required=True)
    parser.add_argument("--target-prefix", required=True)
    parser.add_argument(
        "--additional-prefix",
        action="append",
        default=[],
        help="Additional path prefix for the basic scoped mode",
    )
    parser.add_argument(
        "--process-tree",
        type=Path,
        help="process-tree-1 JSON used to filter all paths to measured PIDs",
    )
    parser.add_argument(
        "--capture-all-paths",
        action="store_true",
        help="Parse all paths, requiring --process-tree for safety",
    )
    args = parser.parse_args()

    if args.capture_all_paths and args.process_tree is None:
        parser.error("--capture-all-paths requires --process-tree")

    process_pids = None
    if args.process_tree is not None:
        process_tree = json.loads(args.process_tree.read_text(encoding="utf-8"))
        raw_pids = process_tree.get("pids", [])
        if not isinstance(raw_pids, list):
            parser.error("process-tree pids must be a JSON list")
        process_pids = tuple(int(pid) for pid in raw_pids)

    records = macos_fs_usage_sidecar(
        args.input.read_text(encoding="utf-8", errors="replace").splitlines(),
        run_id=args.run_id,
        case_id=args.case_id,
        trace_id=args.trace_id,
        target_prefix=args.target_prefix,
        additional_prefixes=args.additional_prefix,
        process_pids=process_pids,
        capture_all_paths=args.capture_all_paths,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        for record in records:
            json.dump(record, stream, sort_keys=True)
            stream.write("\n")
    print(f"{len(records) - 1} filesystem events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
