#!/usr/bin/env python3
"""Compare two operational-1 run bundles."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from efficiency_validator.operational_analysis import save_comparison


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--baseline", type=Path, required=True)
parser.add_argument("--candidate", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--tolerance", type=float, default=0.05)
args = parser.parse_args()
result = save_comparison(args.baseline, args.candidate, args.output, tolerance=args.tolerance)
print(f"{result['verdict']} ({result['evidence_status']})")
