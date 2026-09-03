---
name: fresh-eyes
description: Independently assess a completed task for correctness, omissions, scope creep, risks, and improvements by delegating a fresh review to a subagent. Invoke manually after a task.
---

# Fresh-eyes review

Use this skill after a substantive task when the agent or user may be too invested in the current solution to evaluate it impartially. Review the result, not the effort spent producing it.

This is a review-only pass. Do not edit files, implement suggestions, or silently expand the task.

1. Reconstruct the original request, intended outcome, success criteria, decisions made, changed artifacts, and verification already performed.
2. Prepare the smallest sufficient review packet: the original request or spec, applicable repository guidance, relevant diff or output, and the tests, sources, or evidence needed to judge it. Exclude irrelevant conversation and do not include the primary agent's verdict or arguments defending its choices.
3. Delegate an independent subagent with this brief:

   > Evaluate this completed task with fresh eyes. Do not assume the result is correct and do not defend the existing approach. Compare it with the original objective, applicable rules, current behavior, and available evidence. Look for correctness problems, omissions, scope creep, unnecessary complexity, maintainability issues, weak or missing verification, risks, and better alternatives. Support each finding with concrete evidence and classify its severity. Report strengths as well as problems. Do not edit anything or implement a fix.

4. Present the subagent's assessment with a provisional verdict, strengths, findings ordered by severity, evidence, recommended improvements, remaining uncertainty, and the next decision the user should make.

For code, include the relevant diff, tests, runtime behavior, and repository conventions. For documentation or research, include source authority, coverage, traceability, navigation, and unresolved claims. Match review depth to the task's risk; do not manufacture objections merely to appear thorough.

If independent delegation is unavailable, say so explicitly and do not present the primary agent's own review as an independent assessment. Wait for the user's approval before applying any proposed change.

Finish when the fresh review covers the relevant result and makes clear what is sound, what should change, what remains unverified, and what decision is pending.

Example:

```text
$fresh-eyes Avalia a tarefa que acabaste de concluir e propõe melhorias, mas não alteres nada.
```
