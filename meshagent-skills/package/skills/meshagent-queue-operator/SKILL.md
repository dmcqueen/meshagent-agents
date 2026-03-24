---
name: meshagent-queue-operator
description: Operate MeshAgent room queues. Use this skill for sending JSON or mail payloads to queues, receiving queued messages, checking queue depth, and verifying queue-backed workflows.
metadata:
  short-description: Operate room queues for send, receive, backlog, and delivery verification.
  references:
    bundled:
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - references/queue_discovery.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - docs_root
      - cli_root
      - api_root
    resolved_targets:
      - queue CLI help
      - queue CLI source
      - room queue API examples
  related_skills:
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before using docs or source references.
    - skill: meshagent-scheduler
      when: Queue traffic comes from scheduled tasks.
    - skill: meshagent-mail-operator
      when: The queue is part of a mailbox flow.
    - skill: meshagent-queue-worker-builder
      when: A queue consumer must be created or repaired.
  scope:
    owns:
      - room queue send and receive
      - queue backlog inspection
      - queue-backed workflow verification
    excludes:
      - Worker or service YAML authoring
      - mailbox administration
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

# MeshAgent Queue Operator

Use this skill when the task is to inspect or operate a queue inside a MeshAgent room.

## Use this skill when

- The user wants to send a payload into a room queue.
- The task involves `meshagent room queue send`, `send-mail`, `receive`, or `size`.
- The user needs to verify that a scheduled task, mailbox, webhook, or worker workflow is actually producing queue messages.
- The task is about queue backlog, queue naming, or reading the next queued payload.

## References

- Use `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact `meshagent room queue ...` command shapes.
- Use `references/queue_discovery.md` when the user asks what queues are available in the room or when the queue name is unknown.
- Inspect the resolved queue CLI source for the real queue behavior and payload handling.
- Inspect the resolved room queue API source when queue-name discovery matters. The current CLI does not expose a dedicated room-queue list subcommand, but the room queue API does support listing visible queues.

## Related skills

- `meshagent-sdk-researcher`: Resolve checkout roots before using docs or source references.
- `meshagent-scheduler`: Use it when the queue messages come from scheduled tasks.
- `meshagent-mail-operator`: Use it when the queue is part of a mailbox flow.
- `meshagent-queue-worker-builder`: Use it when the missing piece is a queue-consuming Worker rather than queue operations themselves.

## Default workflow

1. Resolve the active room and the exact queue name.
2. If the queue name is unknown, use `references/queue_discovery.md` and prefer `meshagent room agent list-toolkits` plus `meshagent room agent invoke-tool --toolkit queues --tool list --timeout 0 --arguments '{}'` before writing any SDK code.
3. If toolkit invocation is unavailable, discover queue names from current room configuration or as a last resort through the room queue API. Do not say queue listing is impossible just because the CLI lacks a dedicated `list` subcommand.
4. Inspect the queue state with `meshagent room queue size` before mutating or consuming it.
5. If the task is to inject work, choose `send` for JSON payloads or `send-mail` for email-shaped messages.
6. If the task is to verify end-to-end behavior, confirm both the sender path and the queue contents.
7. After sending or receiving, re-check queue state when backlog or delivery matters.

## Queue operation rules

- Do not invent queue names. Reuse the queue already configured by the scheduler, mailbox, webhook, or Worker.
- Do not claim that queues cannot be listed in a room. The current CLI lacks a dedicated room-queue list command, but the room queue API can enumerate visible queues.
- When the user asks for a clean list of queue names, prefer `meshagent room agent invoke-tool --toolkit queues --tool list --timeout 0 --arguments '{}'` over writing ad hoc Python.
- Use SDK code for queue listing only as a fallback when the generic CLI toolkit invocation path is unavailable.
- Do not answer with “tool output was truncated” for a queue-list request. Rerun the narrow command and return the actual queue names or an explicit empty list.
- Prefer `send` for JSON payloads and `send-mail` only when the receiving workflow expects an email message shape.
- Use `receive` to inspect the next queued message, but treat it as consumption of a live queue entry.
- Use `size` when you need backlog verification without consuming a message.
- If the queue does not exist, verify the upstream configuration before claiming the consumer is broken.

## Verification rules

- Do not claim a queue-backed workflow works just because the sender command succeeded.
- Verify the queue depth or queued payload after the upstream action.
- If a queue-backed Worker is supposed to consume the message, verify both enqueue and downstream dequeue behavior.
- If a queue is empty when it should contain messages, inspect the sender configuration before redesigning the consumer.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return queue evidence and observed state to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- Designing a Worker or service template to consume the queue.
- Mailbox administration beyond queue verification.
