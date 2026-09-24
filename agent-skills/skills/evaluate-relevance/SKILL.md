---
name: evaluate-relevance
description: Assess whether something is relevant to Bernardo's current work, studies, professional direction, or personal knowledge library.
metadata:
  short-description: Assess technology relevance for Bernardo
---

# Evaluate relevance

Use this skill when Bernardo asks whether something is worth adopting, testing,
learning, preserving, or ignoring.

## Purpose

Bernardo is exposed to more skills, frameworks, repositories, AI capabilities,
and ideas than he can realistically adopt or investigate. The purpose of this
evaluation is to protect his attention while preserving genuinely valuable
future knowledge.

The question is not whether a candidate is generally good, impressive, or
interesting. The question is where, if anywhere, it belongs in Bernardo's
world:

- in a current project or workflow;
- in a focused experiment;
- in his personal knowledge library for future use;
- or nowhere in his current or foreseeable context.

This distinction matters because an idea can be valuable without being an
adoption priority. A strong candidate with no plausible place in Bernardo's
work is not relevant now; a promising but immature candidate may deserve a
small experiment or a place in the library.

## Operating principle

Start with Bernardo's context and motivation, not with the candidate's feature
list or category. First establish the candidate's possible role in his work,
studies, projects, or future direction. Only then go into technical details,
trade-offs, and evidence.

The evaluation should help Bernardo answer:

1. Why might this matter to me?
2. Where could it fit, if anywhere?
3. What would it change or enable?
4. Is that value worth the attention and adoption cost now?
5. If not now, is it worth preserving for later?

## Navigation map

| If you need to... | See |
| --- | --- |
| Understand why this evaluation exists | [Purpose](#purpose) and [Operating principle](#operating-principle) |
| Load Bernardo's context | [Source context](#source-context) |
| Position and analyse a candidate | [Evaluation sequence](#evaluation-sequence) |
| Choose an outcome | [Decision](#decision) |
| Structure the result | [Output](#output) |
| Respect the skill's limits | [Boundaries](#boundaries) |

## Source context

Before assessing a candidate:

1. Read the relevant sections of
   [`ABOUT-ME.md`](../../../../ABOUT-ME.md).
2. Read [`CONTEXT.md`](../../../../CONTEXT.md) to locate relevant projects and
   areas.
3. If the candidate may belong in the personal knowledge library, read
   [`personal-library/CONTEXT.md`](../../../../personal-library/CONTEXT.md) and
   only the relevant library material.
4. Open only the nearest project `CONTEXT.md`, `AGENTS.md`, README, plan, or
   other authoritative document needed for the candidate's plausible use cases.
5. Inspect the candidate's primary documentation or source repository. Verify
   current status, dependencies, license, and other changing facts when they
   affect the decision.

Do not read every project by default. Retrieve only the context needed to assess
the candidate responsibly.

## Evaluation sequence

Follow this sequence. Do not begin with a fixed checklist based on the
candidate's category.

### 1. Understand the candidate

Establish what the candidate actually does, what problem it claims to solve,
what it assumes, and what using it would require. Do not rely on its category,
marketing, popularity, or feature count.

### 2. Position it in Bernardo's context

Use `ABOUT-ME.md`, `CONTEXT.md`, and only the relevant project or library
context to identify a plausible connection. Explain why Bernardo might care, or
why there is no credible connection.

Name the likely role explicitly:

- current project or workflow;
- focused experiment;
- personal knowledge library;
- future possibility with no justified action yet;
- no meaningful place in Bernardo's context.

### 3. Understand the change

Describe what the candidate would enable, improve, replace, or make possible.
Compare it with the current approach and realistic alternatives. Focus attention
on the projects and workflows that could actually change; do not survey every
project in the workspace.

### 4. Test the value against the cost

Investigate only the factors material to this decision, such as fit,
integration, maturity, maintenance, cost, privacy, security, learning effort,
lock-in, or evidence quality. Separate immediate usefulness from longer-term
value.

### 5. Decide and explain

State what would have to be true for the candidate to be useful, distinguish
facts from inferences, and make the recommendation from the discovered fit.

Distinguish clearly between:

- confirmed facts from the candidate or Bernardo's context;
- reasonable inferences;
- assumptions that could change the recommendation;
- unknowns that require a focused test or a question.

## Decision

Use one of these outcomes:

- **Adopt now** — clear current value and acceptable cost.
- **Run a focused test** — plausible value, but an experiment is needed.
- **Preserve as library reference** — no immediate action is justified, but the
  candidate contains durable knowledge or a future-facing idea worth keeping in
  the personal library.
- **Do not adopt** — insufficient value, poor fit, excessive cost, or meaningful
  overlap.
- **Insufficient evidence** — the candidate or intended use is not clear enough
  to decide responsibly.

Do not recommend adoption merely because the candidate is interesting.

## Output

Keep the result concise but evidence-based:

```md
## Verdict

**Decision:** Adopt now | Run a focused test |
Preserve as library reference | Do not adopt | Insufficient evidence

**Confidence:** High | Medium | Low

**Library disposition:** None | Preserve as reference | Add to exploratory inbox

## Why this might matter

[The concrete reason Bernardo might care, or why no plausible connection was
found.]

## Position in Bernardo's context

[Current project, focused experiment, personal library, future possibility, or
no meaningful fit.]

## Relevant context

[The specific project, study area, workflow, or longer-term direction involved.]

## Assessment

[What the candidate does and why it does or does not fit the relevant context.]

## Evidence and assumptions

- Confirmed:
- Inferred:
- Unknown:

## Costs and risks

- Adoption and learning:
- Maintenance and opportunity cost:
- Integration, privacy, security, or lock-in:

## Recommendation

[The smallest sensible next action, or why no action is justified.]
```

If the intended use is materially unclear, ask one focused question before
deciding. Otherwise, state the assumption explicitly and continue.

## Boundaries

- Do not duplicate Bernardo's profile or project details in this skill.
- Do not update `ABOUT-ME.md` with inferred conclusions; add new personal
  context only after Bernardo confirms it.
- Do not install, clone, activate, subscribe to, or otherwise adopt anything
  unless Bernardo separately asks for that action.
- Do not add material to the personal library automatically. Recommend a
  library disposition first, and write or move content only when Bernardo asks
  for that action.
- Do not turn general technical quality into personal relevance without
  identifying a plausible connection to Bernardo's context.
