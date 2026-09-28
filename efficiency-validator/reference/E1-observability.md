---
plan_id: E1
kind: subplan
parent: E0
phase: 1
status: complete
depends_on: []
consumers: [E2, efficiency-validator, context-lab/runs]
---

# E1 — Token and filesystem observability

## Objective

Extend the run boundary so token usage and filesystem activity can be recorded
with authoritative provenance, while preserving `unavailable` for signals the
selected runtime cannot expose.

## Scope

- Codex `exec --json` event and SDK usage contracts.
- Codex app-server/exec-server paths relevant to command and filesystem
  visibility.
- Host/runtime or OS-level file-access tracing for the staged target.
- Event correlation, privacy, reproducibility, and parser fixtures.

## Output

An implemented and documented observability contract that produces token
usage fields and filesystem trace fields, or records a precise unavailable
reason for each field.

## Dependencies

- Existing `efficiency_validator` event parser and manifest model.
- A pinned Codex CLI/runtime version.
- The isolated staged-target protocol.
- Official Codex protocol and SDK references:
  - [Codex exec event schema](https://github.com/openai/codex/blob/main/codex-rs/exec/src/exec_events.rs)
  - [Codex TypeScript SDK turn usage](https://github.com/openai/codex/blob/main/sdk/typescript/src/thread.ts)
  - [Parsed command approval schema](https://github.com/openai/codex/blob/main/codex-rs/app-server-protocol/schema/json/ExecCommandApprovalParams.json)
  - [Codex exec-server filesystem/process protocol](https://github.com/openai/codex/blob/main/codex-rs/exec-server/README.md)

## Sequence

1. **E1-S1 — Audit token sources**
   - **Action:** Inspect current and pinned Codex JSONL shapes, SDK/runtime
     surfaces, and turn completion semantics.
   - **Output:** Token-source decision recording input, cached, cache-write,
     output, reasoning, total derivation, and missing-data behaviour.
   - **Exit check:** A fixture proves parsing of `turn.completed.usage` and a
     fixture proves incomplete/failed turns are not reported as complete.

2. **E1-S2 — Audit filesystem sources**
   - **Action:** Compare command-level parsed paths, app-server/exec-server
     signals, and host/OS tracing options for the staged target.
   - **Output:** A selected filesystem signal with alternatives and blind spots
     recorded.
   - **Exit check:** The selected signal distinguishes requested paths,
     returned paths, and physically opened/scanned paths where possible.

3. **E1-S3 — Define correlation and provenance**
   - **Action:** Specify how token and filesystem records attach to run,
     turn, command/process, timestamp, target revision, and runtime revision.
   - **Output:** Versioned event/manifest additions and provenance rules.
   - **Exit check:** A record can be traced back to one run and one runtime
     source without relying on agent self-report.

4. **E1-S4 — Implement collection and parsing**
   - **Action:** Extend the collector/parser and staging launcher while
     keeping the target repository free of validator dependencies.
   - **Output:** Collector, parser, schema, and diagnostics.
   - **Exit check:** Malformed, truncated, denied, and unavailable signals are
     preserved as explicit issues or statuses.

5. **E1-S5 — Verify with fixtures and one real capture**
   - **Action:** Run unit fixtures plus one isolated Codex capture against a
     pinned staged target.
   - **Output:** Verified E1 report and known observability limits.
   - **Exit check:** E2 can consume the output without guessing missing values.

## Consumers

- E2 consumes the metric schema and provenance contract.
- The validator report consumes parsed usage and filesystem events.
- Future runtime upgrades consume the compatibility fixtures.

## Completion criteria

- Token usage is parsed from an authoritative runtime event when available.
- Filesystem evidence has a documented authority boundary and correlation key.
- No shell output or agent prose is promoted to authoritative file access.
- Missing, denied, partial, and unsupported measurements remain distinguishable.
- Existing baseline parsing and reports remain compatible or are versioned.
- Unit tests and one real capture pass with a reproducible manifest.
