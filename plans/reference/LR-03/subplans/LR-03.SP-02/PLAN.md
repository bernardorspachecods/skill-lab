---
plan_id: LR-03.SP-02
kind: subplan
parent: LR-03
phase: S2
status: complete
depends_on: [LR-03.SP-01#outcome]
consumers: []
---

# LR-03.SP-02

## Objective

Make `$research` convert an oriented goal into a bounded, prioritized research
scope that protects evidence quality from unnecessary breadth.

## Scope

Specify how to choose subquestions and material claims, define in-scope and
out-of-scope boundaries, set relevant time or geography constraints, and
recognize when enough evidence has been gathered. Keep the scope proportionate
to the stakes and consumer need. Build on the task orientation completed in
[LR-03.SP-01#outcome](../LR-03.SP-01/PLAN.md#outcome). Do not redesign the
source hierarchy or final answer structure here.

Inputs: the user's second reported failure mode, the current
[`$research` skill](../../../../../agent-skills/skills/research/SKILL.md), and
the reconciled outcome of [LR-03.SP-01](../LR-03.SP-01/PLAN.md).

## Output

A targeted update to the `$research` scope and stop-criteria guidance, with a
concise Outcome record of the change and verification.

## Sequence

1. **S2 — Bound and prioritize the question**
   - **Action:** Research and define practical scope decisions that link the
     user's goal to a manageable set of questions, claims, evidence needs, and
     stop conditions.
   - **Output:** The completed edit to the brief and discovery workflow.
   - **Exit check:** A downstream search can tell what matters, what is
     excluded, and when further searching is unlikely to add material value.

## Completion criteria

- The guidance turns the user's goal into bounded and prioritized questions.
- Scope includes only constraints that can affect the answer, such as dates,
  geography, or decision stakes.
- Completion and stop conditions reduce unproductive breadth without implying
  complete recall of the open web.
- The update uses the S1 orientation and leaves source assessment and output
  formatting to their own stages.
- The subplan Outcome records the changed section and the check performed.

## Outcome

Completed the research, implementation, and independent review gates. The
brief and discovery workflow now turn the oriented goal into prioritized
material questions, justify scope constraints and exclusions by their effect
on the answer, set evidence expectations by importance and stakes, and define
task-sensitive evidence adequacy and stopping criteria without implying
complete open-web recall. Independent review passed and verified the audit's
source descriptions and evidence-to-claim links within their stated limits.
`git diff --check` passed, and the root and SP-02 plan validator reported no
errors or warnings. No tests were run. No required corrections remain.
