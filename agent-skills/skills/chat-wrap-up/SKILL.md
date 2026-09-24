---
name: chat-wrap-up
description: Preserve repository context when ending or nearing chat compaction.
---

Use the conversation and repository state to prepare a seamless continuation.
Preserve what a fresh agent needs, not a generic progress summary.

Ending a chat does not by itself close a phase or decision.

## Capture

Read the applicable repository entrypoints and context guidance. Inspect only
the relevant documents, code, tests, diffs, plans, and notes. Capture:

- objective and scope;
- current phase and status;
- changed artifacts and verification;
- confirmed decisions;
- assumptions, open questions, and blockers;
- the exact next step.

## Reconcile

Route each durable item to its canonical owner. For an active plan tree, update
the existing canonical plan using its established structure:

- link the existing source of truth;
- update its canonical owner when durable information is missing;
- keep plan objective, output, sequence, dependencies, consumers, and status in
  the canonical plan rather than duplicating them in handoff notes;
- invoke the plan-management workflow only when the handoff reveals a
  structural change, new relationship, or coordination problem;
- record unresolved or provisional information explicitly as such;
- omit transient or redundant information.

Keep decisions separate from assumptions and open questions. Preserve the
user's intent and scope: do not infer approval, close unresolved decisions, or
promote provisional findings. Use the designated non-canonical location for
handoff notes. Do not redesign the context structure or change document
ownership; use `$context-architecture` when that work is required.

## Verify

Before reporting, check the relevant active documents, indexes, and links
together:

- contradictions are reconciled or reported as incomplete;
- changed documents have the right owner and no avoidable duplication;
- links and reading paths resolve from the relevant entrypoint;
- a fresh agent can identify the objective, current state, open decisions, and
  next step without this conversation.

Do not commit, clean the worktree, or implement new work. Report changed
documents, reused sources, unresolved items, and the next step.
