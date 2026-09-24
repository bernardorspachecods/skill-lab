---
name: plan-management
description: >
  Design, restructure, coordinate, and validate durable hierarchical plans and
  temporary delegation execution plans. Use after task clarification when
  creating a plan, changing plan structure, or coordinating a structured
  delegation.
---

`grill-task` owns clarification and short plan briefs; `context-architecture`
owns context maps, document placement, and `CURRENT-STATE.json`.

## Core contract

Plan management has two related but distinct contracts:

- a **durable plan** defines canonical work in the repository's plan tree;
- a **temporary delegation plan** defines one structured parallel execution and
  its review packet.

Plans and delegations are different artifacts. A plan defines what must be
done, evaluated, or produced. A delegation produces temporary findings and a
review; it must not turn those findings into plan prose or make delegated
agents co-edit the plan.

Choose the applicable contract and read only its reference:

- For a root plan, subplan, plan revision, or durable execution update, read
  [durable plans](references/durable-plans.md).
- For a structured `medium`, `full`, or `review` delegation from
  `parallel-task`, read
  [temporary delegation plans](references/temporary-delegation-plans.md).

Read both only when the delegation also creates or structurally changes its
durable parent plan.

## Shared coordination rules

- Resolve ownership before writing. Do not create a parallel tracker because a
  canonical plan is inconvenient.
- A temporary delegation may reference a durable parent plan and phase, but it
  never becomes a node in that plan tree automatically.
- Only the coordinator creates or updates the temporary execution plan. Each
  delegated agent receives one reserved findings file and edits only that file.
- The coordinator owns the temporary `review.md`, conducts the joint review
  with the user, and applies accepted findings to the named canonical
  consumer.
- Do not update canonical plans, documentation, or product files from a
  provisional finding before the coordinator and user have reviewed it.
- Temporary delegation packets are non-canonical and must be deleted after
  joint review, application of accepted findings, and cleanup verification.

## Validation boundary

Use the validator named by the selected reference. Validators can check
structure, metadata, links, and relationships; they cannot decide whether an
objective is strategically correct or whether an output is substantively
valuable. Report those as human review items instead of disguising them as
structural failures.

Finish when the selected contract is satisfied, the remaining review items
concern content or decisions rather than form, and—if the run was temporary—
the packet has been reviewed, applied, and cleaned up.
