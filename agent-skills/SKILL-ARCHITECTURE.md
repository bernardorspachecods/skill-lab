# Skill Architecture — Current State

This document is a human-facing map of the skill catalog as it exists today.
It helps maintainers understand activation, composition, and repeated
principles before a later improvement pass.

It is not runtime context. An agent does not need to consult this document in
the middle of a task. The runtime sources remain each skill's `SKILL.md`, its
`agents/openai.yaml`, and the repository guidance that applies to the task.

## Scope and status

- Snapshot date: 2026-09-12.
- Catalog covered: all 20 skills currently under `skills/`.
- Classification basis: frontmatter descriptions, `agents/openai.yaml`, skill
  instructions, linked skill references, and the existing task routes.
- This is an `as-is` inventory. It records current evidence and useful
  inferences; it does not recommend keeping, cutting, merging, splitting, or
  rewriting any skill.
- No activation policy is changed by this document.
- No principle owner is declared canonical here. The `current locations` field
  records where a principle appears today.
- No automation or validator is part of this first phase.

## How to read the map

### Activation status

`agents/openai.yaml` is the technical source for the explicit manual-only
policy:

- `manual-only` — `policy.allow_implicit_invocation: false` is present.
- `model-selectable` — no explicit `allow_implicit_invocation: false` was found
  in the current metadata. This means the skill is eligible for model
  selection; it does not mean that it will activate for every matching task.
- `lifecycle` — the description establishes a conversation or task lifecycle
  position, such as the start of every chat or the end of a task.
- `cross-cutting` — the skill can apply across several routes rather than
  belonging to one route.

### Evidence confidence

- `observed` — directly stated by current frontmatter, metadata, or skill text.
- `inferred` — a useful interpretation of current text or references, not an
  explicit runtime rule.
- `uncertain` — plausible but not sufficiently established by the current
  catalog.

### Composition symbols

The route tables use these symbols only to describe the current catalog:

- `●` — primary apparent role in the scenario;
- `○` — supporting apparent role;
- `→` — likely sequencing or dependency relationship;
- `M` — manual-only or explicitly manual post-step;
- `?` — possible relationship needing future review;
- `—` — no current relationship recorded.

These symbols are not instructions to the runtime.

## 1. Skill catalog

The skill name is the stable identifier because it already matches the directory
and frontmatter contract in `AGENTS.md`. No additional numeric skill IDs are
introduced.

| Skill | Current activation status | Current role | Existing routes / scenarios | Evidence |
| --- | --- | --- | --- | --- |
| [`chat-start`](skills/chat-start/SKILL.md) | lifecycle; model-selectable | Start-of-chat repository context and working style | all routes; conversation entrypoint | observed |
| [`chat-wrap-up`](skills/chat-wrap-up/SKILL.md) | manual-only | Prepare repository context for a seamless next-chat continuation | conversation compaction; task/session transition | observed |
| [`check-docs`](skills/check-docs/SKILL.md) | model-selectable | Documentation and evidence checkpoint after work begins | documentation; software change; code review; research; any route with a material claim | observed/inferred |
| [`code-review`](skills/code-review/SKILL.md) | model-selectable | Two-axis review of a diff against standards and spec | `code_review`; post-implementation review | observed |
| [`codebase-design`](skills/codebase-design/SKILL.md) | model-selectable | Vocabulary and design guidance for deep modules and seams | `software_change`; `app_revamp`; `feature_evaluation` | observed/inferred |
| [`context-architecture`](skills/context-architecture/SKILL.md) | model-selectable | Organize agent-facing repository context | `documentation`; skill/agent-document reorganization | observed |
| [`domain-modeling`](skills/domain-modeling/SKILL.md) | model-selectable | Sharpen terminology, contexts, and architectural decisions | `feature_evaluation`; `documentation`; domain-heavy software change | observed/inferred |
| [`fresh-eyes`](skills/fresh-eyes/SKILL.md) | manual-only | Independent review after a substantive task | post-task review across routes | observed |
| [`git-worktree-cleanup`](skills/git-worktree-cleanup/SKILL.md) | manual-only | Commit relevant changes and leave the worktree clean | task closure after repository changes | observed |
| [`grill-stuck`](skills/grill-stuck/SKILL.md) | model-selectable | Re-ground unreliable work and recover from failed approaches | cross-cutting recovery | observed |
| [`grill-task`](skills/grill-task/SKILL.md) | model-selectable | Clarify tasks and decisions into actionable plans | task routing; complex work before execution | observed/inferred |
| [`grill`](skills/grill/SKILL.md) | model-selectable | Critically examine an idea, plan, or result without documenting it | `feature_evaluation`; `ask_human`; exploratory work | observed/inferred |
| [`handoff`](skills/handoff/SKILL.md) | manual-only | Transfer active work to another agent or session | task transition; long-running work | observed |
| [`lean-context`](skills/lean-context/SKILL.md) | manual-only | Remove redundant or stale agent-facing context | `documentation`; context cleanup | observed |
| [`prompt-design`](skills/prompt-design/SKILL.md) | model-selectable | Create, improve, audit, or structure prompts and briefs | `quick_answer`; `documentation`; route-specific prompt work | observed/inferred |
| [`prototype`](skills/prototype/SKILL.md) | model-selectable | Build a throwaway prototype to answer a design question | `app_revamp`; `feature_evaluation`; exploratory software work | observed/inferred |
| [`research`](skills/research/SKILL.md) | manual-only | Conduct rigorous source-first web research | `research_synthesis`; `long_document_analysis` | observed |
| [`test-first`](skills/test-first/SKILL.md) | model-selectable | Drive suitable software changes with behavior-first tests | `software_change` | observed |
| [`work-style`](skills/work-style/SKILL.md) | model-selectable | Recalibrate collaboration around the user's working principles | cross-cutting collaboration | observed |
| [`skill-authoring`](skills/skill-authoring/SKILL.md) | model-selectable | Create and maintain agent skills | skill creation or editing | observed |

