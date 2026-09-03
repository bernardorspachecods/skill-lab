---
name: reality-check
description: Re-ground an agent that is drifting, hallucinating, losing the task context, or pursuing unsupported reasoning. Invoke manually when the current line of work no longer seems reliable.
---

# Reality check

Use this skill when the agent appears to be delusional, inventing facts, ignoring evidence or repository guidance, losing sight of the original problem, or adding unjustified complexity. Treat the current line of reasoning as suspect.

Pause the current task. Do not continue implementing or make new claims until the situation is re-grounded.

1. Restate the original objective, the desired outcome, and the current decision or blocker.
2. Separate what is confirmed from what is inferred, assumed, unknown, or contradicted. Mark claims that lack evidence.
3. Re-read the relevant user instructions, repository guidance, documentation, code, tests, sources, errors, or runtime state. Use only the smallest context needed to resolve the uncertainty.
4. Identify where the reasoning drifted: stale context, unsupported assumption, ignored constraint, misunderstood requirement, or premature solution.
5. Re-evaluate the plausible interpretations or approaches. Prefer the simplest supported explanation and state meaningful alternatives, risks, and open questions.
6. Report the corrected understanding, evidence, uncertainty, and recommended next step. Ask one focused question only if a real decision remains unresolved.

Be candid about mistakes and uncertainty. Do not rationalize the previous approach, hide contradictions, treat plausibility as proof, or create more process without evidence. Do not modify files during this recovery. Continue only after the user confirms the direction or the corrected understanding is sufficiently grounded for a low-risk next step.

Example:

```text
$reality-check Acho que estás a começar a inventar detalhes e a afastar-te do problema original.
```
