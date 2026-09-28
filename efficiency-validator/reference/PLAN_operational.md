---
plan_id: O1
kind: subplan
parent: O0
phase: 1
status: complete
depends_on: []
consumers: [operator, docs/operational-protocol.md, run bundles]
---

# Phase 1 — Operational collection

## Objective

Make a real task runnable through the evaluator and produce a factual,
inspectable record. This is the first delivery of the [root plan](PLAN_operational-evaluator.md).

## Scope

Capture configuration, raw runtime events, tool calls and exposed results,
search/read evidence, reported tokens, timing, errors, human interventions,
workspace changes, verification results and the final response. Controlled
starting conditions, execution limits and offline report regeneration are
required operational capabilities.
Provide an explicit availability assessment for each field. Comparative
judgments, relevance scoring and statistical analysis belong to phase 2.

## Output

A repeatable operator command and local run bundle containing a manifest,
versioned raw evidence, normalized timeline, preserved inputs and work products,
final result and human-readable report.
The bundle is the input to later analysis and can be inspected on its own.

## Sequence

1. **S1 — Establish what currently works**
   - **Action:** Inspect existing entrypoints, schemas and tests; run a minimal
     real task that searches for and reads a known file. Establish which events
     the installed runtime exposes. Record missing capabilities and reuse
     decisions in this plan as execution findings.
   - **Output:** Real probe bundle and a source/availability map for required data.
   - **Exit check:** Each requested field has a demonstrated source or an
     explicit limitation. Fixture results do not substitute for the real probe.
2. **S2 — Make launching and provenance reliable**
   - **Action:** Repair the existing workflow to accept a target, task and
     identifiable variant without requiring an oracle. Preserve the prompt,
     initial target state (including relevant uncommitted/untracked inputs),
     and selected context/skill files and their required local resources using
     immutable copies or retrievable pinned versions with integrity hashes.
     Variant names and hashes alone are insufficient for reconstruction.
     Record actual launch settings, requested/resolved model and runtime versions
     when exposed, run identifier and manifest schema version. Distinguish
     configured resources from resources demonstrably consumed by the runtime;
     identify ambient configuration that cannot be isolated or established.
   - **Output:** Reconstructable input bundle, manifest and launch command.
   - **Exit check:** Two configurations produce distinct bundles without
     overwriting evidence; failed launches preserve a useful failure record.
     Editing the original skill/context after capture cannot change the retained
     run inputs; a missing resource or unresolved setting is explicit.
3. **S3 — Control starting conditions and execution limits**
   - **Action:** Start a fresh session and isolated workspace from the recorded
     inputs by default, preserving the user's working tree. Record any deliberate
     session reuse, setup/dependency state and observable cache conditions;
     unknown provider cache state must not be described as cold. Keep setup time
     separate from measured task time. Provide a configurable wall-clock limit
     and cancellation; expose token or monetary limits only where they can be
     enforced, stating scope, granularity and possible overshoot. Persist events
     incrementally and finalize partial bundles after cancellation or failure;
     account for launched work that could not be stopped.
   - **Output:** Controlled launch lifecycle with terminal reason and partial
     evidence recovery.
   - **Exit check:** Consecutive runs do not inherit workspace changes or session
     history unintentionally. Timeout and cancellation retain received evidence
     and terminate owned work or report incomplete cleanup. Unsupported budget
     limits are rejected or explicitly unavailable, never promised as enforced.
