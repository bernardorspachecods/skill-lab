---
plan_id: R2
kind: subplan
parent: R0
phase: 2
status: complete
depends_on: [R1]
consumers: [R3, R4, efficiency-validator/scripts]
---

# R2 — Process read capture

> Archived on 2026-09-26; superseded by [the operational evaluator plan](PLAN_operational-evaluator.md).
> Status fields below preserve historical claims, not verified completion.

## Objective

Capture exact returned bytes from every supported local-file read performed by
the measured process tree.

## Scope

- Authorized host/runtime integration on macOS first, with a replaceable
  collector seam for other hosts.
- Direct, positional, vectored, mapped, and tool-mediated reads.
- Process-tree discovery, short-lived child handling, and correlation.
- All path categories and immutable run identity.
- Raw sidecar durability and capture failure reporting.

## Output

A raw exact-read sidecar whose records contain the event fields defined by R1
and whose missing coverage is itself explicit.

## Sequence

1. **R2-S1 — Select the authoritative boundary**
   - **Action:** Compare OS tracing, runtime interception, filesystem
     virtualization, and wrapper approaches against the R1 matrix.
   - **Output:** Chosen collector design and rejected-alternative rationale.
   - **Exit check:** The design can observe returned bytes, not merely opens.
2. **R2-S2 — Implement process-correlated capture**
   - **Action:** Capture reads from the launcher and all descendants without
     silently filtering path categories.
   - **Output:** Versioned raw sidecar and process coverage artifact.
   - **Exit check:** Fixtures demonstrate direct, child-process, and tool
     subprocess reads with exact returned bytes.
3. **R2-S3 — Integrate lifecycle and failures**
   - **Action:** Bind startup, shutdown, timeout, permission, and collector
     failures to the run manifest.
   - **Output:** Capture mode with explicit complete/incomplete status.
   - **Exit check:** Any lost process or read channel is reported as a hard
     validity failure.

## Completion criteria

- The collector captures all supported read mechanisms in the R1 matrix.
- Every captured event identifies the process, path, operation, bytes, and
  source authority.
- Process escapes and collector failures are detectable and fail closed.
- The measured target remains free of validator implementation and sidecars.
