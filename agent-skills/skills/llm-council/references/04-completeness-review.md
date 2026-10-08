# Completeness review

Assign an agent distinct from the chairman. The script has prefilled
`04-chairman/completeness-review.md` with the assignment, exact source paths,
review criteria, and a marked response section. Give the reviewer the exact
path and tell it to read only the files named there, use only response sections
from other agents' files, and write only between the response markers. It must
not rewrite or improve the recommendation. It returns a brief completion
confirmation without duplicating the audit in its handoff.

The generated assignment contains the review criteria and audit format; use it
as the source of truth. Check that the returned audit addresses that assignment
and ends with a clear status before advancing.

If the audit is unusable, assign a replacement the same sources, report,
assignment, and file. The replacement updates only the response section. If
replacement is unavailable, report the council as incomplete. If status is
`REVISE`, the chairman updates its own response section, the coordinator
publishes the report again, and the same reviewer rechecks the revised report
against the same source set, updating only its audit response section. Repeat
until it passes.

Before delivery, run:

```bash
python3 agent-skills/skills/llm-council/scripts/discussion.py check <discussion-dir> --through chairman
```
