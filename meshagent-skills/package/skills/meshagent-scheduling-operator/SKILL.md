---
name: meshagent-scheduling-operator
description: Manage MeshAgent scheduled tasks and explain how they enqueue JSON payloads onto queues for later consumption.
---

# MeshAgent Scheduling Operator

Use this skill for `meshagent scheduled-task ...` workflows and for verifying the queue behavior they trigger.

## Use this skill when

- The user wants to add, inspect, update, pause, resume, or delete a scheduled task.
- The task involves a cron schedule or one-time dispatch through `meshagent scheduled-task ...`.
- The user needs to verify that a scheduled task is actually sending work into a queue.
- The user needs to connect scheduled dispatch to an existing queue consumer or service without designing that consumer.

## References

- Use `references/command_groups.md` and `references/meshagent_cli_help.md` for exact CLI command shapes and flags.

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

1. Resolve the active project, room, queue, and schedule.
2. Inspect existing scheduled tasks with `meshagent scheduled-task list`.
3. Confirm the exact queue name and JSON payload before mutating anything.
4. Create, update, or delete the scheduled task.
5. Verify the task state with `meshagent scheduled-task list`.
6. Verify the queue behavior with `meshagent room queue size` or `meshagent room queue receive`, or with the room queue API.

## Queue consumption

- CLI verification: use `meshagent room queue size --queue <QUEUE_NAME>` and `meshagent room queue receive --queue <QUEUE_NAME>`.
- API verification: use the room queues client, for example `message = await room.queues.receive(name="my-queue")`.
- When you need end-to-end proof, verify both the scheduled task definition and the resulting queued message.

## Service integration

- A service can be connected to a queue by attaching a queue channel such as `--channel queue:QUEUE_NAME` on the service runtime command when that runtime supports channels.
- That queue-service wiring is separate from scheduled-task configuration.
- Designing or implementing the queue consumer belongs in an agent-building workflow, not this skill.

## Operating rules

- Do not invent queue names.
- Do not claim that a scheduled task "works" just because the task exists; verify that messages reach the queue.
- Treat `update` and `delete` as destructive.
- Keep this skill focused on scheduling and queue verification, not on the implementation of the consumer.

## Out of scope

- General cron design that is not tied to an actual MeshAgent scheduled task.