---
plan_id: HC0
kind: root
parent: null
phase: root
status: not_started
depends_on: []
consumers: []
---

# Repo health check

## Objective

Create a generic, read-only health-check skill for repositories that are
intended to be navigable and maintainable by LLMs.

The health check must evaluate both the repository's agent-facing navigation
and the structure that supports it. It must produce evidence-backed findings
and recommendations without checking whether domain content is true or
rewriting content automatically.

The skill should work in repositories that already follow the agent-facing
architecture and in repositories that do not yet have `CONTEXT.md`,
`AGENTS.md`, skills, plans, or equivalent structures.

## Scope

### In scope

- Repository discovery, scope selection, exclusions, and local exceptions.
- Detection of applicable health-check components.
- Agent-facing navigation and progressive retrieval.
- Context maps, task routers, entrypoints, links, anchors, and ownership.
- Document placement, granularity, lifecycle, and canonical authority.
- Plans, current-state pointers, durable work, and temporary work.
- Skills and skill metadata when the repository contains them.
- Duplication between files and within the same file.
- Orphaned, redundant, misplaced, stale, or conflicting documentation.
- Markdown links, frontmatter, JSON/YAML metadata, runtime paths, and
  references.
- Editorial signals such as unclear prose, inconsistent terminology, and
  English or grammar problems.
- Optional behavioural navigation probes using representative tasks.
- Optional efficiency evidence from the reusable
  [`efficiency-validator`](../context-lab/efficiency-validator/reference/PLAN.md)
  when a controlled navigation comparison is justified.
- A normalized findings ledger and a detailed report for human review.

### Out of scope

- Verifying whether domain or product content is factually true.
- Improving domain knowledge or substantive content for its own sake.
- Reviewing product correctness or code quality except where it affects
  agent-facing navigation, ownership, or documentation integrity.
- Automatically editing, moving, deleting, staging, or committing files.
- Treating an advisory prose signal as a structural failure.

### Operating constraints

- The audit is read-only by default.
- The repository root and excluded paths must be explicit in the run context.
- Generated, dependency, vendor, cache, and temporary paths must be excluded
  by default, with repository-specific exclusions supported.
- Local exceptions are acceptable only when they are documented by the
  repository and can be linked to the affected finding.
- A failed, unavailable, or inconclusive check must be reported as such; it
  must not be treated as a pass.
- The health check must use skill names and repository-relative paths rather
  than machine-specific absolute paths.

## Output

The primary output is a detailed report plus a normalized findings ledger.

The report must contain:

1. Repository root, scope, exclusions, and assumptions.
2. Detected repository profile and applicable components.
3. Components executed, skipped, unavailable, or inconclusive, with reasons.
4. A short executive summary grouped by navigation risk and maintenance risk.
5. Findings ordered by severity, confidence, and likely navigation impact.
6. Recommendations grouped into quick fixes, structural refactors, and
   follow-up investigations.
7. Optional behavioural-probe results, clearly separated from static checks.
8. Residual uncertainty and decisions that require repository-owner review.

Each finding should preserve the strongest available evidence and include:

- a stable finding ID;
- component and category;
- severity and confidence;
- file path and line or structural location;
- evidence from a script, agent analysis, behavioural probe, or combination;
- the violated rule or architectural principle;
- why the issue affects LLM navigation or repository maintenance;
- a concrete recommendation;
- the suggested owner or follow-up skill;
- dependencies, related findings, and current status.

The report must distinguish at least:

- pass;
- finding;
- not applicable;
- not detected;
- unavailable;
- indeterminate.

## Plan tree

This root plan currently owns all phases. Split a phase into a subplan only
when it gains an independent owner, output, lifecycle, or execution boundary.

## Sequence

1. **S1 — Establish the repository boundary**
   - **Action:** Identify the repository root, Git state, selected scope,
     default exclusions, `.contextignore` rules, and documented local
     exceptions.
   - **Output:** A run profile describing what is and is not being audited.
   - **Exit check:** Every excluded or included area has an explicit reason.

