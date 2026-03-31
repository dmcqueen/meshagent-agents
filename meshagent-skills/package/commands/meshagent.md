---
description: General MeshAgent CLI operator. Route a request to the right meshagent subcommand and execute it safely.
argument-hint: "<goal, room, service, project, or meshagent command>"
---

# /meshagent

Use this command for any request that involves the MeshAgent CLI.

## Workflow

1. Start with [SKILL.md](../skills/meshagent-cli-operator/SKILL.md).
2. Use [SKILL.md](../skills/meshagent-webapp-backend-builder/SKILL.md) for website and handler implementation, DB-backed contact forms, and mailbox-backed webapp backends.
3. Use [SKILL.md](../skills/meshagent-mail-operator/SKILL.md) for email delivery, mailboxes, inbox evidence, or MailBot toolkits.
4. Use [SKILL.md](../skills/meshagent-scheduler/SKILL.md) for scheduled tasks, cron-based dispatch, or queue scheduling.
5. Use [SKILL.md](../skills/meshagent-webmaster/SKILL.md) for explicit route or domain administration and public hostname diagnostics.
6. Pick the narrowest MeshAgent command path that fits the request.
7. If flags or subcommands are unclear, check [meshagent_cli_help.md](../skills/meshagent-cli-operator/references/meshagent_cli_help.md) first. Only run live `meshagent <path> --help` when the packaged reference is missing the needed detail or appears stale for the installed CLI.
8. Prefer inspection before mutation.
9. After any change, verify with the corresponding `show`, `list`, or read command.
10. For contact-form website requests, do not treat a live site with failing outbound email as complete. Follow the mailbox-backed sender workflow before replying unless an actual permission blocker stops it.
11. For website requests, require at least one live HTTP smoke test after deploy before replying with success.

## Coverage

This command is the generic entrypoint for:
- auth and setup
- projects, api keys, secrets, routes, webhooks, mailboxes, and scheduled tasks
- rooms, room APIs, ports, sessions, calls, and participant tokens
- services, MCP bridges, webservers, and helper services
- chatbot, worker, task-runner, mailbot, voicebot, process, codex, and meeting-transcriber flows
