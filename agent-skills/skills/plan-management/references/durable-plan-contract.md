# Durable plan contract

This reference is for the coordinator creating, revising, or coordinating a
durable repository plan. It defines plan structure, workflow settings, artifact
scaffolding, and execution gates. The coordinator uses it to prepare complete
assignments and artifacts. Assigned researchers, implementers, and reviewers
work from the brief and output locations the coordinator provides; they do not
need this reference to perform their bounded task.

The coordinator owns continuity with the user, plan decisions, assignment
briefs, checkpoints, and integration. It may make small plan or workflow
artifact corrections with the user's agreement. It does not perform assigned
research, implementation, or formal review. Every enabled research and review
stage and all substantive implementation work go to one or more agents. The
coordinator checks and reconciles their returns, but that coordination is not
an independent review. A reviewer must be distinct from the coordinator and
from the implementer whose work is under review.

## Plan setup and execution settings

Recommend a subplan count and execution settings based on task complexity,
dependencies, assurance needs, parallel work, and where focused LLM execution
benefits from smaller tasks. Keep the plan concise; do not add phases, workflow
stages, or deliverables without a concrete need.

Treat research as support for subplan implementation. Enabling research for
subplans does not authorize research on the overall plan. Root-level research
is off unless the user explicitly requests research for the root objective;
record that request with `execution.root_research`.

After drafting the root and subplans with the user, delegate a plan-integrity
check before implementation or plan research begins. The reviewer checks the
root and subplans for logical coverage, sequence, dependencies, feasibility,
and consistent completion conditions. The reviewer writes findings to the
temporary `plan-integrity-check.md` beside the root `PLAN.md`. Reconcile the
findings, make any agreed plan edits, then delete the temporary file. Do not
assign a `REV` identity or treat this as a review of completed output. If
independent delegation is unavailable, report
that the integrity gate could not be completed; do not present a self-review as
independent. Use `$agent-delegation` review procedures for independence and
evidence standards; the temporary file is the only review output for this gate.

Assign implementation to agents for plans with or without subplans. Use one
agent when the work is cohesive; use multiple agents only for bounded work with
non-overlapping responsibilities. The coordinator remains responsible for
reconciliation and integration.

Before scaffolding, ask the user to choose or confirm:

- the number of subplans;
- whether subplan research is off or enabled with a setting defined by
  `$research`;
- the `$research` setting for root-level research only if the user explicitly
  requested research on the root objective;
- whether subplan output review is enabled;
- whether plan-local research discovery logs are retained when research is
  enabled;
- the user checkpoint cadence.

Set `root_research: false` unless the user explicitly requests research for
the root objective. If requested, record the rigor level defined by `$research`
in `root_research`. The `research` setting controls only research assigned to
subplans. When neither setting enables research, record `research_working:
false` without asking. When either enables research, recommend not retaining
working logs unless durable search-path history would help with traceability or
later review; explain the tradeoff and let the user choose. Pass all research
settings through verbatim. `$research` owns rigor-level names and meanings.

The `review` setting controls formal reviews of completed subplan outputs only.
The temporary root plan-integrity check is mandatory for durable plans and is
not controlled by `review`. Its reviewer must be an agent other than the
coordinator.

Recommend `each_handoff` for plans with agent assignments. Also offer
`each_subplan` and `plan_completion`; explain their effect and let the user
choose. Record the agreed settings in root frontmatter. Subplans inherit them.
Ask before adding local exceptions.

The workflow settings are independent:

- `research`: `false` or a rigor level defined by `$research`; enabled research
  is assigned to researchers for subplans only.
- `root_research`: `false` or a rigor level defined by `$research`; enabled
  only when the user explicitly requests research on the root objective.
- `review`: boolean; `true` requires an independent review gate for each
  completed subplan output; `false` disables those output reviews.
- `research_working`: boolean chosen by the user when research is enabled;
  `false` when it is disabled.
- `user_checkpoints`: one of `each_handoff`, `each_subplan`, or
  `plan_completion`.

Subplans inherit `research`, `research_working`, `review`, and
`user_checkpoints`. A subplan may override only dimensions that differ, using
values defined here or by the workflow that owns that dimension. It may
override `research_working` after the user agrees to the local retention
choice. `root_research` applies only to the root and cannot be overridden by a
subplan. Omit `execution_exception` when no override is needed.

