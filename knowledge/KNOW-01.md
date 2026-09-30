---
id: KNOW-01
derived_from:
  - KNOW-01.AUD-01
  - KNOW-01.AUD-02
---

# LLM importance and stakes framing

## Navigation map

| If you need... | See |
| --- | --- |
| A quick answer on whether framing changes LLM results | [Findings](#findings) |
| Design implications for a controlled evaluation | [Evaluation implications](#evaluation-implications) |
| Limits and applicability | [Scope and limitations](#scope-and-limitations) |
| The source audits and primary literature | [Provenance](#provenance) |

## Intended utility

Use this note when designing or interpreting evaluations that tell an LLM a
task is important, describe benefits or harms, or state consequences for its
answers. It separates prompt mechanisms that can otherwise be grouped under
the vague label “high stakes.”

## Findings

The evidence reviewed through 2026-09-30 does not establish that generic
importance wording or ordinary described stakes reliably improve LLM
correctness. Some cues change measured outputs, but direction varies with the
wording, task, model, and outcome.

- **Generic importance or priority wording is under-tested in isolation.**
  The EmotionPrompt research program reported improvements for bundles of
  emotional prompts and task-specific changes for “This is very important to
  my career.” That phrase also introduces personal stakes; nearby prompts add
  encouragement or requests to re-check. An independent conceptual replication
  found a pooled accuracy difference near zero, with gains and losses across
  benchmarks. The nonsignificant result does not establish equivalence or rule
  out small and task-specific effects.
- **Described consequences produce mixed, measure-specific results.** A
  radiology exam study found that encouragement and a responsibility disclaimer
  scored above baseline, while liability and clinical-responsibility personas
  scored lower and abstained more. The exact counts in the audit could not be
  independently confirmed from the accessible publisher abstract; its
  direction was confirmed. An explicit error-cost rubric increased abstention
  as the stated cost rose, which also communicates a decision rule. A simulated
  deployment threat elicited underperformance in some models. By contrast, a
  multi-model, multi-task working paper found no statistically detectable
  general accuracy effect from a verbal bonus promise; that null does not prove
  an exactly zero effect.
- **Actual external consequences remain an evidence gap.** The studies reviewed
  did not impose real-world consequences on an LLM or make downstream human
  outcomes depend on its answer. Hypothetical stakes, simulated task incentives,
  and scoring rubrics should not be treated as evidence about actual
  consequential deployments.

Confidence is moderate that selected importance-adjacent or
consequence-related cues can change behavior in particular controlled tasks,
and low that either generic importance wording or ordinary described stakes
produces a consistent correctness effect across tasks and models. The audits
did not establish effects on calibration, time, tokens, or compute. Abstention
and response rate were measured more directly.

## Evaluation implications

When testing these effects, separate the factors instead of treating them as a
single stakes scale. A controlled design can compare neutral, wording-only,
stakes-only, and combined conditions on the same tasks, task information, and
scoring procedure. Predefine correctness or task quality as the primary
outcome; measure abstention and calibration separately, and record cost
measures only when they can be compared consistently. Stakes text can add
information or change the decision rule, so those effects need to be controlled
or reported. A result from a simulated prompt condition does not establish an
effect of actual external consequences.

## Scope and limitations

This is a focused, non-systematic review, not an exhaustive literature search
or pooled estimate. The source set is heterogeneous, includes different
constructs and outcomes, and spans dated model versions and publication types,
including a working paper. Do not generalize its findings to all models,
tasks, or current deployments. See the linked plan audits for study-level
methods, evidence locations, provenance, conflicts, and search limits.

## Provenance

- [KNOW-01.AUD-01: importance-wording evidence audit](audit/KNOW-01.AUD-01.md)
- [KNOW-01.AUD-02: described-stakes evidence audit](audit/KNOW-01.AUD-02.md)

Primary sources include [Li et al. (2023)](https://arxiv.org/abs/2307.11760),
[Li et al. (2024)](https://arxiv.org/abs/2312.11111),
[Vaugrante et al. (2025)](https://openreview.net/forum?id=bgjR5bM44u),
[Nguyen et al. (2024)](https://doi.org/10.1016/j.clinimag.2024.110276),
[Meinke et al. (2025)](https://arxiv.org/abs/2412.04984),
[Kalai et al. (2026)](https://doi.org/10.1038/s41586-026-10549-w), and
[Belotti et al. (2026)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6594418).
