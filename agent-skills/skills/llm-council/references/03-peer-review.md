# Peer review

After all five advisor response sections are complete, create the anonymized
review packet:

```bash
python3 agent-skills/skills/llm-council/scripts/discussion.py prepare-review <discussion-dir>
```

The script extracts only each advisor's response section, randomizes labels A
through E, and combines the responses with the council brief in
`03-peer-review/anonymized-responses.md`. It writes the advisor-to-label key to
`04-chairman/advisor-key.md`; never provide that key to a reviewer. Instructions
and perspective text from advisor files are excluded from the packet.

The script fills only the untouched packet and key scaffolds created by
`init`. If either file has been edited, it refuses to replace them; inspect the
existing files and preserve any needed content before deciding how to proceed.

Spawn five independent reviewers in parallel. Each reviewer's prefilled file
contains its assignment, the common review prompt, the packet path, and a
marked response section. Assign one file to each reviewer:

```text
03-peer-review/reviewer-01.md
03-peer-review/reviewer-02.md
03-peer-review/reviewer-03.md
03-peer-review/reviewer-04.md
03-peer-review/reviewer-05.md
```

Give each reviewer the exact path to its file. Tell it to read only that
assignment and the anonymized packet, and to write only between the response
markers in its own file, preserving the assignment text. Do not assign
reviewer personas or let reviewers see one another's work. Anonymization hides
labels and names; distinctive arguments may still make an advisor's identity
guessable. Each review must answer the three questions in its file and stay
under 200 words. The reviewer returns a brief completion confirmation without
duplicating its review in the handoff.

If a reviewer fails or returns unusable work, assign a replacement the same
packet, prompt, and file. The replacement updates only the response section.
Do not give it another review or another reviewer's work. If replacement is
unavailable, report the council as incomplete.

After checking all five response sections, run:

```bash
python3 agent-skills/skills/llm-council/scripts/discussion.py check <discussion-dir> --through review
```
