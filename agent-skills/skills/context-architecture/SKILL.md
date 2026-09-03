---
name: context-architecture
description: Design and maintain the information architecture of agent-facing repository documents. Use when creating, moving, splitting, merging, or restructuring context files and folders; preserve existing conventions and avoid imposing a fixed structure.
---

# Organize repository context

Organize information so an unfamiliar agent can discover the repository, its rules, its current behavior, and the relevant context for a task. Optimize for retrieval and reliable decisions, not visual neatness or a universal folder tree.

Before changing context files or folders:

1. Read the applicable repository guidance (`AGENTS.md`, `READ.md`, `CLAUDE.md`, and equivalents).
2. Inspect existing entrypoints, indexes, documentation folders, naming conventions, and the current code or tests they describe. Treat explicit local conventions as the default. If none exist, record that absence and infer from actual usage instead of inventing a taxonomy.
3. Map each relevant document's purpose, audience, authority, and lifecycle. Categories such as rules, architecture decisions, domain knowledge, workflows, source notes, examples, and temporary work are useful distinctions, not a required directory structure.
4. Identify the source of truth and any stale, duplicated, conflicting, or orphaned material. Repair, merge, or link it when safe and in scope; otherwise preserve it and explicitly report what is deferred or needs a decision. Surface meaningful conflicts instead of silently choosing a document.
5. Choose the smallest sufficient change. Extend the canonical document when the audience, authority, and lifecycle are the same. Create a new file only for a genuinely distinct responsibility; create a folder only when multiple related documents or a clear boundary justify it.
6. Make the result navigable from the repository root or the nearest existing relevant entrypoint. Use names that reveal purpose, link related documents, and preserve or repair links when moving material. Create a new root index only when it materially improves discovery.
7. Perform a targeted discovery check: trace the path from the root or nearest entrypoint to the changed material, check affected links and references, and verify that another agent could understand the reading order, authority, and distinction between durable knowledge and temporary notes.

Preserve a working local structure even when it differs from familiar patterns. Do not reorganize files for aesthetics, copy a generic documentation system into the repository, or create duplicate sources of truth. Ask before deleting or rewriting a source of truth, changing document ownership or authority, moving externally referenced or generated material, or making a broad or difficult-to-reverse restructuring.

Finish when the requested information is in the smallest appropriate location, navigation is intact, no avoidable duplicate or orphan was introduced, and the resulting structure is consistent with the repository's own conventions.
