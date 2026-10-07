# Academic Research Mode

Use this reference when `$research` is applied to academic papers, literature
reviews, thesis planning, empirical findings, or research-question design. It
adds academic-specific structures and stages to the parent skill's general
workflow. Follow the parent skill for the research brief, source evaluation,
claim-linked evidence, general synthesis and audit, rigor-dependent records,
and consumer-facing output. Choose only the academic stages that serve the
question.

## Contract for focused academic subtasks

When delegating or composing a focused academic subtask, make its brief
self-contained:

- **Role** — the academic function, such as paper mapper, finding extractor,
  literature synthesizer, or question critic;
- **Objective** — one concrete outcome;
- **Inputs** — source IDs and available papers or excerpts, plus the topic,
  population, period, or decision needed for this subtask;
- **Requirements** — the findings, limitations, comparisons, or checks needed
  for the outcome;
- **Output** — the requested content, destination, and any local finding IDs;
- **Evidence gate** — the page, section, table, figure, dataset, or source link
  needed to verify a material result.

Do not invent a persona or fill missing fields with plausible content. If a
source was not provided or retrieved, say so.

## Academic findings and records

Academic stages belong to the assigned research unit. They do not create a new
research identity or one artifact per stage. Keep `F#` finding cards and
interim stage material in `RES-ID.working`; keep verified source descriptions
and canonical `E#` evidence records in `RES-ID.audit`, following the parent
skill's rigor and retention rules.

An `F#` card is an academic summary of a finding reported by a source. It helps
orient and compare studies; it is not a second evidence record. The parent
skill's `E#` remains the canonical claim-linked record for the exact passage
or data, location, relation to `C#`, limits, support status, and confidence.
Each material `F#` links to the relevant `E#` entry or entries instead of
copying their evidence or claim-support assessment. `F#` IDs are local to the
research unit and do not replace parent `C#`, `E#`, `S#`, or artifact IDs.

## Source-preserving pipeline

Select stages to fit the question. A literature review may use the full
pipeline; work on one paper may need only orientation and finding extraction.

```text
paper/source
   ↓
orientation map → finding cards → thematic synthesis → question cards
                         ↘ limitations / open questions
```

### 1. Orientation map

Link the map to the source ID in the parent source ledger. Record academic
context needed to interpret the study:

- research question or objective;
- theoretical frame, if the paper states one;
- design, data, sample or population, measures, and setting;
- main author-reported results and stated limitations;
- unclear, missing, or inaccessible information.

Separate author-reported results from agent inference. Do not call a paper's
contribution “novel” merely because the paper uses that word. Check the
relevant literature, or qualify novelty as provisional when that comparison
has not been made.

### 2. Finding cards

Create an `F#` card for each source finding material to the task. Keep the
summary concise and use the parent `E#` entry for its claim-linked support:

```text
F1
Finding: result or conclusion reported by the source
Evidence links: relevant E# entries
Author interpretation: what the source says the finding means
Study context: finding-specific context, if not clear from the orientation map
Agent inference: separate and labelled, if needed
```

Do not add exact passages, data, locations, support status, or confidence
assessments to the `F#` card when those are recorded in its linked `E#` entries.
Use the `E#` entries, not the `F#` summary alone, to support material claims.

### 3. Thematic literature synthesis

Organize a literature review by concepts, mechanisms, methods, populations, or
tensions that answer the brief, rather than by writing one paragraph per paper.
Use the academic finding cards to compare results. Consider whether differences
in design, sample, measurement, or context explain apparent conflicts.
Distinguish a gap supported by the reviewed literature from a topic that was
not searched or was inaccessible.

Do not impose a fixed number of studies, a publication cutoff, or a claim of
consensus unless the brief or an appropriate review protocol justifies it.
Treat papers from the same underlying dataset, trial, or result as one
provenance cluster, following the parent skill's provenance rule.

### 4. Research-question cards

When question design is part of the task, generate candidates from supported
findings, explicit limitations, and verified gaps. Each card should contain:

- the question, narrow enough to be answerable;
- the `F#` finding or limitation and linked `E#` evidence that motivates it;
- constructs, population, context, and time period;
- a plausible method and data requirement, if requested;
- what would count as an informative answer or disconfirmation;
- feasibility risks and competing explanations;
- a note that novelty or impact remains provisional until checked against the
  relevant literature and constraints.

Questions are proposals, not findings. Do not treat a question generated from
an unsupported summary as evidence.

### 5. Thesis-oriented critique

When the user asks for thesis mentoring, give a bounded diagnosis. Distinguish:

- a gap supported by the reviewed literature;
- a gap suggested by a limitation or context boundary;
- a gap that is only a hypothesis for further searching;
- methodological, theoretical, data, and practical contributions.

Only formulate a testable hypothesis when its constructs, direction (if
appropriate), population, and observable measures are explicit enough to test.
Ask the human when the thesis discipline, research paradigm, ethics process,
or institutional requirements could materially change the recommendation.

## Academic deliverables

Include only the stages and outputs the task needs. A single-paper task may
need an orientation map and `F#` cards; include open questions when requested
or useful to the question. A literature review may need thematic synthesis. A
research-question task may need question cards; thesis mentoring may need a
bounded gap and contribution diagnosis. Store stage material in the existing
`working` or `audit` records as appropriate. The parent skill governs evidence
requirements, retention, and final presentation; do not duplicate its claim
matrix, `E#` records, source ledger, search record, or stop rationale here.
