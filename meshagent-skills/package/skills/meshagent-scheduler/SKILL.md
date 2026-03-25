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
- Use `../_shared/references/live_room_cli_context.md` when the scheduling workflow runs in or targets a known live room.
- Use `../_shared/references/process_agent_design.md` when the queue target may really be a process-backed agent with queue plus other channels.

## Related skills

- `meshagent-workflow-orchestrator`: Use it when scheduling is only one step inside a larger end-to-end workflow.
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
- For scheduled email workflows, the payload itself should explicitly tell the Worker to send the email or should carry the fields the Worker's rules require for email sending. Do not assume the schedule "knows" to send mail just because the queue consumer has access to toolkit `email`.
- For straightforward scheduled email requests, treat sender provisioning as part of the workflow build, not as extra user input, unless the user explicitly asked to choose the sender identity.

## Default workflow

1. Resolve the active project, room, queue, and intended local execution time.
2. Resolve the requesting user's timezone before setting or changing a schedule.
3. Inspect the current room and current agent context to determine whether the running agent already has an explicit queue-consuming path.
4. Preflight scheduled-task capability before presenting the workflow as end-to-end ready: for a room-scoped workflow, inspect existing scheduled tasks with `meshagent scheduled-task list --room <ROOM_NAME>` first. Treat a permissions failure, `403`, or unexpected `5xx` as a real blocker only after using the narrowest room-scoped read path that matches the workflow.
5. For a new queue-backed workflow, verify that the queue consumer has already passed an immediate smoke test before creating a one-time or near-future scheduled task.
6. If the user expressed the schedule relatively, such as "one minute from now," anchor that relative time to the moment you are actually ready to create the scheduled task, not to the beginning of the broader setup workflow.
7. If you plan to pass `--id`, make sure it is a real UUID. Otherwise omit `--id` and let the server generate the task id.
8. Confirm the exact queue name, JSON payload, requesting-user local execution time, timezone, and UTC cron expression before mutating anything.
9. Create, update, or delete the scheduled task.
10. If `add` has an uncertain result because of timeout, transport noise, or retry pressure, verify with `meshagent scheduled-task list` before issuing another `add`.
11. Verify the task state with `meshagent scheduled-task list`.
12. Verify the queue behavior with `meshagent room queue size` or `meshagent room queue receive`, or with the room queue API.

## Live room execution

- Apply `../_shared/references/live_room_cli_context.md` when the room is already known from runtime context or the user's request.
- Do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as prerequisite checks for room-scoped scheduling work.
- If permissions are uncertain, start with `meshagent scheduled-task list --room <ROOM_NAME>` or another narrow room-scoped scheduler probe before claiming scheduling is blocked.

## Payload design for scheduled email workflows

- A scheduled task only enqueues payload. It does not implicitly request email sending.
- If the target workflow is "send an email later," design the payload so the Worker can clearly infer that it must use toolkit `email`.
- Good scheduled email payloads either:
  - include an explicit prompt such as "Send an email to <RECIPIENT> using the email toolkit", or
  - include the exact structured fields the Worker rules already require, such as `to`, `subject`, `body`, and any other required action field.
- If the Worker was authored around mounted or room-rules workflow files, a prompt that tells it to run that established workflow is usually the safer scheduled payload than ad hoc JSON fields.
- The `industry-report` nightly-report Worker is the preferred model for non-trivial scheduled email/report jobs: durable worker rules plus a scheduled prompt that tells the Worker to run that workflow.
- Keep the MailBot inbox path separate from the scheduled Worker queue. The mailbox-backed MailBot should normally consume the mailbox email address as its queue, while the scheduled Worker consumes its own job queue.
- Do not rely on a generic payload like `{"message":"hello"}` unless the Worker rules clearly define that such a payload means "send an email."
- Before creating the task, restate how the payload maps to the Worker's email-sending logic.
- If that mapping is ambiguous, fix the Worker rules or the payload before scheduling.

## Timezone resolution