2. **S2 — Detect the repository profile**
   - **Action:** Discover whether the repository contains context maps,
     agent rules, plans, current-state pointers, skills, documentation areas,
     scripts, and other structures that activate health-check components.
   - **Output:** An applicability matrix with `applicable`, `not_applicable`,
     `not_detected`, and `unknown` states.
   - **Exit check:** The run can explain why each component was activated or
     skipped.

3. **S3 — Inventory existing machine checks**
   - **Action:** Reuse the existing validators and record their coverage,
     input options, output shape, exit behaviour, and limitations.
   - **Output:** A machine-check adapter matrix.
   - **Exit check:** No existing validator is reimplemented without a stated
     gap or incompatible output contract.

   - **Context architecture validator:**
     `skills/context-architecture/scripts/validate_context_architecture.py`
     is read-only and dependency-free. It discovers tracked and untracked
     files, applies default exclusions and `.contextignore`, and can emit JSON.
     It currently checks root and local context coverage, `AGENTS.md` links,
     the root task router, `CURRENT-STATE.json`, navigation maps, and Markdown
     links. Its configurable thresholds and `--require-context` rules must be
     surfaced in the health-check run profile.

   - **Durable plan validator:**
     `skills/plan-management/scripts/validate_plans.py` checks plan
     frontmatter, IDs, parent and dependency relationships, required sections,
     links, sequence outputs and exit checks, parent-child links, cycles, and
     repeated paragraphs. Its text-only output must be normalized into the
     common findings ledger.

   - **Temporary plan validator:**
     `skills/plan-management/scripts/validate_temporary_plans.py` checks the
     execution plan, finding documents, review document, links, statuses,
     required sections, and the review/cleanup packet. It must be activated
     only when a temporary delegation packet is detected.

   - **Plain technical writing linter:**
     `skills/plain-technical-writing/scripts/lint_plain_english.py` provides
     advisory line-level signals for modal language, vague wording,
     contractions, semicolons, em dashes, and long sentences. It must remain
     advisory and must not be converted into a truth or compliance gate.

4. **S4 — Define the universal navigation checks**
   - **Action:** Specify checks that apply to every repository or to every
     repository with documentation, including entrypoints, task routing,
     discoverability, link integrity, orphaned documents, stale anchors,
     progressive retrieval, authority conflicts, context duplication, and
     excessive hierarchy depth.
   - **Output:** A navigation-check catalogue with rule IDs and evidence
     requirements.
   - **Exit check:** Every navigation finding can point to a concrete file,
     path, link, or failed route.

5. **S5 — Define the structural and lifecycle checks**
   - **Action:** Specify checks for ownership, canonical sources, document
     purpose, file placement, granularity, durable versus temporary work,
     current-state ownership, legacy artifacts, and divergence between
     documented architecture and the actual tree.
   - **Output:** A structure-and-lifecycle check catalogue.
   - **Exit check:** The catalogue distinguishes structural violations from
     recommendations that require human judgement.

6. **S6 — Define conditional component checks**
   - **Action:** Add modules that activate only when their artefacts are
     detected, including skills, `SKILL.md`, `agents/openai.yaml`, plans,
     public documentation, references, scripts, and configuration files.
   - **Output:** Component rules with activation predicates and exclusions.
   - **Exit check:** A repository without a component receives no false
     positive for that component, while a repository with the component gets
     a complete audit.

7. **S7 — Define the bounded agent review**
   - **Action:** Create a fixed checklist and evidence protocol for judgements
     that scripts cannot safely make, such as competing authority, misplaced
     documentation, meaningful duplication, unclear ownership, and language
     consistency.
   - **Output:** An agent review protocol that constrains judgement without
     pretending that semantic review is deterministic.
   - **Exit check:** Every subjective finding records evidence, uncertainty,
     and the reason it was not classified as a machine-check failure.

8. **S8 — Define optional behavioural navigation probes**
   - **Action:** Support representative tasks that test whether an agent can
     identify the correct entrypoint, authoritative rule, current state, and
     affected files without unnecessary reading.
   - **Output:** A probe protocol and result format that reports route,
     evidence path, unnecessary reads, and unresolved uncertainty.
   - **Exit check:** Behavioural results are labelled as verified, failed, or
     not run and are never inferred from static structure alone.

