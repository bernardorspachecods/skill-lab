# Prompt Guidance

Use this reference when the prompt task is complex enough that the compact skill body is not enough.

## Route Before Writing

Classify the prompt by the work it should cause:

| Route | Prompt should emphasize |
| --- | --- |
| Quick answer | concise objective, constraints, output style |
| Software change | inspect first, preserve behavior, verify with tests/build |
| Code review | findings first, severity, file/line evidence |
| App revamp | map current behavior, preserve/change/remove/defer, first safe change |
| Research synthesis | source notes before synthesis, claims/questions separation |
| Long-document analysis | map document, targeted reading, page/section evidence |
| Feature evaluation | user value, evidence, risk, reversibility, recommendation |
| Documentation | audience, source of truth, actionability, maintenance |
| Human decision | options, tradeoffs, recommendation, risk if wrong |

## Context Rules

Good prompts tell the LLM:

- what to read;
- what not to read;
- which source is authoritative;
- whether examples are binding or only shape references;
- whether history is current truth or background.

## Confidence Discipline

For factual work, include:

```text
Separate source-backed facts, inferences, assumptions, unknowns, and human decisions. If the available sources do not support a claim, say so.
```

## Verification

For consequential work, include a verification section:

```text
Verify by:
- [test/source/build/review/check]

If verification cannot be run, say what was not verified and what risk remains.
```

## Ask-Before Rules

Use ask-before rules when the LLM could otherwise make a bad silent decision:

- changing architecture;
- changing public APIs;
- deleting features;
- expanding product scope;
- making irreversible data changes;
- making legal, financial, medical, privacy, or security-sensitive claims;
- using private context not provided.
