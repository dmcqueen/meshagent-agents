---
description: General MeshAgent CLI operator. Route a request to the right meshagent subcommand and execute it safely.
argument-hint: "<goal, room, service, project, or meshagent command>"
---

# /meshagent

Use this command for any request that involves the MeshAgent CLI.

## Workflow

1. Read [SKILL.md](../skills/meshagent-cli-operator/SKILL.md).
2. Pick the narrowest MeshAgent command path that fits the request.
3. If flags or subcommands are unclear, check [meshagent_cli_help.md](../skills/meshagent-cli-operator/references/meshagent_cli_help.md) or run `meshagent <path> --help`.
4. Prefer inspection before mutation.
5. After any change, verify with the corresponding `show`, `list`, or read command.

## Coverage

This command is the generic entrypoint for:
- auth and setup
- projects, api keys, secrets, routes, webhooks, mailboxes, and scheduled tasks
- rooms, room APIs, ports, sessions, calls, and participant tokens
- services, MCP bridges, webservers, and helper services
- chatbot, worker, task-runner, mailbot, voicebot, process, codex, multi, and meeting-transcriber flows
