---
name: skill-authoring
description: Create and maintain agent skills.
---

#

# Skill mechanics

### Invocation

- **Model-invoked:** omit `disable-model-invocation`. The description is a context pointer that is always available for automatic selection, and the user can still invoke the skill by name.
- **User-invoked:** set `policy.allowimplicitinvocation: false` in `agents/openai.yaml`. Use this when the workflow should run only when the human explicitly asks for it.

Choose model invocation only when the agent needs to select the skill autonomously or another skill needs to reach it. Keep automatic skills' descriptions narrow enough to avoid competing with similar skills.

Keep invocation policy in `agents/openai.yaml`; do not add unsupported invocation fields to `SKILL.md` frontmatter.

### Frontmatter and description

Every skill needs a lowercase hyphen-case `name` matching its directory and a concise `description`. The description should state:

- the capability the skill provides;
- the situations that should trigger it;
- an important boundary when similar tasks should not trigger it.

Keep routing information in the description and execution instructions in the body. Do not use the description as a miniature manual.

### Body and resources

The body should contain the shared workflow, decision rules, real constraints, and completion criteria. Put substantial branch-specific guidance in `references/` and link it with a clear condition for reading it. Add scripts or assets only when they provide concrete reusable value.

Use examples to clarify behavior, output shape, or failure modes. Keep them canonical and label examples as examples; do not let their accidental details become requirements.

### Splitting and routing

Split a skill only when a branch has a genuinely different invocation, workflow, or context requirement. A router skill is useful when many manual skills create too much cognitive load, but it can recommend other skills only when they remain user-invoked.

### Final checks

Before publishing, verify that:

- frontmatter parses and the name matches the directory;
- the description is specific and routes the intended cases;
- every relative reference exists;
- invocation policy matches the intended human/agent ownership;
- the skill does not duplicate a stronger source of truth or impose process on unrelated work.
