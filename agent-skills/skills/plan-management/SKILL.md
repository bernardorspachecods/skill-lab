---
name: plan-management
description: >
  Turn an agreed objective into a clear, actionable plan, from a short plan in
  conversation to a durable plan with coordinated work. Use when the user asks
  to plan, structure, or revise work; use brainstorm to explore ideas and
  options before committing to a plan.
---

# Plan management

Turn an agreed objective into work that can be carried out and completed. Use
the same planning principles for a short plan in conversation and a plan that
must persist in a repository. Match the amount of structure and documentation
to the work; review, research, and delegation are optional workflows, not
requirements for making a plan.

Use `$brainstorm` when the user wants to explore an open question, compare
approaches, or reach a decision through discussion. Use this skill when the
user wants to turn an objective or an agreed direction into actionable work.
Resolve ordinary planning details as part of planning; do not route routine
clarification or short plans to another planning skill.

`context-architecture` owns repository context maps and `CURRENT-STATE.json`.
This skill owns durable plan structure and the organization of plan artifacts.

## Planning contract

A plan states what outcome is intended, the boundaries of the work, the work
needed to reach it, and how completion will be recognized. Plans can be kept in
the conversation for immediate use or recorded in the repository to preserve
ownership, dependencies, phases, status, or shared handoffs. Do not choose the
format on the user's behalf. If the user has not specified a format, ask whether
they want a conversation plan or a durable repository plan before drafting it.
Explain the difference neutrally and let the user choose.

Prefer splitting work into small, bounded subtasks that an LLM can handle with
focused context over assigning one large, continuous task. Keep related work
together when a single LLM can do it more effectively with continuity, or when
splitting would add coordination without improving execution. Keep the plan as
concise as the work allows, and do not add phases, research, review, delegation,
or deliverables without a concrete need. Do not create a parallel tracker when
a canonical plan already owns the work.

## Creating or revising a plan

1. Establish the objective and resolve any decision that would materially
   change the plan. Use the user's agreed direction as the basis; do not reopen
   settled decisions without a reason.
2. Identify the owner, scope, inputs, intended output, necessary steps, and
   completion condition. 
3. Record relationships and status in structured metadata when the plan is
   durable. Keep the body focused on the work and avoid repeating metadata or referenced material.
4. Update affected parent and child plans, dependencies, consumers, and status
   together when work is materially re-scoped or reorganized.
5. Validate durable plan structure and references with the repository's plan
   validator. Review substantive questions—such as whether the objective and
   deliverable are right—separately; a structural validator cannot decide them.

Recommend a subplan count and execution settings based on task complexity,
dependencies, assurance needs, parallel work, and where focused LLM execution
benefits from smaller tasks. 

For plans with subplans, recommend delegation by default: the primary agent
coordinates with the user, and agents execute the bounded subplan work. When
enabled, research and review are assigned to agents as separate workflow
stages; the reviewer must be independent of the implementer. For a root plan
without subplans, ask the user whether to delegate.

Ask the user to choose or confirm the subplan count, whether research is off or
enabled with a setting defined by `$research`, whether review is enabled,
whether to retain plan-local research working logs when research is enabled,
whether delegation is enabled, and the user checkpoint cadence. When research
is off, record `research_working: false` without asking. Recommend not
retaining working logs unless durable search-path history would help with
traceability or later review; explain the tradeoff and let the user choose.
Recommend `each_handoff` for delegated plans: after every agent returns work,
the primary agent checks and reconciles it, presents the handoff for user
review, and waits for the user's approval before starting or spawning the next
agent. Also offer
`each_subplan` (continue through a subplan's enabled stages, or the root unit
when there are no subplans, then wait for user review before continuing) and
`plan_completion` (continue through the approved plan, then present the
reconciled result for review and approval). The user may choose a different
cadence. Explain the recommendation and record the agreed contract in root
frontmatter; do not silently select settings. Subplans inherit these settings;
ask before creating any local exceptions.

After the user confirms, scaffold the plan with the creator. From this skill's
directory, run:

```bash
python3 scripts/create_plan.py <repository> \
  --subplans <count> \
  --research <false-or-setting-from-research> \
  --research-working <true|false> \
  --review <true|false> \
  --delegation <true|false> \
  --user-checkpoints <each_handoff|each_subplan|plan_completion>
```

The default destination is `<repository>/plans/`; pass `--destination` to use
another directory. The creator assigns and reserves IDs, creates root and
subplan `PLAN.md` scaffolds, and creates one initial research assignment or
review assessment scaffold for each plan unit where that workflow is enabled.
When research is enabled, it scaffolds the audit artifact for the durable plan
handoff. It creates a `.working` artifact only when the user chose to retain
working logs. These workflow files contain inferable relationship metadata
and empty content sections. The agent fills in their substantive content,
including review targets and criteria, before execution or validation.
If an approved subplan exception enables working-log retention when the root
setting is false, create the `.working` scaffold for that subplan's research
assignment while completing its brief.
Delegation is a plan setting and does not create an artifact or identity.

