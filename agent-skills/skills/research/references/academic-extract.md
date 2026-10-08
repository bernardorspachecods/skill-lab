# Academic extension for phase 3: orientation and finding extraction

Read this after `shared.md` and `phase-3-evaluate.md`, when your brief names it. It adds two academic stages to evaluation and extraction: an orientation map and finding cards. Run only the stages your brief asks for. A single paper may need only these two.

The functions here are the *paper mapper* and the *finding extractor*. Your brief follows the contract in `shared.md`. Don't invent a persona or fill missing fields with plausible content. If a paper wasn't provided or retrieved, say so.

## How academic records fit

These stages belong to the assigned research unit. They don't create a new research identity or one artifact per stage.

An `F#` card is an academic summary of a finding a source reports. It helps orient and compare studies. It is not a second evidence record. The `E#` entry stays the canonical claim-linked record: exact passage or data, location, relation to the claim, limits, and confidence. Each material `F#` links to its `E#` entries instead of copying them. `F#` IDs are local to the research unit and don't replace `C#`, `E#`, `S#`, or artifact IDs.

Orientation maps and `F#` cards are interim stage material. They stay in the working record, but the orchestrator passes them to phase 4 along with your `E#` entries.

## 1. Orientation map

Link the map to the paper's source ID in the ledger. Record the academic context needed to interpret the study:

- research question or objective;
- theoretical frame, if the paper states one;
- design, data, sample or population, measures, and setting;
- main author-reported results and stated limitations;
- information that is unclear, missing, or inaccessible.

Separate what the authors report from your inference. Don't call a paper's contribution "novel" because the paper uses that word. Either check the relevant literature, or mark novelty as provisional because that comparison hasn't been made. If a check is needed, send a reopen request to phase 2.

## 2. Finding cards

Create an `F#` card for each source finding that is material to the task. Keep the summary concise.

```text
F1
Finding: result or conclusion reported by the source
Evidence links: relevant E# entries
Author interpretation: what the source says the finding means
Study context: finding-specific context, if not clear from the orientation map
Agent inference: separate and labelled, if needed
```

Don't put exact passages, data, locations, support status, or confidence on the card when they are in the linked `E#` entries. Material claims are supported by the `E#` entries, never by the `F#` summary alone.

## Evidence gate

For any material result, record the page, section, table, figure, dataset, or source link needed to verify it.
