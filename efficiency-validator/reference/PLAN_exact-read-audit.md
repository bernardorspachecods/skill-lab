---
plan_id: R0
kind: root
parent: null
phase: root
status: in_progress
depends_on: []
consumers: [context-lab, future skill evaluations, efficiency-validator reports]
---

# Exact-read audit for file-efficiency verdicts

> Archived on 2026-09-26; superseded by [the operational evaluator plan](PLAN_operational-evaluator.md).
> Status fields below preserve historical claims, not verified completion.

## Objective

Make file-efficiency measurements objective and usable against the real Codex
CLI by recording the exact bytes returned to every process used by the measured
agent, mapping those bytes to immutable file versions and line ranges where the
input is textual, and rejecting any run whose read evidence is incomplete.

The previous R1–R5 foundation is not sufficient by itself: controlled fixtures
proved the collector contract, but the product remains incomplete until the
chosen capture boundary produces a valid exact-read run from a real Codex CLI
session. A fixture-only result is never an exit condition for this revision.

## Scope

- All local file reads performed by the measured agent and every descendant
  process, across the target, skills, other repositories, caches, dependencies,
  and system paths.
- Exact returned-byte capture with path, process, operation, timestamp, file
  identity/version, offset, byte count, and line mapping when applicable.
- Full local audit bundles, path categories, existing token/context/tool
  metrics, and a human-readable summary of the exact read ledger.
- Automatic invalidation when a read, process, file version, byte span, or line
  mapping cannot be proven.

The existing general observability and comparison work remains historical
infrastructure. This plan adds the stricter evidence contract required before
file-read efficiency can support a verdict.

## Output

A reusable exact-read audit mode that produces a complete, locally retained
read ledger from a real Codex CLI session and permits an efficiency verdict only
when every observed file read is exact, process-correlated, and version-stable.

## Plan tree

- [R1 — Exact evidence contract](PLAN_exact-read-audit-R1.md) defines what a
  valid read means and which access mechanisms must be covered.
- [R2 — Process read capture](PLAN_exact-read-audit-R2.md) implements the
  authoritative capture boundary for all descendant processes.
- [R3 — Byte and line reconstruction](PLAN_exact-read-audit-R3.md) binds
  returned bytes to immutable file versions and exact line ranges.
- [R4 — Fail-closed reporting gate](PLAN_exact-read-audit-R4.md) prevents
  incomplete runs from producing efficiency verdicts.
- [R5 — Fixtures and controlled validation](PLAN_exact-read-audit-R5.md)
  proves the contract across real read patterns and records its limits.
- [R6 — Codex CLI boundary and alternatives](PLAN_exact-read-audit-R6.md)
  selects a capture boundary that can observe the real Codex CLI rather than
  only compatible fixtures.
- [R7 — Real CLI runtime integration](PLAN_exact-read-audit-R7.md) launches
  the real Codex CLI through the selected boundary and proves process coverage.
- [R8 — Real exact-read capture](PLAN_exact-read-audit-R8.md) proves bytes,
  snapshots, lines, and path categories from an actual CLI task.
- [R9 — End-to-end paired verdict](PLAN_exact-read-audit-R9.md) connects two
  real CLI runs to reports, quality, comparison, and a valid file-efficiency
  verdict.
- [R10 — Operational hardening and acceptance](PLAN_exact-read-audit-R10.md)
  documents the supported route and prevents fixture-only completion from
  returning.

## Sequence

1. **R1 — Freeze the exact evidence contract**
   - **Action:** Define read events, supported file-access mechanisms, file
     identity, line semantics, sensitive-data handling, and invalid-run rules.
   - **Output:** Versioned exact-read schema and coverage matrix.
   - **Exit check:** Every required verdict field has an authoritative source
     and every unsupported or missing signal has a fail-closed outcome.
2. **R2 — Capture all process reads**
   - **Action:** Implement and integrate an authorized collector at the
     lowest reliable user/process boundary, covering direct reads, positional
     reads, mapped reads, and tool subprocesses.
   - **Output:** Raw exact-read sidecar correlated to the complete measured
     process tree.
   - **Exit check:** Controlled fixtures show that reads by shell tools,
     scripts, and child processes are captured with returned bytes.
3. **R3 — Reconstruct exact bytes and lines**
   - **Action:** Snapshot or otherwise bind file versions, preserve exact
     returned spans, and calculate line ranges only from the captured version.
   - **Output:** Queryable read ledger with exact bytes, offsets, hashes, and
     line ranges for text files; explicit byte-only semantics for non-text.
   - **Exit check:** The ledger detects changed files, overlapping/partial
     reads, repeated reads, binary data, and missing line mappings without
     guessing.
