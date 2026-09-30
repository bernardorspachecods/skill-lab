---
plan_id: LR-03.SP-01
kind: subplan
parent: LR-03
phase: S1
status: complete
depends_on: []
consumers: []
---

# LR-03.SP-01

## Objective

Improve the `$research` workflow's ability to orient to what the user is
actually trying to learn or decide before beginning web search.

## Scope

Review the current research brief step and define what the researcher should
identify about the user's goal, intended consumer or decision, relevant
context, and material ambiguity. Separate understanding the task from guessing
unstated requirements. Keep clarification focused on ambiguity that could
change the research direction or conclusion. Do not broaden this unit into
scoping query breadth, source selection, or output design.

Inputs: the user's first reported failure mode and the current
[`$research` skill](../../../../../agent-skills/skills/research/SKILL.md).

## Output

A targeted update to the canonical `$research` brief workflow and a concise
Outcome record describing the change and its verification. The implementation
agent must preserve the rest of the skill and coordinate through the primary
agent's handoff checkpoints.

## Sequence

1. **S1 — Define task orientation**
   - **Action:** Research the evidence needed for this design choice, then
     revise the brief guidance to surface goal, decision, consumer, context,
     and material uncertainty.
   - **Output:** The completed edit to the research brief section.
   - **Exit check:** The guidance directs the LLM to anchor the search on the
     user's intended outcome and clarifies only when the answer could change.

## Completion criteria

- The brief distinguishes a research topic from the user's goal or decision.
- The skill tells the researcher what context matters before searching.
- Clarification is limited to ambiguities that materially affect direction or
  conclusion; no speculative questionnaire is introduced.
- The update fits the current brief and does not duplicate scope or output
  instructions.
- The subplan Outcome records the changed section and the check performed.

## Outcome

Completed the research, implementation, and independent review gates. Updated
`Workflow → 1. Define the brief` to orient research around the user's actual
question or task and its decision or learning need; capture consumer and use
context only when it could affect relevance or interpretation; distinguish
supplied context from assumptions; and clarify only material ambiguity. The
research audit labels transfer limits and design judgment, and its S4 source
entry records the reviewed arXiv version and dates. Independent review passed
and verified the cited source descriptions, evidence-to-claim links, and S4
metadata. `git diff --check` passed; the root and SP-01 plan validator reported
no errors or warnings. No tests were run. No required corrections remain.
