---
name: git-worktree-cleanup
description: Clean a Git worktree by committing the changes relevant to the current task, either existing changes before work starts or changes just made by the agent. Invoke manually when you want the worktree clean.
---

# Clean the Git worktree

Infer the phase from the recent conversation and work:

- **Before a task:** when the agent has not changed anything for the current task, commit the changes already present.
- **After a task:** when the agent has just finished work, commit that task's changes and preserve unrelated pre-existing changes.

The invocation may add inclusions, exclusions, or a commit-message preference. Apply them exactly.

1. Inspect the repository root, branch, status, staged and unstaged diffs, and untracked files. Keep ignored files out of scope unless requested.
2. Select the changes for the inferred phase and exception list. Review the staged diff for unrelated files, secrets, credentials, and accidental inclusions; stage only the intended paths or hunks.
3. Create one focused commit with a concise task-derived message. For a start-of-task snapshot without a better description, use `chore(worktree): snapshot existing changes`.
4. Verify the worktree and report the commit hash, message, and anything intentionally left behind.

Do not push, amend, rewrite history, stash, reset, restore, clean, or delete files. Creating a commit is the cleanup operation.

Stop before committing if the intended changes cannot be separated reliably, exceptions conflict, a merge or rebase is in progress, or HEAD is detached. Ask for the smallest clarification needed. If the worktree is clean, report that no commit was necessary.

Examples:

```text
$git-worktree-cleanup
$git-worktree-cleanup, não incluir o .env nem os ficheiros em docs/drafts
$git-worktree-cleanup, usa a mensagem "feat: add billing filters"
```
