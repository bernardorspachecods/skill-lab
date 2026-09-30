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

## Review assignment and output

Use the review assignment and artifact supplied by the coordinator. The
coordinator owns review IDs, frontmatter, paths, and plan relationships; do
not choose or change them, and do not create a separate assignment document.
The assignment identifies the concrete targets and criteria. Supporting
materials help interpret a target but are not themselves targets unless the
assignment says so.

Return the assigned assessment or perspective with conclusions supported by
evidence tied to the criteria, uncertainties, and recommendations. Optional
independent perspectives are separate assigned outputs; they are not needed
when one reviewer can write the final assessment directly. The coordinator
integrates perspectives into the final assessment while preserving supported
disagreement and uncertainty.

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

The reviewer reports the assigned output and its location, the criteria
considered, supporting evidence, uncertainties, and any unmet review
requirement. The coordinator verifies that the review covers the declared
targets and criteria before treating it as complete.

Review conclusions do not themselves make a target or its outputs available
downstream. The plan coordinator applies the review and integration gates in
the plan's execution cycle. Do not copy the assessed target into the review
artifact.

If delegated review is unavailable, say so explicitly and do not present the
primary agent's own assessment as independent.
