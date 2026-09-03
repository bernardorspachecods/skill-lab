# App Workflow Audit Pattern

Use this when giving this repo to an agent that will work inside an existing app.

## Goal

Help the agent design an app-specific LLM workflow without copying this encyclopedia into the app as bureaucracy.

## Pattern

```markdown
# App Workflow Audit

Existing docs:

Existing prompts or agent instructions:

Existing memory files:

Existing review / verification practices:

Existing source indexes:

What already works:

Duplicated or stale material:

Missing behavior rules:

Recommended local workflow:

First safe change:
```

## Good Behavior

- The agent preserves useful existing systems.
- The agent adapts principles to the app.
- The agent creates a small local entrypoint only if it helps future sessions.

## Bad Behavior

- Copying this repo wholesale into the app.
- Replacing working docs with generic templates.
- Building a workflow that hides real product decisions from the human.

## Source Trail

See `knowledge/agents/task-routing.md`, `knowledge/context/context-selection.md`, and `knowledge/memory/docs-as-memory.md`.

Source IDs:

- `anthropic-claude-code-best-practices`
- `anthropic-effective-context-engineering`
- `anthropic-building-effective-agents`
- `agentic-design-patterns`
