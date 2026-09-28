---
plan_id: R1
kind: subplan
parent: R0
phase: 1
status: complete
depends_on: []
consumers: [R2, R3, R4, efficiency-validator/docs]
---

# R1 — Exact evidence contract

> Archived on 2026-09-26; superseded by [the operational evaluator plan](PLAN_operational-evaluator.md).
> Status fields below preserve historical claims, not verified completion.

## Objective

Define the authoritative evidence required for an exact file-read efficiency
measurement before choosing or implementing the collector.

## Scope

- Read, returned, opened, scanned, mapped, and failed access semantics.
- File identity/version, process identity, byte spans, content hashes, and
  text line mapping.
- Required coverage for every descendant process and every path category.
- Sensitive-data retention and explicit authorized audit mode.
- Invalid-run reasons and the distinction between byte-exact and line-exact
  evidence.

## Output

A versioned schema and coverage matrix consumed by capture, reconstruction,
reporting, and comparison work.

## Sequence

1. **R1-S1 — Specify evidence units**
   - **Action:** Define the fields and authority for each read event.
   - **Output:** Exact-read event contract.
   - **Exit check:** Every field needed by the root completion criteria has a
     named producer.
2. **R1-S2 — Specify access coverage**
   - **Action:** Enumerate read APIs and process/path boundaries that must be
     covered or cause invalidation.
   - **Output:** Coverage matrix and unsupported-case policy.
   - **Exit check:** No access path can be silently omitted.
3. **R1-S3 — Specify retention and validity**
   - **Action:** Define local content retention, file version binding, and
     fail-closed reasons.
   - **Output:** Audit retention and validity contract.
   - **Exit check:** A reviewer can decide validity from the schema alone.

## Completion criteria

- The schema distinguishes process access from bytes returned to that process.
- Exact byte and exact line evidence have explicit requirements.
- All unsupported or unavailable cases invalidate an official file-efficiency
  run rather than becoming zero or indeterminate cost.
- R2, R3, and R4 can implement without redefining the evidence meaning.
