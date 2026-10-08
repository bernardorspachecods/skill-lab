---
name: evaluate-relevance
description: Explain and explore candidates with Bernardo, then connect them to his context when useful. Use when he presents a tool, repository, idea, or capability to understand; do not use for simple factual questions.
---

# Evaluate relevance

This skill's invocation and display metadata is in [agents/openai.yaml](agents/openai.yaml).

Use this skill when Bernardo presents a tool, repository, framework, AI
capability, idea, or other candidate and wants to understand or discuss it.

## Purpose

Help Bernardo understand what he presented before asking him to judge its
relevance or value. The evaluation is a staged conversation, not a verdict
delivered in the first response. Explain the candidate clearly, explore the
parts that matter to him, and connect it to his context with concrete possible
applications when the discussion is ready for that.

The first response may flag a clear mismatch with Bernardo's context so he can
stop early. Otherwise, keep the personal-fit check brief until the candidate
has been explained and explored. Do not turn every evaluation into an adoption
decision.

## Conversation flow

### 1. Explain the candidate

Start with the candidate itself, not Bernardo's profile or a recommendation.
Explain what it is, what problem it addresses, how it works, its main parts,
what using it involves, and what distinguishes it from relevant alternatives.
For a GitHub repository, use its README and primary documentation or code to
explain its purpose, architecture or workflow, key components, requirements,
and a concrete example of how it is used.

Give enough detail for Bernardo to understand the candidate. Scale the depth to
its complexity and to what he presented; do not attempt to describe every file
or feature by default. Separate confirmed facts from interpretation, and check
current details such as maintenance, dependencies, license, and cost when they
matter. Use primary sources where available.

### 2. Make an early relevance check

After understanding the candidate, consult only the parts of Bernardo's context
needed to identify an obvious mismatch or plausible connection:

1. Read relevant sections of [`ABOUT-ME.md`](../../../../ABOUT-ME.md) and
   [`CONTEXT.md`](../../../../CONTEXT.md).
2. Open only the nearest project `CONTEXT.md`, `AGENTS.md`, README, plan, or
   other authoritative context needed for a plausible application.
3. If a personal-library connection may matter, read
   [`personal-library/CONTEXT.md`](../../../../personal-library/CONTEXT.md) and
   only the relevant library material.

If there is clearly no meaningful connection to Bernardo's current work,
studies, professional direction, or plausible future interests, say so briefly
and explain why. This is an early filter, not a judgment about the candidate's
general quality. If there is a plausible connection, give at most a short
signal in the first response; save detailed applications for the later
discussion.

### 3. Continue as a conversation

If there is a plausible connection, end the first response with one useful
question about what Bernardo wants to understand or examine next. Offer a few
specific angles only when they help him choose, such as architecture, practical
usage, limitations, alternatives, or fit with a particular project. Do not ask
a question whose answer is already clear from his request. If there is clearly
no meaningful fit, explain that briefly and let Bernardo choose whether he
wants to continue exploring the candidate anyway.

In later turns, follow his interests. Explain details, compare realistic
alternatives, and investigate material trade-offs such as maturity, integration,
maintenance, cost, privacy, security, learning effort, or lock-in as relevant.
Ask focused questions only when a wrong assumption would change the direction
of the discussion. Keep track of unresolved questions and conclusions when the
conversation becomes long enough that they could be lost.

### 4. Connect it to Bernardo's context

When there is enough understanding to make the connection useful, give a few
concrete examples of where or how the candidate might apply in Bernardo's
context. Explain what each example could enable or change, and distinguish
confirmed context from inference. Include limitations or conditions that could
make an example a poor fit.

Possible roles include:

- a current project or workflow;
- a focused experiment;
- a personal knowledge-library reference;
- a future possibility with no action yet;
- no meaningful fit.

These are ways to locate possible applications, not mandatory verdict labels.

## Recommendations and decisions

Do not force a final recommendation, confidence rating, library disposition,
or adoption decision into the first response. Make a recommendation when
Bernardo asks for one or when the discussion has reached that question. Then
weigh the likely value against attention and adoption costs, explain the
evidence and assumptions, and suggest a proportionate next step.

Possible conclusions, when useful, include adopting, running a focused test,
preserving a reference, not adopting, or needing more evidence. Do not
recommend adoption merely because a candidate is interesting or technically
strong.

## Boundaries

- Do not duplicate Bernardo's profile or project details in this skill.
- Do not update `ABOUT-ME.md` with inferred conclusions; add new personal
  context only after Bernardo confirms it.
- Do not install, clone, activate, subscribe to, or otherwise adopt anything
  unless Bernardo separately asks for that action.
- Do not add material to the personal library automatically. Recommend a
  disposition first, and write or move content only when Bernardo asks.
- Do not confuse a candidate's general quality with its relevance to Bernardo.
- Keep the first response explanatory and open-ended. Use an obvious lack of
  personal fit only as an early filter; explore plausible fit through the
  conversation before drawing broader conclusions.
