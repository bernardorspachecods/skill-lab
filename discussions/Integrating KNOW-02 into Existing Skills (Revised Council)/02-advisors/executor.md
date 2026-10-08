# Advisor Assignment: The Executor

Artifact paths in this assignment are relative to the discussion folder (the parent of the phase folders). Read only this assignment and `01-brief/brief.md`. You may conduct focused external research as directed below. Do not inspect other agents' files or unrelated workspace files. You may write only in the response section of this file.

## Perspective

Assess whether the idea can be carried out and identify the fastest concrete first step. Focus on practical action.

## Task

Analyze the question independently from your assigned perspective. Do not assume another advisor will correct unsupported claims or fill gaps in your analysis. Do not stop at the first plausible answer. Examine the underlying decision, the assumptions in the brief, plausible alternatives, their material tradeoffs and failure modes, and the strongest objection to your preferred position. Consider what evidence or changed condition would alter your conclusion.

If the answer materially depends on current, specialized, or empirical facts that the brief does not supply, conduct focused research to resolve that gap. Prefer primary or authoritative sources where appropriate, cite sources for material factual claims, and distinguish what a source establishes from your inference. Do not research merely to decorate a judgment that does not depend on external facts. If research cannot resolve a gap, state the uncertainty.

Return a substantive analysis, not just a quick conclusion. There is no word limit: give enough reasoning to make the tradeoffs, assumptions, evidence, and limitations clear, while avoiding repetition. Do not identify yourself by role in the response; the coordinator tracks roles separately.

Write your response only between the response markers below, preserving all assignment instructions outside them. Return:
1. Position: your conclusion and confidence, with the conditions that matter.
2. Analysis: the strongest supporting reasons, comparison with plausible alternatives, material tradeoffs, and relevant failure modes.
3. Strongest counterargument: the best case against your position and what evidence or condition could change your conclusion.
4. Key risk or opportunity: the most important point from your perspective.
5. Evidence and assumptions: distinguish facts from inference; state material assumptions, missing information, and any research sources used.

## Response

<!-- COUNCIL-RESPONSE-START -->

## Position
Recommend a small, pilot-specific integration in `$plan-management`: make its existing handoff and review guidance an explicit bounded feedback loop. For each delegated task, the coordinator should name the desired artifact, the evidence or criteria that will determine whether it is usable, and the decision options after review: accept, request a targeted revision, or stop/escalate. A revision request should name the gap and the changed result needed to close it. Confidence: moderately high, assuming the brief accurately summarizes current plan-management guidance. This is a recommendation for the council; no skill changes should be made in this run.

## Analysis
The fastest concrete first step is editorial: add a compact checklist or paragraph at the existing handoff-review point in plan-management, rather than adding a new phase or an always-on agent cycle. The brief says the skill already preserves user context with the coordinator, delegates when useful, sets checkpoints, and checks returned work against briefs and criteria. So the practical gap appears to be making the post-handoff decision and any retry criteria explicit, not introducing delegation or review from scratch.

An actionable loop can be expressed in four parts:

1. At assignment, state the goal, deliverable, relevant criteria or evidence, and the boundary of the delegated task.
2. On return, compare the artifact and its evidence with that brief; note any material limitation rather than treating an agent's confidence as proof.
3. Choose and record one outcome: accept; request one bounded, specific follow-up; or stop/escalate if the brief is unmet, the evidence is insufficient, or further work is not justified.
4. After a follow-up, assess whether the requested gap closed and stop when the acceptance criteria are met or the next cycle would need a changed brief, more evidence, or user judgment.

This puts the user's context and decision authority with the coordinator while letting the independent agent supply a reviewable artifact and evidence. It also avoids an arbitrary retry count: the condition for another cycle is an unresolved, task-relevant gap for which a concrete next action is available. The outcome check should ask whether the requested deliverable is fit for its intended use; the signal that triggers another cycle can be narrower, such as a missing section, an unresolved claim, or a failed criterion. Those checks can overlap, but should not be conflated by default.

The main alternatives are weaker for this pilot. Copying the full KNOW-02 synthesis into plan-management would increase loaded context and risk turning qualified recommendations into mandatory rules. A new shared reference could reduce future duplication across skills, but there is no evidence in this brief that several skills need the same operational detail now; creating it first adds a dependency and an extra file to maintain. Conversely, adding nothing preserves simplicity, but leaves an avoidable ambiguity about what counts as a useful follow-up and when to stop. Start with a small change in the pilot skill, then extract shared guidance only if another skill demonstrates the same need.

Avoid mandatory agent use, fixed cadence, a universal retry limit, or extra review passes. Use the loop only where independent work is actually delegated and a meaningful acceptance signal can be stated. For low-consequence work, a quick check may be sufficient; for higher-consequence or weakly evidenced work, the coordinator may need more evidence or a user checkpoint. The brief does not establish universal cadence or stopping thresholds, so these must remain tied to task consequence and evidence.

## Strongest counterargument
Plan-management already checks delegated handoffs against briefs and criteria, so this proposal may simply restate existing practice. Adding a named loop could increase instruction length and encourage coordinators to manufacture a signal or repeat work even when a direct review is enough. The best case for no change is that existing guidance already leads to explicit accept/revise/stop decisions in practice.

I would change my recommendation if a focused review of the actual skill showed that it already directs coordinators to record the post-review decision, define a concrete condition for follow-up, and stop when that condition is met—or if usage evidence showed that a checklist adds friction without improving handoff quality. In either case, retain the current guidance and consider a short example only if users continue to miss the decision step. The brief does not provide the skill text or such usage evidence, so this conclusion is conditional on its summary.

## Key risk or opportunity
The opportunity is to turn delegated output into a reviewable decision and a useful correction, rather than an open-ended second assignment. The main risk is false precision: a checklist can make subjective or weak evidence look authoritative, or imply that KNOW-02 supports a universal retry policy. Keep criteria proportional to consequence, distinguish evidence from judgment, and make follow-up conditional on an actionable gap.

## Evidence and assumptions
The brief reports that KNOW-02 presents a bounded cycle involving goal/current state, change, a task-relevant signal, and next action; it recommends meaningful signals, explicit next actions, and checkpoints/stopping based on consequence and evidence. It also states that the evidence is varied and task/system-specific and does not establish a universal cadence or stopping rule. The brief further summarizes plan-management as already supporting checkpoints, delegation, and handoff checks. These are facts available from the brief; I did not inspect the underlying knowledge file or skill.

The recommendation to add the decision options and make follow-up criteria explicit is my practical inference from that summary and from the stated pilot question. It assumes the current plan-management text has a natural handoff-review location and does not already specify all three outcomes. No external research was needed: the central choice is an integration and workflow-design judgment, and the brief supplies the relevant evidence limitation. The largest missing evidence is whether the existing wording already resolves the loop in practice, plus any observations on revision quality, time cost, or repeated handoff failures. A pilot could evaluate those outcomes before generalizing guidance across skills.
<!-- COUNCIL-RESPONSE-END -->
