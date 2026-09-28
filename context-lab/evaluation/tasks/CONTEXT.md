# Manual Evaluation Tasks

This folder contains the prompts supplied to the agent during baseline runs.
It does not contain the evaluator's expected paths or scoring oracle.

The prompts intentionally use structured evidence checklists so each case
tests a defined cross-area question. Route efficiency must be analysed
separately from answer correctness; the checklist is not a locator protocol.

## Cases

- [001-create-task.md](001-create-task.md) — locate the path and rules for
  creating a task.
- [002-assignment-notification.md](002-assignment-notification.md) — trace task
  assignment into asynchronous notification delivery.
- [003-cross-workspace-sharing.md](003-cross-workspace-sharing.md) — assess a
  proposed change to the workspace ownership rule.
- [004-undelivered-notification.md](004-undelivered-notification.md) — diagnose
  a notification that was created but not delivered.
- [005-chat-start-permission.md](005-chat-start-permission.md) — compare the
  same task with `chat-start` forbidden versus permitted.