## Scaffold and assignment preparation

After the user confirms the settings, run the creator from this skill's
directory:

```bash
python3 scripts/create_plan.py <repository> \
  --subplans <count> \
  --research <false-or-setting-from-research> \
  --root-research <false-or-setting-from-research> \
  --research-working <true|false> \
  --review <true|false> \
  --user-checkpoints <each_handoff|each_subplan|plan_completion>
```

The default destination is `<repository>/plans/`; pass `--destination` to use
another directory. The creator reserves IDs and creates root and subplan
`PLAN.md` scaffolds. It creates a root research audit only when
`root_research` is enabled, and subplan research audits only when `research` is
enabled. It creates review assessments for subplans only when `review` is
enabled. It creates research `.working` scaffolds only when retention was
selected. These workflow files contain relationship metadata and empty content
sections. The coordinator completes the briefs and assignment content,
including subplan review targets and criteria, before validation. The
coordinator creates `plan-integrity-check.md` after the root and subplan briefs
are complete and delegates the check before presenting the finalized plan for
approval. The file is deleted after findings are reconciled. If an approved
subplan exception enables working-log retention while the root setting is
false, create a `.working` scaffold for that subplan's research assignment.

Agent assignment does not create a plan artifact or identity. Assigned work
continues the same plan unit and workflow artifacts. Do not create a
delegation entity or `DEL-*` ID, a separate subplan solely for an agent, or a
persistent agent history in the artifact graph.

Complete the draft root plan, subplan briefs, and workflow assignments, then
run the plan-integrity check. Reconcile its findings and delete the temporary
file. Present the finalized plan with the execution contract and wait for the
user's agreement on scope, outputs, sequence, gates, and settings before
starting root research, subplan research, implementation, or output reviews.
That agreement authorizes those execution assignments subject to the selected
checkpoint cadence.

Plan IDs and workflow IDs are allocated by the shared `scripts/artifact_ids.py`
allocator, not chosen by agents. The repository-level
`.plan-management/id-reservations.json` ledger prevents reuse and concurrent
claims. It records reservations, not file paths, and seeds from IDs found in
the repository on first use. The validator builds an in-memory ID index for
checking references and anchors.

## Plan identities and references

A durable plan has root and subplan entities:

- A root entity has an ID such as `LR-01`; its plan artifact is `LR-01.PLAN`.
- A subplan entity has an ID such as `LR-01.SP-03`; its plan artifact is
  `LR-01.SP-03.PLAN`.
- Artifact IDs extend the entity ID with the artifact role. Type codes and
  canonical artifact roles use uppercase; descriptive roles use lowercase.
- Root plan IDs use a repository-wide sequence. Subplan IDs share a sequence
  within their root. Ordinals have at least two digits. Removed IDs are never
  reused.
- Relationships use stable IDs, not paths. Use `ID#anchor` for a section
  reference. Do not keep a second manual path registry.

## Plan metadata

Every root and subplan `PLAN` uses YAML frontmatter with these base fields:

```yaml
---
plan_id: LR-01.SP-03
kind: subplan
parent: LR-01
phase: S2
status: in_progress
depends_on: [LR-01.SP-02.RESULT]
consumers: []
execution_exception:
  review: true
---
```

A root uses `kind: root`, `parent: null`, and `phase: root`. It also declares
the agreed `execution` defaults:

```yaml
execution:
  research: standard
  root_research: false
  research_working: false
  review: true
  user_checkpoints: each_handoff
```

Field meanings:

- `plan_id`: assigned plan entity ID.
- `kind`: `root` or `subplan`.
- `parent`: `null` for a root; parent plan entity ID for a subplan.
- `phase`: `root` for a root; parent's phase identifier for a subplan.
- `status`: the standardized lifecycle value `not_started`, `in_progress`,
  `blocked`, or `complete`. Keep it concise; use the root plan's `Current
  phase` section for execution detail.
- `depends_on`: output IDs that condition this unit's advancement; not a
  general-purpose input or provenance list.
- `consumers`: destinations outside the plan graph; use an empty list when
  there are none. Consumers inside the graph declare dependencies in their own
  `depends_on` field.
- `execution`: required on the root only; contains the settings above.
- `execution_exception`: optional on a subplan; contains only local deviations
  from root defaults.

Do not add `consumes` or `produces`. `depends_on` records advancement
conditions, `belongs_to` associates an artifact with its entity, and
`derived_from` records content provenance. Do not copy plan frontmatter to
other artifact types; their required fields depend on the artifact.

## Plan content and workflow artifacts

The root `PLAN` maps the overall effort. State the overall objective, approach
and boundaries, current phase, a concise ordered phase map in `Sequence` with
links to its subplans, and the global completion gate. The `Current phase`
section records the active phase, the decision or handoff currently pending,
and the next action. When progress is blocked, name what is blocking it and
what will unblock it; do not merely restate that execution is paused or repeat
the lifecycle value from frontmatter. Do not repeat subplan links in a
separate tree or index section; each subplan's `parent` metadata records its
place in the hierarchy. Put detailed phase objectives, scopes, inputs,
outputs, and completion conditions in their subplans. Do not repeat each
subplan's execution brief in the root.

A subplan `PLAN` is the executable brief for one bounded task. Define its
objective, scope, relevant inputs, expected output, and completion condition.
Refer to inputs by ID. Do not redefine the root objective or repeat the root
plan. When repository knowledge could inform the task, follow the root context
map to its knowledge entrypoint and consult only relevant entries. Record
material `KNOW` IDs as inputs, not as `depends_on` gates unless an output must
be satisfied before the task can advance.

Record completion, verification, and material differences from the brief in a
short `Outcome` section of the subplan `PLAN`. Do not repeat its objective or
completion conditions there. Create a separate `RESULT` only when a standalone
consumer-facing deliverable must be consultable as its own artifact.

Workflow artifact relationships:

- Research and review artifacts declare `belongs_to` their workflow entity.
- Research artifacts identify the requesting root or subplan with
  `requested_by`; formal review artifacts identify the requesting subplan.
- Subplan review assignments declare concrete `targets` and `criteria_refs`.
- Knowledge records declare concrete source artifacts in `derived_from`.
- Each workflow owns the substantive content standards for its artifacts.

Use `depends_on` only for a condition that must be satisfied before a unit
advances. When a unit must wait for an output, reference that output ID there.
The dependency alone does not mean the output is ready for use.

## Research assignment artifacts

Each assigned research unit uses a `RES` identity. The coordinator decides
whether work continues an existing research ID or starts a new assignment.
Deepening a question, checking missing evidence, changing agents, or adding
sources does not by itself create a new ID. Research IDs use a sequence unique
within the root plan and shared by subplans; use two-digit ordinals and never
reuse removed IDs. Do not create a delegation ID.

The research entity has two artifact roles:

- `<RES-ID>.working` holds disposable discovery material: queries, paths,
  candidates, hypotheses, unverified notes, and temporary logs.
- `<RES-ID>.audit` holds curated, verifiable support: material claims,
  evidence, sources, provenance, conflicts, limitations, and validation.

The creator scaffolds a root research audit only when `root_research` is
enabled by the user's explicit request. It scaffolds a subplan audit for each
subplan where `research` is enabled. It scaffolds a working file only when the
effective `research_working` setting is true. Subplans inherit `research` and
may override it with an approved `execution_exception`. Each file declares
`belongs_to: <RES-ID>`; the audit also declares `requested_by:
<PLAN-ID-or-subplan-ID>`. IDs are canonical; resolve them to current paths for
file access. Keep research artifacts directly in the requesting unit's
directory, beside its `PLAN.md`, until a knowledge promotion carries them into
repository knowledge. Scaffold root research artifacts only when the user
explicitly requested root research. Do not create a separate `RESEARCH.md` for
the unit.

The coordinator supplies the requesting plan unit and its objective, scope,
constraints, applicable guidelines, artifact IDs and locations, and intended
consumer-facing destination. The researcher follows `$research` for evidence
quality and returns the output, material conclusions and uncertainties, and
any unmet requirement. Research itself does not create a separate `RESULT`.

## Review assignment artifacts

Each formal subplan output review uses a `REV` identity. The coordinator declares
whether an assignment continues an existing review or starts a new one. Keep
the ID when checking fixes or verifying corrections; a new assignment gets a
new ID. Review IDs use a sequence unique within the root plan and shared by
its subplans. Delegation does not create another ID.

Before review starts, the coordinator completes the scaffolded `assessment`
frontmatter with:

- `belongs_to`: the review entity ID;
- `requested_by`: the requesting subplan ID;
- `targets`: concrete artifact IDs being evaluated; and
- `criteria_refs`: IDs or `ID#anchor` references to evaluation criteria.

