# Durable plan shared rules

Read this file for every durable-plan task. It defines the common plan model,
artifact identities, metadata, validation, and placement. Lifecycle-specific
actions are in [setup](setup.md), [execution](execution.md), and
[closure](closure.md).

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

The shared [artifact ID allocator](../../scripts/artifact_ids.py) assigns plan
and workflow IDs; agents do not choose them. The repository-level
`.plan-management/id-reservations.json` ledger prevents reuse and concurrent
claims. It records reservations, not file paths, and seeds from IDs found in
the repository on first use. The validator builds an in-memory ID index for
checking references and anchors.

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
- `execution`: required on the root only; contains the settings defined in [setup](setup.md).
- `execution_exception`: optional on a subplan; contains only local deviations
  from root defaults.

Do not add `consumes` or `produces`. `depends_on` records advancement
conditions, `belongs_to` associates an artifact with its entity, and
`derived_from` records content provenance. Do not copy plan frontmatter to
other artifact types; their required fields depend on the artifact.

## Plan content and workflow relationships

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
The dependency alone does not mean the output is ready for use; see [execution](execution.md).

## Artifact placement

Keep durable-plan artifacts beside the unit that coordinates them until
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

Consumers refer to shared artifacts by ID; do not copy
artifacts into a consumer's directory or change their membership to the
producing entity.

Use the [repository's plan validator](../../scripts/validate_plans.py). It
checks structural requirements, IDs, references, and supported relationships;
it cannot judge whether an objective
or output is substantively right. For this repository, run from the
`agent-skills/` directory:

```bash
python3 skills/plan-management/scripts/validate_plans.py <repository>
```

Use strict validation when adopting the contract or when selected plans are
expected to comply already. Treat existing plans without required metadata as
migration work; do not rewrite them merely to silence warnings.

For temporary delegation execution plans and run packets, use the
[temporary plan validator](../../scripts/validate_temporary_plans.py).
