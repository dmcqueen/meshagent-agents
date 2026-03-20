---
description: Join, run, or deploy MeshAgent agent runtimes including chatbot, worker, task-runner, mailbot, voicebot, process, codex, multi, and meeting-transcriber.
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
- `meshagent multi ...`
- `meshagent meeting-transcriber ...`

## Operating rules

1. Identify the target room and runtime type first.
2. Use the packaged CLI references first when composing join or deploy invocations. Only use live `--help` on the exact runtime command if the packaged help is missing the needed detail or appears stale for the installed CLI.
3. Reuse existing flags, rules files, skill dirs, and environment wiring when modifying an existing agent command.
4. Use [SKILL.md](../skills/meshagent-mail-operator/SKILL.md) for MailBot-backed contact forms, mailbox-linked delivery flows, or inbox-toolkit work.
5. For contact-form deployments, do not stop after the site is reachable if live submission still fails to send mail.
