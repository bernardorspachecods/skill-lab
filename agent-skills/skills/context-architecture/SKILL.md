---
name: context-architecture
description: Build and maintain repository context and documentation structures. Use when creating, restructuring, or cleaning context files and folders.
---

# Operating posture

Refactoring the documentation structure is a normal outcome, not a last resort. Existing files, paths, links, and committed history are evidence to assess—not constraints to preserve. When the current structure is wrong, change it: merge, move, rename, archive, or delete files as needed. Preserve information and external contracts only when they still have a current owner or a real consumer.

# Core principles

- Avoid duplicating information between documents; keep necessary repetition minimal.
- Document information that helps an agent navigate the repository or make decisions. Omit details that are already clear from the nearest authoritative source.

# Rules

1. **Each document must have a specific purpose.** Split a document only when a genuinely distinct purpose, audience, authority, or lifecycle justifies it.
2. **When writing be as concise and direct as possible** - maximize token efficiency and content quality at the same time
3. **Keep context discoverable.** - an agent shouldn't have to guess where things are. link the documents. think of it as roads in a city, every building should have a road that leads to it
4. **Separate durable context from temporary work.**
5. **Keep related material distinguishable by purpose and lifecycle** - follow local conventions rather than imposing a universal folder structure. Work in progress, archived work, and consolidated work should preferably be kept separate.
6. **Do not repeat rules that an agent will read in skill** - the rules written for a repo should be specific to that repo, do not include general behavioral rules because agents will read those from skills anyways
7. **When the structure is wrong, refactor it** - do not keep a legacy document merely because it exists, is linked, or is already committed. Update consumers and remove the obsolete artifact when its unique information has been transferred. “Propose a refactor” is not sufficient when the task is to clean or restructure the documentation.
8. **Decide the target structure before editing** - classify each relevant artifact as keep, merge, move/rename, archive, or delete. The classification must be resolved by responsibility, authority, lifecycle, and real consumers—not by path familiarity or fear of changing files.

# Structure

- **At the repository root:** always keep `CONTEXT.md`. In addition to its direct top-level destinations, it should contain a short task-intent router that points each common request type to its first area of investigation. Create `AGENTS.md` only when the repository has specific behavioral rules for agents; do not create an empty or placeholder file.
- **In each relevant folder:** give the folder its own `CONTEXT.md`. Do not require context files in generated, temporary, dependency, or otherwise irrelevant folders unless they need durable guidance.
- **When `AGENTS.md` exists:** it must contain an explicit link to the `CONTEXT.md` that maps its same scope. Keep the link visible and actionable near the beginning of the file so an agent can move from local rules to repository orientation. For a root `AGENTS.md`, link the root `CONTEXT.md`; for a nested `AGENTS.md`, link the nearest applicable `CONTEXT.md`.
- **Keep context local and avoid cascading updates:** the `CONTEXT.md` of a parent folder should describe its own scope, stable boundaries, and entrypoints, not every detail inside child folders. Changes inside a child folder should normally update only the nearest `CONTEXT.md`, unless they change the parent's scope, direct structure, or cross-folder contract.

# `CONTEXT.md` format and use

- List relevant direct destinations as `[path](path) — specific responsibility`. The root `CONTEXT.md` must additionally contain one concise task-intent router in a compact table with the request type, first area to open, and likely dependencies. Keep the router limited to first-entry classification; do not turn it into an exhaustive application map or a duplicate of local context files. If descriptions overlap, inspect the contents and resolve any duplicated responsibility.
- Use the root router to choose one primary entrypoint for the task, then read that area's nearest relevant `CONTEXT.md` and only task-relevant links. The router chooses the first door; the local context chooses concrete files; the owner document explains the intended rule or decision; and code, migrations, or scripts confirm current behavior.
- Record repository-specific routing decisions in the root router when they matter, including the appropriate starting point for cross-area work, broad or ambiguous requests, localized bugs, and disagreements between documentation and implementation. Do not impose universal destinations or authority rules when the repository has not established them.
- Update the map or router only when a destination, responsibility, boundary, task category, or primary entrypoint changes; routine edits within an existing responsibility need no map update.

Example entry:

```md
- [user_preferences.md](user_preferences.md) — User preferences for the agent's tone in chats.
```

# Terminology

These files have fixed responsibilities:

- `README.md` is a GitHub-facing public artifact only. Never reference it from application code or application documentation, and never use it to record internal application context. Update it only for public presentation when the user explicitly requests it; record all other application information in the appropriate `CONTEXT.md` or canonical document.
- If a `README.md` is an internal legacy manual or router while `CONTEXT.md` is canonical, migrate any still-needed information, update its consumers, and remove the internal router. Do not preserve it as a second entrypoint merely because it still works.
- `AGENTS.md` for repository-specific behavioral rules that do not repeat general skill guidance. It is not a general repository index or catch-all document; do not use it for product vision, architecture, current state, plans, or general documentation. When present, it must also link explicitly to the `CONTEXT.md` for its scope so agents can continue from local rules to repository orientation.
- `CONTEXT.md` for the map and orientation of a folder.

When the repository needs these distinctions, prefer the following names:

- `PLAN.md` for the main plan at the repository root; use `PLAN_<name>.md` for subsequent plans.
- `working/` for working files and active state.
- `reference/` for archived files that might still be useful as backup or for reference.
- `research/` for files that support research and are still in use; move them to `reference/` when they are no longer in use.

# Maintenance

When cleaning existing context, remove duplicated, stale, vague, or decorative material. Preserve information that changes future decisions, and keep necessary uncertainty visible. Do not reorganize a working local structure solely for neatness or word count. Do not alter authoritative documentation merely to save tokens.

Reorganize when it repairs authority, discoverability, lifecycle, duplication, or obsolete routing, even if the old structure still technically works. Authority comes from the document's current responsibility and consumers, not from its age, location, or commit history. A legacy file that only duplicates, redirects to, or competes with the canonical structure should normally be merged or deleted after references are updated.

# Verification

After editing, verify frontmatter, names, links, references, runtime paths, and repository conventions. Re-read the edited documents as an agent would: can it identify what to do, when to do it, what to read, what to ignore, and when it is finished? Run realistic examples or relevant checks when they can reveal a behavioral regression.

# Bad practices to look out for
1. You have to find your way through the documents, instead of being guided by the documents - violates rule 3
2. You have to update 2+ separate files with the same information or the documents contain overlapping responsibilities  - violates rule 1 and the first core principle
3. A parent `CONTEXT.md` repeats the full contents of child `CONTEXT.md` files - violates rule 1, the first core principle, and Structure.
4. A routine change inside a child folder requires updating several parent `CONTEXT.md` files - violates the local context principle.
5. A document contains work in progress, archived material, and consolidated knowledge without clear separation - violates rules 4 and 5.
6. A relevant document exists but is not linked from the nearest `CONTEXT.md` - violates rule 3.
7. A `CONTEXT.md` lists every file manually and becomes stale after normal development - violates rule 3 and the local context principle.
8. A legacy document is preserved only because it already exists or is linked - violates the refactoring posture and rule 8.
9. A new canonical document is added while a redundant legacy document remains as a compatibility shell - violates rule 1 and creates competing authority.
