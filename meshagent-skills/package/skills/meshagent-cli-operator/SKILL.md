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

## Command routing

- Start with `references/command_groups.md` to choose the correct command family.
- Use `references/meshagent_cli_help.md` for exact command shapes and flags.
- Prefer the smallest command path that can complete the task.
- Prefer non-interactive commands over interactive flows.

## Operating rules

- Do not assume the active project, active room, hostname, filesystem layout, or environment variables. Inspect them or ask when they matter.
- Use `--help` on the exact subcommand before composing long invocations.
- Prefer read commands before create, update, deploy, or delete.
- Restate the exact mutation target before destructive changes.
- Verify the resulting state after mutation.
- Do not print secret values unless the user explicitly asks for them and the command returns them.

## Out of scope

- This skill does not define product workflows for mail, scheduling, domain management, website construction, or agent building.
- This skill does not assume any particular container image, mount layout, room runtime, or deployment topology.

## Bundled resources

- `references/command_groups.md`: fast routing map for the CLI.
- `references/meshagent_cli_help.md`: packaged CLI help reference for the MeshAgent CLI version recorded in `compat.json`.
