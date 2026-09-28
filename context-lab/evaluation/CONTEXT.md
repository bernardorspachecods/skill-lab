# Evaluation Cases

This area owns manually authored tasks and controlled documentation variants.
Evaluator ground truth is external to this harness area. Evaluation evidence
is not canonical product or architecture guidance.

## Destinations

- [tasks/](tasks/) — manual task cases and expected evidence.
- [variants/](variants/) — controlled documentation defects created after the
  canonical baseline is stable.

Evaluator-only ground truth is kept outside the agent-facing repository. It is
joined to a case only after the Codex run has finished. Baseline runs must
expose only the pinned canonical repository to the measured agent; the host
evaluator owns the join.
