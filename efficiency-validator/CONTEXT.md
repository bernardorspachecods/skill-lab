# LLM Efficiency Validator

This is the reusable tool that captures observable LLM-run evidence, applies a
quality gate, compares equivalent runs, and produces explainable efficiency
reports. It is independent of any one experiment, target repository, or task
corpus.

## Task router

| If you need to... | Start here |
| --- | --- |
| Capture a new LLM run | [operational protocol](docs/operational-protocol.md#capture) |
| Review the completed evaluator plan | [archived evaluator plan](reference/PLAN_operational-evaluator.md#plan-tree) |
| Investigate exact file-read auditing | [archived exact-read plan](reference/PLAN_exact-read-audit.md#objective) |
| Review quality or comparison rules | [archived plan](reference/PLAN.md#objective) |
| Inspect schemas or evidence limits | [trace schema](docs/trace-schema.md#primary-baseline-evidence) |
| Understand historical decisions | [reference plans](reference/PLAN_report-hardening.md#objective) |

## Navigation map

| If you need... | See |
| --- | --- |
| Completed scope and delivered outputs | [archived evaluator plan](reference/PLAN_operational-evaluator.md#objective) |
| Historical scope and completed work | [archived plan](reference/PLAN.md#objective) |
| Plan state pointer | [CURRENT-STATE.json](CURRENT-STATE.json) |
| Product and protocol documentation | [docs/CONTEXT.md](docs/CONTEXT.md#efficiency-validator-documentation) |
| Archived plans and implementation history | [hardening history](reference/PLAN_report-hardening.md#objective) |
| Run the command-line tools | [operational protocol](docs/operational-protocol.md#capture) |
| Understand schemas and evidence limits | [docs/trace-schema.md](docs/trace-schema.md#primary-baseline-evidence) |
| Use the tool in context-lab | [context-lab harness](../context-lab/CONTEXT.md#context-lab-harness) |

## Ownership boundary

- This project owns reusable capture, parsing, quality, comparison, and
  report-generation code.
- It does not own experiment tasks, target repositories, evaluator ground
  truth, or experiment results.
- A caller supplies the target, task prompt, configuration and output location;
  operational capture does not require an oracle.
- The evaluator sidecar remains external to both this tool and the measured
  target; the tool consumes its normalized evidence after a run.

## Main implementation areas

- [src/efficiency_validator/](src/efficiency_validator/) — reusable library.
- [scripts/](scripts/) — host-side command-line entrypoints.
- [tests/](tests/) — fixtures and regression tests for the tool.
- [docs/](docs/) — current protocol and schema documentation.
- [reference/](reference/) — completed or superseded plans and historical decisions.
