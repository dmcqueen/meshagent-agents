---
name: meshagent-runtime-operator
description: Operate and debug live MeshAgent room runtime state. Use this skill for developer log streaming, container listing/logs/exec/run/image operations, and local port forwarding into room containers.
metadata:
  short-description: Debug live room runtime state, containers, logs, and port forwarding.
  references:
    bundled:
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - cli_root
      - server_root
    resolved_targets:
      - shared live-room CLI context rules
      - developer CLI source
      - containers CLI source
      - port-forward CLI source
  related_skills:
    - skill: meshagent-workflow-orchestrator
      when: Runtime debugging is one part of a larger end-to-end workflow that still needs one owner.
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before using CLI or server source references.
    - skill: meshagent-participant-token-operator
      when: The remaining question is whether the runtime or shell actually received a participant token and where it came from.
    - skill: meshagent-queue-worker-builder
      when: The runtime to inspect is a queue consumer and the question is whether it actually dequeues or completes jobs.
    - skill: meshagent-service-operator
      when: The fix belongs in service definition or room service lifecycle rather than runtime debugging.
    - skill: meshagent-webapp-backend-builder
      when: The remaining issue is public web behavior rather than container state.
    - skill: meshagent-webapp-dev-operator
      when: The remaining issue is whether a room-webapp dev loop is hot-reloading Python handler changes correctly.
  scope:
    owns:
      - live runtime inspection
      - developer watch and container operations
      - local-to-container port forwarding
    excludes:
      - full service-template authoring
      - non-runtime queue, memory, database, or storage workflows
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

# MeshAgent Runtime Operator

Use this skill when the task is about the live runtime state inside a room rather than declarative YAML authoring.

## Use this skill when

- The user wants to inspect running containers in a room.
- The task involves `meshagent room developer watch`, `meshagent room container ...`, or `meshagent port forward`.
- The user needs container logs, container exec access, temporary container runs, image operations, or port forwarding for debugging.
- The workflow needs runtime diagnosis of a deployed service, worker, or website.

## References

