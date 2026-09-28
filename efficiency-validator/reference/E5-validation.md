---
plan_id: E5
kind: subplan
parent: E0
phase: 5
status: complete
depends_on: [E4]
consumers: [future skill evaluations, context-lab reports, dashboards]
---

# E5 — Validation and operationalization

## Objective

Demonstrate that the reusable validator is reliable enough for repeated skill
evaluations and expose its remaining blind spots clearly.

## Scope

- Unit, contract, integration, and regression fixtures.
- Repeated paired runs and result stability.
- One real controlled comparison.
- Documentation, versioning, and future dashboard/export seams.

## Output

A validated release of the efficiency validator with an example real-pair
report, calibration notes, regression suite, and operational limitations.

## Dependencies

- E2 reusable capture pipeline.
- E3 quality-gate fixtures.
- E4 comparison/verdict implementation.
- A controlled task and declared variation.

## Sequence

1. **E5-S1 — Build the fixture matrix**
   - **Action:** Cover quality outcomes, verdict classes, missing signals,
     malformed artifacts, pair mismatches, and trade-offs.
   - **Output:** Complete deterministic fixture suite.
   - **Exit check:** Every branch in the report policy has a fixture.

2. **E5-S2 — Test repeatability**
   - **Action:** Replay identical bundles and compare report hashes and reasons.
   - **Output:** Stability evidence and nondeterminism policy.
   - **Exit check:** Same inputs and policy produce the same report.

3. **E5-S3 — Run one real controlled pair**
   - **Action:** Capture baseline and one variation against the same pinned
     task, target, model, runtime, and oracle.
   - **Output:** End-to-end paired report.
   - **Exit check:** No manual arithmetic or hidden missing metric is needed.

4. **E5-S4 — Publish operational contract**
   - **Action:** Document installation, capture permissions, artifact retention,
     privacy, version upgrades, and known blind spots.
   - **Output:** Reusable operator/developer documentation.
   - **Exit check:** A future skill evaluation can run the validator without
     bespoke interpretation.

## Consumers

- Future skill evaluations use the release contract and CLI.
- Context-lab reports and dashboards consume stable JSON output.
- Runtime upgrades use the regression and compatibility fixtures.

## Completion criteria

- All declared quality, cost, pairing, and observability branches are tested.
- One real pair completes end to end.
- Repeated identical inputs are reproducible.
- Limitations and authorization requirements are explicit.
- The validator is ready for repeated skill comparisons.

## Verification record

- The fixture and full validator suite pass with 42 tests.
- A real controlled pair used the same canonical task hash,
  `context-lab-target` revision, runtime lock, model, oracle, and sandbox.
- Baseline variation `without-skill`: 16 commands and 626,149 total tokens.
- Candidate variation `with-skill`: 14 commands and 565,734 total tokens.
- Both quality reports passed all five required claims, had no disallowed
  claims, and passed authority/support checks.
- The comparison report emitted `better` with a 60,415-token reduction
  (9.65%), while leaving filesystem cost explicitly unavailable for both runs.
- Recomputing the comparison twice produced the same stable JSON digest.
