---
name: meshagent-cli-operator
description: Use the MeshAgent CLI. This skill is for choosing command paths, reading help output, composing non-interactive commands, and verifying results.
---

# MeshAgent CLI Operator

Use this skill when the task is primarily about running or explaining MeshAgent CLI commands.

## Quick start

1. Resolve the `meshagent` binary from `PATH` or use the explicit binary path the user provides.
2. Identify the narrowest command path that matches the request.
3. If flags are uncertain, consult `references/command_groups.md`, then `references/meshagent_cli_help.md`, or run `meshagent <path> --help`.
4. Prefer read-only inspection before mutation.
5. Verify the result with the corresponding read command.

## Resolve the CLI

- Prefer `meshagent` on `PATH`.
- If the user gives an explicit MeshAgent binary path, use that path.
- If no MeshAgent CLI binary is available, stop and report that clearly.

## Live room execution

- If this skill is running inside a live MeshAgent room agent or room shell, first try the existing runtime context before asking the user to log in again.
- If `MESHAGENT_ROOM` is present, prefer room-scoped commands and pass `--room "${MESHAGENT_ROOM}"` when the command requires it.
- If `MESHAGENT_API_URL` is present and the task needs a default MeshAgent-managed public hostname, derive the suffix from that API URL: use `*.meshagent.app` for `.com` environments and `*.meshagent.dev` for `.life` environments.
- If `MESHAGENT_API_URL` is absent or does not clearly identify the environment, inspect an existing route in the current project or ask before inventing a managed public hostname.
- Packaged help examples that show `.meshagent.app` are illustrative only. Do not copy that suffix blindly when `MESHAGENT_API_URL` indicates a different environment.
- If authentication is uncertain, test a room-scoped read command first. Do not claim that the CLI is unauthenticated until an actual MeshAgent command fails for that reason.
- Treat existing MeshAgent environment variables and active CLI session state as real runtime context to inspect and use, not as something to ignore by default.
- For room-site or room-service work, keep user-visible artifacts under `/data` unless the command explicitly requires a different path.
- Do not use room file tools such as listing or writing files against filesystem root paths like `.` or `/`, or temporary/build paths such as `/tmp` or `/src`. Use concrete room-visible paths under `/data`, or use shell commands when the task truly needs a non-room-local temporary path.

## Command routing

- Start with `references/command_groups.md` to choose the correct command family.
- Use `references/meshagent_cli_help.md` for exact command shapes and flags.
- Prefer the smallest command path that can complete the task.
- Prefer non-interactive commands over interactive flows.

## Operating rules

- Do not invent the active project, active room, hostname, filesystem layout, or environment variables. Inspect them or ask when they matter.
- Use `--help` on the exact subcommand before composing long invocations.
- Prefer read commands before create, update, deploy, or delete.
- Restate the exact mutation target before destructive changes.
- Verify the resulting state after mutation.
- Do not print secret values unless the user explicitly asks for them and the command returns them.
- For live room workflows, do not treat `/tmp` or `/src` as the durable room workspace. Put room-owned site and service files under `/data`.

## Bundled resources

- `references/command_groups.md`: fast routing map for the CLI.
- `references/meshagent_cli_help.md`: packaged CLI help reference for the MeshAgent CLI version recorded in `compat.json`.
