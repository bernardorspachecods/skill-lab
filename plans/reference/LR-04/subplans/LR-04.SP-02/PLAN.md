---
plan_id: LR-04.SP-02
kind: subplan
parent: LR-04
phase: S2
status: complete
depends_on: []
consumers: []
---

# LR-04.SP-02

## Objective

Determine what existing empirical evidence shows about whether prompts that
describe real-world benefits, harms, or consequences change LLM task
performance.

## Scope

Research LLM studies where prompts describe plausible consequences associated
with the model's output, including hypothetical high-stakes scenarios, actual
consequential settings, or real incentives when studied. Separate those cases
in the synthesis: a prompt's hypothetical narrative does not itself create
real-world stakes, and actual incentives or deployment consequences may
introduce mechanisms beyond prompt framing. Keep generic importance or
priority wording distinct, using studies that compare both as relevant
cross-mechanism evidence and identifying the overlap.

Focus on empirical studies of LLM performance. Extract the described stakes or
actual consequence/incentive, task, model and version, comparison condition,
outcome measure, results, and limitations. Assess task quality or correctness
as the primary outcome and capture instruction following, calibration,
response characteristics, or resource use when measured. Distinguish measured
effects from author interpretation and proposed mechanisms. Include null and
negative findings. Do not infer a general effect from a single model, task,
or benchmark. No fixed publication cutoff is set.

## Output

Complete `LR-04.RES-02.audit.md` as a standard-rigor evidence record with a
focused question, claim matrix, linked evidence entries, source ledger,
conflicts and limitations, and validation/stop rationale. Use primary study
sources when accessible and preserve bibliographic identity, dates, methods,
results, and evidence locations. The audit is the research output for review.

## Sequence

1. **S1 — Map and synthesize described-stakes evidence**
   - **Action:** Follow the research skill's standard workflow and academic
     research mode. Find, inspect, and compare primary empirical studies of
     described consequences, actual incentives, or consequential settings;
     check backward/forward references and search for null or conflicting
     results.
   - **Output:** A completed, cited research audit at the scaffolded path.
   - **Exit check:** Every material conclusion is linked through an evidence
     entry to a source and a specific page, section, table, figure, or data
     location where available; limits and unresolved gaps are explicit.

## Completion criteria

- The audit distinguishes hypothetical stakes descriptions from actual
  consequences or incentives and keeps both distinct from generic importance
  wording.
- It identifies what the located evidence says about task quality or
  correctness and reports other outcomes only where studies measured them.
- It records study conditions and material limits needed to judge transfer
  across models and tasks.
- Important positive, null, conflicting, and negative evidence found through
  the prescribed search is represented, with source independence assessed.
- Claims, evidence, and sources are traceable and uncertainty is calibrated;
  absence of evidence is not presented as evidence of no effect.

## Outcome

Research and independent review are complete. The audit finds mixed,
mechanism-specific effects from described consequences, simulated incentives,
and decision rubrics, with no located direct test of real external outcomes
contingent on an LLM's answer. There is no required correction. The reviewer
recommends, optionally, adding a more precise locator for E1's exact accuracy
counts if the primary full text is available, and keeping explicit scoring
thresholds distinct from ordinary consequence narratives in synthesis. The
user approved this subplan for use in the root synthesis after review. The
audit was promoted to repository knowledge as `KNOW-01.AUD-02`.