9. **S9 — Integrate the efficiency validator**
   - **Action:** Use the reusable
     [`efficiency-validator`](../context-lab/efficiency-validator/reference/PLAN.md)
     as the optional behavioural-evidence provider. Consume its saved run
     bundles and reports through a stable contract rather than importing its
     implementation internals.
   - **Output:** An integration contract supporting two modes:
     `audit_mode`, which runs static checks and bounded agent review, and
     `evidence_mode`, which additionally runs controlled navigation probes.
   - **Required evidence:** Evidence-mode runs must define a navigation task,
     expected entrypoint or authority, target revision, model/runtime,
     evaluator oracle, sandbox, and one declared controlled variation.
   - **Quality boundary:** The quality gate must verify that the agent reached
     the expected navigation context and completed the task. It must not turn
     domain-content truth into a health-check requirement.
   - **Cost boundary:** Pair comparison may use tokens, context, commands,
     searches, tool calls, filesystem evidence, failures, retries, and timing
     when available. Missing signals remain `unavailable` and are never treated
     as zero.
   - **Output contract:** Attach the run bundle, quality result, comparison
     verdict, observability coverage, and limitations to the health-check
     report as behavioural evidence. Keep evidence-backed observations
     separate from static findings and agent judgements.
   - **Exit check:** No behavioural efficiency claim is emitted unless pair
     identity, provenance, quality, controlled variation, and observability
     requirements pass. Otherwise the result is `inconclusive` or
     `unavailable` with a reason.

10. **S10 — Define finding normalization and report merging**
   - **Action:** Normalize JSON, text, and agent-generated findings into the
     common ledger; deduplicate overlapping findings; preserve source evidence;
     classify severity and confidence; and distinguish failures from
     unavailable or indeterminate checks.
   - **Output:** A stable ledger schema and merge rules.
   - **Exit check:** The same underlying issue is represented once while all
     contributing evidence sources remain traceable.

11. **S11 — Specify read-only orchestration**
    - **Action:** Define how the health-check skill invokes applicable
      validators, handles non-zero exits, continues after independent failures,
      records run metadata, and delivers the report without changing the
      target repository.
    - **Output:** An orchestration contract and safety boundary.
    - **Exit check:** A dry run can prove that no target file was modified.

12. **S12 — Implement the generic skill package**
    - **Action:** Package the health check under the normal skill catalog
      contract, with a narrow description, invocation policy, references,
      scripts or adapters, and report examples.
    - **Output:** A reusable health-check skill that does not depend on
      `/Users/...` paths or this repository's private layout.
    - **Exit check:** The skill can discover and audit a conforming repository,
      a partially conforming repository, and a repository without agent-facing
      context structures.

13. **S13 — Verify on representative repositories**
    - **Action:** Run the health check against at least one well-structured
      repository, one repository with controlled defects, and one repository
      with no agent-facing structure. Verify both machine findings and agent
      findings.
    - **Output:** Verification reports and a list of remaining false positives,
      false negatives, and unsupported cases.
    - **Exit check:** Reports are detailed, reproducible, read-only, and useful
      for deciding what another skill or human should change next.

## Completion criteria

- The health check is generic and does not contain machine-specific absolute
  paths.
- The run is read-only and its validators preserve that property.
- Components are activated from repository evidence rather than assumed.
- Existing context, durable-plan, temporary-plan, and prose validators are
  reused where their contracts fit.
- Machine output and agent analysis are normalized into one findings ledger.
- The ledger records evidence, location, severity, confidence, impact,
  recommendation, owner, and uncertainty.
- Static navigation checks and optional behavioural probes are clearly
  separated.
- Efficiency evidence is optional and uses the `efficiency-validator` only
  through a stable run/report contract.
- Navigation quality gates verify route/context completion rather than domain
  truth.
- Paired efficiency claims require controlled variation, provenance, quality,
  and observable-cost coverage; unavailable metrics remain explicit.
- Findings about truth or substantive domain quality are excluded.
- The final report distinguishes pass, finding, not applicable, not detected,
  unavailable, and indeterminate states.
- The skill is validated against representative repositories and its report
  can be reviewed without requiring automatic fixes.
