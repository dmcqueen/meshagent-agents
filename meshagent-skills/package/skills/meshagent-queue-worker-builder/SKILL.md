---
name: meshagent-queue-worker-builder
description: Build or update MeshAgent room queue-backed Worker YAML, especially Worker services that dequeue tasks in a room and process scheduled or queued jobs.
metadata:
  short-description: Build queue-backed Worker agent and service YAML for room jobs.
  references:
    bundled:
      - references/scheduled_email_worker.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/process_agent_design.md
      - ../_shared/references/runtime_image_environment_rules.md
      - ../_shared/references/service_yaml_correctness.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - docs_root
      - examples_root
      - cli_root
    resolved_targets:
      - Worker examples
      - shared live-room CLI context rules
      - shared process-agent design rules
      - shared runtime image environment rules
      - shared service YAML correctness rules
      - packaging docs
      - Worker CLI source
  related_skills:
    - skill: meshagent-workflow-orchestrator
      when: The request spans Worker build, mail, runtime proof, and scheduling as one end-to-end workflow.
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before following example or source references.
    - skill: meshagent-participant-token-operator
      when: The remaining issue is token-backed environment wiring, delegated shell token behavior, or participant-token scope inside the Worker or MailBot runtime.
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
      - generic process-agent design across chat, mail, toolkit, and queue channels
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
  - `examples/cli/process-news-agent/meshagent.yaml` when a queue workflow is part of a larger process-backed agent design
  - `examples/cli/meshagent-writer/meshagent.yaml` and `examples/cli/meshagent-codex-writer/meshagent.yaml` for scheduled writer workflows that rely on a Worker queue consumer
- Use `references/scheduled_email_worker.md` for workflows that must dequeue a message and send an email before a one-time schedule is considered complete.
- Use `../_shared/references/live_room_cli_context.md` when the workflow runs in or targets a known live room.
- Use `../_shared/references/process_agent_design.md` when the user may really want one process-backed agent with queue plus other channels.
- Use `../_shared/references/runtime_image_environment_rules.md` when the workflow must choose a container image for a room worker or MailBot.
- Use `../_shared/references/service_yaml_correctness.md` when writing or repairing service YAML so command flags, mailbox wiring, and role composition stay valid.
- Use the resolved packaging docs for service-template structure and annotation semantics.
- Inspect the resolved Worker CLI source for the actual Worker flags and runtime shape.

## Related skills

- `meshagent-workflow-orchestrator`: Use it when the request spans Worker build, mail, runtime proof, and scheduling as one end-to-end workflow.
- `meshagent-sdk-researcher`: Resolve the MeshAgent checkout roots and the exact example/source paths before using codebase references.
- `meshagent-participant-token-operator`: Use it when the blocker is token-backed env injection, participant-token scope, or delegated shell token behavior inside the Worker or MailBot runtime.
- `meshagent-scheduler`: Use it after the Worker exists and the task becomes scheduled-task creation, timezone resolution, or queue verification.
- `meshagent-mail-operator`: Use it when the queued job sends mail and must reuse a real mailbox-backed sender identity.
- `meshagent-service-operator`: Use it when the main job is validating, rendering, creating, or updating a service rather than authoring the Worker spec itself.
- `meshagent-runtime-operator`: Use it when the YAML exists but the remaining work is proving that the live Worker runtime is actually running, dequeuing, and completing the job.

## Default workflow

