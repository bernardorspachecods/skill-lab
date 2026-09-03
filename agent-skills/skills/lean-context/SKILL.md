---
name: lean-context
description: Simplify and clarify agent-facing skills and repository context documents by removing duplication, stale guidance, unnecessary process, and avoidable ambiguity while preserving behavior-changing information. Invoke manually for cleanup.
---

# Keep context lean

Use this skill for deliberate cleanup of skills, `AGENTS.md`, `READ.md`, `CLAUDE.md`, and other Markdown documents that agents consume. Optimize for the smallest sufficient context and clearest possible decisions, not for the lowest word count.

Before editing:

1. Read the applicable repository guidance and define the cleanup scope.
2. Inventory the documents in scope, their links, audience, authority, lifecycle, and existing source of truth. Read related documents together when their instructions may overlap.
3. Classify each passage as behavior-changing guidance, necessary context, useful example, duplicate, stale claim, vague instruction, temporary note, or decorative prose.
4. Consolidate each meaning into one canonical location. Remove repetition, merge overlapping documents, and replace secondary copies with precise links or pointers when that preserves discoverability.
5. Rewrite vague or conflicting guidance into direct instructions with clear conditions, actions, and completion criteria. Make unavoidable uncertainty explicit instead of hiding it.
6. Preserve constraints, edge cases, evidence, examples, and guardrails when removing them would change behavior. Do not add process merely to make the documents look systematic.

Work in small related groups and verify each group before broadening the cleanup. Ask before deleting or rewriting a source of truth, changing the meaning or ownership of a document, or making a broad and difficult-to-reverse change.

After editing, verify frontmatter, names, links, references, runtime paths, and repository conventions. Re-read the cleaned documents as an agent would: can it identify what to do, when to do it, what to read, what to ignore, and when it is finished? Run realistic examples or relevant checks when they can reveal a behavioral regression.

Report what was removed, merged, clarified, preserved, deferred, and what the verification does or does not prove. Leave unresolved conflicts and irreducible ambiguity visible.

Example:

```text
$lean-context Limpa as skills desta repo, reduz duplicação e mantém todas as regras que alteram o comportamento do agente.
```
