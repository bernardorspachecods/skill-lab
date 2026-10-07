# Agent skills

This area is the source of truth for reusable agent skills and the tooling
that validates and catalogs them.

## Navigation map

| Request | First area | Likely dependencies |
| --- | --- | --- |
| Use or change a skill | [Skill authoring rules](skills/skill-authoring/SKILL.md) and the target package under [`skills/`](skills/) | Generated catalog and package resources |
| Redo a plan that missed the user's need | [Redo plan protocol](skills/plan-management/references/redo-plan-protocol.md#redo-plan-protocol) | Original plan and outputs; [durable plan contract](skills/plan-management/references/durable-plan-contract.md#durable-plan-contract) |
| Discuss the shared artifact model for plans, research, reviews, and knowledge | [Artifact model decisions](ARTIFACT-MODEL-DECISIONS.md) | Evolution drafts and the linked organization experiment handoff |
| Inspect the generated catalog | [SKILL-ARCHITECTURE.md](SKILL-ARCHITECTURE.md) or [interactive catalog](SKILL-ARCHITECTURE.html) | Skill packages and supported runtime metadata |
| Validate skill packages | [validate_skill_catalog.py](scripts/validate_skill_catalog.py) | `skills/`, `agents/openai.yaml`, and references |
| Regenerate or check the catalog | [generate_skill_catalog.py](scripts/generate_skill_catalog.py) | Validator contract and `SKILL-ARCHITECTURE.md` |
| Work on repository health checks | [health-check.md](health-check.md) | Context architecture, plans, and skill validation |
| Review the completed catalog plan | [reference/skill-catalog.md](reference/skill-catalog.md) | Generated catalog and regression tests |
| Run catalog regression tests | [test_skill_catalog.py](tests/test_skill_catalog.py) | Catalog scripts and controlled fixtures |

## Ownership and boundaries

- `skills/` contains the canonical skill packages; project-specific skills
  remain in their project repositories.
- `SKILL-ARCHITECTURE.md` and `SKILL-ARCHITECTURE.html` are generated from the
  packages and supported runtime metadata. Do not edit them manually.
- `scripts/` contains deterministic catalog tooling, and `tests/` contains its
  controlled verification cases.
- `reference/` contains archived plans and consultative material, not active
  execution state.

## Catalog maintenance

From this directory:

```bash
python3 scripts/validate_skill_catalog.py . --json
python3 scripts/generate_skill_catalog.py . --write
python3 scripts/generate_skill_catalog.py . --check
```

The validator is read-only. The generator writes only when `--write` is
explicitly supplied, and only to the two generated catalog files.