1. Determine whether the target is a new Worker service, a modification to an existing Worker template, or a repair to a broken queue/schedule setup.
2. Use `meshagent-sdk-researcher` to find the closest working example before drafting YAML.
3. If the room is already known, apply `../_shared/references/live_room_cli_context.md` and start with narrow room-scoped probes rather than broad auth or project-listing commands.
4. Inspect the current room, current queue names, and existing service files so you can reuse real names and identities. If the CLI does not expose a dedicated queue-list command, use the room queue API or the current room configuration rather than assuming queue discovery is impossible.
5. If the queued job sends email, inspect or provision the mailbox first and reuse its address as the sender identity instead of inventing one.
6. If the Worker will call the `email` toolkit, prove that a live publisher for toolkit `email` already exists in the room or build one first. The normal pattern is a MailBot publishing `--toolkit-name=email`.
7. Prefer a generated asset shape over freehand YAML:
   - if the requested runtime is really one process-backed agent with queue plus other channels, switch to the process-agent design reference before authoring YAML
   - use `meshagent worker spec` for a dedicated Worker
   - use `meshagent mailbot spec` for a dedicated MailBot
   - use `meshagent service spec` only when a narrower agent-specific spec is not the right fit
8. Choose the nearest example and adapt it only after the generated or example shape is in hand.
9. Choose the container image family from the actual MeshAgent environment. Do not copy a production docs image into a `.life` room without checking the environment first.
10. Make sure the Worker runtime explicitly consumes the intended queue with `meshagent worker join --queue=<QUEUE_NAME>`.
11. If the workflow is schedulable, make sure the schedule targets the same queue that the Worker consumes.
12. Validate the resulting YAML against `../_shared/references/service_yaml_correctness.md`, including real CLI flag support, mailbox identity, queue wiring, mounted files, and whether the workflow needs both MailBot and Worker roles.
13. Validate the resulting YAML with `meshagent service validate` or `validate-template` and `render-template` when available.
14. If validation fails, inspect the exact error, repair the YAML, and rerun validation before attempting deployment.
15. Hand off to the service workflow to create or update the service, then verify the room service appears in live room state.
16. Hand off to the runtime workflow to prove the Worker runtime is alive with room developer output, container state, or logs.
17. Enqueue an immediate smoke-test message and confirm that the Worker dequeues it and completes the job before claiming the Worker is ready.
18. Only after the smoke test passes should you hand off to the scheduler skill for a one-time or recurring scheduled task.

## Worker service model

- Prefer a dedicated Worker agent with `meshagent.agent.type: "Worker"` when the job is queue-driven background work.
- The core runtime pattern is a container command that starts `meshagent worker join --agent-name=... --queue=...`.
- Treat the queue as the Worker's primary input channel. The Worker is useful only if something in the room actually sends payloads to that queue.
- Room storage mounts, toolkits, and rules should support the queued task behavior, not distract from it.
- If the Worker requires toolkit `email`, that toolkit must be published by some running room participant. A mailbox alone does not publish toolkit `email`.
- The normal email-toolkit pattern is a MailBot in the same room publishing `--toolkit-name=email`, then the Worker can use `--require-toolkit=email`.
- For non-trivial scheduled email workflows, prefer a durable setup that writes or mounts Worker rule files, then points the Worker at those rules with `--room-rules`.
- For new shared-identity queue-plus-mail workflows, follow `../_shared/references/process_agent_design.md` instead of inventing an ad hoc combined runtime shape.
- Use separate MailBot and Worker services only when the room architecture truly needs distinct participants or a dedicated Worker is clearly the better fit.
- If the Worker behavior lives in room-rules or startup-generated rule files, keep the scheduled payload thin and let it trigger that established workflow instead of restating the entire mail job ad hoc.

## Queue and scheduling rules

- Do not add a scheduled task to a Worker definition that lacks a matching queue consumer.
- The queue named inside `meshagent.agent.schedule` must match the queue consumed by `meshagent worker join --queue=...`.
- Prefer reusing an existing queue in the current room when it already represents the intended workflow.
- If there is no queue yet, define one explicitly and keep the name consistent across scheduler, sender, and Worker YAML.
- A queue channel or queue annotation alone is not enough. The runtime must show an actual queue-consuming path, normally `meshagent worker join --queue=...`, and the surrounding service/container setup must point at the same workflow.
- For one-time scheduled jobs, do not schedule first and hope the Worker path works later. Prove the Worker path with an immediate queue message before creating the scheduled task.
- The smoke-test payload should use the same payload style as the final scheduled task. If the scheduled run will enqueue a prompt-style instruction, smoke-test with a prompt-style instruction. If the scheduled run will enqueue structured fields, smoke-test with those same structured fields.

