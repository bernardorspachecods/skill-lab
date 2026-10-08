# Advisor Assignment: The Expansionist

Artifact paths in this assignment are relative to the discussion folder (the parent of the phase folders). Read only this assignment and `01-brief/brief.md`. You may conduct focused external research as directed below. Do not inspect other agents' files or unrelated workspace files. You may write only in the response section of this file.

## Perspective

Look for upside, overlooked opportunities, and what could become possible if the idea works. Focus on growth and potential.

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

Recommend a small, reusable feedback-loop contract for delegated work, with `$plan-management` as the pilot. Confidence: moderately high that this can improve handoff clarity and make useful follow-up more targeted; low that any particular checkpoint rhythm or stopping threshold will be generally optimal. The integration should make each delegation easier to assess and act on, while leaving cadence and escalation dependent on the task’s stakes, evidence, and cost.

## Analysis

Independent agents create an opportunity to turn delegation from a one-way request into a bounded learning cycle. A well-shaped handoff can give the agent enough context to produce a useful artifact, and give the coordinator enough evidence to choose among acceptance, a narrow correction, or a stop/escalation. Over time, that pattern can make delegation more repeatable across research, implementation, and review without requiring every skill to restate the full knowledge base.

For the pilot, add a compact handoff-and-return pattern to `$plan-management`, ideally backed by one shared reference if the same guidance is adopted elsewhere. The handoff should identify the goal/current state, requested change or deliverable, relevant success signal or criteria, requested evidence, checkpoint if one is useful, and the condition for stopping or escalating. The agent’s return should include the artifact, evidence tied to the criteria, unresolved gaps, and a proposed next action. The coordinator then makes an explicit disposition: accept, request a specific follow-up, or stop/escalate. That disposition is the part that closes the loop; merely receiving a report does not.

Keep the pattern conditional rather than adding a mandatory review phase to every delegation. A small, reversible task with an inspectable result may need only a concise handoff and final check. Work with high consequence, uncertain evidence, or costly rework may justify an early checkpoint and stronger evidence request. This preserves the skill’s existing caution against extra phases without a concrete need, and lets the coordinator spend review effort where it has the most leverage.

There is also a growth opportunity in separating the signal used to decide whether work needs another cycle from the outcome check used to decide whether the intended result was achieved. For example, evidence coverage or unresolved assumptions might prompt a targeted research follow-up; the later plan-quality check determines whether the plan is ready for its intended use. Naming those questions separately can prevent endless refinement and help the coordinator stop when the required outcome is met, even if other possible improvements remain.

Plausible alternatives are to leave the skill unchanged, to embed the entire KNOW-02 synthesis in the skill, or to create a universal, rigid agent-review checklist. Leaving the skill unchanged avoids overhead but misses an opportunity to make its existing handoff and assessment practices more explicit and consistently reusable. Embedding the full synthesis risks duplicating source material and loading irrelevant guidance. A mandatory checklist with fixed cycles or thresholds could standardize reporting, but the brief explicitly says the evidence does not establish a universal cadence or stopping rule; such rigidity would add cost and could generate low-value follow-ups. A short shared reference plus a small plan-management-specific invocation appears to capture reuse while retaining judgment.

## Strongest counterargument

The strongest case against changing `$plan-management` is that it already keeps user-facing context with the coordinator, sets checkpoints, checks delegated handoffs against briefs and criteria, and has explicit validation and integrity checks in relevant workflows. Adding another contract could duplicate these instructions, increase handoff overhead, and encourage agents to produce process reports instead of better artifacts. The brief does not establish empirically that formalizing the loop improves outcomes.

That objection would change my recommendation if a review of actual plan-management use showed that its current handoffs already reliably specify evidence and next actions, or if trial use showed the added fields increased latency without improving acceptance or follow-up quality. In that case, preserve the current skill and perhaps add only a short reminder in a shared reference. Conversely, repeated cases of ambiguous agent returns, ungrounded acceptance, or broad follow-up requests would strengthen the case for a more explicit pilot.

## Key risk or opportunity

The key opportunity is compounding: better evidence-bearing returns let the coordinator ask smaller, more precise follow-ups and build confidence in delegation across different work types. The key risk is turning a flexible reasoning aid into a paperwork gate. Make the loop scale with consequence and uncertainty, and make each cycle end in a concrete disposition.

## Evidence and assumptions

- **Facts supplied by the brief:** KNOW-02 describes a bounded feedback loop, recommends selecting a meaningful signal before cadence, making the next action explicit, and setting checkpoints and stopping around consequence and evidence. It distinguishes empirical findings, observed practices, inferences, and recommendations, and says no universal best checkpoint cadence or stopping rule is established. The brief also summarizes existing `$plan-management` behavior and its caution against phases or reviews without a concrete need.
- **Inference:** A shared compact contract could make the existing delegation practices easier to apply consistently and could improve the precision of follow-up. That is a design judgment, not an outcome established by KNOW-02.
- **Assumptions and gaps:** I assume delegated tasks vary enough in consequence and evidence needs to make a fixed cadence undesirable, and that the cost of inserting a concise handoff/return pattern is modest. The brief does not provide usage examples, observed failure rates, or measurements comparing current handoffs with a formal loop. Those would be useful before making the pattern mandatory or expanding it beyond the pilot.
- **Research:** No external research was needed; the recommendation is about integrating the supplied bounded synthesis into the supplied skill context, and the brief states the material evidence limitations.
<!-- COUNCIL-RESPONSE-END -->
