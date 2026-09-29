---
name: context-architecture
description: Build and maintain repository context and documentation structures. Use when creating, restructuring, or cleaning context files and folders.
---

# Principles

- Give each document a specific purpose. Split only when a genuinely distinct purpose, audience, authority, or lifecycle justifies it.
- Keep decision-relevant information coherent in its canonical document. Write concisely, omit details already clear from an authoritative source, and avoid duplicating information between documents.
- A parent map describes its own scope, stable boundaries, and entrypoints, not every detail inside child folders. A child change should normally update only the nearest `CONTEXT.md`, unless it changes the parent's scope, direct structure, or cross-folder contract.
- Make context discoverable: an agent should not have to guess where information is. Link maps to destinations and destinations to their specific responsibilities.
- Keep the layers distinct: the root router records first entrypoints; a local `CONTEXT.md` records concrete destinations; an owner document records intended rules; and code, migrations, or scripts confirm current behavior. Link the layers where appropriate.
- Separate durable context from temporary work, and keep related material distinguishable by purpose and lifecycle according to local conventions.
- Do not repeat general skill behavior in repository docs. Repository rules should add only local conventions, owners, map names, workflows, or exceptions that the skill cannot know.

# Document vocabulary

## CONTEXT.md

- Repository root: always keep a root `CONTEXT.md`. This file must additionally contain one concise task-intent router in a compact table with the request type, first area to open, and likely dependencies. Keep the router limited to first-entry classification; do not turn it into an exhaustive application map or a duplicate of local context files
- Record repository-specific routing decisions in the root router when they matter, including cross-area work, broad or ambiguous requests, localized bugs, and disagreements between documentation and implementation. Do not impose universal destinations or authority rules where the repository has not established them.
- When a repository maintains repository-level knowledge, link its entrypoint from the root context map. For the knowledge area's purpose, structure, index, entry identities, and provenance, see [Repository knowledge structure](references/knowledge.md). Keep the map as a routing pointer; do not copy knowledge content into it.
- Area boundaries: give a folder its own `CONTEXT.md` only when it is an ownership boundary, a probable agent entrypoint for independent work, an independent documentation area, or contains rules that cannot be inferred quickly from its parent map. Treat these as a small set of parent/area maps, not one map per directory or nesting level.
- A folder without its own `CONTEXT.md` uses the nearest ancestor map. A parent map may link directly to a child folder, file, input, output, or script; that link does not by itself justify a child map. Code internals, generated, temporary, dependency, and otherwise technical folders normally inherit without a context file.
- List relevant direct destinations as Markdown links followed by their specific responsibility.


## AGENTS.md

- Create `AGENTS.md` only when applicable - do not create an empty or placeholder file. The  files contain repository-specific behavioral rules. They are not general repository indexes or catch-all documents; do not use them for product vision, architecture, current state, plans, or general documentation.
- Link explicitly to the `CONTEXT.md` that maps the same scope, visibly near the beginning. A root file links the root map; a nested file links the nearest applicable map.

## README.md

- `README.md` is a public GitHub-facing artifact, not internal application context. If it is an internal legacy manual or router while another document is canonical, migrate the needed information and consumers to the appropriate owner, then remove the obsolete material.

## CURRENT-STATE.json

- Optional, machine-readable resume pointer. Only relevant when there is an active plan whose implementation an agent may need to resume — do not create one per folder, and do not create a context boundary merely to house a state file.
- When a scope has an active plan to resume, its `CONTEXT.md` must link to the adjacent `CURRENT-STATE.json`.

# Workflows

## Creating a new structure

Before creating a nested `CONTEXT.md`, ask:

1. Does the folder represent a distinct responsibility or ownership boundary?
2. Is it a likely first entrypoint for a class of tasks rather than an implementation detail?
3. Does it contain durable local rules or an independent documentation area?

If the answer is no to all three, keep the folder under its nearest parent map. Prefer a shallow hierarchy of root and area-level maps; add depth only when it materially reduces task-oriented retrieval. Indexing an important child from a parent is not the same as assigning the child its own map.

## Refactoring an existing structure

Refactoring the documentation structure is a normal outcome, not a last resort. Existing files, paths, links, and committed history are evidence to assess—not constraints to preserve. When the current structure is wrong, change it: merge, move, rename, archive, or delete files as needed. Preserve information and external contracts only when they still have a current owner or a real consumer.

**Before editing**
1. Inspect the relevant documents, paths, links, implementation evidence, and real consumers.
2. Classify each relevant artifact as `keep`, `merge`, `move/rename`, `archive`, or `delete`.
3. Decide the target structure from responsibility, authority, lifecycle, and real consumers—not from path familiarity or fear of changing files.

**After deciding the target**
4. Transfer unique information to its current owner, update consumers, and remove obsolete artifacts. Do not preserve a legacy document merely because it exists, is linked, or is already committed; do not leave a redundant compatibility shell.

# Templates

## Example direct destination

```md
- [scripts/validate_context_architecture.py](scripts/validate_context_architecture.py) — Audits a repository against these conventions.
```

## Example navigation map

A document with multiple independent areas or enough size to make over-reading likely must have a concise navigation map near the beginning — roughly more than 300–400 lines, more than 2,000 words, or three or more independent functional areas. Orient it around task questions or needs and link directly to real headings; an automatic table of contents is not a substitute.

```md
## Navigation map

| If you need... | See |
| --- | --- |
| Cycle states | [Assessment Cycle](#assessment-cycle) |
| Reassessment | [Reassessment Request](#reassessment-request) |
```

## CURRENT-STATE.json format

```json
{
  "plan": "authentication.md",
  "phase": "verification",
  "status": "blocked"
}
```

`plan` and `status` are required; `phase` is optional for simple plans. Use `not_started`, `in_progress`, `blocked`, or `complete` for `status`. Keep explanations, blockers, decisions, and next steps in the linked Markdown plan or its responsible documents.

# Verification

- Verify frontmatter, names, links, references, runtime paths, and repository conventions.
- When `CURRENT-STATE.json` exists, verify that it is valid JSON, contains only `plan`, `status`, and optional `phase`, uses an allowed `status`, points to an existing Markdown plan, and is linked from the applicable `CONTEXT.md`.
- Re-read edited documents as an agent would: can it identify what to do, when to do it, what to read, what to ignore, and when it is finished?
- Use [scripts/validate_context_architecture.py](scripts/validate_context_architecture.py) to audit a repository against these conventions. Store recurring exclusions for generated, vendor-owned, or out-of-scope artifacts in a root `.contextignore`; use `--exclude` for one-off exclusions. The auditor reports actionable findings and does not modify files; review each finding with the repository owner before deciding what to change.

## Common failure patterns

- **Competing authority:** the same information is maintained in multiple documents, a parent map repeats a child map, or a new canonical document leaves a redundant legacy shell behind.
- **Hidden context:** a relevant destination is not linked from the nearest map, a root router does not identify a first entrypoint, or a navigation map is missing, too distant, points to missing anchors, or is only an automatic heading list.
- **Over-mapping:** a `CONTEXT.md` lists every file, a child map exists merely because a parent links to it, or a routine implementation folder has its own map despite being clear from the nearest parent.
- **Cascading maintenance:** a routine child change requires updates to several parent maps instead of only the nearest map, unless a parent scope or cross-folder contract changed.
- **Mixed lifecycle:** work in progress, archived material, and consolidated knowledge are combined without clear separation.
- **Duplicated state:** current state is copied into multiple Markdown files, or `CURRENT-STATE.json` grows into an inventory, decision log, or second plan.
