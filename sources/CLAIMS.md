# Claims

This file stores reusable source-backed claims. It is not a final synthesis.

## Claim: Start With The Smallest Sufficient Workflow

Claim:
LLM workflows should start simple and add chaining, routing, parallelization, reflection, tools, or agents only when they improve reliability or outcome quality.

Source IDs:
- `anthropic-building-effective-agents`
- `agentic-design-patterns`

Confidence:
Source-backed

Applies when:
- Designing app workflows, research workflows, code workflows, or agent orchestration.

Does not apply when:
- External policy, safety, or regulatory requirements mandate a heavier process.

Implication:
Avoid turning every request into an agentic workflow.

## Claim: Context Is A Finite Attention Budget

Claim:
Relevant, well-structured context is usually more useful than large undifferentiated context.

Source IDs:
- `anthropic-effective-context-engineering`
- `anthropic-manage-tool-context`
- `anthropic-compaction`
- `agentic-design-patterns`

Confidence:
Source-backed

Applies when:
- The task has many possible files, docs, sources, tools, or historical notes.

Does not apply when:
- The task explicitly requires exhaustive review of a small source set.

Implication:
Use indexes, maps, targeted reads, and compaction.

## Claim: Grounded Work Requires Evidence Before Synthesis

Claim:
For factual or research work, the LLM should extract evidence before producing final synthesis.

Source IDs:
- `anthropic-reduce-hallucinations`
- `anthropic-effective-context-engineering`
- `anthropic-multi-agent-research-system`

Confidence:
Source-backed

Applies when:
- Answering source-sensitive questions, analyzing long documents, or building durable knowledge.

Does not apply when:
- The task is explicitly creative or low-stakes and does not depend on factual accuracy.

Implication:
Separate source notes, claim cards, questions, and synthesis.

## Claim: Human Checkpoints Are For Judgment, Not Routine Discovery

Claim:
The LLM should ask the human when decisions are high-risk, ambiguous, irreversible, private-context dependent, or outside available evidence; it should not ask for context it can safely discover.

Source IDs:
- `anthropic-building-effective-agents`
- `anthropic-claude-code-best-practices`
- `agentic-design-patterns`

Confidence:
Source-backed

Applies when:
- Agents work in apps, codebases, research systems, or documentation workflows.

Does not apply when:
- The human explicitly requests a collaborative brainstorming mode.

Implication:
Questions should include options, tradeoffs, and a recommendation when possible.

## Claim: Tools Are Part Of Context Engineering

Claim:
Tool definitions, tool results, schemas, names, errors, and return shapes influence agent behavior and consume context.

Source IDs:
- `anthropic-writing-tools-for-agents`
- `anthropic-tool-use-overview`
- `anthropic-manage-tool-context`

Confidence:
Source-backed

Applies when:
- Designing tools or using tools in long-running agent workflows.

Does not apply when:
- The task has no external-state dependency and can be answered directly.

Implication:
Design tools as model-facing contracts and keep outputs concise, grounded, and metadata-rich.
