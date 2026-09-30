---
plan_id: LR-03
kind: root
parent: null
phase: root
status: in_progress
depends_on: []
consumers: []
execution:
  research: standard
  root_research: false
  research_working: false
  review: true
  user_checkpoints: each_handoff
---

# LR-03

## Objective

Improve the canonical `$research` skill so an LLM is better oriented to the
research goal, keeps the search within a useful scope, finds and evaluates
valuable sources, extracts direct findings, and presents them in a clear
consumer-facing form with supporting evidence kept auditable.

## Scope

Revise `agent-skills/skills/research/SKILL.md` and add or update a reference
only when a distinct branch of guidance needs its own focused context. Use the
five failure modes reported by the user as the design input: weak understanding
of the goal; overly broad scope; poor source selection; failure to turn good
sources into direct findings; and a blurred boundary between the consumer's
answer and internal evidence or guardrails.

Keep these concerns distinct during execution, then check that they work as one
workflow. Preserve the skill's existing evidence standards, uncertainty
handling, source provenance, untrusted-content rule, and artifact lifecycle
unless a change is needed to address the stated failures. Treat the reported
experiences as user observations, not evidence of how often all LLMs fail.
Do not build a new search tool or broaden the skill beyond web research unless
execution finds a concrete need and the user approves the scope change.

The canonical target is
[`$research`](../../agent-skills/skills/research/SKILL.md). Inputs also include
the user's five failure descriptions in this plan and the current skill text.

## Output

An integrated revision of the canonical `$research` skill, with any necessary
focused reference updates, that gives LLMs concrete orientation, scoping,
search, extraction, and delivery guidance. The consumer-facing answer and the
supporting audit trail should remain distinct and suited to their readers.

## Current phase

The required independent plan-integrity check is complete and reconciled; the
plan now awaits the user's approval before execution. No root-level research is
assigned. The former root research audit and root review scaffold are retained
in [history](history/) as records from the previous workflow, not as active
assignments or gates. The subplan research audits and review assessments are
active assignment scaffolds; all five subplans remain `not_started`. The
selected setting is `research_working: false`; no discovery-log files are
retained. After approval, execute one subplan at a time. Assign each enabled
research, implementation, and review stage to a distinct agent, then reconcile
each handoff with the user at the `each_handoff` checkpoint.

## Sequence

1. **S1 — Orient to the research goal** ([LR-03.SP-01](subplans/LR-03.SP-01/PLAN.md))
   - **Action:** Define how `$research` identifies the user's goal, intended
     decision or learning need, context, and material ambiguity.
   - **Output:** A focused update to the research brief workflow.
   - **Exit check:** The brief can distinguish the user's task from a broad
     topic and identifies when clarification could change the research.

2. **S2 — Bound the research scope** ([LR-03.SP-02](subplans/LR-03.SP-02/PLAN.md))
   - **Action:** Define how to turn the oriented goal into bounded questions,
     priorities, evidence needs, constraints, and stopping conditions.
   - **Output:** A focused scope and coverage update.
   - **Exit check:** Scope is actionable and proportionate, with the required
     gate from [LR-03.SP-01#outcome](subplans/LR-03.SP-01/PLAN.md#outcome) met.

3. **S3 — Improve source and search choices** ([LR-03.SP-03](subplans/LR-03.SP-03/PLAN.md))
   - **Action:** Improve source mapping, query paths, and the choice of valuable
     sites or source types for the scoped question.
   - **Output:** A focused search and source-selection update.
   - **Exit check:** Search paths match the question and preserve the existing
     distinction between source quality and claim support.

4. **S4 — Extract and synthesize direct findings** ([LR-03.SP-04](subplans/LR-03.SP-04/PLAN.md))
   - **Action:** Define how evidence is converted into findings that answer the
     user's question, including what each source establishes and does not.
   - **Output:** A focused extraction and synthesis update.
   - **Exit check:** Each material finding maps to evidence and addresses the
     intended question, with [LR-03.SP-03#outcome](subplans/LR-03.SP-03/PLAN.md#outcome) reconciled.

5. **S5 — Separate and shape the deliverables** ([LR-03.SP-05](subplans/LR-03.SP-05/PLAN.md))
   - **Action:** Specify the consumer-facing answer and its relationship to
     confidence, citations, and the supporting audit trail.
   - **Output:** An integrated `$research` revision and an account of the
     changes in the final plan outcome.
   - **Exit check:** The integrated skill addresses all five failure modes
     without blending internal records into the answer or duplicating rules.

## Completion criteria

- The current `$research` skill has been revised in the approved scope.
- Each of the five reported failure modes has a concrete response in the
  workflow or output contract; the overlap between direct findings and output
  structure is handled without duplicating guidance.
- The research brief, bounded scope, source strategy, extraction path, and
  consumer-facing output connect into one usable sequence.
- Evidence rules, source provenance, uncertainty, artifact lifecycle, and
  untrusted-content safeguards remain coherent with the new guidance.
- Examples or review criteria check a realistic task whose requested answer
  needs topics or situations, with confidence and source support available
  separately from the main answer.
- The plan's required research, review, integration, and user checkpoint gates
  are complete; references and skill structure pass the applicable validators.
