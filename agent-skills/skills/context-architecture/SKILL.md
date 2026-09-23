---
name: context-architecture
description: Build and maintain repository context and documentation structures. Use when creating, restructuring, or cleaning context files and folders.
---

# Operating posture

Refactoring the documentation structure is a normal outcome, not a last resort. Existing files, paths, links, and committed history are evidence to assess—not constraints to preserve. When the current structure is wrong, change it: merge, move, rename, archive, or delete files as needed. Preserve information and external contracts only when they still have a current owner or a real consumer.

# Core principles

- Avoid duplicating information between documents; keep necessary repetition minimal.
- Document information that helps an agent navigate the repository or make decisions. Omit details that are already clear from the nearest authoritative source.
- Optimize context for task-level retrieval: keep decision-relevant information coherent in its canonical document and avoid unnecessary reads or prose.

# Rules

1. **Each document must have a specific purpose.** Split a document only when a genuinely distinct purpose, audience, authority, or lifecycle justifies it.
2. **When writing be as concise and direct as possible** - maximize token efficiency and content quality at the same time
3. **Keep context discoverable.** - an agent shouldn't have to guess where things are. link the documents. think of it as roads in a city, every building should have a road that leads to it
4. **Separate durable context from temporary work.**
5. **Keep related material distinguishable by purpose and lifecycle** - follow local conventions rather than imposing a universal folder structure. Work in progress, archived work, and consolidated work should preferably be kept separate.
6. **Do not repeat general skill behavior in repository docs** - repository rules should add only local conventions, owners, map names, workflows, or exceptions that the skill cannot know.
7. **When the structure is wrong, refactor it** - do not keep a legacy document merely because it exists, is linked, or is already committed. Update consumers and remove the obsolete artifact when its unique information has been transferred. “Propose a refactor” is not sufficient when the task is to clean or restructure the documentation.
8. **Decide the target structure before editing** - classify each relevant artifact as keep, merge, move/rename, archive, or delete. The classification must be resolved by responsibility, authority, lifecycle, and real consumers—not by path familiarity or fear of changing files.

# Repository structure

- **At the repository root:** always keep `CONTEXT.md`. In addition to its direct top-level destinations, it must contain one short task-intent router that points common request types to their first area of investigation. Create `AGENTS.md` only when the repository has specific behavioral rules for agents; do not create an empty or placeholder file.
- **At selected area boundaries:** give a folder its own `CONTEXT.md` only when it is an ownership boundary, a probable agent entrypoint for independent work, an independent documentation area, or contains rules that cannot be inferred quickly from its parent map. Treat these as a small set of parent/area maps, not as one map per directory or per nesting level.
- **Inherit by default:** a folder without its own `CONTEXT.md` uses the nearest ancestor map. A parent map may link directly to a child folder, file, input, output, or script; that link does not by itself justify creating a child `CONTEXT.md`. Create a child map only when the child has its own durable responsibility, entrypoint, documentation area, or local rules. Code internals, generated, temporary, dependency, and otherwise technical folders normally inherit without a context file.
- **At an active context boundary:** an optional `CURRENT-STATE.json` may sit beside the applicable `CONTEXT.md` when there is a plan whose implementation an agent may need to resume. Do not create one per folder, or create a context boundary merely to house a state file.
- **When `AGENTS.md` is maintained by the team:** it must contain an explicit link to the `CONTEXT.md` that maps its same scope. Keep the link visible and actionable near the beginning of the file. For a root `AGENTS.md`, link the root `CONTEXT.md`; for a nested `AGENTS.md`, link the nearest applicable `CONTEXT.md`. Generated, vendor-owned, or tool-regenerated `AGENTS.md` files are excluded from this rule and remain oriented by the parent map.
- **Keep context local and avoid cascading updates:** a parent `CONTEXT.md` describes its own scope, stable boundaries, and entrypoints, not every detail inside child folders. Changes inside a child folder should normally update only the nearest `CONTEXT.md`, unless they change the parent's scope, direct structure, or cross-folder contract.

# File responsibilities

- `README.md` is a public GitHub-facing artifact, not internal application context. If it is an internal legacy manual or router while another document is canonical, migrate the needed information and consumers to the appropriate owner, then remove the obsolete material.
- Team-maintained `AGENTS.md` files contain repository-specific behavioral rules that do not repeat general skill guidance. They are not general repository indexes or catch-all documents; do not use them for product vision, architecture, current state, plans, or general documentation. Generated, vendor-owned, or tool-regenerated files are exceptions and should be excluded from this contract.
- `CONTEXT.md` maps and orients its folder. It links to relevant direct destinations and their specific responsibilities.
- `CURRENT-STATE.json` is an optional machine-readable resume pointer for the same scope as a `CONTEXT.md`. It records only the active plan, its coarse status, and an optional phase; it is not an implementation inventory, decision record, rationale, or place for next-step prose.
- Prefer `PLAN.md` for the main plan at the repository root and `PLAN_<name>.md` for subsequent plans. Use `research/` for research that is still in use and `reference/` for archived or consultative material.

## Choosing the granularity

Before creating a nested `CONTEXT.md`, ask:

1. Does this folder represent a distinct responsibility or ownership boundary?
2. Is it a likely first entrypoint for a class of tasks rather than an implementation detail?
3. Does it contain durable local rules or an independent documentation area?

