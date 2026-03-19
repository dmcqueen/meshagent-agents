---
name: meshagent-scheduling-operator
description: Operate MeshAgent scheduled-task workflows that support the current room or a clearly scoped project workflow. Use this skill for adding, listing, updating, verifying, and deleting MeshAgent scheduled tasks.
---

# MeshAgent Scheduling Operator

Use this skill for `meshagent scheduled-task ...` workflows.

## Use this skill when

- The user wants to add, inspect, update, pause, resume, or delete a scheduled task.
- The task involves a cron schedule, recurring dispatch, or one-time queued execution through `meshagent scheduled-task ...`.
- The user wants to connect scheduled execution to a room queue or room workflow.

## Shared runtime

Use the room runtime defined in `../meshagent-cli-operator/SKILL.md`.

- Use the companion references in `../meshagent-cli-operator/references/command_groups.md` and `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact command shapes and flags.

## Primary command group

- `meshagent scheduled-task add`
- `meshagent scheduled-task list`
- `meshagent scheduled-task update`
- `meshagent scheduled-task delete`

## Operating rules

- Treat scheduling as project-scoped configuration that must remain tightly tied to a specific room workflow, queue, or operational need.
- Confirm the target project context before making changes. If a task is meant for the current room workflow, prefer `--room "${MESHAGENT_ROOM}"` when the command supports it.
- Identify the exact target queue before adding or updating a task. Do not invent queue names.
- Use `meshagent scheduled-task list` first when the task might already exist.
- Prefer the smallest change that satisfies the request: update an existing task instead of creating a duplicate when the target task is clearly the same workflow.
- If the schedule is ambiguous, stop and resolve the intended cron expression before mutating anything.
- For `--payload` or `--payload-file`, ensure the payload is valid JSON before sending it to the CLI.
- Use `--once` only when the user clearly wants one-time execution followed by deactivation.
- Use `--inactive` for staged setup when the user wants a task created but not yet running.
- Treat `update` and `delete` as destructive. Confirm the exact task id and blast radius before executing them.
- Do not claim success until you verify with `meshagent scheduled-task list` or another corresponding read command.
- Do not broaden a simple scheduling request into a larger worker, reporting, or orchestration system unless the user explicitly asks for that architecture.

## Default workflow

1. Resolve the active project and room context.
2. Inspect existing tasks with `meshagent scheduled-task list`, usually filtered by `--room`, `--task-id`, or both.
3. Confirm the queue, cron schedule, payload, and desired active state.
4. Apply the narrowest mutation with `add`, `update`, or `delete`.
5. Verify the resulting state with `meshagent scheduled-task list` and summarize the exact task id, room, queue, schedule, and active state.

## Command-specific guidance

### Add

- Use `meshagent scheduled-task add` when a new scheduled task is required.
- Supply a real queue with `--queue` and a real cron expression with `--schedule`.
- Use `--id` only when a stable caller-controlled id is clearly useful.
- If the task is for the current room workflow, include `--room "${MESHAGENT_ROOM}"` unless the user explicitly asks for a different room-scoped target.

### List

- Use `meshagent scheduled-task list` before and after mutation.
- Prefer filtering by `--room`, `--task-id`, `--active`, or `--inactive` to avoid ambiguous results.
- Use `--output json` when you need stable parsing or exact field verification.

### Update

- Use `meshagent scheduled-task update TASK_ID` when modifying schedule, queue, room, payload, or active state.
- Prefer updating the existing task instead of creating a second task for the same workflow.
- Restate the exact task id and intended changes before mutating.

### Delete

- Use `meshagent scheduled-task delete TASK_ID` only when the user explicitly wants removal.
- Verify the task id with a read command first.
- Re-run `list` afterward to confirm the task is gone.

## Out of scope

- Do not use this skill for general-purpose cron design that is not tied to an actual MeshAgent scheduled task.
- Do not use this skill for mailbox, inbox, or MailBot workflows; use `meshagent-mail-operator` for those.
- Do not use this skill for generic room runtime deployment; use `meshagent-cli-operator` for that.
