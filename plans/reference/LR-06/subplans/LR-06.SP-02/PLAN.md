---
plan_id: LR-06.SP-02
kind: subplan
parent: LR-06
phase: S2
status: complete
depends_on:
  - KNOW-02.AUD-01#claims-and-evidence
consumers: []
---

# LR-06.SP-02

## Objective

Identify useful cases where feedback loops are used in user workflows with AI
agents and determine what evidence supports their effects.

## Scope

Use S1's reviewed map as a search guide, not a closed list. Search empirical
studies, documented deployments, and practitioner accounts of people using
AI agents for tasks such as research, planning, writing, analysis, coding, or
tool-mediated work. Include other tasks when discovery supports them.

For each material case, record the user's task and starting problem; agent
role; feedback source and timing; what changes over cycles; stop condition and
human control; how people use or interact with the loop when reported; intended
and measured outcomes; comparator and resource budget; evidence type; and
limitations. Distinguish observed use from recommended practice, and direct
user-agent workflow evidence from adjacent benchmarks, model training, or
system-level feedback. Record positive, null, mixed, and adverse findings
when located, and state explicitly when the search found no material result in
one or more categories. A described capability or single success story is not
proof of effectiveness.

Do not infer a general benefit from a single task, model, or benchmark. Search
for comparisons that separate the loop's contribution from extra turns,
compute, tool access, or human attention when available.

## Output

Complete `LR-06.RES-02.audit.md` as a standard-rigor case evidence audit with
claim/evidence links, source provenance, case comparison, conflicts, and
transfer limits. Preserve exact searches and material scope changes in
`LR-06.RES-02.working.md`.

## Sequence

1. **S1 — Locate and compare agent-workflow cases**
   - **Action:** Follow standard `$research` rigor, using S1's reviewed
     terminology and expanding from primary studies and well-documented
     applications.
   - **Output:** Completed audit and retained discovery log.
   - **Exit check:** Every material case has a source and evidence type;
     observed effects are separated from intended outcomes and capability;
     conflicts, transfer limits, and review findings are reconciled.

## Completion criteria

- The case set centers on users working with AI agents; adjacent evidence is
  visibly labeled and cannot silently stand in for direct evidence.
- Each case states task, signal, agent change, stopping/human role, outcomes,
  user practice where reported, comparator, cost/resource context, and
  limitations where reported.
- Located positive, null, mixed, and adverse evidence is represented without
  pooling unlike measures into a common effectiveness claim; categories with
  no located evidence are stated explicitly.
- The audit and working log follow standard `$research` rigor, pass
  independent review, and are reconciled by the coordinator before S3 starts.

## Outcome

Completed. The audited case set covers direct and adjacent workflows,
outcome polarity, comparison strength, provenance, and search limits.
Independent review passed; the E4 wording now distinguishes study-task
trajectories and subjective questionnaire outcomes. Alibaba remains
abstract-only, and no clean powered direct null effect for loop contribution
to information-work quality was located. S2 is available as input to S3.
