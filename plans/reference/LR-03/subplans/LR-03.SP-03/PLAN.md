---
plan_id: LR-03.SP-03
kind: subplan
parent: LR-03
phase: S3
status: complete
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
[`$research` skill](../../../../../agent-skills/skills/research/SKILL.md), and
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

Completed the research, implementation, and independent review gates. The
discovery workflow now maps source roles and records from prioritized
questions, keeps query expansions small and traceable, follows citations and
records when useful, and searches for disconfirmation when it could change the
answer. Search results remain discovery leads until provenance and exact claim
support are checked. Existing source-quality and source-role guidance is
preserved. Independent review passed and verified the audit's source
descriptions and evidence-to-claim links within their stated limits. `git diff
--check` passed, and the root and SP-03 plan validator reported no errors or
warnings. No tests were run. No required corrections remain.
