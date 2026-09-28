# Review delegation

Use this reference when an agent is assigned to evaluate a completed task,
implementation, plan, or other concrete target. A request for a quick opinion
or advice can use the lightweight **Advice** assignment in the main skill; use
this review contract when the work is a review activity with its own scope,
targets, criteria, and assessment.

A formal review in the shared artifact model is requested by a root plan or
subplan. For an unplanned, lightweight opinion, use **Advice** and return the
answer in the conversation rather than creating a review entity and its
artifacts. If the user requests a formal, persistent review and no existing
plan owns it, use `$plan-management` to establish the smallest suitable root
plan before assigning the review.

## Review identity and assignment

The coordinator declares whether this assignment continues an existing review
or creates a new one. Continuing a review keeps its ID when checking fixes,
completing it, or verifying corrections. A new review assignment gets a new
ID, even when its subject is similar. Adding perspectives or changing the
target does not by itself require a new review ID.

The tool assigns and reserves the review ID; agents do not choose a number. A
review ID uses the `REV` type code (for example, `LR-01.REV-02`) and the
sequence is unique within its root plan, shared by its subplans. Delegation
does not create an additional identity or a `DEL-*` ID.

Before the review starts, the review assignment's frontmatter declares:

- `requested_by`: the ID of the root plan or subplan that requested the review;
- `targets`: one or more concrete artifact IDs being evaluated; and
- `criteria_refs`: one or more IDs or `ID#anchor` references to the criteria
  used for evaluation.

All three are required. Materials that help interpret the target may be
included as optional references, but are not targets unless explicitly listed
in `targets`. References use stable IDs, not paths. Resolve IDs to current
locations for operational access. Store these assignment fields in the
frontmatter of the review's `assessment` artifact, which is created before the
evaluation begins; do not create a second assignment document.

The review's final output is one `assessment` artifact. Its artifact ID is the
review entity ID followed by `.assessment` (for example,
`LR-01.REV-02.assessment`). Its frontmatter links it to the review entity with
`belongs_to`, alongside the assignment fields above. Optional independent
perspectives use numbered descriptive artifact roles such as
`.perspective-01`; each links to the review entity with `belongs_to`. They are
not required when one reviewer can produce the final assessment directly. The
assessment records supported conclusions, evidence, uncertainties, and
recommendations relevant to the declared criteria. Synthesis is the act of
integrating perspectives, not an additional required artifact.

## Stable target and review boundary

Start only after the executor declares the assigned work complete and the
coordinator has received and reconciled its result. Keep every target stable
throughout evaluation. Reviewers may create or update the artifacts belonging
to their own review, but must not change the targets, implement recommendations,
or expand the assignment. If the review identifies required corrections,
return to execution; begin verification only after the executor completes and
the coordinator reconciles those corrections. Continue the existing review or
create a new one according to the coordinator's assignment.

Evaluate the work and its outputs against the declared targets and criteria.
Do not assess an individual agent's performance. Do not treat supporting
materials as targets or introduce criteria that are absent from the assignment
without clearly identifying the gap for the coordinator.

## Delegated reviewers

Use one reviewer by default. Add reviewers only when independent perspectives
or a distinct specialist view would materially improve the assessment. Assign
each reviewer one reserved perspective artifact with a distinct question or
angle. Reviewers must not read one another's perspectives while forming their
independent first assessments.

Each reviewer returns only the assigned perspective artifact, including
conclusions, evidence tied to the criteria, uncertainties, and recommendations.
The reviewer must not edit the target, another reviewer's artifact, or the
coordinator's final assessment.

The coordinator checks every perspective against the assignment and its
evidence. The coordinator authors the final `assessment` by integrating the
supported conclusions and preserving material disagreement and uncertainty.
With a single reviewer, that reviewer may prepare the assessment directly;
the coordinator still checks it against the declared targets and criteria.

## Handoff and completion

The reviewer reports the assessment or perspective ID and its resolved
location, the criteria considered, supporting evidence, uncertainties, and any
unmet review requirement. The coordinator verifies that the review covers the
declared targets and criteria before treating it as complete.

Review conclusions do not themselves make a target or its outputs available
downstream. The plan coordinator applies the review and integration gates in
the plan's execution cycle. Keep review artifacts with the root plan or
subplan that requested the review, in that unit's `reviews/` area; do not copy
the assessed target into the review directory.

If delegated review is unavailable, say so explicitly and do not present the
primary agent's own assessment as independent.
