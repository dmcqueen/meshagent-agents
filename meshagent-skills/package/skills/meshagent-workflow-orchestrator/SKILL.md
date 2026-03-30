---
name: meshagent-workflow-orchestrator
description: Orchestrate end-to-end MeshAgent workflows that span multiple specialized skills. Use this skill when the user's goal crosses queues, workers, mail, services, runtime, scheduling, storage, or room web workflows and one skill must keep accountability for the final outcome.
metadata:
  short-description: Own cross-skill MeshAgent workflows from preflight through verified outcome.
  references:
    bundled:
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/environment_profile_rules.md
      - ../_shared/references/runtime_image_environment_rules.md
      - ../_shared/references/service_yaml_correctness.md
      - ../_shared/references/workflow_accountability.md
      - ../meshagent-cli-operator/references/command_groups.md
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
    requires_roots:
      - cli_root
      - docs_root
      - server_root
    resolved_targets:
      - shared live-room CLI context rules
      - shared runtime image environment rules
      - shared service YAML correctness rules
      - shared workflow accountability contract
      - command-group routing reference
      - packaged CLI help
  related_skills:
    - skill: meshagent-cli-operator
      when: Exact command routing or command syntax is the remaining question.
    - skill: meshagent-sdk-researcher
      when: The workflow depends on examples, docs, or code-path inspection from the MeshAgent checkout.
    - skill: meshagent-participant-token-operator
      when: The workflow depends on participant token discovery, token-backed env injection, delegated shell token behavior, or token minting.
    - skill: meshagent-queue-operator
      when: Queue inspection, send, receive, or backlog verification is needed.
    - skill: meshagent-queue-worker-builder
      when: The workflow needs a queue consumer or mail runtime service.
    - skill: meshagent-mail-operator
      when: Mailbox identity, room SMTP behavior, or outbound email verification is required.
    - skill: meshagent-service-operator
      when: Declarative service lifecycle or room service operations are required.
    - skill: meshagent-runtime-operator
      when: Live runtime, toolkit publication, logs, or container behavior must be proven.
    - skill: meshagent-scheduler
      when: Scheduled-task creation, timing, timezone resolution, or queue-schedule verification is required.
    - skill: meshagent-storage-operator
      when: Room storage copy, inspection, or path verification is required.
    - skill: meshagent-webapp-backend-builder
      when: The workflow includes room-hosted website or web-handler implementation.
    - skill: meshagent-webapp-dev-operator
      when: The workflow needs a hot-reload development loop for a room-hosted webapp backend.
    - skill: meshagent-webapp-release-operator
      when: The workflow needs an image-backed candidate, release, promotion, or rollback-ready room-webapp deploy.
    - skill: meshagent-webmaster
      when: Route or managed-hostname administration is required.
  scope:
    owns:
      - workflow ownership selection
      - preflight of required backend surfaces
      - cross-skill sequencing and completion gating
      - end-to-end evidence collection
    excludes:
      - deep domain execution when a narrower specialist skill is the right executor
      - low-level command syntax authoring without the CLI operator
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

# MeshAgent Workflow Orchestrator

Use this skill when the user's goal spans multiple MeshAgent domains and one skill needs to keep accountability for the whole outcome.

## Use this skill when

- The user asked for an end-to-end workflow rather than one isolated command or resource.
- The workflow crosses two or more of these surfaces: queues, workers, mail, services, runtime, scheduling, storage, or room-hosted web behavior.
- The task requires sequencing setup, verification, and handoffs across multiple specialized skills.
- The user wants a result like "make this work" or "set this up end to end" and the outcome depends on several components being correct together.

## References

- Use `../_shared/references/live_room_cli_context.md` when the workflow runs inside or targets a known live room.
- Use `../_shared/references/runtime_image_environment_rules.md` when the workflow includes service or worker image selection.
- Use `../_shared/references/service_yaml_correctness.md` when the workflow depends on authored `Service` or `ServiceTemplate` YAML.
- Use `../_shared/references/workflow_accountability.md` as the contract for ownership, handoffs, evidence, and forbidden shortcuts.
- Use `../meshagent-cli-operator/references/command_groups.md` when you need to route sub-steps to the right CLI family quickly.
- Use `../meshagent-cli-operator/references/meshagent_cli_help.md` when a sub-step depends on exact command shapes.

## Related skills

- `meshagent-cli-operator`: exact command routing and syntax
- `meshagent-sdk-researcher`: docs, examples, and source inspection
- `meshagent-participant-token-operator`: token sourcing and token-backed env wiring
- `meshagent-queue-operator`: queue send, receive, and backlog checks
- `meshagent-queue-worker-builder`: queue-consuming service YAML
- `meshagent-mail-operator`: mailbox, sender identity, and SMTP behavior
- `meshagent-service-operator`: service lifecycle and room service operations
- `meshagent-runtime-operator`: runtime state, toolkit publication, logs, and containers
- `meshagent-scheduler`: scheduled-task timing and queue alignment
- `meshagent-storage-operator`: room storage copy and path verification
- `meshagent-webapp-backend-builder`: room-hosted website and handler implementation
- `meshagent-webapp-dev-operator`: hot-reload dev loops for room-hosted webapp backends
- `meshagent-webapp-release-operator`: image-backed candidate and release workflow for room-hosted webapps
- `meshagent-webmaster`: routes and managed hostnames

## Core model

- Keep one owner for the whole user-visible result.
- Start with the narrowest action that could satisfy the request or expose the next blocker.
- Preflight only the surfaces needed for that next action.
- Use specialist skills for execution, but require evidence back from them.

## Default workflow

