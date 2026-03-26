---
name: meshagent-scheduler
description: Manage MeshAgent scheduled tasks and explain how they enqueue JSON payloads onto queues for later consumption.
metadata:
  short-description: Operate scheduled tasks, timezone conversion, and queue delivery verification.
  references:
    bundled:
      - ../meshagent-cli-operator/references/command_groups.md
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/process_agent_design.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - docs_root
      - cli_root
      - examples_root
    resolved_targets:
      - scheduled task CLI help
      - shared live-room CLI context rules
      - shared process-agent design rules
      - scheduled task examples
  related_skills:
    - skill: meshagent-workflow-orchestrator
      when: Scheduling is one step inside a larger queue, mail, service, or worker workflow.
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before using examples or source references.
    - skill: meshagent-queue-operator
      when: The task is generic queue inspection or queue injection outside scheduled-task management.
    - skill: meshagent-queue-worker-builder
      when: A queue-consuming runtime must be created or repaired before scheduling.
  scope:
    owns:
      - scheduled-task CRUD
      - timezone resolution for UTC storage
      - scheduled queue verification
    excludes:
      - queue consumer implementation
      - general cron guidance outside MeshAgent scheduled tasks
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

# MeshAgent Scheduler

Use this skill for `meshagent scheduled-task ...` work and for proving what those tasks actually enqueue.

The scheduler stores cron text only. Treat every stored schedule as UTC/GMT unless the implementation changes.

## Use this skill when

- The user wants to add, inspect, update, pause, resume, or delete a scheduled task.
- The task is about one-time or recurring queue dispatch through `meshagent scheduled-task ...`.
- The user needs proof that a scheduled task reaches a queue.
- The user already has, or is trying to target, a known queue consumer.

## References

