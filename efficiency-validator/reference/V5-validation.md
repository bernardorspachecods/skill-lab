---
plan_id: V5
kind: subplan
parent: V0
phase: 5
status: complete
depends_on: [V2, V3, V4]
consumers: [future skill evaluations, context-lab reports]
---

# V5 — Fixtures, migration, and revalidation

## Objective

Prove the hardened contract, preserve the old artifacts as history, and only
resume skill evaluations when the validator can audit them end to end.

## Scope

- Fixtures for complete, missing, mismatched, partial, contaminated, and
  unavailable evidence.
- Legacy E0–E5 artifact reading without treating it as new evidence.
- Deterministic replay and report hashing.
- One post-hardening controlled pair followed by repeated replicates.
- Retrospective classification of existing runs as exploratory.

## Output

A regression-verified hardened validator and a new evaluation set whose reports
are provenance-complete and auditable.

## Sequence

1. **V5-S1 — Build the regression matrix**
   - **Action:** Cover every new provenance, capture, report, quality, pair, and
     aggregation branch.
   - **Output:** Complete fixture matrix.
   - **Exit check:** Every invalid evidence state has a deterministic reason.

2. **V5-S2 — Replay and migrate**
   - **Action:** Reproduce reports from saved bundles and classify legacy runs
     without inventing missing metadata.
   - **Output:** Replay evidence and historical-status policy.
   - **Exit check:** Same inputs produce the same report; missing history stays
     missing.

3. **V5-S3 — Re-run evaluation**
   - **Action:** Capture a controlled skill evaluation only after V1–V4 gates
     pass, then aggregate enough replicates to expose variance.
   - **Output:** First post-hardening evaluation.
   - **Exit check:** Every published result links exact prompts, provenance,
     quality reviews, raw traces, and aggregate calculations.

## Completion criteria

- Full regression suite passes.
- Legacy runs remain accessible but are not silently upgraded to trusted data.
- A post-hardening evaluation can be reproduced and audited from saved files.
- The evaluator is ready for new skill experiments with explicit limitations.

## Verification record — 2026-09-24

- Regression suite: `.venv/bin/python -m pytest -q` — 50 passed.
- Legacy replay: the historical three-pair `check-docs` set remains readable but
  aggregates as `inconclusive` and `blocked` (`2 better`, `1 worse`) because its
  manifests lack complete provenance.
- Post-hardening evidence: runs `run-044`, `run-045`, and `run-046` each have
  exact prompts, prompt hashes, oracle digests, controlled variations, raw
  events, token usage, quality reports, and comparison reports.
- Post-hardening aggregate: `runs/check-docs-post-hardening-aggregate.json` is
  `inconclusive` and `exploratory` (`2 better`, `1 same`), so no skill claim is
  promoted. Token deltas range from `-23,786` to `-200,273`; filesystem traces
  are explicitly unavailable in all six runs.
- Reproducibility: stable JSON fingerprints are covered by
  `tests/test_reproducibility.py`; saved reports and aggregate inputs
  are replayable from their local paths without inventing missing metadata.
- Limitation carried forward: authoritative filesystem traces are still an
  unavailable source and remain a visible limitation, not a synthesized metric.
