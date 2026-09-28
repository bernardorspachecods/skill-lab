---
plan_id: R9
kind: subplan
parent: R0
phase: 9
status: not_started
depends_on: [R8]
consumers: [R10, context-lab/runs, future skill evaluations]
---

# R9 — End-to-end paired verdict

> Archived on 2026-09-26; superseded by [the operational evaluator plan](PLAN_operational-evaluator.md).
> Status fields below preserve historical claims, not verified completion.

## Objective

Prove that two equivalent real Codex CLI runs can be compared on exact file
efficiency while preserving quality and provenance gates.

## Scope

- Same task, target, oracle, model/runtime, and evaluator.
- One controlled architecture/skill variation.
- Exact bytes/lines plus tokens, commands, network, timing, and quality as
  separate dimensions.
- Invalid baseline, candidate, and pair behavior.

## Output

Two valid real-CLI reports, one comparison report, and a reviewer-facing
verdict with deltas and trade-offs.

## Sequence

1. **R9-S1 — Capture the paired runs**
   - **Action:** Execute baseline and candidate through the selected real-CLI
     boundary with identical task identity.
   - **Output:** Paired exact-read bundles and manifests.
   - **Exit check:** Both bundles pass exact and quality validity.
2. **R9-S2 — Compare exact costs**
   - **Action:** Run the existing comparison layer with exact bytes/lines as
     eligible metrics and other costs kept separate.
   - **Output:** Deltas, trade-offs, prompt diff, and verdict.
   - **Exit check:** The verdict is non-blocked only when both exact ledgers
     are valid.
3. **R9-S3 — Break the pair deliberately**
   - **Action:** Remove or corrupt one read, process record, or snapshot.
   - **Output:** Rejected comparison report.
   - **Exit check:** No corrupted pair receives `better`, `same`, or `worse`.

## Completion criteria

- A real Codex pair produces a valid file-efficiency verdict.
- Quality failures and prohibited claims still override cost improvements.
- Exact and general observability metrics remain distinguishable.
