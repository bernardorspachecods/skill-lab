---
name: test-first
description: Use test-first development for new features or bug fixes when the behavior is clear enough to specify before implementation and TDD is a good fit. Also use when the user asks for TDD, red-green-refactor, or a regression test before implementation.
---

# Test first

Use this workflow when implementing a feature or fixing a bug whose expected behavior is clear enough to drive with tests. Do not force it onto prototypes, exploratory work, documentation, visual experimentation, or trivial configuration changes.

Before coding, read the applicable `AGENTS.md`, `READ.md`, `CONTEXT.md`, ADRs, and test conventions. Identify the first behavior and the public seam through which it should be observed. Ask for clarification only when the behavior or seam is genuinely ambiguous.

Work in small vertical slices:

1. Write one focused test for a concrete behavior.
2. Run it and confirm that it fails for the expected reason.
3. Implement the smallest change that makes it pass.
4. Run the test again, then refactor while it is green.
5. Repeat for the next behavior.

Tests should describe observable behavior through public interfaces and use independent expected values. Prefer real collaborators; mock system boundaries only when necessary. Avoid tests coupled to implementation details, private methods, call counts, or duplicated implementations. Read [tests.md](tests.md) for examples and [mocking.md](mocking.md) when deciding how to isolate a boundary.

For bug fixes, start with a regression test that reproduces the bug. If the test does not fail for the expected reason, investigate before changing production code. If tests cannot run or their result is inconclusive, report that clearly and do not claim the cycle is complete. Do not write a large batch of speculative tests or implementation ahead of the next slice.

Finish when the requested behavior is covered, the relevant tests pass, and no speculative behavior was added. Report the tests run and any limitations.

Example:

```text
$test-first Adiciona suporte para cupões de desconto, começando pelos comportamentos esperados.
```
