# Operational run protocol

Use `scripts/operational.py` to capture a real Codex task without an oracle,
privileged tracing or exact-read instrumentation. This is the operator route
for phase 1 of the [archived evaluator plan](../reference/PLAN_operational-evaluator.md). The older
[natural-baseline protocol](run-protocol.md) remains the context-lab adapter.

## Navigation map

| Need | Read |
| --- | --- |
| Run a task or change its context/skills | [Capture](#capture) |
| Find inputs, outputs and event evidence | [Bundle contract](#bundle-contract) |
| Stop a run or recover interrupted evidence | [Lifecycle](#lifecycle) |
| Regenerate a report or record an intervention | [Offline operations](#offline-operations) |
| Understand measured and unavailable fields | [Evidence coverage](#evidence-coverage) |

## Capture

Prerequisites: Python 3.12+, an installed authenticated Codex CLI supporting
`exec --json --ephemeral --ignore-user-config`, and the task's required host
tools. No Python dependencies are needed for this command. Run from the
efficiency-validator directory:

```sh
python3 scripts/operational.py run \
  --source /absolute/path/to/project \
  --bundle /absolute/path/to/experiments/run-001 \
  --prompt-file /absolute/path/to/task.txt \
  --variant baseline \
  --model gpt-6-astra --reasoning low \
  --timeout 300 \
  --check '["python3", "-m", "unittest", "-v"]'
```

Choose an available model and effort appropriate to the experiment; the example
uses the model configured on the acceptance host. Model resolution at the
provider may remain unavailable even with an explicit requested model.
`--check` is optional and repeatable. Each value is a JSON argument array,
executed by the evaluator after the agent exits successfully, outside the
agent's measured task duration. These are operator-selected host commands;
they do not inherit the Codex sandbox. Use checks appropriate for trusted local
projects. Outputs and exit status are retained even when checks fail. Exit code
0 from `run` means agent execution completed; consult `checks.json` or the report
for check outcomes. No checks means unassessed, not passing quality.

Add a context file or a complete skill directory to a second run:

```sh
--overlay CONTEXT.md=/absolute/path/to/context-variant.md
--overlay .agents/skills/example=/absolute/path/to/example-skill
```

Overlays are copied into the retained input and then the isolated workspace.
File overlays may replace files in the copy; directory destinations must be
absent. Relative resource structure within a skill is preserved. These are
configured inputs, not proof the agent used the skill. A supplied variant name
does not modify the prompt. Fresh calls create new sessions and workspaces.

The source is copied including uncommitted/untracked files, excluding named
directories `.git`, `.venv`, `node_modules`, `__pycache__`, `.pytest_cache`.
Exclusions appear in the manifest. Dependencies are not installed automatically;
prepare a source runnable with the available host tools. Git-dependent tasks
need a future Git-aware staging mode and are not supported by this route.
External or absolute symlinks and special files are rejected explicitly rather
than copied through. Bundle and source must be disjoint directories.

The collector preserves host authentication in place and never copies it to
another runtime. It ignores the user CLI config but global instructions/skills,
system policy and host tools may still apply. This limitation is in every
manifest/report. The source, prompt and tool outputs can themselves contain
sensitive information: bundles have a private top-level directory (0700).
No credentials or environment values are added to manifests by the collector.

If an enclosing application sandbox prevents Codex's app-server from starting,
run the collector in an authorized ordinary terminal. This does not require
disabling the Codex sandbox: `workspace-write` remains the default and
`read-only` is supported. `danger-full-access` is not offered by this command.

## Bundle contract

`operational-1` is separate from the older context-lab bundle format. The
`scripts/compare_operational.py` CLI consumes two completed operational bundles
and produces an exploratory paired report. It blocks comparisons when the
starting source, prompt, requested model, reasoning effort, sandbox, collection
or evaluator quality gate differs or is incomplete. One passing pair is a case
observation, not evidence of a general improvement. See
[Analysis acceptance](analysis-acceptance.md) for a reproduced command and its
limits.

| Artifact | Meaning |
| --- | --- |
| `manifest.json` | Run/configuration, input inventories and hashes, requested checks, versions, lifecycle, environment limits, artifact hashes |
| `inputs/prompt.txt`, `inputs/target/` | Retained prompt and actual starting files after overlays |
| `events.jsonl`, `events.stderr` | Original stdout bytes and separate diagnostics; unknown events are retained |
| `events.arrivals.jsonl` | Line number and host monotonic receipt time, including unterminated final lines |
| `events.process.json` | Launched PID and start timestamp for recovery diagnostics |
| `outputs/target/`, `changes.json`, `changes.patch` | Agent work products before evaluator checks; binary contents in output snapshot, text diff for review |
| `checks.json`, `check-N.*` | Evaluator commands, outcomes, stdout, stderr and receipt times; `.jsonl` stdout extension does not imply JSON check output |
| `annotations.jsonl` | Explicit operator observations; separate from immutable runtime evidence |
| `derived/report.json`, `derived/report.md` | Regenerable normalized evidence and human-readable report |

Input and output inventories are checked when reporting, including added or
missing files. Hashes detect accidental changes; bundles are not signed or
tamper-proof against someone rewriting both manifest and evidence. Partial
captures can lack some artifacts. The temporary workspace path is recorded and
retained for diagnosis; the bundle does not depend on it for reporting. Remove
that specific disposable workspace manually when no longer needed. Deleting a
bundle removes its retained evidence; the original project is unchanged.

## Lifecycle

`--timeout` limits agent task wall time, excluding setup, snapshot/report work
and subsequent checks. Each evaluator check has the same separate timeout.
Process-group termination gets up to three seconds to finish; descendants that
escape the group are not certified as stopped. Cleanup status says so. Token
and money budgets are explicitly unavailable; no such flags are accepted.

From another terminal:

```sh
python3 scripts/operational.py cancel /absolute/path/to/experiments/run-001
```

SIGINT/SIGTERM during execution also request cancellation. Received streams are
written incrementally and the collector finalizes partial evidence. After a
collector crash or SIGKILL, with the collector and task processes stopped:

```sh
python3 scripts/operational.py recover /absolute/path/to/experiments/run-001
```

Recovery refuses a known live PID; it does not kill or relaunch anything.
`--confirm-stopped` is only for early captures without collector PID metadata,
after independently checking that their processes stopped. Recovery marks the
run interrupted and preserves available workspace output; end time, final
usage and cleanup cannot be reconstructed. Never interpret interrupted runs
as successful zero-cost runs. An existing bundle is never overwritten.

## Offline operations

```sh
python3 scripts/operational.py report /absolute/path/to/experiments/run-001
python3 scripts/operational.py report /absolute/path/to/experiments/run-001 \
  --output /absolute/path/to/regenerated-report
python3 scripts/operational.py annotate /absolute/path/to/experiments/run-001 \
  --kind hint --text 'I supplied a file location during the task' \
  --start 12.0 --end 18.0
```

Reporting requires only the bundle, no network, CLI invocation, original source
or temporary workspace. Derived files can be regenerated; retained evidence is
unchanged. Unsupported bundle schemas and integrity failures are rejected.
Annotations record kind, text and insertion timestamp. Optional wait intervals
are offsets from task start; overlapping intervals are unioned. They record
operator testimony, not an interaction sent to the measured agent. Exec mode
has no live steering/approval UI in this implementation, so automatic human
intervention coverage and total wait time are unavailable.

## Evidence coverage

| Field | Source and practical limit |
| --- | --- |
| Configuration | Copied inputs and manifest; global context and provider configuration may be unresolved |
| Task/setup/total time | Collector monotonic clock; total also includes snapshot and evaluator work |
| Tool timing | Host receipt of start/end events; exact execution duration remains unavailable, including when events arrive together |
| Commands/searches/reads | Emitted tool inputs and returned text; no inference of complete file reads from shell syntax |
| Token totals | `turn.completed.usage`; input already includes cached input, output includes reasoning; omitted fields stay null |
| Partial usage | Completed-turn observations only; incomplete-run coverage explicitly marked |
| Returned output bytes | UTF-8 length of exposed command text; not filesystem bytes or model-input tokens |
| Repeated outputs | Identical nonempty command outputs; not a claim of irrelevant reading |
| Changes/tests | Before/after retained files, agent command events and separate evaluator command results |
| Human involvement | Explicit annotations only; zero annotations is not proof of zero interventions |
| Truncation/unknown events | Raw payload retained; upstream truncation may be unknown; parser issues are visible |

Implementation: [collector](../src/efficiency_validator/operational.py),
[offline report](../src/efficiency_validator/operational_report.py),
[CLI](../scripts/operational.py). The existing Codex parser is reused for event
and lifecycle validation; the oracle-dependent legacy reporting contract is
not imposed on this operational format.

The CLI event/options boundary follows the
[official non-interactive documentation](https://learn.chatgpt.com/docs/non-interactive-mode)
and was demonstrated with installed Codex CLI 0.157.0. Real acceptance artifacts
and their exact coverage are recorded in the
[operational acceptance record](operational-acceptance.md).
