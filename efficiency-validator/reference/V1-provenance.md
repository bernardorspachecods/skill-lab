---
plan_id: V1
kind: subplan
parent: V0
phase: 1
status: complete
depends_on: []
consumers: [V2, V3, V4, validator manifests]
---

# V1 — Run identity and provenance

## Objective

Bind every run to the exact prompt, oracle, controlled variation, skill/context
inputs, and execution identity needed to judge whether a pair is comparable.

## Scope

- Manifest fields and validation for prompt/oracle/variation provenance.
- Exact prompt bytes, canonical `prompt_hash`, and task identity semantics.
- Oracle path, case identity, oracle digest, and evaluator revision.
- Structured variation metadata rather than a free-text label alone.
- Skill/context artifact paths and digests when observable.

## Output

A versioned provenance contract and manifest implementation that cannot silently
represent missing identity as a trustworthy run.

## Sequence

1. **V1-S1 — Define identities**
   - **Action:** Specify prompt, task, oracle, variation, skill/context, target,
     runtime, model, and observer identities.
   - **Output:** Field-level contract with canonicalization rules.
   - **Exit check:** Equal and intentionally different inputs produce distinct
     hashes and structured metadata.

2. **V1-S2 — Capture and validate metadata**
   - **Action:** Extend collector and capture orchestration to write the
     contract and reject missing mandatory provenance.
   - **Output:** Provenance-complete manifests and diagnostics.
   - **Exit check:** A pair with a changed prompt, oracle, or uncontrolled
     variation is rejected with a concrete reason.

3. **V1-S3 — Cover legacy and unavailable states**
   - **Action:** Add fixtures for old manifests, missing fields, inaccessible
     skill files, and hidden/unobservable instructions.
   - **Output:** Migration and unavailable-state policy.
   - **Exit check:** Legacy artifacts are readable as historical but cannot pass
     the new evidence gate without explicit migration data.

## Completion criteria

- Exact prompt, `prompt_hash`, oracle identity/digest, and structured variation
  are present or explicitly unavailable.
- Manifest and pair validation consume those fields.
- No comparison can treat a missing provenance field as equivalent to zero or
  as proof that two runs were controlled.