- Do not assume the requesting user's local timezone from the cron expression alone.
- Prefer an explicit IANA timezone such as `America/Los_Angeles` or `Asia/Bangkok`.
- If the user already gave a timezone, use it and restate the UTC conversion you will schedule.
- If no timezone was provided, first try to determine the requesting user's timezone from user-specific context such as an explicit location, profile data, client-local timezone, or another reliable signal tied to that user.
- Do not use the room host timezone, server timezone, or agent runtime timezone as a proxy for the requesting user unless you have evidence that they are the same person in the same locale.
- If the requesting user's timezone still cannot be determined reliably without asking, ask the user directly before scheduling.
- Convert the requested local time into the exact UTC cron expression that will be stored.
- When the request is tied to a named local timezone that observes DST, explain that the current scheduler stores UTC cron only, so the UTC schedule may need seasonal adjustment.
- Before agreeing to create the task, make sure the requesting user's timezone is known and restated explicitly.

## One-time scheduling guard

- Restate the exact requesting-user local scheduled time and the exact UTC time before creating a one-time task.
- Use absolute times in the explanation, not just "one minute from now" or similar relative phrasing.
- Interpret relative requests such as "one minute from now" relative to the actual `meshagent scheduled-task add` moment after setup is complete, not relative to the original user message timestamp.
- If setup, deployment, or smoke testing took longer than expected, recompute the relative time from the current moment before creating the scheduled task.
- If setup, deployment, or smoke testing has consumed most of the time window, move the one-time run farther into the future instead of leaving it effectively in the past.
- Before sending `meshagent scheduled-task add`, make sure the computed UTC minute is still in the future with a real safety margin rather than merely equal to the next displayed minute.
- Before sending `meshagent scheduled-task add`, check whether an equivalent near-future one-time task already exists for the same room, queue, schedule, and payload so you do not create duplicates during a retry loop.
- If the scheduler endpoint is already showing `403`, `500`, or another backend failure during preflight, do not treat a near-future one-time request as ready for completion. Explain that scheduler creation is blocked before claiming end-to-end success.
- Do not create a near-future one-time task until the queue consumer path is already proven with an immediate smoke test.
- If the user asked for "a minute from now" but the workflow is not yet ready, explain that you are moving the one-time run to the next safe minute window rather than pretending the original time still makes sense.
- If an `add` attempt may already have succeeded, prefer inspecting existing tasks over issuing a second `add`.

## Scheduler API preflight

- For room-scoped scheduling work, prefer `meshagent scheduled-task list --room <ROOM_NAME>` before an unfiltered project-wide `list`.
- An unfiltered `meshagent scheduled-task list` can require broader project-level permissions than a room-scoped create or room-scoped list. Do not use the broader query as your first preflight when the actual workflow targets one room.
- `meshagent scheduled-task list --room <ROOM_NAME>` is the fastest packaged preflight for a room-scoped scheduler workflow. Run it before treating scheduled completion as available in the current environment.
- If room-scoped `list --room` fails with `403`, treat scheduled-task visibility for that room as blocked by permissions and do not promise that create/list verification will work later in the workflow.
- If only the unfiltered project-wide `list` fails with `403`, explain that project-wide scheduled-task visibility is blocked, but do not assume the room-scoped create path is blocked too.
- If `list` or `add` fails with an unexpected `5xx`, treat the scheduler backend as unhealthy for this room or project until proven otherwise.
- The current CLI and API do not locally validate that a one-time cron expression is still safely in the future. The backend create path is thin and backend cron failures can surface as generic server errors.
- When preflight shows scheduler failure, either stop before provisioning a half-complete scheduled workflow or clearly label any continued Worker or MailBot setup as partial preparation only.

## Queue consumption

