---
name: meshagent-cli-operator
description: Operate the MeshAgent CLI primarily at room scope. Use this skill for inspecting, updating, deploying, and troubleshooting the current room, its storage, its services, and room-scoped MeshAgent runtimes. Do not use this skill for meshagent auth or meshagent setup workflows.
---

# MeshAgent CLI Operator

Use this skill for any task that should be completed with the MeshAgent CLI.

## Runtime assumptions

This skill assumes it is running inside a MeshAgent room container based on `meshagent/shell-codex:default`.

- The MeshAgent CLI is expected at `/usr/bin/meshagent`.
- `meshagent` on `PATH` is an acceptable fallback.
- `MESHAGENT_TOKEN` may be present for room-scoped MeshAgent access and delegated shell execution.
- The current room is the value of `MESHAGENT_ROOM`.
- The default public MeshAgent domain in this environment is `__MESHAGENT_PUBLIC_DOMAIN__`.
- The user-visible room filesystem is mounted at `/data`.
- To create or modify files the user should see, write them under `/data` and report paths relative to `/data`.
- Do not assume a repo-local virtualenv or checkout exists inside the container.
- Do not install packages into `/data`.

## Quick start

1. Resolve the CLI binary.
2. Identify the narrowest command path that matches the request.
3. If flags are uncertain, consult `references/command_groups.md`, then `references/meshagent_cli_help.md`, or run `meshagent <path> --help`.
4. Use `meshagent-mail-operator` for mailbox provisioning, inbox evidence, MailBot toolkits, or contact-form email delivery.
5. Use `meshagent-scheduling-operator` for scheduled-task creation, update, verification, pause, resume, or deletion.
6. Use `meshagent-webmaster-operator` for websites, `meshagent webserver ...`, routes, or public hostname exposure.
7. Prefer read-only inspection before mutation.
8. After a change, verify the result with the corresponding read command.

## Resolve the CLI

Prefer these paths in order:

1. `/usr/bin/meshagent`
2. `meshagent`

If neither exists, stop and report that the MeshAgent CLI is unavailable.

## Command routing

Start with `references/command_groups.md` to choose the right area:

- room lifecycle and room APIs
- service and deployment workflows
- agent runtime orchestration
- inspection and diagnostics

Use `references/meshagent_cli_help.md` for the exact installed command tree and flags.

Follow the explicit top-level command policy in `references/command_groups.md`:

- `USE`: normal command family for this skill
- `USE WITH CAUTION`: allowed only when clearly needed and tightly scoped
- `DON'T USE`: out of scope for this skill

## Operating rules

- Scope the target first: room, room service, room storage path, room participant, room queue, room port, or agent runtime.
- Prefer the smallest command path that can complete the task.
- Use `--help` on the exact subcommand before composing long invocations.
- When executing commands in this runtime, prefer `/usr/bin/meshagent ...` so command examples match the container image.
- This skill is primarily for room-scoped work in the current room. Prefer `meshagent room ...`, room service commands, service deployment into the current room, room storage access, and runtime commands that operate within the current room.
- If a command accepts `--room`, it must target `MESHAGENT_ROOM` only. Omit `--room` when the command already defaults to the current room, or set it explicitly to `MESHAGENT_ROOM`. Do not use a different room value.
- For website, route, and public hostname work, default to `*.__MESHAGENT_PUBLIC_DOMAIN__` hostnames unless the user explicitly asks for a different MeshAgent public domain.
- When the user asks to make, update, or deploy a site in room context, create or deploy the site in the current room and return the resulting public URL. Do not stop at local file edits or local build success when the requested outcome is a live room site.
- Do not modify unrelated example apps, sample repos, bundled SDK examples, or maintainer reference projects to satisfy a room deployment request. For room-site work, create or update the assets and services that belong to the current room workflow.
- When authorization is uncertain, test the actual target read command for the current room before concluding that authentication is missing.
- Treat `/data` as the writable user-visible workspace. If a command writes files for the user, keep them under `/data`.
- Do not expose secret values unless the user explicitly asks for them.
- Treat delete and overwrite operations as destructive. Confirm the target and blast radius before executing them.
- After create, update, deploy, or delete, run the appropriate verification command and summarize the resulting state.

## Out Of Scope

Do not use these commands as part of this skill:

- `meshagent auth ...`
- `meshagent setup`
- `meshagent api-key ...`
- `meshagent project create`
- `meshagent project activate -i`
- `meshagent token generate`
- `meshagent secret ...`

Avoid these project-wide or account-wide command families unless the user explicitly asks for them and the task clearly cannot be completed with room-scoped commands:

- `meshagent project ...`
- `meshagent webhook ...`
- `meshagent route ...`
- `meshagent scheduled-task ...`
- project-wide `meshagent service ...` operations that are not targeting the current room

Treat these command families as `USE WITH CAUTION`, not defaults:

- `meshagent project list`
- `meshagent project activate PROJECT_ID` only when a room task clearly requires switching to a specific existing project first
- `meshagent webhook ...`
- `meshagent route ...`
- `meshagent scheduled-task ...`
- `meshagent helper ...`

## Bundled resources

- `references/command_groups.md`: fast routing map for the CLI.
- `references/meshagent_cli_help.md`: packaged CLI help reference for the MeshAgent CLI version recorded in `compat.json`.
