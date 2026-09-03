# Task Router Pattern

Use this when the human gives a task and the right workflow is not obvious.

## Goal

Help the LLM decide what kind of work is being requested before choosing context, tools, memory updates, or verification.

## Pattern

```text
Classify the request.

Return:
1. Route
2. Why this route
3. Context needed
4. Context not needed
5. First action
6. Verification method
7. Human decision points, if any
```

## Good Behavior

- The model chooses one primary route and names secondary concerns.
- The model excludes irrelevant context.
- The model asks the human only for real decisions.

## Bad Behavior

- The model says "I will inspect everything."
- The model asks the human to choose the route.
- The model starts editing before it understands risk.

## Source Trail

See `knowledge/agents/task-routing.md`.

Source IDs:

- `anthropic-building-effective-agents`
- `agentic-design-patterns`
