---
name: llm-structuring
description: Use this skill when writing, reviewing, or troubleshooting instructions, prompts, or documentation intended for an LLM to read and act on. Trigger on: drafting or reviewing a skill, prompt, or instruction set for a model; deciding what to emphasize or how to phrase a rule for LLM consumption; an instruction isn't being followed reliably and the cause is unclear; structuring how one model or agent hands context to another.
---

# LLM Structuring

Help make structural and framing decisions when writing anything an LLM must read and act on. Focus on judgment in novel situations, not pre-mapped cases.

Run the four questions below against the draft. Where one exposes a problem, apply its fix. If none matches the situation, use the procedure under "Cases none of the heuristics name."

Each cluster has a Heuristic (a question to run), a Why, and an Anchor (one concrete illustration); some add a note.

## A. Positioning and weighting

**Heuristic:** Is the most important information positioned to survive attention drop-off (start or end, not buried mid-document), and is its relative importance stated explicitly rather than implied by tone?

**Why:** Position can affect what gets noticed and followed, especially in long contexts. Hedged phrasing can blur priority: a soft "it'd be great if..." may be read as a preference rather than the requirement the author meant. If content could be truncated or only partially attended to, the important part should already have landed: put the instruction or conclusion at the start or end, not in the middle of narrative build-up.

**Anchor:** A non-negotiable rule in paragraph 4 of 7, phrased as "it'd be great if...", is weaker on both counts than the same rule stated as "must," placed up top, and reinforced as the closing line.

**Watch-out:** Recency cuts both ways. In long sessions, later turns can silently override earlier rules. The mechanism that helps when placed deliberately hurts when left unaccounted for. If an earlier constraint must stay active, restate it.

## B. Signal density

**Heuristic:** Does every sentence and every example pull its own weight, or does volume (extra context, an exhaustive edge-case list) dilute the core ask?

**Why:** Attention is a limited resource. Exhaustive edge-case lists tend to encourage literal matching on the listed cases and can do worse on anything unlisted. A few well-chosen examples often generalize better than many cases in dense prose, provided they cover the meaningful differences.

**Anchor:** Ten paragraphs of backstory, or 15 listed edge cases, can be weighted as heavily as the one sentence that mattered. A handful of well-chosen cases can communicate the pattern better than a long catalog.

**Boundary with A:** Deliberately restating a critical constraint (a closing line, a restatement in a long session) is reinforcement, not dilution. Cut redundancy that carries no priority signal.

## C. Concreteness and format consistency

**Heuristic:** Is the instruction anchored with a concrete example, formatted with clear structure (headers, delimiters), phrased the same way every time it repeats, and explained where the reader must apply it beyond the example?

**Why:** Concrete anchors tend to generalize better than descriptive rules alone, but a single example can be copied too literally, so mark it as illustrative or vary it. Clear structure helps a reader locate and follow each part of an instruction, beyond aesthetics. Consistent phrasing is more reliable than stylistically varied restatements of the same idea. State the reason behind a rule when the reader must apply it to cases the examples do not cover: the reason is a transferable principle.

**Anchor:** Restating a constraint five different ways for "good writing" can be worse than repeating the same sentence verbatim, with one worked example marked as illustrative.

## D. Conflict resolution

**Heuristic:** When instructions of equal authority conflict, is there a stated tie-breaker (for example: specificity beats generality, recency beats primacy, explicit beats implied), or is the model left to guess which one wins?

**Why:** Unstated conflicts do not announce themselves. The model picks one silently, often not the one the author intended, so the outcome depends on model idiosyncrasy instead of design. Conflicts across authority levels (system, developer, user) are outside these tie-breakers: flag them and defer to the applicable instruction hierarchy.

**Anchor:** In a document that gets added to over time, an early heuristic and a later addition can contradict each other without anyone noticing until behavior gets strange.

## Cases none of the heuristics name

When nothing above directly matches, do not scan for the closest-sounding anchor.

1. Name the mechanism actually at play (placement or weighting, dilution, ambiguity or format, or conflict), not the surface topic of the new situation.
2. Apply the fix tied to that mechanism, even though the situation appears in no anchor.

Surface matching produces confident but wrong extrapolation. The Why is what licenses reasoning past the listed anchors.

**Anchor:** In a handoff where agent 2 only sees a summary of agent 1's work, surface matching might reach for B ("multiple pieces of info, so trim it"). The mechanism is A's: agent 2 never sees the original context, so whatever it needs must survive as an explicit, prominent statement at the start or end of the handoff.

## Failure-mode flags

Recognize these; do not restructure around them by default.

- **Sycophancy / premise agreement:** Models tend to accept a stated framing unless told to verify it independently.
- **Negation blindness:** A prohibition can prime the behavior it names, and nested exceptions are easy to drop. Prefer flat statements: "Do X. Exception: if Y, do Z."
- **Exception-clause erosion:** Nested conditionals lose exceptions. Enumerate exceptions flatly.
- **Verbosity/confidence bias:** Longer, more assertive output tends to be rated higher even when it is not better. Request terse output explicitly, and more than once.

## Guardrail

This skill governs how information is structured and framed. When a person's phrasing works against how an LLM reads, change the wording, not the request. Legitimate direction from a user or developer stays intact.
