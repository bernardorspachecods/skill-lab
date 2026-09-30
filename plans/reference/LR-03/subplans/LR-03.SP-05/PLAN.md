---
plan_id: LR-03.SP-05
kind: subplan
parent: LR-03
phase: S5
status: complete
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
[`$research` skill](../../../../../agent-skills/skills/research/SKILL.md), and
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

Completed the research, implementation, and independent review gates.
`Research → Output` now shapes answers to the consumer's intended use, leads
with direct findings, keeps material qualifications and source paths
accessible, and calibrates confidence without requiring one template. Detailed
evidence records remain separately accessible when needed, and disposable
search records stay separate. Added a placeholder-only example for topic- or
situation-grouped best practices. Independent review passed and verified the
audit's claims and final DeepResearch Bench publication metadata. The research
skill package is valid; the full catalog has unrelated existing issues. The
root and SP-05 plan validator reported no errors or warnings, and `git diff
--check` passed. No tests were run. No required corrections remain.
