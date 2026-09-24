# Delegation modes

## Light mode

Use only when the user explicitly requests `light` for a clear, simple,
isolated task. The request authorizes launch. Create no execution plan,
findings file, or review packet.

## Medium mode

Medium is the default for an independent side task.

Before launch, apply the shared principles from the main skill and define how
the side task supports the main task and what remains with the primary agent.

Present the plan and wait for the first explicit `go`; do not launch yet. After
that approval, create the run-scoped temporary execution plan, one reserved
findings file, and `review.md` according to the plan-management reference. Set
the execution-plan status to `awaiting_launch`. Show the packet path and wait
for a second explicit `go`; only then launch one independent agent and change
the plan status to `in_progress`.

The agent writes only to its reserved findings file. The primary agent audits
the findings, evidence, tests, and any diff, then the primary agent and user
review them together before adopting conclusions, merging changes, or updating
canonical documentation. The primary agent records the joint decision in
`review.md`. A material change to scope or plan requires new approval.

## Full mode

Use only when the user explicitly requests `full`. It is for demanding tasks
that need 2–4 independent perspectives, a second-pass agent, and joint
evaluation. Run three phases. After the first `go`, prepare all files; after
the second, launch Phase 1. Keep the execution plan, findings, and review
non-canonical.

### Phase 1 — independent perspectives

Create the temporary execution plan with the approved task definition,
constraints, status, and chosen Phase 2 role. Also prepare
one reserved findings file per perspective, a separate Phase 2 findings file
with status `awaiting_phase2`, and `review.md`. The coordinator owns the plan
and review file; agents must not overwrite them concurrently.

Launch 2–4 agents with the same execution plan and distinct, meaningfully different
directions. They must not read one another's findings before this phase ends;
each owns and updates its reserved findings file.

### Phase 2 — independent second pass

Use the Phase 2 role recorded in the execution plan:

- **Synthesis:** reconcile supported perspectives into a decision,
  recommendation, or integrated conclusion while preserving evidence,
  disagreements, limitations, alternatives, and uncertainty.
- **Completeness review:** for exhaustive extraction, knowledge-source building,
  or preservation tasks. Compare every Phase 1 finding with the objective and
  the named source/deliverable; verify coverage and identify omissions,
  distortions, duplicates, or unsupported transformations. Organise information
  only when no material knowledge is lost. Do not create a compressed synthesis.

Delegate a new independent agent for the chosen role. It reads the objective,
execution plan, all Phase 1 findings, and evidence, then populates the prepared
Phase 2 findings file. It must not delete or rewrite earlier findings, edit the
execution plan or review file, make canonical changes, or silently resolve
conflicts. No new `go` is needed: this is part of the approved full plan and
only updates its reserved findings file.

### Phase 3 — coordinator audit and joint evaluation

Before involving the user, compare the Phase 2 output with the execution plan,
every Phase 1 finding, and the evidence. Check that synthesis has not dropped,
distorted, or strengthened material content, or that a completeness review has
not missed knowledge from the source or deliverable. If it has, return the file
to the Phase 2 agent and repeat the audit; do not silently edit or declare it
ready.

The primary agent and user then evaluate the Phase 2 report and individual
findings together. The primary agent records the joint decision in `review.md`.
Only after that may the primary agent adopt conclusions, merge changes, or
update canonical documentation.
