---
name: git-worktree-cleanup
description: Commit the work done and preserve unrelated work.
---

## Core rules

- Keep ignored files out of scope unless requested.
- Verify the worktree and report the commit message, and anything intentionally left behind.
- Create one commit for the selected scope, with a concise message that describes it. For a start-of-task snapshot without a better description, use `chore(worktree): snapshot existing changes`.
- If the worktree is clean, report that no commit was necessary.

## Choose the commit scope

### `all`

When the user says `$git-worktree-cleanup all`, commit all non-ignored changes in the worktree in one commit. This includes unrelated pre-existing changes. Ignored files remain out of scope unless the user explicitly requests them.

### `only`

When the user says `$git-worktree-cleanup only`, commit only changes made for the current task and preserve unrelated pre-existing work. If isolating the task changes requires more than three separate staging groups, stop and report back to the user. Count each group that must be selectively staged or excluded as one staging group.

### No mode specified

If the user says `$git-worktree-cleanup` without a mode, assume `$git-worktree-cleanup all`.


