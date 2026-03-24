---
name: meshagent-cli-operator
description: Use the MeshAgent CLI. This skill is for choosing command paths, reading help output, composing non-interactive commands, and verifying results.
metadata:
  short-description: Route and run MeshAgent CLI commands safely and non-interactively.
  references:
    bundled:
      - references/command_groups.md
      - references/meshagent_cli_help.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/managed_hostname_rules.md
      - ../_shared/references/workflow_accountability.md
    resolved_targets:
      - live meshagent help output when bundled help is missing or stale
  related_skills:
    - skill: meshagent-sdk-researcher
      when: The task depends on SDK or server source, not just CLI behavior.
    - skill: meshagent-webapp-builder
      when: A CLI deploy task also requires authoring or debugging the web app itself.
    - skill: meshagent-service-operator
      when: The main task is service lifecycle semantics rather than command routing.
  scope:
    owns:
      - command-family routing
      - safe non-interactive CLI composition
      - CLI-side verification patterns
    excludes:
      - SDK API design
      - app-specific implementation work
  workflow:
    can_be_owner: true
    handoff_policy: retain_accountability_until_owner_transfer
    completion_gates:
      - mutation_target_confirmed_when_relevant
      - observed_state_matches_claim
      - user_visible_result_verified_or_exact_blocker_reported
    evidence:
      - exact_commands_or_artifacts_used
      - observed_room_or_runtime_state
      - user_visible_result_or_exact_blocker
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

## Command routing

- Start with `references/command_groups.md` to choose the correct command family.
- Use `references/meshagent_cli_help.md` for exact command shapes and flags.
- Use `../_shared/references/live_room_cli_context.md` for shared live-room CLI rules.
- Use `../_shared/references/managed_hostname_rules.md` for shared managed-hostname selection and validation rules.
- Prefer the packaged references over live `--help` in a live room to avoid noisy recursive help probing.
- Prefer the smallest command path that can complete the task.
- Prefer non-interactive commands over interactive flows.

## Related skills

- `meshagent-sdk-researcher`: Use it when the answer depends on source-level behavior or examples rather than command shape.
- `meshagent-webapp-builder`: Use it when a CLI deploy command is only one part of building or fixing a room website.
- `meshagent-service-operator`: Use it when the task is primarily about service semantics, templates, or room service lifecycle.

## Live room execution

- Apply `../_shared/references/live_room_cli_context.md` for room context reuse, `MESHAGENT_ROOM`, auth-first checks, durable workspace rules, and local-vs-room path handling.
- Apply `../_shared/references/managed_hostname_rules.md` for `MESHAGENT_API_URL`-driven hostname suffix selection and collision handling.

## Operating rules

- Do not invent the active project, active room, hostname, filesystem layout, or environment variables. Inspect them or ask when they matter.
- Do not use live `meshagent ... --help` as a default discovery step in a live room when the packaged references already cover the command. Use live `--help` only as a fallback for missing or version-mismatched details.
- Before writing ad hoc SDK code for a room operation, check whether the CLI already exposes a generic toolkit path such as `meshagent room agent list-toolkits` or `meshagent room agent invoke-tool`.
- When a first command returns noisy or truncated output for a simple inspection task, rerun the narrowest command and summarize the exact result instead of handing the truncation problem back to the user.
- Prefer read commands before create, update, deploy, or delete.
- Restate the exact mutation target before destructive changes.
- Verify the resulting state after mutation.
- For room website requests that ask for a live URL, do not stop at local file creation or `meshagent webserver check`. Either complete the deploy and return the public URL, or report the exact blocking command and error.
- For room website requests, verify the live behavior of the deployed site itself, not just the deploy command result. At minimum, check that the public URL returns the expected status and content for the primary route.
- For contact-form websites, test both a GET of the form page and representative POST submissions after deploy. Treat any live 500 as an application/runtime failure to diagnose before blaming room infrastructure.
- When a deployed MeshAgent webserver returns 500, first suspect route-handler import/render/runtime errors before concluding that the room route or platform is broken.
- For Python handlers that render inline HTML templates, do not use `str.format()` on raw HTML/CSS/regex-heavy strings unless every literal brace is escaped. Prefer a safer templating approach or pre-escaped placeholders.
- Do not print secret values unless the user explicitly asks for them and the command returns them.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return command evidence and observed state to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Bundled resources

- `references/command_groups.md`: fast routing map for the CLI.
- `references/meshagent_cli_help.md`: packaged CLI help reference for the MeshAgent CLI version recorded in `compat.json`.
- `../_shared/references/live_room_cli_context.md`: shared live-room CLI context rules for room-scoped work.
- `../_shared/references/managed_hostname_rules.md`: shared managed-hostname selection and validation rules.
