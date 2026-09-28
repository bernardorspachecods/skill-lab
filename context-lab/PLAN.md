# Context Lab Plan

Status: Natural baseline corpus complete; first architecture candidate frozen for comparison; ready for architecture comparison and refinement

## Navigation map

| If you need... | See |
| --- | --- |
| Objective and boundary | [Objective](#objective), [Scope](#scope) |
| Workstreams and phase order | [Workstreams](#workstreams), [Phases](#phases) |
| Measurement rules | [Measurement principles](#measurement-principles) |
| Completion criteria | [Initial success criteria](#initial-success-criteria) |
| Settled choices and remaining questions | [Material decisions](#material-decisions), [Open decisions](#open-decisions) |
| Review efficiency validator hardening | [Validator reference plans](../efficiency-validator/reference/) |

## Objective

Develop and improve a philosophy for agent-facing context architecture: how a
repository should store, name, connect, and expose information so an LLM can
find the right evidence for realistic engineering tasks.

The lab uses an isolated, reproducible synthetic repository as a controlled
testbed. It must let us distinguish:

1. the quality of a context architecture and its information boundaries;
2. the agent's natural ability to navigate a repository built with that
   architecture; and
3. later navigation interventions that may influence the agent independently
   of the repository's intrinsic architecture.

The first priority is architecture research: establish a candidate, observe
where it succeeds or fails, compare alternatives, and refine the principles.
Navigation interventions are a separate, later workstream and must not be used
to hide weaknesses in the repository architecture.

## Desired outcome

The target repository will contain a small but realistic synthetic project and
an explicit first candidate for its context architecture. The harness will
contain manually authored evaluation tasks and evaluator-only ground truth,
while the sibling efficiency validator produces reproducible traces from
natural agent runs.
The lab will compare architectural alternatives and use the evidence to
refine the candidate into more useful principles. File-level retrieval metrics
require a separate authoritative runtime signal and must not be inferred from
shell commands.

The canonical repository is an experimental candidate, not an assertion that
one structure is universally perfect. Controlled degraded variants are useful
as diagnostic ablations, but the main comparison is between coherent
architectural alternatives and improvements.

## Initial architecture hypotheses

These are provisional claims to test, not rules already validated by the lab:

- **H1 — Task-intent routing:** a concise root map that routes a request to its
  first area of investigation reduces irrelevant exploration and authority
  mistakes.
- **H2 — Local ownership maps:** context maps at genuine ownership or
  documentation boundaries reduce the need to read unrelated material while
  preserving discoverability.
- **H3 — Layered authority:** separating product intent, architecture contracts,
  current implementation, and tests helps the agent distinguish intended from
  implemented behaviour.
- **H4 — Explicit seams:** documenting ownership boundaries and links between
  adapters, core rules, and storage helps the agent trace cross-area behaviour
  without treating implementation details as product rules.
- **H5 — Durable versus temporary context:** keeping repository guidance,
  experiment control, evaluator ground truth, and run outputs in distinct
  owners reduces contamination and stale-context errors.

Each comparison should identify which hypothesis it probes, what was held
constant, and what evidence would count against it.

## Scope

### In scope

- An isolated agent-facing target repository named `context-lab-target`.
- A separate harness repository named `context-lab`.
- A small Python monorepo built around a project and task-management product.
- FastAPI, SQLite, pytest, and a simple background worker.
- Agent-facing context maps, task routers, ownership boundaries, and links in
  the target repository.
- Product, architecture, operations, and decision documentation in the target
  repository.
- A small, high-quality set of manually authored navigation task prompts.
- Evaluator-only ground truth stored in a sibling sidecar outside the agent
  repository.
- A passive observation model and an initial trace schema.
- Baseline runs and documented findings.
- Comparative context-architecture candidates and refinement findings.
- Later controlled documentation defects as diagnostic ablations.

### Explicitly out of scope for the first baseline

- Forcing the agent to use a locator.
- Changing the agent's prompt or navigation policy.
- Treating the agent's self-reported steps as ground truth.
- Automatically generating the initial task corpus.
- Treating the first architecture candidate as the final or universally best
  structure.
- Optimising the repository for one model before observing natural behaviour.
- Testing `chat-start`, locators, or other navigation mechanisms before the
  architecture comparison and refinement cycle is complete.
- Claiming that results generalise to every repository or every LLM.

## Workstreams

### A. Context-architecture research

This is the primary workstream. It produces the candidate repository
architecture, task corpus, comparative variants, and evidence about which
information boundaries and navigation structures help or fail.

### B. Passive measurement

This workstream supplies experiment control and the reproducible runtime
boundary needed to compare architecture candidates without prescribing a route
to the measured agent. Reusable capture, scoring, and reporting belong to the
separate `efficiency-validator` project.

### C. Navigation interventions

This is deferred until the architecture has been compared and refined. It may
later contain `chat-start` adaptations, locators, navigation protocols, or
enforced tool interfaces. Its results must be reported separately from the
architecture research.

## Phases

### Phase 0 — Plan and decisions

- Maintain this plan as the canonical project plan.
- Record material decisions and rejected alternatives.
- Keep provisional parallel-task handoffs and findings outside canonical docs.
- State the architecture hypotheses, comparison variables, outcome measures,
  and boundaries between repository effects and navigation interventions.

Completion: the research question, architecture candidate, measurement
boundary, success criteria, and open decisions are explicit.

### Phase 1 — Canonical repository foundation

- Add the root `CONTEXT.md` and only the relevant local context maps.
- Add repository-specific `AGENTS.md` rules only where needed.
- Build the small monorepo and keep the application executable locally using
  the baseline layout below.
- Add product, architecture, operations, and decision documents.
- Validate links, routers, maps, and context coverage.

Completion: the first architecture candidate is coherent, runnable,
navigable, auditable, and explicit enough to compare against alternatives.

#### Target repository layout

```text
context-lab-target/
├── apps/           HTTP and background adapters
├── packages/       core rules and storage adapters
└── docs/           product, architecture, operations, and decisions

context-lab/
├── evaluation/     manual prompts and later variants
└── docs/decisions/ experiment-level decisions
```

The intended seams are deliberately small:

- `apps/api` and `apps/worker` call the use-case interface in `packages/core`;
- `packages/core` depends on storage interfaces, not SQLite details;
- `packages/storage` provides the SQLite adapter and an in-memory adapter for
  tests;
- The efficiency validator observes the runtime from outside the target and
  never becomes a navigation dependency of the measured agent. The harness
  owns the experiment inputs and invokes that external tool.

The implementation and tests now confirm that these boundaries have useful
depth. This is the baseline layout for the hardening and natural-run stages;
future restructuring must create a new pinned repository revision.

### Phase 2 — Evaluation cases

- Write a small manual corpus of realistic tasks.
- Define expected sources, authoritative sources, answer criteria, and useful
  cost bounds for each task.
- Include tasks that stay within one ownership boundary and tasks that cross
  multiple boundaries.

Completion: each case has a human-reviewed ground truth, a clear failure
interpretation, and a reason it probes the architecture rather than merely a
single implementation detail.

### Phase 3 — Passive observation

- Define the observable event boundary before implementing collection.
- Observe real Codex sessions at the strongest available runtime boundary,
  recording normal tool requests and returned repository artefacts without
  adding a new navigation tool to the agent.
- Distinguish requested/read files from files physically scanned when the
  runtime can expose both.
- Generate reports from traces, never from agent self-report.
- Run the task corpus naturally against the first architecture candidate before
  adding navigation guidance.

Completion: at least one natural run produces a trace and a reproducible
command-level report with a provenance manifest and known observability limits.
The initial candidate has a complete natural corpus, and file-level metrics
remain unavailable unless a separate authoritative signal is joined.

### Baseline hardening gate

Before a state is used as a comparison baseline:

- product documents label implemented versus intended behaviour;
- implementation paths, tests, tasks, and sidecar oracles agree;
- required answer claims and disallowed overclaims are explicit;
- the efficiency validator preserves malformed/diagnostic input as issues and writes a
  provenance manifest;
- the host protocol stages a clean committed target, verifies its content hash,
  and refuses unstaged or overwritten captures;
- the host protocol prepares a locked dependency runtime outside the target,
  injects it into the measured process, and records its revision;
- the report is generated by a deterministic CLI from the raw stream,
  manifest, and external oracle;
- command-level and file-level evidence are reported separately;
- the context validator and full test suite pass; and
- the repository revision, task hash, runtime, validator, and sidecar revision
  are pinned together.

Current gate result: the documentation, task/oracle contracts, and validator
boundaries have been corrected. Both context validators report no findings;
the harness passes 15 tests and the target passes 10 tests, with one existing
FastAPI/httpx deprecation warning in the target suite. The prior plan records
the four-case natural post-split corpus under `runs/run-009/`, `runs/run-019/`,
`runs/run-020/`, and `runs/run-021/`; none of these directories is present in
the current checkout. Restore or link the bundles before relying on that corpus
for an auditable architecture comparison.

#### Current runtime evidence

The local Codex runtime supports `codex exec --json` in a read-only,
ephemeral session. Its JSONL includes completed `command_execution` items with
the command, aggregated output, exit code, and status, plus completed
`agent_message` items. The efficiency validator has a parser for these events.

These events do not guarantee filesystem-level visibility into every file a
shell command inspected. The current boundary therefore supports reliable
command/action traces, while exact physical scan counts remain an open runtime
question rather than an inferred metric.

The first direct Codex run completed the create-task case in a read-only
session against the original combined checkout. That trace is historical and
is not a target-repository baseline. A repo-local Python subprocess could not reproduce the same app-server
initialisation because of runtime permissions. This suggests that faithful
collection may need to live in the host/runtime launcher, while this repository
owns the event schema and evaluator.

The post-split staging and runtime paths succeed without installing dependencies
into the target. The complete `run-009` capture uses target revision `6d7173b`,
runtime revision `sha256:713dd33b`, validator adapter version `0.5.0`, Codex CLI
`0.156.1`, and the configured Codex default model. Its report has a complete
parser stream with 45 observed commands and 5 agent messages. Two commands
failed for known host/workspace reasons: pytest's temporary capture file is
blocked by the read-only sandbox, and the staged target intentionally has no
`.git` for `git status`. File-level physical scan metrics remain unavailable.

#### First architecture candidate freeze

The natural corpus for the first architecture candidate is complete. The
candidate is frozen at target revision
`6d7173b67eaa825d0601768818d7d4e88aa3e2a2` (`6d7173b`) for comparison. This
freeze is an experimental anchor, not a quality verdict or a claim that the
architecture is optimal. The four manual cases are preserved as
`runs/run-009/`, `runs/run-019/`,
`runs/run-020/`, and `runs/run-021/`, respectively. All four manifests pin the
same target revision, runtime revision
`sha256:713dd33b065e524a3ad2a4e551180627736c00457230f34331329bbe32bbe442`,
validator adapter `0.5.0`, Codex CLI `0.156.1`, and evaluator sidecar revision
`sha256:bb27acbfd29369eea114a1664d842f80249c4ec73405d0aa08a37f0abc0132fb`.

The captures are complete with zero parser issues. They contain 121 observed
commands and 16 agent messages in total; case 001 has two known host/workspace
command failures, while cases 002–004 have none. All reports keep file-level
metrics unavailable. The original `report.json` files retain the unjoined
`0.0` claim-coverage state because no normalized claim adjudication was
supplied to those first reports; that value is not a finding that the final
answers contained none of the required claims. The separately generated
`report-adjudicated.json` files record the manual post-run join: all four
cases cover 100% of their required claims, with no oracle disallowed claim
identified in answer review.

This freeze applies only to the first natural candidate. No locator,
navigation protocol, prompt change, or architecture change may be introduced
into these runs. Future candidates, diagnostic defects, and navigation
interventions must use new pinned revisions and be reported separately. The
four bundle paths above are absent in the current checkout, so the recorded
121-command/16-message summary cannot be independently checked from local run
evidence here. The nine currently present `runs/run-048/`–`runs/run-056/`
directories are diagnostic captures, not replacements for those four baseline
bundles.

### Phase 4 — Architecture comparison and refinement

- Define coherent architecture candidates and diagnostic ablations from the
  first candidate. Change one material architectural choice at a time where
  practical: map granularity, ownership boundaries, routing links, document
  authority, or separation of durable and temporary context.
- Keep task prompts, target behaviour, model, runtime, validator, and evaluation
  oracle fixed while comparing candidates.
- Include both degraded ablations, which reveal what the architecture protects,
  and improved alternatives, which test whether a design change helps.
- Analyse answer correctness, required-claim coverage, disallowed claims,
  authority selection, relevant versus irrelevant exploration, command cost,
  failures, and final-answer support separately.
- Record which findings are architecture failures, task-design failures,
  validator blind spots, or natural agent limitations.
- Produce a refined candidate and rerun the shared task corpus against it.

Completion: at least one architecture comparison produces evidence for a
strength or weakness of a context-architecture choice, and the next candidate
is documented without changing the agent's navigation policy.

### Phase 5 — Independent architecture evaluation gate

Use `parallel-task` in full mode only after Phases 1–4 have concrete
architecture candidates, comparative traces, and refinement findings.
The independent perspectives should assess:

- context-architecture compliance and discoverability;
- whether the task corpus actually distinguishes architecture choices;
- validity and blind spots of passive observation; and
- whether the proposed refinement follows from evidence rather than one
  model's incidental behaviour.

A second-pass agent synthesises the findings. The coordinator audits the
synthesis, and canonical changes are adopted only after joint review.

Completion: the candidate architecture and its limits have been independently
challenged; the resulting corrections are applied before selecting the
architecture for intervention studies.

### Phase 6 — Navigation guidance intervention: `chat-start` (future)

- Freeze the best-supported architecture candidate and task matrix first.
- Test whether `chat-start` changes navigation, correctness, or cost under the
  same repository and tasks.
- Compare natural and `chat-start` runs without changing the repository
  architecture between them.
- Report the intervention effect separately from the architecture effect.

### Phase 7 — Future navigation mechanisms

- Consider locators, structured navigation protocols, or enforced tool
  interfaces only after the architecture and `chat-start` results are clear.
- Treat these as mechanisms for influencing navigation, not as evidence that
  the underlying information architecture is good.
- Report instrumentation and intervention effects separately from repository
  quality.

## Measurement principles

- The validator is passive; it must not prescribe a route in baseline runs.
- The primary object of comparison is the context architecture, not the
  validator or a navigation script.
- Architecture candidates must be compared under the same task, prompt, model,
  runtime, target behaviour, oracle, and validator conditions wherever
  possible.
- A trace is stronger evidence than an agent narrative.
- Final-answer correctness is necessary but not sufficient for retrieval
  efficiency.
- Primary outcome measures are required-claim coverage, disallowed-claim
  avoidance, authority selection, and support for the final answer. Secondary
  efficiency measures include relevant versus irrelevant exploration,
  command/action cost, failed actions, and—only when authoritative signals
  exist—files, scans, and tokens.
- Counts must distinguish discovered, returned, opened, cited, and physically
  scanned files where the runtime allows it; unavailable values remain
  unavailable rather than becoming zero.
- Deterministic checks and explicit ground truth are primary; model-based
  judgement is secondary.
- A candidate is not considered better because it helps one task or one model;
  conclusions require repeated evidence across task types and must state their
  generalisation limits.
- Every comparison pins the repository commit, task case, validator version,
  model, and relevant runtime configuration.
- The validator records externally observable actions, not hidden chain-of-
  thought or unexposed internal deliberation.
- Evaluation prompts may be agent-visible; their ground-truth oracles must live
  outside the agent-facing repository and be joined only after the run. The
  first corpus intentionally uses structured evidence checklists; route
  efficiency is analysed separately from claim coverage.

## Initial success criteria

The first architecture research cycle must have:

- an executable synthetic application;
- a root context map and justified local maps;
- an explicit first architecture candidate and its design hypotheses;
- a clean context-architecture audit with no unresolved baseline findings;
- manually authored tasks with ground truth;
- a passive trace schema and collector boundary;
- a provenance manifest for every captured run;
- a complete natural corpus with generated reports;
- at least one controlled comparison between architecture candidates or a
  diagnostic ablation;
- a written evidence-backed refinement or a justified decision not to refine;
- a written list of observability blind spots;
- no locator or navigation intervention mixed into the architecture study.

## Material decisions

| Decision | Choice | Reason |
| --- | --- | --- |
| Repository location | `context-lab-target` plus external `context-lab` harness | Keeps the measured project separate from experiment control and the `agent-skills` source catalog. |
| Evaluator oracle location | External evaluator sidecar joined after the run | Keeps ground truth outside the agent-facing repository and out of the measured workspace. |
| Repository type | Synthetic reference project | Gives us controlled ground truth, reproducible architecture candidates, and isolated comparisons before validation on real repositories. |
| Product domain | Project and task management | Provides realistic cross-cutting rules without excessive domain complexity. |
| Application shape | Small monorepo | Creates meaningful ownership and navigation boundaries. |
| Target code layout | API, worker, core, storage, and docs in `context-lab-target`; evaluation in `context-lab`; reusable validator in `efficiency-validator` | Keeps the measured project, experiment control, and reusable tool separate. |
| Stack | Python, FastAPI, SQLite, pytest, simple worker | Keeps the lab legible and locally runnable. |
| Evaluation cases | Manual, high quality over quantity | Makes expected sources and failure meanings reviewable. |
| Initial task corpus | Four manually authored cases | Covers local, cross-boundary, decision, and failure-investigation routes without optimising for quantity. |
| Baseline language | English | Avoids mixing documentation architecture with a multilingual evaluation variable. |
| Observed runtime | Real Codex sessions | Preserves ecological validity; any unobservable activity is reported as a blind spot. |
| Observation boundary | Externally verifiable Codex actions only | Keeps metrics evidence-based and avoids inferring hidden reasoning. |
| Initial Codex adapter | `codex exec --json` event parser | Uses real Codex sessions in read-only/ephemeral mode without introducing a locator. |
| Collection placement | Host/runtime launcher preferred; repo owns parsing and evaluation | Avoids pretending that a nested subprocess has the same runtime privileges as the measured Codex. |
| Baseline metric boundary | Command-level evidence is primary; file-level metrics require an authoritative joined signal | Prevents shell-command text, agent narratives, or missing values from becoming false retrieval precision. |
| Oracle contract | Required claim ids and disallowed overclaims are joined after the run | Makes answer review explicit and deterministic after normalized claim adjudication. |
| Prompt design | Structured evidence checklists are intentional | Gives the small corpus defined coverage while keeping route efficiency separate from answer quality. |
| Agent workspace boundary | Run the measured agent from an isolated staging copy containing only the pinned canonical repository | A sibling evaluator sidecar must never be reachable through the measured workspace. |
| Baseline runtime fixture | Prepare a separate locked runtime outside the staged target and inject it into the Codex process | Keeps documentation/navigation measurements separate from missing dependency setup; blank-checkout onboarding remains a separate scenario. |
| First architecture candidate | The current context architecture is a testable hypothesis, not the final design | Gives the lab a concrete starting point while preserving the purpose of comparative refinement. |
| First measurement | Passive natural observation | Measures the candidate's intrinsic behaviour before testing navigation improvements. |
| Architecture variants | Compare coherent alternatives and diagnostic ablations with the same task matrix | Tests which information-architecture choices improve agent work; defects alone are not the research objective. |
| Navigation interventions | Defer `chat-start`, locators, and enforced protocols until architecture refinement is complete | Separates repository information design from mechanisms that influence agent navigation. |
| `parallel-task full` | Deferred until architecture comparisons have concrete artefacts | Challenges the candidate architecture and evidence after the first refinement cycle. |

## Open decisions

- Whether to add a Portuguese documentation variant after the English
  baseline.
- Whether interactive Codex sessions expose the same event stream as `codex exec`.
- Which context-architecture hypotheses and alternatives belong in the first
  comparison set.
- How many repeated runs and held-out task types are needed before calling an
  architecture improvement robust.
- When and how to validate the refined principles on an existing real
  repository rather than only the synthetic target.
- A reliable filesystem-level signal for physical scan counts.
- Whether to add an external OS/process tracing layer for physical file access;
  this remains a future validator enhancement and must stay separate from
  navigation interventions.
- The commit or immutable working-tree identifier to use for each frozen
  architecture candidate.
- Which diagnostic documentation defects are useful after the architecture
  comparison is defined.

## Non-canonical working material

Future provisional handoffs, findings, traces, and experiment outputs must be
kept in a clearly marked working area and must not silently become canonical
repository guidance. The exact working layout will be defined before the
first parallel review.
