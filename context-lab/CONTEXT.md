# Context Lab Harness

This repository owns the context-architecture research around the synthetic
target repository. It contains the plan, task prompts, experiment control, and
results used to compare and refine agent-facing information structures. The
reusable capture and comparison tool lives in the sibling `efficiency-validator`
project.
It is not the repository navigated by the measured agent.

## Navigation map

| If you need... | See |
| --- | --- |
| Experiment scope and phase order | [PLAN.md](PLAN.md#objective) |
| Agent-facing target repository | [target pointer](TARGET.md#target-repository) |
| Manual prompts | [task context](evaluation/tasks/CONTEXT.md#manual-evaluation-tasks) |
| Run capture, scoring, and reports | [Efficiency Validator](../efficiency-validator/CONTEXT.md#llm-efficiency-validator) |
| Durable experiment decisions | [harness decisions](docs/CONTEXT.md#harness-decisions) |
| Evaluator-only ground truth | External evaluator sidecar, joined after a run |

## Task router

| Request type | First area to open |
| --- | --- |
| Change experiment scope or baseline rules | [PLAN.md](PLAN.md#objective) |
| Change an agent-facing target document | [target pointer](TARGET.md#target-repository) |
| Add or revise a task prompt | [evaluation/tasks/CONTEXT.md](evaluation/tasks/CONTEXT.md) |
| Change exact-read collection or scoring | [active exact-read plan](../efficiency-validator/PLAN_exact-read-audit.md#objective) |
| Review historical validator work | [archived Efficiency Validator plan](../efficiency-validator/reference/PLAN.md#objective) |
| Review validator history | [Hardening history](../efficiency-validator/reference/PLAN_report-hardening.md#objective) |

The target repository must remain free of harness plans, prompts, validator
code, reports, and evaluator oracles.

## Validator invocation

The harness invokes the sibling reusable tool from
`../efficiency-validator/scripts/capture_run.py`, passing this repository's
target, task prompt, evaluator oracle, and output bundle path. The validator
owns capture/parsing/reporting; this harness owns the experiment inputs and
results. A complete integration example is preserved at
[`runs/run-050-forensic-baseline/`](runs/run-050-forensic-baseline/).

## Efficiency validator vocabulary

- **Quality gate:** the decision that a run satisfies the minimum answer
  requirements before any cost comparison is allowed to reward it.
- **Quality review:** normalized evaluator evidence about claims, prohibited
  claims, completeness, authority, and support; it is separate from the
  agent's self-report.
- **Observable cost:** a measured resource such as tokens, commands, or
  filesystem events with provenance and an explicit availability state.
- **Indeterminate:** evidence is insufficient to pass or fail safely; it is
  never treated as zero cost or successful quality.
- **Controlled variation:** the single declared difference between paired runs;
  task identity and all other comparison conditions remain fixed.
