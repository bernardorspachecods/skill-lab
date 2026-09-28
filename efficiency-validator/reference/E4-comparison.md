---
plan_id: E4
kind: subplan
parent: E0
phase: 4
status: complete
depends_on: [E2, E3]
consumers: [E5, future skill evaluations, context-lab reports]
---

# E4 — Paired comparison and automatic verdict

## Objective

Compare two equivalent runs under one declared variation and determine whether
the candidate preserves quality at lower observable cost.

## Scope

- Pair identity and equivalence validation.
- Cost normalization and availability states.
- Absolute/relative deltas, regressions, Pareto trade-offs, and verdicts.
- Explainable JSON report and CLI/library interface.

## Output

A deterministic comparison report with quality gate, normalized costs, deltas,
trade-offs, observability coverage, and one verdict:
`better`, `same`, `worse`, `tradeoff`, or `inconclusive`.

## Dependencies

- E2 run bundles and provenance.
- E3 quality reports.
- Declared primary cost objective, tolerances, and experiment variation.

## Sequence

1. **E4-S1 — Validate pair identity**
   - **Action:** Require matching task, target, model, runtime, prompt,
     oracle, observer, sandbox, and controlled-variation metadata.
   - **Output:** Pair schema and invalid-pair diagnostics.
   - **Exit check:** Uncontrolled differences are rejected, not normalized away.

2. **E4-S2 — Normalize observable costs**
   - **Action:** Normalize tokens, context, search/tool calls, commands,
     filesystem events, failures, retries, and time with provenance.
   - **Output:** Versioned cost vector with unavailable dimensions preserved.
   - **Exit check:** Missing metrics are never coerced to zero.

3. **E4-S3 — Calculate deltas and trade-offs**
   - **Action:** Compute absolute/relative deltas, quality differences,
     regressions, and Pareto relationships.
   - **Output:** Explainable comparison object.
   - **Exit check:** Synthetic cases produce stable, auditable calculations.

4. **E4-S4 — Emit the verdict**
   - **Action:** Apply the quality gate, primary objective, tolerances, and
     coverage policy in a fixed order.
   - **Output:** Verdict with reasons and machine-readable evidence.
   - **Exit check:** A cheaper incomplete answer cannot be `better`.

## Consumers

- E5 consumes comparison reports for fixture and real-pair validation.
- Future skill evaluations consume verdicts and trade-off explanations.
- Context-lab reports aggregate normalized deltas by skill, task, model, and
  runtime.

## Completion criteria

- Equivalent tasks can be compared with one explicit controlled variation.
- Costs carry units, provenance, and availability state.
- Deltas and trade-offs are deterministic and explainable.
- All verdict classes have fixtures.
- The CLI can reproduce a verdict from saved run bundles and policy.