1. Restate the goal in one sentence and identify the current owner.
2. Pick the cheapest action that can move the workflow forward.
3. Identify only the surfaces needed for that step.
4. Check only the blockers that matter before the next risky or user-visible mutation.
5. Ask for missing inputs only when they are truly blocking.
6. Route the sub-step to the narrowest specialist skill.
7. Collect evidence after each mutation or handoff.
8. Re-evaluate the remaining gates.
9. Finish only when the remaining gates are satisfied.

## Operating rules

- Do not inventory every backend surface before the first useful action.
- For room-scoped work, apply `../_shared/references/live_room_cli_context.md` and start from the known room context.
- Do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as gatekeeper checks for known-room workflows.
- If service discovery is needed, prefer `meshagent room service list` over generic toolkit invocation.
- If a broad probe fails but a narrower room-scoped probe succeeds, continue and report the broad-scope limitation accurately.
- If the workflow depends on authored service YAML, prefer generated specs and require valid flags, roles, and wiring before treating the asset as deployable.
- If the workflow must choose a service image, derive the image family from the actual environment before copying an example.
- If a service runtime is under active iteration and changes should be containable, prefer a versioned image-build -> service-update -> verify -> rollback-if-needed loop over mutating the live runtime in place.
- If the user asks for a release candidate and does not explicitly ask to replace the current site, treat the candidate as a side-by-side deploy: separate service identity, separate candidate URL, and unchanged dev/stable URL.
- If the user asks for a release candidate without naming details, derive deterministic defaults from the current site or service instead of inventing arbitrary names: `<base>-rc` for candidate service and hostname, and the next `x.y-rcN` image tag in the active release line.
- If the workflow includes relative scheduling, make schedule creation the last mutation after the runtime path is proven.
- If the workflow includes real outbound email, require a real recipient unless the user explicitly asked for a payload-only template.
- If the workflow is active Python-handler iteration and the user needs hot reload or rapid preview feedback, keep backend implementation decisions with `meshagent-webapp-backend-builder` and route the runtime loop to `meshagent-webapp-dev-operator`.
- If the workflow asks for a release candidate, release, promotion, rollback, or image-backed web deploy, keep backend implementation decisions with `meshagent-webapp-backend-builder` and route packaging plus deploy lifecycle to `meshagent-webapp-release-operator`.
- If the workflow returns a managed public URL, require the hostname suffix to match the active API environment before treating that URL as valid output.
- If the workflow produces a wrong-suffix managed hostname for the active environment, stop immediately and repair the hostname. Do not spend time debugging downstream route, edge, or application behavior behind that invalid URL.
- If the workflow is a public site that sends email, inherit the webapp and mail completion rules together rather than relaxing either one at the orchestration layer.
- Apply the shared minimal change discipline from `../_shared/references/workflow_accountability.md` when the workflow modifies an existing working handler, service, or runtime.
- Apply the shared isolation-before-integration discipline from `../_shared/references/workflow_accountability.md` before approving a mixed patch to an existing working workflow.
- When the workflow is reacting to review or external implementation feedback, apply the shared review discipline from `../_shared/references/workflow_accountability.md` before mutating the workflow.
- If the workflow adds a new database write path to a live site or handler, route schema and `room.database.*` call-shape decisions to `meshagent-database-operator`, then let `meshagent-webapp-backend-builder` integrate the proven DB path into the live handler.
- If the workflow adds a new database write path to a live site or handler, require the DB insert path to be proven before accepting a larger mixed patch as the next step.
- If the workflow adds one new behavior to an existing handler, prefer helper-based integration with the smallest practical call-site change.
- If the request clearly includes ordinary prerequisite setup, do not stop to ask permission for that setup unless a real missing input remains.
- If a near-future one-time schedule is retried, treat duplicate creation as a workflow bug to avoid.

## Evidence rules

- Apply the shared debugging discipline from `../_shared/references/workflow_accountability.md` before deciding which specialist should change what.
- If repeated fixes fail on the same cross-surface workflow, stop widening the patch set and reassess the chosen design or integration path.
- Collect evidence by surface, not just by command.
- Prefer evidence like queue names, mailbox addresses, service ids, toolkit visibility, runtime logs, scheduled-task ids, or live URLs.
- Translate supporting-skill claims into concrete workflow-gate evidence before moving on.
- Name blockers by surface, for example scheduler permissions, missing toolkit publication, or unhealthy runtime.
- For mail workflows, do not let queue drain or object creation stand in for delivery evidence.
- For public-site workflows, do not let route creation, deploy success, DNS resolution, or redirects stand in for a verified working site.
- For a public site-to-email workflow, require all of the following before declaring success:
  - the active API environment is resolved clearly enough to state the expected managed hostname suffix
  - the managed hostname suffix matches the active API environment
  - the public URL reaches the intended page with the expected final success status, normally `200`
  - representative form submission paths behave as expected
  - the valid submission path shows real mail-send success or the exact SMTP/provider blocker

## Ownership rules

- Keep ownership here when the request is cross-surface and end-to-end.
- Transfer ownership only when the remainder is clearly inside one specialist skill.
- If ownership stays here, supporting skills return evidence rather than declaring the whole workflow complete.
- If ownership transfers, the new owner must continue tracking gates and evidence.

## Workflow accountability

- This skill should own the workflow when the goal spans multiple specialized skills.
- If another skill already owns the workflow and the remainder is now fully inside that narrower scope, transfer ownership explicitly.
- If this skill hands off without ownership transfer, keep accountability until the handoff returns evidence or an exact blocker.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- Acting as the only specialist for queue, mail, scheduler, runtime, or service details when a narrower skill already covers that work.
- Replacing the CLI operator for exact command syntax.
