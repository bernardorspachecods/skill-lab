---
name: llm-council
description: Run a structured council of five independent advisors, five peer reviewers, and a chairman when the user explicitly invokes the council. Do not use for ordinary questions or decisions without an explicit request.
---

# LLM Council

Run the full five-advisor, five-reviewer, chairman workflow only when the user
explicitly invokes this skill. Read `$brainstorm` for guidance on handling the
discussion with the user; this skill does not duplicate that guidance.

## Shared workflow contract

- Keep each council run under `discussions/<discussion name>/`, beside `plans/`.
  These artifacts are version-controlled.
- Use the discussion script to create the complete run folder and all output
  scaffolds, prepare the anonymized reviewer packet, and check phase gates. The
  script does not launch agents or enforce per-agent filesystem boundaries.
- The coordinator owns the general brief, anonymized packet, advisor key, and
  phase gates. The script prepopulates each agent's individual brief file with
  its assignment and a marked response section. The coordinator may edit a
  generated assignment file before dispatch to tailor that run's perspective
  or instructions. Each agent reads only the files named in its assignment and
  writes only between the response markers in that same file. Agents may
  conduct external research only when their assignment allows it. Do not give
  agents broad access instructions to scan the discussion folder or unrelated
  workspace files. The coordinator checks agent-written response sections but
  does not copy, edit, or rewrite them; route unusable work to the assigned
  agent or a replacement.
- The user must approve the complete council brief before advisors are
  dispatched. Link the brief file and ask the user to read and approve it or
  request changes; do not paste its contents into chat. Wait for explicit
  approval and record it in the brief frontmatter for that exact version with
  `discussion.py approve-brief`. Any later brief edit invalidates that
  approval; link the revised file and get approval again before continuing.
  Every phase gate checks that approval matches the current brief.
- Keep each phase's full source artifacts in that phase folder. Pass only the
  explicit handoff packet to the next phase. Give agents read access only to
  the specific source files authorized for their assignment and write access
  only to their designated output file. Folder separation supports this
  boundary but does not technically enforce it.
- If an agent fails or returns unusable work, assign a fresh agent the same
  mission with the same permitted inputs. Do not give it other agents' outputs
  unless that phase's input contract allows them. Have the replacement update
  only the response section in the same assigned file. Do not advance until the
  required response is usable; if replacement is unavailable, report the
  council as incomplete.
- Scope workspace context to material that directly informs the question,
  its constraints, or relevant prior decisions. Do not scan unrelated files.
- Use the full workflow for every council session. Do not skip a phase.

## Run sequence

Create a discussion folder and all phase files with
[`scripts/discussion.py`](scripts/discussion.py):

```bash
python3 agent-skills/skills/llm-council/scripts/discussion.py init "<discussion name>"
```

This creates `discussions/<discussion name>/` with the approved-brief file,
five advisor assignment files, an anonymized-packet scaffold and five reviewer
assignment files, chairman and completeness-review assignments, an advisor-key
scaffold, and a `results.md` scaffold. Choose a name without path separators.
If that discussion folder already exists, initialization stops without
overwriting it; choose a distinct name.

Then load each phase guide only when the coordinator reaches that phase. In
Phase 1, complete the brief, link it for the user to read, wait for explicit
approval, record it in the brief frontmatter, and pass the brief gate before dispatching advisors. The
coordinator fills coordinator-owned artifacts and generated packets. Give each
agent the exact path to its prepopulated assignment file and tell it to write
only between that file's response markers, leaving the assignment intact. It
should return a brief completion confirmation, not duplicate the artifact in
its handoff. The coordinator checks the response section before advancing.
After the chairman writes `04-chairman/chairman.md`, run
`discussion.py publish-report <discussion-dir>` to publish the report to
root-level `results.md` for the completeness reviewer and final delivery.

| Order | Phase | Guide | Main output |
|---|---|---|---|
| 1 | Frame the question and get user approval | [Framing](references/01-framing.md) | `01-brief/brief.md` with approval metadata in its frontmatter |
| 2 | Convene five advisors | [Advisors](references/02-advisors.md) | Five assignment-and-response files in `02-advisors/` |
| 3 | Peer review | [Peer review](references/03-peer-review.md) | Anonymized packet and five assignment-and-response files in `03-peer-review/` |
| 4 | Synthesis, completeness review, and delivery | [Chairman](references/04-chairman.md), then [completeness review](references/04-completeness-review.md) | Chairman and audit assignment-and-response files in `04-chairman/`; published `results.md` at the discussion root; then link the report in chat |

After each production phase, run the script's `check` command for that gate.
In Phase 4, link `results.md` at the discussion root in chat only after the
completeness review passes. The report should stand on its own; the chat handoff
can briefly introduce it without repeating the report.

## Runtime metadata

Invocation and display metadata is in [agents/openai.yaml](agents/openai.yaml).