## What to build

- Prefer a room `Service` or `ServiceTemplate` that can be deployed into a room and stay available to dequeue tasks.
- Include the minimum container command, token identity, storage mounts, and Worker rule set required for the job.
- If the Worker needs storage, mail, web search, memory, or database access, add only the capabilities the actual task requires.
- Keep the Worker focused on consuming queue messages and completing the queued job.
- Prefer YAML that is generated or minimally edited from the real CLI spec commands over hand-written manifests assembled from scratch.

## Verification and handoff rules

- Do not call the Worker complete based only on YAML generation or service creation.
- For a queue-backed Worker, success requires live room service evidence, live runtime evidence, and a successful immediate dequeue smoke test.
- If the Worker uses `--require-toolkit=email`, verify that toolkit `email` is visible in the room before treating a non-dequeuing Worker as healthy. A Worker can wait on a missing required toolkit and never reach its queue-consume loop.
- If the Worker sends email, do not call the workflow complete until logs or other runtime evidence show that the message send succeeded or show the exact blocker.
- If the Worker runtime is missing, unhealthy, or not visibly dequeuing, switch to `meshagent-service-operator` and `meshagent-runtime-operator` before touching the schedule.
- If the immediate queue smoke test fails, do not create the scheduled task yet.

## Operating rules

- Do not invent undocumented annotation keys, runtime flags, or environment variables.
- Do not guess YAML structure when a nearby Worker example already covers the pattern.
- Prefer the simplest Worker example that satisfies the requested queued-job behavior.
- In a known live room, do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as prerequisite checks before room-scoped worker setup.
- Do not copy a docs example runtime image blindly. Match the worker or MailBot image family to the actual MeshAgent environment first.
- Do not emit a worker command with flags that `meshagent worker join` does not support. For worker instructions, use `--rule` or `--room-rules`, not invented flags like `--prompt`.
- Preserve the parts that make dequeueing work: `meshagent.agent.type: "Worker"`, `meshagent worker join --queue=...`, and any required room/container setup.
- If the queued job sends email, use a real mailbox-backed sender identity from the current room instead of synthesizing a sender address.
- Do not assume mailbox creation is enough to satisfy `--require-toolkit=email`. Mailbox provisioning and email-toolkit publication are separate concerns.
- For scheduled email workflows, do not point a standalone MailBot at the scheduled job queue and call that complete. The MailBot publishes toolkit `email`; the Worker consumes the scheduled job queue.
- For scheduled email workflows, do not declare both `MailBot` and `Worker` roles in one YAML asset unless you are intentionally repairing an existing combined deployment and the container command really starts both roles.
- When adapting a pattern like the news reporter example, keep the MailBot or equivalent toolkit publisher that makes `email` visible to the Worker. Do not copy only the Worker half of the pattern.
- For scheduled email workflows, make the scheduled payload match how the Worker was authored. A prompt-driven Worker should usually receive a prompt-driven scheduled payload. A structured-field Worker should receive those exact structured fields plus any required action field.
- If the user only asked to schedule an already running agent and the current room lacks a queue-consuming Worker, stop the scheduler workflow and switch to this skill before claiming scheduling is possible.
- If the user actually needs a process-backed agent with queue plus other channels rather than a dedicated Worker, say so and switch to `../_shared/references/process_agent_design.md` instead of forcing a Worker pattern.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return worker, service, runtime, and smoke-test evidence to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- This skill does not replace the scheduler skill for creating or verifying scheduled tasks.
- This skill is not the default choice for chat-first, mail-first, or generic process-agent authoring across multiple channels.
- This skill does not replace the CLI operator skill for command discovery and execution details.
