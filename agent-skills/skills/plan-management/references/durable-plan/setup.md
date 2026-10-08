# Durable plan setup

Read [shared rules](shared-rules.md) with this file when creating a plan or making changes that affect its structure, workflow settings, or assignments.

## Design the plan and execution settings

Recommend a subplan count and execution settings based on task complexity,
dependencies, assurance needs, parallel work, and where focused LLM execution
benefits from smaller tasks. Keep the plan concise; do not add phases, workflow
stages, or deliverables without a concrete need.

Treat research as support for subplan implementation. Enabling research for
subplans does not authorize research on the overall plan. Root-level research
is off unless the user explicitly requests research for the root objective;
record that request with `execution.root_research`.

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
not controlled by `review`; its reviewer must be an agent other than the
coordinator. Follow the integrity gate below.

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

## Scaffold assignments and artifacts

After the user confirms the settings, run the [plan creator](../../scripts/create_plan.py)
from this skill's directory:

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
sections. Complete the briefs and assignment content, including subplan review targets
and criteria, before validation. If an approved subplan exception enables
working-log retention while the root setting is false, create a `.working`
scaffold for that subplan's research assignment.

The creator refuses to overwrite an existing plan root or any generated file
that already exists. If it reports a collision, inspect the destination and
choose a different destination or resolve the existing plan before retrying.

Agent assignment does not create a plan artifact or identity. Assigned work
continues the same plan unit and workflow artifacts. Do not create a
delegation entity or `DEL-*` ID, a separate subplan solely for an agent, or a
persistent agent history in the artifact graph.


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

## Integrity check and approval gate

After completing the initial draft, and after any later revision that materially
changes the plan's scope, sequence, dependencies, or completion conditions,
delegate a plan-integrity check before implementation or plan research begins
or resumes.
Create the temporary `plan-integrity-check.md` beside the root `PLAN.md` and
give the reviewer the root plan, subplans, and these criteria: logical
coverage, ordering, dependencies, feasibility, and consistent completion
conditions. The reviewer records concise findings, evidence in the plan, and
recommended corrections in that file. Reconcile the findings, make any agreed
plan edits, then delete the temporary file.

The reviewer must be an agent other than the coordinator. Do not assign a
`REV` identity or treat this as a review of completed output. Use
`$agent-delegation` review procedures for independence and evidence standards;
the temporary file is the only review output for this gate. If independent
delegation is unavailable, report that the integrity gate could not be
completed; do not present a self-review as independent.

Run the plan validator described in [shared rules](shared-rules.md), then
present the finalized plan with the execution contract. Wait for the user's
agreement on scope, outputs, sequence, gates, and settings before starting
root research, subplan research, implementation, or output reviews. That
agreement authorizes those execution assignments subject to the selected
checkpoint cadence.
