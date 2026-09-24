# Temporary delegation execution plans

Use this contract for a structured `medium`, `full`, or `review` run from
`parallel-task`. It coordinates a temporary packet; it does not create a
durable plan or add a node to the repository's plan tree.

If the delegation requires creating or structurally changing its durable
parent plan, also read [durable plans](durable-plans.md). Otherwise, do not
load the durable-plan contract for this run.

## Boundary

The execution plan is the coordinator-owned contract for what the delegated
agents must do or evaluate. Findings are independent agent outputs. The review
is the coordinator-owned record of the joint decision with the user. Do not
copy findings into the execution plan.

All packet files belong in one run-scoped folder under the repository's
designated non-canonical findings location:

```text
<findings-root>/parallel-task/<delegation-id>/
├── execution-plan.md
├── findings/
│   ├── <agent-id>.md
│   └── ...
└── review.md
```

The folder is temporary, must not be committed, and is deleted after the
joint review and application of accepted findings. Preserve it only when the
user explicitly requests retention or the review/application is still pending.

## Frontmatter

The coordinator creates `execution-plan.md` with:

```yaml
---
delegation_id: D-20260924-001
kind: temporary-execution-plan
lifecycle: temporary
parent_plan: P0.1
parent_phase: 2
status: awaiting_launch
depends_on: []
consumers: []
coordinator: primary-agent
review_owner: primary-agent
---
```

`parent_plan` and `parent_phase` are references to a durable plan, not a
request to create or edit a subplan. Use `null` when the delegation is not
attached to a durable plan. `delegation_id` is unique within the run root.

Allowed temporary-plan statuses:

`awaiting_launch` (prepared), `in_progress` (running), `awaiting_review`
(findings ready), `awaiting_application` (review complete, not applied),
`complete` (applied; cleanup ready), `blocked`, `cancelled`.

Findings may use `awaiting_launch`, `in_progress`, `awaiting_phase2`,
`provisional`, `complete`, `blocked`, or `cancelled`. They must not edit the
execution-plan status or frontmatter.

`depends_on` records inputs or entry conditions. `consumers` records the
canonical task, plan, or files that receive accepted findings. Optional notes
must add unique context and must not repeat structured fields or create new
instructions.

## Required document sections

`execution-plan.md` contains these sections in order:

```markdown
## Objective
## Scope
## Output
## Sequence
## Participants and file ownership
## Completion criteria
## Review contract
## Cleanup
```

The durable-plan sequence rule still applies: every ordered step has an
`Action`, an `Output`, and an `Exit check`.

`Participants and file ownership` must identify the coordinator, each agent's
reserved findings path, and the review owner. The minimum ownership contract
is:

| Artifact | Owner | Write boundary |
| --- | --- | --- |
| `execution-plan.md` | coordinator | The coordinator only |
| `findings/<agent-id>.md` | named agent | That agent only |
| `review.md` | coordinator | The coordinator only, after audit and joint review |
| canonical task, plan, or product files | primary agent | Only after joint review and approval |

## Findings and review

Each delegated agent receives the same execution plan and one reserved
findings file. It writes its assessment, evidence, uncertainties, and
recommendations only to that file. During an independent first phase, agents
must not read one another's findings.

The coordinator audits the findings against the execution plan and evidence
before the joint review. The coordinator and user then decide which findings
are applicable and accepted. The coordinator records the decision and applied
changes in `review.md`, then updates the canonical consumer named in the plan.

The review file must not become a second plan or a copy of every finding. It
records the supported decisions, rejected or unresolved items, applied
artifacts, remaining uncertainty, and cleanup readiness.

## Findings file contract

Each reserved `findings/<agent-id>.md` file has one owner and uses this
frontmatter:

```yaml
---
delegation_id: D-20260924-001
kind: finding
agent_id: perspective-1
role: independent-assessment
status: provisional
---
```

The file contains these sections in order:

```markdown
## Assignment
## Assessment
## Evidence
## Uncertainties
## Recommendations
## Open questions
```

The assignment points back to `execution-plan.md` and states the agent's
reserved direction. The agent records conclusions in `Assessment`, supporting
material in `Evidence`, limitations in `Uncertainties`, and proposed next
steps in `Recommendations`. It must not silently turn a recommendation into a
canonical change.

## Review file contract

The coordinator prepares `review.md` and completes it only after auditing the
findings and conducting the joint review with the user:

```yaml
---
delegation_id: D-20260924-001
kind: review
status: awaiting_review
coordinator: primary-agent
---
```

It contains these sections in order:

```markdown
## Coordinator audit
## Joint decisions
## Applied changes
## Unresolved items
## Cleanup
```

`Joint decisions` identifies which findings were accepted or rejected.
`Applied changes` names the canonical task, plan, or files changed by the
primary agent. `Cleanup` confirms that no pending decision or application
remains before the run folder is deleted.

The findings and review templates deliberately do not repeat the execution
plan. Link back to it instead.

## Workflow boundary

`parallel-task` owns launch authorization, mode-specific phases, coordinator
audits, joint review sequencing, and renewed approval after material scope
changes. This reference owns only the temporary packet's structure and file
contracts; do not duplicate the `go` workflow here.
