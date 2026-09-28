---
plan_id: V6
kind: subplan
parent: V0
phase: 6
status: complete
depends_on: [V5]
consumers: [efficiency-validator, future skill evaluations, context-lab reports]
---

# V6 — Authoritative filesystem tracing

## Objective

Capture actual filesystem access performed during a measured Codex run, with
macOS kernel-level provenance, without treating command text or agent prose as
file-access evidence.

## Scope

- A local macOS helper that requests administrator authorization through the
  operating system and runs `fs_usage`.
- Start/stop lifecycle around the Codex process, target-prefix filtering, and
  run/case correlation.
- Explicit permission, timeout, denied, malformed, and unavailable states.
- Unit fixtures, documentation, and one authorized smoke capture.

## Output

An opt-in `capture_run.py` filesystem mode that produces a correlated
`filesystem-trace-1` sidecar automatically, while failing closed when the
requested authoritative collector cannot be started.

## Sequence

1. **V6-S1 — Define the privileged boundary**
   - **Action:** Fix the helper command, authorization boundary, target filter,
     and lifecycle contract.
   - **Output:** Local helper interface and security notes.
   - **Exit check:** No password is accepted by the harness and no
     unfiltered system-wide event is attributed to a run.

2. **V6-S2 — Implement automatic capture**
   - **Action:** Add the macOS helper and integrate it around the collector.
   - **Output:** Opt-in automatic filesystem sidecar mode.
   - **Exit check:** Start, stop, timeout, and authorization failures produce
     deterministic statuses and never silently become zero events.

3. **V6-S3 — Verify and document**
   - **Action:** Add mocked lifecycle tests, run the full suite, and perform one
     authorized smoke capture when the host permits it.
   - **Output:** Tested helper, report evidence, and operator instructions.
   - **Exit check:** A real run contains filesystem events or an explicit
     unavailable/denied reason tied to the capture attempt.

## Completion criteria

- The helper never receives or stores the administrator password.
- Filesystem events are filtered to the staged target and correlated to the
  measured run.
- Automatic mode is opt-in, fail-closed, and covered by tests.
- The report distinguishes kernel-observed filesystem events from commands,
  requested paths, and unavailable evidence.
- At least one host-authorized smoke capture is recorded, or the exact host
  permission blocker is preserved as an explicit limitation.

## Verification record — 2026-09-24

- Focused helper and integration tests pass; the full validator suite passes
  with 53 tests.
- `runs/run-048-fs-auto-filtered` completed with filesystem status `available`,
  source `macos-fs-usage`, authority `os-kernel-observation`, 175 events, and
  no validation issues.
- The filtered raw sidecar contains 175 lines and 43,178 bytes; every captured
  path is under the staged target prefix. No unrelated host path is written to
  the new raw capture.
- The helper is opt-in through `capture_run.py --filesystem-auto`, requests
  authorization through macOS, and never receives or stores the password.
