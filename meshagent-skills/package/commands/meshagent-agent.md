---
description: Join, run, or deploy MeshAgent agent runtimes including chatbot, worker, task-runner, mailbot, voicebot, process, codex, and meeting-transcriber.
argument-hint: "<agent runtime task>"
---

# /meshagent-agent

Use this command for agent runtime orchestration.

## Primary command groups

- `meshagent chatbot ...`
- `meshagent worker ...`
- `meshagent task-runner ...`
- `meshagent mailbot ...`
- `meshagent voicebot ...`
- `meshagent process ...`
- `meshagent codex ...`
- `meshagent meeting-transcriber ...`

## Operating rules

1. Identify the target room and runtime type first.
2. Use the packaged CLI references first when composing join or deploy invocations. Only use live `--help` on the exact runtime command if the packaged help is missing the needed detail or appears stale for the installed CLI.
3. Reuse existing flags, rules files, skill dirs, and environment wiring when modifying an existing agent command.
4. Use [SKILL.md](../skills/meshagent-webapp-builder/SKILL.md) for contact forms, room-hosted web apps, and web handler implementation.
5. Use [SKILL.md](../skills/meshagent-mail-operator/SKILL.md) for mailbox-linked delivery flows or inbox-toolkit work.
6. For contact-form deployments, do not stop after the site is reachable if live submission still fails to send mail.
7. For webserver-backed deployments, do not stop after deploy until the live route has been smoke-tested.
