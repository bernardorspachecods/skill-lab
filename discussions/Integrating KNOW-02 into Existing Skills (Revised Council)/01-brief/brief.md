---
approval_status: approved
approved_sha256: 0ff679b4c446aaad44c1276384ec6abef769031b1ca2d6098dc0d78149fc825c
---

# Council Brief

## Question
How should skills support independent-agent feedback loops, using `$plan-management` as the example? Recommend an integration pattern and identify what changes, if any, plan-management should make.

## Context
`knowledge/KNOW-02.md` is the source of knowledge for this discussion, not the integration target. It is a bounded synthesis about feedback loops in user-facing AI-agent workflows. It describes goal/current state, what changed, a task-relevant signal for judging the result, and a next action. It recommends choosing a meaningful signal before cadence, making the next action explicit, setting checkpoints and stopping around consequence/evidence, and using an outcome check distinct from the signal that drives another cycle. It distinguishes empirical findings, observed practices, inferences, and recommendations; evidence is varied and task/system-specific, with no universal best checkpoint cadence or stopping rule established. Source: `knowledge/KNOW-02.md`.

The focus is how a skill can coordinate a bounded cycle with an independent agent: assign work, receive the agent's artifact and evidence, assess it against the brief and relevant criteria, then decide whether to accept it, request targeted follow-up, or stop/escalate.

`$plan-management` already keeps the user-facing context with the coordinator, sets agreed checkpoints, delegates research/implementation/formal review when useful, checks handoffs against briefs and criteria, uses a temporary integrity check before durable-plan execution, and requires validation for durable plan structure. It cautions against adding phases or reviews without a concrete need. Source: `agent-skills/skills/plan-management/SKILL.md`.

Skills are maintained as independently loaded instructions, with shared references where appropriate. The council should consider how to translate the source knowledge into agent handoffs and coordinator decisions without duplicating the full knowledge source, loading irrelevant context, adding unnecessary cycles, or overstating what the evidence proves.

## Stakes
The decision affects how skills assign and follow up on independent agent work, the quality and cost of that work, and whether feedback produces useful corrections without adding unnecessary cycles or unsupported requirements.

## Assumptions and unresolved context
The council should recommend changes, not make them in this run. Treat plan-management as the pilot rather than inventorying every skill. The threshold for repeating agent work and the best location for shared versus skill-specific guidance remain open.
