---
name: parallel-task
description: Plan and delegate independent side tasks in light, medium, or explicitly requested full multi-agent mode, with provisional findings and later review.
---

# Delegate an independent side task

Use the current conversation as context. Do not ask the user to restate the
main task.

## Choose a mode

- **Light:** only when the user explicitly requests `light` for a clear, simple,
  isolated task. The request authorizes launch; create no plan or findings file.
- **Medium:** the default. Delegate one bounded task with a plan, two approval
  gates, provisional findings, and later review.
- **Full:** only when the user explicitly requests `full`. Use for demanding
  tasks that need 2–4 independent perspectives, a second-pass agent, and joint
  evaluation. Never infer it from complexity alone.

If any part involves online research, use `$research` for that work in every
mode. Require the delegated agent to invoke `$research`; do not substitute
generic web research.

## Common planning, approval, and delegation rules

For medium and full, define the objective and how it supports the main task,
what remains with the primary agent, scope, non-goals, context, deliverable,
completion criteria, allowed changes, dependencies, risks, isolation, and
whether parallel work is useful. Ask one material question at a time.

Present the plan and wait for the first explicit `go` to prepare provisional
files; do not launch agents yet. Show their paths and wait for a second `go` to
launch. In full mode, the explicit `full` request is also required before
planning. A material change to scope or plan requires new approval.

Use the smallest sufficient packet: approved scope, applicable guidance, and
relevant code, tests, sources, or evidence. Omit irrelevant conversation and
the primary agent's verdict or defence. Instruct agents to read applicable
documentation themselves and remain independent. Use an isolated worktree or
branch for changes and avoid overlap with the primary agent. If delegation is
unavailable, say so and do not pretend it occurred.

Monitor every delegated task: confirm its state, treat silence while `running`
as pending rather than failure, and wait or poll for a terminal state. Stop
only for an explicit error, timeout, blocked state, or user instruction. Elapsed
time alone is never a reason to interrupt or terminate a running task.

## Findings contract

For medium and full Phase 1, each provisional findings file must contain:

- work performed and relevant documentation, code, tests, sources, and evidence;
- findings and conclusions, distinguishing evidence from interpretation;
- uncertainties, limitations, alternatives, and recommended next steps.

Mark every findings file:

> PROVISIONAL — requires review by the primary agent and the user.

Keep all handoff and findings files in the repository's designated
non-canonical location. Never treat them as definitive or update canonical
documentation from them automatically.

## Medium mode

After the first `go`, create the findings file with the objective, plan, initial
context, and status `awaiting_launch`. Show its path and wait for the second
`go`; only then launch one independent agent and change the status to
`in_progress`.

The primary agent and user review the findings, evidence, tests, and any diff
before adopting conclusions, merging changes, or updating canonical
documentation.

## Full mode

Run three phases. After the first `go`, prepare all files; after the second,
launch Phase 1. Keep the handoff and findings non-canonical.

### Phase 1 — independent perspectives

Create one shared handoff with the approved objective, scope, non-goals,
context, completion criteria, constraints, dependencies, risks, status, and
the chosen Phase 2 role. Also prepare one findings file per perspective and a
separate Phase 2 findings file with status `awaiting_phase2`. The coordinator
owns the handoff and agents must not overwrite it concurrently.

Launch 2–4 agents with the same handoff and distinct, meaningfully different
directions. They must not read one another's findings before this phase ends;
each owns and updates its reserved findings file.

### Phase 2 — independent second pass

Use the Phase 2 role recorded in the handoff:

- **Synthesis:** reconcile supported perspectives into a decision,
  recommendation, or integrated conclusion while preserving evidence,
  disagreements, limitations, alternatives, and uncertainty.
- **Completeness review:** for exhaustive extraction, knowledge-source building,
  or preservation tasks. Compare every Phase 1 finding with the objective and
  the named source/deliverable; verify coverage and identify omissions,
  distortions, duplicates, or unsupported transformations. Organise information
  only when no material knowledge is lost. Do not create a compressed synthesis.

Delegate a new independent agent for the chosen role. It reads the objective,
handoff, all Phase 1 findings, and evidence, then populates the prepared Phase
2 file. It must not delete or rewrite earlier findings, make canonical changes,
or silently resolve conflicts. No new `go` is needed: this is part of the
approved full plan and only updates a provisional file.

### Phase 3 — coordinator audit and joint evaluation

Before involving the user, the coordinator compares the Phase 2 output with
the handoff, every Phase 1 finding, and the evidence. Check that synthesis has
not dropped, distorted, or strengthened material content, or that a
completeness review has not missed knowledge from the source or deliverable. If
it has, return the file to the Phase 2 agent and repeat the audit; do not
silently edit or declare it ready.

The primary agent and user then evaluate the Phase 2 report and individual
findings together. Only after that may the primary agent adopt conclusions,
merge changes, or update canonical documentation.

## Report

Report the mode, delegated work, handoff and findings paths, learned results,
disagreements or limitations, and what remains unverified.
