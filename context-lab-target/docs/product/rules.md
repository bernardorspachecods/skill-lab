# Product Rules

The product is a small workspace for organising projects and tasks.

## Authority status

This document separates the implemented baseline from intended product
behaviour. The current baseline is verified by the linked code and tests;
intended behaviour is not evidence that a use case already exists.

## Navigation map

| If you need... | See |
| --- | --- |
| Ownership relationships | [Ownership invariants](#ownership-invariants) |
| Roles and permissions | [Roles](#roles) |
| Allowed task transitions | [Task lifecycle](#task-lifecycle) |
| Notification behaviour | [Notifications](#notifications) |

## Ownership invariants

- A user may belong to multiple workspaces through separate memberships.
- A workspace owns its projects and memberships.
- A project belongs to exactly one workspace.
- A task belongs to exactly one project.
- A user must have a membership in the relevant workspace to view or mutate
  its projects and tasks.
- A task may only be assigned to a user who has membership in the task's
  workspace.

## Roles

- Intended product roles are: `owner` can manage workspace memberships and
  all workspace content; `member` can create and update projects and tasks but
  cannot manage memberships. Role-specific authorization is not implemented
  in this baseline; the current use case checks workspace membership.

## Task lifecycle

The intended lifecycle is `todo` → `in_progress` → `done`, with a possible
return from `done` to `in_progress`; archived tasks would be immutable and
excluded from active project views. The current baseline only creates a task
with status `todo`; it has no transition, archive, or active-view use case.

## Notifications

The current baseline creates a `task_assigned` notification synchronously when
`create_task` receives an assignee. The worker attempts asynchronous delivery
and marks the notification delivered only after the delivery call succeeds.
There is no completion-transition use case, so completion notifications are
intended future behaviour rather than current behaviour.
