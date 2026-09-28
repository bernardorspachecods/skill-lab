---
plan_id: V2
kind: subplan
parent: V0
phase: 2
status: complete
depends_on: [V1]
consumers: [V3, validator reports, run bundles]
---

# V2 — Exhaustive observable capture

## Objective

Capture the maximum evidence available at the runtime boundary so the report
can explain both cost and the path taken by each run.

## Scope

- Explicit and effective prompts, skill/context artifacts, and prompt inputs.
- Turns, command/tool/search calls, call outcomes, retries, failures, and
  timing.
- Token categories, input/context usage, cache usage, output, reasoning, and
  derived totals.
- Filesystem traces and all unavailable/denied/partial reasons.
- Raw event retention and correlation to run, turn, command, and process.

## Output

An exhaustive run bundle containing raw observable evidence and explicit
availability/provenance records for every attempted signal.

## Sequence

1. **V2-S1 — Inventory observable surfaces**
   - **Action:** Audit Codex events, collector boundaries, runtime hooks, and
     OS tracing without promoting agent prose to authority.
   - **Output:** Observable-surface matrix.
   - **Exit check:** Every desired metric is marked authoritative, secondary,
     or unavailable with a reason.

2. **V2-S2 — Extend collection**
   - **Action:** Preserve raw events and add structured records for all
     observable calls, prompts, context, tokens, failures, and timings.
   - **Output:** Extended trace schema and collector.
   - **Exit check:** Fixtures prove complete, partial, malformed, denied, and
     unavailable captures remain distinguishable.

3. **V2-S3 — Verify boundaries and privacy**
   - **Action:** Keep target isolation, evaluator separation, redaction, and
     privileged filesystem capture explicit.
   - **Output:** Boundary and retention rules.
   - **Exit check:** The measured target receives no evaluator or validator
     dependency, and sensitive raw data has an explicit retention policy.

## Completion criteria

- A run can expose all currently observable prompt, context, call, token,
  filesystem, failure, retry, and timing data.
- Raw evidence is retained and correlated without relying on self-report.
- Unsupported or privileged signals remain explicit rather than silently zero.
