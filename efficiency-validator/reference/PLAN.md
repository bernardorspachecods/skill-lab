---
plan_id: P0
kind: root
parent: null
phase: root
status: complete
depends_on: []
consumers: [context-lab, future skill evaluations]
---

# Efficiency Validator — Observable Efficiency Evaluation

## Navigation map

| If you need... | See |
| --- | --- |
| Product objective and ownership | [Objective](#objective), [Scope](#scope) |
| Work order and observability priority | [Sequence](#sequence) |
| Definition of done | [Completion criteria](#completion-criteria) |

## Objective

Maintain the efficiency validator as an independent reusable tool that can
capture enough observable evidence to compare equivalent LLM runs: same or
better quality with less model, tool, filesystem, and external-access cost.
Keep experiment control, evaluator truth, targets, and results in their own
owners.

## Scope

- Reusable capture, parsing, quality, comparison, aggregation, and reporting.
- Stable artifact and provenance contracts.
- CLI use by `context-lab` and future evaluation harnesses.
- Documentation and tests owned by the tool.
- Explicit boundaries preventing experiment-specific data from entering the
  product implementation.
- Observable filesystem evidence for the full measured process tree, including
  read coverage rather than only path access.
- Network metadata capture without retaining network payloads.
- Local retention of raw metadata evidence for later analysis, without
  automatically uploading it or silently including it in token totals.

The first implementation priority is capture completeness. How the additional
evidence is weighted in a composite verdict is deliberately deferred until the
raw evidence is reliable.

## Plan tree

- **P0.1 — Establish the independent project boundary** — separate the tool
  from the context-lab harness and migrate reusable implementation.
- **P0.2 — Stabilize package and CLI contracts** — remove migration-only
  assumptions and document caller-provided inputs and outputs.
- **P0.3 — Maximize forensic observability** — capture process-correlated
  filesystem reads, read coverage/content evidence, and network metadata.
- **P0.4 — Operate through controlled evaluations** — use the tool from
  harnesses without copying implementation or experiment truth.

## Output

A self-contained validator project that another harness can invoke with a
target, prompt, oracle, and output directory, without importing context-lab
implementation or reading its experiment corpus.

## Sequence

1. **P0.1 — Establish the project boundary**
   - **Action:** Keep reusable code, tests, current docs, and validator history
     under this project; keep experiment material in its caller.
   - **Output:** One canonical validator owner and updated repository maps.
   - **Exit check:** No validator implementation or plan remains duplicated in
     `context-lab`.
2. **P0.2 — Stabilize interfaces**
   - **Action:** Verify imports, CLI paths, artifact contracts, and legacy
     compatibility after the move.
   - **Output:** Tested package and documented invocation contract.
   - **Exit check:** The full validator suite passes from this project root.
3. **P0.3 — Maximize forensic observability**
   - **Action:** Extend the capture seam beyond the staged target prefix. Tie
     filesystem events to the measured agent process tree, classify target,
     skill, other-repository, external-context, cache/dependency, system,
     evaluator, and sensitive/unknown paths, and record read coverage for each
     file where the host can expose it. Preserve exact read spans or returned
     content in an explicit local audit mode, alongside safe metadata such as
     file size, bytes, line ranges, offsets, and content hashes. Add a network
     metadata adapter recording destination, process, timing, byte counts, and
     result without retaining payloads.
   - **Output:** Versioned forensic evidence bundle and documented capture
     availability/indeterminate states, with no fabricated token counts and no
     automatic upload of raw evidence.
   - **Exit check:** Fixtures and a real smoke path demonstrate process-tree
     correlation, partial-versus-full file-read evidence, category labels, and
     network metadata when the host permits it; unavailable or denied sensors
     remain explicit rather than being treated as zero.
   - **Evidence:** `tests/` covers structured partial/full reads, process-name
     correlation, path categories, and network metadata. The real bundles
     `context-lab/runs/run-052-forensic-fs-corrected/` and
     `context-lab/runs/run-053-forensic-final-smoke/` demonstrate complete
     Codex capture plus the macOS forensic sensor. The host exposed no network
     sidecar and no byte offsets for the observed real reads, so those states
     remain `unavailable`/`indeterminate`.
4. **P0.4 — Use through harness integration**
   - **Action:** Update context-lab to call this tool while retaining only its
     own tasks, targets, oracles, and results.
   - **Output:** Thin harness integration with no copied validator logic.
   - **Exit check:** A context-lab evaluation can produce a report through the
     new owner and the target remains free of tool/evaluator files.
   - **Evidence:** `context-lab/runs/run-050-forensic-baseline/` is a valid
     complete report produced by the new owner from the context-lab target,
     oracle, prompt, and runtime manifests.

## Completion criteria

- `efficiency-validator` has one clear owner for reusable code and docs.
- `context-lab` contains only experiment control and experiment outputs.
- `context-lab-evaluator` remains the owner of task-specific ground truth.
- `context-lab-target` remains free of harness, validator, and evaluator data.
- Tests, links, imports, and documented commands work from the new boundary.
- The validator can distinguish a partial file read from a full-file read when
  the selected host sensor exposes the required offsets, bytes, or content
  spans; otherwise it says indeterminate.
- Additional filesystem and network evidence is reported separately from
  provider token usage until a later plan explicitly defines a composite cost.
