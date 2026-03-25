# Process Agent Design

Use this reference when the requested runtime is one shared-identity agent that should be reachable through more than one entry path, such as chat, mail, queue, or toolkit calls.

## Use process when

- One agent should keep the same identity, rules, tools, memory, and thread model across several channels.
- Queue work is just one entry path into that same agent rather than a dedicated background-only worker identity.
- The requested design sounds like one agent that should handle chat, email, scheduled work, and/or toolkit calls together.

## Core model

- Use `meshagent process` for shared-identity agent designs.
- Use `meshagent process spec` before freehanding service YAML for that shape.
- For new authored YAML that needs queue handling plus mail or other channels, treat `meshagent process` as the default runtime shape.
- Assume current rooms are not legacy unless the user or observed room state proves otherwise.
- Add channels explicitly with repeated `--channel` flags such as:
  - `--channel=chat`
  - `--channel=mail:<MAILBOX_ADDRESS>`
  - `--channel=queue:<QUEUE_NAME>`
  - `--channel=toolkit:<TOOLKIT_NAME>`
- Use durable `--room-rules` or mounted rule files when the agent must keep stable behavior across those channels.

## Good design anchors

- Treat `examples/cli/process-news-agent/meshagent.yaml` as the primary packaged example for a process agent with chat, mail, and queue channels.
- Treat `meshagent-router/meshagent/router/templates/assistant.yaml` as the primary service-template example for a process room assistant.

## Queue-specific cautions

- A queue channel such as `--channel=queue:<QUEUE_NAME>` is an entry path, not proof by itself that the runtime is the right consumer for the business workflow.
- The scheduled task queue, queue channel, startup command, and surrounding runtime behavior must still line up.
- For new authored YAML, a process queue channel is the default shape. Use a dedicated `meshagent worker` only when the user explicitly asked for that runtime shape.

## Scheduling guidance

- For scheduled tasks targeting a process agent, make the scheduled payload match how the process agent was authored.
- If the process agent uses durable workflow rules, prefer a prompt that tells it to run that established workflow.
- Do not assume that queue wiring alone proves the process agent will perform the requested external action.
