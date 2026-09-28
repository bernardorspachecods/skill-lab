---
plan_id: V3
kind: subplan
parent: V0
phase: 3
status: complete
depends_on: [V1, V2]
consumers: [V4, reviewers, future dashboards]
---

# V3 — Exhaustive report and prompt diff

## Objective

Make one saved report sufficient for a human to inspect the complete
difference between runs before any later filtering or dashboarding.

## Scope

- Full explicit prompt and structured variation for every run.
- Prompt hash and human-readable prompt diff.
- Raw events plus derived metrics in the same report contract.
- Calls, tokens, context, filesystem, failures, retries, timings, quality,
  provenance, and availability states.
- Technical evidence and analysis inputs may be grouped, but no information is
  removed or hidden in this first version.

## Output

An exhaustive report schema and CLI that show the complete run and pair
difference without requiring manual arithmetic or raw JSONL inspection.

## Sequence

1. **V3-S1 — Design report contract**
   - **Action:** Map every captured field to raw evidence, derived metric,
     provenance, or analysis input.
   - **Output:** Versioned report schema.
   - **Exit check:** Each displayed number links to its source and unit.

2. **V3-S2 — Render run and pair views**
   - **Action:** Add complete single-run and baseline/candidate diff output,
     including prompts and unavailable reasons.
   - **Output:** Reconstructable report CLI.
   - **Exit check:** A reviewer can identify every material difference from one
     report artifact.

3. **V3-S3 — Test losslessness**
   - **Action:** Replay fixtures and compare raw-to-report coverage.
   - **Output:** Report coverage tests.
   - **Exit check:** No required observable field disappears during rendering.

## Completion criteria

- Prompts are visible and diffable.
- Raw and derived evidence coexist without premature filtering.
- Calls, tokens, context, filesystem, failures, retries, timing, quality, and
  provenance are visible with units and status.
