# Codex Event Adapter

The local Codex runtime can emit JSONL with `codex exec --json`. The observer
keeps completed `command_execution` and `agent_message` items and ignores
structural thread and turn events. `parse_codex_stream` also quarantines
non-JSON diagnostics, malformed records, and missing required fields as parser
issues instead of treating the stream as complete.

This adapter is intentionally conservative. A command such as `rg` exposes its
command text and aggregated output, but not necessarily every file inspected by
the underlying process. The adapter therefore does not claim filesystem-level
precision. Such precision requires a separate runtime or OS audit signal.

## Token usage

The pinned local runtime (`codex-cli 0.156.1`) emits a terminal
`{"type":"turn.completed","usage":...}` record in `codex exec --json`.
The observer records the five provider-reported fields:

- `input_tokens`;
- `cached_input_tokens`;
- `cache_write_input_tokens` (defaults to `0` for older compatible payloads);
- `output_tokens`;
- `reasoning_output_tokens`.

`total_tokens` is derived as `input_tokens + output_tokens`. Cached and
cache-write values are dimensions of input usage and are not added again. A
turn is token-complete only when it has a valid terminal `turn.completed` usage
record. Failed, truncated, malformed, or usage-less turns remain respectively
`failed`, `incomplete`, or parser-invalid and are never reported as complete.
Each usage record retains the JSONL line index, turn ordinal, and source name
`codex-exec-json`.

The official Codex event definitions describe the same usage fields and the
TypeScript SDK returns usage on a completed turn. These sources define the
wire shape; the local pinned capture is the compatibility evidence for this
harness.

## Filesystem authority boundary

The command event's `command` is requested command metadata. Its
`aggregated_output` is returned output and is preserved as
`observability.returned_content` with a byte count and content hash. That
proves what was visible to the agent, but neither field proves that a
particular file was opened, read, or scanned. The observer therefore reports
filesystem status as `unavailable` unless `report_codex.py` receives an
independent JSONL filesystem sidecar via `--filesystem-trace`.

The sidecar schema is `filesystem-trace-1`. It carries a run/case/trace key,
source, authority, status, process identity, timestamp, operation, and path.
Each access record also declares `evidence_kind`: `requested`, `returned`,
`opened`, or `scanned`.
Read records can additionally carry byte offsets/counts, file size, line
ranges, and an explicit `content_capture` mode. This is what allows a report to
say “10 of 1000 lines” instead of merely “the file was opened”. A `full`
content capture is opt-in local audit evidence; it is retained in the raw
sidecar and summarized by hash/coverage in the report. An `open` or `stat`
event alone never proves that the file body reached the agent.
Supported source declarations are `macos-fs-usage`, `linux-audit`,
`exec-server-rpc`, and `structured-read`. `macos-fs-usage` and `linux-audit`
are OS-level logical access observations; `exec-server-rpc` is an executor RPC
observation and does not claim a kernel-level open; `structured-read` is a
runtime-provided structured read event. Path requests, returned paths, opened
paths, and scanned paths must remain separate in downstream analysis.

Missing, denied, partial, malformed, and truncated traces have distinct
statuses. A sidecar with a mismatched run or case is retained as `partial` and
cannot silently attach to another run.

On macOS, `scripts/parse_fs_usage.py` converts a privileged
`fs_usage -w -F -f pathname` capture into this sidecar. `-F` keeps the front
of long pathnames so category classification does not receive a truncated
prefix. It filters the
system-wide stream to the immutable staged-target prefix, preserves the
kernel-observed operation and process identity, and labels only `open*`
operations as `opened`; `stat`, `read`, `getattrlist`, and similar operations
remain `requested` observations. The conversion is explicit: the normal
read-only collector does not silently request administrator access.
The numeric suffix in wide `fs_usage` output is a thread identifier, not a
process PID; process-tree filtering uses the sampled process names.

The first direct Codex invocation worked from the host terminal, while a
repo-local Python subprocess could not initialise the same app-server client
under the current permissions. `collect_codex.py` is therefore a host-runtime
collector: it verifies an immutable staged target, records a raw stream plus a
required run manifest, refuses to overwrite an existing capture, and records
timeout/process status. The collector injects a separately prepared locked
runtime and an ephemeral workspace temp directory, while the measured target
remains free of dependency installations. The nested subprocess path remains
unsupported until the runtime integration is solved.

The read-only Codex sandbox can still reject tools that require temporary files
or Git metadata. Those are host/workspace limitations and remain visible as
command failures; they must not be interpreted as documentation failures.

The manifest must pin the run id, case, repository revision, runtime revision,
the requested or configured-default model, Codex version, observer version,
launch mode, sandbox, completion status, and evaluator-sidecar revision. A successful process exit is not by itself proof
that every event was captured or that a file-level trace exists.
`report_codex.py` keeps parser issues explicit and reports command-level
evidence separately from claim coverage.

The versioned manifest additions are `observability_schema`,
`token_usage_source`, `filesystem_trace_source`, and `network_trace_source`.
Old manifests remain
readable and are labelled `legacy-command-only` / `not-captured` when those
fields are absent.
