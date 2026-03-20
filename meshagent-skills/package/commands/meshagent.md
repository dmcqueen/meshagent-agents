---
description: General MeshAgent CLI operator. Route a request to the right meshagent subcommand and execute it safely.
argument-hint: "<goal, room, service, project, or meshagent command>"
---

# /meshagent

Use this command for any request that involves the MeshAgent CLI.

## Workflow

1. Start with [SKILL.md](../skills/meshagent-cli-operator/SKILL.md).
2. Use [SKILL.md](../skills/meshagent-mail-operator/SKILL.md) for contact forms, email delivery, mailboxes, inbox evidence, or MailBot toolkits.
3. Use [SKILL.md](../skills/meshagent-scheduling-operator/SKILL.md) for scheduled tasks, cron-based dispatch, or queue scheduling.
4. Use [SKILL.md](../skills/meshagent-webmaster-operator/SKILL.md) for websites, webservers, routes, domains, or public URL exposure.
5. Pick the narrowest MeshAgent command path that fits the request.
6. If flags or subcommands are unclear, check [meshagent_cli_help.md](../skills/meshagent-cli-operator/references/meshagent_cli_help.md) first. Only run live `meshagent <path> --help` when the packaged reference is missing the needed detail or appears stale for the installed CLI.
7. Prefer inspection before mutation.
8. After any change, verify with the corresponding `show`, `list`, or read command.

## Coverage

This command is the generic entrypoint for:
- auth and setup
- projects, api keys, secrets, routes, webhooks, mailboxes, and scheduled tasks
- rooms, room APIs, ports, sessions, calls, and participant tokens
- services, MCP bridges, webservers, and helper services
- chatbot, worker, task-runner, mailbot, voicebot, process, codex, multi, and meeting-transcriber flows
