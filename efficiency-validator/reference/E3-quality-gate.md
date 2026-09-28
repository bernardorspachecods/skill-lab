---
plan_id: E3
kind: subplan
parent: E0
phase: 3
status: complete
depends_on: [E1, E2]
consumers: [E4, E5, future skill evaluations]
---

# E3 — Quality gate and answer adjudication

## Objective

Convert evaluator evidence into a deterministic quality result so cost savings
cannot compensate for missing required information, prohibited claims, weak
authority, or unsupported answers.

## Scope

- Required and disallowed claims.
- Completeness, correctness, authority, and support.
- Parser/process status and answer usability.
- Quality result schema with concrete failure reasons.

## Output

A quality report for one run with pass/fail/indeterminate status, claim-level
evidence, authority/support findings, and a machine-readable gate decision.

## Dependencies

- E1 observability contract.
- E2 reusable run bundle.
- Existing evaluator oracles and claim-adjudication model.

## Sequence

1. **E3-S1 — Freeze claim semantics**
   - **Action:** Define required, disallowed, optional, and authority-sensitive
     claim types.
   - **Output:** Versioned quality policy.
   - **Exit check:** Every oracle claim maps to one adjudication state.

2. **E3-S2 — Implement claim and evidence adjudication**
   - **Action:** Evaluate final answers against claims, sources, support, and
     completion state.
   - **Output:** Deterministic quality result and failure reasons.
   - **Exit check:** Missing or prohibited claims fail the gate explicitly.

3. **E3-S3 — Handle uncertain evidence**
   - **Action:** Preserve unknown, partial, unavailable, and parser-failed
     evidence without treating it as a pass or zero.
   - **Output:** Quality coverage and indeterminacy fields.
   - **Exit check:** A run with insufficient evidence cannot receive a clean
     quality pass silently.

4. **E3-S4 — Test quality mutations**
   - **Action:** Add fixtures for complete answers, omissions, prohibited
     claims, wrong authority, unsupported assertions, and failed runs.
   - **Output:** Quality-gate test matrix.
   - **Exit check:** Each quality failure has a stable reason and status.

## Consumers

- E4 uses the quality gate before calculating efficiency verdicts.
- E5 uses quality mutations for regression and calibration.
- Future skill evaluations use quality status as the primary safety gate.

## Completion criteria

- Quality is machine-readable and independent from cost.
- Required and disallowed claims affect the result.
- Authority and support are evaluated explicitly.
- Unknown or unavailable evidence remains distinct from failure and success.
- Fixtures cover all declared quality outcomes.
