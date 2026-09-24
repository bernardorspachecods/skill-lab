# LLM Workspace Context

This repository contains reusable agent skills and the development work that
supports them. General LLM knowledge and database knowledge live in the
personal library; do not recreate those corpora here.

## Task router

The table below routes each request to its first destination. Open the linked
area map before reading deeper files.

## Navigation map

| If you need to... | Start here | Likely dependencies |
| --- | --- | --- |
| Use or change a reusable agent skill | [Agent Skills Catalog](agent-skills/AGENTS.md) | The affected skill and its resources |
| Develop or validate skill-related context workflows | [Context Lab](context-lab/CONTEXT.md) | `context-lab-target/`, `context-lab-evaluator/` |
| Work on the research-skill development area | [Research skill work](new/research_skill/PLAN.md) | Its local plans and evaluation documents |
| Consult general LLM knowledge | [LLMs area in the personal library](../personal-library/LLMs/CONTEXT.md) | The relevant topic index or source |
| Consult database knowledge | [Databases area in the personal library](../personal-library/Databases/CONTEXT.md) | Its `INDEX.md` and the relevant note |

## Direct destinations

- [agent-skills/](agent-skills/) — reusable agent skills and their catalog
  contract.
- [context-lab/](context-lab/) — research and improvement of context
  architecture, with navigation interventions evaluated later.
- [context-lab-target/](context-lab-target/) — synthetic repository used as a
  navigation-test target.
- [context-lab-evaluator/](context-lab-evaluator/) — evaluator sidecar with
  ground truth; it is not context for the measured agent.
- [new/](new/) — skill-development work that is not yet part of the catalog.
- [../personal-library/LLMs/CONTEXT.md](../personal-library/LLMs/CONTEXT.md) —
  canonical owner for the general LLM knowledge corpus moved out of this
  repository.
- [../personal-library/Databases/CONTEXT.md](../personal-library/Databases/CONTEXT.md)
  — canonical owner for the database encyclopedia moved out of this
  repository.

## Ownership boundary

- Executable agent behaviour and directly related development work belong in
  this repository.
- General explanations, patterns, examples, source notes, and database
  references belong in `personal-library`.
- Project implementation details and current state belong in their project
  repositories.
- Keep one canonical owner. Link to the personal library when knowledge is
  needed; do not copy it back into this workspace.
