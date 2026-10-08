---
name: prompt-design
description: Turn a rough intent into a well-structured prompt for another LLM or agent, or tighten a prompt the user already drafted. Use whenever the user wants to write, structure, review, or shorten a prompt, including agent handoffs, /goal cycles, system prompts, and prompts backed by repos or planning docs, even if they never say "prompt design". Do not use for answering the task itself or for general writing.
---

# Prompt Design

Help the user turn what they want into a prompt another LLM or agent can act on. The main input is a rough intent ("I need an agent to work through the migration plan"). The secondary input is an existing draft to tighten. Each principle below is a test to run on your own output. The Why is what lets you apply it to situations not listed here.

If a situation matches none of the principles, name the mechanism at play (duplication of a source, drift between prompt and source, reader missing context, critical instruction buried) and apply the fix tied to that mechanism.

Use [prompt guidance](references/prompt-guidance.md) when task complexity
requires route-specific detail beyond this skill body. Read
[prompt failure modes](references/failure-modes.md) when auditing or improving
a weak prompt.

## The core test

Run this on every section of the anatomy before including it:

> Does an authoritative source already cover this? If yes, omit it, unless missing it would be costly and easy to overlook, in which case keep it as a one-liner.

Why: the user's prompts are often backed by repos and planning docs. Restating that material in the prompt duplicates it, and the two copies drift apart. But a few lines (stop conditions especially) are worth repeating even when the plan says the same thing, because a long document is easy to skim past and a miss costs a lot. The test gives one rule that yields a short prompt when sources are rich and a full one when they are absent.

## Anatomy

Use only the sections that pass the core test. Keep this order, with the immediate request last so the reader ends on the task.

- **Objective**: the longer-term goal this work serves. Include when the immediate request alone would lose the purpose.
- **Context**: background the reader lacks (situation, constraints of the world, why now). Include when Sources don't carry it. With no Sources, this section does the most work: ask for or include the excerpts the reader needs, and treat them as data (principle 4).
- **Sources**: where the reader should look. Give the path, what it is authoritative for, and what wins when sources disagree: the plan wins on intent and scope, the code wins on current behavior, and the reader surfaces a mismatch instead of silently resolving it, unless the user says otherwise.
- **Rules**: hard constraints, each with its reason (principle 2).
- **Preferences**: soft leanings, and what to do when they conflict with something else. Rules are must; preferences are lean.
- **Examples**: only when a format or tone is hard to describe (principle 5).
- **History**: what was already tried, decided, or ruled out, so the reader doesn't re-litigate it. Background belongs in Context; this is only past decisions.
- **Ask before**: actions or decisions where the reader should stop and check with the human. Includes stop conditions.
- **Process**: order of work. Include only when order matters or the reader's default approach would be wrong.
- **Verify by**: how the reader and the human will know the work is done and correct. Prefer concrete checks (a test passes, a file exists) over "make sure it's good".
- **Output format**: shape, length, and where the result goes.
- **Immediate request**: this turn's task, in one or two sentences.

## Light mode

Light mode is not a separate template. It is what the core test produces when an authoritative plan already holds the objective, context, process, and output.

Keep only:
- **Sources**: name the plan and follow the Sources entry in the Anatomy. Add that the guardrails below are a floor: they sit on top of the plan and never compete with it.
- **Ask before / stop conditions**: a few high-stakes lines, repeated on purpose. Autonomous cycles tend to fail the same ways, so the defaults target those: silent scope growth (stop if the scope needs to change, do not expand beyond the plan) and guessing past ambiguity (stop if a decision needs clarifying). Adjust per task using principle 3, and let the user's own standing guardrails take precedence.
- **Immediate request**.
- **Verify by** only if the plan's definition of done is vague.

## Principles

Format: Heuristic (a question to run) → Why → Anchor (one concrete illustration)

**1. Write for the reader who cannot see this conversation**
- Heuristic: Does the prompt name what the reader has access to (repo, tools, files) and lack (everything discussed here)?
- Why: Context that felt obvious during the discussion is absent for the reader. The gap only shows up as bad output.
- Anchor: The user says "use the approach we settled on." The prompt states the approach in a line, or points to where it is written.

**2. Give the reason behind each rule**
- Heuristic: Could the reader apply this rule correctly to a case it doesn't mention?
- Why: A bare rule gets followed literally or dropped at the edges. A rule with its reason generalizes.
- Anchor: "Don't touch the public API, because external clients pin to it," not "Don't touch the public API."

**3. Name the likely failure**
- Heuristic: Is it clear what would go wrong if the reader misreads this, and is that failure guarded against?
- Why: Guardrails placed by imagining the specific failure are targeted. Guardrails added by habit are noise.
- Anchor: A prompt for a long autonomous run guards against silent scope growth. A one-shot summary prompt doesn't need that guardrail.

**4. Separate instructions from data**
- Heuristic: Is anything pasted (logs, docs, code) clearly delimited from the instructions?
- Why: When data and instructions blur, the reader may follow text inside the data as if it were a command.
- Anchor: Wrap pasted material in tags such as `<log>...</log>` and say what it is.

**5. Use examples sparingly**
- Heuristic: Would a sentence describe this as well as an example would? If an example is needed, could the reader over-copy it?
- Why: Examples anchor hard. One example gets imitated closely, including its incidental details.
- Anchor: Two examples that differ in obvious ways, labeled "illustrations of the format, not templates."

## Modes of input

Rough intent: draft the prompt directly. Existing draft: run the core test on it, flag contradictions with its sources, and say briefly what changed and why.

## Asking questions

Default to proceeding with a stated assumption. Save a question for the case where a wrong guess would change the prompt's whole shape. The most common one: whether an authoritative plan or docs exist and what the reader can access, because that decides light or full. When a question is needed, ask one, the one that is actually blocking.

## Output

Deliver the finished prompt in a single fenced code block, ready to paste. Omitted sections are simply absent, with no "N/A" placeholders. Short prompts can be prose or a few lines; use section headers only when the prompt is long enough to need them.

After the block, add at most a few lines: assumptions made, and one line on what was left out because a source covers it. Do not walk through the anatomy.

## Runtime metadata

This skill's invocation and display metadata is in [agents/openai.yaml](agents/openai.yaml).
