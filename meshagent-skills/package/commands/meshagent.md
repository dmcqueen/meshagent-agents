---
description: General MeshAgent CLI operator. Route a request to the right meshagent subcommand and execute it safely.
argument-hint: "<goal, room, service, project, or meshagent command>"
---

# /meshagent

Use this command for any request that involves the MeshAgent CLI.

## Workflow

1. Start with [SKILL.md](../skills/meshagent-cli-operator/SKILL.md).
2. Use [SKILL.md](../skills/meshagent-webapp-backend-builder/SKILL.md) for website and handler implementation, DB-backed contact forms, and mailbox-backed webapp backends.
3. Use [SKILL.md](../skills/meshagent-webapp-dev-operator/SKILL.md) when a room-hosted webapp backend must hot-reload in a dev loop.
4. Use [SKILL.md](../skills/meshagent-webapp-release-operator/SKILL.md) when a room-hosted webapp should become an image-backed release candidate or release.
5. Use [SKILL.md](../skills/meshagent-mail-operator/SKILL.md) for email delivery, mailboxes, inbox evidence, or MailBot toolkits.
6. Use [SKILL.md](../skills/meshagent-scheduler/SKILL.md) for scheduled tasks, cron-based dispatch, or queue scheduling.
7. Use [SKILL.md](../skills/meshagent-webmaster/SKILL.md) for explicit route or domain administration and public hostname diagnostics.
8. Pick the narrowest MeshAgent command path that fits the request.
9. If flags or subcommands are unclear, check [meshagent_cli_help.md](../skills/meshagent-cli-operator/references/meshagent_cli_help.md) first. Only run live `meshagent <path> --help` when the packaged reference is missing the needed detail or appears stale for the installed CLI.
10. Prefer inspection before mutation.
11. After any change, verify with the corresponding `show`, `list`, or read command.
12. For contact-form website requests, do not treat a live site with failing outbound email as complete. Follow the mailbox-backed sender workflow before replying unless an actual permission blocker stops it.
13. For website requests, require at least one live HTTP smoke test after deploy before replying with success.

## Coverage

This command is the generic entrypoint for:
- auth and setup
- projects, api keys, secrets, routes, webhooks, mailboxes, and scheduled tasks
- rooms, room APIs, ports, sessions, calls, and participant tokens
- services, MCP bridges, webservers, and helper services
- chatbot, worker, task-runner, mailbot, voicebot, process, codex, and meeting-transcriber flows
