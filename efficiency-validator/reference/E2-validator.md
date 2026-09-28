---
plan_id: E2
kind: subplan
parent: E0
phase: 2
status: complete
depends_on: [E1]
consumers: [E3, E4, efficiency-validator, context-lab/runs]
---

# E2 — Reusable capture and artifacts

## Objective

Turn the E1 observability proof into a reusable, controlled run-capture
pipeline that emits complete artifacts or explicit unavailable states without
adding validator dependencies to the measured target.

## Scope

- One-command host capture around `codex exec --json`.
- Optional privileged macOS filesystem sidecar and future Linux adapter seam.
- Run manifests, sidecar correlation, redaction, and artifact layout.
- Stable library/CLI interfaces for downstream quality and comparison phases.

## Output

A reusable capture package that produces a run bundle containing the raw Codex
stream, manifest, observability report, optional filesystem sidecar, and clear
availability/provenance diagnostics.

## Dependencies

- E1 observability contract and pinned runtime.
- Isolated staged-target protocol.
- Existing validator parser, report, evaluator sidecar, and run layout.
- Host authorization policy for privileged filesystem tracing.

## Sequence

1. **E2-S1 — Define the run-bundle interface**
   - **Action:** Specify bundle paths, manifest fields, correlation keys, and
     versioning rules.
   - **Output:** Stable capture API and artifact contract.
   - **Exit check:** A consumer can locate every required input without
     inspecting implementation details.

2. **E2-S2 — Build the capture orchestrator**
   - **Action:** Coordinate staging, runtime, Codex collection, optional
     filesystem tracing, conversion, and report generation.
   - **Output:** Reusable CLI with safe cleanup and no silent elevation.
   - **Exit check:** A fresh run produces a bundle with one command or reports
     the exact unavailable reason.

3. **E2-S3 — Add platform and privacy seams**
   - **Action:** Keep macOS `fs_usage` behind an adapter, define the Linux
     audit adapter boundary, and redact or root-relativize sensitive paths.
   - **Output:** Platform adapter interface and privacy policy.
   - **Exit check:** Unsupported, denied, partial, and available sources remain
     distinguishable and testable.

4. **E2-S4 — Verify artifact integrity**
   - **Action:** Validate hashes, manifest joins, sidecar correlation, and
     refusal to overwrite or mix runs.
   - **Output:** Integrity checks and diagnostics.
   - **Exit check:** Tampered, mismatched, and incomplete bundles are rejected
     before downstream evaluation.

## Consumers

- E3 consumes the captured command report and final answer.
- E4 consumes the run manifest, observability metrics, and E3 quality result.
- E5 consumes the complete bundle for fixtures and real-pair validation.
- Future skill evaluations consume the reusable capture CLI.

## Completion criteria

- A host can capture a run without manually assembling intermediate commands.
- Every metric has source, authority, correlation, and availability state.
- Privileged tracing is explicit and never silently requested.
- Artifacts are reproducible, integrity-checked, and safe to compare.
- Unit and integration fixtures cover available, denied, partial, malformed,
  and unavailable capture paths.