- Use `../meshagent-cli-operator/references/command_groups.md` and `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact commands and flags.
- Use `../_shared/references/live_room_cli_context.md` for known live-room work.
- Use `../_shared/references/process_agent_design.md` when the target consumer is a process agent.

## Related skills

- `meshagent-workflow-orchestrator`: scheduling is only one step in a larger workflow.
- `meshagent-sdk-researcher`: resolve checkout roots before citing examples or source.
- `meshagent-queue-operator`: queue inspection or injection outside scheduled-task management.
- `meshagent-queue-worker-builder`: the room still lacks a real queue consumer.

## Primary command groups

- `meshagent scheduled-task add`
- `meshagent scheduled-task list`
- `meshagent scheduled-task update`
- `meshagent scheduled-task delete`
- `meshagent room queue receive`
- `meshagent room queue size`

## Core model

- A scheduled task only enqueues JSON onto a queue.
- It does not execute business logic directly.
- The workflow is only useful if some runtime actually consumes that queue.
- For scheduled email, the payload must clearly map to the runtime's email-sending rules. Do not assume the schedule itself "knows" to send email.

## Default workflow

1. Resolve the active project, room, queue, and intended execution time.
2. Resolve the requesting user's timezone.
3. Confirm that the target runtime really consumes the queue.
4. Preflight scheduler access with the narrowest matching read path, usually `meshagent scheduled-task list --room <ROOM_NAME>`.
5. For new queue-backed workflows, require a successful immediate smoke test before creating a near-future task.
6. For relative requests such as "in 2 minutes," anchor the time to the moment you are actually ready to create the task.
7. Confirm queue, payload, local execution time, timezone, and UTC cron before mutating anything.
8. Create, update, or delete the task.
9. Verify the stored task and the resulting queue behavior.

## Live room rules

- Apply `../_shared/references/live_room_cli_context.md`.
- If permissions are unclear, start with `meshagent scheduled-task list --room <ROOM_NAME>` or another narrow room-scoped scheduler probe.

## Scheduled email payloads

- The payload must explicitly request email sending in the style the queue consumer already expects.
- Good payloads either:
  - use an explicit prompt such as `Send an email to <RECIPIENT> using the email toolkit`, or
  - provide the exact structured fields the runtime rules already require, such as `to`, `subject`, `body`, and any required action field.
- If the runtime is built around durable room-rules workflows, a prompt that tells it to run that workflow is usually safer than ad hoc JSON fields.
- Keep the mailbox inbox path separate from the scheduled job queue unless the implementation clearly requires them to be the same.
- If the payload-to-runtime mapping is ambiguous, fix the runtime or the payload before scheduling.

## Timezone rules

- Prefer an explicit IANA timezone such as `America/Los_Angeles` or `Asia/Bangkok`.
- Do not use the room, server, or agent runtime timezone as a proxy for the requesting user unless you know they are the same.
- If no timezone was provided, use the best reliable user-specific signal first:
  - current session or client-local timezone
  - explicit user timezone or location
  - recent user-specific context
  - only then weaker defaults
- Ask the user only when no credible user-specific basis exists.
- Relative requests such as `in 2 minutes` need a credible current-user `now`.
- Absolute requests such as `9 AM every day` need the intended local timezone itself to be correct.
- Always restate the timezone assumption and the UTC conversion before creating or changing the task.
- Build cron fields from the converted UTC timestamp itself, not from the user's local clock fields.

## One-time task guard

- Restate the exact local time and exact UTC time before creating a one-time task.
- Use absolute times in the explanation, not only relative phrasing.
- Recompute relative times after setup if deployment or smoke testing took long enough to matter.
- Keep a real safety margin so the stored UTC minute is still in the future.
- Before `add`, check for an equivalent near-future task so you do not create duplicates after retries.
- If the first `add` may already have succeeded, inspect before retrying.
- If setup consumed too much of the original window, move the task to the next safe future time and say so.

## Scheduler preflight

- For room-scoped work, prefer `meshagent scheduled-task list --room <ROOM_NAME>` over an unfiltered project-wide `list`.
- A project-wide `list` can require broader permissions than a room-scoped workflow.
- If room-scoped `list --room` fails with `403`, treat scheduler visibility for that room as blocked.
- If only the unfiltered project-wide `list` fails with `403`, do not assume the room-scoped path is blocked too.
- If `list` or `add` returns an unexpected `5xx`, treat the scheduler backend as unhealthy until proven otherwise.
- If preflight already failed, do not present the workflow as fully completable.

## Queue checks

- Apply the shared verification discipline from `../_shared/references/workflow_accountability.md`, then use the scheduler-specific rules below for what counts as proof here.
- Apply the shared debugging discipline from `../_shared/references/workflow_accountability.md`, then use the scheduler-specific rules below to separate schedule-definition, queue-delivery, consumer, and downstream-send failures.
- Verify queue behavior with `meshagent room queue size --queue <QUEUE_NAME>` and `meshagent room queue receive --queue <QUEUE_NAME>`.
- If the queue name is unknown, prefer room toolkit invocation or the room queue API over ad hoc SDK code.
- Do not say queue listing is impossible just because the CLI lacks a dedicated room-queue list subcommand.
- For end-to-end proof, verify both the scheduled task definition and the queued message.
- Queue delivery alone is still not enough when the queued workflow must send email or perform another external action.

## Queue consumer checks

- In a process agent, `meshagent process join` plus `--channel=queue:<QUEUE_NAME>` is the normal queue-consuming path.
- If the user explicitly asked for a dedicated Worker runtime, `meshagent worker join --queue=<QUEUE_NAME>` is valid too.
- Queue-looking metadata alone is not enough; the startup command must show the real queue-consuming runtime.
- If the current agent already consumes a matching queue, reuse it.
- If the room still lacks a confirmed queue consumer, hand off to `meshagent-queue-worker-builder` instead of inventing one here.

## Operating rules

- Do not invent queue names.
- Do not invent timezones.
- Do not pass a human-readable `--id`; omit it unless you already have a real UUID.
- Do not schedule a near-future task until the queue consumer has passed an immediate smoke test.
- Do not anchor a relative request to the start of a long setup workflow.
- Treat `update` and `delete` as destructive.
- Keep this skill focused on scheduling and queue verification, not consumer implementation.

## Workflow accountability

- If another skill already owns the workflow, return schedule, queue, and timing evidence to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- General cron design that is not tied to an actual MeshAgent scheduled task.
