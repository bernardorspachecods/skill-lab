# Baseline observes command-level evidence

Status: accepted

The natural baseline reports only externally observable Codex command/message
events and parser completeness. It must not infer file reads, physical scans,
result counts, tokens, or hidden reasoning from shell commands or agent prose;
file-level metrics require a separately validated runtime signal. Evaluator
oracles stay outside the agent-facing repository and are joined after each
run, while normalized answer claims are scored separately from route evidence.

## Consequences

- A complete command trace can still have unavailable file-level metrics.
- Every run needs a provenance manifest joining repository, task, runtime,
  validator, and sidecar revisions.
- Future locators, navigation protocols, or filesystem instrumentation are
  interventions or separate observation layers, not part of this baseline.
