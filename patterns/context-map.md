# Context Map Pattern

Use this when a task may require multiple docs, source files, sources, or historical notes.

## Goal

Keep the LLM focused on the smallest high-signal context.

## Pattern

```markdown
# Context Map

Task:

Current route:

Must read:

May read if needed:

Should not read:

Source of truth:

Stale or lower-authority material:

Open questions:
```

## Good Behavior

- The model reads indexes before full documents.
- The model explains why context is included.
- The model names context that should be ignored.

## Bad Behavior

- Loading every doc because it exists.
- Mixing source-backed facts with guesses.
- Treating examples as requirements.

## Source Trail

See `knowledge/context/context-selection.md` and `knowledge/foundations/context-memory-and-attention.md`.

Source IDs:

- `anthropic-effective-context-engineering`
- `anthropic-manage-tool-context`
- `anthropic-compaction`
- `agentic-design-patterns`
