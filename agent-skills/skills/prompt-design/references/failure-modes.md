# Prompt Failure Modes

Use this reference when auditing or improving a weak prompt.

## Vague Objective

Bad:

```text
Make this better.
```

Better:

```text
Improve the onboarding copy for first-time users. Preserve the existing feature scope. Return three options with tradeoffs.
```

## Context Hoarding

Bad:

```text
Use all the docs and all previous conversations.
```

Better:

```text
First classify the task. Read only the current product brief, relevant source files, and decision records that affect this change. Ignore stale brainstorming unless it is explicitly referenced.
```

## Missing Verification

Bad:

```text
Implement the change and tell me it works.
```

Better:

```text
After implementation, run the relevant test/build command. If unavailable, explain what was checked manually and what remains unverified.
```

## Silent Scope Change

Bad:

```text
Redesign the checkout.
```

Better:

```text
Map the current checkout flow first. Preserve payment behavior and analytics events. Ask before changing data collection, payment logic, or product scope.
```

## Research Overreach

Bad:

```text
Use this source to prove the conclusion.
```

Better:

```text
Extract what the source actually supports, what it does not support, and what additional evidence would be needed before making the conclusion.
```
