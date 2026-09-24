---
name: grill-task
description: Clarify tasks and decisions into actionable plan briefs when scope, questions, decisions, or completion criteria are unclear; do not use for lightweight critique or durable plan maintenance.
---

# Clarify a task

Turn an unclear task or decision into a short, actionable plan brief. Use the
surrounding request and applicable repository context; do not ask the user to
repeat information that is already available.

## Workflow

1. State the overarching objective.
2. Resolve safe assumptions and inspect only context that could change the
   direction.
3. Ask one question at a time when an unresolved decision could cause rework;
   reassess after each answer.
4. Keep the scope useful: exclude unrelated ideas, preserve valuable future
   ideas separately, and challenge weak assumptions.
5. Decide whether the task is ready for execution, needs a short brief, or
   needs a durable hierarchical plan.

For decision questions, use:

```text
**Q<n> — <short title>**: <one decision question>

Recomendo: <the preferred answer and its main trade-off>
```

## Output

When clarification is complete, provide:

- the desired outcome and completion criteria;
- scope, non-goals, and immediate next steps;
- confirmed decisions, assumptions, risks, and open questions; and
- the boundary between what can proceed and what needs approval.

If a durable or hierarchical plan is required, hand this brief to
`$plan-management`. Do not define its metadata, plan-tree structure,
cross-plan dependencies, or durable document format here.

Do not implement changes during clarification. For a durable plan or any
material execution direction, wait for the user's explicit approval before
implementation.
