---
plan_id: R5
kind: subplan
parent: R0
phase: 5
status: complete
depends_on: [R4]
consumers: [efficiency-validator/docs, context-lab/runs, future skill evaluations]
---

# R5 — Fixtures and controlled validation

> Archived on 2026-09-26; superseded by [the operational evaluator plan](PLAN_operational-evaluator.md).
> Status fields below preserve historical claims, not verified completion.

## Objective

Prove that exact-read mode is reliable enough for repeated efficiency
comparisons and document every remaining unsupported condition.

## Scope

- Fixtures for shell, search, scripting, mapped, repeated, partial, binary,
  mutated, deleted, and child-process reads.
- Negative tests for permission loss, process escape, truncation, malformed
  sidecars, and missing content.
- Controlled paired evaluations across all path categories.
- Performance, bundle size, sensitive-content, and operational documentation.

## Output

A regression suite, controlled evidence bundles, protocol documentation, and a
reviewed list of remaining limitations that block official verdicts.

## Sequence

1. **R5-S1 — Build positive and negative fixtures**
   - **Action:** Exercise every R1 access class and every invalidation reason.
   - **Output:** Deterministic exact-read fixture corpus.
   - **Exit check:** Expected bytes and lines match independently calculated
     ground truth.
2. **R5-S2 — Run controlled process-tree evaluations**
   - **Action:** Measure target, skill, external, cache, dependency, and
     system reads in paired runs.
   - **Output:** Complete valid and intentionally invalid bundles.
   - **Exit check:** Valid bundles pass; every injected gap is rejected.
3. **R5-S3 — Document operational limits**
   - **Action:** Record host permissions, supported APIs, retention, overhead,
     and safe handling requirements.
   - **Output:** Exact-read run protocol and limitation register.
   - **Exit check:** A new operator can tell before a run whether an exact
     verdict will be eligible.

## Completion criteria

- Positive fixtures prove exact bytes and lines for every supported operation.
- Negative fixtures prove fail-closed behavior for every declared gap.
- At least one controlled paired evaluation produces a valid file-efficiency
  verdict with a complete read ledger.
- Unsupported mechanisms are explicit, tested, and prevented from producing
  official verdicts.
