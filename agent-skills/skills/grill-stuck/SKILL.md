---
name: grill-stuck
description: Recover from repeated failed attempts by diagnosing the cause, revisiting repository guidance, comparing alternatives, and choosing a robust direction. Use grill for a first-pass idea critique and reality-check when unsupported reasoning is the main problem.
---

# Recover from a stuck approach

Use this skill when the agent is stuck, repeating an approach, accumulating failures, or reaching for a workaround without understanding the cause. Pause implementation and re-evaluate from first principles.

When a repository is in scope, read applicable guidance (`AGENTS.md`, `READ.md`, and equivalents), then inspect relevant documentation, code, tests, errors, and recent changes. Treat architecture and conventions as constraints.

Work through the following:

- separate the symptom from the desired outcome;
- review attempts, failures, and evidence that rules hypotheses out;
- identify the likely root cause and surface assumptions, invariants, edge cases, and failure modes;
- compare plausible alternatives, including a simpler or more maintainable direction;
- recommend the option that fits the application's rules and long-term needs.

Be honest about uncertainty. Do not repeat failed approaches, weaken tests, ignore guidance, or invent complexity. Use focused, non-destructive diagnostics when they distinguish hypotheses; do not modify the implementation.

## Clean up failed attempts

After diagnosing the cause and before implementing:

- inspect the current changes;
- revert or remove only changes attributable to the failed attempts;
- preserve unrelated or uncertain changes;
- state the cleanup scope and ask before destructive actions;
- verify the baseline, then implement the approved direction.

If ownership is uncertain, leave the change untouched and report it.

Report the diagnosis, cleanup scope, recommendation, and open questions. Wait for approval before cleanup or implementation.
