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
      when: The workflow needs a queue-backed Worker or MailBot service.
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

- `meshagent-cli-operator`: Use it for exact command routing and execution details.
- `meshagent-sdk-researcher`: Use it when the workflow depends on examples, docs, or source inspection.
- `meshagent-participant-token-operator`: Use it when a workflow depends on participant token source, service token injection, delegated shell token behavior, or token minting.
- `meshagent-queue-operator`: Use it for queue discovery, send, receive, and backlog verification.
- `meshagent-queue-worker-builder`: Use it when the workflow needs a queue-backed Worker or MailBot.
- `meshagent-mail-operator`: Use it for mailbox provisioning, sender identity, and outbound mail behavior.
- `meshagent-service-operator`: Use it for declarative service lifecycle and room service operations.
- `meshagent-runtime-operator`: Use it to prove runtime state, toolkit publication, logs, or live container behavior.
- `meshagent-scheduler`: Use it for scheduled-task timing, timezone handling, and queue-schedule alignment.
- `meshagent-storage-operator`: Use it for room storage copy, inspection, and path verification.
- `meshagent-webapp-builder`: Use it for room-hosted websites, handlers, and public web verification.
- `meshagent-webmaster`: Use it for route and managed-hostname administration.

## Default workflow

1. Restate the user-visible goal in one sentence and identify the current likely workflow owner.
2. Choose the narrowest first action that could directly satisfy the request or expose the next blocker.
3. Identify only the surfaces needed for that first action, such as queue, mailbox, service, runtime, scheduler, or public web endpoint.
4. Preflight only the surfaces required before that next risky or user-visible step. If a required surface is blocked by `403`, `5xx`, or missing room capability, treat that as an early blocker for that branch.
5. Identify the concrete missing inputs, ask for them together only when they are truly blocking, and do not ask the user to restate the overall goal.
6. Choose the specialist skill that should execute the next sub-step, but keep workflow ownership unless you intentionally transfer it.
7. After each handoff, collect evidence rather than accepting a generic success claim.
8. Re-evaluate the remaining completion gates after every mutation or verification step.
9. Do not call the workflow complete until the final user-visible outcome is verified or the exact blocker is isolated.

## Fast path

- Start with one narrow task-matching action before surveying every dependent surface.
- For simple room asks, prefer the exact room-scoped read or mutation path that would satisfy the request directly.
- For larger workflows, the first step should still be the cheapest action that can prove whether the workflow is viable, not a full environment inventory.

## Escalate when

- The first narrow path fails or returns an ambiguous blocker.
- The next step depends on a new surface such as scheduler access, toolkit publication, mailbox ownership, or public route health.
- The workflow is about to make a mutation whose success depends on a backend surface that has not been checked yet.
- The user asked for an end-to-end verified outcome and the remaining completion gates require broader proof.

## Orchestration rules

- Prefer one owner and several supporting skills over bouncing ownership implicitly between specialists.
- Choose the narrowest specialist skill for execution, but keep orchestration here when the job spans multiple surfaces.
- Preflight cheap blockers early only when the currently chosen execution path actually depends on them.
- Do not start by inventorying room access, scheduler visibility, toolkit publication, service visibility, queue discovery, mailbox identity, and route readiness all at once when the user's first requested action only needs one of those surfaces.
- For room-scoped work, apply `../_shared/references/live_room_cli_context.md`, start from the known room context, and use the narrowest room-scoped probe first.
- Do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as prerequisite gatekeeper commands for a known-room workflow.
- If the workflow needs service discovery, prefer `meshagent room service list` over generic toolkit invocation because the direct room command is narrower and faster.
- If the workflow must choose a service or worker image, derive the image family from the actual MeshAgent environment before copying a docs example.
- If the workflow depends on authored service YAML, prefer a generated spec first and require command-flag correctness, role correctness, and wiring correctness before treating the asset as deployable.
- If a broad probe fails but a narrower room-scoped probe succeeds, continue the workflow and report the broad-scope limitation accurately instead of giving up.
- If the workflow includes a relative schedule such as "one minute from now," make scheduling the final creation step after the worker/runtime path has already been proven.
- If the workflow includes a real outgoing email, require a real recipient address unless the user explicitly asked for a payload-only template.
- If one branch of the workflow is healthy and another is blocked, report partial preparation clearly and keep the blocked surface attached to the overall outcome.
- If the user's request already clearly includes ordinary prerequisite setup, do not stop to ask for permission to do that setup unless a real missing input or blocker remains.
- If a near-future one-time schedule is being created, treat duplicate creation after retries as a workflow bug to avoid, not as an acceptable side effect.

## Evidence rules

- Collect evidence per surface, not just per command.
- Prefer evidence such as queue names, service ids, mailbox addresses, toolkit visibility, runtime logs, scheduled-task ids, or live URLs.
- When a supporting skill reports success, translate that into concrete workflow-gate evidence before moving on.
- If a blocker appears, name the blocked surface directly, for example scheduler permissions, missing toolkit publication, or unhealthy runtime.
- For delivered-email workflows, do not let queue drain or object creation stand in for mail-delivery evidence. Require runtime send evidence or clearly report that delivery is still unproven.

## Ownership transfer rules

- Keep ownership here when the user asked for a cross-surface end-to-end result.
- Transfer ownership only when the remainder of the job is now clearly inside one specialist skill's scope.
- If ownership transfers, say so in reasoning and make sure the new owner continues tracking completion gates and evidence.
- If ownership does not transfer, supporting skills should return evidence to this skill rather than declaring the whole workflow complete.

## Workflow accountability

- This skill should own the workflow outcome when the user's goal spans multiple specialized skills.
- If another skill already owns the workflow and the remaining task is now fully within that narrower scope, transfer ownership explicitly rather than keeping two implicit owners.
- If this skill hands off to another skill without ownership transfer, keep accountability for the original goal until the handoff returns evidence or an exact blocker.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- Acting as the only specialist for queue, mail, scheduler, runtime, or service details when a narrower skill already covers that work.
- Replacing the CLI operator for exact command syntax.
