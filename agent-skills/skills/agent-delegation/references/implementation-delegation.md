# Implementation delegation

Use this reference when a delegated agent is expected to change files or
produce an implementation. The primary agent coordinates the assignment and
reconciles the result; the delegated agent may edit only within its assigned
write boundary.

## Assignment brief

Pass the agent the smallest brief that lets it complete and verify the work:

- the objective and expected output;
- the applicable plan and subplan IDs, when the work belongs to a durable
  plan;
- the inputs and relevant decisions, referenced by stable IDs where they are
  model relationships;
- the files or components the agent owns, and any write boundaries;
- constraints, completion conditions, and verification already performed or
  required by the plan.

Use the existing subplan as the assignment brief when it already provides this
information. Do not create a second plan or copy the entire parent plan. Resolve
IDs to current paths for the agent's operational use, while keeping IDs as the
canonical relationship references.

## Execution

1. Confirm that the requested implementation is within the user's request and,
   when applicable, the plan's approved scope. If completing it requires a
   scope change, stop and consult the user before assigning that change.
2. Follow the approved plan's assignment structure when it specifies one. If
   there is no plan, or the plan leaves the agent count unspecified, ask the
   user how many agents they want before assigning the work; do not default to
   one. Split work across agents only when their outputs and write boundaries
   are independent. Keep shared files under one writer and have the primary
   agent reconcile shared changes.
3. Give the agent authority to implement only the named work and edit only its
   assigned files. It may resolve minor issues within the approved scope. It
   must surface unmet requirements, material ambiguities, and scope changes
   rather than omit or work around them.
4. Use the smallest available isolation that prevents conflicting edits. For
   overlapping files, use a single writer or have agents return proposed
   changes without editing those files.
5. Require the agent to report what it changed, verification performed and
   results, remaining uncertainty, and any unmet completion condition.
6. Inspect the returned diff or deliverable against the brief. Check for
   out-of-scope changes, missed requirements, and relevant verification. The
   primary agent remains responsible for integrating and reconciling the work.

Delegation continues the same plan unit and artifact identities. Do not create
a delegation entity, `DEL-*` ID, separate subplan solely to represent the
agent, or persistent history of which agent worked on it.

When execution transfers to another agent, pass the current state of the work,
unresolved points, and next action with the existing unit and artifact IDs.
The incoming agent assumes that same unit; changing the executor does not
create a new identity or make provisional work complete.

## Coordination for larger assignments

Add coordination only when independent work, a long handoff, or several
contributors make it necessary. A concise temporary assignment brief may
record the objective, scope, owners, file boundaries, dependencies, outputs,
and completion checks. Keep it operational and temporary; it is not a node in
the plan graph and does not replace or duplicate the canonical plan.

Agents report and hand off their changes to the primary agent. The primary
agent checks the result and reconciles it into the canonical work. Do not
present provisional implementation as a completed plan output until the
producing unit is complete, the coordinator has received and reconciled it,
and applicable dependency, review, or integration gates are satisfied.

Delete temporary coordination material after the handoff is reconciled and no
decision is pending. Preserve it only while work or review is pending, or when
the user asks to retain it. This cleanup rule does not apply to canonical plan
artifacts or required implementation outputs.
