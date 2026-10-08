# Chairman report

After all five advisor responses and peer reviews are complete, assign one
chairman. The script has prefilled `04-chairman/chairman.md` with the full
assignment, source paths, report requirements, and a marked response section.
The generated assignment is editable before dispatch. Give the chairman the
exact path and tell it to read only the files listed in that assignment and
write only between its response markers. It returns a brief completion
confirmation without duplicating the report in its handoff.

The chairman file contains the response to the assignment, while the report
users read remains at the discussion root. After the chairman completes its
response section, publish it to `results.md` with:

```bash
python3 agent-skills/skills/llm-council/scripts/discussion.py publish-report <discussion-dir>
```

This extracts the report section without assignment instructions or markers.
Each run replaces the discussion-root `results.md` with the current chairman
response. Edit the chairman response and rerun this command to publish a
revision; do not edit `results.md` as the source copy.
Then assign an agent distinct from the chairman to perform the completeness
review in [`04-completeness-review.md`](04-completeness-review.md). Do not
deliver the report until that review passes.

If the completeness review returns `REVISE`, send the findings to the same
chairman and have it update only the response section in
`04-chairman/chairman.md`. Run `publish-report` again, then have the same
completeness reviewer recheck the revised `results.md` against the same source
set, updating only its response section in
`04-chairman/completeness-review.md`. The coordinator checks both response
sections but does not edit them.

After the completeness review passes, run:

```bash
python3 agent-skills/skills/llm-council/scripts/discussion.py check <discussion-dir> --through chairman
```

Then post a chat handoff with a link to the discussion-root `results.md`. The
report is the full result; do not paste a second, divergent version into chat.
