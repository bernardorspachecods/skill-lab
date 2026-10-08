---
name: research
description: Conduct rigorous web research matching source quality, evidence, corroboration, synthesis, and uncertainty to the stakes. Use whenever the user invokes `$research`, asks for sourced or verified findings that need multiple sources, comparison, or an auditable evidence trail, a durable plan assigns a research unit, or a research phase is dispatched to you.
---

# Research

Two kinds of agent use this skill: an **orchestrator** that runs the research, and **phase agents** that each do one phase of it. The phases are split across agents on purpose, so the agent that checks the work did not produce it, and the agent that writes conclusions did not choose the sources. Reading material outside your role weakens that split, so find your role first and read only the files listed for it.

All paths below are relative to this skill's folder.

## Find your role

Look for a line starting with `ROLE:` in the brief you were given.

| Your brief says | You are | Read exactly these files |
|---|---|---|
| no `ROLE:` line | the orchestrator | [`references/orchestrator.md`](references/orchestrator.md), [`references/shared.md`](references/shared.md) |
| `ROLE: phase-1-brief` | phase 1 agent | [`references/shared.md`](references/shared.md), [`references/phase-1-brief.md`](references/phase-1-brief.md) |
| `ROLE: phase-2-discover` | phase 2 agent | [`references/shared.md`](references/shared.md), [`references/phase-2-discover.md`](references/phase-2-discover.md) |
| `ROLE: phase-3-evaluate` | phase 3 agent | [`references/shared.md`](references/shared.md), [`references/phase-3-evaluate.md`](references/phase-3-evaluate.md) |
| `ROLE: phase-4-synthesize` | phase 4 agent | [`references/shared.md`](references/shared.md), [`references/phase-4-synthesize.md`](references/phase-4-synthesize.md) |
| `ROLE: phase-5-audit` | phase 5 agent | [`references/shared.md`](references/shared.md), [`references/phase-5-audit.md`](references/phase-5-audit.md) |

If your brief also names [`references/academic-extract.md`](references/academic-extract.md) or [`references/academic-synthesize.md`](references/academic-synthesize.md), read that file too. Otherwise don't.

## If you are a phase agent

- Do only your phase. Do not read any other file in `references/`, do not dispatch other agents, and do not do work that belongs to another phase.
- If your files are missing, or your `ROLE:` value is not in the table, stop and report that to whoever dispatched you. Do not guess a role.

## If you are the orchestrator

`references/orchestrator.md` covers choosing the level, dispatching phases, the reopen loop, and delivery. You read `shared.md` as well; you need its ID rules, field ownership, and handoff formats to validate handoffs and merge records.

## Runtime metadata

This skill's invocation and display metadata is in [agents/openai.yaml](agents/openai.yaml).
