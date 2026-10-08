# Advisor Assignment: The Contrarian

Artifact paths in this assignment are relative to the discussion folder (the parent of the phase folders). Read only this assignment and `01-brief/brief.md`. You may conduct focused external research as directed below. Do not inspect other agents' files or unrelated workspace files. You may write only in the response section of this file.

## Perspective

Look for what is wrong, missing, or likely to fail. Assume the proposal may have a serious flaw and test it. Be rigorous, not reflexively negative.

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
Do not add a general-purpose, mandatory “feedback loop” phase to `$plan-management`, and do not make every delegated handoff iterative by default. Confidence: moderately high. The brief says plan-management already assigns work, checks handoffs against briefs and criteria, and requests follow-up where useful. KNOW-02’s synthesis concerns user-facing agent workflows; the transfer from those workflows to an independent-agent coordination loop is plausible but not established by the evidence summarized here. If plan-management needs a change, make it a small clarification to its existing delegation guidance: every delegated task should have a clear expected artifact and relevant acceptance evidence, and any follow-up should name the specific gap and a stop/escalation condition. Treat that as a conditional decision aid, not a new phase or universal retry count.

## Analysis
The central risk is mistaking a useful description of feedback for evidence that adding more cycles improves delegated work. The cycle in the brief—assign, receive artifact and evidence, assess, then accept, follow up, or stop—is already close to ordinary brief-based coordination. Renaming this a loop could add ceremony without changing decisions. A mandatory sequence of checkpoints, signals, outcome checks, and retries would be especially costly for bounded research or implementation tasks where the acceptance criteria are already clear and the artifact can be reviewed once.

The knowledge source as summarized has a more limited reach than the proposed application. It concerns feedback in user-facing workflows and expressly lacks a universal cadence or stopping rule. A coordinator reviewing an independent agent has different control: the coordinator can inspect the deliverable, compare it to the original brief, request a bounded correction, or end the delegation. It does not follow that user-facing feedback patterns establish how often to reassign work, what evidence a delegated agent must produce, or whether a signal should be separate from the final acceptance check in every task. Those are design inferences, not demonstrated findings.

The better integration, if any, is to sharpen the existing handoff and review points rather than insert a new lifecycle. The handoff can make the requested artifact and task-relevant acceptance evidence explicit when they are not already obvious. The review can choose among accept, a targeted follow-up that identifies the discrepancy and desired evidence, or stop/escalate when the gap is material or the task is no longer bounded. This uses the synthesis’s most useful elements—explicit next action and consequence-aware stopping—without requiring an artificial metric for qualitative work or another review stage for every task. For tasks with objective outputs, the signal may be a direct check; for exploratory work, it may be a concise evidence trail and judgment against the brief. A single universal “signal” field risks forcing false precision.

The failure mode of an underspecified follow-up is an open-ended retry loop: the agent is asked to “improve” a result, the target shifts, and the coordinator spends more effort than the deliverable warrants. Explicitly limiting follow-up to a named gap, a bounded request, and a stop/escalation decision helps prevent that. A fixed maximum number of retries is not justified by the supplied evidence; the right boundary depends on consequence, evidence, cost, and whether the original task remains valid.

The alternative of making no change is credible because the current skill, as described in the brief, already has checkpoints and handoff assessment. Before editing it, the owner should confirm there is a real recurring failure—such as agents returning unsupported conclusions or coordinators repeatedly asking vague follow-ups. If no such failure exists, adding guidance solely to encode KNOW-02 is documentation churn. If a failure does exist, a short clarification alongside the current delegation/review instructions is more proportionate than a shared, separately loaded reference or a new mandatory phase. A shared reference could preserve conceptual detail for skills that need it, but it adds discovery/loading and maintenance overhead for a narrow pilot; copying the whole synthesis would duplicate caveats and invite overstatement.

## Strongest counterargument
Independent agents can return polished but ungrounded work, and a brief-plus-final-review pattern may discover that only after substantial work has been spent. Making the expected evidence and a meaningful mid-task checkpoint explicit could catch divergence earlier, make corrections cheaper, and improve auditability. This case strengthens if task histories show that agents commonly misunderstand scope, if delegated work is consequential, or if multi-step tasks produce useful early signals before the final artifact is ready. Under those conditions, a task-specific checkpoint should be planned in the handoff. The evidence summarized in the brief does not establish that such checkpoints should be routine across plan-management tasks, nor that they reduce total cost for this class of work.

## Key risk or opportunity
The main risk is converting a qualified, context-specific synthesis into a universal agent-management protocol. The opportunity is narrower: prevent vague or unbounded follow-ups by tying each requested correction to an observable gap and an explicit accept, stop, or escalate decision.

## Evidence and assumptions
Facts supplied by the brief: KNOW-02 synthesizes feedback loops in user-facing AI-agent workflows; it recommends meaningful signals, explicit next actions, checkpoints and consequence/evidence-aware stopping, and distinguishes an outcome check from a cycle-driving signal. Its evidence is varied and task/system-specific, and it establishes neither a universal cadence nor a universal stopping rule. The brief also states that `$plan-management` already keeps user-facing context with the coordinator, sets checkpoints, delegates when useful, checks handoffs against briefs and criteria, and cautions against unnecessary phases or reviews.

Inference: these principles can usefully inform independent-agent delegation, but that transfer is not validated by the evidence described. The suggested clarification is a judgment about minimizing process overhead while making follow-up bounded; it is not an empirical claim that this wording improves agent outcomes.

Assumptions and missing information: I assume current handoff guidance is generally followed and that no known incident data was included. The brief does not provide examples of failed agent handoffs, review cost, correction success, or the amount of work lost when checkpoints occur late. Those data could show that a planned early checkpoint has positive value for a subset of tasks. No external sources were used because the recommendation turns on the supplied synthesis’s scope and on local failure/cost evidence that web research could not resolve.
<!-- COUNCIL-RESPONSE-END -->
