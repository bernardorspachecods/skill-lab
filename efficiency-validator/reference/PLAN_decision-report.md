---
plan_id: D0
kind: root
parent: null
phase: root
status: complete
depends_on: []
consumers: [efficiency-validator, context-lab reports, future skill evaluations]
---

# Human decision report

## Objective

Turn raw run, quality, comparison, and aggregate artefacts into one
decision-oriented report that a person can read without opening intermediate
JSONL traces, while preserving links to the complete technical evidence.

## Scope

- Compact normalized JSON summary for machines and a Markdown report for people.
- Exact task prompt(s), run labels, quality status, costs, calls, filesystem
  summary, deltas, trade-offs, limitations, and verdict evidence.
- Automatic aggregation of existing report/comparison/aggregate files without
  changing their authoritative raw contents.
- Links to raw technical artefacts instead of embedding every event.

## Output

`scripts/decision_report_codex.py` and its library renderer, producing
`decision-report.md` and optionally `decision-report.json` for any saved run
set.

## Sequence

1. **D0-S1 — Define the human schema**
   - **Action:** Select the decision fields and compact summaries that hide
     intermediary protocol noise without hiding evidence or limitations.
   - **Output:** Renderer contract and fixtures.
   - **Exit check:** A reviewer can identify the task, prompt variation, costs,
     quality, evidence status, trade-offs, and limitations from one document.

2. **D0-S2 — Implement the renderer**
   - **Action:** Build the JSON/Markdown renderer and CLI over saved artefacts.
   - **Output:** Reusable decision-report generator.
   - **Exit check:** A pair report contains no raw event dump and links its
     technical sources.

3. **D0-S3 — Generate and validate an example**
   - **Action:** Render the existing post-hardening evaluation and run the full
     regression suite.
   - **Output:** Human-readable report and compact machine summary.
   - **Exit check:** The report preserves the inconclusive conclusion and all
     material limitations from the authoritative comparison.

## Completion criteria

- Markdown is the default human-facing output.
- JSON summary is compact, deterministic, and suitable for dashboards.
- Prompts are visible in full, while raw events remain linked rather than
  expanded.
- Costs, calls, context/input usage, filesystem summaries, quality, deltas,
  trade-offs, verdict, evidence status, and limitations are present.
- Existing reports are not modified and the full suite passes.

## Verification record — 2026-09-25

- Full suite: `.venv/bin/python -m pytest -q` — 55 passed.
- Plan validator: 14 plan documents, 0 errors, 0 warnings.
- Example output: `runs/check-docs-post-hardening-decision-report.md` and its
  adjacent compact JSON summary.
- The example contains all three pair comparisons, full prompts, normalized
  run costs, quality statuses, filesystem summaries, aggregate variance,
  limitations, and technical artefact links. It does not embed raw event
  streams.
