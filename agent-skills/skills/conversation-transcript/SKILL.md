---
name: conversation-transcript
description: Clean exported Codex session files into a user-assistant transcript, optionally retaining a compact activity trail. Use when asked to remove session artifacts or preserve an audit trail; do not use to summarize or rewrite the conversation.
---

# Conversation transcript

Keep user and assistant messages verbatim and in their original order. Remove activity artifacts unless the user selects the activity mode.

Choose a mode from the request. If the user has not specified one, ask: “Which mode should I use: `messages-only` or `messages-and-activity`?” Wait for the answer before editing.

- **`messages-only`**: keep only user and assistant messages with speaker headings. Remove activity logs, tool calls, command output, and other artifacts.
- **`messages-and-activity`**: keep the messages and a concise activity trail showing files read or searched, relevant commands, exact web search queries, and agents started. Keep completion or interruption status when recorded. Drop bulky outputs that do not help identify the work.

Run the [transcript cleaner](scripts/clean_transcript.py) with the selected mode. In `messages-and-activity`, merge consecutive activity sections into one `## Activity` block. Add category headings such as `### Commands and file reads` or `### Web searches` only when that category appears, in the order its events occur. Start a new activity block after each user or assistant message.

The cleaner preserves only information present in the session. It keeps commands and web queries in their recorded form, marks searches whose query is missing, and preserves agent start, completion, or interruption events. It drops command output and other artifacts.

Run `python3 scripts/clean_transcript.py INPUT --mode MODE`. Use `--output PATH` to write a separate file, `--in-place` to replace the source, or `--rename` when the user asks to rename it. The rename mode uses `codex-trancript-{number}.md`; pass `--rename-number N` when the user supplies a number, or let the script choose the lowest unused positive integer, starting at `1`.
