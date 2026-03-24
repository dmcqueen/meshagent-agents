---
name: meshagent-scheduler
description: Manage MeshAgent scheduled tasks and explain how they enqueue JSON payloads onto queues for later consumption.
metadata:
  short-description: Operate scheduled tasks, timezone conversion, and queue delivery verification.
  references:
    bundled:
      - ../meshagent-cli-operator/references/command_groups.md
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
    requires_roots:
      - docs_root
      - cli_root
      - examples_root
    resolved_targets:
      - scheduled task CLI help
      - scheduled task examples
  related_skills:
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before using examples or source references.
    - skill: meshagent-queue-operator
      when: The task is generic queue inspection or queue injection outside scheduled-task management.
    - skill: meshagent-queue-worker-builder
      when: A queue-consuming Worker must be created or repaired before scheduling.
  scope:
    owns:
      - scheduled-task CRUD
      - timezone resolution for UTC storage
      - scheduled queue verification
    excludes:
      - queue consumer implementation
      - general cron guidance outside MeshAgent scheduled tasks
---

# MeshAgent Scheduler

Use this skill for `meshagent scheduled-task ...` workflows and for verifying the queue behavior they trigger.

The scheduler currently stores cron text only. Treat every schedule as a UTC/GMT schedule unless the implementation changes.

## Use this skill when

- The user wants to add, inspect, update, pause, resume, or delete a scheduled task.
- The task involves a cron schedule or one-time dispatch through `meshagent scheduled-task ...`.
- The user needs to verify that a scheduled task is actually sending work into a queue.
- The user needs to connect scheduled dispatch to an existing queue consumer or service without designing that consumer.

## References

- Use `../meshagent-cli-operator/references/command_groups.md` and `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact command shapes and flags.

## Related skills

- `meshagent-sdk-researcher`: Resolve checkout roots before using examples or implementation references.
- `meshagent-queue-operator`: Use it when the task is queue inspection or queue injection outside scheduled-task management.
- `meshagent-queue-worker-builder`: Use it when a queue-consuming Worker or other explicit queue consumer must be built before scheduling can be claimed to work.

## Primary command groups

- `meshagent scheduled-task add`
- `meshagent scheduled-task list`
- `meshagent scheduled-task update`
- `meshagent scheduled-task delete`
- `meshagent room queue receive`
- `meshagent room queue size`

## Delivery model

- A scheduled task does not execute business logic directly.
- It enqueues a JSON payload onto the configured queue on the requested schedule.
- The scheduled workflow is only end-to-end useful when something else consumes that queue.

## Default workflow

1. Resolve the active project, room, queue, and intended local execution time.
2. Resolve the user's timezone before setting or changing a schedule.
3. Inspect the current room and current agent context to determine whether the running agent already has an explicit queue-consuming path.
4. Inspect existing scheduled tasks with `meshagent scheduled-task list`.
5. Confirm the exact queue name, JSON payload, timezone, and UTC cron expression before mutating anything.
6. Create, update, or delete the scheduled task.
7. Verify the task state with `meshagent scheduled-task list`.
8. Verify the queue behavior with `meshagent room queue size` or `meshagent room queue receive`, or with the room queue API.

## Timezone resolution

- Do not assume the user's local timezone from the cron expression alone.
- Prefer an explicit IANA timezone such as `America/Los_Angeles` or `Asia/Bangkok`.
- If the user already gave a timezone, use it and restate the UTC conversion you will schedule.
- If no timezone was provided, first look up the current local timezone from the environment or system clock.
- If the current timezone is still ambiguous, if the task is for a different region, or if DST boundaries matter, ask the user to confirm the intended timezone before scheduling.
- Convert the requested local time into the exact UTC cron expression that will be stored.
- When the request is tied to a named local timezone that observes DST, explain that the current scheduler stores UTC cron only, so the UTC schedule may need seasonal adjustment.

## Queue consumption

- CLI verification: use `meshagent room queue size --queue <QUEUE_NAME>` and `meshagent room queue receive --queue <QUEUE_NAME>`.
- API verification: use the room queues client, for example `message = await room.queues.receive(name="my-queue")`.
- When you need end-to-end proof, verify both the scheduled task definition and the resulting queued message.

## Current agent queue discovery

- If this skill is running inside a live MeshAgent room runtime, first inspect the current room and current agent before inventing a queue or assuming a separate worker exists.
- First look for an explicit queue-consuming runtime such as `meshagent worker join --queue=<QUEUE_NAME>` in the current startup command or service template.
- If the runtime is not a Worker, a queue channel such as `--channel=queue:<QUEUE_NAME>` is only supporting evidence. Treat it as sufficient only when the runtime and surrounding implementation clearly consume that queue.
- Also inspect agent annotations or nearby service YAML when the current runtime was created from a template. The schedule queue and the actual consumer path must match.
- If the current agent already consumes a queue in the current room, reuse that queue for scheduling the current agent.
- If the current agent does not already consume a queue, do not claim that scheduling the current running agent is possible yet.
- If the queue-consuming path is ambiguous, inspect the actual service template, startup command, or room-visible agent files before asking the user or choosing a queue name.

## Service integration

- A service may expose queue channels such as `--channel=queue:QUEUE_NAME`, but channel wiring alone does not prove the runtime actually dequeues work.
- Scheduled-task configuration must match the queue that the runtime really consumes.
- Designing or implementing the queue consumer belongs in an agent-building workflow, not this skill.

## Handoff to agent building

- If the current room already has an agent with a matching explicit queue consumer, stay in this skill and schedule against that queue.
- If the current agent does not have an explicit queue consumer, hand off to the `meshagent-queue-worker-builder` skill instead of inventing a queue consumer here.
- The `meshagent-queue-worker-builder` skill should construct or update `meshagent.yaml` so the agent consumes a queue and can be scheduled.
- When handing off, direct that skill to use `meshagent-sdk-researcher` first to inspect the nearest MeshAgent examples and packaging docs before writing YAML.
- Relevant examples are the resolved process-news-agent, multi-agent-news-reporter, and meshagent-writer examples under the docs/examples tree.

## Operating rules

- Do not invent queue names.
- Do not invent timezones.
- Do not schedule a task until the timezone has been confirmed or reliably detected.
- Do not schedule the current running agent unless you have confirmed that it already consumes the target queue.
- Do not treat a bare `queue:` channel as proof of consumption unless the runtime clearly shows how it dequeues that queue.
- Always state the timezone assumption and the resulting UTC schedule when adding or updating a task.
- Do not claim that a scheduled task "works" just because the task exists; verify that messages reach the queue.
- Treat `update` and `delete` as destructive.
- Keep this skill focused on scheduling and queue verification, not on the implementation of the consumer.

## Out of scope

- General cron design that is not tied to an actual MeshAgent scheduled task.
