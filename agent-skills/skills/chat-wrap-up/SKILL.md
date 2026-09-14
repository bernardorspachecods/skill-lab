---
name: chat-wrap-up
description: Prepare repository context for seamless continuation after chat compaction. Invoke explicitly when ending or nearing compaction.
---

# Wrap up the chat

Use the conversation and repository state to prepare a seamless continuation.
Preserve what a fresh agent needs, not a generic progress summary.

## Reconcile and document

Read the repository's entrypoints and documentation ownership/routing guidance,
then inspect relevant documents, code, tests, diffs, and notes. Capture the
objective, status, changed artifacts, confirmed decisions, assumptions, open
questions, blockers, verification, and exact next step.

Route each material item to its proper place:

- link the existing source of truth;
- update its canonical owner when durable information is missing;
- record unresolved or provisional information explicitly as such;
- omit transient or redundant information.

Keep decisions separate from assumptions and open questions. Preserve the
user's intent and scope: do not infer approval, close unresolved decisions, or
promote provisional findings. Prefer the existing canonical owner and avoid
duplication; use the designated non-canonical location for any handoff note.

## Consistency gate

When closing a phase or decision, check the relevant documents, indexes, and
links together. No active or canonical document may contradict the closed
phase or current plan.

Historical material may preserve earlier decisions only when clearly marked as
reference or archive and excluded from active reading paths. If contradictions
remain, reconcile them or report the wrap-up as incomplete. Never silently
choose a source or claim a seamless handoff while the documentation conflicts.

## Verify the wrap-up

Check that:

- every material item is linked, documented, or explicitly unresolved;
- changed documents have the right owner, without avoidable duplication;
- links and reading paths resolve from the relevant entrypoint;
- the current phase and decisions are represented consistently across the
  relevant documentation;
- a fresh agent can identify the objective, current state, open decisions, and
  next step without this conversation.

Do not commit, clean the worktree, or implement new work. Report changed
documents, reused sources, unresolved items, and the next step.
