# LLM Field Manual

A source-grounded encyclopedia for LLM behavior and human-AI workflows.

This repo is a knowledge base, not an installable product, prompt pack, or rigid workflow framework. Its purpose is to educate humans and LLM agents about how competent LLM work should behave across apps, refactors, research workflows, documentation-heavy work, and long-context tasks.

The core question is:

> Given a human request, how should an LLM decide what to read, what to do, what to ask, what to verify, what to remember, and what to discard?

## How To Use This Repo

Use the encyclopedia by topic. Read only the topic that fits the task.

- Use `knowledge/foundations/` to understand LLM capabilities, limits, uncertainty, context, and memory.
- Use `knowledge/context/` to decide what information belongs in the active context.
- Use `knowledge/agents/` to route tasks, use tools, plan, delegate, and stop.
- Use `knowledge/collaboration/` to decide when the human should be asked or protected from unnecessary questions.
- Use `knowledge/memory/` to decide what should become durable documentation.
- Use `knowledge/verification/` to ground claims, review work, and avoid hallucinations.
- Use `knowledge/research-workflows/` for source-to-synthesis and second-brain workflows.
- Use `patterns/` for reusable thinking structures. They are teaching instruments, not mandatory forms.
- Use `examples/` to see good and bad LLM behavior in realistic scenarios.
- Use `sources/` to inspect where principles came from and avoid reusing the same source blindly.

## Start By Task

| Situation | Start with | Then use |
| --- | --- | --- |
| A human gives a broad or ambiguous task | `knowledge/agents/task-routing.md` | `patterns/task-router.md` |
| An agent must choose what context to read | `knowledge/context/context-selection.md` | `patterns/context-map.md` |
| A task may create durable project knowledge | `knowledge/memory/durable-vs-temporary.md` | `patterns/memory-update.md` |
| The output must be factual or source-grounded | `knowledge/verification/grounding-and-confidence.md` | `patterns/verification-plan.md` |
| An app needs its own LLM workflow | `knowledge/agents/app-local-workflows.md` | `patterns/app-workflow-audit.md` |
| A research source must become reusable knowledge | `knowledge/research-workflows/source-to-synthesis.md` | `patterns/research-source-note.md` |
| You want to see failure modes | `examples/llm-behavior-failures.md` | Relevant knowledge topic |

## Information Architecture

```text
knowledge/
  foundations/          # how LLMs behave, fail, and use context
  context/              # context selection, long documents, compaction
  agents/               # routing, workflows, tools, orchestration
  collaboration/        # human checkpoints, questions, handoffs
  memory/               # docs as memory, durable vs temporary notes
  verification/         # grounding, confidence, review, evals
  research-workflows/   # source notes, claims, synthesis

patterns/               # compact operational patterns
examples/               # filled examples and anti-examples
sources/                # source index, source notes, claims, evidence map
maintenance/            # quality criteria and validation policy
```

## Editorial Standard

Each durable topic should teach behavior, not just describe concepts:

- what the LLM should do;
- what the LLM should not do;
- common pitfalls and symptoms;
- when to ask the human;
- how to verify;
- where the idea comes from.

The repo should stop growing when new material is redundant, weakly sourced, or decorative.

## Source Scope

The current source base is strongest for Anthropic-style agent practice, context engineering, tool use, hallucination reduction, evaluation, coding-agent workflows, and research workflows.

It is not yet a general academic source base for human-computer interaction, cognitive science, AI safety, regulated-domain governance, or master-thesis methodology. Add primary sources before turning those areas into durable advice.

## Maintenance Rule

If a file does not help a future LLM or human make a better decision, shorten it, move it to an example, or delete it.
