# Advisor Assignment: The First Principles

Artifact paths in this assignment are relative to the discussion folder (the parent of the phase folders). Read only this assignment and `01-brief/brief.md`. You may conduct focused external research as directed below. Do not inspect other agents' files or unrelated workspace files. You may write only in the response section of this file.

## Perspective

Identify the underlying problem, examine assumptions, and rebuild the question from its foundations. Say when the user may be asking the wrong question.

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
Recommend a lightweight shared feedback-loop pattern, invoked at the points where a skill delegates work and evaluates its return. `$plan-management` should make its existing cycle explicit in those moments, rather than add a mandatory new phase or repeat the full KNOW-02 synthesis. Confidence: high for this pattern; moderate on the exact wording and placement, which should be checked against the skill's operating flow by the coordinator.

The underlying decision is not primarily where to copy KNOW-02 into a skill. It is how to help the coordinator make a sound next-step decision from an independent agent's bounded work, without surrendering user context or creating cycles whose expected value is lower than their cost. The skill should make the decision inputs and possible actions clear: what was asked, what result or evidence would count as progress, what the agent returned, and whether to accept, request a bounded correction, or stop/escalate.

## Analysis
Start from the asymmetry in the workflow. The independent agent has a delegated brief and produces an artifact; the coordinator retains the full user context and authority to decide what happens next. The agent's completion claim is therefore evidence to assess, not the decision itself. A useful handoff needs a target artifact, relevant acceptance criteria, and a request for evidence or a concise account of what changed. A useful coordinator review compares that return with the brief and criteria, then chooses among accept, targeted follow-up, and stop/escalate. This is a closed loop only when the review can alter the next action; collecting status updates without an action rule is overhead, not feedback.

The KNOW-02 concepts transfer selectively. Goal/current state and what changed help frame the task and assess the return. A task-relevant signal helps decide whether another cycle is useful. An explicit next action prevents an agent loop from continuing by inertia. Checkpoints and stopping around consequence and evidence are useful guardrails. An outcome check distinct from the signal driving another cycle is relevant when the task has an independently observable outcome; it need not become a required field for every handoff. These are design prompts, not proof that every agent task benefits from a formal metric, fixed cadence, or two-stage review.

For `$plan-management`, the brief says the skill already keeps user context with the coordinator, sets agreed checkpoints, delegates when useful, checks returns against briefs and criteria, uses a temporary integrity check before durable-plan execution, and validates durable-plan structure. These are most of the functional pieces. The gap appears to be making the feedback decision legible and consistently bounded: at delegation, state the expected return and what evidence lets the coordinator judge it; at review, explicitly choose accept, targeted follow-up with a specific correction and stopping condition, or stop/escalate. When repeated work is warranted, identify the signal that would justify another cycle and the next action. Preserve existing checkpoints and specialized integrity/structure checks where their concrete purpose applies; do not turn them into universal extra reviews.

This is preferable to three plausible alternatives:

- **Copy the entire knowledge synthesis into plan-management.** This may keep the source close, but duplicates a bounded, nuanced synthesis, increases maintenance and context load, and risks making findings from varied user-facing workflows sound like validated rules for agent delegation.
- **Require a universal set of loop fields, metrics, cadence, and outcome checks for every delegated task.** This offers consistency, but many tasks have qualitative criteria or a one-shot deliverable. A fixed apparatus could make simple work cumbersome, invent false precision, and reward compliance with fields over useful judgment.
- **Leave the skill unchanged and rely on the coordinator to infer the loop.** This avoids added instruction, and may suffice for experienced coordinators, but leaves the most consequential transition—whether and how to repeat work—implicit. It can produce vague follow-ups, ungrounded acceptance, or unbounded iteration.

The smallest useful integration is a shared, concise reference for the general loop, linked from the skill at the delegation and return-assessment instructions. The skill-specific text should say when to use it and preserve domain-specific checks. In the skill, the handoff prompt can ask for the artifact/result, key evidence, and limitations relevant to the brief. The assessment prompt can ask whether criteria are met and, if not, what bounded next action could close the gap. Do not require a numeric signal when a concrete rubric or artifact inspection is the right signal. The coordinator's review should be proportionate to consequence, uncertainty, reversibility, and the cost of another cycle.

Failure modes to guard against are: accepting an agent's self-assessment in place of inspecting the returned work; criteria that are too vague to support a decision; follow-ups that merely say “improve” without naming the gap; repeated cycles that do not change the evidence or approach; and escalating every uncertainty into another agent pass. A stopping rule can be practical rather than numerical: stop when the brief's criteria are met, when a bounded correction is unlikely to resolve the gap, when evidence is insufficient and needs user input, or when added work no longer justifies its cost. For durable plans, retain the existing integrity check as a distinct safeguard when its described trigger applies; conflating it with ordinary progress feedback could dilute its purpose.

## Strongest counterargument
The strongest objection is that `$plan-management` already performs most of this behavior. Adding shared guidance and explicit language could restate existing instructions, increase skill length, or turn a useful judgment call into another checklist. Also, KNOW-02 is a synthesis about user-facing agent workflows; the brief does not establish that its concepts improve independent-agent delegation. A skill can remain lean and let the coordinator apply common sense.

That objection would change my recommendation if inspection of actual plan-management handoffs showed that expected returns, evidence, criteria-based assessment, and bounded follow-up decisions are already consistently explicit, and that users or coordinators experience no recurring ambiguity or gratuitous iteration. The brief alone says the pieces exist but does not establish how reliably the handoffs operationalize them. In that case, no skill change is justified; a shared reference could remain optional or be omitted. Conversely, examples of vague follow-up, missed criteria, or repeated work without new evidence would strengthen the case for a short, concrete instruction. I have not inspected the underlying skill or KNOW-02 source because the assignment restricts input to this prompt and the brief, so that empirical check remains for the council's later phase.

## Key risk or opportunity
The main opportunity is to make “another cycle?” an evidence-based, explicit decision while leaving context and judgment with the coordinator. The key risk is importing a source about feedback loops as if it established a universal agent workflow. Treat the loop as a decision aid: enough structure to prevent unbounded or ungrounded repetition, with no required metric or cadence absent a task-specific reason.

## Evidence and assumptions
- **Facts supplied by the brief:** KNOW-02 describes goal/current state, change, task-relevant signal, and next action; recommends consequence/evidence-sensitive checkpoints and stopping; distinguishes an outcome check from the loop-driving signal; and reports no universal cadence or stopping rule. The brief says evidence and observed practices are varied and task/system-specific. It also summarizes plan-management's current practices and says the council is to recommend changes rather than make them.
- **Inference:** Those concepts support a compact decision pattern for agent work, but do not demonstrate that a particular integration improves results. The existing practices make an explicit loop/decision cue more plausible than adding a new lifecycle phase.
- **Assumptions:** The coordinator can inspect the artifact and relevant evidence; the delegated task has a brief or criteria; and any proposed follow-up is authorized by the user's scope and proportionate to its likely benefit. Some tasks will require a user decision rather than another agent cycle.
- **Missing information:** Actual skill text and handoff examples, rates of rework or unnecessary cycles, the range of delegated task types, and measured effects of any wording change. The assignment prohibits inspecting the source files, so I have not independently verified the brief's summaries or conducted external research. No external research was needed for this first-principles recommendation; the missing evidence concerns the local skill's performance and is best resolved by reviewing examples or observing a small pilot, not by general web research.
<!-- COUNCIL-RESPONSE-END -->
