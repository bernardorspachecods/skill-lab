---
plan_id: R8
kind: subplan
parent: R0
phase: 8
status: not_started
depends_on: [R7]
consumers: [R9, efficiency-validator/reports]
---

# R8 — Real exact-read capture

> Archived on 2026-09-26; superseded by [the operational evaluator plan](PLAN_operational-evaluator.md).
> Status fields below preserve historical claims, not verified completion.

## Objective

Demonstrate that an actual Codex CLI task yields a complete, queryable ledger
of the files, bytes, offsets, processes, and text lines it read.

## Scope

- A deterministic task with known files in target, skills, external context,
  dependency/cache, evaluator, and system categories.
- Direct reads, search/tool subprocesses, repeated and partial reads.
- Immutable snapshots, mutations, binary files, and sensitive-content policy.

## Output

A retained real-CLI audit bundle and human-readable read ledger linked to its
raw exact sidecar.

## Sequence

1. **R8-S1 — Create the known-read task**
   - **Action:** Prepare harmless sentinel files and an oracle identifying the
     expected categories without prescribing the route.
   - **Output:** Controlled real-CLI task and ground truth.
   - **Exit check:** The task can distinguish a missing file read from an
     unobserved file read.
2. **R8-S2 — Capture and reconcile**
   - **Action:** Run Codex and reconcile every returned span against immutable
     snapshots and line mappings.
   - **Output:** Complete exact ledger and report.
   - **Exit check:** The ledger shows actual real-CLI reads with no guessed
     content or lines.
3. **R8-S3 — Inspect the reviewer view**
   - **Action:** Verify the compact report against the raw sidecar and oracle.
   - **Output:** Human-readable audit section.
   - **Exit check:** A reviewer can identify each file/process/span without
     opening unrelated technical traces.

## Completion criteria

- At least one real Codex CLI bundle is exact-read valid.
- Every reported file and line is backed by returned bytes and a file hash.
- All path categories used by the task are classified.
