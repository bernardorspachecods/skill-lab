---
name: writing-for-agents
description: Design concise, reliable instructions that agents can select, understand, execute, and verify. Use when creating or editing skills, AGENTS.md, READ.md, CLAUDE.md, or other durable instructions for agents.
---

# Write for agents

Treat the document as a behavior contract, not as prose. Its job is to help the agent make better decisions with the smallest sufficient amount of context and process.

When creating or editing an agent-facing document:

1. **Route the task.** Identify the document type, audience, scope, and invocation mode. Inspect the existing repository guidance and related documents before introducing new rules.
2. **Find authority.** Prefer, in order: current user instructions; current code, tests, files, logs, or source material; official or primary documentation; decision records; recent notes; older notes; general model knowledge. Surface meaningful conflicts instead of silently merging them.
3. **Define the contract.** Make the objective, success condition, relevant context, rules, preferences, examples, human decision points, verification method, and expected output clear. Include only the parts that matter for this document.
4. **Choose the smallest sufficient workflow.** Use a direct instruction for simple work. Add routing, planning, reflection, delegation, or extra context only when it materially improves reliability. Give each meaningful step a checkable completion condition and set a stop condition for iterative work.
5. **Write for execution.** Put actions in the order they should happen. State positive target behavior, preserve hard guardrails where needed, and use familiar terms. Ask the human only about decisions that are high-risk, ambiguous, private-context dependent, irreversible, or not safely discoverable.
6. **Manage context deliberately.** Read indexes, maps, and outlines before large sources; retrieve targeted details just in time; name what is relevant and what is not. Put branch-specific detail behind clear pointers and keep the entrypoint focused on the workflow shared by all branches.
7. **Protect durable knowledge.** Keep one canonical source of truth. Update documentation only when a fact, decision, convention, command, or pitfall will change future behavior. Link to raw material instead of duplicating it, and keep assumptions, open questions, and temporary notes distinct from conclusions.
8. **Verify the result.** Check frontmatter, names, links, referenced files, runtime paths, and repository conventions. For repeated workflows, test with realistic examples and known failure modes. Report what was checked, what it proves, and what remains uncertain.

Before finishing, remove duplicated guidance, stale claims, generic advice, unnecessary process, and examples whose accidental details could be mistaken for requirements. The final document should make it easy to tell when to act, when to ask, what to read, what to ignore, and when the work is complete.

When the document is a skill, read [SKILL-MECHANICS.md](SKILL-MECHANICS.md) for invocation, frontmatter, and supporting-resource decisions.
