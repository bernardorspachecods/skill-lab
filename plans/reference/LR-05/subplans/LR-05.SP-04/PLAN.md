---
plan_id: LR-05.SP-04
kind: subplan
parent: LR-05
phase: S4
status: in_progress
depends_on:
  - LR-05.RES-01#claims-and-evidence
  - LR-05.RES-02#claims-and-evidence
  - LR-05.RES-03#claims-and-evidence
consumers: []
execution_exception:
  research: false
  research_working: false
---

# LR-05.SP-04

## Objective

Use the full reviewed evidence base to recommend clear implementation
strategies for incorporating supported loop patterns into the repository's
skills workflow.

## Scope

Synthesize the approved S1–S3 audits before assessing the local workflow.
Identify what the evidence supports, where findings conflict or remain
uncertain, which outcomes matter, and what transfer limits apply. Then inspect
the canonical `plan-management`, `research`, `brainstorm`, `agent-delegation`,
`skill-authoring`, and `context-architecture` guidance to locate possible
implementation points.

Compare materially different strategies using explicit, balanced criteria,
including evidence strength and transfer, user control, expected outcome,
measurement independent of the loop's own signal, operational cost,
reversibility, failure risk, and maintenance burden. Do not treat the current
workflow as the default or presumed recommendation. Include no change as a
comparator, not as a preferred answer. Clearly separate research findings
from local observations and implementation inferences.

For each proposed strategy, state the target skill and workflow step, local
need, feedback signal, action and handoff, prerequisite, safeguards, expected
benefit, independent measure, cost, risk, and evidence for transfer. Give a
clear recommendation and an appropriate next step. Recommend no change if no
strategy is sufficiently supported. This subplan performs no new external
research, edits no skills, and changes no active workflow.

## Output

Complete the Outcome section with a reviewed, source-traceable analysis and
clear implementation strategies, tradeoffs, uncertainties, and recommendation.
After user approval, this Outcome becomes the root plan's final Outcome.

## Sequence

1. **S1 — Evidence-first integration analysis**
   - **Action:** Assign an agent who did not produce the S1–S3 research audits.
     First synthesize the approved audits without using the superseded S4
     recommendation. Then inspect the named canonical skills, compare options
     against the stated criteria, and draft implementation strategies.
   - **Output:** A complete Outcome assessment with balanced alternatives,
     evidence links, transfer assumptions, and measures.
   - **Exit check:** An independent reviewer accepts the assessment; the
     coordinator reconciles it; the user approves the S4 checkpoint.

## Completion criteria

- The assessment accurately synthesizes S1–S3, including positive, null,
  mixed, adverse, and uncertain findings.
- Evidence synthesis is kept distinct from local skill observations and
  transfer inferences.
- Options are compared against explicit, balanced criteria; the current
  workflow is not privileged as the presumptive answer.
- Every proposed strategy names concrete skills/workflow points, actions,
  signals, safeguards, independent measures, costs, risks, and prerequisites.
- The recommendation is clear and calibrated; it may recommend no change.
- No external research, skill edit, or active workflow change is made.
- An independent review is reconciled and the user checkpoint is approved.

## Outcome

### Recommendation

**Do not add a default self-critique loop or a new cross-skill loop rule now.**
Keep the existing task-specific checks and human handoffs. If a recurring gap
later appears in work with an independent, task-relevant verifier, test a
single bounded correction cycle in one low-risk task before considering any
skill change. The approved research does not establish that adding a loop to
these skills improves outcomes, while the canonical guidance already includes
several relevant review and verification steps.

This recommendation is limited to the local skills workflow. It is an
implementation judgment from the evidence and local inspection below, not a
finding that loops are generally ineffective.

### Evidence-first synthesis