- Use `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact command shapes.
- Use `../_shared/references/live_room_cli_context.md` when the runtime workflow runs in or targets a known live room.
- Inspect the resolved developer CLI source for log-streaming behavior.
- Inspect the resolved containers CLI source for container and image operations.
- Inspect the resolved port CLI source for local-to-container port forwarding.

## Related skills

- `meshagent-workflow-orchestrator`: end-to-end workflows with multiple surfaces
- `meshagent-sdk-researcher`: source and docs lookup
- `meshagent-participant-token-operator`: runtime token presence and delegated shell token behavior
- `meshagent-queue-worker-builder`: queue consumer behavior and runtime design
- `meshagent-mail-operator`: mailbox identity, toolkit `email`, and outbound mail behavior
- `meshagent-scheduler`: scheduler permissions, create/list health, and timing issues
- `meshagent-service-operator`: service definition and lifecycle fixes
- `meshagent-webapp-backend-builder`: public site behavior after runtime checks pass
- `meshagent-webapp-dev-operator`: dev-loop and hot-reload behavior for room-hosted webapp backends

## Live room execution

- Apply `../_shared/references/live_room_cli_context.md` when the room is already known from runtime context or the user's request.
- If permissions are uncertain, start with a narrow room-scoped read such as `meshagent room service list`, `meshagent room developer watch`, or `meshagent room container list` before claiming runtime access is blocked.

## Core workflow

1. Resolve the room and the runtime target: service, container, log stream, or port-forward target.
2. Start read-only: service list, toolkit visibility, developer watch, container list, container logs.
3. For queue workflows, check in order: service state, required toolkits, runtime logs, immediate smoke test, then scheduler or external-action proof.
4. Use `exec`, `run`, `stop`, or image operations only after the live state is clear.
5. If local inspection is needed, use port forwarding with an explicit target container and port.

## Operating rules

- Prefer `meshagent room service list` before container actions when the symptom is about a deployed service.
- Prefer `meshagent room developer watch` for room-wide telemetry and `meshagent room container log` for one container.
- Prefer `container list` before `log`, `exec`, `stop`, or `port forward` so you target the right container.
- Prefer `meshagent room agent list-toolkits` before concluding a runtime dependency such as toolkit `email` is missing.
- Do not use generic toolkit invocation for ordinary service discovery when `meshagent room service list` already answers the question.
- Treat `container stop` as disruptive.
- Treat `container exec` as debugging, not as a substitute for fixing the service definition.
- Do not assume `container exec` will work against another participant's private container.
- If `container exec` fails with a private-container ownership or isolation error, stop using exec for that target and switch to logs, developer watch, service state, public HTTP probes, or deployed artifacts.
- Use image build/pull/push/load/save only when the runtime problem actually requires image operations.
- For service-style iteration, image operations are primarily for versioned candidate builds and artifact checks. Rollback still happens at the service layer by updating the service back to a previous image tag.
- If the remaining problem is that a Python web handler change is not taking effect in a live dev loop, prefer `meshagent-webapp-dev-operator` over treating that as a generic runtime debugging problem.

## Queue and toolkit diagnosis

- Distinguish “service exists” from “runtime is ready.”
- If a runtime uses `--require-toolkit=<NAME>`, verify that toolkit is visibly published in the room.
- Do not assume mailbox, service, or queue creation also publishes a toolkit.
- For email workflows, separate three cases:
  - mailbox existence
  - a runtime with its own `mail:` channel
  - a queue-only runtime that depends on external toolkit `email`
- A process runtime with `--channel=mail:<MAILBOX_ADDRESS>` does not need a separate external toolkit `email` publisher to be viable.
- Only insist on visible toolkit `email` publication when the runtime actually depends on external `--require-toolkit=email`.
- Prefer an immediate smoke-test message over waiting for a future scheduled task when you need to prove dequeue behavior.
- A queue size of `0` is not enough by itself. Confirm whether the message was consumed successfully, failed during handling, or never arrived.
- If a smoke-test message remains queued, first match the investigation to the actual runtime design:
  - for `mail:` channel runtimes, check startup logs, service/container restart state, and live mail-send behavior
  - for queue-only `--require-toolkit=email` runtimes, check toolkit publication, startup logs, and restart state

## Cross-surface rules

- For queue-backed mail workflows with a process `mail:` channel, use this order: service list, developer watch, container list/logs, immediate smoke test, then mail-send evidence.
- For queue-backed mail workflows that intentionally use external `--require-toolkit=email`, use this order: service list, toolkit list, developer watch, container list/logs, immediate smoke test, then mail-send evidence.
- If the runtime path is healthy but scheduled runs fail, hand off to `meshagent-scheduler`.
- If scheduler create or list fails with `403` or `5xx`, report a scheduler blocker even when the runtime is healthy.
- If the runtime path is unhealthy, fix service state, required toolkits, or runtime readiness before spending time on scheduler diagnosis.

## Verification rules

- Apply the shared verification discipline from `../_shared/references/workflow_accountability.md`, then use runtime-specific evidence such as service state, toolkit visibility, logs, and processed test work.
- Apply the shared debugging discipline from `../_shared/references/workflow_accountability.md`, then use runtime-specific evidence to separate unhealthy service state, startup failure, toolkit absence, and post-start processing failures.
- Do not conclude that the runtime is healthy based only on service metadata.
- Use logs, running container state, toolkit visibility, and port-forwarded behavior to confirm what is actually happening.
- For queue-backed runtimes, do not conclude success until you have evidence that a test message was actually processed.
- For runtimes with required toolkits, do not conclude readiness until those toolkits are visibly present.
- For queue-backed mail runtimes with their own `mail:` channel, do not require a separate visible external `email` publisher unless the runtime also explicitly depends on one.
- If a container-local check passes but the public behavior is still broken, hand off to the appropriate website or route skill rather than stopping at the runtime layer.
- If a runtime issue persists after restart or stop/start behavior, inspect the declarative service definition before repeating the same action.
- For website debugging, do not use repeated `container exec` attempts against another private container as the main path to inspect handler code or env vars.

## Workflow accountability

- If another skill already owns the workflow, return runtime evidence and observed state to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- Full service-template authoring.
- Queue, memory, database, or storage workflows except where needed to debug the runtime symptom.
