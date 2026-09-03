# Source Index

This is the canonical source registry. Use it to avoid repeating sources, understand scope, and trace principles back to source notes.

Each source has a stable ID. Encyclopedia files should reference source IDs in `Source Trail` sections and link to source notes when deeper inspection is needed.

## Local Sources

### `agentic-design-patterns`

Title: Agentic Design Patterns

Path: `sources/Agentic-Design-Patterns.pdf`

Source note: `sources/notes/2026-06-29-agentic-design-patterns.md`

Source type: PDF / broad practical reference

Authority level: Broad secondary/practical reference for agentic design patterns.

Scope:

- Context engineering.
- Prompt chaining.
- Routing.
- Parallelization.
- Reflection.
- Tool use.
- Planning.
- Multi-agent collaboration.
- Memory management.
- Human-in-the-loop.
- RAG / Agentic RAG.
- Evaluation and monitoring.

Limitations:

- Contains framework/vendor-specific implementation material.
- Repeats concepts across chapters.
- Current source note should be improved with page/section locators before supporting very specific claims.

## Anthropic Engineering Sources

### `anthropic-building-effective-agents`

Title: Building Effective Agents

URL: https://www.anthropic.com/engineering/building-effective-agents

Source note: `sources/notes/2026-06-29-anthropic-building-effective-agents.md`

Source type: Engineering article

Authority level: Primary vendor engineering guidance for agent workflow design.

Scope:

- Simple workflows before agents.
- Prompt chains.
- Routing.
- Parallelization.
- Orchestrator-worker patterns.
- Evaluator-optimizer patterns.
- Tool design basics.

Limitations:

- Vendor-specific perspective.
- Should not be treated as a complete theory of agents.

### `anthropic-effective-context-engineering`

Title: Effective Context Engineering for AI Agents

URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

Source note: `sources/notes/2026-06-29-anthropic-effective-context-engineering.md`

Source type: Engineering article

Authority level: Primary vendor engineering guidance on context management.

Scope:

- Context as an attention budget.
- Context engineering beyond prompt wording.
- Tool, history, external data, and runtime state as context.
- Progressive disclosure.
- Just-in-time retrieval.
- Sub-agent exploration.

Limitations:

- Focused on agent context strategy, not a general cognitive theory of LLMs.

### `anthropic-writing-tools-for-agents`

Title: Writing Effective Tools for AI Agents

URL: https://www.anthropic.com/engineering/writing-tools-for-agents

Source note: `sources/notes/2026-06-29-anthropic-writing-tools-for-agents.md`

Source type: Engineering article

Authority level: Primary vendor engineering guidance on agent-facing tool design.

Scope:

- Tool names, descriptions, schemas, and return values.
- Tool evals.
- Token efficiency.
- Redundant tool calls.
- Tool-call metrics.

Limitations:

- Focused on tool design, not broader security or governance.

### `anthropic-claude-code-best-practices`

Title: Claude Code: Best Practices for Agentic Coding

URL: https://www.anthropic.com/engineering/claude-code-best-practices

Source note: `sources/notes/2026-06-29-anthropic-claude-code-best-practices.md`

Source type: Engineering article

Authority level: Primary vendor guidance for coding agents.

Scope:

- Project-specific memory/instructions.
- Testing and build commands.
- Visual checks.
- Small reviewable changes.
- Human control over high-impact decisions.

Limitations:

- Claude Code specific; translate principles before generalizing.

### `anthropic-multi-agent-research-system`

Title: How Anthropic Built a Multi-Agent Research System

URL: https://www.anthropic.com/engineering/multi-agent-research-system

Source note: `sources/notes/2026-06-29-anthropic-multi-agent-research-system.md`

Source type: Engineering case study

Authority level: Primary vendor case study for multi-agent research.

Scope:

- Parallel exploration.
- Orchestrator-worker research.
- Exploration vs synthesis separation.
- Cost and coordination tradeoffs.