Complete the root plan, subplan briefs, and workflow assignments, then present
them with the execution contract to the user. Wait for the user's agreement on
the scope, outputs, sequence, gates, and execution settings before launching
any agent. The agreed contract authorizes in-scope assignments, subject to its
user checkpoint cadence.

Pass the user's research choice through verbatim; `$research` owns research
setting names and meanings. Plan management does not maintain a separate list.
Pass the user's research working-log choice through as `--research-working`
and record it as `execution.research_working`.

ID reservations are stored in the repository-level
`.plan-management/id-reservations.json` ledger so removed IDs are not reused
and concurrent allocation runs cannot claim the same ID. It records reservations,
not file paths. On first use, it seeds reservations from IDs it can find in
the repository. The shared allocator is `scripts/artifact_ids.py`; use it for
plan, workflow, and knowledge IDs. The validator builds an in-memory ID index
on each run to check references and anchors.

## Durable plan identities and references

A durable plan is organized around root and subplan entities:

- A root plan entity has an ID such as `LR-01`; its plan artifact is
  `LR-01.PLAN`.
- A subplan entity has an ID such as `LR-01.SP-03`; its plan artifact is
  `LR-01.SP-03.PLAN`.
- Artifact IDs extend the entity ID with the artifact role. Type codes and
  canonical artifact roles use uppercase; descriptive artifact roles use
  lowercase.
- The creator assigns and reserves the next available number; agents do not
  choose numbers. Root plan IDs use a repository-wide sequence. Subplan IDs
  share a sequence within their root. Ordinals have at least two digits, with
  a leading zero when needed. Removed IDs are never reused.
- Relationships use stable IDs, not paths. Use `ID#anchor` to refer to a
  section. The validator checks IDs and anchors against the current repository;
  do not maintain a second manual path registry.

## Durable plan metadata

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
`execution`, with the workflow dimensions `research`, `review`, and
`delegation`, plus `research_working` for the user's choice to retain
plan-local working logs and `user_checkpoints` for the agreed handoff cadence.
Their valid values and configurations belong to their owner skills: `research`
defines research; `agent-delegation` defines review and delegation. Plan
management defines working-log retention and checkpoint cadence and records
the user's choices.

For example, a root might record:

```yaml
execution:
  research: standard
  research_working: false
  review: true
  delegation: true
  user_checkpoints: each_handoff
```

Subplans inherit the root's `execution` defaults. A subplan may declare
`execution_exception` with only the dimensions that differ. An exception may
disable a dimension or enable it with a value defined by its owning skill,
even when the root disabled that dimension. It may also override
`research_working` when the user agrees to a local retention choice. Omit
`execution_exception` when there is no local override.

Field meanings:

- `plan_id`: the plan entity's assigned ID.
- `kind`: `root` or `subplan`.
- `parent`: `null` for a root; the parent plan entity ID for a subplan.
- `phase`: `root` for a root; the parent's phase identifier for a subplan.
- `status`: `not_started`, `in_progress`, `blocked`, or `complete`.
- `depends_on`: IDs of outputs that condition this unit's advancement. It is
  not a general-purpose list of inputs or provenance.
- `consumers`: destinations outside the plan graph; use an empty list when
  there are none. Consumers within the graph declare dependencies on relevant
  outputs in their own `depends_on` field.
- `execution`: required on the root only; the workflow dimensions,
  `research_working`, and `user_checkpoints` above.
- `research_working`: whether plan-coordinated research retains its
  `<RES-ID>.working` artifact; a boolean chosen by the user when research is
  enabled. It is false when research is disabled.
- `user_checkpoints`: when the coordinator pauses for user review of delegated
  work; one of `each_handoff`, `each_subplan`, or `plan_completion`.
- `execution_exception`: optional on a subplan; local deviations from the
  root's defaults.

Do not add `consumes` or `produces`. `depends_on` records advancement
conditions, `belongs_to` associates an artifact with its entity, and
`derived_from` records content provenance. Do not copy plan frontmatter to
other artifact types; their required fields depend on their type and owning
workflow.

## Durable plan content

The root `PLAN` maps the overall effort. Its body states the overall objective,
approach and boundaries, current phase, a concise ordered phase map linked to
its subplans, and the global completion gate. Detailed phase objectives,
scopes, inputs, outputs, and completion conditions belong to the relevant
subplans. The root may state cross-phase constraints, but should not repeat
each subplan's execution brief.

