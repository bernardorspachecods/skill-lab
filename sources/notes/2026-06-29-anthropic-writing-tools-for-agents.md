# Source Note

Source: https://www.anthropic.com/engineering/writing-tools-for-agents

Date inspected: 2026-06-29

Source date: Published Sep 11, 2025 on the Anthropic engineering page; verified 2026-06-30.

Authority level: Primary Anthropic engineering guidance on agent tool design.

Relevant sections inspected:

- Tool definitions.
- Tool selection and descriptions.
- Return formats.
- Token efficiency.
- Tool evaluations.

Retained claims:

- Tools are contracts between deterministic systems and nondeterministic agents.
- More tools are not automatically better.
- Names, descriptions, parameter schemas, and return shapes affect agent reliability.
- Tool outputs should be concise and actionable.
- Realistic evals should inspect tool-call behavior, not only final answers.

Excluded claims:

- Tool examples that do not generalize to this repo.
- Deep implementation details outside documentation operating guidance.

Review cadence:

Review quarterly or when changing tool-design guidance.
