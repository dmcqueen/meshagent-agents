---
name: meshagent-service-operator
description: Operate MeshAgent services and service templates. Use this skill for service spec generation, validation, create/update/delete, template rendering, room-scoped service lifecycle, and service inspection.
metadata:
  short-description: Operate services, service templates, and room service lifecycle.
  references:
    bundled:
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/runtime_image_environment_rules.md
      - ../_shared/references/service_yaml_correctness.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - docs_root
      - cli_root
      - server_root
    resolved_targets:
      - shared live-room CLI context rules
      - shared runtime image environment rules
      - shared service YAML correctness rules
      - services CLI source
      - room-services CLI source
      - service examples and packaging docs
  related_skills:
    - skill: meshagent-workflow-orchestrator
      when: The service work is only one part of a larger end-to-end workflow.
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before using docs or source references.
    - skill: meshagent-participant-token-operator
      when: The main question is token-backed environment injection, participant identity, or service token wiring rather than generic service lifecycle.
    - skill: meshagent-queue-worker-builder
      when: The main task is authoring queue-consumer YAML.
    - skill: meshagent-webapp-backend-builder
      when: The main task is a website or public web application rather than service lifecycle.
    - skill: meshagent-runtime-operator
      when: The remaining issue is live container behavior rather than service definition.
  scope:
    owns:
      - service and service-template validation
      - service create, update, delete, show, list
      - room service listing and restart
    excludes:
      - detailed runtime debugging
      - queue, database, memory, or storage operations by themselves
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

# MeshAgent Service Operator

Use this skill when the task is primarily about MeshAgent services or service templates rather than one specific app running inside them.

## Use this skill when

- The user wants to create, update, list, show, validate, or delete a MeshAgent service.
- The task involves `meshagent service spec`, `create`, `update`, `validate`, or template commands.
- The user needs to render or validate a `ServiceTemplate`.
- The task involves room-scoped services through `meshagent room service list` or `restart`.
- The user needs to connect a YAML spec or template to an actual deployed service lifecycle.

## References

- Use `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact command shapes.
- Use `../_shared/references/live_room_cli_context.md` when the service workflow runs in or targets a known live room.
- Use `../_shared/references/runtime_image_environment_rules.md` when choosing or reviewing a service container image.
- Use `../_shared/references/service_yaml_correctness.md` when validating authored service YAML beyond basic shape.
- Inspect the resolved services CLI source for project/global/room service behavior, template rendering, and upsert rules.
- Inspect the resolved room-services CLI source for live room service listing and restart behavior.

## Related skills

- `meshagent-workflow-orchestrator`: Use it when the service work is only one part of a larger end-to-end workflow.
- `meshagent-sdk-researcher`: Resolve checkout roots before using docs or source references.
- `meshagent-participant-token-operator`: Use it when the issue is token-backed environment injection or participant-token wiring inside the service manifest.
- `meshagent-queue-worker-builder`: Use it when the main task is authoring queue-consumer YAML.
- `meshagent-webapp-backend-builder`: Use it when the main task is a website or public web application rather than service lifecycle.
- `meshagent-webmaster`: Use it when the main task is route and hostname management rather than service lifecycle.
- `meshagent-runtime-operator`: Use it when the remaining problem is live runtime behavior rather than service definition.

## Default workflow

1. Determine whether the task is about a raw `Service`, a `ServiceTemplate`, or a live room service already running in a room.
2. Read the existing YAML or list the current services before mutating anything.
3. When the asset is being authored, prefer a generated starting point instead of building the YAML from scratch:
   - `meshagent process spec` first for new authored agent services
   - `meshagent worker spec` or `meshagent mailbot spec` only when the user explicitly wants that runtime shape
   - `meshagent service spec` when the narrower runtime-specific specs are not the right fit
4. Validate or render the spec/template before create or update when a file is involved.
5. If validation fails, inspect the exact error, repair the asset, and rerun validation. Keep that fix-and-revalidate loop local to the service YAML until it passes or the remaining blocker is no longer a YAML problem.
6. Use the narrowest command path: `spec`, `validate`, `render-template`, `create`, `update`, `show`, `list`, `delete`, or room-service `restart`.
7. After mutation, verify the service record and, when relevant, the live room service state.
8. If the service is a queue consumer or other background runtime, hand off to runtime inspection before calling the deployment successful.

## Live room execution

- Apply `../_shared/references/live_room_cli_context.md` when the room is already known from runtime context or the user's request.
- Do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as prerequisite checks for room-scoped service work.
- If permissions are uncertain, start with `meshagent room service list --room <ROOM_NAME>` or another narrow room-scoped read before claiming service access is blocked.
- For service discovery, prefer `meshagent room service list` over generic toolkit invocation. Do not route ordinary service listing through `meshagent room agent invoke-tool --toolkit services --tool list --arguments '{}'` when the direct room command exists.

## Service scope rules

- Distinguish project/global services from room-scoped services before acting.
- Distinguish declarative service CRUD (`meshagent service ...`) from runtime room-service state (`meshagent room service ...`).
- Match the container image family to the actual MeshAgent environment. Do not copy a production docs image into a `.life` room unless the environment already proves that image family is correct there.
- Validate service YAML for workflow correctness, not just schema shape. Check command flags, mailbox identity, queue wiring, and whether the declared roles actually match the intended behavior.
- Prefer `validate` or `validate-template` before deployment when the source YAML is being authored or changed.
- If `validate` or `validate-template` fails, repair the YAML and rerun validation before moving on. Do not treat validation as a one-time gate or blindly retry without making a fix.
- Prefer `render-template` when the user needs to inspect the concrete resolved template output.
- Prefer generated specs or rendered templates over handwritten YAML when the runtime shape already has a CLI spec command.
- Treat `force` and `replace` as potentially destructive because they can redirect an existing service identity.

## Verification rules

- Do not claim a service is deployed correctly based only on YAML generation.
- After create or update, verify with `meshagent service show`, `meshagent service list`, or `meshagent room service list` as appropriate.
- When the question is simply "what services are running in this room?", `meshagent room service list` is the default answer path.
- For queue consumers, a visible service record is not enough. Confirm that the room service is present and then use runtime inspection to prove that a live runtime or container is actually running.
- If a room service is unhealthy, use room-service state and runtime inspection before rewriting the spec.
- If restart is requested, confirm the target by `--id` or `--name` before issuing it.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return service and live-room evidence to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- Detailed debugging inside running containers.
- Queue, database, memory, or storage operations except where needed to confirm service wiring.
