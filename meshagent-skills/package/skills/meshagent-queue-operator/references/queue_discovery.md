# Queue Discovery

Use this reference when the user asks what queues are available in the current room or when the queue name is unknown.

## Preferred workflow

1. Prefer built-in CLI and toolkit invocation before writing any ad hoc SDK code.
2. First inspect the room toolkits:

```bash
meshagent room agent list-toolkits --room <ROOM_NAME>
```

3. If the room exposes the `queues` toolkit, list visible queues directly through the toolkit:

```bash
meshagent room agent invoke-tool \
  --room <ROOM_NAME> \
  --toolkit queues \
  --tool list \
  --timeout 0 \
  --arguments '{}'
```

4. Return the queue names and sizes from that tool output.
5. If the first command output is noisy, truncated, or mixed with progress lines, rerun the narrow `invoke-tool` command and extract the exact queue names before replying.
6. If the result contains no queues, say that the room currently has no visible queues rather than leaving the answer ambiguous.

## Interpretation rules

- Do not say queue listing is impossible just because `meshagent room queue` lacks a dedicated `list` subcommand.
- `meshagent room queue send`, `receive`, and `size` are specialized queue commands. `meshagent room agent invoke-tool` is the generic fallback when the CLI does not expose a dedicated queue-list command.
- If the `queues` toolkit is not visible from `list-toolkits`, explain that the room did not expose the toolkit to this caller instead of claiming queue listing is unsupported by MeshAgent.
- Do not stop at “the output was truncated” when the user asked for queue names. Rerun the narrow command, parse the result, and report the exact names or an explicit empty list.

## Only use SDK code as a fallback

- The room API supports `room.queues.list()`, but do not jump straight to writing Python just to answer “what queues are available?”
- Prefer SDK code only when the generic CLI toolkit invocation path is unavailable and the environment is known to have a working SDK/runtime combination.
