# Convene the advisors

Spawn five advisors in parallel. The script has prefilled an individual
assignment file for each advisor with the perspective, full analysis prompt,
input path, and a marked response section. The generated files are editable:
tailor a perspective or instruction for this discussion before dispatch when
useful. Keep the five perspectives distinct and provide the same
`01-brief/brief.md` to each advisor.

Assign one file to each advisor:

```text
02-advisors/contrarian.md
02-advisors/first-principles.md
02-advisors/expansionist.md
02-advisors/outsider.md
02-advisors/executor.md
```

Give each advisor the exact path to its file. Tell it to read only that
assignment and the general brief named there, and to write only between the
response markers in its own file, preserving the assignment text. It should
return a brief completion confirmation without duplicating its response in the
handoff. Advisors may conduct focused external research because their
assignment permits it; they should research only material factual gaps that
could change the conclusion and cite material sourced claims.

If an advisor fails or writes an unusable response, assign a fresh agent the
same mission with the same permitted inputs and file. The replacement updates
only the response section in that file. Do not advance until all five response
sections are usable; if replacement is unavailable, report the council as
incomplete.

After checking the five response sections, run:

```bash
python3 agent-skills/skills/llm-council/scripts/discussion.py check <discussion-dir> --through advisors
```
