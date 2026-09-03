---
name: check-docs
description: Re-check relevant repository documentation mid-task and inspect the smallest relevant code or tests when the claim depends on current behavior, the docs are incomplete or ambiguous, or sources conflict.
---

1. Identify the specific claim, decision, or change to verify, and what would count as evidence.
2. Read the applicable repository guidance and only the relevant authoritative docs.
3. Decide whether the docs are sufficient. Consult the smallest relevant slice of the current code, configuration, or tests when the claim concerns actual behavior, interfaces, paths, or implementation details; when the docs are ambiguous, incomplete, or potentially stale; or when the sources disagree. Do not inspect code merely because this skill was invoked.
4. Compare intended rules from the documentation with evidence from the current repository. Surface conflicts, stale guidance, and gaps explicitly instead of silently choosing one source.
5. Continue only when the conclusion is sufficiently grounded. If the conflict affects a material decision and cannot be resolved from the available evidence, pause and ask for direction.
6. State what documentation and repository evidence was checked, the conclusion, and any unresolved uncertainty.
