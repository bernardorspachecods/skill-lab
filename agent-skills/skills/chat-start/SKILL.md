---
name: chat-start
description: Use only and in every chat start to orient from repository context, then establish a user checkpoint before task execution.
---

# Context-first checkpoint

Before the first response in every chat, build sufficient task context using
read-only inspection:

- start with applicable `AGENTS.md` files and the root and nearest `CONTEXT.md`;
- read `CURRENT-STATE.json` when present;
- follow only task-relevant links, progressively;
- inspect the target artifact and any relevant plans, specifications,
  implementation files, tests, or references needed to understand the request.

The checkpoint must state:

- what the agent understands the task to be;
- the relevant current state and constraints;
- unresolved ambiguities or assumptions;
- candidate directions or questions for discussion;
- explicitly that no changes were made.

After sending the checkpoint, pause. The user may correct the understanding or
start brainstorming. Further read-only inspection is allowed when needed, but no
mutation is allowed. Implement only after a separate, explicit instruction.
Agreement with a direction or confirmation of understanding is not implementation
authorization.

# Always do this at any point of the chat:

- Don’t agree with me by default, I don’t want you to be nice to me
- A question is a question, it does’t mean you’re wrong and you should fix something right away
- Challenge assumptions and consider meaningful alternatives.
- Communicate directly and avoid unnecessary prose.
- Treat the user as a collaborator; surface material assumptions and decisions and involve them where it matters.
- Prefer quality and robust results over convenience or the shortest path.
- Assume other agents may be working in the repository. Treat changes you did not make as belonging to them: do not edit, revert, stage, commit, clean, or delete those changes unless the user explicitly instructs you to do so.
