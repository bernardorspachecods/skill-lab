# Academic Research Mode

Use this reference when `research` is applied to academic papers, literature
reviews, thesis planning, empirical findings, or research-question design.

This is an optional branch of the `research` skill, not a separate skill. It
shares the same source ledger, claim IDs, evidence entries, uncertainty rules,
and citation audit. The branch supplies a compact contract for academic
subtasks and a pipeline that keeps evidence from being lost between stages.

## Contract for each subtask

Before delegating or composing a focused academic task, make the brief
self-contained:

- **Role** — the function being performed, such as paper mapper, finding
  extractor, literature synthesizer, or question critic;
- **Objective** — one concrete outcome;
- **Inputs** — paper/source IDs, excerpts or files, topic, population, period,
  and the decision the work supports;
- **Requirements** — the claims, limitations, comparisons, or checks that must
  be present;
- **Output format** — the requested content, its destination within the
  research artifacts or consumer-facing output, and any local finding IDs;
- **Evidence gate** — what must be linked to a page, section, table, figure,
  dataset, or external source before the artifact is accepted.

Treat this as a task contract, not as permission to invent a persona or fill
missing fields with plausible content. If the source was not provided or
retrieved, say so.

Academic stages and records are content within the assigned research unit;
they do not create separate research identities or shared-model artifacts.
Use the parent skill's `RES-ID.working` for temporary extraction and stage
material, and `RES-ID.audit` for verified source descriptions, material
findings, evidence, and limitations. Local IDs such as `F1` identify finding
records within that work; they do not replace the parent skill's claim IDs,
evidence IDs, source IDs, or artifact IDs. Keep the original paper or source
available by its source ID and resolved location for each later stage, without
copying it into additional artifacts.

Deliver the final academic synthesis through the parent skill's consumer-facing
output contract: use or update `KNOW` when findings are intended for reuse, put
a concise local decision synthesis in the requesting plan's `Outcome` when
applicable, or answer in the conversation when there is no durable consumer.
The parent skill's rigor level determines which research artifacts are
temporary or retained.

## Source-preserving pipeline

Choose only the stages that serve the user's question. A literature review may
need all of them; a question about one paper may need only mapping and finding
extraction.

```text
paper/source
   ↓
orientation map → finding cards → thematic synthesis → question cards
                         ↘ limitations / open questions
```

### 1. Orientation map

Record enough context to prevent a result from being detached from its study:

- bibliographic identity, version, publication/access dates, and source ID;
- research question or objective;
- theoretical frame, if the paper actually states one;
- design, data, sample/population, measures, and setting;
- main results and the authors' stated limitations;
- unclear, missing, or inaccessible information.

Separate what the authors report from what the agent infers. Do not call a
paper's contribution “novel” merely because the text uses that word; check the
relevant literature and qualify the result as a candidate contribution when
that comparison has not been done.

### 2. Finding cards

For each material finding, create a compact card:

```text
F1
Claim: what the source supports
Location: page/section/table/figure or exact web passage
Evidence: data, method, comparison, or quotation that supports it
Scope: population, setting, period, and conditions
Author interpretation: what the source says it means
Agent inference: separate and labelled, if needed
Limitations: threats, exclusions, uncertainty, and unreported details
Support/confidence: supported | partial | uncertain | contradicted
```

Finding cards point to the original source. A summary can help navigate a long
paper, but it cannot be the sole support for a material finding when the paper
or underlying data is available.

### 3. Thematic literature synthesis

Organize a review by concepts, mechanisms, methods, populations, or tensions
that answer the brief—not by producing one paragraph per paper. For each theme,
show:

- which finding cards and sources belong to it;
- where results converge and where they conflict;
- differences in design, sample, measurement, or context that may explain the
  conflict;
- what is genuinely missing versus merely not searched or not accessible.

Do not impose a fixed number of studies, a publication cutoff, or a claim of
consensus unless the brief or an appropriate review protocol justifies it.
Group papers that report the same underlying dataset, trial, or result as one
provenance cluster; multiple papers are not automatically independent evidence.

### 4. Research-question cards

Generate candidate questions from supported findings, explicit limitations,
and verified gaps. Each card should contain:

- the question, narrow enough to be answerable;
- the finding/limitation IDs that motivate it;
- constructs, population, context, and time period;
- a plausible method and data requirement, if requested;
- what would count as an informative answer or disconfirmation;
- feasibility risks and competing explanations;
- a note that “novel” or “impactful” remains provisional until checked against
  the relevant literature and constraints.

Questions are proposals, not findings. Do not feed questions generated from an
unsupported summary back into the synthesis as if they were evidence.

### 5. Thesis-oriented critique

When the user asks for thesis mentoring, return a bounded diagnosis rather than
a confident gap statement. Distinguish:

- gap supported by the reviewed literature;
- gap suggested by a limitation or context boundary;
- gap that is only a hypothesis for further searching;
- methodological, theoretical, data, and practical contributions.

Only formulate a testable hypothesis when the constructs, direction (if
appropriate), population, and observable measures are explicit enough to test.
Ask the human when the thesis discipline, research paradigm, ethics process,
or institutional requirements would materially change the recommendation.

## Minimum academic output

For a single paper, provide an orientation map plus finding cards and open
questions in proportion to the chosen rigor level. For a literature review or
thesis decision, add the thematic synthesis, source/claim trail, conflicts, and
the question cards or bounded gap diagnosis requested by the user. Keep these
as sections or records in `working`/`audit` as appropriate; do not create one
artifact per academic stage.

The concise version may be prose, but every material finding must still be
traceable. Standard and high-stakes work follows the parent skill's visible
claim matrix, `E#` entries, source ledger, search record, and stop rationale
in the applicable research artifacts. The consumer-facing synthesis should
summarize the audit trail rather than duplicate it.