4. **S4 — Retain operational evidence and work products**
   - **Action:** Preserve raw events and normalize tool inputs/results, ordering,
     timestamps, result status, final response and usage fields. Separate run
     duration from tool duration; record cached/input/output tokens according to
     their source semantics. Keep unknown events and indicate truncation or
     missing correlation. Expose file paths and requested spans only at the
     confidence supported by the source; do not infer complete reads from commands.
     Record user corrections, hints and approval requests/responses with event
     source and timestamps; separate waiting for the user from total elapsed time
     where observable, without subtracting overlapping waits twice. Support an
     explicit operator annotation for interventions outside the captured channel;
     unavailable observation must not be reported as zero interventions. Retain
     the before/after workspace difference, including created/deleted files and
     binary artifacts where applicable, plus verification commands, outputs and
     exit status. Distinguish agent-run checks from evaluator-run checks.
   - **Output:** Evidence-linked timeline, intervention record, work products and
     usage/timing summary.
   - **Exit check:** The known search/read task can be followed through captured
     calls and exposed outputs. Missing tool evidence is explicitly reported;
     phase acceptance requires a useful observable tool trajectory, not just a
     final answer and token total.
     A modifying task preserves its resulting changes and actual check outcomes;
     tests not run cannot appear as passing.
5. **S5 — Produce and regenerate the factual report**
   - **Action:** Connect existing reporting to the bundle. Show configuration,
     outcome, activity, usage, timing and coverage, with links to raw evidence.
     Separate execution failure, collection failure and optional audit failure.
     Include starting conditions, interventions/waits, termination reason and
     work products. Version the bundle/event formats and record collector,
     normalizer and report-generator versions. Generate reports offline from
     retained evidence into separate derived artifacts without modifying the raw
     capture. Reject unsupported schema versions with an actionable explanation.
   - **Output:** Readable per-run report plus machine-readable data.
   - **Exit check:** A user can inspect what happened and its recorded costs
     without an oracle, paired run or exact-read sidecar. Missing metrics cannot
     silently appear as zero or erase independent valid measurements.
     Regeneration succeeds without a model call, network access or the original
     workspace; retained raw evidence stays unchanged.
6. **S6 — Verify repeatable operation**
   - **Action:** Run a small real task under two identified configurations;
     include a task that modifies a file and runs a check. Verify fresh-start
     isolation, input retention after source changes, intervention/wait recording,
     timeout/cancellation, partial-output recovery and offline regeneration with
     targeted checks. Document the supported command, prerequisites, evidence retention
     and access restrictions. Preserve existing host authentication; do not copy
     credentials into alternate runtimes. Do not retain secrets in manifests.
   - **Output:** Acceptance bundles and updated operator protocol.
   - **Exit check:** A fresh invocation produces its own consultable report;
     failures remain diagnosable. Relevant regression checks pass and any
     unsupported capability is documented with its effect on evidence.

## Completion criteria

- A real CLI task and a second configured run yield separately identifiable
  bundles and factual reports through a documented workflow.
- Raw exposed tool activity is retained and navigable; normalization does not
  discard unknown events or conceal truncation.
- Tokens and timing are measured where supported, with explicit unavailable
  fields and no unsupported per-call or per-file attribution.
- Capture is usable without evaluator ground truth or privileged OS tracing.
- Retained configuration and inputs identify the actual experiment and survive
  later edits; unresolved ambient inputs are explicit reproducibility limits.
- Fresh starts isolate session/workspace state; cache and setup conditions are
  recorded without unsupported claims of full environmental reproducibility.
- Changes, check results and human interventions are inspectable, with explicit
  coverage limits and distinct total/task/setup/user-wait timing where observable.
- Limits and cancellation preserve useful partial evidence and report the
  termination reason; offline reporting requires no repeated agent execution.
- Success is backed by actual artifacts; historical completion claims and
  synthetic-only tests cannot satisfy acceptance.

## Execution findings

- S1 established useful command inputs/results, lifecycle events and token
  usage from the installed CLI. Global skills remain visible even with user
  configuration ignored; that is an explicit reproducibility limit.
- S2–S5 are implemented by `scripts/operational.py`, using the existing event
  parser with a separate operational bundle and offline reporter. The legacy
  context-lab route remains intact for its current consumer.
- S6 evidence, regression results and retained real runs are published in
  [the acceptance record](docs/operational-acceptance.md). The supported command,
  source/availability map and limits are in
  [the operator protocol](docs/operational-protocol.md).
