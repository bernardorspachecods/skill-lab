# Natural baseline run protocol

This is the context-lab-specific route. For reusable operational capture
without an oracle, use the [operational protocol](operational-protocol.md).

This protocol defines the boundary for a natural baseline. It is a host-side
condition, not an instruction supplied to the measured agent.

1. Run `stage_target.py` against a clean, committed `context-lab-target`
   checkout. It creates an immutable archive extraction and a staging manifest
   containing the source revision and staged tree hash. The staged workspace
   must contain no evaluator sidecar, findings, or other sibling repositories.
   It intentionally has no `.git` directory; Git metadata is not part of the
   measured target and Git-only commands are therefore environment evidence,
   not repository evidence.
   The host also reserves `.context-lab-tmp` as an ephemeral runtime directory;
   it is excluded from the semantic tree hash and is not target content.
2. Run `prepare_runtime.py` against the staged target. It installs the locked
   target dependencies, including the `test` extra, into a separate runtime and
   writes a runtime manifest associated with the staging manifest.
3. Supply only the task prompt to Codex. Do not add a locator, route checklist,
   narrated-reasoning request, or navigation policy beyond the task itself.
4. Give both manifests to `collect_codex.py`. The collector verifies the
   staged tree before launching the read-only, ephemeral `codex exec --json`
   session from that workspace with the prepared runtime on `PATH`. It derives
   the source revision, runtime revision, Codex version, observer version, and
   evaluator-sidecar revision; callers cannot provide substitute values.
5. Preserve the raw JSONL and the required manifest. The manifest must join the
   repository revision, runtime revision, resolved/requested model, Codex
   version, observer version, launch mode, sandbox, process result, and
   evaluator-sidecar revision. New captures also store the exact explicit
   prompt and hash, oracle path/hash/status, and structured controlled
   variation. A legacy or partial manifest is historical evidence only and
   cannot establish a trustworthy pair by itself.
6. Run `report_codex.py` after the session ends. It parses the raw stream and
   reports command-level evidence. Join the evaluator oracle only
   after the session ends; normalized answer claim adjudication is separate
   from route evidence.

The minimal host-side sequence is:

For a reusable bundle, `capture_run.py` composes the same sequence and refuses
to overwrite a non-empty bundle. It accepts an optional raw filesystem trace
that was collected around the run; it does not self-elevate:

```text
python3 scripts/capture_run.py \
  --source ../context-lab-target \
  --bundle /tmp/context-lab-run-001 \
  --prompt '...the task prompt...' \
  --oracle ../context-lab-evaluator/oracles/001-create-task.json \
  --evaluator-root ../context-lab-evaluator \
  --run-id run-001 \
  --case-id 001-create-task \
  [--filesystem-raw /tmp/context-lab-run-001/fs_usage.log]
```

The explicit raw-trace option is intentionally an input seam: a privileged
host wrapper can collect it, while an ordinary run still produces a valid
bundle with filesystem status `unavailable`.

An externally collected network metadata sidecar can be supplied with
`--network-trace`. It is copied into the bundle as `network.jsonl` and joined
to the report without retaining network payloads or adding its bytes to token
usage.

For an authorized exact-read attempt, add `--exact-read` to
`capture_run.py`. The harness compiles the local macOS interposer into the
bundle, retains the returned-byte sidecar locally, and rejects the bundle if
the target or any descendant bypasses the supported boundary. A hardened or
two-level executable can therefore produce an intentionally invalid exact
run; this is evidence that exact capture was unavailable, not a zero-read
result.

For automatic macOS collection, use the opt-in helper mode. macOS displays
the administrator authorization prompt; the harness never receives or stores
the password. The helper starts before `collect_codex.py`, stops after it
exits, and keeps the raw stream locally for later correlation to the measured
process tree:

```text
python3 scripts/capture_run.py \
  --source ../context-lab-target \
  --bundle /tmp/context-lab-run-001 \
  --prompt '...the task prompt...' \
  --oracle ../context-lab-evaluator/oracles/001-create-task.json \
  --evaluator-root ../context-lab-evaluator \
  --run-id run-001 \
  --case-id 001-create-task \
  --filesystem-auto
```

Automatic mode fails before the measured run if authorization cannot be
established. This prevents a requested filesystem trace from silently turning
into an unavailable or zero-event metric.

The automatic bundle also writes `process-tree.json`, containing the measured
Codex launcher PID and descendant PIDs observed during the run. When that
metadata is available, the converter can retain filesystem events from the
measured process tree even when paths belong to a skill, another repository,
external context, or a dependency/cache. If process sampling is unavailable,
the bundle falls back to explicit path prefixes and reports the narrower scope.

```text
python3 scripts/stage_target.py \
  --source ../context-lab-target \
  --destination /tmp/context-lab-run-001/target \
  --manifest /tmp/context-lab-run-001/staging.json

python3 scripts/prepare_runtime.py \
  --target /tmp/context-lab-run-001/target \
  --staging-manifest /tmp/context-lab-run-001/staging.json \
  --runtime /tmp/context-lab-run-001/runtime \
  --manifest /tmp/context-lab-run-001/runtime.json

python3 scripts/collect_codex.py \
  --repo /tmp/context-lab-run-001/target \
  --prompt '...the task prompt...' \
  --oracle ../context-lab-evaluator/oracles/001-create-task.json \
  --output /tmp/context-lab-run-001/events.jsonl \
  --manifest /tmp/context-lab-run-001/manifest.json \
  --run-id run-001 \
  --case-id 001-create-task \
  --staging-manifest /tmp/context-lab-run-001/staging.json \
  --runtime-manifest /tmp/context-lab-run-001/runtime.json \
  --sidecar-root ../context-lab-evaluator

python3 scripts/report_codex.py \
  --events /tmp/context-lab-run-001/events.jsonl \
  --manifest /tmp/context-lab-run-001/manifest.json \
  --oracle ../context-lab-evaluator/oracles/001-create-task.json \
  --output /tmp/context-lab-run-001/report.json
```

On macOS, an operator may capture the authoritative OS signal in parallel
with the collector. Start the privileged host tracer before the collector,
stop it after the collector exits, and convert only the staged target's
pathname records:

```text
sudo fs_usage -w -F -f pathname -t 900 > /tmp/context-lab-run-001/fs_usage.log

python3 scripts/parse_fs_usage.py \
  --input /tmp/context-lab-run-001/fs_usage.log \
  --output /tmp/context-lab-run-001/filesystem.jsonl \
  --run-id run-001 \
  --case-id 001-create-task \
  --trace-id trace-run-001 \
  --target-prefix /tmp/context-lab-run-001/target
```

Pass the generated `filesystem.jsonl` to `report_codex.py` with
`--filesystem-trace`. The trace is OS-level logical access evidence, not a
claim of physical disk I/O, and the privileged process must be stopped after
the run.

When `fs_usage` exposes `B=<bytes>` and `O=<offset>`, those values are kept in
the sidecar. They support byte-level coverage calculations but do not contain
the file body. Exact text returned by command tools is separately retained in
the report as `observability.returned_content`; it is labelled as tool output,
not automatically as a file read.

The collector's `--cd` option identifies the working repository but is not by
itself a security boundary. The staging manifest is therefore mandatory: the
collector refuses to run against an unstaged, modified, or mismatched target.

Pass `--model` only when the account supports an explicit model name. When it
is omitted, the collector uses the account's configured Codex default and
records `codex-default` in the manifest.
