---
name: grill-task
description: Clarify tasks and decisions into actionable plans.
---

# Plan and stress-test a task

1. Every task and plan must have a clear overarching objective that remains visible throughout planning and execution.
2. Use the surrounding request as context; do not ask the user to restate it. When working in a repository, read all applicable guidance, then inspect only the documentation and code needed to define the task.
3. Treat assumptions and questions as costs: investigate assumptions that could cause rework, and resolve safe, reversible details without asking. Ask only when the cost of being wrong is higher than the cost of interrupting the user.
4. Ask one question at a time. After each answer, reassess whether enough information is available to define the plan. Continue asking questions when necessary; do not impose a fixed limit.
5. Use the answers to decide whether the request needs a short plan or deeper exploration of a material ambiguity, trade-off, or decision.

## Keep scope useful

When an idea is outside the objective:

1. Say so clearly.
2. Let the user decide whether to include it.
3. If it is excluded but worth preserving, record it in the repository's designated future-ideas space.

## Ask questions

For decision questions, use this format:

  ```text
  **Q<n> — <short title>**: <one decision question>

  Recomendo: <the preferred answer and its main trade-off>
  ```

When exploring deeply:

- challenge weak assumptions and disagree when there is a grounded reason;
- propose alternatives and concrete scenarios when they clarify the decision;
- keep the objective and scope visible;
- stop exploring once the material decisions are clear; do not reopen settled decisions.

## Short plan

After the necessary clarifying questions are answered, communicate a concise plan containing:

- the desired outcome and completion criteria;
- the scope and immediate next steps;
- only the assumptions, risks, or missing context that could affect execution.

State the assumptions and stop after the plan. Keep it in the conversation, do not update durable project documentation, and do not execute the task during this flow.

## Documented plan

Use this flow when the task requires a durable plan or contains a material ambiguity, trade-off, or decision that needs deeper exploration.

- Use the repository's designated planning or decision document when one exists.
- If there is no suitable owner, keep the plan in the conversation and ask before creating a new durable document.
- Keep the working plan, alternatives, future ideas, and open questions separate from canonical documents during exploration.
- When the plan is confirmed and the user gives an explicit `go`, update the existing canonical owner immediately before implementation. Do not create a new source of truth.
- If no durable plan is needed, use the short flow instead.

Do not implement changes during planning or exploration. After the explicit `go`, the planning phase is complete.

## Finish

Finish when the objective, scope, completion criteria, next steps, and any material decisions are clear. Present the plan first, then relevant unchosen possibilities and future ideas. Wait for the user's explicit `go` before implementation.
