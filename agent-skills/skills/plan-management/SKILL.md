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
to the work. The coordinator keeps the user-facing context, develops and
maintains the plan with the user, and handles small plan corrections with
them. Research, implementation, and formal output reviews are carried out by
one or more independent agents; the coordinator does not act as researcher,
implementer, or reviewer. Research and formal output review remain optional
workflows. Durable plans also require the temporary integrity check described
below before execution.

For durable plans, research supports subplan implementation by default. Do not
research the overall plan unless the user explicitly requests root-level
research. After drafting a durable plan with the user, delegate a temporary
plan-integrity check before execution; this checks the plan's logic and order,
not the completed plan output. Formal output reviews belong to subplans.

Use `$brainstorm` when the user wants to explore an open question, compare
approaches, or reach a decision through discussion. Use this skill when the
user wants to turn an objective or an agreed direction into actionable work.
Resolve ordinary planning details as part of planning; do not route routine
clarification or short plans to another planning skill.

`context-architecture` owns repository context maps and `CURRENT-STATE.json`.
This skill owns durable plan structure and the organization of plan artifacts.

The coordinator prepares bounded briefs, assigns each enabled research,
implementation, and formal review stage to agents, and keeps the user informed
at the agreed checkpoints. It receives, checks, and reconciles agent returns
against the assignment brief, agreed scope, plan criteria, and workflow gates.
Use the submitted artifacts for this check; route substantive gaps to the
assigned owner instead of doing new research or review to fill them. This
coordination check is not a formal output review. The coordinator may edit plan
and workflow artifacts and make small plan corrections with the user's
agreement, but substantive work on the planned deliverable stays with assigned
agents.

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
concise as the work allows, and do not add phases, research, review, or
deliverables without a concrete need. Do not create a parallel tracker when a
canonical plan already owns the work.

## Creating or revising a plan

1. Establish the objective and resolve any decision that would materially
   change the plan. Use the user's agreed direction as the basis; do not reopen
   settled decisions without a reason.
2. Identify the owner, scope, inputs, intended output, necessary steps, and
   completion condition. Split into subtasks only when separate ownership,
   dependencies, or lifecycle make the split useful.
3. Keep a conversation plan concise and sufficient for immediate execution.
   Do not add durable structures or workflow settings to it.
4. Before creating, revising, or coordinating a durable repository plan, read
   the [durable plan contract](references/durable-plan-contract.md). It owns
   durable plan structure, artifact scaffolding, execution settings, workflow
   assignments, handoff gates, and closure. Complete the draft plan, run and
   reconcile its temporary integrity check, then get the user's agreement
   before launching research, implementation, or output-review assignments.
5. Validate durable plan structure and references with the repository's plan
   validator. Review substantive questions—such as whether the objective and
   deliverable are right—separately; a structural validator cannot decide them.

Plan-specific artifact instructions live in the durable plan contract. The
coordinator uses that reference to create complete briefs and scaffolds.
Assigned researchers, implementers, and reviewers use the brief and artifact
locations supplied by the coordinator, alongside the applicable specialist
skill; they do not need to load the durable plan contract for a bounded task.
