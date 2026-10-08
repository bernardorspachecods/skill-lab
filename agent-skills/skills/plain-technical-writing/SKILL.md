---
name: plain-technical-writing
description: Improve technical documentation, agent skills, runbooks, and repository context for clarity while preserving facts, structure, links, commands, and identifiers. Use only when the user explicitly asks for a technical-writing rewrite or review. Do not use for code changes, marketing copy, creative writing, normal replies, or repository-structure redesign.
---

# Plain Technical Writing

Use this skill as an editorial pass. Improve the prose without changing the document's architecture or meaning.

## Before editing

1. Identify the artifact: skill, context file, runbook, error message, report, or release note.
2. Read the nearest repository guidance and preserve its authority order.
3. Separate prose from content that must remain exact.
4. Note whether each statement describes current behavior, intended behavior, or an uncertain claim.

## Writing rules

- Prefer short sentences and active voice. Name the actor when it matters.
- Put a condition before the action: `If X, do Y.`
- Use one consistent term for each concept. Define a technical term at first use when the audience may not know it.
- Remove filler, vague intensifiers, and promotional wording. Replace claims such as “fast” or “robust” with observable facts.
- Use complete grammar and ordinary verb forms. Treat 20 words for procedures and 25 words for descriptive prose as review signals, not hard limits.
- State the current behavior, intended change, and uncertainty separately. Do not turn a possibility into a fact.
- Put the action or command before its warning when giving operational guidance.
- Preserve exceptions and scope. A shorter sentence must not remove a condition, dependency, or limitation.

## Preserve exactly

Do not alter facts, links, frontmatter, headings, lists, tables, commands, code blocks, file paths, identifiers, quoted errors, product names, or navigation structure. Do not translate or normalize technical terms when that would change their meaning.

Keep Markdown structure when it carries meaning. In skills and context files, headings and links define the route through the documentation. In runbooks, commands and their order define the procedure.

## Artifact-specific emphasis

- For skills and context files, clarify ownership, entry points, dependencies, and the difference between instructions and descriptions.
- For procedures and runbooks, use condition-first steps and one action per sentence.
- For error messages, separate what happened, the known cause, and the next action.
- For reports and release notes, state the time, fact, impact, and remaining uncertainty.

Read [use-cases.md](references/use-cases.md) for these patterns and [word-swaps.md](references/word-swaps.md) for optional lexical cleanup. Use the [linter](scripts/lint_plain_english.py) only as an advisory review aid:

```text
python3 scripts/lint_plain_english.py path/to/document.md
```

## Final check

Before returning the edited document, confirm that links, code, commands, identifiers, facts, headings, lists, and navigation are unchanged unless the user explicitly requested those changes. Check that the rewrite adds no claim, removes no limitation, and does not impose a prose-only reply style on surrounding conversation.

## Runtime metadata

This skill's invocation and display metadata is in [agents/openai.yaml](agents/openai.yaml).
