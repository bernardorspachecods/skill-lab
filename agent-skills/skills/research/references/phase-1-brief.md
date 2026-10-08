# Phase 1: Define the brief

**Role.** You turn the request into a bounded research question and a prioritized set of material claims. Every later phase works from what you write, so a vague or mis-scoped brief spreads through the whole pipeline.

Read `shared.md` first if you haven't.

## Inputs

The user request or assignment brief, the research level, and any stated constraints. In revision mode, also the reopen requests and the current claim matrix.

## What to produce

Write these to the audit record:

1. **The research question**, bounded and answerable.
2. **The claim matrix rows.** Each material claim or subquestion gets:
   - a stable `C#` ID;
   - the claim, written as a testable statement or an answerable subquestion with one idea in it, so evidence can clearly support or conflict with it;
   - its importance (high, medium, low; definitions in `shared.md`);
   - what kind of evidence would answer it, such as primary data, official records, peer-reviewed studies, or first-hand accounts;
   - how much corroboration it needs, in proportion to importance and the level. For example: one authoritative source is enough; a primary source plus independent corroboration; multiple independent primary sources. Later phases use this to judge whether collection and support are adequate.
3. **Scope limits with reasons**: geography, time period, population, jurisdiction, version, or anything else relevant, and why each matters. Recording why lets later phases tell an irrelevant source from an inconvenient one.
4. **Assumptions and exclusions**, with reasons.
5. **Order or dependencies**, if some claims must be settled before others make sense.

Keep the set small. Include what is material by the definition in `shared.md`, and rank it. Don't pad it with trivia, and don't skip a claim the answer rests on.

## Method

- Work out what the user actually needs decided or understood, not only what they typed. Define claims that serve that need.
- If you must understand unfamiliar terms to frame the question, do a small amount of orientation reading. Note it in the working record as leads, not evidence.
- Ask for clarification only when the answer could materially change direction. You can't ask the user directly, so put one focused question under `Clarification needed:` in your phase report. Otherwise state your assumption and proceed.

## Revision mode

When dispatched to revise the claim set after a reopen request:

- You own the decision to accept or decline the proposed claim-set change within the assigned brief. The orchestrator routes the request and records your disposition; it does not pre-approve the claim change.
- Change the set append-only. Add new `C#` entries; mark replaced ones `superseded by C#` or `split into C#, C#` with a reason. Never delete, renumber, or reuse an ID.
- State whether you accepted or declined each request and give the reason.
- Include each request's disposition and reason in your phase report so the orchestrator can log the outcome without another approval round.
- If a change would alter the assigned question, scope limits, level, or output locations fixed by the brief, decline it under the current brief and report it under `Clarification needed:` so the orchestrator can take it to the coordinator or user.

## Don't

Don't search for evidence, name sources as answers, or draft conclusions. A brief shaped by what is easy to find is a biased brief.

## Done when

Every material claim has an ID, importance, evidence expectation, and corroboration expectation, and scope limits and assumptions are recorded with reasons. Finish with the phase report from `shared.md`.
