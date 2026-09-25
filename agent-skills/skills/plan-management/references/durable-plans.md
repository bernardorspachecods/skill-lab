## Durable plan contract

Treat a durable plan as a small directed graph, not as a collection of essays.
Every plan document has one owner, one objective, one intended output, and
explicit links to the plans that produce or consume its work.

- The root plan owns the overall objective, global scope, non-goals, phase map,
  cross-phase constraints, and consolidated status.
- A subplan owns one bounded phase or outcome. It references the root and does
  not copy the root's objective, context, decisions, or other subplans' work.
- A parent records the child plan's purpose and link; the child records the
  execution detail and output. Neither document becomes a duplicate of the
  other.
- Each output has a stable description, a completion check, and an explicit
  consumer or handoff. If no consumer exists, state why the output is the
  final result or remove the output.

## Plan document contract

New or materially edited plan documents use this frontmatter:

```yaml
---
plan_id: P0.1
kind: subplan
parent: P0
phase: 1
status: not_started
depends_on: []
consumers: []
---
```

Required values:

- `plan_id` is unique within the repository's plan tree.
- `kind` is `root` or `subplan`.
- A root has `parent: null`; a subplan names an existing plan ID.
- `phase` is `root` for a root or identifies the parent's phase for a
  subplan.
- `status` is one of `not_started`, `in_progress`, `blocked`, or `complete`.
- `depends_on` and `consumers` are lists.
- `depends_on` is the canonical record of incoming dependencies. Plan
  consumers are derived from other plans' `depends_on`; `consumers` is explicit
  only for external artifacts or destinations that are not plan nodes.

Relationships live in frontmatter. The body may include optional dependency or
handoff notes only when they add unique interpretive context that does not fit
the frontmatter or structured sections. Notes must not repeat relationships,
outputs, requirements, sequence, completion criteria, or create new
instructions. If a note adds no unique information, omit it. Every plan
contains these sections, in this order:

```markdown
## Objective
## Scope
## Output
## Sequence
## Completion criteria
```

Keep the sections concise. The structure carries the workflow; prose explains
only decisions, constraints, or context that the reader needs to act.

Each sequence item is an ordered step with an action, an output, and an exit
check:

```markdown
## Sequence

1. **S1 — Establish the source boundary**
   - **Action:** Identify the authoritative inputs.
   - **Output:** A source list linked from this plan.
   - **Exit check:** Every required input has an owner and link.
```

The root additionally has a `## Plan tree` section listing its phases and
linking each child plan. A child plan names its parent in frontmatter and links
back to the relevant parent phase where useful.

## Construction workflow

1. Read the applicable `CONTEXT.md`, `AGENTS.md`, current state, and existing
   plan tree. Reuse the existing canonical plan; do not create a parallel
   tracker because the current document is inconvenient.
2. Classify the requested change as root-plan, subplan, plan revision, or
   execution update. Resolve ownership before writing.
3. State the objective and the single output for the plan. Reject a plan whose
   output cannot be distinguished from its parent's output or another child's
   output.
4. Define frontmatter relationships and the sequence before adding
   explanatory prose. Order steps by required inputs and produced outputs, not
   by the order in which ideas were discussed.
5. Write only the local detail needed to execute this plan. Replace repeated
   context with a link and a short statement of its local consequence.
6. Update parent links, child metadata, consumers, and status together when a
   plan is added, removed, renamed, or materially re-scoped.
7. Run the durable plan validator and manually inspect only the semantic
   questions it cannot establish: whether the objective is worthwhile,
   whether the output is substantively correct, and whether the trade-offs are
   acceptable.

## Coordination rules

- A subplan may consume a parent output, but must not redefine the parent
  objective. Use the parent plan ID and a link instead.
- A downstream plan may start only when its declared dependencies and entry
  conditions are satisfied.
- A completed subplan publishes its output at the location named in the plan
  and updates its status. Downstream plans declare their dependency on that
  output; external consumers are recorded explicitly in `consumers`. It does
  not silently modify unrelated plans.
- `CURRENT-STATE.json` is only a resume pointer. Do not put plan prose,
  decisions, or a second status narrative there.

## Completion and closure gate

`status: complete` closes execution, not the plan's lifecycle. Before
continuing, verify the output, dependencies, consumers, and owned information,
then ask the user to choose:

- **Delete** the plan, repairing any affected links or metadata.
- **Archive** it in the relevant `reference/` directory as legacy and remove it
  from the active plan tree.

Until the user chooses, leave the plan untouched and do not create another
plan. Use: “O plano `<path>` está concluído. Quer que o apague ou que o mova
para `<reference-path>/` como referência legada?”

## Validation boundary

The durable-plan validator can check metadata, required sections, sequence
shape, plan IDs, parent references, dependency references, parent-child links,
and repeated paragraphs. It cannot decide whether an objective is strategically
correct or whether an output is substantively valuable. Report those as human
review items instead of disguising them as structural failures.

Run:

```bash
python3 skills/plan-management/scripts/validate_plans.py <repository>
```

Use `--strict` when a repository is adopting the contract or when explicitly
selected plan files must already comply. Existing plans without the frontmatter
are reported as migration warnings by default; do not rewrite them merely to
silence the validator.

Finish when the plan tree has one clear owner per fact, every active plan has a
bounded output and sequence, all required links and dependencies resolve, the
completion gate has an explicit user disposition for every completed plan, and
the remaining review items concern content or decisions rather than form.
