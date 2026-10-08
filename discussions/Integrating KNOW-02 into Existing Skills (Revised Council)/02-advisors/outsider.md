# Advisor Assignment: The Outsider

Artifact paths in this assignment are relative to the discussion folder (the parent of the phase folders). Read only this assignment and `01-brief/brief.md`. You may conduct focused external research as directed below. Do not inspect other agents' files or unrelated workspace files. You may write only in the response section of this file.

## Perspective

Respond only to the supplied brief. Look for confusing assumptions, unexplained terms, and gaps that an informed newcomer would notice.

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

Adopt a small, conditional feedback-loop pattern in `$plan-management`, with the plan skill retaining the operational instructions and a short shared reference carrying any reusable principles. Confidence: moderately high. The existing plan-management behavior, as summarized in the brief, already covers delegation, checkpoints, handoff review, and avoiding unnecessary phases. So the pilot should clarify the decision between handoff and follow-up rather than add a new mandatory review phase or reproduce KNOW-02. Apply the pattern when an agent returns work that the coordinator must judge or act on; use its full structure only when uncertainty, consequence, or evidence gaps make another cycle plausible.

## Analysis

The brief describes two related but distinct jobs: getting an agent to produce a useful artifact, and deciding whether the artifact is good enough to accept or needs correction. The feedback loop is useful at the boundary between those jobs. The handoff should give the agent a clear objective, scope, expected artifact, and relevant acceptance criteria. The return should include the artifact and enough evidence to assess it. The coordinator then compares that evidence with the criteria and chooses one explicit next action: accept, request a targeted change, stop, or escalate. A request for follow-up should name the specific gap, desired evidence or change, and the condition that will close the loop. “Try again” is not an adequate instruction.

KNOW-02's concepts can be translated without importing its full synthesis. In an agent handoff, the goal and current state describe the task and relevant context; “what changed” is the returned artifact or result; the task-relevant signal is the criterion or evidence used to decide whether to continue; and the next action is the coordinator's decision. Before dispatch, the coordinator should identify which observable result would actually warrant follow-up. At return, it should distinguish that cycle-driving signal from the final outcome check: an artifact may satisfy a local acceptance criterion while the larger plan still needs validation, or may be locally imperfect without affecting the outcome that matters.

This fits the existing plan-management practices in the brief: keep user context with the coordinator, use agreed checkpoints, assess handoffs against the brief and criteria, and avoid phases without concrete need. I recommend a short conditional subsection in plan-management that supplies a handoff/return/decision checklist and says to request targeted follow-up only for a material, actionable gap. Keep examples, criteria, and stopping conditions specific to the task. If multiple skills later need the same concept, a compact shared reference can define the loop's common vocabulary; skill-specific instructions should still say when to apply it and what counts as acceptance for that domain. Link to or summarize only the needed principles, rather than copy the full KNOW-02 source into each skill.

This pattern has lower overhead than requiring a formal signal, checkpoint schedule, and outcome review for every delegated action. A mandatory procedure could make trivial work slower, encourage ritualized metrics, and create extra agent turns whose evidence does not affect the decision. At the other extreme, relying only on informal judgment risks accepting polished but unsupported work, repeatedly sending vague revisions, or letting a cycle continue after its value is exhausted. Conditional use with an explicit decision gate addresses both failure modes. Checkpoint timing and any loop limit should be chosen for the task's consequence, uncertainty, reversibility, and available evidence; the brief gives no basis for a universal cadence or fixed number of retries.

## Strongest counterargument

The strongest case against even a plan-management change is that the skill already does the essential work: it delegates against a brief, checks results, uses checkpoints, and requires durable-plan validation. A new checklist could restate those instructions and imply that every delegation needs a feedback cycle. In addition, the source synthesis itself does not establish that making these concepts explicit improves independent-agent outcomes. If the current handoff guidance already reliably yields evidence-backed artifacts and targeted follow-ups, the change may add words without changing behavior. That evidence would favor leaving plan-management unchanged. Conversely, repeated examples of vague assignments, ungrounded acceptance, or avoidable follow-up turns would support adding the concise subsection. The pilot should be reviewed against such observed failure patterns rather than justified by the source's general recommendations alone.

## Key risk or opportunity

The main opportunity is to turn review from an impressionistic “looks good” check into a small evidence-based decision while preserving coordinator ownership and avoiding automatic iteration. The main risk is converting a useful mental model into mandatory ceremony or treating a proxy signal as the plan's ultimate outcome. Require the coordinator to identify the relevant criterion and next action, but permit a direct accept when the evidence is sufficient and no meaningful further decision depends on another cycle.

## Evidence and assumptions

- **Facts supplied by the brief:** KNOW-02 is a bounded synthesis for user-facing AI-agent workflows; it recommends meaningful signals, explicit next actions, checkpoints and stopping tied to consequence/evidence, and an outcome check distinct from the cycle-driving signal. Its evidence is varied and task/system-specific, and it establishes no universal cadence or stopping rule. The brief also summarizes plan-management as already retaining user context, setting checkpoints, delegating when useful, checking handoffs, performing a temporary integrity check before durable-plan execution, validating durable plan structure, and cautioning against unnecessary phases.
- **Inference:** A conditional operational checklist is a proportionate integration because it makes the decision points visible while preserving existing plan-management behavior. This is a design judgment, not an empirical finding that the checklist will improve outcomes.
- **Assumptions and limits:** The assignment did not provide the full KNOW-02 or plan-management files, so this recommendation relies on the brief's summaries and does not claim to audit their exact language or discover duplication elsewhere. I assume independent agents return artifacts and evidence to a coordinator who remains responsible for acceptance and follow-up. I have not conducted external research: the unresolved question is principally how to adapt the supplied synthesis to this workflow, not a current factual question, and the brief explicitly leaves cadence and threshold open.
<!-- COUNCIL-RESPONSE-END -->
