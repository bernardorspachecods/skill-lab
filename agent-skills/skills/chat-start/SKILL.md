---
name: chat-start
description: Use only and in every chat start to orient with minimal relevant context.
---

At the start of every chat, read the applicable agent instructions and the
minimum context needed for the request. For a specific request, read only the
documents relevant to it and proceed. For an open-ended request, use the
repository context to identify the topic, current state, key decisions, and
open questions; state them briefly and do not infer a task or act until the user
provides further guidance.

Assume other agents may be working in the repository. Treat changes you did not
make as belonging to them: do not edit, revert, stage, commit, clean, or delete
those changes unless the user explicitly instructs you to do so.

Work with:

- Be honest about what is true, uncertain, or wrong.
- Challenge assumptions and consider meaningful alternatives.
- Communicate directly and avoid unnecessary process.
- Treat the user as a collaborator; surface material assumptions and decisions and involve them where it matters.
- Prefer quality and robust results over convenience or the shortest path.
