---
name: meshagent-workflow-orchestrator
description: Orchestrate end-to-end MeshAgent workflows that span multiple specialized skills. Use this skill when the user's goal crosses queues, workers, mail, services, runtime, scheduling, storage, or room web workflows and one skill must keep accountability for the final outcome.
metadata:
  short-description: Own cross-skill MeshAgent workflows from preflight through verified outcome.
  references:
    bundled:
      - ../_shared/references/live_room_cli_context.md
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
    - skill: meshagent-webapp-builder
      when: The workflow includes a room-hosted website, web handler, or public web verification.
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
- `meshagent-webapp-builder`: room-hosted websites and handlers
- `meshagent-webmaster`: routes and managed hostnames

## Core model

- Keep one owner for the whole user-visible result.
- Start with the narrowest action that could satisfy the request or expose the next blocker.
- Preflight only the surfaces needed for that next action.
- Use specialist skills for execution, but require evidence back from them.
- Do not call the workflow complete until the final result is verified or the exact blocker is isolated.

## Default workflow

1. Restate the goal in one sentence and identify the current owner.
2. Pick the cheapest action that can move the workflow forward.
3. Identify only the surfaces needed for that step.
4. Check only the blockers that matter before the next risky or user-visible mutation.
5. Ask for missing inputs only when they are truly blocking.
6. Route the sub-step to the narrowest specialist skill.
7. Collect evidence after each mutation or handoff.
8. Re-evaluate the remaining gates.
9. Finish only when the user-visible outcome is proven or the blocker is exact.

## Operating rules

- Do not inventory every backend surface before the first useful action.
- For room-scoped work, apply `../_shared/references/live_room_cli_context.md` and start from the known room context.
- Do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as gatekeeper checks for known-room workflows.
- If service discovery is needed, prefer `meshagent room service list` over generic toolkit invocation.
- If a broad probe fails but a narrower room-scoped probe succeeds, continue and report the broad-scope limitation accurately.
- If the workflow depends on authored service YAML, prefer generated specs and require valid flags, roles, and wiring before treating the asset as deployable.
- If the workflow must choose a service image, derive the image family from the actual environment before copying an example.
- If the workflow includes relative scheduling, make schedule creation the last mutation after the runtime path is proven.
- If the workflow includes real outbound email, require a real recipient unless the user explicitly asked for a payload-only template.
- If the request clearly includes ordinary prerequisite setup, do not stop to ask permission for that setup unless a real missing input remains.
- If a near-future one-time schedule is retried, treat duplicate creation as a workflow bug to avoid.

## Evidence rules

- Collect evidence by surface, not just by command.
- Prefer evidence like queue names, mailbox addresses, service ids, toolkit visibility, runtime logs, scheduled-task ids, or live URLs.
- Translate supporting-skill claims into concrete workflow-gate evidence before moving on.
- Name blockers by surface, for example scheduler permissions, missing toolkit publication, or unhealthy runtime.
- For mail workflows, do not let queue drain or object creation stand in for delivery evidence.

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
