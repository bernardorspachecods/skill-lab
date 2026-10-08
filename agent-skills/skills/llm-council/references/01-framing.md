# Frame the question

Read the task-relevant context, then prepare one neutral brief for the council.

1. Capture the user's core question or decision and the context they supplied.
2. Inspect workspace material only when it directly informs the question, its
   constraints, or relevant prior decisions. Record the source paths in the
   brief so the coordinator can trace the context.
3. Include the stakes and relevant constraints when they are known. Distinguish
   facts from assumptions. If relevant sources conflict or may be stale, state
   the conflict instead of silently resolving it.
4. Save the framed question and necessary context in
   `01-brief/brief.md`. Keep it neutral and specific enough for all five
   advisors to answer independently.
5. After approval and a passing brief gate, pass the same brief to all five
   advisors. Do not add an advisor's perspective or another agent's output to
   the brief.

## Mandatory user checkpoint

After completing the brief, give the user a link to `01-brief/brief.md` and ask
them to read it and approve it or request changes. Do not paste the brief into
chat. Wait for the user's response. Do not start the advisor phase until the
user approves the brief. If the user requests changes, update
`01-brief/brief.md`, link the revised file, and wait for approval of that
version.

After explicit approval, record it in the brief's frontmatter for the current
version:

```bash
python3 agent-skills/skills/llm-council/scripts/discussion.py approve-brief <discussion-dir>
```

Then run the brief gate:

```bash
python3 agent-skills/skills/llm-council/scripts/discussion.py check <discussion-dir> --through brief
```

The gate requires matching approval metadata in the brief frontmatter. If the
brief body changes later, its approval becomes stale; link the revised file,
ask the user to review it, and record approval again before continuing.

Use `$brainstorm` for guidance about the discussion with the user. 

## Brief format

Keep the sections distinct. Put established facts, constraints, and sourced
context in `Context`. Use `Assumptions and unresolved context` only for
material uncertainties, assumptions, or open questions that could affect the
council's analysis and are not already stated above. Do not repeat the task
scope, context, or stakes in that section. If no such items remain, write
`None identified`.