4. **R4 — Enforce the validity gate**
   - **Action:** Make exact-read mode mandatory for file-efficiency verdicts;
     integrate coverage checks, report fields, and comparison eligibility.
   - **Output:** Fail-closed run status and report section explaining every
     accepted or rejected read.
   - **Exit check:** One missing or unverifiable read makes the run ineligible
     and no comparison or verdict is emitted.
5. **R5 — Validate and document operation**
   - **Action:** Run fixtures and controlled evaluations across path classes,
     process lifetimes, read APIs, file mutations, and failure conditions.
   - **Output:** Regression suite, controlled evidence bundles, protocol docs,
     and an explicit list of remaining unsupported cases.
   - **Exit check:** Valid runs contain a complete exact-read ledger; every
     invalid run is rejected for a concrete, inspectable reason.
6. **R6 — Choose a boundary that reaches real Codex CLI**
   - **Action:** Evaluate direct runtime interposition, a rebuilt/unhardened
     CLI, a controlled self-hosted executor/runtime, and privileged OS tracing
     against the exact-read contract.
   - **Output:** A recorded architecture decision with a runnable proof plan
     and rejected-alternative reasons.
   - **Exit check:** At least one candidate boundary is shown, with evidence,
     to expose returned bytes from the real Codex CLI or its complete local
     executor process tree; fixtures alone do not pass this check.
7. **R7 — Integrate the selected real-CLI boundary**
   - **Action:** Make the capture harness launch the real Codex CLI through the
     selected boundary while retaining its normal prompts, tools, sandbox, and
     descendant processes.
   - **Output:** A real-CLI exact-read capture mode and process-coverage
     artifact.
   - **Exit check:** A real `codex exec` task emits trace start/end records and
     identifies the launcher plus every observed descendant, or the run is
     rejected with a concrete boundary failure.
8. **R8 — Prove exact reads from the real task**
   - **Action:** Run a task designed to read known target, skill, external,
     dependency/cache, evaluator, and system files, then reconcile returned
     bytes, immutable snapshots, offsets, and lines.
   - **Output:** A retained real-CLI audit bundle and reviewer-facing ledger.
   - **Exit check:** The bundle shows the actual files and byte/line spans read
     by Codex and passes every validity check without fixture substitution.
9. **R9 — Produce a real paired efficiency verdict**
   - **Action:** Execute two equivalent real Codex CLI runs with one controlled
     variation and feed both through quality, report, and comparison layers.
   - **Output:** Two valid reports, prompt/provenance records, deltas, and a
     file-efficiency verdict.
   - **Exit check:** The pair produces a non-blocked verdict with exact-read
     evidence; an injected missing read still produces no verdict.
10. **R10 — Harden and accept the route**
    - **Action:** Measure operational overhead, document permissions and
      sensitive-content handling, add a real-CLI regression/acceptance test,
      and remove any completion path that accepts fixtures as a substitute.
    - **Output:** Final operator protocol, limitation register, acceptance
      bundle, and updated plan status.
    - **Exit check:** A fresh operator can run the real Codex CLI path and get
      either a valid exact ledger or an explicit invalid run; the plan cannot
      become complete while only controlled fixtures pass.

## Completion criteria

- A valid file-efficiency run has exact returned-byte evidence for every local
  file read by every measured descendant process.
- The valid-run proof is produced by the real Codex CLI or its complete
  selected executor boundary, not only by a synthetic fixture.
- Each read is bound to a stable file identity/version and process identity.
- Text reads expose exact line ranges reconstructed from captured bytes and the
  corresponding file version; binary reads remain byte-exact without invented
  line numbers.
- Target, skills, other repositories, caches, dependencies, and system paths
  are captured and classified rather than silently excluded.
- Missing instrumentation, inaccessible reads, process escapes, changed files,
  unsupported access modes, and malformed sidecars invalidate the run.
- No invalid run can produce an efficiency comparison or verdict.
- Full captured content remains local to an explicitly authorized audit bundle;
  the summary report can expose hashes, spans, lines, and selected content
  without changing the validity decision.
- Existing token, context, tool-call, command, search, timing, network, and
  quality metrics remain separate and available for the eventual composite
  analysis.
- The installed/current Codex CLI path has a demonstrated valid run, or the
  plan remains incomplete with the exact external blocker recorded.
