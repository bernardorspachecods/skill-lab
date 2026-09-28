---
plan_id: R4
kind: subplan
parent: R0
phase: 4
status: complete
depends_on: [R1, R2, R3]
consumers: [R5, context-lab, future skill evaluations]
---

# R4 — Fail-closed reporting gate

> Archived on 2026-09-26; superseded by [the operational evaluator plan](PLAN_operational-evaluator.md).
> Status fields below preserve historical claims, not verified completion.

## Objective

Make exact-read completeness a mandatory eligibility condition for file-based
efficiency comparisons and verdicts.

## Scope

- Run validity and per-read completeness checks.
- Manifest and report integration.
- Existing token, context, command, search, timing, network, and quality
  metrics as separate evidence dimensions.
- Invalid-run explanations and comparison suppression.
- Human-readable exact-read summary and machine-readable status.

## Output

A reporting and comparison gate that emits a verdict only for complete exact
read ledgers and explains every rejection.

## Sequence

1. **R4-S1 — Define validity aggregation**
   - **Action:** Aggregate per-event and per-process coverage into a run-level
     exact-read status.
   - **Output:** Deterministic validity function and failure reasons.
   - **Exit check:** One missing or unverifiable read makes the run invalid.
2. **R4-S2 — Integrate reports and manifests**
   - **Action:** Add exact-read evidence and status to raw and reviewer-facing
     artifacts.
   - **Output:** Complete report section with ledger summary.
   - **Exit check:** Reports cannot present invalid runs as comparable.
3. **R4-S3 — Gate comparisons**
   - **Action:** Require valid exact-read evidence before file-efficiency cost
     deltas or verdicts are calculated.
   - **Output:** Fail-closed comparison behavior.
   - **Exit check:** Invalid baseline, candidate, or pair produces no verdict.

## Completion criteria

- No incomplete exact-read run can produce an efficiency verdict.
- Every invalidation names the missing or unverifiable evidence.
- Existing metrics remain available without being confused with file-read
  proof.
- The report shows exact files, bytes, lines, and categories used in analysis.
