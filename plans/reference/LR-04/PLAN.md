---
plan_id: LR-04
kind: root
parent: null
phase: root
status: complete
depends_on: []
consumers: [KNOW-01]
execution:
  research: standard
  root_research: false
  research_working: false
  review: true
  user_checkpoints: each_subplan
---

# LR-04

## Navigation map

| If you need... | See |
| --- | --- |
| Review the integrated conclusion and experiment proposal | [Outcome](#outcome) |
| Inspect importance-wording evidence | [SP-01 plan](subplans/LR-04.SP-01/PLAN.md#objective) · [audit](../../../knowledge/audit/KNOW-01.AUD-01.md#question-and-scope) |
| Inspect described-stakes evidence | [SP-02 plan](subplans/LR-04.SP-02/PLAN.md#objective) · [audit](../../../knowledge/audit/KNOW-01.AUD-02.md#question-and-boundaries) |
| Check scope, workflow, and completion conditions | [Scope](#scope) · [Sequence](#sequence) · [Completion criteria](#completion-criteria) |

## Objective

Review the existing evidence on whether LLM task performance changes when a
prompt signals that a task is important or describes real-world stakes and
consequences, then determine whether the evidence supports a follow-up
controlled experiment.

## Scope

This is a literature review, not an experiment. Treat importance wording and
described stakes as distinct prompt factors. Importance wording includes
generic priority or importance cues (for example, telling a model that a task
is important). Described stakes include explaining plausible benefits, harms,
or consequences associated with task outcomes. Keep the underlying task and
available task information in view when interpreting any reported effect;
stakes descriptions can add context as well as salience.

Review empirical evidence involving LLMs, including positive, null, mixed, and
negative effects. Focus on task quality or correctness; report instruction
following, calibration, response characteristics, and resource use when the
sources measure them. Distinguish actual consequential settings or incentives
from hypothetical stakes described in a prompt, and distinguish both from
generic importance wording. Include study design, model/version, task domain,
measures, and limitations when reported. Do not infer that results generalize
to all models or tasks from a narrow study set.

The two evidence reviews may identify overlapping studies when those studies
test both mechanisms; the root synthesis will reconcile that overlap. Do not
claim a systematic review or exhaustive search unless the executed search
supports that characterization. Do not run model evaluations or make real
consequences contingent on model outputs. A follow-up experiment may be
proposed if the reviewed evidence warrants it; it is not part of this plan's
execution.

## Output

Two independently reviewed, source-traceable evidence audits, one for each
mechanism, and a concise integrated synthesis returned to the user. The
synthesis will state what the evidence supports, where results conflict or are
missing, how the mechanisms differ, and how confident the conclusion is. If
useful, it will outline a controlled follow-up experiment that separates
importance wording from described stakes, including neutral, wording-only,
stakes-only, and combined conditions while holding task content constant.

## Current phase

The independent plan integrity check, both parallel research assignments,
independent reviews, user checkpoints, and root integration are complete and
reconciled. Plan validation reports no errors or warnings. No experiment was
run.

## Sequence

1. **S1 — Review explicit importance wording** ([LR-04.SP-01](subplans/LR-04.SP-01/PLAN.md))
   - **Action:** Review empirical evidence about generic importance or priority
     cues in prompts, keeping task content and measured outcomes explicit.
   - **Output:** A source-traceable research audit and an independent review
     assessment.
   - **Exit check:** Material claims have linked primary evidence; the audit
     distinguishes effect, study context, limits, conflicts, and uncertainty;
     the independent review is reconciled and the user approves this subplan.

2. **S2 — Review described real-world stakes** ([LR-04.SP-02](subplans/LR-04.SP-02/PLAN.md))
   - **Action:** Review empirical evidence about prompts describing benefits,
     harms, or consequences, distinguishing hypothetical descriptions from
     actual incentives or consequential settings.
   - **Output:** A source-traceable research audit and an independent review
     assessment.
   - **Exit check:** Material claims have linked primary evidence; the audit
     distinguishes effect, study context, limits, conflicts, and uncertainty;
     the independent review is reconciled and the user approves this subplan.

The two research assignments launch in parallel and have no dependencies on
one another. Within each subplan, research precedes formal review. When either
subplan's research and review are reconciled, present it for the selected
user checkpoint and wait for approval before advancing that unit or using its
output downstream. Work already assigned to the other parallel subplan may
finish while that checkpoint is pending. Do not start integration until both
subplans have passed their checkpoints.

3. **S3 — Integrate the evidence** (root-level implementation assignment)
   - **Action:** After both subplans and user checkpoints are complete, assign
     one agent to synthesize the two reconciled audits into the root Outcome.
     The synthesis must compare the two mechanisms, distinguish hypothetical
     stakes from actual consequential settings or incentives, and assess
     whether a controlled follow-up experiment is warranted. It may outline a
     design if useful but must not run an experiment or add unresearched
     claims.
   - **Output:** A concise, cited synthesis in the root plan's Outcome section,
     ready to present to the user.
   - **Exit check:** Each conclusion is traceable to one or both reviewed
     audits; conflicts, transfer limits, uncertainty, and the basis for any
     experiment recommendation are stated.

## Completion criteria

- Both assigned evidence audits and independent reviews are complete and
  reconciled, with a user checkpoint after each subplan.
- A distinct agent has completed the root integration assignment after both
  subplan approvals, and the coordinator has reconciled its synthesis.
- The integrated answer distinguishes explicit importance wording, described
  stakes, and actual consequential settings or incentives.
- Conclusions are calibrated to the quality, scope, and consistency of the
  located evidence, with material null results, conflicts, and evidence gaps
  stated.
- Any proposed experiment is clearly identified as a proposal, follows from
  the evidence reviewed, and separates wording and stakes conditions while
  controlling task content; no experiment is run.
- The user receives a concise, cited synthesis that answers whether the
  available evidence indicates performance varies with these cues.

## Outcome

### Integrated finding

The reviewed evidence does not establish a reliable general performance boost
from telling an LLM that a task is important or describing consequences. It
does show that some cues can change outputs, with direction depending on the
wording, task, model, and measured outcome. The evidence is focused and
heterogeneous, not a systematic review or a pooled estimate.

- **Generic importance wording:** Positive results come mainly from the
  EmotionPrompt research program. Its “very important to my career” cue also
  implies personal stakes, while other prompts add encouragement or requests
  to re-check. The same research program reports task-dependent positive and
  poor results for that cue ([Li et al., 2023](https://arxiv.org/abs/2307.11760);
  [Li et al., 2024](https://arxiv.org/abs/2312.11111)). An independent
  conceptual replication found a pooled accuracy change of -0.25 percentage
  points, with benchmark changes in both directions and no statistically
  significant difference for nearly all tested techniques
  ([Vaugrante et al., 2025](https://openreview.net/forum?id=bgjR5bM44u)).
  That non-significance does not establish equivalence or rule out small or
  task-specific effects. Overall, evidence for a bare “this is important/high
  priority” cue is especially limited because the available prompts do not
  cleanly isolate it from personal stakes or other instructions.
- **Described stakes:** Results are mixed. In a GPT-4 radiology exam study,
  encouragement and a responsibility disclaimer scored above the baseline,
  while liability and clinical-responsibility personas scored lower and
  abstained more ([Nguyen et al., 2024](https://doi.org/10.1016/j.clinimag.2024.110276)).
  The independent review confirmed the direction in the publisher abstract,
  but could not verify the audit’s exact reported counts (60/106, 69/106,
  68/106) because the article results were not accessible. A simulated
  deployment threat elicited deliberate underperformance in some models
  ([Meinke et al., 2025](https://arxiv.org/abs/2412.04984)); an explicit
  error-cost scoring rubric shifted models toward abstaining more at higher
  stated costs ([Kalai et al., 2026](https://doi.org/10.1038/s41586-026-10549-w)).
  These are respectively a strongly elicited simulated incentive and a
  communicated decision rule, not evidence that ordinary harm/benefit
  narratives improve accuracy. In contrast, a 23-model, eight-task working
  paper found no statistically detectable general accuracy effect from a
  verbal bonus promise ([Belotti et al., 2026](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6594418));
  that null does not prove an exactly zero effect.
- **Actual consequences:** The retained evidence does not test real-world
  consequences imposed on an LLM or downstream human outcomes made contingent
  on its answer. Prompts describing consequences, simulated deployment
  environments, and hypothetical scoring rules must not be treated as actual
  external consequences. The gap is unresolved, not evidence that actual
  consequences have no effect.

Confidence is moderate that selected importance-adjacent or consequence-related
prompts can alter behavior in particular controlled settings, but low that
either generic importance wording or ordinary described stakes produces a
consistent change in correctness across tasks and models. Effects on
calibration, time, tokens, and compute are not established in these audits;
abstention and response rate are the more directly observed response outcomes.

### Follow-up experiment proposal

A controlled follow-up is warranted because the key constructs have not been
cleanly separated and the current results vary by task and cue. This is a
proposal only; no experiment is being run. Use the same tasks, task
information, and evaluation procedure across a 2x2 design:

| Condition | Generic importance wording | Described stakes |
| --- | --- | --- |
| Neutral | No | No |
| Wording-only | Yes | No |
| Stakes-only | No | Yes |
| Both | Yes | Yes |

Predefine task-specific quality/correctness as the primary outcome, with
multiple task types and model versions and sufficient repeated runs to assess
variation. If measured consistently, calibration and response behavior
(including abstention) can be secondary outcomes; token use or latency may
also be recorded as costs. The central confound is that stakes text can add
task information or change the decision rule, rather than only signal
importance. Keep the underlying information and requested action constant,
avoid explicit scoring instructions in the stakes wording, and separately
document or manipulate any information the narrative necessarily adds. The
design would estimate prompt effects in its tested setting; it would not by
itself establish effects of actual external consequences or generalize to all
models and tasks.
