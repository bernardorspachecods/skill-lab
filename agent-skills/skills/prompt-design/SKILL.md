---
name: prompt-design
description: Create, improve, audit, compress, or structure prompts and task briefs for LLMs, agents, coding, research, reviews, or documentation. Use when the user asks how to prompt an LLM; do not use when they want the underlying task executed.
---

# Prompt Design

Design prompts as task briefs. A good prompt tells the LLM what to do, what context matters, what rules to obey, what uncertainty to preserve, how to verify, and what to return.

Use the smallest prompt that makes correct behavior likely.

## Clarification Rule

If the user's goal is unclear, stop and ask one concise question before writing the prompt.

Ask when:

- the target task is ambiguous;
- the intended user, model, agent, or environment materially changes the prompt;
- the output format matters but is unspecified;
- there are multiple valid prompt directions with different tradeoffs;
- the prompt could trigger risky, destructive, private, legal, financial, medical, or high-impact work;
- required context is missing and cannot be safely inferred.

Do not ask when:

- the missing detail is minor;
- a safe default is obvious;
- the user clearly wants a draft;
- placeholders are acceptable.

If clarification is needed, return only:

```text
Question:
[one concise question]

Why it matters:
[one sentence]
```

## Core Workflow

1. Identify the prompt's route: quick answer, software change, code review, app revamp, research synthesis, long-document analysis, feature evaluation, documentation, or human decision.
2. Decide the minimum useful context.
3. Separate hard rules from preferences.
4. Add examples only when they clarify output shape or boundary behavior.
5. Add verification expectations when correctness matters.
6. Add "ask before" rules for risky or ambiguous decisions.
7. Remove sections that do not help the task.
8. Return a ready-to-use prompt plus short usage notes when helpful.

## Documentation-Backed Prompts

When a repository or workspace already has authoritative instructions, plans,
or domain documentation, treat the prompt as a routing brief rather than a copy
of those sources.

- Point to the smallest required source set and require it to be read first.
- Put durable detail in the repository documentation, not repeatedly in prompts.
- Include only the delta: current objective, newly approved decisions, scope,
  immediate request, stop/ask boundary, and observable definition of done.
- Do not repeat rules already owned by `AGENTS.md`, a current plan, or domain and
  operations documents.
- Inline a rule from documentation only when it is unusually high-risk,
  currently disputed, inaccessible to the target agent, or essential to
  interpreting the immediate request.
- If sources conflict, require the agent to stop and report the conflict instead
  of silently choosing one.
- Prefer one current plan over several overlapping or historical trackers.

For `/goal` and other long-running agent prompts, be especially strict: the goal
should say what outcome to pursue and when human input is required, while the
linked plan owns the workflow and technical detail. Before returning a prompt,
remove every paragraph that merely restates an accessible source. Robustness
comes from clear ownership and verification, not prompt length.

## Prompt Anatomy

Use only the sections that matter:

```text
Objective:
Context:
Sources:
Rules:
Preferences:
Examples:
History:
Ask before:
Process:
Verify by:
Output format:
Immediate request:
```

## Behavior Rules

Do:

- make the objective concrete;
- tell the LLM what context to read and what to ignore;
- label sources, rules, preferences, examples, history, assumptions, and open questions;
- include confidence discipline for factual work;
- require source grounding for research, legal-ish, technical, or documentation-heavy work;
- include verification for code, data, claims, UI, or high-risk output;
- keep humans as decision-makers for product, architecture, irreversible, or high-impact choices;
- make output structure easy to review or reuse.

Do not:

- create a giant prompt by default;
- duplicate accessible project documentation inside the prompt;
- use "be comprehensive" without saying what matters;
- ask the LLM to use all context blindly;
- let the model silently choose product or architecture direction;
- mix examples with requirements;
- ask for long reasoning traces when the user only needs a usable prompt;
- hide uncertainty or missing evidence.

## Common Prompt Patterns

### Software Change

Include:

- goal;
- user-facing behavior;
- relevant files or search instructions;
- existing behavior to preserve;
- constraints;
- test/build/verification command if known;
- definition of done;
- ask-before rules for data model, public API, architecture, or scope changes.

For repo continuation prompts:

- split sources into required-first and conditional-if-touched;
- define done as observable UI/API behavior, not just intent;
- if identifiers/contracts are missing, require options and approval before changing API, schema, permissions, or navigation.

### Code Review

Require findings first. Each finding should include severity, file/line, problem, impact, and suggested fix.

Tell the model to prioritize correctness, security/privacy, data loss, user-facing regressions, performance with real impact, and maintainability likely to cause defects.

### App Revamp

Tell the model to map the current app before changing it:

- routes/screens;
- core flows;
- data/API dependencies;
- broken workflows;
- features to preserve;
- first safe change;
- screenshots or smoke checks when UI is involved.

### Research / Second Brain

Use source-to-synthesis discipline:

1. source index;
2. source notes;
3. claim cards;
4. open questions;
5. synthesis.

Do not let the model jump from raw source to final conclusions.

### Long Document Analysis

Tell the model to map the document first, identify relevant sections, extract notes with section/page/URL locators, synthesize only after extraction, and flag unread sections that may matter.

### Documentation

Include:

- audience;
- reader goal;
- source of truth;
- maintenance expectation;
- examples to preserve;
- assumptions and open questions.

## Output Format

Default output:

```markdown
## Prompt

[ready-to-use prompt]

## Why This Works

- [short reason]
- [short reason]

## Optional Adjustments

- [only if useful]
```

If the user asks only for the prompt, return only the prompt.

## Reference Guidance

This skill is derived from the local LLM Field Manual. When deeper guidance is needed and available, read:

- `references/prompt-guidance.md` for route-specific prompt patterns.
- `references/failure-modes.md` for common bad prompt behavior.
