---
plan_id: LR-06.SP-03
kind: subplan
parent: LR-06
phase: S3
status: complete
depends_on:
  - KNOW-02.AUD-01#claims-and-evidence
  - KNOW-02.AUD-02#claims-and-evidence
consumers: []
---

# LR-06.SP-03

## Objective

Assess when agent-workflow loops help, fail, or remain unproven, including
what evidence demonstrates about loop effectiveness, how effectiveness varies
by conditions, and the costs and human factors that shape use.

## Scope

Build on S1 and S2's reviewed evidence, then search for independent
evaluations, contrary findings, and boundary conditions that could change the
case-level conclusions. Examine feedback reliability and relevance, initial
output quality, loop length and stopping, independent verification, resource
comparability, user effort and control, proxy alignment, and failure recovery.
Investigate adverse patterns such as reinforcing an error, over-correction,
proxy optimization, evaluator blind spots, unnecessary iterations, and
automation that obscures when the person must intervene. Treat these as
discovery prompts, not assumed findings.

For every conclusion, distinguish source-reported outcomes from explanations
and cross-case synthesis. Do not treat a metric optimized inside the loop as
an independent measure of user value. Keep findings bounded to tested tasks,
systems, participants, and study designs.

## Output

Complete `LR-06.RES-03.audit.md` as a standard-rigor cross-case evidence
record on evaluation, effectiveness conditions, costs, human factors, and
failure modes. Link claims to specific source evidence and preserve conflicts,
limitations, and search paths in `LR-06.RES-03.working.md`.

## Sequence

1. **S1 — Compare conditions and failure evidence**
   - **Action:** Follow standard `$research` rigor, starting from S1–S2 and
     checking material alternatives, nulls, harms, and independent outcome
     measures.
   - **Output:** Completed audit and retained discovery log.
   - **Exit check:** Measures and claims are traceable; direct findings are
     separated from transfer inferences; evidence limitations and review
     findings are reconciled.

## Completion criteria

- The audit states what each measure establishes and whether it is
  independent of the loop's own feedback signal.
- Benefits, costs, and failure patterns are reported only at the strength and
  scope supported by evidence.
- Conclusions explain which conditions appear to improve or weaken results
  and distinguish directly tested conditions from cross-case inference.
- Located null, mixed, adverse, and countervailing evidence is represented;
  categories with no located evidence are stated explicitly, and overlapping
  sources are not counted as independent confirmation.
- The audit and working log follow standard `$research` rigor, pass
  independent review, and are reconciled by the coordinator before S4 starts.

## Outcome

Completed. The reviewed audit synthesizes condition-dependent outcomes,
measurement independence, iteration/stopping, user effort, resource
comparability, and failures across direct and adjacent evidence. Independent
review's required correction was resolved: E8's tests are external to model
self-report but reused as loop feedback and final score. Remaining evidence
gaps include adaptive-stop comparisons with independent quality and full
resource costs. S3 is available as input to S4.
