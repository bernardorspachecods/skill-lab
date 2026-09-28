---
plan_id: R6
kind: subplan
parent: R0
phase: 6
status: in_progress
depends_on: [R1, R2, R4, R5]
consumers: [R7, efficiency-validator/docs]
---

# R6 — Codex CLI boundary and alternatives

> Archived on 2026-09-26; superseded by [the operational evaluator plan](PLAN_operational-evaluator.md).
> Status fields below preserve historical claims, not verified completion.

## Objective

Select an evidence boundary that can observe exact returned bytes from the
real Codex CLI and its complete local executor process tree.

## Scope

- Current installed `codex exec` binary and launch environment.
- A rebuilt or ad-hoc-signed Codex CLI where legally and operationally viable.
- A controlled self-hosted executor/runtime.
- Privileged OS tracing only if it exposes returned bytes, not just paths.
- Security, credentials, sandbox semantics, and fidelity to normal Codex runs.
- Credential isolation for any VM or Linux alternative: host Codex OAuth state
  must never be mounted into a different Codex binary or runtime.

## Output

An architecture decision record naming the chosen boundary, proof command,
rejected alternatives, and the exact failure signal for each unsupported route.

Current execution record: the candidate probes and their failure evidence are
recorded in [the boundary decision record](../docs/codex-cli-exact-read-boundary.md).
No boundary has been selected, so R6 remains in progress.

## Sequence

1. **R6-S1 — Inventory the real CLI boundary**
   - **Action:** Record binary provenance, signing/hardening, child launch
     behavior, tool execution path, and normal `codex exec --json` semantics.
   - **Output:** Reproducible boundary inventory.
   - **Exit check:** Every process that can read local files has an identified
     observation point or an explicit unknown. **Result:** the installed CLI
     and its protected shell/tool readers were inventoried; the shell/tool
     observation point remains unknown.
2. **R6-S2 — Test candidate authorities**
   - **Action:** Run minimal real CLI probes through interposition, rebuilt
     runtime, self-hosted executor, and privileged OS tracing where available.
   - **Output:** Candidate evidence matrix with returned-byte proof, not just
     open/path proof.
   - **Exit check:** At least one candidate observes a real Codex read or all
     candidates are rejected with inspectable technical evidence. **Result:**
     the installed hardened CLI, temporary re-signed package, protected shell
     and tool copies, managed sandbox, source-build route, and Colima/Linux
     route did not produce a valid real-CLI returned-byte ledger.
3. **R6-S3 — Choose without weakening validity**
   - **Action:** Select the smallest boundary that preserves normal CLI
     behavior and satisfies the exact-read contract.
   - **Output:** Decision record consumed by R7.
   - **Exit check:** The choice cannot declare success from `fs_usage`, paths,
     command output, or fixtures alone. **Result:** no boundary was selected;
     fixture-only and lifecycle-only evidence remain insufficient.

The Colima/Linux attempt also caused an operational authentication incident:
an alternative Linux Codex binary ran inside the VM with access to the Mac
authentication state (`hostmount=yes`, `auth=yes`). The Mac Codex OAuth token
was subsequently revoked, producing `401 Unauthorized`, `token_revoked`,
`Incorrect API key`, and websocket failures for new chats. Logout, a complete
app close, reopening, and signing in again renewed the token and restored
authentication. This is recorded as a boundary-isolation failure, not as
exact-read evidence; future attempts must use isolated credentials and must
not reuse the host authentication state.

## Completion criteria

- The chosen boundary reaches the real Codex CLI or the plan records a genuine
  external blocker and remains incomplete.
- Normal prompt, tool, sandbox, and process-tree semantics are preserved.
- The authority for returned bytes is named and independently testable.