### Current activation inventory

The current catalog contains:

- 14 skills without an explicit manual-only policy in `agents/openai.yaml`;
- 6 skills explicitly marked `manual-only`:
  `fresh-eyes`, `git-worktree-cleanup`, `handoff`, `lean-context`,
  `research`, and `chat-wrap-up`;
- 1 lifecycle skill whose description says it starts every chat:
  `chat-start`;
- several cross-cutting skills whose descriptions do not map to only one
  route, including `check-docs`, `grill-stuck`, `grill-task`, `grill`,
  `work-style`, and `chat-start`.

The absence of a manual-only policy is recorded as technical eligibility, not
as proof of actual activation in a given run.

## 2. Route and scenario matrix

The rows reuse the routes currently documented in
[`knowledge/agents/task-routing.md`](../knowledge/agents/task-routing.md).
The relationships are a current-state map inferred from descriptions and
workflow references. They are not target bundles.

| Route / scenario | Primary apparent skill(s) | Supporting apparent skill(s) | Conditional or manual participants | Confidence |
| --- | --- | --- | --- | --- |
| `quick_answer` | — | `chat-start` ○, `work-style` ? | `prompt-design` M when the request is about a prompt; `grill-stuck` ? if reasoning drifts | inferred |
| `software_change` | `test-first` ● when behavior is testable; `codebase-design` ● when interface/seam design is material | `chat-start` ○, `grill-task` ○, `check-docs` ○ | `prototype` ? for a design question; `code-review` → after implementation; `fresh-eyes` M; `git-worktree-cleanup` M | inferred |
| `code_review` | `code-review` ● | `chat-start` ○, `check-docs` ○ | `fresh-eyes` M as an independent post-review perspective | inferred |
| `app_revamp` | `prototype` ● when the design question benefits from a throwaway prototype | `codebase-design` ○, `chat-start` ○, `grill-task` ○ | `test-first` ? if production behavior is implemented; `code-review` → after implementation; `fresh-eyes` M | inferred |
| `research_synthesis` | `research` M ● | `chat-start` ○, `grill-task` ○ | `prompt-design` ? for the research brief; `grill-task` ? when evidence becomes durable documentation; `check-docs` ? for repository claims | inferred |
| `long_document_analysis` | `research` M ● | `chat-start` ○ | `prompt-design` ? for the brief; `grill-task` ? when the result becomes a decision or durable plan | inferred |
| `feature_evaluation` | `grill` ● or `grill-task` ● when a durable plan is needed | `grill-task` ○, `codebase-design` ○, `domain-modeling` ○ | `research` M for external evidence; `prototype` ? for a design question; `fresh-eyes` M after a result | inferred |
| `documentation` | `context-architecture` ● for structure | `check-docs` ○, `grill-task` ○ | `grill-task` ? for a durable decision; `domain-modeling` ? for terminology; `lean-context` M for cleanup; `prompt-design` ? for prompts | inferred |
| `ask_human` | `grill` ● for critical examination; `grill-task` ● when an actionable or documented plan is needed | `work-style` ○ | `grill-stuck` ? when evidence or context is unreliable; `research` M when external evidence is needed | inferred |

