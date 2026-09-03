---
name: grill-docs
description: Explore a plan, decision, or idea with critical questions, plausible alternatives, and concrete scenarios, then record the confirmed plan in the repository's existing documentation system. For discussion without a durable plan, use grill.
---

# Stress-test and document a plan

## Start

1. State the objective in one sentence and keep it visible.
2. When a repository is in scope, use its entry points, documentation owners,
   and routing rules before asking for repository facts.
3. Separate exploration from commitment: implement only after the user's
   explicit `go` call.

## Explore

Ask exactly one question per turn. Use this format:

```text
**Q<n> — <short title>**: <one decision question>

Recomendo: <the preferred answer and its main trade-off>
```

After each answer:

- challenge weak assumptions and disagree when there is a grounded reason;
- propose alternatives and concrete scenarios when a meaningful trade-off or
  ambiguity exists;
- keep the scope visible and let the user decide whether a tangent belongs.

Stop exploring small details once material decisions are clear; surface
remaining possibilities without reopening settled decisions.

## Keep scope useful

When an idea is outside the objective:

1. say so clearly;
2. let the user decide whether to include it;
3. if excluded but worth preserving, record it in the repository's designated
   future-ideas space.

## Document the plan

Use the repository's designated planning or decision document as the working
plan when one exists. If there is no suitable owner, keep the plan in the
conversation until it is confirmed, then ask before creating a new durable
document.

During exploration, update the working plan with the objective, scope,
decisions, alternatives, scenarios, and open questions. Keep canonical
documents unchanged and keep alternatives and future ideas separate from the
plan.

When the plan is confirmed and implementation is authorized, update the repository's
canonical owners immediately before implementation. Then review the plan and
repository documents together, resolving contradictions, omissions, stale
wording, and unnecessary duplication.

## Finish

Finish when the objective, decisions, trade-offs, scenarios, and plan are
clear. Present the confirmed plan first, then relevant unchosen possibilities
and future ideas. Wait for the user's explicit `go` call before implementation.
