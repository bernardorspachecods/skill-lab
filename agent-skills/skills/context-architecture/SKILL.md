---
name: context-architecture
description: Organize repository context and documentation structure. Use when creating or restructuring context files and folders.
---


# Rules

1. **Each document must have a specific purpose** - if it combines many purposes at once considering splitting
2. **There should only be one source of truth.** - if there is duplication clean it, if there is contradictory info talk it out with the user
3. **When writing be as concise and direct as possible** - maximize token efficiency and content quality at the same time
4. **Keep context discoverable.** - an agent shouldn't have to guess where things are. link the documents. think of it as roads in a city, every building should have a road that leads to it
5. **Separate durable context from temporary work.**
6. **Keep things tidy and organized** - folders and files should always be organized and follow a consistent structure within the folder. Work in progress, archived work, and consolidated work should preferably be kept separate.
7. **Just because it's written and committed doesn't make it correct** - If the repo docs structure is incorrect propose changes. By the end we should have all the core info intact, but better organized and with 0 duplicated rules, knowledge…
8. **Do not repeat rules that an agent will read in skill** - the rules written for a repo should be specific to that repo, do not include general behavioral rules because agents will read those from skills anyways

# Structure

- **At the repository root:** use `README.md` for the public introduction, installation, and general usage; `AGENTS.md` for repository-specific behavioral rules that do not repeat general skill guidance; and `CONTEXT.md` for the map and orientation of the root folder.
- **In each relevant folder:** give the folder its own `CONTEXT.md`, responsible for its purpose, organization, and orientation. Do not require context files in generated, temporary, dependency, or otherwise irrelevant folders unless they need durable guidance.
- **Keep context local and avoid cascading updates:** the `CONTEXT.md` of a parent folder should describe its own scope, stable boundaries, and entrypoints, not every detail inside child folders. Changes inside a child folder should normally update only the nearest `CONTEXT.md`, unless they change the parent's scope, direct structure, or cross-folder contract.


# Bad practices to look out for
1. You have to find your way through the documents, instead of being guided by the documents - violates rule 4
2. You have to update 2+ separate files with the same information when updating the repo documentation - violates rules 1 and 2
3. A parent `CONTEXT.md` repeats the full contents of child `CONTEXT.md` files - violates rules 1, 2, and Structure.
4. A routine change inside a child folder requires updating several parent `CONTEXT.md` files - violates the local context principle.
5. A document contains work in progress, archived material, and consolidated knowledge without clear separation - violates rules 5 and 6.
6. A relevant document exists but is not linked from the nearest `CONTEXT.md` - violates rule 4.
7. `README.md`, `AGENTS.md`, and `CONTEXT.md` contain overlapping responsibilities - violates rule 1 and the root Structure.
8. A `CONTEXT.md` lists every file manually and becomes stale after normal development - violates local context and discoverability.
