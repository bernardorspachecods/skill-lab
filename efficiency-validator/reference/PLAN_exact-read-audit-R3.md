---
plan_id: R3
kind: subplan
parent: R0
phase: 3
status: complete
depends_on: [R1, R2]
consumers: [R4, efficiency-validator/reports]
---

# R3 — Byte and line reconstruction

> Archived on 2026-09-26; superseded by [the operational evaluator plan](PLAN_operational-evaluator.md).
> Status fields below preserve historical claims, not verified completion.

## Objective

Turn exact returned-byte events into a version-stable ledger of bytes and line
ranges without guessing when the evidence is insufficient.

## Scope

- File snapshots or equivalent content/version binding.
- Offset and byte-range validation, overlap, repetition, and partial reads.
- Newline and encoding handling for text files.
- Binary, generated, compressed, deleted, and mutated files.
- Human-readable file/line summaries backed by raw evidence.

## Output

A queryable read ledger that can answer which exact bytes and lines were
returned for each file/process event.

## Sequence

1. **R3-S1 — Bind file versions**
   - **Action:** Match every event to immutable content, size, and hash.
   - **Output:** Versioned file evidence records.
   - **Exit check:** Mutations and missing snapshots are detected.
2. **R3-S2 — Map bytes to lines**
   - **Action:** Calculate line spans from the captured file version and
     preserve exact returned content.
   - **Output:** Line-aware ledger for textual files and byte-only ledger for
     non-text files.
   - **Exit check:** Partial, full, repeated, and overlapping reads produce
     deterministic results.
3. **R3-S3 — Expose the ledger**
   - **Action:** Add raw and compact views without dropping evidence needed for
     replay or audit.
   - **Output:** Machine-readable ledger and reviewer-facing read summary.
   - **Exit check:** A reviewer can identify file, version, process, bytes, and
     lines without opening unrelated raw traces.

## Completion criteria

- Line ranges are calculated only against the exact file version returned.
- No line range is invented for binary or incomplete evidence.
- The ledger retains enough raw data to audit every reported metric.
- R4 can determine completeness from the ledger without heuristics.
