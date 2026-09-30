---
plan_id: LR-03.SP-03
kind: subplan
parent: LR-03
phase: S3
status: not_started
depends_on: [LR-03.SP-02#outcome]
consumers: []
---

# LR-03.SP-03

## Objective

Improve how `$research` chooses useful search paths and source types for a
bounded question, including how it identifies valuable sites and records.

## Scope

Review the current discovery workflow and strengthen its guidance for mapping
source types, accountable producers, domain terms, likely primary records,
independent corroboration, alternatives, and disconfirming paths. Clarify when
to search within known valuable sites or follow citations and records. Preserve
the distinction between source quality and whether a source supports the exact
claim. Do not assume a domain's design, ranking, or popularity establishes
quality. Respect the scope defined in
[LR-03.SP-02#outcome](../LR-03.SP-02/PLAN.md#outcome).

Inputs: the user's third reported failure mode, the current
[`$research` skill](../../../../agent-skills/skills/research/SKILL.md), and
the reconciled outcome of [LR-03.SP-02](../LR-03.SP-02/PLAN.md).

## Output

A targeted update to the search and source-selection guidance, with a concise
Outcome record of the change and verification.

## Sequence

1. **S3 — Map search paths and valuable sources**
   - **Action:** Research the relevant source-selection and web-search
     practices, then revise how the researcher maps sources, expands queries,
     and follows useful evidence paths.
   - **Output:** The completed edit to the discovery workflow.
   - **Exit check:** The search plan identifies source roles and paths for the
     scoped question and includes a way to find contrary or corrective evidence.

## Completion criteria

- Source discovery begins from the question and likely source roles, not a
  generic list of prestigious sites.
- Query expansion is controlled and terms have a traceable reason for use.
- Search paths include relevant primary or accountable records and
  disconfirmation when suitable.
- The skill distinguishes discovery leads from evidence and source quality
  from claim support.
- The subplan Outcome records the changed section and the check performed.

## Outcome

[Record completion, verification, and material differences when the unit is complete.]
