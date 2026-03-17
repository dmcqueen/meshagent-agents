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
2. Use `--help` on the exact runtime command before composing long join or deploy invocations.
3. Reuse existing flags, rules files, skill dirs, and environment wiring when modifying an existing agent command.
