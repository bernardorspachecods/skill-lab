# Product Documentation

This folder records user-visible behaviour, terminology, workflows, and
product rules that the application depends on.

## Language

**User**:
A human identity that can belong to one or more workspaces.
_Avoid_: Account, member (when referring to the identity itself)

**Workspace**:
The top-level collaboration boundary that owns projects and their memberships.
_Avoid_: Organization, team (unless a separate concept is introduced later)

**Membership**:
The role-bearing relationship between a user and a workspace.
_Avoid_: Permission, account role

**Project**:
A named collection of tasks owned by exactly one workspace.
_Avoid_: Board, workspace

**Task**:
A work item owned by exactly one project. The baseline creates tasks in `todo`;
status transitions are intended future behaviour.
_Avoid_: Ticket, issue (unless a later product decision distinguishes them)

**Notification**:
A durable user-facing message produced by a task event. The baseline creates
assignment notifications during task creation; other event types are future
behaviour.
_Avoid_: Alert, event (an internal event may be a separate concept)

## Destinations

- [rules.md](rules.md) — product invariants, workflows, and permissions.
