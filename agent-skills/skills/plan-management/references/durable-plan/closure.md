# Durable plan closure

Read [shared rules](shared-rules.md) with this file when completing a durable
plan. For work that includes the final execution handoff, also read
[execution](execution.md).

## Status and completion

Use only `not_started`, `in_progress`, `blocked`, and `complete` for durable
plan units. Agreed requirements are mandatory. Resolve minor issues within the
approved scope. `blocked` means progress is paused for a user decision; it is
not a final state or a way to accept incomplete work. If a requirement cannot
be met within scope, stop and explain the affected requirement and blocker.
After the user's decision, update the plan if needed and resume as
`in_progress`. `complete` means the unit's work has ended; output availability
still depends on the gates in [execution](execution.md).

## Reusable knowledge and plan retention

When a durable plan reaches `complete`, verify outputs, dependencies,
consumers, and owned information. Before asking whether to archive or delete
the plan, compare reconciled outputs with repository knowledge and surface
likely reusable candidates, or say none were found. For each candidate, state
its utility, limitations, proposed create-or-update action, and source
artifacts. Do not create or update repository knowledge until the user
approves. If approved, follow the
[repository knowledge structure](../../../context-architecture/references/knowledge.md).
As part of promotion, move every supporting research audit into repository
`knowledge/audit/`. Move a retained research working file into
`knowledge/working/` when it supports the promoted entry. Assign each moved
artifact a knowledge-owned ID such as `KNOW-01.AUD-01` or `KNOW-01.WORK-01`,
rename its file to match, and set `belongs_to` to the owning knowledge ID.
Preserve the former research ID, artifact role, and requester in
`source_artifact_id`, `source_artifact_role`, and `source_requested_by`. Update
`derived_from`, links, and references to the new IDs. Keep one canonical copy
and complete this migration before the plan can be deleted. This makes the
promoted entry's provenance independent of the plan's lifecycle.

The plan no longer needs to be retained to preserve promoted knowledge or its
research audits. Ask whether to delete the plan or move it to the relevant
`reference/` directory for its workflow history. Until the user chooses, leave
it in place and do not continue it or create another plan in its place.
