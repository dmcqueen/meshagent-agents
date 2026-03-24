---
name: meshagent-scheduler
description: Manage MeshAgent scheduled tasks and explain how they enqueue JSON payloads onto queues for later consumption.
metadata:
  short-description: Operate scheduled tasks, timezone conversion, and queue delivery verification.
  references:
    bundled:
      - ../meshagent-cli-operator/references/command_groups.md
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../_shared/references/workflow_accountability.md
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
5. For a new queue-backed workflow, verify that the queue consumer has already passed an immediate smoke test before creating a one-time or near-future scheduled task.
6. If the user expressed the schedule relatively, such as "one minute from now," anchor that relative time to the moment you are actually ready to create the scheduled task, not to the beginning of the broader setup workflow.
7. Confirm the exact queue name, JSON payload, local execution time, timezone, and UTC cron expression before mutating anything.
8. Create, update, or delete the scheduled task.
9. Verify the task state with `meshagent scheduled-task list`.
10. Verify the queue behavior with `meshagent room queue size` or `meshagent room queue receive`, or with the room queue API.

## Timezone resolution

- Do not assume the user's local timezone from the cron expression alone.
- Prefer an explicit IANA timezone such as `America/Los_Angeles` or `Asia/Bangkok`.
- If the user already gave a timezone, use it and restate the UTC conversion you will schedule.
- If no timezone was provided, first look up the current local timezone from the environment or system clock.
- If the current timezone is still ambiguous, if the task is for a different region, or if DST boundaries matter, ask the user to confirm the intended timezone before scheduling.
- Convert the requested local time into the exact UTC cron expression that will be stored.
- When the request is tied to a named local timezone that observes DST, explain that the current scheduler stores UTC cron only, so the UTC schedule may need seasonal adjustment.

## One-time scheduling guard

- Restate the exact local scheduled time and the exact UTC time before creating a one-time task.
- Use absolute times in the explanation, not just "one minute from now" or similar relative phrasing.
- Interpret relative requests such as "one minute from now" relative to the actual `meshagent scheduled-task add` moment after setup is complete, not relative to the original user message timestamp.
- If setup, deployment, or smoke testing took longer than expected, recompute the relative time from the current moment before creating the scheduled task.
- If setup, deployment, or smoke testing has consumed most of the time window, move the one-time run farther into the future instead of leaving it effectively in the past.
- Do not create a near-future one-time task until the queue consumer path is already proven with an immediate smoke test.
- If the user asked for "a minute from now" but the workflow is not yet ready, explain that you are moving the one-time run to the next safe minute window rather than pretending the original time still makes sense.

## Queue consumption

- CLI verification: use `meshagent room queue size --queue <QUEUE_NAME>` and `meshagent room queue receive --queue <QUEUE_NAME>`.
- For queue-name discovery, prefer `meshagent room agent list-toolkits` and `meshagent room agent invoke-tool --toolkit queues --tool list --arguments '{}'` before writing SDK code.
- API verification: use the room queues client, for example `queues = await room.queues.list()` or `message = await room.queues.receive(name="my-queue")`.
- The current CLI does not expose a dedicated `meshagent room queue list` subcommand. If the queue name is unknown, use the room queue API or inspect room configuration rather than claiming queue discovery is impossible.
- When you need end-to-end proof, verify both the scheduled task definition and the resulting queued message. For mail-sending workers, this is still not enough by itself; runtime mail-send evidence must also be checked.

## Current agent queue discovery

- If this skill is running inside a live MeshAgent room runtime, first inspect the current room and current agent before inventing a queue or assuming a separate worker exists.
- If the queue name is not already known from the scheduled task, service config, mailbox config, or Worker config, first try generic CLI toolkit invocation to enumerate visible queues, then use the room queue API if needed.
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
- Do not say queue names cannot be listed just because the CLI lacks a dedicated `meshagent room queue list` subcommand.
- For “what queues are available?” questions, prefer generic CLI toolkit invocation over ad hoc SDK code.
- Do not invent timezones.
- Do not schedule a task until the timezone has been confirmed or reliably detected.
- Do not schedule a near-future one-time task until the queue consumer has already passed an immediate smoke test.
- Do not anchor a relative scheduling request to the beginning of a longer setup workflow when the user's intent is relative to the actual task-creation moment.
- Do not schedule the current running agent unless you have confirmed that it already consumes the target queue.
- Do not treat a bare `queue:` channel as proof of consumption unless the runtime clearly shows how it dequeues that queue.
- Always state the timezone assumption and the resulting UTC schedule when adding or updating a task.
- Do not claim that a scheduled task "works" just because the task exists; verify that messages reach the queue.
- Do not treat queue delivery alone as end-to-end success when the queued workflow must send email or perform another externally visible action.
- Treat `update` and `delete` as destructive.
- Keep this skill focused on scheduling and queue verification, not on the implementation of the consumer.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return schedule, queue, and timing evidence to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- General cron design that is not tied to an actual MeshAgent scheduled task.
