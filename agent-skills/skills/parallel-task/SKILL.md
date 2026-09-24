---
name: parallel-task
description: Delegate independent side tasks or review completed work when explicitly requested.
---

Use the current conversation as context. Do not ask the user to restate the
main task.

## Choose a mode

- **Review:** independently assess completed work.
- **Light:** explicit request for a clear, simple, isolated task.
- **Medium:** the default for one bounded independent side task.
- **Full:** explicit request for a demanding task requiring multiple perspectives.

Read `references/independent-review.md` for `review` mode and
`references/delegation-modes.md` for `light`, `medium`, or `full` mode before
continuing. The selected reference defines the detailed workflow and output.

## Shared principles

For delegated work, use the smallest sufficient packet and keep the work
independent from the primary agent. When the task belongs to a durable plan,
carry the existing plan ID, parent phase, local objective, expected output,
dependencies, consumers, and completion condition in the packet. Do not create
a parallel subplan or repeat the parent plan's context. Invoke the plan
management workflow only if the delegation creates or changes plan structure
or relationships. Omit irrelevant context and the primary agent's verdict or
defence.

Keep changes isolated from the primary agent. Keep handoffs and findings in a
dedicated, run-scoped folder in the repository's designated non-canonical
location. These are temporary review artifacts: they are not product files,
canonical documentation, or part of the repository's deliverable, and must not
be committed.

After the primary agent and the user complete their joint review, the primary
agent must apply the findings they consider applicable and accepted to the
task, plan, or canonical files. Once that application is complete and no
decision remains pending, delete the entire run-scoped review folder. A
delegation is not complete until this cleanup is done and verified. If the user
explicitly asks to preserve the findings, or review/application is still
pending, keep the folder temporarily and report why; report any cleanup
failure rather than silently leaving the artifacts behind.

Monitor every delegated task. Treat silence while `running` as pending rather
than failure, and stop only for an explicit error, timeout, blocked state, or
user instruction. If delegation is unavailable, say so and do not pretend it
occurred.

For medium, full, and review, mark provisional findings as:

> PROVISIONAL — requires review by the primary agent and the user.

If any part involves online research require the delegated agent to invoke `$research`; do not substitute
generic web research.
