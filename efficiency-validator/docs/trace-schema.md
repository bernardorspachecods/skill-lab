# Trace Schema

The observer consumes externally collected events from real Codex sessions. It
does not ask the agent to narrate its reasoning and it does not add a locator
tool to baseline runs.

## Primary baseline evidence

The current Codex adapter provides command-level evidence: command text,
aggregated output, exit code, status, completed agent messages, parser issues,
source-line order, and (when a terminal usage event is present) provider-
reported turn token usage. It does not provide authoritative file reads or
physical scans. The command evaluator reports filesystem-level metrics as
unavailable rather than inferring them from shell commands.

The final captured agent message is the last completed `agent_message` item;
the adapter does not claim that this is a protocol-level final-answer marker.

## Run provenance

New captures store the exact explicit `prompt`, its `prompt_hash`, an `oracle`
record with case, evaluator-relative path, content digest, and availability
status, plus structured `controlled_variation` metadata containing its label,
task hash, and prompt hash. `provenance_status` distinguishes complete,
partial, and legacy manifests. Older bundles remain readable as historical
artifacts but do not provide complete provenance for a trustworthy comparison.

The parser also retains every valid JSON protocol event in `raw_events`, even
when the current adapter does not yet interpret its event type. Malformed or
non-JSON input remains a parser issue; it is never silently discarded or
counted as a complete stream.

Each event records:

```json
{
  "run_id": "run-001",
  "case_id": "001-create-task",
  "event_index": 3,
  "operation": "read",
  "paths": ["docs/product/rules.md"],
  "scanned_paths": [],
  "result_count": null,
  "tokens": null
}
```

This structured event format is reserved for a separately instrumented,
authoritative file-level trace. It is not populated by the current
`codex exec --json` parser. The E1 sidecar parser accepts the versioned
`filesystem-trace-1` JSONL form and includes explicit authority and status
fields.

`paths` are files visible in the tool request or result. `scanned_paths` are
files physically inspected by the underlying search operation when the runtime
can expose them. Missing `result_count` and `tokens` values remain missing;
they are not silently converted to zero.

Read observations may additionally carry `offset`, `bytes`, `file_size`,
`line_start`, `line_end`, and `file_line_count`. These fields let the report
distinguish a partial read from a complete read when the producer exposes
them. An event may also declare `content_capture` as `none`, `hash`, or
`full`; `full` is an explicit local-audit mode and preserves the returned
content in the raw sidecar, while the compact report only exposes its hash and
coverage summary. Content is never inferred from an `open` event.

The report adds `filesystem.read_coverage.files`, one entry per observed read
path. Its `coverage_status` is `partial`, `full`, or `indeterminate`; the last
value means that the sensor proved an access but did not expose enough bytes or
line ranges to calculate coverage. `line_coverage` takes precedence over
`byte_coverage` when both are present. This is evidence about bytes or content
returned by the observed reader, not a claim about what the model understood.

The observer keeps these evidence classes distinct:

- command text: requested command metadata;
- aggregated output: returned output, including an optional exact-content
  record in `observability.returned_content`; this proves visibility to the
  agent but does not by itself prove which file produced it;
- executor RPC: a runtime filesystem operation, not proof of a kernel open;
- OS trace: a logical system-call observation, not necessarily a physical disk
  transfer.

The sidecar joins to one capture with `run_id`, `case_id`, and `trace_id`.
Every sidecar event declares an `evidence_kind` (`requested`, `returned`,
`opened`, or `scanned`) so a downstream metric cannot silently count a
requested path as an opened file.
`macos-fs-usage` is the selected host option on macOS. It normally requires
root privileges, so the host starts it as an explicit privileged sidecar and
`scripts/parse_fs_usage.py` filters it to the staged-target prefix. The
read-only collector never silently requests administrator access. `linux-audit`
is the Linux alternative and also has host privilege and performance
implications.

In macOS `fs_usage -w` output, the numeric suffix printed after a process name
is a thread identifier, not a process PID. The sidecar stores it as
`thread_id`; process-tree correlation therefore uses the observed process
names, while real structured/runtime events may still provide a true `pid`.

Automatic capture additionally samples the measured launcher process and its
descendants. When the process-tree sidecar is available, filesystem events can
be correlated by PID instead of being limited to a target path prefix. The
sampling is evidence of observed descendants, not a guarantee that a very
short-lived child between samples was seen; that limitation remains explicit
in the process-tree artifact.

The macOS converter preserves `B=<bytes>` and `O=<offset>` markers from
`fs_usage` when they are present. Those are kernel-observed read dimensions;
they do not contain the bytes themselves. A future process-correlated forensic
producer may combine them with file-size and line-map evidence, while a
structured runtime producer can supply the optional returned content directly.

The structured operations are `search`, `list`, `read`, and `follow_link`. The
schema intentionally records actions, not hidden model reasoning. Its
evaluator only counts a first authoritative path when it appears in a
structured `read` event; it must not be used as a proxy for the command-level
baseline.
