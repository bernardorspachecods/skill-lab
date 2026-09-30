---
plan_id: LR-03.SP-04
kind: subplan
parent: LR-03
phase: S4
status: not_started
depends_on: [LR-03.SP-03#outcome]
consumers: []
---

# LR-03.SP-04

## Objective

Improve how `$research` turns inspected sources into direct findings that
answer the user's question.

## Scope

Make the transition from source selection to extraction and synthesis
operational. Define what to extract from each source, how to connect it to a
material claim or question, how to state what the evidence establishes and
does not establish, and how to combine evidence into a direct finding. Preserve
the skill's evidence IDs, source provenance, independence checks, and
confidence calibration. Use the scoped question and search paths from
[LR-03.SP-03#outcome](../LR-03.SP-03/PLAN.md#outcome). Do not design the final
consumer-facing document structure in this unit.

Inputs: the user's fourth reported failure mode, the current
[`$research` skill](../../../../agent-skills/skills/research/SKILL.md), and
the reconciled outcome of [LR-03.SP-03](../LR-03.SP-03/PLAN.md).

## Output

A targeted update to the extraction and synthesis workflow, with a concise
Outcome record of the change and verification.

## Sequence

1. **S4 — Extract evidence into findings**
   - **Action:** Research and define a practical evidence-to-finding path,
     then revise the skill so source inspection produces answers to the
     prioritized questions rather than a pile of source summaries.
   - **Output:** The completed edit to the evaluation and synthesis workflow.
   - **Exit check:** Each material finding connects the question, claim,
     evidence, and supported conclusion, with limits preserved.

## Completion criteria

- The skill specifies what information to extract and how it answers a
  prioritized question or claim.
- Direct findings are distinguishable from source summaries, inference, and
  recommendation.
- Evidence is evaluated for support, scope, provenance, date, and conflict
  before it is synthesized.
- Findings state material limits rather than turning strong sources into
  unsupported certainty.
- The subplan Outcome records the changed section and the check performed.

## Outcome

[Record completion, verification, and material differences when the unit is complete.]
