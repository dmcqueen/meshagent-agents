# MeshAgent Skills

This package contains MeshAgent CLI commands and skills for room operations, mail workflows, scheduled tasks, and website deployment.

## Package layout

- `commands/`
  Slash-command entrypoints for MeshAgent CLI requests.
- `skills/meshagent-cli-operator/`
  General room-scoped MeshAgent CLI operations and the shared room runtime contract for this package.
- `skills/meshagent-mail-operator/`
  Mailbox, MailBot, inbox evidence, and contact-form email workflows.
- `skills/meshagent-scheduling-operator/`
  `meshagent scheduled-task ...` workflows tied to a room or clearly scoped project workflow.
- `skills/meshagent-webmaster-operator/`
  `meshagent webserver ...`, `meshagent route ...`, and public website deployment workflows.

## Review Notes

- The machine-readable compatibility source is `compat.json`.
- The packaged CLI references are anchored to the MeshAgent CLI version recorded in `compat.json`.
- The shared room runtime assumptions for these skills are defined in `skills/meshagent-cli-operator/SKILL.md`.
- The generated CLI reference lives at `skills/meshagent-cli-operator/references/meshagent_cli_help.md`.
- The package-local maintenance entrypoints live under `scripts/` so the CLI reference can be regenerated and validated from any repository that vendors this package.
- User-visible files created by these skills should live under `/data` when running inside the room container.

## Update Workflow

1. Install the target MeshAgent CLI version.
2. Update `compat.json`.
3. Run `python3 scripts/sync_meshagent_cli_reference.py --meshagent-bin <meshagent>` to regenerate `skills/meshagent-cli-operator/references/meshagent_cli_help.md` from the installed CLI.
4. Review `skills/meshagent-cli-operator/references/command_groups.md` against `meshagent --help`.
5. Run `python3 scripts/validate_meshagent_skills.py --meshagent-bin <meshagent>`.

## Command Map

- `commands/meshagent.md`
  General entrypoint for MeshAgent CLI work.
- `commands/meshagent-room.md`
  Room lifecycle and room-scoped operations.
- `commands/meshagent-service.md`
  Service specs, deploys, MCP, helpers, and webserver-adjacent work.
- `commands/meshagent-project.md`
  Project-scoped administration such as routes, mailboxes, and scheduled tasks.
- `commands/meshagent-agent.md`
  Agent runtime orchestration such as chatbot, worker, mailbot, process, and related runtimes.
- `commands/meshagent-inspect.md`
  Read-only inspection and diagnostics.
