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

The package now has one general CLI skill plus a larger specialized operator bundle:

- `skills/meshagent-cli-operator/`
  General MeshAgent CLI routing, command composition, live-room execution rules, and packaged CLI reference material.
- `skills/meshagent-sdk-researcher/`
  Guidance for resolving the MeshAgent checkout roots and using docs, examples, and source to answer SDK/API questions.
- `skills/meshagent-database-operator/`
  Room database schema, CRUD, search, SQL, namespace, index, and `RequiredTable` workflows.
- `skills/meshagent-memory-operator/`
  Room memory creation, ingestion, recall, and query workflows.
- `skills/meshagent-workflow-orchestrator/`
  End-to-end cross-skill workflow ownership, preflight, sequencing, and completion-gate tracking.
- `skills/meshagent-queue-operator/`
  Queue send, receive, backlog inspection, and queue-delivery verification.
- `skills/meshagent-queue-worker-builder/`
  Queue-backed process YAML authoring for schedulable or dequeued room jobs.
- `skills/meshagent-runtime-operator/`
  Live runtime debugging for developer logs, containers, and port forwarding.
- `skills/meshagent-scheduler/`
  `meshagent scheduled-task ...` workflows, timezone handling, and queue-delivery verification.
- `skills/meshagent-service-operator/`
  Service and service-template lifecycle, validation, rendering, and room service operations.
- `skills/meshagent-storage-operator/`
  Room storage inspection, copy, show, and removal workflows.
- `skills/meshagent-webapp-backend-builder/`
  Canonical backend path for deployable room-hosted web applications, including Python handlers, contact forms, room DB integration, and mailbox-backed outbound email workflows.
- `skills/meshagent-webapp-frontend-builder/`
  Canonical frontend path for interactive room websites using Preact + htm on top of the backend path.
- `skills/meshagent-mail-operator/`
  Mailbox administration, room SMTP behavior, inbound queue inspection, and mailbox-backed sender guidance.
- `skills/meshagent-participant-token-operator/`
  Participant token source discovery, service token injection, delegated shell token behavior, and API-key-signed token guidance.
- `skills/meshagent-webmaster/`
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

## Package layout

Key files and directories in this package:

- `README.md`
  Package overview and maintenance notes.
- `compat.json`
  Target MeshAgent CLI version for the packaged references and validation.
- `.claude-plugin/plugin.json`
  Plugin metadata for the packaged skill pack.
- `skills/_shared/references/`
  Shared package-level references for live-room CLI context and managed hostname rules.
- `skills/_shared/references/process_agent_design.md`
  Shared process design reference for shared-identity agents across chat, mail, queue, and toolkit channels.
- `skills/_shared/references/workflow_accountability.md`
  Shared workflow-owner, completion-gate, evidence, and handoff contract for cross-skill outcomes.
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
- `scripts/audit_meshagent_skill_commands.py`
  Command-reference audit against the live CLI tree.
- `skills/meshagent-cli-operator/SKILL.md`
  Core CLI execution and command-routing skill.
- `skills/meshagent-cli-operator/agents/openai.yaml`
  OpenAI agent metadata for the core CLI skill.
- `skills/meshagent-cli-operator/references/command_groups.md`
  Curated command-family routing reference.
- `skills/meshagent-cli-operator/references/meshagent_cli_help.md`
  Generated recursive CLI help reference.
- `skills/meshagent-sdk-researcher/SKILL.md`
  SDK/docs/example lookup skill for resolving a MeshAgent checkout and its docs/examples roots.
- `skills/meshagent-sdk-researcher/agents/openai.yaml`
  OpenAI agent metadata for the SDK researcher.
- `skills/meshagent-database-operator/SKILL.md`
  Room database schema, CRUD, search, SQL, namespace, and index skill.
- `skills/meshagent-database-operator/agents/openai.yaml`
  OpenAI agent metadata for the database operator.
- `skills/meshagent-memory-operator/SKILL.md`
  Room memory ingestion, recall, and query skill.
- `skills/meshagent-memory-operator/agents/openai.yaml`
  OpenAI agent metadata for the memory operator.
- `skills/meshagent-workflow-orchestrator/SKILL.md`
  End-to-end cross-skill workflow orchestration and accountability skill.
- `skills/meshagent-workflow-orchestrator/agents/openai.yaml`
  OpenAI agent metadata for the workflow orchestrator.
- `skills/meshagent-queue-operator/SKILL.md`
  Queue send, receive, backlog, and delivery-verification skill.
- `skills/meshagent-queue-operator/agents/openai.yaml`
  OpenAI agent metadata for the queue operator.
- `skills/meshagent-queue-operator/references/queue_discovery.md`
  Preferred room queue-discovery workflow using CLI toolkit inspection and invocation before any SDK fallback.
- `skills/meshagent-queue-worker-builder/SKILL.md`
  Queue-backed process and queue-consumer `meshagent.yaml` authoring skill.
- `skills/meshagent-queue-worker-builder/agents/openai.yaml`
  OpenAI agent metadata for the queue worker builder.
