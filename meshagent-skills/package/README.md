# MeshAgent Skills

This package contains MeshAgent CLI commands and skills for room operations, SDK reference lookups, mail workflows, scheduled tasks, and website/domain workflows.

## Package layout

- `commands/`
  Slash-command entrypoints for MeshAgent CLI requests.
- `skills/meshagent-cli-operator/`
  General MeshAgent CLI usage and command routing.
- `skills/meshagent-sdk-operator/`
  SDK/docs lookup guidance for using the preloaded `/src/meshagent-sdk` checkout, docs, and examples.
- `skills/meshagent-mail-operator/`
  Mailbox administration, SMTP behavior, and inbound mail queue inspection.
- `skills/meshagent-scheduling-operator/`
  `meshagent scheduled-task ...` workflows plus queue verification guidance.
- `skills/meshagent-webmaster-operator/`
  Domain mappings and a static webserver reference example.

## Review Notes

- The machine-readable compatibility source is `compat.json`.
- The packaged CLI references are anchored to the MeshAgent CLI version recorded in `compat.json`.
- The generated CLI reference lives at `skills/meshagent-cli-operator/references/meshagent_cli_help.md`.
- The package-local maintenance entrypoints live under `scripts/` so the CLI reference can be regenerated and validated from any repository that vendors this package.
- The SDK reference skill assumes the live room image preloads the SDK checkout at `/src/meshagent-sdk`.

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
