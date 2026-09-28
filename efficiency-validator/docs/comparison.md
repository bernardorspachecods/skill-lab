# Paired comparison

The comparison layer consumes two command reports, two `quality-report-1`
artefacts, and a policy configuration:

```json
{
  "baseline_variation": "without-skill",
  "candidate_variation": "with-skill",
  "primary_metric": "tokens",
  "relative_tolerance": 0.05
}
```

The pair must match on case, task hash, target/runtime revision, model, Codex
version, observer version, sandbox, sidecar revision, and oracle identity.
Each manifest must also contain complete prompt/oracle/controlled-variation
provenance with internally consistent hashes. Variation labels must be
explicit and different. A missing or mismatched identity is `inconclusive`
with evidence status `blocked`.

Policies may provide `baseline_forbidden_markers` to detect an intervention
that appeared in the baseline trace. A marker match blocks the pair instead of
silently treating the baseline as natural.

The initial normalized dimensions are tokens, command count, and filesystem
event count. A missing dimension remains `unavailable`; it is never treated as
zero. The primary metric determines `better`, `same`, or `worse`. If the
primary metric improves while another available metric regresses, the result is
`tradeoff`.

Quality is applied first: a failed candidate is `worse`, an indeterminate gate
is `inconclusive`, and no cost saving can override a quality failure.

Generate a report with:

```text
python3 scripts/compare_codex.py \
  --baseline-report runs/base/report.json \
  --candidate-report runs/candidate/report.json \
  --baseline-quality runs/base/quality.json \
  --candidate-quality runs/candidate/quality.json \
  --config comparison-policy.json \
  --output comparison.json
```

The output schema is `comparison-report-1` and includes pair validation,
quality statuses, measurements, deltas, reasons, the verdict, and a
`prompt_diff` object. `prompt_diff` retains both complete explicit prompts,
their hashes, exact-equality status, and a unified diff when both prompts are
available. The individual run reports retain all valid protocol events under
`observability.raw_events`; unknown future event types are not discarded.

Multiple comparison reports can be aggregated with the library's
`aggregate_comparisons` function. Mixed verdicts remain `inconclusive`, and a
`supported` aggregate requires the configured minimum number of valid,
quality-passing, provenance-complete replicates.

The CLI form is:

```text
python3 scripts/aggregate_codex.py \
  --comparison runs/pair-01/comparison.json \
  --comparison runs/pair-02/comparison.json \
  --comparison runs/pair-03/comparison.json \
  --output runs/aggregate.json
```

Legacy comparison reports without the new evidence status remain readable but
aggregate as blocked rather than becoming supported evidence.

For human review, render a single Markdown report and compact JSON summary from
the saved runs and analysis artefacts:

```text
python3 scripts/decision_report_codex.py \
  --run baseline=runs/base/report.json \
  --run candidate=runs/candidate/report.json \
  --quality baseline=runs/base/quality.json \
  --quality candidate=runs/candidate/quality.json \
  --comparison runs/pair-01/comparison.json \
  --comparison runs/pair-02/comparison.json \
  --aggregate runs/aggregate.json \
  --output runs/decision-report.md
```

The renderer shows prompts, normalized costs, quality, filesystem summaries,
pair deltas, aggregate variance, limitations, and the final evidence status.
Raw events and full technical reports remain available through links instead
of being expanded into the decision view.
