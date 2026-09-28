---
plan_id: O2
kind: subplan
parent: O0
phase: 2
status: complete
depends_on: [O1]
consumers: [operator, experiment comparison reports, docs/analysis-acceptance.md]
---

# Phase 2 — Analysis

## Objective

Turn operational bundles into useful comparisons of context and skill variants
under the [root plan](PLAN_operational-evaluator.md). Refine analytical choices after phase 1 works.

## Scope

Quality, navigation, observed reading/repetition, tokens, time, interventions
and variation across runs. Only claim what the operational evidence supports.
Do not make this phase a prerequisite for using the collector.

## Output

A comparative report that explains measured differences, quality outcomes,
trade-offs and uncertainty, linked to the underlying runs.

## Sequence

1. **S1 — Define comparable experiments**
   - **Action:** Agree task identity, controlled variation, quality criteria and
     repetition policy from available bundles; reuse existing comparison logic
     where its assumptions hold.
   - **Output:** Experiment configuration and evidence eligibility rules.
   - **Exit check:** Confounded or incomplete pairs cannot support claims that
     require the missing controls.
2. **S2 — Calculate supported dimensions**
   - **Action:** Calculate cost and navigation measures from captured evidence.
     Use task references when judging relevance; distinguish observed repeated
     outputs from complete filesystem rereads. Apply quality before efficiency
     judgments and label estimates or heuristic classifications.
   - **Output:** Traceable per-run and cross-run measurements.
   - **Exit check:** Each value identifies its evidence and meaning; unsupported
     dimensions are unavailable without blocking independent comparisons.
3. **S3 — Explain differences and uncertainty**
   - **Action:** Report deltas, distributions across repetitions, quality and
     trade-offs. Validate against controlled examples and real variant runs.
   - **Output:** Human-readable comparison with underlying structured results.
   - **Exit check:** A single pair is described as a case observation; general
     improvement claims require adequate repeated evidence.

## Completion criteria

- Real variant runs produce a report with inspectable supporting evidence.
- Quality losses and missing measurements are visible in conclusions.
- Navigation and reading claims respect the demonstrated capture boundary.
- Analytical configuration can evolve without rerunning already sufficient
  capture or changing the meaning of preserved raw evidence.

## Execution findings

- S1–S2 are implemented by `operational_analysis.py` and
  `scripts/compare_operational.py`. Pair identity checks cover prompt, starting
  target, requested model, reasoning effort and sandbox; variants may differ in
  retained overlays.
- S3 produced [the first comparison acceptance record](../docs/analysis-acceptance.md)
  from two real completed Codex bundles. It is explicitly exploratory because
  only one pair exists. The report remains regenerable offline and links to both
  source runs.
