# Skill Lab Context

This repository develops reusable agent skills, context workflows, and
evaluation tooling.

## Task router

The table below routes each request to its first destination. Open the linked
area map before reading deeper files.

## Navigation map

| If you need to... | Start here | Likely dependencies |
| --- | --- | --- |
| Use or change a reusable agent skill | [Agent Skills](agent-skills/CONTEXT.md#navigation-map) | The affected skill and its resources |
| Build, run, or improve the LLM efficiency validator | [Efficiency Validator](efficiency-validator/CONTEXT.md#llm-efficiency-validator) | Its active plan, CLI, schemas, and tests |
| Develop or validate skill-related context workflows | [Context Lab](context-lab/CONTEXT.md) | `context-lab-target/`, `context-lab-evaluator/` |
| Reuse or add repository-level findings | [Knowledge index](knowledge/INDEX.md#repository-knowledge) | The relevant entry and its provenance |

## Direct destinations

- [agent-skills/](agent-skills/) — reusable agent skills and their catalog
  contract.
- [efficiency-validator/](efficiency-validator/CONTEXT.md#llm-efficiency-validator) — reusable tool for
  capturing, quality-gating, comparing, and reporting LLM runs.
- [context-lab/](context-lab/) — research and improvement of context
  architecture, with navigation interventions evaluated later.
- [context-lab-target/](context-lab-target/) — synthetic repository used as a
  navigation-test target.
- [context-lab-evaluator/](context-lab-evaluator/) — evaluator sidecar with
  ground truth; it is not context for the measured agent.
- [knowledge/INDEX.md#repository-knowledge](knowledge/INDEX.md#repository-knowledge) — reusable repository-level findings
  and their entrypoints.
- [LR-04 archived plan](plans/reference/LR-04/PLAN.md#objective) — completed
  literature review with durable research and review records.

## Ownership boundary

- Executable agent behaviour and directly related development work belong in
  this repository.
- `knowledge/` contains repository-level reusable findings; its index routes
  to entries and each entry records its source artifacts and limitations.
- General explanations, patterns, examples, and source notes belong with the
  project or skill that owns them.
- Keep one canonical owner for each piece of guidance; link to it instead of
  maintaining competing copies.
