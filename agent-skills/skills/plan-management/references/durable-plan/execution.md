# Durable plan execution

Read [shared rules](shared-rules.md) with this file when coordinating work
under an approved durable plan. For initial plan creation, also read
[setup](setup.md).

Assign each enabled research stage, implementation stage, and formal output
review to agents as separate sequential stages. Use distinct agents for
different stages; a reviewer must be independent of both the implementer and
the coordinator. Research supports subplan implementation by default; root
research is assigned to a researcher only when the user explicitly requested
research on the root objective. The coordinator does not become the researcher
or implementer, even when the plan has no subplans. A subplan review starts
only after its output is complete and reconciled. After a review, the
coordinator discusses any needed small plan corrections with the user;
changes to the planned deliverable return to an implementer agent.

The root's `execution.user_checkpoints` controls when the coordinator pauses
for the user's review:

- `each_handoff`: after each agent returns, check and reconcile the handoff,
  show it to the user, and wait for approval before another assignment,
  advancing the unit, or making the output available downstream.
- `each_subplan`: continue through a subplan's enabled stages, then present
  the reconciled unit and wait for approval before the next subplan or
  downstream use.
- `plan_completion`: continue through the approved plan, then present the
  reconciled result and wait for review and approval. Pause earlier for a
  blocker, unmet requirement, or a decision that changes approved scope.

The approved execution contract authorizes in-scope assignments, but does not
waive required user checkpoints. If a request conflicts with plan settings or
scope, stop and reconcile the plan before proceeding.

An output becomes available to consumers after its producing unit is complete,
the coordinator has received and reconciled it, applicable dependencies,
review, and integration gates are satisfied, and any required checkpoint is
approved. File existence or a provisional result does not unlock downstream
work. Do not create a parallel artifact state machine.

To identify subplans eligible to start, derive the list from the root's
`Current phase`, each subplan's `status` and `depends_on`, output availability,
and the agreed execution gates. Include a `not_started` subplan only when it
belongs to the active phase, every output it depends on is available under the
rule above, and no blocker, pending decision, review, or user checkpoint
prevents work from starting. An empty `depends_on` satisfies only the
dependency condition. Do not advance to a later phase just because its
dependencies are satisfied. Report all eligible subplans and, when none are
eligible, the specific unmet condition for each candidate. Treat this as a
derived coordination view: do not add or persist a `ready` status. In-progress
subplans remain active work; blocked subplans remain blocked until the blocker
is resolved and their status is updated according to the status rules.
