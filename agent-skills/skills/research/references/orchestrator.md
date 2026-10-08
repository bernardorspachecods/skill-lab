# Orchestrator

**Is this file for you?** If your brief contains a line starting with `ROLE:`, you are a phase agent. Stop reading this file and go back to `SKILL.md`.

You run the research: choose the level, dispatch the phases to separate agents, validate what comes back, route reopen requests, and deliver the result. Read `shared.md` as well; you need its ID rules, field ownership, and handoff formats to validate handoffs and merge records.

## Contents

- Starting a task
- Choose the level
- The pipeline and dispatch
- Academic tasks
- Validating handoffs
- The reopen loop
- If you cannot dispatch agents
- Finishing

## Starting a task

When a durable plan assigns the research unit, follow the coordinator-provided brief, research level, and required output locations. Don't change plan structure or artifact metadata. Changes to the assigned question, scope limits, level, or output locations go to the coordinator, never to a phase agent to decide.

When the user invokes you directly, ask at most one focused clarification, and only if the answer would materially change direction. Otherwise state your assumption and proceed.

## Choose the level

Use Standard by default. When uncertain, choose the higher level.

**Quick.** A narrow lookup that one authoritative source can answer, with no comparison, no expected conflict, and low consequences. Do it yourself, without phase agents or an audit record:
1. State the question.
2. Find the closest authoritative source and open it.
3. Read the relevant part and copy the exact wording.
4. Answer with the citation, the source's date, and any limits.

Escalate to Standard if the source is weak, the answer is dated or disputed, or a second look shows conflict. Quick work still follows the principles in `shared.md`. Collection is deliberately minimal here.

**Standard.** Questions that need multiple sources, comparison, or an auditable evidence trail. Run all five phases with separate agents. Compact source ledger, a deliberate refutation pass in phase 2, a concise conflict summary, and one auditor for all material claims (one per claim if you prefer).

**High-stakes.** Safety, legal, financial, medical, security, public claims, and expensive or hard-to-reverse decisions. Run all five phases with separate agents. Seek multiple independent primary or authoritative sources for each high-importance claim, keep full provenance and dates, keep the conflict log, and use one auditor per material claim. Recommend specialist or human review when possible. If the evidence is inadequate, deliver a bounded answer rather than a confident recommendation.

### Search ceilings

Phase 2 follows a collect-first rule with no natural end, so give it a ceiling per claim. A `Q#` is one submitted search query or one citation lead followed; separate actions need separate records. Each record lists the `C#` claims it serves, and counts once toward the ceiling of every listed claim. Starting values, to be overridden by the assignment:

| Importance | Standard | High-stakes |
|---|---|---|
| high | 20 | 40 |
| medium | 10 | 20 |
| low | 5 | 10 |

The ceiling is an upper bound, not a target or a sufficiency test. At the ceiling, phase 2 must stop searching that claim until you decide whether to extend its budget. If a mapped route could materially change the answer, phase 2 sends you a reopen request naming the claim, route, expected contribution, and proposed revised ceiling. Continue within the existing ceilings on other claims while waiting. Accept or decline with a reason and log the decision; when accepting, state the revised ceiling for each affected claim. An accepted extension counts as one reopen cycle for each affected claim; a declined request authorizes no additional search and the claim is reported as budget-constrained, not fully covered.

## The pipeline and dispatch

```text
phase 1 brief -> phase 2 discover -> phase 3 evaluate -> phase 4 synthesize -> phase 5 audit
      ^______________|__________________|___________________|___________________|
                              reopen requests (via you)
```

Run each phase as its own agent. Give each only what its row below allows. The omissions are deliberate: they stop one phase's verdicts from anchoring the next.

| Phase | Role token | Receives | Does not receive |
|---|---|---|---|
| 1 | `phase-1-brief` | user request or assignment brief, level, constraints | - |
| 2 | `phase-2-discover` | brief, claim matrix (claims, importance, evidence expectations, scope), level, search ceilings, any user-supplied sources | - |
| 3 | `phase-3-evaluate` | claim matrix, source list (`S#`, location, access date, collected-for claims as a lead), ID block | phase 2's apparent-role notes, `Q#` records, any preliminary answer |
| 4 | `phase-4-synthesize` | claim matrix, `E#` entries, ledger assessment fields, coverage summary | the working record, discovery notes |
| 5 | `phase-5-audit` | claim matrix with support status and confidence, draft answer, `E#` entries, ledger, coverage summary, conflict log | phase 4's reasoning notes, the working record |

If the user supplied sources or a single document, still dispatch phase 2 in a registration-only role: phase 2 assigns `S#` IDs and records the initial ledger fields for those sources, then skips discovery searches. Record the skipped search and reason in the coverage summary. Don't invent searching to fill the phase.

### Parallelism

You may run phase 3 per source group and phase 5 per claim. Give each parallel agent its own ID block (for example `E101-E199`, `E201-E299`), and merge the records yourself. Run phase 4 as a single agent so the synthesis is coherent.

### Dispatch brief template

Put the `ROLE:` line first. Name the files to read, so the agent gets the instruction in two places.

```text
ROLE: phase-3-evaluate

Objective: <one concrete outcome>
Read: references/shared.md, references/phase-3-evaluate.md[, references/academic-extract.md]
Do not read any other file from this skill and do not dispatch other agents.
Level: <Quick | Standard | High-stakes>
Inputs: <records and sources provided, topic, population, period, decision>
Requirements: <checks needed; academic stages to run, if any>
Output: <destination in the audit or working record; ID block>
Evidence gate: <what is needed to verify a material result>
```

