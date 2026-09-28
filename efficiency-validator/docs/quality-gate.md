# Quality gate

The quality gate is deliberately separate from observable cost. It consumes a
run report, the evaluator oracle, and an explicit normalized review:

```json
{
  "required_claim_ids": ["workspace-membership-required"],
  "disallowed_claims": [],
  "answer_complete": true,
  "authority_status": "pass",
  "support_status": "pass"
}
```

`pass` requires all required claims, no prohibited claims, a complete answer,
approved authority and support, a complete Codex stream, and no parser issues.
`fail` means a concrete quality violation is known. `indeterminate` means the
review or runtime evidence is insufficient to decide safely.

The review is an evaluator-side normalized input. The gate does not promote
agent prose or claimed paths to authoritative evidence, and it never uses
lower token or filesystem cost to override a failed or indeterminate quality
result.

Generate a report with:

```text
python3 scripts/quality_codex.py \
  --report runs/run-030/report.json \
  --oracle ../context-lab-evaluator/oracles/001-create-task.json \
  --review /path/to/quality-review.json \
  --output runs/run-030/quality.json
```

Omit `--review` to obtain an explicit `indeterminate` result. The report
schema is `quality-report-1` and is the input contract for E4.