S1 maps different mechanisms: revision of a current artifact, tool/action and
observation, human-guided learning, preference training, retrieval feedback,
user/recommender cycles, deployment monitoring, and governance. Their
feedback signals and changed objects differ; “loop” is not one intervention
with a common outcome ([S1 audit](../LR-05.SP-01/LR-05.RES-01.audit.md#claims-and-evidence),
C1–C10).

S2 found useful applications but mixed, task-bound results. Self-Refine
improved several benchmark and preference measures, while some already-valid
programs did not improve and weaker models sometimes failed to use feedback.
Code execution/self-debugging improved selected code tasks, with little
marginal gain after the first turn on one Spider analysis. RLHF, retrieval
rewriting, document annotation, adaptive experiments, recommender correction,
and scientific discovery used materially different signals and measures.
Annotation showed quality/efficiency tradeoffs; adaptive-bandit results were
mixed and sparse ratings constrained interpretation; the recommender
correction was simulation-based; CAMEO reported a discovery without a
non-loop comparator. Monitoring studies and guidance document operational
processes and post-deployment fragility, but not a causal benefit from
monitor-triggered remediation ([S2 audit](../LR-05.SP-02/LR-05.RES-02.audit.md#claims-and-evidence),
C1–C9; E1–E12; “Findings by setting and mechanism”).

S3 makes evaluation design central. Strong baselines, comparable resources,
initial-output quality, task-relevant verification, and outcomes separate from
the optimized score affect what a result means. Same-model evaluators and
human labels can vary; proxy scores can rise while human-valued outcomes or
safety constraints worsen in studied settings. Repeated revision can help,
leave a result unchanged, or damage it. Trained self-correction provides a
bounded counterexample to blanket skepticism, but does not establish transfer
to a skills workflow. Available deployment-monitoring evidence does not test
causal remediation benefit; relative costs, cross-domain transfer, and
failure prevalence remain unknown ([S3 audit](../LR-05.SP-03/LR-05.RES-03.audit.md#claims-and-evidence),
C1–C8; especially E1–E8 and E12–E14; “Conflicts, limitations and open
evidence”).

### Local workflow observations

The named canonical skills already use mechanisms resembling bounded feedback
and independent checking:

- [plan-management](../../../../agent-skills/skills/plan-management/SKILL.md)
  defines intended outcomes, work, and completion conditions; it assigns
  research, implementation, and optional formal review to distinct agents,
  with coordinator reconciliation and user checkpoints. It also says the
  coordinator does not act as the researcher, implementer, or reviewer.
- [research](../../../../agent-skills/skills/research/SKILL.md) calls for
  claim/evidence links, separate source-quality, claim-fit and independence
  assessments, conflict/refutation checks, uncertainty, and a reasoned stop.
  These checks evaluate evidence provenance and claim support; they do not in
  themselves measure whether a recommended local workflow improved user
  outcomes.
- [brainstorm](../../../../agent-skills/skills/brainstorm/SKILL.md) already asks
  for visible tradeoffs and a recommendation, a running decision log, genuine
  reconsideration when challenged, and periodic checks for drift or
  contradiction. It emphasizes making the basis of critique legible.
- [agent-delegation](../../../../agent-skills/skills/agent-delegation/SKILL.md)
  requires a review target to be stable before review, keeps reviewer and
  executor boundaries separate, and assigns the coordinator responsibility
  for checking and reconciling the handoff.
- [skill-authoring](../../../../agent-skills/skills/skill-authoring/SKILL.md)
  has final checks for invocation, frontmatter, links, policy, and duplicated
  or overbroad process. It cautions against adding modes or branches without
  a concrete use and verification need.
- [context-architecture](../../../../agent-skills/skills/context-architecture/SKILL.md)
  requires examining relevant documents and consumers before refactoring,
  keeps one canonical owner for information, and gives concrete verification
  checks and a non-mutating validator for context architecture.

These steps provide existing human checkpoints, evidence checks, code or
document validation, and independent review where enabled. Local inspection
does not show outcome data comparing them with alternative workflows, nor a
recurring defect that an additional generic loop would address.

### Options compared

| Strategy | Evidence and transfer | User control and independent outcome measure | Cost, risk, reversibility, maintenance |
|---|---|---|---|
| **A. No new loop rule; retain the current task-specific checks** | Strong fit to the local process as written, but no direct evidence that the current skill set is superior. Research supports the existing distinctions among evidence checks, validators, and independent reviews; it does not show that adding another pass improves these skills. | Existing user checkpoints and human authority remain. For any later comparison, use independently sampled reviewer corrections, unsupported-claim or validation-defect rates, downstream task success, and user-visible rework; do not use an LLM's own pass score as the outcome. | No added loop-specific maintenance or recurring inference cost. Existing review/checkpoint work remains. Risk: a real unobserved gap persists; reversibility is high because a later targeted pilot remains possible. |
| **B. Require repeated same-model critique and rewrite for outputs across the named skills** | Weak transfer. S2/S3 show some positive cases, but also null or adverse outcomes; evaluator scores can diverge from human judgment, and evaluator stability is not guaranteed. Trained policy results do not support a prompted self-critique default. | A rubric or model-generated critique is the signal; the same model revises until a pass or fixed round limit, then hands off. User control can be reduced if a confident score masks a defect. A blinded independent reviewer or external task measure would still be required. | High recurring latency/token cost and maintenance of rubrics/stop rules. Risks include proxy gaming, repeated damage, false confidence, and convergence being assumed from a pass score. Easy to disable, but broad coverage increases burden. |
| **C. Add a gated external-check-and-one-correction cycle for independently verifiable tasks** | Mechanistically plausible where a check genuinely measures the task: research claim/source checks, code or static checks, and context-architecture validation are represented locally and in S1/S2. S2/S3 provide task-bounded support for tool-verifiable code and retrieval, but no evidence of incremental benefit over the existing local checks or transfer to broad planning/brainstorm work. | Trigger only when a plan states an objective external check and the first check finds a material defect. Signal is a test, source passage, architecture validator, or independent reviewer. Producer gets one bounded correction pass; the same checker or a different reviewer verifies; unresolved mismatch goes to the coordinator/user instead of another automatic retry. Require user/plan authorization for scope changes. Measure defect detection and resolution by an independent reviewer plus total task time/rework and user outcome. | Adds verifier setup, reviewer coordination, and correction time. Risks include incomplete tests or validators, over-reliance on a single proxy, and duplicate review rules. Highly reversible as a one-task pilot; making it a generic skill rule would create maintenance and inappropriate-trigger risks. |

The criteria are evidence fit, relevance to the local workflow, user control,
measurement independent of the loop signal, operating cost, failure risk,
reversibility, and maintenance burden. Strategy B performs poorly on evidence
and evaluator reliability despite being easy to describe. Strategy C has a
clearer external signal but overlaps with checks and review gates already
present, and its incremental benefit is unmeasured. Strategy A does not claim
the present workflow is optimal; it avoids imposing an additional process
without a demonstrated local problem or measurable expected gain.

### Strategy details

**A. No new loop rule; retain current task-specific checks (recommended).**

- **Target and local need:** Existing acceptance and review points in
  `plan-management`; claim/source validation in `research`; stable-target
  review and handoff in `agent-delegation`; final checks in `skill-authoring`;
  and the non-mutating architecture validator in `context-architecture`.
  The local inspection found no repeated failure that the skills currently
  leave without an applicable check.
- **Trigger, signal, action, and handoff:** Use the trigger already stated by
  each workflow: a planned research review, a stable artifact assigned for
  independent review, a skill's final check, or a context-architecture
  validation need. Signals remain the source evidence, reviewer findings,
  explicit skill criteria, or validator output. The assigned researcher or
  author addresses findings under the existing task scope; the independent
  reviewer or validator checks its own criteria; the coordinator reconciles
  the result and presents the existing user checkpoint.
- **Prerequisites and safeguards:** A plan must already enable the relevant
  review/check or a skill's current validation trigger must apply. Preserve
  executor/reviewer separation, scope limits, user authority, and human
  escalation for unresolved or non-objective findings. Do not treat this
  assessment as evidence that the current workflow is optimal.
- **Expected benefit and independent measure:** Avoids adding unsupported
  process while retaining current controls; no incremental quality benefit is
  claimed. If later compared with a pilot, use an independent sample of
  reviewer corrections, unsupported-claim/validation-defect rate, residual
  defects, downstream task success, and user-visible rework. Record time and
  compute separately; these are outcomes, not claims that the baseline has
  already been measured.
- **Cost, risk, and transfer:** Adds no loop-specific cost or maintenance
  beyond the existing reviews/checkpoints. The risk is that an unobserved
  gap persists; the decision is reversible. Evidence supports the component
  mechanisms, not the superiority of this local combination.

**B. Default same-model critique and rewrite for all named skills (not
recommended).**

- **Target and local need:** A shared default added to
  `plan-management`, `research`, `brainstorm`, and skill-writing/validation
  workflows. Its proposed need would be to catch quality defects broadly, but
  the local inspection did not identify a recurring defect that justifies
  applying it to every output.
- **Trigger, signal, action, and handoff:** Trigger on every draft or
  deliverable; the same model scores its own output against a rubric, rewrites
  it, and repeats until the rubric passes or a fixed round cap is reached.
  Handoff occurs after that stop condition, with human review still required
  for material decisions.
- **Prerequisites and safeguards:** Requires a stable rubric and a round cap.
  A passing self-score must not replace source inspection, tests, an
  independent reviewer, or a user decision. Keep scope and permitted changes
  explicit and surface disagreement rather than silently iterating.
- **Expected benefit and independent measure:** It might improve consistency
  or catch omissions on tasks where the rubric matches the desired outcome;
  the supplied evidence does not establish this for the skills. Evaluate using
  blind independent review, externally verifiable task outcomes, and residual
  defect rates, not the model's own rubric score.
- **Cost, risk, and transfer:** Repeated inference adds latency and token
  cost, while maintaining rubrics and stopping rules adds upkeep. S3 records
  judge instability and proxy divergence (E4–E6, E11); repeated optimization
  may entrench a poor criterion or damage already-good work. This option
  assumes benchmark/refinement results transfer to open-ended skill behavior,
  for which no supporting outcome data were found. It is easy to disable but
  broad in reach and recurring in cost.

**C. Triggered external verification with one bounded correction cycle
(candidate for a later pilot only).**

- **Target and local need:** Existing research claim/source checks, the
  `skill-authoring` final checks, and `context-architecture` validation. A
  `plan-management` completion criterion could name the independent outcome
  measure for a future pilot. This pattern applies only when an objective
  check is available and current evidence shows a material defect; it is not
  suitable for every brainstorm or user-preference decision.
- **Trigger, signal, action, and handoff:** Trigger when a plan declares a
  specific verifier and its first pass flags a material defect. Use a primary
  source passage, test, validator, or independent review as the signal. The
  producer makes one bounded correction, then the same or another independent
  checker verifies it. If the signal is inconclusive or still fails, stop and
  hand the issue to the coordinator/user rather than retrying automatically.
- **Prerequisites and safeguards:** Before any pilot, agree the target
  defect, baseline, acceptance threshold, external signal and known blind
  spots. Keep review independent of the producer; tests cover only tested
  behavior, source support does not prove downstream usefulness, and a second
  opinion does not make a subjective judgment objective. Cap the cycle at one
  correction, preserve scope, and require human authorization for a change in
  intended outcome.
- **Expected benefit and independent measure:** Could resolve a detectable
  source, test, or structural defect before handoff, with fewer unverified
  defects reaching the user. Assess with blinded reviewer findings or an
  objective downstream task outcome, residual defects, correction acceptance,
  and user-visible rework; compare total elapsed time and compute with a
  baseline. No incremental benefit over existing checks has been measured.
- **Cost, risk, and transfer:** Requires setting up/maintaining the verifier,
  producer correction time, and a second check. An incomplete test, a weak
  source, or a mistaken review can send the correction in the wrong direction;
  adding a generic rule risks duplicating checks and increasing maintenance.
  A single low-risk pilot is reversible. Transfer is most plausible for
  code/source/structural correctness because S2 includes external-execution,
  query-retrieval, and annotation cases (E3, E5–E6), while S3 notes that
  reliable task-relevant external feedback is a favorable condition (E1–E2).
  None of those studies tests this exact skill workflow.

### Candidate pilot if a concrete gap emerges

If future tasks show repeated, consequential defects that current checks miss,
the most defensible first experiment is Strategy C on one low-risk, bounded
task, not a cross-skill default. The plan should state before execution:

1. the defect or outcome the cycle is meant to improve and a baseline from
   comparable prior work;
2. the independent signal and its known blind spots (for example, tests may
   miss behavior outside their coverage; source checking validates support,
   not downstream usefulness);
3. a cap of one producer correction pass and one verification handoff, with
   human escalation if the check remains inconclusive;
4. a blinded reviewer or objective outcome measure that is not the signal
   optimized during revision; and
5. total extra time/compute, correction acceptance, residual defects, and
   downstream/user outcome for comparison with the baseline.

This pilot is a possible later decision, not authorized work in this subplan.
No skill files or active workflow were changed. S1–S3 concern other AI tasks,
and their results do not predict a workflow effect here; that transfer
assumption must be tested locally before any reusable instruction is added.

### Decision and next step

Recommend **Strategy A now**: make no skill-level or active-workflow change.
Continue using the existing evidence, validation, independent-review, and
user-checkpoint steps when their current triggers apply. At the next user
checkpoint, review this comparison; if the user wants an effectiveness test,
first select a concrete low-risk task and agree on baseline, independent
measure, and stop condition before piloting Strategy C. Only observed benefit
with acceptable cost and no material quality regressions would justify
considering a narrow skill update. This outcome makes no claim that a loop
would be ineffective in a future, specifically measured use case.

### Handoff

The independent review accepted the replacement S4 assessment after six
canonical skill links were corrected and rechecked. Pending the user's S4
checkpoint approval.
