# Analysis acceptance

Evidence date: 2026-09-26. This is the first operational comparison produced
from the phase 1 bundles.

The command was:

```sh
python3 scripts/compare_operational.py \
  --baseline ../evals/efficiency-operational/runs/baseline-fixed \
  --candidate ../evals/efficiency-operational/runs/context-fixed \
  --output ../evals/efficiency-operational/comparison-01
```

The [comparison report](../../evals/efficiency-operational/comparison-01/comparison.md)
and [structured result](../../evals/efficiency-operational/comparison-01/comparison.json)
show one completed pair using the same prompt, starting target, requested model,
reasoning effort and sandbox. The candidate includes one context overlay. Both
explicit evaluator checks passed.

Observed candidate deltas in this pair:

- total tokens: −700 (−1.04%);
- input tokens: −615 (−0.93%);
- output tokens: −85 (−11.72%);
- task time: −4.59 seconds (−14.47%);
- observed commands and tool items: unchanged at 3 and 4;
- returned command output: −58 UTF-8 bytes (−1.79%).

The result is deliberately labelled `exploratory`: a single pair supports a
case observation, not a general claim that the context variant is better. The
quality gate covers only the explicit evaluator checks, not a universal answer
quality judgment. Reading metrics cover CLI-emitted tool inputs/results and do
not certify complete filesystem reads, internal search work or model context.
Missing metrics remain unavailable. A mismatched task prompt, starting target,
requested model, reasoning effort, sandbox, incomplete collection or failed
quality check blocks the comparison.

The comparison is derived offline from retained operational reports. It can be
regenerated after analysis code changes without another model execution.