Limitations:

- A case study, not a universal architecture recommendation.

## Anthropic Documentation Sources

### `anthropic-prompt-engineering`

Title: Prompt Engineering Overview

URL: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview

Source note: `sources/notes/2026-06-29-anthropic-docs-prompt-engineering.md`

Source type: Vendor docs

Authority level: Primary vendor docs for prompt design.

Scope:

- Clear instructions.
- Context.
- Examples.
- Structured output.
- Iteration.

Limitations:

- Basic prompt guidance; not sufficient alone for agent workflow design.

### `anthropic-test-evaluation`

Title: Define Success Criteria and Build Evaluations

URL: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests

Source note: `sources/notes/2026-06-29-anthropic-docs-test-evaluation.md`

Source type: Vendor docs

Authority level: Primary vendor docs for evaluation.

Scope:

- Success criteria.
- Realistic eval examples.
- Failure modes.
- Regression tracking.

Limitations:

- Does not replace product-specific or domain-specific evaluation design.

### `anthropic-reduce-hallucinations`

Title: Reduce Hallucinations

URL: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

Source note: `sources/notes/2026-06-29-anthropic-docs-hallucination-reduction.md`

Source type: Vendor docs

Authority level: Primary vendor docs for factuality guardrails.

Scope:

- Grounding answers in sources.
- Saying when the model does not know.
- Evidence and citations.
- Uncertainty preservation.

Limitations:

- Practical guardrail guidance, not a full explanation of hallucination mechanisms.

### `anthropic-tool-use-overview`

Title: Tool Use Overview

URL: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

Source note: `sources/notes/2026-06-29-anthropic-docs-tool-use.md`

Source type: Vendor docs

Authority level: Primary vendor docs for tool-use mechanics.

Scope:

- Model-selected tool calls.
- Tool schemas.
- Tool results as context.

Limitations:

- Mechanics-focused; should be paired with tool-design guidance.

### `anthropic-manage-tool-context`

Title: Manage Tool Context

URL: https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context

Source note: `sources/notes/2026-06-29-anthropic-docs-tool-context.md`

Source type: Vendor docs

Authority level: Primary vendor docs for tool context pressure.

Scope:

- Tool definitions consuming context.
- Loading tools on demand.
- Batching repetitive tool chains.
- Removing or compacting stale tool results.

Limitations:

- Platform-specific implementation details may not transfer directly.

### `anthropic-compaction`

Title: Compaction

URL: https://platform.claude.com/docs/en/build-with-claude/compaction

Source note: `sources/notes/2026-06-29-anthropic-docs-compaction.md`

Source type: Vendor docs

Authority level: Primary vendor docs for long-context continuity.

Scope:

- Replacing old history with continuity summaries.
- Preserving state, next steps, learnings, decisions, and source references.

Limitations:

- Platform-specific compaction details may vary.

### `anthropic-agent-skills-best-practices`

Title: Agent Skills Best Practices

URL: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Source note: `sources/notes/2026-06-29-anthropic-docs-skills-best-practices.md`

Source type: Vendor docs

Authority level: Primary vendor docs for packaging reusable skills.

Scope:

- Focused skills.
- Triggers.
- Concise instructions.
- Examples only when useful.

Limitations:

- Relevant when packaging knowledge into skills; not central to the encyclopedia itself.

## Known Source Gaps

Do not create durable encyclopedia guidance in these areas without adding better sources:

- Human-AI collaboration research: trust calibration, overreliance, delegation, interruption cost, team workflows.
- LLM internals: hallucination mechanisms, calibration, sycophancy, context-window failure modes, reasoning limits.
- Security: prompt injection, tool-use threat models, data leakage, privacy, governance.
- Regulated domains: medical, legal, finance, education assessment, enterprise compliance.
- Master-thesis methodology: university rules, literature review methods, citation standards, research methodology.
