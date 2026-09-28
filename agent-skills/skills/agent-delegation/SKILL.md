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
to repeat information already available.

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

- Keep every assignment within the user's request or the enabled plan scope.
  A clear request to delegate or a plan's execution setting authorizes that
  work; do not create an extra approval step for the same scope. If delegation
  is only a suggestion, ask before launching agents.
- Use the smallest sufficient assignment and context. State the question or
  objective, expected output, relevant inputs, constraints, and the boundary
  of the agent's authority.
- Lightweight delegation is the default. Use multiple agents, extra
  coordination artifacts, or staged handoffs only when the task needs
  independent perspectives, distinct ownership, durable coordination, or
  another concrete control.
- Preserve independence when independent perspectives are requested. Give
  agents the same objective, criteria, and relevant context; assign distinct
  lenses only when useful. Keep their initial assignments and findings hidden
  from one another until each submits an independent first response. Share
  findings afterward when synthesis or coordination requires it. Do not apply
  this isolation to implementation work that depends on collaboration.
- Keep parallel work genuinely independent. Assign non-overlapping write
  boundaries when agents edit files; coordinate shared files through the
  primary agent.
- Delegation does not create a shared-model entity or a new identity for the
  work. The delegated agent continues the same plan unit and artifacts. Do not
  create `DEL-*` IDs or maintain an agent history in the artifact graph.
- Monitor delegated work to its handoff. Treat silence from a running agent as
  pending; stop for an explicit error, timeout, blocked state, or user
  instruction. If delegation is unavailable, say so; do not imply it occurred.
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

For a durable plan, `execution.review` and `execution.delegation` are
independent booleans. `review: true` requires a review gate for the applicable
unit; `review: false` disables that gate. `delegation: true` permits bounded
implementation or advisory work in the plan's scope to be assigned to agents;
`delegation: false` keeps that work with the primary executor. A review may
still use an independent reviewer when `review` is enabled, regardless of the
implementation-delegation setting.

Subplan exceptions use the same boolean values and override only the named
dimension. If a request conflicts with the plan's setting or scope, stop and
reconcile the plan before proceeding. These settings govern durable plan work;
an explicit standalone user request to delegate is sufficient authorization
for that assignment.

## Completion

Finish when each assignment has returned its specified output, the primary
agent has checked and reconciled the result, and any required review or
integration gate is satisfied. Do not report the delegated work as complete
while an agent is still running or a required handoff is unresolved.
