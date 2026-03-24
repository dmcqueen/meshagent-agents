---
name: meshagent-queue-worker-builder
description: Build or update MeshAgent room queue-backed Worker YAML, especially Worker services that dequeue tasks in a room and process scheduled or queued jobs.
metadata:
  short-description: Build queue-backed Worker agent and service YAML for room jobs.
  references:
    bundled:
      - references/scheduled_email_worker.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - docs_root
      - examples_root
      - cli_root
    resolved_targets:
      - Worker examples
      - packaging docs
      - Worker CLI source
  related_skills:
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before following example or source references.
    - skill: meshagent-scheduler
      when: The remaining task is to create or verify a scheduled task after the Worker exists.
    - skill: meshagent-mail-operator
      when: The queued job sends email or depends on mailbox-backed sender identity.
    - skill: meshagent-service-operator
      when: The main task is service lifecycle rather than Worker YAML authoring.
    - skill: meshagent-runtime-operator
      when: The YAML exists but the remaining work is proving that the live Worker runtime actually dequeues and completes jobs.
  scope:
    owns:
      - queue-backed Worker YAML authoring
      - queue and schedule alignment in agent definitions
      - Worker service template adaptation from examples
    excludes:
      - scheduled-task CRUD
      - generic multi-channel agent design
      - low-level CLI command discovery
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

# MeshAgent Queue Worker Builder

Use this skill when the task is to create or update `meshagent.yaml` for a queue-backed MeshAgent Worker agent or Worker service template.

## Use this skill when

- The current workflow needs a Worker agent that consumes a queue in a room.
- The scheduler workflow needs a real queue consumer before a scheduled task can be added safely.
- The user needs a `meshagent.yaml` or service template that starts `meshagent worker join --queue=...`.
- The task involves fixing queue names, Worker annotations, container commands, or room-service YAML for dequeued jobs.
- The user wants a room worker that can be spun up, receive queued payloads, and process them with storage, tools, or other room capabilities.

## References

- After root resolution, start with the Worker examples under the resolved docs/examples tree:
  - `examples/cli/worker/meshagent.yaml` for the simplest queue-backed Worker service pattern
  - `examples/cli/multi-agent-news-reporter/meshagent.yaml` when a dedicated Worker cooperates with other agents in the same room
  - `examples/cli/meshagent-writer/meshagent.yaml` and `examples/cli/meshagent-codex-writer/meshagent.yaml` for scheduled writer workflows that rely on a Worker queue consumer
- Use `references/scheduled_email_worker.md` for workflows that must dequeue a message and send an email before a one-time schedule is considered complete.
- Use the resolved packaging docs for service-template structure and annotation semantics.
- Inspect the resolved Worker CLI source for the actual Worker flags and runtime shape.

## Related skills

- `meshagent-sdk-researcher`: Resolve the MeshAgent checkout roots and the exact example/source paths before using codebase references.
- `meshagent-scheduler`: Use it after the Worker exists and the task becomes scheduled-task creation, timezone resolution, or queue verification.
- `meshagent-mail-operator`: Use it when the queued job sends mail and must reuse a real mailbox-backed sender identity.
- `meshagent-service-operator`: Use it when the main job is validating, rendering, creating, or updating a service rather than authoring the Worker spec itself.
- `meshagent-runtime-operator`: Use it when the YAML exists but the remaining work is proving that the live Worker runtime is actually running, dequeuing, and completing the job.

## Default workflow

