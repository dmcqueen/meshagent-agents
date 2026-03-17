# MeshAgent CLI command groups

Use this file to choose the narrowest MeshAgent CLI area before reading the full help reference.

Room-runtime default: when executing commands inside `meshagent/shell-codex:default`, prefer `/usr/bin/meshagent ...` and write user-visible artifacts under `/data`.

## Auth and setup

- `meshagent version`
- `meshagent setup`
- `meshagent auth ...`
- `meshagent project ...`
- `meshagent api-key ...`

Use for login, active project selection, and API key management.

## Project administration

- `meshagent secret ...`
- `meshagent webhook ...`
- `meshagent mailbox ...`
- `meshagent route ...`
- `meshagent scheduled-task ...`

Use for project-scoped configuration and external integrations.

## Service and deployment workflows

- `meshagent service ...`
- `meshagent mcp ...`
- `meshagent helper ...`
- `meshagent webserver ...`
- `meshagent codex ...`

Use for service specs, templates, deployment, service discovery, web serving, and Codex-backed runtime helpers.

## Room lifecycle and room APIs

- `meshagent rooms ...`
- `meshagent room agent ...`
- `meshagent room secret ...`
- `meshagent room queue ...`
- `meshagent room messaging ...`
- `meshagent room storage ...`
- `meshagent room service ...`
- `meshagent room developer ...`
- `meshagent room database ...`
- `meshagent room memory ...`
- `meshagent room container ...`
- `meshagent room sync ...`
- `meshagent port ...`

Use when the task is clearly scoped to a room or to resources that live inside a room.

## Agent runtime orchestration

- `meshagent chatbot ...`
- `meshagent worker ...`
- `meshagent task-runner ...`
- `meshagent mailbot ...`
- `meshagent voicebot ...`
- `meshagent process ...`
- `meshagent multi ...`
- `meshagent meeting-transcriber ...`
- `meshagent codex chatbot ...`
- `meshagent codex task-runner ...`
- `meshagent codex worker ...`

Use for join, run, and deploy flows for prebuilt MeshAgent runtimes.

## Inspection and diagnostics

- `meshagent session ...`
- `meshagent token ...`
- `meshagent call ...`
- `meshagent rooms ...`
- `meshagent room ...`
- `meshagent service show`
- `meshagent service list`

Use for discovery, verification, and troubleshooting before making changes.

## Notes

- `meshagent room ...` is the deepest public area. Use it for room-scoped agents, storage, messaging, services, database tables, memories, containers, and sync.
- The generated help reference also captures hidden aliases and locally available internal namespaces, including `meshagent test` when that command is present in the installed CLI.
- The help reference documents command names and flags. In this runtime, prefer `/usr/bin/meshagent` as the executable path.
- If the installed CLI version changes, rerun `scripts/refresh_cli_reference.sh`.
