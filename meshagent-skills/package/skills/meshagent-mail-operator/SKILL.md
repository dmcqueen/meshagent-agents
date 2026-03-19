---
name: meshagent-mail-operator
description: Manage MeshAgent mailboxes, explain room SMTP behavior, and inspect inbound mail queues with the CLI and room APIs.
---

# MeshAgent Mail Operator

Use this skill for mailbox administration, SMTP behavior, and inbound mail queue inspection.

## Use this skill when

- The task involves `meshagent mailbox ...` provisioning, inspection, update, or deletion.
- The user needs to understand how inbound email is routed into a room queue.
- The user needs enough SMTP detail to write code that sends email from a room workflow.
- The user wants to inspect or consume incoming mail messages through the CLI or room API.

## References

- Use `references/command_groups.md` and `references/meshagent_cli_help.md` for exact CLI command shapes and flags.

## Live room execution

- If this skill is running inside a live MeshAgent room runtime, first use the existing MeshAgent CLI session and room context before asking for login or manual re-authentication.
- If mailbox or queue access is uncertain, try the corresponding room-scoped or mailbox read command first and use the observed result.

## Primary command groups

- `meshagent mailbox create`
- `meshagent mailbox show`
- `meshagent mailbox list`
- `meshagent mailbox update`
- `meshagent mailbox delete`
- `meshagent room queue receive`
- `meshagent room queue size`

## Mailbox model

- A mailbox maps an email address to a room and a queue.
- Inbound email to that mailbox is delivered into the configured queue.
- The queue name is part of the mailbox configuration. Do not invent it.
- Creating a mailbox does not by itself create a consumer, service, or agent.

## Queue inspection

- Use `meshagent room queue size --queue <QUEUE_NAME>` to check whether messages are accumulating.
- Use `meshagent room queue receive --queue <QUEUE_NAME>` to read the next queued message.
- In code, use the room queues client to consume messages, for example `message = await room.queues.receive(name="my-queue")`.
- Queue inspection is different from agent design. Reading the queue does not require introducing a MailBot or other runtime.

## Verification rules

- Do not claim that inbound mail handling works until you verify the mailbox mapping and inspect the target queue.
- Do not claim that outbound mail delivery works until you distinguish message construction from SMTP/provider acceptance.
- If SMTP rejects delivery, report the exact observed blocker.
- Do not stop at "the MeshAgent CLI is not logged in" unless an actual mailbox, room queue, or related MeshAgent command fails with an authentication or authorization error.
