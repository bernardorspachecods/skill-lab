# Context Lab Harness Agent Rules

Read [CONTEXT.md](CONTEXT.md) first, then use [PLAN.md](PLAN.md) as the
canonical experiment plan.

## Repository-specific rules

- Keep the synthetic target separate from this harness.
- Do not add validator, evaluator, task, or experiment-control files to the
  target repository.
- Keep evaluator-only ground truth outside both the target and measured
  workspace.
- Do not add locator instructions, navigation protocols, or prompt changes to
  natural-baseline tasks.
- Treat agent self-reported paths as secondary evidence only.
- Record material changes to scope, measurement boundary, or evaluation design
  in `PLAN.md` before implementation.

## Verification expectation

Check the harness, validator, and target context links, run the applicable
validators and tests in each affected project, and keep natural-baseline
revisions pinned.
