---
name: git-worktree-cleanup
description: Commit the work done and preserve unrelated work.
---

- Commits only the changes that belong to you and preserve unrelated pre-existing work.
- Keep ignored files out of scope unless requested.
- Create one focused commit with a concise task-derived message. For a start-of-task snapshot without a better description, use `chore(worktree): snapshot existing changes`.
- Verify the worktree and report the commit message, and anything intentionally left behind.

If the worktree is clean, report that no commit was necessary.

If this committing only your changes involves a lot of work (more than 3 separations), STOP and report back to the user
