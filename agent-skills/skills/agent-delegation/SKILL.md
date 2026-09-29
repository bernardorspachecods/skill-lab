---
name: agent-delegation
description: >
  Delegate bounded implementation, review, or advisory work to one or more
  agents. Use when the user requests delegation or a plan enables it; use
  research for evidence gathering that needs its own research workflow.
---

# Agent delegation

Delegate a clearly bounded assignment to one or more agents and coordinate the
handoff. Use the current conversation and plan as context; do not ask the user
to repeat information already available. If delegation is unavailable, say so; do not imply it occurred.

## Choose the assignment

- **Advice:** ask an agent a focused question or request an independent opinion.
  Keep this lightweight: send only the context needed to answer and return the
  response with its uncertainty. Do not create a packet or persistent artifact
  unless the work itself needs one.
- **Implementation:** when an agent is expected to change files or produce an
  implementation, read [implementation delegation](references/implementation-delegation.md).
- **Review:** when an agent is expected to assess completed work or a stable
  target, read [review delegation](references/review-delegation.md).

Review the target only after its executor has declared the work complete and
the coordinator has reconciled the result. Do not allow implementation and
review to modify the same target at the same time.

## Shared delegation rules


- Use the smallest sufficient assignment and context. 
- Preserve independence when independent perspectives are requested.
- Keep parallel work genuinely independent. Assign non-overlapping write
  boundaries when agents edit files
- Delegation does not create a shared-model entity or a new identity for the
  work. The delegated agent continues the same plan unit and artifacts. Do not
  create `DEL-*` IDs or maintain an agent history in the artifact graph.
- Monitor delegated work to its handoff. Treat silence from a running agent as
  pending; stop for an explicit error, timeout, blocked state, or user
  instruction. 
- The primary agent remains responsible for checking the handoff against the
  assignment, evidence, and applicable completion criteria. Reconcile results
  into the canonical task or plan within the authorized scope. Report
  unresolved conflicts, unsupported claims, and incomplete work clearly.
- If a plan enables research, or the user explicitly requests `$research`, the
  delegated agent follows that skill for evidence gathering. In a simple task
  without a plan, propose research when a material evidence gap appears and
  wait for the user's explicit invocation; do not substitute an unstructured
  search for the research workflow.

## Durable plan settings

For a durable plan, `execution.research`, `execution.review`, and
`execution.delegation` are independent settings. `research` selects whether
and at what level to conduct research; when enabled, assign the research work
to a researcher. `review: true` requires a review gate for the applicable
unit; `review: false` disables that gate. Assign enabled review to an
independent reviewer, whether or not implementation delegation is enabled.
`delegation: true` assigns bounded implementation work to agents;
`delegation: false` keeps implementation with the primary executor.

For durable plans with subplans, the primary agent coordinates the plan with
the user. If delegation is enabled, the primary agent does not implement the
subplans; assign each subplan's implementation to an agent. For each subplan,
assign enabled research, implementation, and review stages as separate
sequential handoffs, each to a distinct agent. Review follows completed and
reconciled implementation, and the reviewer must be independent of the
implementer. When implementation delegation is disabled, the primary agent
implements the subplans; enabled research and review are still assigned to
agents.

The root plan's `execution.user_checkpoints` controls when the coordinator
pauses for the user's file review:

- `each_handoff`: after each agent returns, check and reconcile its handoff,
  show the files or output to the user, and wait for approval before spawning
  or starting the next agent assignment, advancing the plan unit, or making its
  output available downstream.
- `each_subplan`: continue through the enabled stages for the current subplan
  (or the root unit when there are no subplans), then show the reconciled unit
  to the user and wait for approval before starting the next subplan or making
  its output available downstream.
- `plan_completion`: continue through the approved plan, then show the
  reconciled result and wait for the user's review and approval. Pause earlier
  only for a blocker, an unmet requirement, or a decision that changes the
  approved scope.

The user agrees to the checkpoint cadence before plan scaffolding. The
coordinator must follow that cadence; the plan's approved execution contract
authorizes its assignments, but does not waive its required user checkpoints.
For a root plan without subplans, the user decides whether implementation is
delegated. Research and review remain independently selectable workflows.

Subplan exceptions override only the named dimension, using values defined by
the dimension's owner. A subplan may override `user_checkpoints` using one of
the values above. If a request conflicts with the plan's setting or scope, stop
and reconcile the plan before proceeding. These settings govern durable plan
work; an explicit standalone user request to delegate is sufficient
authorization for that assignment.

## Completion

Finish when each assignment has returned its specified output, the primary
agent has checked and reconciled the result, and any required review or
integration gate is satisfied. Do not report the delegated work as complete
while an agent is still running or a required handoff is unresolved.
