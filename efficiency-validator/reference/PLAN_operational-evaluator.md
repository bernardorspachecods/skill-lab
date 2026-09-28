---
plan_id: O0
kind: root
parent: null
phase: root
status: complete
depends_on: []
consumers: [context-lab, skill and context experiments, operator]
---

# Operational LLM efficiency evaluator

## Objective

Deliver a working evaluator that runs real agent tasks, retains inspectable
operational evidence, and subsequently compares context architectures and skills.
First make collection usable; interpretation follows as a separate phase.

## Scope

- Start with the real Codex CLI and user-selected tasks, targets and variants.
- Record execution configuration, observable activity, usage, timing, outcomes
  and evidence limitations in a reusable local bundle.
- Phase 1 must preserve reproducible inputs, controlled starting conditions,
  work products, human interventions and partial evidence, and support offline
  report regeneration. Its plan owns the detailed acceptance requirements.
- Reuse existing capture, parsing and reporting code only after verification.
- Keep experiment tasks and results with the caller, outside this tool's source.
- Do not require an oracle or efficiency verdict to capture an operational run.
- Full OS read auditing, privileged tracing, VM migration, replacement runtimes
  and a universal efficiency score are outside the initial delivery.

The [previous exact-read plans](PLAN_exact-read-audit.md) are archived
research. Their completion labels are not acceptance evidence for this plan.
Existing exact-read code remains optional and must not certify completeness
without independent proof or block unrelated operational measurements.

Evidence must distinguish requested file operations, returned tool output,
observed filesystem access and proven model input. None implies all the others.
Unobserved data is unavailable, never zero. Truncated output stays explicitly
truncated. Token estimates must not be labelled measured usage.

Without exact OS byte capture, the tool cannot certify every file read by every
process, exact read offsets/line spans, total filesystem bytes or complete
filesystem rereads. It can still report exposed tool activity and usage; their
actual availability must be established in phase 1. Even exact OS capture would
not prove which content entered the model context or was used in reasoning.

## Output

A reusable capture-and-report workflow, followed by evidence-backed comparative
analysis. Phase 1 is independently useful and ships before phase 2 starts.

## Plan tree

- [Phase 1 — Operational collection](PLAN_operational.md): real execution,
  evidence retention and a factual report usable without comparative analysis.
- [Phase 2 — Analysis](PLAN_analysis.md): quality-aware comparisons of variants
  using the measurements demonstrated by phase 1.

## Sequence

1. **O1 — Deliver operational collection**
   - **Action:** Execute the phase 1 plan against the installed CLI.
   - **Output:** Verified capture workflow and inspectable real-run bundle.
   - **Exit check:** A user can repeat a task with another configuration and
     obtain separate reports with explicit coverage and execution status.
2. **O2 — Deliver analysis**
   - **Action:** Execute phase 2 after operational acceptance, refining analysis
     choices with the user from actual captured evidence.
   - **Output:** Comparative report with traceable claims and limitations.
   - **Exit check:** Supported differences can be inspected; missing evidence
     and insufficient repetitions constrain conclusions.

## Completion criteria

- Both phase outputs have real execution evidence, not only synthetic fixtures.
- Capture and factual reporting work without optional exact-read instrumentation.
- Configurations and raw evidence remain identifiable and reusable for analysis.
- Collection limitations constrain only claims that depend on missing evidence.
- A documented operator workflow reproduces the accepted result.

## Execution state

O1 is accepted and archived in `PLAN_operational.md`; evidence is
published in [the operational acceptance record](../docs/operational-acceptance.md).
O2 is complete; the comparison is published in
[the analysis acceptance record](../docs/analysis-acceptance.md).

The plan-management closure gate now applies to this root plan. Its outputs,
dependencies and consumers have been verified; choose whether to archive or
delete the root plan before starting another plan.
