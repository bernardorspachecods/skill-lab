# Source Note

Source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

Date inspected: 2026-06-29

Source date: Published Sep 29, 2025 on the Anthropic engineering page; verified 2026-06-30.

Authority level: Primary Anthropic engineering guidance on context engineering.

Relevant sections inspected:

- Context engineering vs prompt engineering.
- Context retrieval and just-in-time exploration.
- Sub-agent context isolation.
- Context as finite attention budget.

Retained claims:

- Context is finite and should be actively managed.
- Context engineering includes prompts, tools, external data, message history, and runtime state.
- Just-in-time retrieval and progressive disclosure can outperform loading everything up front.
- Sub-agents can explore large context areas and return concise summaries.
- Examples should be canonical rather than numerous.

Excluded claims:

- Platform-specific details not needed by a general reusable docs package.
- Long explanations already captured as concise operating rules.

Review cadence:

Review quarterly or when updating context-management guidance.
