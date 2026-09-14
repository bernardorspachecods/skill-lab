# Agent Skills Catalog

This repository is the source of truth for reusable agent skills.

## Contract

- Every skill lives in `skills/<skill-name>/`.
- Every skill has `SKILL.md` with `name` and `description` frontmatter.
- Use lowercase hyphen-case names and keep the directory name equal to the
  frontmatter `name`.
- Put UI metadata in `agents/openai.yaml` when the runtime supports it.
- Keep detailed, branch-specific material in `references/`; keep deterministic
  helpers in `scripts/`.
- Project-specific skills stay in their project repository and do not get
  copied into this catalog.
- Runtime paths must point to this catalog; do not maintain independent copies.

## Architecture map

See [SKILL-ARCHITECTURE.md](SKILL-ARCHITECTURE.md) for the current-state
catalog, route-to-skill matrix, principle inventory, and inferred composition
relationships. That document is an `as-is` inventory, not a runtime instruction
or a decision about which skills should later be kept, changed, or removed.

## Verification

Validate every changed skill with the skill validator and check that runtime
links resolve before publishing the catalog.
