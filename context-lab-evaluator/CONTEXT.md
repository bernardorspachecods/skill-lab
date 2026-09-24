# Context Lab Evaluator

This sidecar stores evaluator-only ground truth for the sibling
`context-lab` repository. It must not be placed inside the agent-facing repo
or made available in a Codex baseline session.

## Destinations

- [oracles/](oracles/) — expected sources and answer criteria for manual cases.

Each oracle separates authoritative paths, implementation/supporting paths,
required claim ids, and disallowed overclaims. A host-side review may provide
normalized claim ids after reading an answer; the evaluator then computes
coverage deterministically. The sidecar is never mounted into the measured
agent's repository view.

The evaluator reads prompts from `context-lab/evaluation/tasks/` and joins them
with these oracles after the agent run has finished.