### Cross-cutting lifecycle and recovery map

| Lifecycle point | Current skill relationship |
| --- | --- |
| Start of conversation | `chat-start` is described as the entrypoint for every chat. |
| Before conversation compaction or a next-chat transition | `chat-wrap-up` prepares durable context and a non-canonical handoff when needed. |
| Before a complex task | `grill-task` may provide a short task plan; this is inferred from its description and workflow. |
| While a material claim or decision is being made | `check-docs` may re-check authoritative repository documentation. |
| When reasoning or execution becomes unreliable | `grill-stuck` is model-selectable and covers re-grounding and recovery. |
| After a substantive task | `fresh-eyes` is explicitly manual-only and reviews the completed result. |
| At task/session transition | `handoff` is explicitly manual-only. |
| At worktree closure | `git-worktree-cleanup` is explicitly manual-only. |

### Current composition examples

These are documentation examples of relationships already suggested by the
catalog. They are not runtime bundles and do not prescribe a future workflow.

#### C-01 — Create or reorganize an agent-facing document

```text
context-architecture  → identifies audience, authority, ownership, and placement
check-docs             → checks current repository guidance when claims depend on it
lean-context           → optional manual cleanup when redundancy is the task
fresh-eyes             → optional manual review after the result exists
```

#### C-02 — Make a software change

```text
grill-task             → possible preflight planning
test-first             → applicable when behavior is clear and TDD fits
codebase-design        → applicable when interface, seam, depth, or testability is material
check-docs             → applicable when repository rules or decisions matter
code-review            → review route after a diff exists
fresh-eyes             → optional manual independent review
git-worktree-cleanup   → optional manual closure
```

#### C-03 — Explore and document a decision

```text
grill                  → critical examination without an actionable plan
grill-task             → exploration that can end in a confirmed documented plan
domain-modeling        → applicable when terms, contexts, or an ADR need sharpening
context-architecture   → applicable when the decision changes document ownership or structure
```

The current repository does not contain a separate canonical composition
registry. The examples above are therefore `inferred`, not implemented
activation rules.

## 3. Current principle inventory

This inventory records principles that appear in the current material. It does
not decide which skill should own them in the future. “Current locations” means
where the idea currently appears, not an accepted ownership assignment.

