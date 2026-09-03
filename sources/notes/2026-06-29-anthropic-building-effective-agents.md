# Source Note

Source: https://www.anthropic.com/engineering/building-effective-agents

Date inspected: 2026-06-29

Source date: Published Dec 19, 2024 on the Anthropic engineering page; verified 2026-06-30.

Authority level: Primary Anthropic engineering guidance on agent patterns.

Relevant sections inspected:

- When to use agents.
- Building blocks, workflows, and agents.
- Prompt chaining.
- Routing.
- Parallelization.
- Orchestrator-workers.
- Evaluator-optimizer.
- Tool design guidance.

Retained claims:

- Start with the simplest solution and add complexity only when it measurably improves outcomes.
- Workflows are predefined paths; agents dynamically direct their own process and tool use.
- Prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer are practical composable patterns.
- Tool interfaces should be clear and documented for the model, not only for humans.
- Agents need grounding from environment feedback and tool results.

Excluded claims:

- Implementation details tied to a specific model release.
- Examples not needed for this repo's reusable operating guidance.

Review cadence:

Review quarterly or when Anthropic updates agent workflow guidance.