## Academic tasks

For academic papers, literature reviews, thesis planning, empirical findings, or research-question design, choose the level first, then attach the academic files. They add structures and stages on top of the same workflow and don't replace the claim and evidence rules.

- Add `references/academic-extract.md` to phase 3 briefs and `references/academic-synthesize.md` to phase 4 briefs.
- In each brief's Requirements, name only the academic stages the task needs.
- Pass the phase 3 stage material (orientation maps, `F#` cards) to phase 4 together with the `E#` entries. Phase 4 must never receive `F#` cards alone.

## Validating handoffs

Check each returned phase report before using its output.

- The report has all fields, and `Read:` lists only files from that agent's set. If it read outside its set, treat its output as suspect and re-dispatch.
- It stayed in its phase: no conclusions from phase 2, no support statuses from phase 3, no new searching from phase 4. Strip or re-dispatch.
- It wrote only the fields it owns, and used only its ID block.
- Limits are stated, and unfinished work is marked rather than papered over.
- If `Clarification needed:` names a material question, pause dependent work and resolve it under the clarification rule in the reopen loop before continuing.

## The reopen loop

Research isn't sequential. Evaluation shows a claim was badly framed, a source type is missing, or an audit finds an overreaching conclusion. Phase agents can't change the pipeline themselves; they send reopen requests to you.

### Routing

| From | May reopen | Typical reasons |
|---|---|---|
| 2 | 1, 2 | ill-posed claim, needed subquestion; a phase-2 budget extension may target phase 2 |
| 3 | 2, 1 | citation lead, evidence gap, missing source role, claim needs splitting |
| 4 | 3, 2, 1 | passage insufficient, unresolved conflict, missing support |
| 5 | 4, 3, 2 | overreaching conclusion, quote mismatch, counter-evidence, coverage gap |

Route each request to its target and log its outcome in the reopen log. For a request targeting phase 1, dispatch revision mode without pre-approving the proposed claim change; phase 1 decides whether to accept or decline that change within the assigned brief. Log phase 1's disposition. For requests targeting other phases, decide whether to accept, decline with a reason, or merge them before dispatch.

### Rules

- **Claim changes go through phase 1.** Dispatch phase 1 in revision mode with the request and the current claim matrix. Changes are append-only: new `C#` entries, old ones marked `superseded` or `split` with a reason. Never delete or reuse an ID. Changes to the assigned question or scope limits need the coordinator or, in direct use, an explicit assumption stated to the user.
- **Clarifications raised after dispatch.** If a phase report includes `Clarification needed:`, pause work that depends on the answer and take the question to the user for direct research or to the plan coordinator for an assigned unit. Once answered, return the answer to phase 1 in revision mode if the claim matrix may change; otherwise record the answer and resume. Do not silently resolve a question the phase marked material.
- **New sources found by phase 5.** Route a newly found candidate source to phase 2 for collection and ledger entry, then phase 3 for evaluation. Route a source already in the ledger directly to phase 3 only when it needs re-evaluation. Phase 5 never adds sources to the evidence record itself.
- **Phase 5 verdicts.** A `pass` needs no revision. For `weaken` or `remove`, send the affected claims and required changes to phase 4 in revision mode; phase 4 revises the draft and its support status or confidence, then phase 5 re-audits the affected claims and checks the rest for regressions. For `reopen`, route the request to the phase that owns the missing work and complete all affected downstream phases in order; phase 4 revises the draft and phase 5 re-audits it. If a cap prevents rework, disclose the unresolved verdict and deliver a bounded conclusion.
- **Don't let the loop widen the work.** Accept new subquestions only if they are material by the definition in `shared.md`.
- **Rework only what's affected.** The `C#` to `E#` links show which downstream work depends on a changed claim or source. Re-run only those parts, then re-run the audit on affected claims plus a regression check on the rest.
- **Blocking requests come first.** A reopen request marked blocking must be resolved, or disclosed in the final answer.
- **Caps.** At most 2 accepted reopen cycles per claim and 3 rework rounds overall after the first audit (starting values; the assignment may override). An accepted search-budget extension after the first audit also counts as one rework round. At a cap, don't accept another extension or research reopen; apply any required phase-5 correction, then deliver a bounded conclusion with the support status, what was tried, and what remains documented. A declined request does not count as a reopen cycle.

## If you cannot dispatch agents

Report back to the user and STOP

## Finishing

Before delivering, check that every blocking audit item is resolved or disclosed, that phase 5 verdicts have been applied (or the reason they weren't is stated), and that the answer includes the reason collection stopped and a summary of conflicts or refutation findings.

Where the result goes:

- Return findings in the conversation when there is no durable consumer. Create or update a knowledge entry when findings are likely to be reused.
- For plan assignments, use the assigned destination and report its location, the material conclusions and uncertainties, and any unmet requirements. Follow the assignment's retention instructions. Don't present provisional research as completed plan output.
- Rigor sets the minimum record: Quick needs a cited answer with its limits; Standard and High-stakes need the audit record. Research does not require a separate result artifact.
- Keep the evidence record separately accessible from the consumer-facing answer, and don't merge it with the working search record. For direct research with no assigned or user-requested artifact location, present the audit record as a separate labeled section in the conversation. For plan assignments or a user-requested persistent artifact, use the assigned or requested location. A knowledge entry links to its evidence record.
- Keep the claim matrix, evidence entries, and ledger current whenever traceability, persistent review, or the assignment calls for them.

Phase 4's draft answer follows the shape in `phase-4-synthesize.md`. You review it, apply the audit verdicts, and deliver it.