- CLI verification: use `meshagent room queue size --queue <QUEUE_NAME>` and `meshagent room queue receive --queue <QUEUE_NAME>`.
- For queue-name discovery, prefer `meshagent room agent list-toolkits` and `meshagent room agent invoke-tool --toolkit queues --tool list --arguments '{}'` before writing SDK code.
- API verification: use the room queues client, for example `queues = await room.queues.list()` or `message = await room.queues.receive(name="my-queue")`.
- The current CLI does not expose a dedicated room-queue list subcommand. If the queue name is unknown, use the room queue API or inspect room configuration rather than claiming queue discovery is impossible.
- When you need end-to-end proof, verify both the scheduled task definition and the resulting queued message. For mail-sending workers, this is still not enough by itself; runtime mail-send evidence must also be checked.

## Current agent queue discovery

- If this skill is running inside a live MeshAgent room runtime, first inspect the current room and current agent before inventing a queue or assuming a separate worker exists.
- If the queue name is not already known from the scheduled task, service config, mailbox config, or Worker config, first try generic CLI toolkit invocation to enumerate visible queues, then use the room queue API if needed.
- First look for an explicit queue-consuming runtime such as `meshagent worker join --queue=<QUEUE_NAME>` in the current startup command or service template.
- If the runtime is not a Worker, follow `../_shared/references/process_agent_design.md` before treating a queue channel such as `--channel=queue:<QUEUE_NAME>` as sufficient evidence of the intended queue consumer path.
- Also inspect agent annotations or nearby service YAML when the current runtime was created from a template. The schedule queue and the actual consumer path must match.
- If the current agent already consumes a queue in the current room, reuse that queue for scheduling the current agent.
- If the current agent does not already consume a queue, do not claim that scheduling the current running agent is possible yet.
- If the queue-consuming path is ambiguous, inspect the actual service template, startup command, or room-visible agent files before asking the user or choosing a queue name.

## Service integration

- A service may expose queue channels such as `--channel=queue:QUEUE_NAME`, but channel wiring alone does not prove the runtime actually dequeues work. Use `../_shared/references/process_agent_design.md` when scheduling against a process-backed runtime.
- Scheduled-task configuration must match the queue that the runtime really consumes.
- Designing or implementing the queue consumer belongs in an agent-building workflow, not this skill.

## Handoff to agent building

- If the current room already has an agent with a matching explicit queue consumer, stay in this skill and schedule against that queue.
- If the current agent does not have an explicit queue consumer, hand off to the `meshagent-queue-worker-builder` skill instead of inventing a queue consumer here.
- The `meshagent-queue-worker-builder` skill should construct or update `meshagent.yaml` so the agent consumes a queue and can be scheduled.
- When handing off, direct that skill to use `meshagent-sdk-researcher` first to inspect the nearest MeshAgent examples and packaging docs before writing YAML.
- Relevant examples are the resolved process-news-agent and meshagent-writer examples under the docs/examples tree.

## Operating rules

- Do not invent queue names.
- Do not say queue names cannot be listed just because the CLI lacks a dedicated room-queue list subcommand.
- For “what queues are available?” questions, prefer generic CLI toolkit invocation over ad hoc SDK code.
- When the request is simply "schedule a test email," do not stop just because no mailbox already exists. Hand off or continue into mailbox-backed sender provisioning as part of the ordinary workflow.
- When the request itself already asks for the end-to-end outcome, do not stop to ask "should I set it up?" unless a true missing user input or hard blocker remains.
- Do not invent timezones.
- Do not schedule a task until the requesting user's timezone has been confirmed or reliably detected.
- Do not agree to schedule based on the room, server, or agent runtime timezone when the requesting user's timezone may be different.
- If the requesting user's timezone cannot be acquired from reliable user-specific context, ask the user directly before creating the scheduled task.
- Do not treat scheduler create as reliable just because the CLI command exists. Preflight actual scheduler access and health first.
- Do not pass a human-readable custom scheduled-task id such as `scheduled-email-once-2min`. The backend scheduled-task id is a UUID. Omit `--id` unless you already have a real UUID to use.
- If scheduler preflight already failed, do not present the workflow as fully completable without clearly labeling the scheduler step as blocked.
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
