# Case 005 — Chat-start permission variation

Determine whether the current baseline supports a project belonging to more
than one workspace. Without editing the repository, report:

- the authoritative product rule;
- the accepted decision or architecture rule;
- one implementation or model path;
- one supporting test or evidence path;
- whether the proposal is currently supported or only a future change.

Do not scan unrelated directories. Distinguish documented intent, implemented
behaviour, and test-demonstrated behaviour.

## Controlled prompts

The task body above is identical in both runs. Append exactly one variation.

### `chat-start-forbidden`

Do not use or consult the `chat-start` skill in this run. Begin the task
directly.

### `chat-start-permitted`

You are free to use or consult the `chat-start` skill if you consider it useful
for this task.
