#!/usr/bin/env python3
"""Stage one immutable target revision outside the measured workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from efficiency_validator.staging import stage_target
except ModuleNotFoundError:  # direct execution from the repository checkout
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from efficiency_validator.staging import stage_target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    manifest = stage_target(args.source, args.destination)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest.open("x", encoding="utf-8") as stream:
        json.dump(manifest.to_dict(), stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(manifest.staged_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
