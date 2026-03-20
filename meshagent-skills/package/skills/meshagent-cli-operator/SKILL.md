---
name: meshagent-cli-operator
description: Use the MeshAgent CLI. This skill is for choosing command paths, reading help output, composing non-interactive commands, and verifying results.
---

# MeshAgent CLI Operator

Use this skill when the task is primarily about running or explaining MeshAgent CLI commands.

## Quick start

1. Resolve the `meshagent` binary from `PATH` or use the explicit binary path the user provides.
2. Identify the narrowest command path that matches the request.
3. If flags are uncertain, consult `references/command_groups.md`, then `references/meshagent_cli_help.md`. Only run live `meshagent <path> --help` when the packaged references are missing the needed subcommand detail or appear inconsistent with the observed CLI version.
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
- Before running a deploy with `--domain` or reporting a managed public URL, validate that the chosen hostname suffix matches `MESHAGENT_API_URL`. In a `.life` environment, `.meshagent.app` is wrong and must be corrected to `.meshagent.dev`.
- If authentication is uncertain, test a room-scoped read command first. Do not claim that the CLI is unauthenticated until an actual MeshAgent command fails for that reason.
- Treat existing MeshAgent environment variables and active CLI session state as real runtime context to inspect and use, not as something to ignore by default.
- For room-site or room-service work, distinguish between local authoring files and room-visible runtime files. User-visible runtime data belongs under `/data`, but `meshagent webserver deploy` copies local sources from the current working directory, so deployable website source trees must live under a subdirectory of that working directory in the live room runtime.
- For `meshagent webserver deploy`, use `--website-path` as the room storage destination. Do not treat `/data/...` as the local source root for deployable route files unless the current working directory is already under `/data`.
- Do not use room file tools such as listing or writing files against filesystem root paths like `.` or `/`, or temporary/build paths such as `/tmp`. Use concrete room-visible paths under `/data`, or use shell commands when the task truly needs a non-room-local path. When the task is a deployable webserver project, a shell-managed source tree under the current working directory is valid.

## Command routing

- Start with `references/command_groups.md` to choose the correct command family.
- Use `references/meshagent_cli_help.md` for exact command shapes and flags.
- Prefer the packaged references over live `--help` in a live room to avoid noisy recursive help probing.
- Prefer the smallest command path that can complete the task.
- Prefer non-interactive commands over interactive flows.

## Operating rules

- Do not invent the active project, active room, hostname, filesystem layout, or environment variables. Inspect them or ask when they matter.
- Do not use live `meshagent ... --help` as a default discovery step in a live room when the packaged references already cover the command. Use live `--help` only as a fallback for missing or version-mismatched details.
- Prefer read commands before create, update, deploy, or delete.
- Restate the exact mutation target before destructive changes.
- Verify the resulting state after mutation.
- For room website requests that ask for a live URL, do not stop at local file creation or `meshagent webserver check`. Either complete the deploy and return the public URL, or report the exact blocking command and error.
- For room website requests, verify the live behavior of the deployed site itself, not just the deploy command result. At minimum, check that the public URL returns the expected status and content for the primary route.
- For contact-form websites, test both a GET of the form page and representative POST submissions after deploy. Treat any live 500 as an application/runtime failure to diagnose before blaming room infrastructure.
- If `MESHAGENT_ROOM` is already present, do not use `meshagent rooms list` as a prerequisite for room-scoped deploy work.
- If a room website deploy hits a managed-hostname collision, do not stop after the first candidate. Automatically retry with additional same-environment hostname candidates before asking the user to choose one.
- If `meshagent webserver deploy --domain ...` fails because the hostname is already in use and follow-up route inspection is forbidden, treat that as a collision on that candidate and try a different hostname. Do not present it as a generic permissions blocker unless repeated candidate creation attempts also fail.
- Do not report a managed URL whose suffix contradicts the active API environment. If the composed or observed URL ends with the wrong MeshAgent-managed suffix, treat that as an invalid candidate and correct it before replying.
- When a deployed MeshAgent webserver returns 500, first suspect route-handler import/render/runtime errors before concluding that the room route or platform is broken.
- For Python handlers that render inline HTML templates, do not use `str.format()` on raw HTML/CSS/regex-heavy strings unless every literal brace is escaped. Prefer a safer templating approach or pre-escaped placeholders.
- Do not print secret values unless the user explicitly asks for them and the command returns them.
- For live room workflows, do not treat `/tmp` as the durable room workspace. Room-owned runtime files belong under `/data`, but deployable webserver source trees may need to live under the current working directory so `meshagent webserver deploy` can upload them.

## Bundled resources

- `references/command_groups.md`: fast routing map for the CLI.
- `references/meshagent_cli_help.md`: packaged CLI help reference for the MeshAgent CLI version recorded in `compat.json`.
