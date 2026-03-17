---
name: meshagent-cli-operator
description: Operate the MeshAgent CLI end to end. Use this skill whenever the user asks to authenticate, inspect, create, update, deploy, or troubleshoot anything with meshagent or meshagent-cli, including projects, api keys, secrets, webhooks, routes, mailboxes, scheduled tasks, rooms, room data, services, MCP bridges, ports, sessions, calls, tokens, or agent runtimes such as chatbot, worker, task-runner, mailbot, voicebot, process, codex, multi, and meeting-transcriber.
---

# MeshAgent CLI Operator

Use this skill for any task that should be completed with the MeshAgent CLI.

## Runtime assumptions

This skill assumes it is running inside a MeshAgent room container based on `meshagent/shell-codex:default`.

- The MeshAgent CLI is expected at `/usr/bin/meshagent`.
- `meshagent` on `PATH` is an acceptable fallback.
- The user-visible room filesystem is mounted at `/data`.
- To create or modify files the user should see, write them under `/data` and report paths relative to `/data`.
- Do not assume a repo-local virtualenv or checkout exists inside the container.
- Do not install packages into `/data`.

## Quick start

1. Resolve the CLI binary.
2. Identify the narrowest command path that matches the request.
3. If flags are uncertain, consult `references/command_groups.md`, then `references/meshagent_cli_help.md`, or run `meshagent <path> --help`.
4. Prefer read-only inspection before mutation.
5. After a change, verify the result with the corresponding read command.

## Resolve the CLI

Prefer these paths in order:

1. `/usr/bin/meshagent`
2. `meshagent`

If neither exists, stop and report that the MeshAgent CLI is unavailable.

## Command routing

Start with `references/command_groups.md` to choose the right area:

- auth and setup
- project administration
- service and deployment workflows
- room lifecycle and room APIs
- agent runtime orchestration
- inspection and diagnostics

Use `references/meshagent_cli_help.md` for the exact installed command tree and flags.

## Operating rules

- Scope the target first: project, room, service, participant, route, secret, or agent.
- Prefer the smallest command path that can complete the task.
- Use `--help` on the exact subcommand before composing long invocations.
- When executing commands in this runtime, prefer `/usr/bin/meshagent ...` so command examples match the container image.
- Treat `/data` as the writable user-visible workspace. If a command writes files for the user, keep them under `/data`.
- Do not expose secret values unless the user explicitly asks for them.
- Treat delete and overwrite operations as destructive. Confirm the target and blast radius before executing them.
- After create, update, deploy, or delete, run the appropriate verification command and summarize the resulting state.

## Bundled resources

- `references/command_groups.md`: fast routing map for the CLI.
- `references/meshagent_cli_help.md`: generated full CLI help for the installed MeshAgent version.
- `scripts/refresh_cli_reference.sh`: maintainer utility to regenerate the help reference when the installed CLI changes. This is not required for normal in-room operation.
