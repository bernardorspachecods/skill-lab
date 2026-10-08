---
name: chat-wrap-up
description: Preserve repository context when ending or nearing chat compaction.
---

Use the conversation and repository state to prepare a seamless continuation,
preserving what a fresh agent needs rather than a generic progress summary.
Ending a chat does not by itself close a phase or decision. The normal handoff
is a short response linking to existing canonical documents; do not create a
handoff file, working note, plan, or duplicate summary just to preserve chat
context.

## Capture

Read the applicable repository entrypoints and context guidance. Inspect only
relevant documents, code, tests, diffs, plans, and notes. Capture:

- objective, scope, current phase, and status;
- changed artifacts and verification;
- confirmed decisions; assumptions, open questions, and blockers;
- the exact next step.

## Reconcile

Find the canonical owner before deciding where anything belongs. Update an
existing plan or document, using its established structure, only when durable
information is missing or stale:

- keep plan objective, output, sequence, dependencies, consumers, and status in
  the canonical plan rather than duplicating them;
- record unresolved or provisional information explicitly as such;
- keep transient chat-resume details and the short next-chat prompt in the
  response; do not create or reopen a plan merely for that prompt;
- invoke plan-management only when a structural change, new relationship, or
  coordination problem requires it.

Keep decisions separate from assumptions and open questions. Preserve the
user's intent and scope: do not infer approval, close unresolved decisions, or
promote provisional findings. If there is a genuine documentation gap, no clear
owner, or a structure problem, do not create or reorganize files: consult
`$context-architecture` only on this branch, explain the gap and options to the
user, and wait for direction. Never invent a non-canonical handoff location.

## Verify

Before reporting, check the relevant active documents, indexes, and links
together: reconcile contradictions or report them as incomplete, confirm that
changed documents have the right owner and no avoidable duplication, and verify
that links and reading paths resolve from the relevant entrypoint.

Do not commit, clean the worktree, or implement new work. Report changed
documents, reused sources, unresolved items, and the next step. If no canonical
document needs changing, say so and provide a short, copyable prompt pointing
to the canonical sources without repeating their contents.

## Runtime metadata

This skill's invocation and display metadata is in [agents/openai.yaml](agents/openai.yaml).
