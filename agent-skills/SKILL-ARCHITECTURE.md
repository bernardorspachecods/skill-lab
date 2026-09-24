# 1. Skill catalog

This document is a human-facing map of the skill catalog as it exists today.
It helps maintainers understand activation, composition, and repeated
principles before a later improvement pass.

| Skill | Current activation status | Current role |
| --- | --- | --- |
| [`chat-start`](skills/chat-start/SKILL.md) | lifecycle; model-selectable | Start-of-chat repository context and working style |
| [`chat-wrap-up`](skills/chat-wrap-up/SKILL.md) | manual-only | Prepare repository context for a seamless next-chat continuation |
| [`check-docs`](skills/check-docs/SKILL.md) | model-selectable | Repository documentation checkpoint before repository-specific work |
| [`code-review`](skills/code-review/SKILL.md) | model-selectable | Two-axis review of a diff against standards and spec |
| [`codebase-design`](skills/codebase-design/SKILL.md) | model-selectable | Vocabulary and design guidance for deep modules and seams |
| [`context-architecture`](skills/context-architecture/SKILL.md) | model-selectable | Organize agent-facing repository context |
| [`domain-modeling`](skills/domain-modeling/SKILL.md) | model-selectable | Sharpen terminology, contexts, and architectural decisions |
| [`evaluate-relevance`](skills/evaluate-relevance/SKILL.md) | draft; model-selectable | Context-led assessment of technology relevance for Bernardo |
| [`git-worktree-cleanup`](skills/git-worktree-cleanup/SKILL.md) | manual-only | Commit task-relevant changes and preserve unrelated work |
| [`grill-stuck`](skills/grill-stuck/SKILL.md) | model-selectable | Re-ground unreliable work and recover from failed approaches |
| [`grill-task`](skills/grill-task/SKILL.md) | model-selectable | Clarify tasks and decisions into actionable plans |
| [`grill`](skills/grill/SKILL.md) | model-selectable | Critically examine an idea, plan, or result without executing it |
| [`new-project-guidelines`](skills/new-project-guidelines/SKILL.md) | model-selectable | Apply simple guidelines when starting a new project |
| [`prompt-design`](skills/prompt-design/SKILL.md) | model-selectable | Create, improve, audit, or structure prompts and briefs |
| [`parallel-task`](skills/parallel-task/SKILL.md) | manual-only | Delegate independent side tasks or review completed work in multiple modes |
| [`prototype`](skills/prototype/SKILL.md) | model-selectable | Build a throwaway prototype to answer a design question |
| [`research`](skills/research/SKILL.md) | manual-only | Conduct rigorous source-first web research |
| [`test-first`](skills/test-first/SKILL.md) | model-selectable | Drive suitable software changes with behavior-first tests |
| [`skill-authoring`](skills/skill-authoring/SKILL.md) | model-selectable | Create and maintain agent skills |