A subplan `PLAN` is the executable brief for one bounded task. It defines the
task objective and scope, relevant inputs, expected output, and completion
condition. Refer to inputs by ID. Do not redefine the root objective or repeat
the root plan. When repository knowledge could inform the task, follow the root
context map to its knowledge entrypoint and consult only relevant entries.
Record `KNOW` IDs that materially inform the task as inputs in the brief, not
as `depends_on` gates unless an output must be satisfied before the task can
advance. Simple coordination may consult repository knowledge without creating
a plan or tracking the consultation.

Record completion, verification, and material differences from the brief in a
short `Outcome` section of the subplan `PLAN`. Do not repeat the objective or
completion conditions there. Create a separate `RESULT` artifact only when the
task requires a standalone, consumer-facing deliverable that should be
consultable as its own artifact. Implementation work alone does not require a
separate `RESULT`.

## Workflow and artifact relationships

Research, review, and knowledge artifacts declare only the relationships
relevant to their type. Associated artifacts use `belongs_to`. Research and
review identify the requesting root or subplan with `requested_by`; review
assignments also declare their concrete `targets` and `criteria_refs`.
Knowledge records the concrete source artifacts in `derived_from`. The owning
skills define those artifacts' internal content and lifecycle.

Use `depends_on` only for a condition that must be satisfied before a unit
advances. When a unit must wait for an output, reference that output ID there.
This dependency does not by itself mean that the output is ready for use.

An output becomes available to consumers after its producing unit is complete,
the coordinator has received and reconciled the result, and applicable
dependency, review, and integration gates are satisfied, along with any user
checkpoint required before advancing beyond that output. A file's existence or
a provisional result does not unlock downstream work. The plan cycle controls
output availability; do not create a parallel artifact state machine.

Plan management records the agreed execution contract, coordinates with the
user, and manages plan gates. With subplans and delegation enabled, the primary
agent coordinates; delegated agents execute subplan work. `agent-delegation`
defines assignment, implementation, and review procedures. When research or
review is enabled, those stages are assigned to agents; review follows
completed, reconciled execution and evaluates a stable target. At each
required user checkpoint, the primary agent presents the reconciled handoff
and waits for approval before spawning or starting the next agent assignment.
Delegation changes who performs work, not the identity of the plan unit or its
artifacts.

For durable plans, keep artifacts beside the unit that coordinates them. Root
plan artifacts live in the root plan directory; artifacts specific to a
subplan live in that subplan's directory. Plan-local knowledge is shared by
the root plan and its subplans, so it lives only in the root plan's
`knowledge/` directory, which the creator makes even when empty. A typical
layout is:

```text
<plan>/
├── PLAN.md
├── research/
├── reviews/
├── knowledge/
└── subplans/
    └── <subplan>/
        ├── PLAN.md
        ├── RESULT.md       # only for a required standalone deliverable
        ├── research/
        └── reviews/
```

Create workflow directories other than the root plan's `knowledge/` only when
needed. Consumers refer to shared artifacts by ID; do not copy an artifact
into the consumer's directory or change its membership to the producing
entity.

## Status and blocked work

Use only `not_started`, `in_progress`, `blocked`, and `complete` for durable
plan units. Requirements agreed in the plan are mandatory. Resolve minor
issues autonomously within the approved scope.

`blocked` is a pause while awaiting a user decision, not a final state or a way
to accept incomplete work. If a requirement cannot be met within the approved
scope, or progress requires changing that scope, stop and explain the affected
requirement and blocker to the user. Do not bypass or omit the requirement or
report incomplete work as complete. After the user's decision, update the plan
when needed and resume as `in_progress`.

`complete` means the unit's work has ended. It does not by itself make outputs
available; the output availability conditions above still apply.

## Closing a completed plan

When a durable plan reaches `status: complete`, verify its outputs,
dependencies, consumers, and owned information. Before asking whether to
archive or delete the plan, always compare its reconciled outputs with the
repository's existing knowledge and surface likely reusable candidates to the
user, or say that none were found. For each candidate, state its intended
utility, material limitations, proposed create-or-update action, and the
source artifacts needed to support it. Do not create or update repository
knowledge until the user approves. If approved, follow the [repository
knowledge structure](../context-architecture/references/knowledge.md) and
preserve the source artifacts needed to resolve provenance independently of
the plan's lifecycle. The user may request this knowledge check at any time.

Then ask whether to delete the plan or move it to the relevant `reference/`
directory as legacy. Until the user chooses, leave the plan in place and do not
continue it or create another plan in its place.

## Validation

Use the plan validator provided by the repository. It can check structural
requirements, IDs, references, and relationships supported by its
implementation. It cannot decide whether an objective is strategically sound,
an output is substantively correct, or trade-offs are acceptable; review those
as human questions.

For the agent-skills repository, the current validator command is:

```bash
python3 skills/plan-management/scripts/validate_plans.py <repository>
```

Use strict validation when a repository is adopting the contract or selected
plans are expected to comply already. Treat existing plans without the required
metadata as migration work; do not rewrite them merely to silence a warning.
