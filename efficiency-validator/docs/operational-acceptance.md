# Operational collection acceptance

Evidence date: 2026-09-26. This record accepts operational collection only;
comparative efficiency judgments remain the responsibility of phase 2.

## Real CLI evidence

Both acceptance runs used the installed Codex CLI 0.157.0, requested
`gpt-6-astra` with `low` reasoning, a fresh ephemeral session and a separate
workspace-write sandbox. The same task required adding cocoa at price 4,
adding a test and running the tests. The context variant adds only a
`CONTEXT.md` navigation map through the overlay mechanism.

| Evidence | Baseline | Context map |
| --- | --- | --- |
| Human-readable report | [baseline-fixed](../../evals/efficiency-operational/runs/baseline-fixed/derived/report.md) | [context-fixed](../../evals/efficiency-operational/runs/context-fixed/derived/report.md) |
| Manifest | [baseline manifest](../../evals/efficiency-operational/runs/baseline-fixed/manifest.json) | [context manifest](../../evals/efficiency-operational/runs/context-fixed/manifest.json) |
| Raw events | [baseline events](../../evals/efficiency-operational/runs/baseline-fixed/events.jsonl) | [context events](../../evals/efficiency-operational/runs/context-fixed/events.jsonl) |
| Changes | [baseline changes](../../evals/efficiency-operational/runs/baseline-fixed/changes.json) | [context changes](../../evals/efficiency-operational/runs/context-fixed/changes.json) |
| Checks | [baseline checks](../../evals/efficiency-operational/runs/baseline-fixed/checks.json) | [context checks](../../evals/efficiency-operational/runs/context-fixed/checks.json) |
| Agent task duration | 31.74 seconds | 27.15 seconds |
| Input/output tokens | 66,385 / 725 | 65,770 / 640 |
| Observed commands | 3 | 3 |
| Execution / evaluator checks | completed / pass | completed / pass |

Evaluator checks included both the project's unittest suite and an independent
assertion that `ITEMS["cocoa"] == 4` and `total(["tea", "cocoa"]) == 7`.
Original source files remained byte-identical to retained baseline input.
Both reports regenerated from the saved bundles without new model calls, and
their evidence integrity checks passed. There were no parser issues.
These numbers demonstrate capture; one pair is not evidence of a general
improvement. Cache conditions and ambient global skills were not controlled.

An earlier [failed launch](../../evals/efficiency-operational/runs/baseline-01/manifest.json)
preserves the enclosing sandbox's app-server permission error and its
diagnostic stream. Launching the collector outside that enclosing sandbox,
while retaining the Codex sandbox, resolved the launch issue. Another
[successful exploratory run](../../evals/efficiency-operational/runs/baseline-02/derived/report.md)
survived interruption of the supervising conversation and completed its bundle;
it was not relaunched or relabelled interrupted.

## Regression evidence

` .venv/bin/python -m pytest -q `: **96 passed**, including 11 operational tests.
The operational tests use a subprocess fixture at the CLI executable interface
for deterministic failure cases; real acceptance above uses the installed CLI.

Covered cases: preserving original inputs and binary/text work products,
created/deleted files, fresh workspaces, retained skill resources after source
edits, unavailable versus zero usage, timeout, explicit cancellation, abandoned
capture recovery, launch failure, overlapping annotated waits, offline
regeneration, corruption/added-file rejection, unsupported schemas, symlink
escape rejection, failed evaluator checks, refusal to overwrite a bundle, and
preventing partial progress messages from appearing as final answers.

All three active plans passed the strict plan validator with zero errors and
warnings. CLI help and source-preservation checks passed. This is not a claim
that global runtime isolation, exact file reads or interactive steering exist;
the [coverage table](operational-protocol.md#evidence-coverage) states the limits.

## Implementation decision

The existing parser is reused. The old capture/report route depends on
context-lab staging, an oracle and a read-only task; it remains available to
that consumer. The new operational CLI and bundle remove those dependencies
without silently changing legacy report semantics. The source/availability map
is maintained in the [operator protocol](operational-protocol.md#evidence-coverage).
