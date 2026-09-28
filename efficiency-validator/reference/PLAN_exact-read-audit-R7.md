---
plan_id: R7
kind: subplan
parent: R0
phase: 7
status: not_started
depends_on: [R6]
consumers: [R8, efficiency-validator/scripts]
---

# R7 — Real Codex CLI runtime integration

> Archived on 2026-09-26; superseded by [the operational evaluator plan](PLAN_operational-evaluator.md).
> Status fields below preserve historical claims, not verified completion.

## Objective

Launch a real Codex CLI session through the selected capture boundary without
changing the task semantics or silently losing descendants.

## Scope

- `codex exec --json` lifecycle and exit handling.
- Launcher, shell, tool, script, search, and short-lived child processes.
- Exact sidecar startup, shutdown, flushing, and process-tree correlation.
- Read-only sandbox and evaluator isolation.

## Output

A reusable real-CLI capture mode that produces a correlated process and exact
read sidecar for an actual Codex task.

## Sequence

1. **R7-S1 — Wire the selected launcher**
   - **Action:** Integrate the chosen boundary into `capture_run` and preserve
     existing Codex arguments and environment contracts.
   - **Output:** One command that launches real Codex with exact capture.
   - **Exit check:** The CLI starts and completes a normal read-only task.
2. **R7-S2 — Prove process lifecycle coverage**
   - **Action:** Correlate root, descendants, exec replacements, and short-lived
     tools with the exact sidecar and process artifact.
   - **Output:** Real process-tree coverage report.
   - **Exit check:** An uninstrumented or escaped PID invalidates the run.
3. **R7-S3 — Prove failure propagation**
   - **Action:** Inject timeout, permission, child escape, and sidecar truncation
     conditions.
   - **Output:** Real-CLI failure bundles with concrete reasons.
   - **Exit check:** No failure mode produces a valid exact report.

## Completion criteria

- A real Codex CLI run emits complete trace lifecycle records.
- Every observed local-file reader is process-correlated.
- Existing Codex output, token, and command evidence remains intact.
