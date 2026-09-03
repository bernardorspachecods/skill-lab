---
name: handoff
description: Compact the current conversation into a handoff document for another agent or session to pick up; do not use it for an ordinary progress summary.
argument-hint: "What will the next session be used for?"
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Include the objective and current status, decisions and assumptions, changed artifacts, verification and its limits, blockers or open questions, and the exact next step. Keep each item factual and link to existing artifacts instead of copying them.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

Verify that the handoff was written to the temporary directory, contains the required sections, and does not expose sensitive information.
