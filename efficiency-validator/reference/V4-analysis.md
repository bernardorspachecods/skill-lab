---
plan_id: V4
kind: subplan
parent: V0
phase: 4
status: complete
depends_on: [V1, V3]
consumers: [V5, future skill evaluations, context-lab reports]
---

# V4 — Trustworthy comparison and aggregation

## Objective

Prevent incomplete provenance, contaminated controls, and stochastic single-run
results from being presented as reliable skill conclusions.

## Scope

- Pair integrity over prompt, oracle, target, runtime, model, skill, and
  controlled variation evidence.
- Baseline isolation and detection of automatically applied interventions.
- Quality-gated cost comparisons and explicit exploratory status.
- Replicate aggregation, variance, distribution, and confidence limitations.
- Verdict explanations that distinguish better, worse, mixed, and unsupported.

## Output

A conservative comparison and aggregate-analysis contract that only supports a
claim when the evidence contract and quality gate pass.

## Sequence

1. **V4-S1 — Gate pair eligibility**
   - **Action:** Reject missing/mismatched provenance and uncontrolled
     interventions before cost comparison.
   - **Output:** Pair-integrity diagnostics.
   - **Exit check:** A declared variation cannot compensate for missing actual
     prompt, oracle, or skill evidence.

2. **V4-S2 — Aggregate replicates**
   - **Action:** Compute per-pair deltas plus mean, median, spread, and verdict
     counts without hiding mixed outcomes.
   - **Output:** Aggregate report schema.
   - **Exit check:** One favorable run cannot establish a skill advantage when
     replicates disagree or variance is high.

3. **V4-S3 — Separate evidence from interpretation**
   - **Action:** Mark results exploratory, supported, or blocked according to
     evidence coverage and declared thresholds.
   - **Output:** Conservative analytical verdict.
   - **Exit check:** The report explains why a result is inconclusive instead of
     forcing `better` or `worse`.

## Completion criteria

- Pair comparison validates actual provenance, not only labels.
- Aggregates reveal variance and mixed verdicts.
- Quality remains a non-negotiable gate.
- Under-specified or contaminated evaluations cannot be published as claims.
