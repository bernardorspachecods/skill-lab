---
plan_id: LR-05
kind: root
parent: null
phase: root
status: in_progress
depends_on: []
consumers: []
execution:
  research: "standard"
  root_research: false
  research_working: true
  review: true
  user_checkpoints: each_subplan
---

# LR-05

## Objective

Build a broad, evidence-based map of automated loops used in AI information
work, examine where they are applied and what evidence supports their effects,
then decide whether any patterns could improve the repository's plan-management
and related skills. The work ends with a recommendation and possible workflow
designs; changing skills or adopting a loop is outside this plan.

## Scope

Treat “loop” as an open research concept. Use a provisional lens: a recurring
cycle observes or evaluates a state or output and uses feedback to change a
later action, output, model, data, or workflow. This lens guides comparison;
it is not a gate for discovery. Search adjacent terminology and report how
sources use it rather than assuming one settled taxonomy.

Cover loops involving AI systems and information work across technical,
human, and organizational settings. Examine what is fed back, who or what
produces the signal, what changes on the next cycle, how often and with what
degree of autonomy, what outcome is intended or measured, and what role people
have. Include loops that generate, retrieve, check, revise, learn from, monitor,
or govern AI-related information when evidence supports their inclusion.

Require a direct connection to AI handling, producing, checking, retrieving,
learning from, monitoring, or governing information. Keep loops with only a
loose or indirect AI connection in an adjacent-cases note rather than expanding
the core survey to general control systems or iterative work.

Do not claim exhaustive coverage of the open literature. Set no fixed date or
geography cutoff unless evidence discovery shows one is material. Separate
documented capability from demonstrated effectiveness; distinguish source
findings, cross-source synthesis, and recommendation. The final workflow-fit
phase may inspect canonical local skills but must not edit them.

## Output

A concise, source-traceable synthesis that maps loop mechanisms and terms,
summarizes applications and evidence, explains evaluation limits and recurring
failure modes, and assesses fit with plan-management and related skills. The
recommendation will show candidate workflow patterns, evidence strength,
tradeoffs, assumptions, and an appropriate next step. It may recommend no
change. No skill changes or live workflow experiments are part of this plan.

## Current phase

The user approved the plan and execution contract. The S1 independent review
requires a bounded probe of six specialist vocabularies named in its coverage
limits. The researcher is extending the existing assignment; after the probe,
coordinator reconciliation, and review of the correction, present S1 for the
user checkpoint before advancing to S2.

## Sequence

1. **S1 — Map terminology and loop mechanisms** ([LR-05.SP-01](subplans/LR-05.SP-01/PLAN.md))
   - **Action:** Search broadly for how loops are named and structured in AI
     information work, then produce a candidate mechanism map and vocabulary
     for later searches.
   - **Output:** Standard-rigor evidence audit with a mechanism map, term
     families, source-supported definitions, and explicit coverage limits.
   - **Exit check:** Distinct mechanisms and neighboring terms are represented
     without claiming a universal taxonomy; evidence and gaps are traceable;
     the independent review is reconciled and the user checkpoint is approved.

2. **S2 — Survey applications and observed outcomes** ([LR-05.SP-02](subplans/LR-05.SP-02/PLAN.md))
   - **Action:** Use S1's reviewed map to find where the mechanisms are applied
     and what outcomes, contexts, and evidence types are reported.
   - **Output:** Standard-rigor evidence audit comparing applications,
     intended outcomes, observed results, and transfer limits.
   - **Exit check:** Material application claims have source-level support and
     are distinguished from demonstrated effectiveness; conflicts and gaps are
     explicit; the review and user checkpoint are complete.

3. **S3 — Assess evaluation, limitations, and failure modes** ([LR-05.SP-03](subplans/LR-05.SP-03/PLAN.md))
   - **Action:** Examine how loop effects are measured and what conditions
     improve or undermine them, including cases where feedback reinforces
     errors or optimizes a poor proxy.
   - **Output:** Standard-rigor evidence audit of evaluation approaches,
     benefits, costs, risks, and boundary conditions across the mapped uses.
   - **Exit check:** Positive, null, mixed, and adverse evidence is handled;
     measured outcomes are separated from proxies and explanations; limits are
     explicit; the review and user checkpoint are complete.

4. **S4 — Assess fit with the skills workflow** ([LR-05.SP-04](subplans/LR-05.SP-04/PLAN.md))
   - **Action:** Synthesize S1–S3 and inspect relevant canonical skills to map
     supported loop patterns to current workflow steps and identify costs,
     risks, and missing evidence.
   - **Output:** A reviewed workflow-fit assessment with candidate options and
     a recommendation; no skill files are changed.
   - **Exit check:** Each proposed fit links to research and local workflow
     evidence, alternatives and tradeoffs are visible, and the review and user
     checkpoint are complete.

5. **S5 — Integrate the final recommendation**
   - **Action:** Assign a distinct agent to integrate the reconciled research
     audits and S4 assessment into the root output after all four checkpoints.
   - **Output:** The final concise synthesis and recommendation in this root
     plan's Outcome section.
   - **Exit check:** The agent handoff is reconciled into the root Outcome;
     claims trace to reconciled outputs; uncertainty, conflicts, applicability
     assumptions, and the basis for the recommendation are clear.

The subplans run in order because later searches depend on earlier vocabulary
and evidence. Within each subplan, research (when enabled) precedes independent
output review. Present each reconciled subplan for the selected user checkpoint
before advancing or using its output downstream. S4 has a local exception:
it uses the prior research and local skill files without a new external
research assignment. Do not start root integration until all four checkpoints
are approved.

## Completion criteria

- The three external research audits follow standard `$research` rigor and
  distinguish source quality, claim support, provenance, and uncertainty.
- Search discovery covers multiple useful terms and source roles without
  claiming complete recall; the retained working logs preserve material search
  paths and scope adjustments.
- The synthesis explains the range of mechanisms and applications found,
  including contrary or inconclusive evidence and meaningful limits.
- S4 maps candidate mechanisms to relevant local workflows, evaluates fit and
  tradeoffs, and does not modify skills or claim an untested improvement.
- All four subplan outputs have independent reviews, are reconciled, and pass
  the user checkpoints; root integration is completed by a distinct agent.
- The user receives a clear recommendation or a supported conclusion that the
  evidence does not yet justify a workflow change.

## Outcome

Pending execution.
