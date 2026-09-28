#!/usr/bin/env python3
"""Prepare a locked target runtime outside the staged workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from efficiency_validator.runtime import prepare_runtime
except ModuleNotFoundError:  # direct execution from the repository checkout
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from efficiency_validator.runtime import prepare_runtime


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--staging-manifest", type=Path, required=True)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    manifest = prepare_runtime(
        args.target,
        args.staging_manifest,
        args.runtime,
        args.manifest,
    )
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest.open("x", encoding="utf-8") as stream:
        json.dump(manifest.to_dict(), stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(manifest.runtime_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