All assignment fields are required. Additional materials may be supplied as
references but are not targets unless listed in `targets`. The assessment is
the final review artifact. Optional independent perspectives use numbered
descriptive roles such as `.perspective-01`; they are not required when one
reviewer can produce the assessment directly. Keep formal review artifacts
directly in the requesting subplan's directory, beside its `PLAN.md`. Do not
create a formal review artifact for the root's completed output. Do not copy
the target into the subplan directory.

The coordinator's subplan brief and assessment frontmatter define the review
assignment; do not create a separate assignment document. When independent
perspectives are assigned, the coordinator checks and integrates them into the
final assessment while preserving supported disagreement and uncertainty.
With one reviewer, that reviewer may prepare the assessment directly; the
coordinator still checks it against the targets and criteria. The reviewer
must not edit another reviewer's perspective or the coordinator's final
assessment.
`$agent-delegation` defines how to conduct and reconcile subplan output reviews.

## Execution sequence, checkpoints, and output availability

The main agent completes the root and subplan briefs with the user, then
delegates the temporary plan-integrity check. Create the named file and give
the reviewer the root plan, subplans, and these criteria: logic and coverage,
ordering, dependencies, feasibility, and consistent completion conditions.
The reviewer records concise findings, evidence in the plan, and recommended
corrections in that file. Reconcile the check, make agreed edits, and delete
the file before presenting the finalized plan and execution contract for user
approval. Do not start root research, subplan research, or implementation
before that approval.

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

For durable plans, keep artifacts beside the unit that coordinates them until
they are promoted into repository knowledge. Subplan-specific research and
review artifacts live directly in that subplan's directory. Root research
artifacts live at the root only when explicitly requested. Plan-local knowledge
is shared by the root and subplans, so it lives only in the root plan's
`knowledge/` directory. The creator makes that directory even when empty. A
typical layout is:

```text
<plan>/
├── PLAN.md
├── knowledge/
└── subplans/
    └── <subplan>/
        ├── PLAN.md
        ├── RESULT.md       # only for a required standalone deliverable
        ├── <RES-ID>.audit.md       # when research is enabled
        ├── <RES-ID>.working.md     # only when working-log retention is enabled
        └── <REV-ID>.assessment.md  # when output review is enabled
```

The root may temporarily contain `plan-integrity-check.md`; delete it after
reconciliation. Consumers refer to shared artifacts by ID; do not copy
artifacts into a consumer's directory or change their membership to the
producing entity.

## Status, closure, and validation

Use only `not_started`, `in_progress`, `blocked`, and `complete` for durable
plan units. Agreed requirements are mandatory. Resolve minor issues within the
approved scope. `blocked` means progress is paused for a user decision; it is
not a final state or a way to accept incomplete work. If a requirement cannot
be met within scope, stop and explain the affected requirement and blocker.
After the user's decision, update the plan if needed and resume as
`in_progress`. `complete` means the unit's work has ended; output availability
still depends on the gates above.

When a durable plan reaches `complete`, verify outputs, dependencies,
consumers, and owned information. Before asking whether to archive or delete
the plan, compare reconciled outputs with repository knowledge and surface
likely reusable candidates, or say none were found. For each candidate, state
its utility, limitations, proposed create-or-update action, and source
artifacts. Do not create or update repository knowledge until the user
approves. If approved, follow the [repository knowledge structure](../../context-architecture/references/knowledge.md).
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

Use the repository's plan validator. It checks structural requirements, IDs,
references, and supported relationships; it cannot judge whether an objective
or output is substantively right. For this repository, run from the
`agent-skills/` directory:

```bash
python3 skills/plan-management/scripts/validate_plans.py <repository>
```

Use strict validation when adopting the contract or when selected plans are
expected to comply already. Treat existing plans without required metadata as
migration work; do not rewrite them merely to silence warnings.
