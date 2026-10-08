---
name: writing-for-agents
description: Use this skill when writing, reviewing, or troubleshooting instructions, prompts, or documentation intended for an LLM to read and act on. Trigger on: drafting or reviewing a skill, prompt, or instruction set for a model; deciding what to emphasize or how to phrase a rule for LLM consumption; an instruction isn't being followed reliably and the cause is unclear; structuring how one model or agent hands context to another.
---

# Writing for Agents

Produce the least reading burden that reliably supports the consuming agent's
task. Preserve required behavior and necessary reasoning. When revising, remove
or consolidate content that adds no distinct operational value.

Perform these authoring checks without adding their commentary to the target
file. Include only the reasoning the consuming agent needs for its task.

## 1. Select content

- Identify the consumer's task, available context, and what this file must
  supply. Assume ordinary task competence; supply local conventions, facts,
  and prior decisions the consumer will not otherwise have.
- Identify distinct requirements before drafting or rewriting; state required
  behavior, constraints, and completion conditions explicitly. Organize around
  those requirements.
- Assess the entire target file; choose the extent of rewriting from its needs.
  A local correction alone does not complete that assessment.
- Keep supporting content only when it supplies a fact, decision distinction,
  or reasoning not already established. Ground precautionary guidance in a
  credible scenario and consequence.
- Give each rule one canonical home. Reference existing guidance when the
  consumer can access it; include essential context explicitly in isolated
  handoffs or summaries. Load branch-specific detail conditionally and name
  that condition at the link.

## 2. Allocate detail and choose representation

- Start with a direct instruction. For decisions that vary by context, consider
  a diagnostic question and the principle for answering it. Explain the
  mechanism when the consumer must generalize to unfamiliar cases. Add an
  illustrative example only when it clarifies a difficult distinction or
  resolves competing interpretations; retain only distinguishing details.
- Use steps for order, bullets for independent rules, tables for comparisons,
  and schemas for exact output contracts. Use short prose for relationships
  or reasoning. Name the actor when ownership matters.
- Put conditions before actions; keep exceptions explicit and flat. Preserve
  complete meaning rather than compressing into cryptic fragments.
- Place task-defining instructions and critical constraints early. State their
  priority explicitly; arrange remaining guidance in the order the consumer
  needs it. Use stable terms and consistent wording throughout.
- State the intended tie-breaker for conflicting instructions of equal
  authority. Flag conflicts across authority levels and defer to the applicable
  instruction hierarchy.
- Repeat a rule only to address a concrete risk of it being missed or lost,
  such as a long-session reminder or a separately loaded reference.

## 3. Review and stop

- Remove repeated meaning across instructions, rationale, examples, and
  checklists. Cut framing that adds no operational information. Replace case
  lists with a general rule when it preserves the distinctions needed to act.
- Compare original and revised requirements in both directions: check for lost
  behavior and newly introduced obligations. Preserve scope, authority,
  conditions, exceptions, dependencies, uncertainty, and completion criteria
  unless a substantive change is authorized. Brevity must not make the agent
  guess.
- Walk through a representative task using only the context the consumer will
  have. Check that it can find the instructions, resolve relevant conditions,
  produce the required result, and recognize completion. Repair gaps and remove
  content that contributes to none of these. Stop when further removal would
  impair execution or judgment. Count references in the reading burden;
  word counts alone do not establish quality. Treat the walkthrough as an
  inspection, not evidence of execution by another agent.

## Diagnose failures

When instructions fail, identify the cause from observed behavior before
adding rules. If uncertain, state a hypothesis and check it against an actual
task. Address the mechanism rather than copying the closest-looking example;
check that the fix preserves other requirements.

## Runtime metadata

This skill's invocation and display metadata is in [agents/openai.yaml](agents/openai.yaml).
