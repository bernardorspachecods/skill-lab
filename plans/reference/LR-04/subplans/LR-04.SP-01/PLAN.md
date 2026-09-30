---
plan_id: LR-04.SP-01
kind: subplan
parent: LR-04
phase: S1
status: complete
depends_on: []
consumers: []
---

# LR-04.SP-01

## Objective

Determine what existing empirical evidence shows about whether generic
importance or priority wording in a prompt changes LLM task performance.

## Scope

Research prompts that explicitly label a task as important, urgent, high
priority, or otherwise signal that the model should treat it as especially
important. Include adjacent terminology only when the source tests the same
kind of verbal priority cue. Keep this mechanism distinct from prompts that
describe concrete benefits, harms, or consequences; use studies that compare
both mechanisms as relevant cross-mechanism evidence and identify the overlap.

Focus on empirical studies of LLM performance. Extract the wording or
operational definition of the cue when available; task, model and version,
comparison condition, outcome measure, results, and limitations. Assess task
quality or correctness as the primary outcome and capture instruction
following, calibration, response characteristics, or resource use when
measured. Distinguish measured effects from author interpretation and from
proposed mechanisms such as extra effort or attention. Include null and
negative findings. Do not infer a general effect from a single model, task,
or benchmark. No fixed publication cutoff is set.

## Output

Complete `LR-04.RES-01.audit.md` as a standard-rigor evidence record with a
focused question, claim matrix, linked evidence entries, source ledger,
conflicts and limitations, and validation/stop rationale. Use primary study
sources when accessible and preserve bibliographic identity, dates, methods,
results, and evidence locations. The audit is the research output for review.

## Sequence

1. **S1 — Map and synthesize importance-cue evidence**
   - **Action:** Follow the research skill's standard workflow and academic
     research mode. Find, inspect, and compare primary empirical studies of
     explicit importance or priority wording; check backward/forward
     references and search for null or conflicting results.
   - **Output:** A completed, cited research audit at the scaffolded path.
   - **Exit check:** Every material conclusion is linked through an evidence
     entry to a source and a specific page, section, table, figure, or data
     location where available; limits and unresolved gaps are explicit.

## Completion criteria

- The audit states what counts as an importance/priority cue and keeps it
  distinct from concrete stakes descriptions.
- It identifies what the located evidence says about task quality or
  correctness and reports other outcomes only where studies measured them.
- It records study conditions and material limits needed to judge transfer
  across models and tasks.
- Important positive, null, conflicting, and negative evidence found through
  the prescribed search is represented, with source independence assessed.
- Claims, evidence, and sources are traceable and uncertainty is calibrated;
  absence of evidence is not presented as evidence of no effect.

## Outcome

Research and independent review are complete. The audit concludes that
importance-adjacent prompt cues can have context-dependent effects, but the
available evidence does not establish a reliable general improvement from
bare importance or priority wording. There is no required correction. The
reviewer recommends, optionally, recording exact search venues/query strings
and preserving the replication's uncertainty caveat if numerical details are
used in the root synthesis. The user approved this subplan for use in the root
synthesis after review. The audit was promoted to repository knowledge as
`KNOW-01.AUD-01`.
