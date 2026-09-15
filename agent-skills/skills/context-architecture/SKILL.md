---
name: context-architecture
description: Organize repository context and documentation structure. Use when creating or restructuring context files and folders.
---

# Core principles

- Avoid duplicating information between documents; keep necessary repetition minimal.
- Document information that helps an agent navigate the repository or make decisions. Omit details that are already clear from the nearest authoritative source.

# Rules

1. **Each document must have a specific purpose.** Split a document only when a genuinely distinct purpose, audience, authority, or lifecycle justifies it.
2. **When writing be as concise and direct as possible** - maximize token efficiency and content quality at the same time
3. **Keep context discoverable.** - an agent shouldn't have to guess where things are. link the documents. think of it as roads in a city, every building should have a road that leads to it
4. **Separate durable context from temporary work.**
5. **Keep related material distinguishable by purpose and lifecycle** - follow local conventions rather than imposing a universal folder structure. Work in progress, archived work, and consolidated work should preferably be kept separate.
6. **Just because it's written and committed doesn't make it correct** - If the repo docs structure is incorrect propose changes. By the end we should have all the core info intact, but better organized and with 0 duplicated rules, knowledge…
7. **Do not repeat rules that an agent will read in skill** - the rules written for a repo should be specific to that repo, do not include general behavioral rules because agents will read those from skills anyways

# Structure

- **At the repository root:** always keep `README.md` and `CONTEXT.md`. Create `AGENTS.md` only when the repository has specific behavioral rules for agents; do not create an empty or placeholder file.
- **In each relevant folder:** give the folder its own `CONTEXT.md`. Do not require context files in generated, temporary, dependency, or otherwise irrelevant folders unless they need durable guidance.
- **Keep context local and avoid cascading updates:** the `CONTEXT.md` of a parent folder should describe its own scope, stable boundaries, and entrypoints, not every detail inside child folders. Changes inside a child folder should normally update only the nearest `CONTEXT.md`, unless they change the parent's scope, direct structure, or cross-folder contract.

# Terminology

These files have fixed responsibilities:

- `README.md` for the public introduction, installation, and general usage at a repository or independently used package root. Do not create or maintain one for an internal folder merely to document its contents; use the nearest `CONTEXT.md` instead.
- `AGENTS.md` for repository-specific behavioral rules that do not repeat general skill guidance. It is not a general repository index or catch-all document; do not use it for product vision, architecture, current state, plans, or general documentation.
- `CONTEXT.md` for the map and orientation of a folder.

When the repository needs these distinctions, prefer the following names:

- `PLAN.md` for the main plan at the repository root; use `PLAN_<name>.md` for subsequent plans.
- `working/` for working files and active state.
- `reference/` for archived files that might still be useful as backup or for reference.
- `research/` for files that support research and are still in use; move them to `reference/` when they are no longer in use.

# Bad practices to look out for
1. You have to find your way through the documents, instead of being guided by the documents - violates rule 3
2. You have to update 2+ separate files with the same information or the documents contain overlapping responsibilities  - violates rule 1 and the first core principle
3. A parent `CONTEXT.md` repeats the full contents of child `CONTEXT.md` files - violates rule 1, the first core principle, and Structure.
4. A routine change inside a child folder requires updating several parent `CONTEXT.md` files - violates the local context principle.
5. A document contains work in progress, archived material, and consolidated knowledge without clear separation - violates rules 4 and 5.
6. A relevant document exists but is not linked from the nearest `CONTEXT.md` - violates rule 3.
7. A `CONTEXT.md` lists every file manually and becomes stale after normal development - violates rule 3 and the local context principle.