If the answer is no to all three, keep the folder under its nearest parent map. Prefer a shallow hierarchy of root and area-level maps; add depth only when it materially reduces task-oriented retrieval. A parent map should index the child when the child is important, but indexing is not the same as assigning the child its own map.

# Documentation layers

- In `CONTEXT.md`, list relevant direct destinations as Markdown links followed by their specific responsibility. The root `CONTEXT.md` must additionally contain one concise task-intent router in a compact table with the request type, first area to open, and likely dependencies. Keep it limited to first-entry classification; do not turn it into an exhaustive application map or a duplicate of local context files.
- The root router records first entrypoints; a local `CONTEXT.md` records concrete destinations; an owner document records intended rules; and code, migrations, or scripts confirm current behavior. Keep these responsibilities distinct and link the layers where appropriate.
- When a scope has an active plan to resume, its `CONTEXT.md` should link to the adjacent `CURRENT-STATE.json`. Read the state file as a pointer, then follow its `plan` field for detail; do not copy its `status` or `phase` into multiple Markdown documents.
- A parent `CONTEXT.md` may link directly to code, outputs, inputs, or other artifacts without requiring a child `CONTEXT.md`. If a file or folder is a recurring retrieval target, reference it from the nearest appropriate application or documentation context; create a child context only when it is an independent boundary.
- Record repository-specific routing decisions in the root router when they matter, including cross-area work, broad or ambiguous requests, localized bugs, and disagreements between documentation and implementation. Do not impose universal destinations or authority rules when the repository has not established them.
- A document with multiple independent areas or enough size to make over-reading likely must have a concise navigation map near the beginning when it has roughly more than 300–400 lines, more than 2,000 words, or three or more independent functional areas. Orient the map around task questions or needs and link directly to real headings; do not use an automatic table of contents as a substitute.
- The skill defines progressive retrieval in general terms. When a repository uses navigation maps, its `AGENTS.md` should add only the local adaptation: which files act as maps, how owners are chosen, and which repository-specific exceptions apply. It may state, for example, that this repository starts at `CONTEXT.md` and uses each document's `Navigation map` according to its local conventions.

Example direct destination:

```md
- [user_preferences.md](user_preferences.md) — User preferences for the agent's tone in chats.
```

Example navigation map:

```md
## Navigation map

| If you need... | See |
| --- | --- |
| Cycle states | [Assessment Cycle](#assessment-cycle) |
| Reassessment | [Reassessment Request](#reassessment-request) |
```

## Current state format

Keep `CURRENT-STATE.json` small and stable. The `plan` path is relative to the JSON file, and the referenced plan must exist.

```json
{
  "plan": "authentication.md",
  "phase": "verification",
  "status": "blocked"
}
```

`plan` and `status` are required; `phase` is optional for simple plans. Use `not_started`, `in_progress`, `blocked`, or `complete` for `status`. Omit `phase` when the plan does not have meaningful phases. Keep explanations, blockers, decisions, and next steps in the linked Markdown plan or its responsible documents.

# Verification

- Verify frontmatter, names, links, references, runtime paths, and repository conventions.
- When `CURRENT-STATE.json` exists, verify that it is valid JSON, contains only `plan`, `status`, and optional `phase`, uses an allowed `status`, points to an existing Markdown plan, and is linked from the applicable `CONTEXT.md`.
- Re-read edited documents as an agent would: can it identify what to do, when to do it, what to read, what to ignore, and when it is finished?
- Use [scripts/validate_context_architecture.py](scripts/validate_context_architecture.py) to audit a repository against these conventions. Store recurring exclusions for generated, vendor-owned, or out-of-scope artifacts in a root `.contextignore`; use `--exclude` for one-off exclusions. The auditor reports actionable findings and does not modify files; review each finding with the repository owner before deciding what to change.

# Bad practices to look out for
1. You have to find your way through the documents, instead of being guided by the documents - violates rule 3
2. You have to update 2+ separate files with the same information or the documents contain overlapping responsibilities  - violates rule 1 and the first core principle
3. A parent `CONTEXT.md` repeats the full contents of child `CONTEXT.md` files - violates rule 1, the first core principle, and Repository structure.
4. A routine change inside a child folder requires updating several parent `CONTEXT.md` files - violates the local context principle.
5. A document contains work in progress, archived material, and consolidated knowledge without clear separation - violates rules 4 and 5.
6. A relevant document exists but is not linked from the nearest `CONTEXT.md` - violates rule 3.
7. A `CONTEXT.md` lists every file manually and becomes stale after normal development - violates rule 3 and the local context principle.
8. A legacy document is preserved only because it already exists or is linked - violates the refactoring posture and rule 8.
9. A new canonical document is added while a redundant legacy document remains as a compatibility shell - violates rule 1 and creates competing authority.
10. A document that needs selective retrieval has no task-oriented navigation map - violates Documentation layers.
11. A navigation map is only an automatic heading list or points to missing anchors - violates discoverability and Documentation layers.
12. A `CONTEXT.md` is created merely because a folder contains files or is linked from a parent map, without an independent ownership, entrypoint, documentation, or local-rules boundary - violates Repository structure and the inheritance rule.
13. A routine implementation subfolder has its own `CONTEXT.md` even though the nearest parent map already orients the work - violates the granularity rule and increases retrieval cost.
14. Current state is copied into several Markdown files instead of being read from one applicable `CURRENT-STATE.json` - violates single ownership and increases drift.
15. `CURRENT-STATE.json` grows into an implementation inventory, decision log, or second plan - violates file responsibilities and creates competing authority.
