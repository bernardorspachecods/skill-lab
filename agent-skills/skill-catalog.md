---
plan_id: SC0
kind: root
parent: null
phase: root
status: not_started
depends_on: []
consumers: [agent-skills/SKILL-ARCHITECTURE.md]
---

# Skill catalog validator and generator

## Objective

Create a deterministic, read-only validator and generator for the reusable
skill catalog.

The validator must detect invalid skill packages, empty skill directories,
missing or inconsistent metadata, broken internal references, and catalog
drift. The generator must produce `SKILL-ARCHITECTURE.md` from the actual skill
directories and their supported metadata so that the catalog is never edited
manually.

The resulting catalog contains only information that can be derived from the
repository. It must not invent lifecycle, role, composition, or architectural
relationships that are not explicitly represented by a supported source.

## Scope

### Skill package validation

- Treat each direct child of `agent-skills/skills/` as a candidate package.
- Reject empty candidate directories unless an explicit future exception
  contract is introduced.
- Require `SKILL.md` for every package.
- Parse and validate `SKILL.md` frontmatter.
- Require `name` and `description`.
- Require the frontmatter `name` to match the directory name.
- Validate relative links and referenced files under the skill package.
- Validate `agents/openai.yaml` when present.
- Check that referenced scripts, references, and assets exist.
- Detect machine-specific absolute paths where repository-relative paths are
  expected.
- Detect duplicate skill names and ambiguous package paths.
- Report optional metadata as missing or unknown rather than guessing.

### Generated catalog

- Generate `SKILL-ARCHITECTURE.md` from the discovered skill packages.
- Include stable ordering and deterministic formatting.
- Include the skill name, description, package path, and metadata that can be
  derived from the package and supported runtime configuration.
- Include links that resolve from the generated document.
- Exclude fields such as `draft`, `current role`, or inferred composition
  until a future explicit metadata contract exists.
- Mark the output as generated and not manually editable.
- Make generated output reproducible from the same repository state.

### Read-only and write boundaries

- `validate_skill_catalog.py` must never modify the repository.
- The generator must write only when explicitly invoked in write mode.
- A check mode must compare generated output with the committed
  `SKILL-ARCHITECTURE.md` and fail on drift without writing.
- External auditors may consume validator results, but the catalog plan does
  not depend on any particular auditor or health-check workflow.

## Output

The plan produces:

1. A deterministic skill-package validator.
2. A deterministic catalog generator.
3. A generated `SKILL-ARCHITECTURE.md` with an explicit generated-file
   header.
4. A machine-readable validation result suitable for the health-check ledger.
5. Fixtures and verification cases for valid packages and controlled defects.

Validation results must distinguish at least:

- valid;
- invalid;
- missing;
- empty;
- drifted;
- unavailable;
- indeterminate.

Each issue should include a stable code, severity, path, line or structural
location where available, explanation, and suggested action.

## Plan tree

No child subplans are defined yet. Split a phase out only when it gains an
independent owner, output, lifecycle, or execution boundary; the generated
catalog remains the single output of this plan.

## Sequence

1. **S1 — Establish the catalog boundary**
   - **Action:** Confirm the skill root, package discovery rules, generated
     output path, ignored paths, and the relationship with the HC0 health-check
     plan.
   - **Output:** A source-boundary and output contract.
   - **Exit check:** The validator can identify which directories are skill
     packages and which file is the generated catalog.

2. **S2 — Freeze the package contract**
   - **Action:** Translate the `skill-authoring` and catalog conventions into
     deterministic rules for frontmatter, package names, references, scripts,
     assets, and optional runtime metadata.
   - **Output:** Versioned validation rule catalogue with stable codes.
   - **Exit check:** Every planned finding maps to a concrete file-system or
     metadata observation.

3. **S3 — Implement package validation**
   - **Action:** Implement `validate_skill_catalog.py` as a read-only,
     dependency-conscious validator with text and machine-readable output.
   - **Output:** Validator covering empty directories, missing `SKILL.md`,
     frontmatter, names, links, references, runtime metadata, and paths.
   - **Exit check:** Controlled fixtures produce deterministic findings and
     the validator never writes to the target repository.

4. **S4 — Define the generated catalog schema**
   - **Action:** Define the exact fields, ordering, headings, links, generated
     header, and unknown-value policy for `SKILL-ARCHITECTURE.md`.
   - **Output:** A versioned generated-document contract.
   - **Exit check:** Every generated field has one documented source and no
     field depends on manual edits.

5. **S5 — Implement catalog generation**
   - **Action:** Implement deterministic generation with explicit write and
     check modes. Generate the catalog from package discovery, `SKILL.md`, and
     supported runtime metadata.
   - **Output:** Generator and reproducible `SKILL-ARCHITECTURE.md` output.
   - **Exit check:** Repeated generation from unchanged inputs produces the
     same output and check mode detects manual or stale edits.

6. **S6 — Migrate the existing catalog**
   - **Action:** Replace the manually maintained inventory in
     `SKILL-ARCHITECTURE.md` with generated output, including existing skills
     that were previously omitted and excluding empty directories.
   - **Output:** A catalog synchronized with the actual skill packages.
   - **Exit check:** No skill package is missing from the catalog and no
     catalog entry points to a nonexistent package.

7. **S7 — Verify operational boundaries**
   - **Action:** Test valid packages, empty directories, missing metadata,
     mismatched names, broken references, malformed runtime metadata, stale
     catalog output, duplicate packages, and machine-specific paths.
   - **Output:** Regression fixtures and a verification report.
   - **Exit check:** Validator and generator preserve their read-only/write
     boundaries and produce stable machine-readable results.

8. **S8 — Document the maintenance workflow**
   - **Action:** Document that maintainers edit skills and metadata, then run
     the generator or check command; they do not edit the generated catalog.
   - **Output:** A concise catalog maintenance contract linked from the
     relevant repository guidance.
   - **Exit check:** A new skill can be added without manually editing the
     catalog, and stale generated output is caught before publication.

## Completion criteria

- Empty skill directories are detected and reported.
- Every real skill package is validated and represented in the generated
  catalog.
- `SKILL.md` names and descriptions are valid and directory names match.
- Relative references, scripts, assets, and supported runtime metadata are
  checked.
- `SKILL-ARCHITECTURE.md` is generated deterministically and marked as such.
- Check mode detects catalog drift without modifying files.
- Write mode is explicit and limited to the generated catalog.
- The generated catalog contains no manually maintained lifecycle or role
  claims.
- Validator output is machine-readable and compatible with the HC0 findings
  ledger.
- Fixtures cover valid, invalid, missing, empty, drifted, unavailable, and
  indeterminate states.
