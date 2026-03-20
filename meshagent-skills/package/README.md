# MeshAgent Skills

This package is a vendorable MeshAgent skill pack.

It combines:

- slash-command entrypoints under `commands/`
- focused `SKILL.md` files under `skills/`
- packaged CLI reference material under `skills/meshagent-cli-operator/references/`
- maintenance scripts under `scripts/`
- a machine-readable compatibility target in `compat.json`
- plugin metadata in `.claude-plugin/plugin.json`

The package is designed so a live room agent can answer MeshAgent workflow requests with package-local instructions and references instead of relying on ad hoc prompting.

## Current system

The package currently has one general CLI skill plus five specialized skills:

- `skills/meshagent-cli-operator/`
  General MeshAgent CLI routing, command composition, live-room execution rules, and packaged CLI reference material.
- `skills/meshagent-sdk-researcher/`
  Guidance for using the preloaded `/src/meshagent-sdk` checkout, docs, examples, and source to answer SDK/API questions.
- `skills/meshagent-webapp-builder/`
  Build and verify deployable room-hosted web applications, including contact forms, public handlers, and mailbox-backed outbound email workflows.
- `skills/meshagent-mail-operator/`
  Mailbox administration, room SMTP behavior, inbound queue inspection, and mailbox-backed sender guidance for room-hosted mail workflows.
- `skills/meshagent-scheduling-operator/`
  `meshagent scheduled-task ...` workflows and queue-delivery verification.
- `skills/meshagent-webmaster-operator/`
  Route/domain mapping behavior and the static webserver YAML reference example.

The package also exposes command entrypoints for common request classes:

- `commands/meshagent.md`
  General MeshAgent CLI entrypoint.
- `commands/meshagent-room.md`
  Room lifecycle and room-scoped operations.
- `commands/meshagent-service.md`
  Services, deploys, MCP, helpers, and webserver-adjacent work.
- `commands/meshagent-project.md`
  Project-scoped administration such as routes, mailboxes, and scheduled tasks.
- `commands/meshagent-agent.md`
  Agent runtime orchestration such as chatbot, worker, mailbot, and process runtimes.
- `commands/meshagent-inspect.md`
  Read-only inspection and diagnostics.

## File inventory

Current files in this package:

- `README.md`
  Package overview and maintenance notes.
- `compat.json`
  Target MeshAgent CLI version for the packaged references and validation.
- `.claude-plugin/plugin.json`
  Plugin metadata for the packaged skill pack.
- `commands/meshagent.md`
  General MeshAgent CLI entrypoint.
- `commands/meshagent-room.md`
  Room-scoped command entrypoint.
- `commands/meshagent-service.md`
  Service, deploy, MCP, and webserver-adjacent entrypoint.
- `commands/meshagent-project.md`
  Project-scoped administration entrypoint.
- `commands/meshagent-agent.md`
  Agent runtime orchestration entrypoint.
- `commands/meshagent-inspect.md`
  Read-only inspection and diagnostics entrypoint.
- `scripts/refresh_meshagent_skills_package.py`
  One-command updater for `compat.json`, packaged CLI help, and validation.
- `scripts/generate_meshagent_cli_help_reference.py`
  CLI help reference generator.
- `scripts/validate_meshagent_skills_package.py`
  Package validator.
- `skills/meshagent-cli-operator/SKILL.md`
  Core CLI execution and command-routing skill.
- `skills/meshagent-cli-operator/references/command_groups.md`
  Curated command-family routing reference.
- `skills/meshagent-cli-operator/references/meshagent_cli_help.md`
  Generated recursive CLI help reference.
- `skills/meshagent-sdk-researcher/SKILL.md`
  SDK/docs/example lookup skill for the preloaded `/src/meshagent-sdk` checkout.
- `skills/meshagent-webapp-builder/SKILL.md`
  Deployable room webapp build, verification, and contact-form workflow skill.
- `skills/meshagent-mail-operator/SKILL.md`
  Mailbox, SMTP, queue, and room-hosted outbound mail workflow skill.
- `skills/meshagent-scheduling-operator/SKILL.md`
  Scheduled-task and queue-delivery skill.
- `skills/meshagent-webmaster-operator/SKILL.md`
  Route/domain mapping and static webserver reference skill.

## Packaged references

- `compat.json`
  The machine-readable target MeshAgent CLI version for this package.
- `skills/meshagent-cli-operator/references/meshagent_cli_help.md`
  Generated recursive `meshagent --help` capture for the CLI version in `compat.json`.
- `skills/meshagent-cli-operator/references/command_groups.md`
  Curated command-family routing guidance layered on top of the raw help reference.

These references are part of the package contract. The skills are expected to use them rather than inventing command shapes.

## Live room assumptions

The current skills assume the following when they are installed into a live room runtime:

- room-scoped work should prefer the existing MeshAgent CLI session before asking for auth again
- `MESHAGENT_ROOM` identifies the current room when a command needs `--room`
- `MESHAGENT_API_URL` can be used to derive the managed public hostname family for routes and published sites
- room-owned runtime artifacts should live under `/data`
- deployable `meshagent webserver` source trees should live under the current working directory for that runtime, with `--website-path` used as the room-storage destination
- website tasks are only complete after a live HTTP smoke test, not merely after file generation or deploy success
- the MeshAgent SDK checkout is preloaded at `/src/meshagent-sdk` for SDK/docs lookup

These are package-level conventions enforced by the current skill text. They are intentionally documented here because the skills depend on them for live-room behavior.

## Skill package rules

The current validator enforces these package rules:

- the packaged CLI version in `compat.json` must match the installed CLI used for validation
- generated help must mention that exact CLI version
- command-group references must stay aligned with `meshagent --help`
- skills must not reference sibling skills by name
- skills must not reference sibling `SKILL.md` files by relative path
- specialized skills must include the package-local CLI reference pointers unless they are explicitly exempt

## Scripts

- `scripts/refresh_meshagent_skills_package.py`
  User-facing wrapper. Detects the installed MeshAgent CLI version from `<meshagent-bin> version`, writes that version into `compat.json`, regenerates the packaged CLI help reference, and runs the validator.
- `scripts/generate_meshagent_cli_help_reference.py`
  Regenerates `skills/meshagent-cli-operator/references/meshagent_cli_help.md` by recursively capturing `meshagent --help`. This script reads the version label from `compat.json`; it does not update `compat.json`.
- `scripts/validate_meshagent_skills_package.py`
  Validates package consistency against the installed CLI and the current skill-package rules.

## Update workflow

Recommended one-command flow:

```bash
python3 scripts/refresh_meshagent_skills_package.py --meshagent-bin <meshagent>
```

Manual equivalent:

1. Install or locate the target MeshAgent CLI binary.
2. Run `<meshagent> version` and write that exact version into `compat.json`.
3. Run `python3 scripts/generate_meshagent_cli_help_reference.py --meshagent-bin <meshagent>`.
4. Review `skills/meshagent-cli-operator/references/command_groups.md` if command-family routing needs adjustment for the new CLI behavior.
5. Run `python3 scripts/validate_meshagent_skills_package.py --meshagent-bin <meshagent>`.