| ID | Current principle | Evidence type | Current locations | Future review note |
| --- | --- | --- | --- | --- |
| `P-001` | Read applicable repository guidance before acting. | explicit | `chat-start`; `context-architecture`; `test-first`; `grill`; `grill-stuck` | repeated across entrypoint and task-specific workflows |
| `P-002` | Route or classify the work before choosing context and workflow. | explicit | `grill-task`; `prompt-design`; `knowledge/agents/task-routing.md`; `knowledge/context/context-selection.md` | shared routing principle across skills and knowledge docs |
| `P-003` | Choose the smallest sufficient workflow and avoid unnecessary process. | explicit | `skill-authoring`; `context-architecture`; `knowledge/agents/agent-workflows.md` | appears in both skill-writing and general workflow guidance |
| `P-004` | Keep one canonical source of truth and link rather than duplicate. | explicit | `skill-authoring`; `context-architecture`; `lean-context` | likely overlap to resolve later |
| `P-005` | Preserve local conventions and surface conflicts instead of silently replacing them. | explicit | `context-architecture`; `skill-authoring`; `check-docs` | shared documentation/context rule |
| `P-006` | Separate exploration, commitment, and implementation. | explicit | `grill`; `grill-task` | the two skills have different planning outcomes |
| `P-007` | Ask the human only when the decision is material, ambiguous, private, risky, or not safely discoverable. | explicit | `skill-authoring`; `prompt-design`; `grill-task`; `knowledge/agents/task-routing.md` | compare different wording and thresholds later |
| `P-008` | State uncertainty honestly and distinguish evidence from inference. | explicit | `chat-start`; `research`; `grill-stuck`; `check-docs` | recovery and research have different operating contexts |
| `P-009` | Verify the result against explicit criteria before finishing. | explicit | `skill-authoring`; `check-docs`; `test-first`; `research`; `fresh-eyes` | verification roles may overlap without being identical |
| `P-010` | Prefer behavior and public interfaces over implementation details in tests. | explicit | `test-first`; `codebase-design` | code-design-specific expression |
| `P-011` | Prefer deep interfaces, locality, and small surfaces over pass-through abstractions. | explicit | `codebase-design` | currently concentrated in one skill |
| `P-012` | Use independent review when the primary agent may be too invested in the result. | explicit | `fresh-eyes`; `code-review` | review axes and independence differ |
| `P-013` | Set stop conditions for iterative, delegated, or evidence-gathering work. | explicit | `research`; `code-review`; `skill-authoring`; `knowledge/agents/agent-workflows.md` | repeated across workflow types |
| `P-014` | Load targeted context and remove stale or irrelevant material. | explicit | `lean-context`; `context-architecture`; `knowledge/context/context-selection.md` | related to `P-004`, but not identical |
| `P-015` | Make prototypes disposable and capture only validated decisions in the real system. | explicit | `prototype` | currently concentrated in one skill |
| `P-016` | Use source-ledger and claim-level evidence for rigorous research. | explicit | `research` | research-specific; not automatically shared by all documentation |
| `P-017` | Adapt collaboration to the user's working principles and keep them involved. | explicit | `work-style`; `chat-start` | collaboration-specific expression |
| `P-018` | Keep manual-only workflows explicit and human-triggered. | explicit | `fresh-eyes`; `git-worktree-cleanup`; `handoff`; `lean-context`; `research` metadata/descriptions | runtime policy and prose should be compared in future review |

No principle in this table has a canonical owner yet. That is intentional for
the current-state phase.

## 4. Observed overlap ledger

This is a neutral record of areas that deserve the future improvement pass. It
does not label the overlap as a defect.

| Overlap area | Current locations | What is currently known | Status |
| --- | --- | --- | --- |
| Repository guidance before action | `chat-start`, `context-architecture`, `test-first`, `grill`, `grill-stuck` | Similar entry behavior is expressed in several workflows. | observed; unresolved |
| Routing before workflow | `grill-task`, `prompt-design`, task-routing and context-selection docs | Several documents describe routing at different levels. | observed; unresolved |
| Single source of truth / duplication control | `context-architecture`, `skill-authoring`, `lean-context` | All three address duplication, but with different audiences. | observed; unresolved |
| Verification before completion | `check-docs`, `skill-authoring`, `test-first`, `research`, `fresh-eyes` | Verification is distributed across task types and review modes. | observed; unresolved |
| Critical examination and human checkpoints | `grill`, `grill-task`, `grill-stuck`, `work-style` | The skills have distinct stated purposes, but their selection boundaries merit comparison. | inferred; unresolved |
| Context reduction and selective reading | `lean-context`, `context-architecture`, `context-selection` | Related context-management guidance exists at skill and knowledge levels. | observed; unresolved |

## 5. Sources and maintenance boundary

### Primary sources used for this snapshot

- [`agent-skills/AGENTS.md`](AGENTS.md)
- all 20 `skills/*/SKILL.md` files;
- all present `skills/*/agents/openai.yaml` files;
- [`knowledge/agents/task-routing.md`](../knowledge/agents/task-routing.md);
- [`knowledge/context/context-selection.md`](../knowledge/context/context-selection.md);
- [`knowledge/agents/agent-workflows.md`](../knowledge/agents/agent-workflows.md);

### Not part of this first phase

- changing skill descriptions or bodies;
- changing invocation metadata;
- deciding canonical principle ownership;
- resolving apparent duplication;
- judging whether a skill should be kept, cut, merged, or split;
- adding scripts, schemas, generators, or validators;
- treating inferred scenario combinations as runtime behavior.

The next improvement phase can use this document as its starting inventory and
record decisions separately from the current-state facts.
