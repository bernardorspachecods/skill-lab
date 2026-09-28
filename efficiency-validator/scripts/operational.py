#!/usr/bin/env python3
"""Capture and inspect operational agent runs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from efficiency_validator.operational import capture, recover
from efficiency_validator.operational_report import annotate, save_report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    run = sub.add_parser("run", help="Fresh isolated CLI run; never overwrites a bundle")
    run.add_argument("--source", type=Path, required=True)
    run.add_argument("--bundle", type=Path, required=True)
    run.add_argument("--prompt-file", type=Path, required=True)
    run.add_argument("--variant", required=True)
    run.add_argument("--model")
    run.add_argument("--reasoning", choices=["minimal", "low", "medium", "high", "xhigh"])
    run.add_argument("--sandbox", choices=["read-only", "workspace-write"], default="workspace-write")
    run.add_argument("--timeout", type=float, default=300)
    run.add_argument("--codex", default="codex", help="CLI executable path")
    run.add_argument("--overlay", action="append", default=[], metavar="DEST=SOURCE",
                     help="Copy a context/skill file or directory into the isolated input")
    run.add_argument("--check", action="append", default=[], metavar='["python3","-m","unittest"]',
                     help="Evaluator verification command as JSON argv, not a shell string")
    regen = sub.add_parser("report", help="Regenerate offline from preserved evidence")
    regen.add_argument("bundle", type=Path)
    regen.add_argument("--output", type=Path)
    cancel = sub.add_parser("cancel", help="Request cancellation and partial evidence retention")
    cancel.add_argument("bundle", type=Path)
    recovery = sub.add_parser("recover", help="Finalize partial evidence after collector death")
    recovery.add_argument("bundle", type=Path)
    recovery.add_argument("--confirm-stopped", action="store_true", help="Confirm stopped state for older captures without PID metadata")
    note = sub.add_parser("annotate", help="Record an intervention not exposed by the runtime")
    note.add_argument("bundle", type=Path)
    note.add_argument("--kind", choices=["correction", "hint", "approval", "note"], required=True)
    note.add_argument("--text", required=True)
    note.add_argument("--start", type=float)
    note.add_argument("--end", type=float)
    args = parser.parse_args()
    try:
        if args.action == "run":
            checks = [json.loads(value) for value in args.check]
            if any(not isinstance(c, list) or not c or not all(isinstance(a, str) for a in c) for c in checks):
                raise ValueError("--check must be a nonempty JSON array of strings")
            overlays = {}
            for value in args.overlay:
                name, origin = value.split("=", 1)
                if name in overlays:
                    raise ValueError("Repeated overlay destination")
                overlays[name] = Path(origin)
            result = capture(args.source, args.bundle, prompt=args.prompt_file.read_text(),
                             variant=args.variant, model=args.model, reasoning=args.reasoning,
                             sandbox=args.sandbox, timeout=args.timeout, codex=args.codex,
                             overlays=overlays, checks=checks)
            save_report(args.bundle)
            print(json.dumps({"bundle": str(args.bundle), "termination": result["termination"],
                              "report": str(args.bundle / "derived/report.md")}))
            return 0 if result["termination"] == "completed" else 1
        if args.action == "report":
            result = save_report(args.bundle, args.output)
            print(json.dumps({"run_id": result["manifest"]["run_id"], "status": result["execution_status"]}))
        elif args.action == "cancel":
            manifest = json.loads((args.bundle / "manifest.json").read_text())
            if manifest.get("termination") != "running":
                raise ValueError("Only a running bundle can be cancelled")
            (args.bundle / "cancel.request").touch(exist_ok=False)
        elif args.action == "recover":
            recover(args.bundle, confirmed_stopped=args.confirm_stopped)
            save_report(args.bundle)
        elif args.action == "annotate":
            annotate(args.bundle, kind=args.kind, text=args.text, start=args.start, end=args.end)
            save_report(args.bundle)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
