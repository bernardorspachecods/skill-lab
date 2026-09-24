---
name: chat-start
description: Use only and in every chat start to orient with minimal relevant context.
---

At the start of every chat, read the applicable `AGENTS.md` files and the
minimum relevant context. Use the root `CONTEXT.md` as the canonical repository
orientation and the nearest `CONTEXT.md` as the map for the area being entered.
Follow only task-relevant links; consult the parent map when the boundary is
unclear. If present, read `CURRENT-STATE.json` after the applicable `CONTEXT.md`. 

Use progressive retrieval: when a document has a navigation map, read its
purpose and map first, then load only the relevant section and dependencies.

`README.md` is for public GitHub presentation only, never for internal
repository context.

If the user's request is 100% specific and obvious, read the relevant documents
and proceed. Otherwise (open-ended request or no request), only load context:
briefly state the topic, current state, key decisions, and open questions, then
stop and wait for guidance. Never infer a task from documents, TODOs, or open
questions; only the user defines the task.

Assume other agents may be working in the repository. Treat changes you did not
make as belonging to them: do not edit, revert, stage, commit, clean, or delete
those changes unless the user explicitly instructs you to do so.

Work with:

- Be honest about what is true, uncertain, or wrong.
- Challenge assumptions and consider meaningful alternatives.
- Communicate directly and avoid unnecessary process.
- Treat the user as a collaborator; surface material assumptions and decisions and involve them where it matters.
- Prefer quality and robust results over convenience or the shortest path.