1. Determine whether the target is a new Worker service, a modification to an existing Worker template, or a repair to a broken queue/schedule setup.
2. Use `meshagent-sdk-researcher` to find the closest working example before drafting YAML.
3. Inspect the current room, current queue names, and existing service files so you can reuse real names and identities. If the CLI does not expose a dedicated queue-list command, use the room queue API or the current room configuration rather than assuming queue discovery is impossible.
4. If the queued job sends email, inspect or provision the mailbox first and reuse its address as the sender identity instead of inventing one.
5. Choose the nearest Worker example and adapt it instead of inventing a new template structure.
6. Make sure the Worker runtime explicitly consumes the intended queue with `meshagent worker join --queue=<QUEUE_NAME>`.
7. If the workflow is schedulable, make sure the schedule targets the same queue that the Worker consumes.
8. Validate the resulting YAML with the CLI when available.
9. Hand off to the service workflow to create or update the service, then verify the room service appears in live room state.
10. Hand off to the runtime workflow to prove the Worker runtime is alive with room developer output, container state, or logs.
11. Enqueue an immediate smoke-test message and confirm that the Worker dequeues it and completes the job before claiming the Worker is ready.
12. Only after the smoke test passes should you hand off to the scheduler skill for a one-time or recurring scheduled task.

## Worker service model

- Prefer a dedicated Worker agent with `meshagent.agent.type: "Worker"` when the job is queue-driven background work.
- The core runtime pattern is a container command that starts `meshagent worker join --agent-name=... --queue=...`.
- Treat the queue as the Worker's primary input channel. The Worker is useful only if something in the room actually sends payloads to that queue.
- Room storage mounts, toolkits, and rules should support the queued task behavior, not distract from it.

## Queue and scheduling rules

- Do not add a scheduled task to a Worker definition that lacks a matching queue consumer.
- The queue named inside `meshagent.agent.schedule` must match the queue consumed by `meshagent worker join --queue=...`.
- Prefer reusing an existing queue in the current room when it already represents the intended workflow.
- If there is no queue yet, define one explicitly and keep the name consistent across scheduler, sender, and Worker YAML.
- A queue channel or queue annotation alone is not enough. The runtime must show an actual queue-consuming path, normally `meshagent worker join --queue=...`, and the surrounding service/container setup must point at the same workflow.
- For one-time scheduled jobs, do not schedule first and hope the Worker path works later. Prove the Worker path with an immediate queue message before creating the scheduled task.

## What to build

- Prefer a room `Service` or `ServiceTemplate` that can be deployed into a room and stay available to dequeue tasks.
- Include the minimum container command, token identity, storage mounts, and Worker rule set required for the job.
- If the Worker needs storage, mail, web search, memory, or database access, add only the capabilities the actual task requires.
- Keep the Worker focused on consuming queue messages and completing the queued job.

## Verification and handoff rules

- Do not call the Worker complete based only on YAML generation or service creation.
- For a queue-backed Worker, success requires live room service evidence, live runtime evidence, and a successful immediate dequeue smoke test.
- If the Worker sends email, do not call the workflow complete until logs or other runtime evidence show that the message send succeeded or show the exact blocker.
- If the Worker runtime is missing, unhealthy, or not visibly dequeuing, switch to `meshagent-service-operator` and `meshagent-runtime-operator` before touching the schedule.
- If the immediate queue smoke test fails, do not create the scheduled task yet.

## Operating rules

- Do not invent undocumented annotation keys, runtime flags, or environment variables.
- Do not guess YAML structure when a nearby Worker example already covers the pattern.
- Prefer the simplest Worker example that satisfies the requested queued-job behavior.
- Preserve the parts that make dequeueing work: `meshagent.agent.type: "Worker"`, `meshagent worker join --queue=...`, and any required room/container setup.
- If the queued job sends email, use a real mailbox-backed sender identity from the current room instead of synthesizing a sender address.
- If the user only asked to schedule an already running agent and the current room lacks a queue-consuming Worker, stop the scheduler workflow and switch to this skill before claiming scheduling is possible.
- If the user actually needs a multi-channel process agent rather than a dedicated Worker, say so and use the more appropriate example instead of forcing a Worker pattern.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return worker, service, runtime, and smoke-test evidence to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- This skill does not replace the scheduler skill for creating or verifying scheduled tasks.
- This skill is not the default choice for chat-first, mail-first, or generic multi-channel agent authoring.
- This skill does not replace the CLI operator skill for command discovery and execution details.
