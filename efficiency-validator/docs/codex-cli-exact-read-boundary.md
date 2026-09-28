# Codex CLI exact-read boundary decision

Status: unresolved historical investigation — the exact-read acceptance criterion is not met.

The [operational evaluator plan](../reference/PLAN_operational-evaluator.md) supersedes the
[archived exact-read plan](../reference/PLAN_exact-read-audit.md).
The findings below remain evidence about that optional audit boundary, not a
prerequisite for operational collection.

## Evidence date

2026-09-25.

## Target

- Installed command: `codex` -> `codex-cli 0.156.1`.
- Installed binary: `/opt/homebrew/Caskroom/codex/0.156.1/bin/codex`.
- The installed binary is a signed macOS arm64 executable with hardened runtime.
- The official source revision inspected for an alternative boundary was
  `58670eeac4b0bdb9fcb86929d8631c14aee0d9f6`.

## Observed results

1. Injecting the exact-read DYLD library into the installed CLI produces no
   `exact-read.trace.started` record for `codex --version` or a real task.
   This is expected for the hardened signed binary and is not exact evidence.
2. A complete temporary copy of the CLI package, re-signed only in `/private/tmp`,
   does load the interposer. It emitted lifecycle records for `codex` and
   `codex-code-mode-host`.
3. A real read-only `codex exec` task ran successfully outside the managed
   sandbox and emitted normal JSONL events and token usage. Its exact sidecar
   still contained only process lifecycle records: no returned-byte reads.
4. The task's shell commands run through macOS protected `/bin/zsh`; the
   DYLD variables do not reach an instrumentable shell/reader. `--no-daemon`
   and `shell_environment_policy.inherit=all` did not change this.
5. Running the same real CLI inside the managed sandbox fails earlier with
   `failed to initialize in-process app-server client: Operation not permitted`.
6. The source-build route was attempted but exhausted the disk while compiling
   the official workspace. Rust/LLVM and all temporary build artefacts were
   removed afterwards.
7. The existing Colima VM was started to evaluate a Linux route, but Docker
   provisioning failed at `containerd.service`; no Linux executor run was
   claimed.
8. The installed package also contains a Codex-managed `zsh` and `rg`. Copies
   of both were made only in `/private/tmp` and ad-hoc signed for a direct
   interposition probe. Neither copy emitted an exact-read lifecycle or access
   record when reading `CONTEXT.md`; this does not provide a viable boundary.

## Decision

No boundary is selected yet. `fs_usage`, command output, paths, lifecycle-only
records, and controlled fixtures remain auxiliary evidence and cannot promote a
real Codex run to exact-read valid.

The next acceptable boundary must either:

- run a Linux Codex CLI/executor with an `LD_PRELOAD` reader that reaches every
  local-file reader in the task; or
- use a source/in-process executor instrumentation point that records returned
  bytes and all descendant readers while preserving task semantics.

At archival, neither route had produced a valid real-CLI ledger and paired run;
R7–R10 remained unstarted and the exact-read objective was incomplete.
