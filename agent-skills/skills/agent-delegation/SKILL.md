---
name: agent-delegation
description: >
  Delegate bounded implementation, review, or advisory work to one or more
  agents. Use when the user requests delegation or a plan enables it; use
  research for evidence gathering that needs its own research workflow.
---

# Agent delegation

Delegate a clearly bounded assignment to one or more agents and coordinate the
handoff. Use the current conversation and relevant task brief as context; do
not ask the user to repeat information already available. If delegation is
unavailable, say so; do not imply it occurred.

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
  boundaries when agents edit files.
- Delegation does not create a new identity for the work. The delegated agent
  continues the canonical task and its agreed scope.
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

## Durable plan coordination

For durable plans, `$plan-management` owns the execution contract, artifact
scaffolding, and handoff gates. The coordinator reads the durable plan contract
reference under `$plan-management` when creating or coordinating a durable
plan. Assigned agents work from the coordinator's brief and the artifacts named
there; they do not need to load the plan contract to carry out a bounded
assignment. A standalone user request to delegate authorizes that assignment
without a durable plan.

## Completion

Finish when each assignment has returned its specified output, the primary
agent has checked and reconciled the result, and any required review or
integration gate is satisfied. Do not report the delegated work as complete
while an agent is still running or a required handoff is unresolved.