- `skills/meshagent-queue-worker-builder/references/scheduled_email_worker.md`
  End-to-end reference for mailbox-backed queue Workers that must pass an immediate smoke test before one-time scheduling.
- `skills/meshagent-runtime-operator/SKILL.md`
  Live room runtime inspection and debugging skill.
- `skills/meshagent-runtime-operator/agents/openai.yaml`
  OpenAI agent metadata for the runtime operator.
- `skills/meshagent-webapp-backend-builder/SKILL.md`
  Deployable room webapp backend, verification, DB, and contact-form workflow skill.
- `skills/meshagent-webapp-backend-builder/agents/openai.yaml`
  OpenAI agent metadata for the webapp backend builder.
- `skills/meshagent-webapp-backend-builder/references/contact_form_example.py`
  Known-good contact-form handler reference using real room SMTP defaults and a mailbox-backed sender placeholder.
- `skills/meshagent-webapp-backend-builder/references/dev_hot_reload_loop.sh`
  Preferred `meshagent webserver join --watch` launcher for room-hosted backend dev loops.
- `skills/meshagent-webapp-backend-builder/references/mailbox_backed_sender.md`
  Mailbox provisioning and sender-identity reference for room-hosted contact forms.
- `skills/meshagent-webapp-backend-builder/references/minimal_webserver.yaml`
  Minimal deployable public webserver YAML example.
- `skills/meshagent-webapp-backend-builder/references/verification_checklist.md`
  Short completion checklist for deployed contact-form sites.
- `skills/meshagent-webapp-frontend-builder/SKILL.md`
  Interactive room-webapp frontend skill using Preact + htm on top of the backend path.
- `skills/meshagent-webapp-frontend-builder/agents/openai.yaml`
  OpenAI agent metadata for the frontend webapp builder.
- `skills/meshagent-mail-operator/SKILL.md`
  Mailbox, SMTP, queue, and room-hosted outbound mail workflow skill.
- `skills/meshagent-mail-operator/agents/openai.yaml`
  OpenAI agent metadata for the mail operator.
- `skills/meshagent-participant-token-operator/SKILL.md`
  Participant token source, injection, delegation, and minting skill.
- `skills/meshagent-participant-token-operator/agents/openai.yaml`
  OpenAI agent metadata for the participant token operator.
- `skills/meshagent-scheduler/SKILL.md`
  Scheduled-task and queue-delivery skill.
- `skills/meshagent-scheduler/agents/openai.yaml`
  OpenAI agent metadata for the scheduler.
- `skills/meshagent-service-operator/SKILL.md`
  Service validation, rendering, lifecycle, and room service operations skill.
- `skills/meshagent-service-operator/agents/openai.yaml`
  OpenAI agent metadata for the service operator.
- `skills/meshagent-storage-operator/SKILL.md`
  Room storage inspection, copy, show, and cleanup skill.
- `skills/meshagent-storage-operator/agents/openai.yaml`
  OpenAI agent metadata for the storage operator.
- `skills/meshagent-webmaster/SKILL.md`
  Route/domain mapping and static webserver reference skill.
- `skills/meshagent-webmaster/agents/openai.yaml`
  OpenAI agent metadata for the webmaster.
- `skills/meshagent-webmaster/references/static_webserver_example.yaml`
  Packaged static webserver YAML example for route and website work.

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
- when a MeshAgent SDK checkout is preloaded into the runtime, it is commonly mounted at `/src/meshagent-sdk`, but skills should still use `meshagent-sdk-researcher` to resolve the actual checkout root before relying on that path

These are package-level conventions enforced by the current skill text. They are intentionally documented here because the skills depend on them for live-room behavior.

## Skill package rules

The current validator enforces these package rules:

- the packaged CLI version in `compat.json` must match the installed CLI used for validation
- generated help must mention that exact CLI version
- command-group references must stay aligned with `meshagent --help`
- skills must not reference sibling `SKILL.md` files by relative path
- any packaged relative resource path mentioned by a skill must resolve to a real bundled file
- every skill must provide `agents/openai.yaml` with an `interface` mapping that contains `display_name`, `short_description`, and a `default_prompt` that names the skill as `$skill-name`
- every skill must carry workflow-accountability metadata and a `## Workflow accountability` section

## Scripts

- `scripts/refresh_meshagent_skills_package.py`
  User-facing wrapper. Detects the installed MeshAgent CLI version from `<meshagent-bin> version`, writes that version into `compat.json`, regenerates the packaged CLI help reference, and runs the validator.
- `scripts/generate_meshagent_cli_help_reference.py`
  Regenerates `skills/meshagent-cli-operator/references/meshagent_cli_help.md` by recursively capturing `meshagent --help`. This script reads the version label from `compat.json`; it does not update `compat.json`.
- `scripts/validate_meshagent_skills_package.py`
  Validates package consistency against the installed CLI and the current skill-package rules.
- `scripts/audit_meshagent_skill_commands.py`
  Crawls the live `meshagent --help` tree and checks whether packaged command references resolve to real command nouns.

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
