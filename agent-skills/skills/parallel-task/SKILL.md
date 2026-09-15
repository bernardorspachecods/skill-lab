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

For delegated work, use the smallest sufficient packet, keep the work
independent from the primary agent, and make the objective, scope, deliverable,
and completion condition explicit. Omit irrelevant context and the primary
agent's verdict or defence.

Keep changes isolated from the primary agent. Keep handoffs and findings in the
repository's designated non-canonical location, and do not merge conclusions
or update canonical documentation until the provisional result has been
reviewed.

Monitor every delegated task. Treat silence while `running` as pending rather
than failure, and stop only for an explicit error, timeout, blocked state, or
user instruction. If delegation is unavailable, say so and do not pretend it
occurred.

For medium, full, and review, mark provisional findings as:

> PROVISIONAL — requires review by the primary agent and the user.

If any part involves online research, use `$research` for that work in every
mode. Require the delegated agent to invoke `$research`; do not substitute
generic web research.
