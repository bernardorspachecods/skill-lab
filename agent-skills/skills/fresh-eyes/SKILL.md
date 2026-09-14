---
name: fresh-eyes
description: Independently assess a completed task for correctness, omissions, risks, and improvements, producing a provisional review report. Invoke manually after a task.
---

# Fresh-eyes review

Use this skill after a substantive task when the agent or user may be too invested in the current solution to evaluate it impartially. Review the result, not the effort spent producing it.

This is a review-only pass. Do not edit product files, implement suggestions,
or silently expand the task. The only file it may create or update is the
provisional review report described below.

1. Reconstruct the original request, intended outcome, success criteria,
   decisions made, changed artifacts, and verification already performed.
2. Prepare the smallest sufficient review packet: the original request or
   spec, applicable repository guidance, relevant diff or output, and the
   tests, sources, or evidence needed to judge it. Exclude irrelevant
   conversation and the primary agent's verdict or defence.
3. Create a provisional review report in the repository's designated
   non-canonical findings location. Start it with the review objective, packet,
   and status `in_progress`.
4. Delegate an independent subagent with this brief:

   > Evaluate this completed task with fresh eyes. Do not assume the result is correct and do not defend the existing approach. Compare it with the original objective, applicable rules, current behavior, and available evidence. Look for correctness problems, omissions, scope creep, unnecessary complexity, maintainability issues, weak or missing verification, risks, and better alternatives. Support each finding with concrete evidence and classify its severity. Report strengths as well as problems. Do not edit anything or implement a fix.

5. Have the subagent update the report with a provisional verdict, strengths,
   findings ordered by severity, concrete evidence, recommended improvements,
   remaining uncertainty, and the next decision the user should make.

For code, include the relevant diff, tests, runtime behavior, and repository
conventions. For documentation or research, include source authority, coverage,
traceability, navigation, and unresolved claims. Match review depth to the
task's risk; do not manufacture objections merely to appear thorough.

Mark the report clearly as:

> PROVISIONAL — requires review by the primary agent and the user.

Never treat the report as definitive or update canonical documentation from it
automatically.

Monitor the delegated agent's state: silence while `running` is still pending,
not failure. Stop only for an explicit error, timeout, blocked state, or user
instruction.

If independent delegation is unavailable, say so explicitly and do not present
the primary agent's own review as independent. Report the review report's
location and assessment, then wait for the user's approval before applying any
change.

Finish when the report and assessment make clear what is sound, what should
change, what remains unverified, and what decision is pending.

Example:

```text
$fresh-eyes Avalia a tarefa que acabaste de concluir e propõe melhorias, mas não alteres nada.
```
