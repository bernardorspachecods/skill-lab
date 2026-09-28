---
plan_id: V0
kind: root
parent: null
phase: root
status: complete
depends_on: []
consumers: [efficiency-validator, future skill evaluations, context-lab reports]
---

# Efficiency Validator — Report and Evidence Hardening

## Objective

Make the efficiency validator trustworthy enough to support skill evaluations
by capturing the maximum observable evidence, binding every run to its exact
inputs and provenance, and producing an exhaustive auditable report before any
efficiency conclusion is trusted.

Existing E0–E5 artifacts remain available as the implementation history and
input to this work. Their real-run conclusions are exploratory until this plan
closes the provenance and comparison gaps.

## Scope

- Exact prompt capture, prompt hashes, task identity, and structured controlled
  variation metadata.
- Oracle identity and digest, model/runtime/target identity, skill/context
  artifacts, and capture configuration in the run manifest.
- Maximum observable raw evidence: turns, commands, searches, tool calls,
  tokens, context/input usage, filesystem traces, failures, retries, timing,
  and unavailable reasons.
- One exhaustive report containing raw evidence, normalized metrics, prompt
  differences, quality evidence, deltas, trade-offs, and verdict inputs.
- Pair integrity, baseline isolation, aggregation, replay, and fixtures.

## Output

A hardened validator release whose saved run bundles and reports can reconstruct
what was sent, what was observed, what was unavailable, and why a comparison is
or is not eligible for a verdict.

The first report version intentionally retains maximum detail. Filtered
technical and analytical views are deferred until real reports show which
fields are useful.

## Plan tree

- [V1 — Run identity and provenance](V1-provenance.md) binds prompts, oracles,
  variations, and execution identities to each manifest.
- [V2 — Exhaustive observable capture](V2-capture.md) records the maximum
  available prompt, context, call, token, filesystem, and failure evidence.
- [V3 — Exhaustive report and prompt diff](V3-report.md) exposes raw and
  derived evidence together, including complete run-to-run differences.
- [V4 — Trustworthy comparison and aggregation](V4-analysis.md) rejects
  contaminated pairs and separates exploratory results from supported claims.
- [V5 — Fixtures, migration, and revalidation](V5-validation.md) proves the
  contract and reruns evaluations only after the evidence gates pass.
- [V6 — Authoritative filesystem tracing](V6-filesystem-tracing.md) adds a
  macOS-native privileged collector and binds its output to each run.

## Sequence

1. **V0-S1 — Freeze the evidence contract**
   - **Action:** Define which observable inputs, events, metrics, identities,
     hashes, and unavailable states are mandatory or optional.
   - **Output:** V1–V5 plan tree and evidence contract.
   - **Exit check:** A report consumer can identify every field's source,
     authority, and absence semantics.

2. **V0-S2 — Harden capture and manifests**
   - **Action:** Execute V1 and V2 against fixtures and one controlled run.
   - **Output:** Provenance-complete bundles with exhaustive observable traces.
   - **Exit check:** Missing prompt, oracle, variation, or identity evidence
     makes a run explicitly ineligible instead of silently producing nulls.

3. **V0-S3 — Build the exhaustive report**
   - **Action:** Execute V3 with raw evidence, normalized metrics, and prompt
     diffs in one report.
   - **Output:** Reconstructable report schema and CLI output.
   - **Exit check:** A reviewer can see the complete difference between two
     runs without opening raw JSONL first.

4. **V0-S4 — Make comparison conservative**
   - **Action:** Execute V4 with pair-integrity gates, baseline-isolation
     checks, aggregation, variance, and explicit exploratory status.
   - **Output:** Trustworthy comparison and aggregate report contract.
   - **Exit check:** A contaminated or under-specified pair cannot emit a
     supported efficiency verdict.

5. **V0-S5 — Revalidate before new skill claims**
   - **Action:** Execute V5, migrate fixtures, and rerun controlled pairs only
     after all mandatory evidence gates pass.
   - **Output:** Regression suite and a new evidence-backed evaluation set.
   - **Exit check:** Replayed inputs are deterministic and every published
     result links to complete prompts, provenance, quality, and raw evidence.

## Completion criteria

- Every run stores the exact explicit prompt and a deterministic prompt hash.
- Every run stores oracle identity/digest and a structured controlled
  variation; absent values are rejected or explicitly unavailable with a
  reason.
- Reports expose all observable calls, token categories, context/input data,
  filesystem evidence, failures, retries, timing, and provenance before any
  filtering.
- A reviewer can inspect prompt additions/removals and all material run
  differences from the report itself.
- Pair validation checks the actual evidence contract, not only a declared
  `task_hash` and variation label.
- Quality remains a gate, and aggregate results expose variance rather than
  allowing one favorable run to stand for a skill.
- Existing E0–E5 runs remain preserved as history and are not presented as
  trustworthy evidence until they satisfy the new contract.
- Fixtures cover missing, mismatched, partial, contaminated, and fully valid
  bundles; the full suite passes before new skill evaluations resume.
- Automatic filesystem tracing is available as an explicitly authorized,
  fail-closed capture mode; unavailable or denied tracing remains visible.
