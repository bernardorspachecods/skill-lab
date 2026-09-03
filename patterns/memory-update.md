# Memory Update Pattern

Use this near the end of a substantial task.

## Goal

Decide what should become durable memory and what should be discarded.

## Pattern

```markdown
# Memory Update

Durable facts learned:

Decisions made:

Commands or workflows discovered:

Pitfalls worth preserving:

Open questions:

Temporary notes to discard:

Docs to update:
```

## Good Behavior

- The model updates memory only when future behavior changes.
- Temporary debugging details are discarded.
- Open questions stay separate from conclusions.

## Bad Behavior

- Saving raw transcripts.
- Updating docs to look productive.
- Duplicating the same rule in multiple files.

## Source Trail

See `knowledge/memory/docs-as-memory.md` and `knowledge/memory/durable-vs-temporary.md`.

Source IDs:

- `anthropic-effective-context-engineering`
- `anthropic-compaction`
- `agentic-design-patterns`
