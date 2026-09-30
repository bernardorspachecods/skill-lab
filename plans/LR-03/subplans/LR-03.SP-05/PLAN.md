---
plan_id: LR-03.SP-05
kind: subplan
parent: LR-03
phase: S5
status: not_started
depends_on: [LR-03.SP-04#outcome]
consumers: []
---

# LR-03.SP-05

## Objective

Ensure `$research` delivers findings in a form the intended consumer can use,
while keeping detailed evidence and internal process records in their proper
supporting artifacts.

## Scope

Define how the researcher chooses an answer structure from the consumer's
question and use, leads with the conclusion or direct findings, and keeps
confidence, provenance, and detailed guardrails appropriately accessible.
Account for requests such as best practices organized by topic or situation,
with source and confidence details available separately. Keep the consumer
answer distinct from the audit artifact and disposable working record. Use the
extraction guidance from
[LR-03.SP-04#outcome](../LR-03.SP-04/PLAN.md#outcome), then integrate and
reconcile the full skill. Do not change the research identity or artifact
lifecycle without evidence and an approved scope change.

Inputs: the user's fifth reported failure mode and example, the current
[`$research` skill](../../../../agent-skills/skills/research/SKILL.md), and
the reconciled outcome of [LR-03.SP-04](../LR-03.SP-04/PLAN.md).

## Output

An integrated revision of the canonical `$research` skill and a concise
Outcome record describing the final changes, validation, and any material
difference from this brief.

## Sequence

1. **S5 — Shape consumer and support outputs**
   - **Action:** Research useful output patterns for consumer-facing
     synthesis and evidence support, then revise and integrate the skill.
   - **Output:** The integrated skill revision and final unit Outcome.
   - **Exit check:** A representative request can produce a structured,
     readable answer with confidence and sources auditable without merging all
     internal workflow detail into the answer.

## Completion criteria

- The output format follows the consumer's need and leads with direct findings.
- The answer is separated from the detailed audit trail and disposable search
  record, with links or identifiers that preserve traceability where needed.
- Confidence and limitations are visible at the point useful to the consumer
  without requiring the full audit to be read first.
- The example of best practices organized by topic or situation is supported
  without making every answer use the same template.
- All five changes read as one coherent workflow, with no contradictory or
  duplicated rules.
- The canonical skill's frontmatter and links validate, and the root
  completion criteria are met.

## Outcome

[Record completion, verification, and material differences when the unit is complete.]
