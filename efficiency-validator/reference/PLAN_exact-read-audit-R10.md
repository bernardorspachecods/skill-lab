---
plan_id: R10
kind: subplan
parent: R0
phase: 10
status: not_started
depends_on: [R9]
consumers: [efficiency-validator/docs, context-lab, future skill evaluations]
---

# R10 — Operational hardening and acceptance

> Archived on 2026-09-26; superseded by [the operational evaluator plan](PLAN_operational-evaluator.md).
> Status fields below preserve historical claims, not verified completion.

## Objective

Make real Codex CLI exact-read capture repeatable, safe, and impossible to
declare complete from fixture-only evidence.

## Scope

- Permissions, signing/runtime prerequisites, overhead, bundle size, and
  sensitive content.
- Fresh-operator protocol, diagnostics, cleanup, and reproducibility.
- Acceptance tests against the real Codex CLI.
- Plan status and closure evidence.

## Output

The final real-CLI operator protocol, limitation register, acceptance bundle,
and a plan closure packet.

## Sequence

1. **R10-S1 — Harden the route**
   - **Action:** Add preflight checks, clear failure diagnostics, and safe
     retention/cleanup rules.
   - **Output:** Operator-ready capture command.
   - **Exit check:** Unsupported hosts fail before claiming exact evidence.
2. **R10-S2 — Run acceptance from a clean state**
   - **Action:** Repeat the real CLI valid pair and invalidation probes without
     relying on prior bundles or fixture-only shortcuts.
   - **Output:** Clean acceptance evidence.
   - **Exit check:** Real valid pair passes; every invalid probe is blocked.
3. **R10-S3 — Close only on the real criterion**
   - **Action:** Audit code, docs, tests, and reports against this plan.
   - **Output:** Closure report and status update.
   - **Exit check:** The plan remains `in_progress` or `blocked` unless a real
     Codex CLI valid exact-read pair exists.

## Completion criteria

- A fresh operator can obtain a valid exact-read run from real Codex CLI.
- Limitations are explicit and do not masquerade as success.
- The regression suite and plan validator pass.
