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
- The user wants a room-hosted workflow such as a contact form to send email correctly.
- The user wants to inspect or consume incoming mail messages through the CLI or room API.

## References

- Use `references/command_groups.md` and `references/meshagent_cli_help.md` for exact CLI command shapes and flags.
- For room SMTP sending behavior, inspect the actual implementation in `/src/meshagent-sdk/meshagent-agents/meshagent/agents/mail.py` and `/src/meshagent-sdk/meshagent-agents/meshagent/agents/mail_common.py`.

## Live room execution

- If this skill is running inside a live MeshAgent room runtime, first use the existing MeshAgent CLI session and room context before asking for login or manual re-authentication.
- If mailbox or queue access is uncertain, try the corresponding room-scoped or mailbox read command first and use the observed result.
- If the workflow also publishes a public contact-form site, derive the managed hostname suffix from `MESHAGENT_API_URL` and keep that suffix consistent with the current environment.

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
- For room-hosted outbound email workflows, the mailbox email address is the sender identity to use. Do not synthesize a sender address from the participant name and mail domain.

## Outbound delivery workflow

- For a room-hosted email workflow, first inspect or provision the mailbox that will own the sender address.
- If a mailbox already exists for the room workflow, reuse its email address and queue configuration.
- If no mailbox exists and the task requires sending mail from the room, create one before claiming the workflow is complete.
- Do not construct `From` as `<participant-name>@<mail-domain>`. Use the provisioned mailbox email address as the sender identity.
- If the implementation uses the room mail agent path, let it keep the mailbox address as the default sender instead of overriding it with a synthesized address.
- Only fall back to a custom raw SMTP implementation when the user explicitly asks for it or the MeshAgent mailbox-backed path is unavailable.
- If a room website or service needs to send email, keep its durable runtime assets under `/data`. When the workflow uses `meshagent webserver deploy`, keep the local website source tree under the current working directory and use `--website-path` to upload the deployable files into room storage.

## Queue inspection

- Use `meshagent room queue size --queue <QUEUE_NAME>` to check whether messages are accumulating.
- Use `meshagent room queue receive --queue <QUEUE_NAME>` to read the next queued message.
- In code, use the room queues client to consume messages, for example `message = await room.queues.receive(name="my-queue")`.
- Queue inspection is different from agent design. Reading the queue does not require introducing another runtime.

## Room SMTP sending behavior

- The current room mail implementation uses `SmtpConfiguration` from `meshagent.agents.mail_common`.
- If `SMTP_USERNAME` is unset, the room mail implementation uses `room.local_participant.get_attribute("name")` as the SMTP username.
- If `SMTP_PASSWORD` is unset, the room mail implementation uses `room.protocol.token` as the SMTP password.
- If `SMTP_HOSTNAME` is unset, the room mail implementation uses its configured mail domain from the runtime configuration.
- If `SMTP_PORT` is unset, the room mail implementation uses port `587`.
- The current implementation reads those values when sending in `start_thread` and `send_reply_message`. Do not invent a different SMTP retrieval path.
- Do not hardcode or assume a production-only or development-only mail hostname. Use the domain configured for the current runtime.
- In a live room workflow, first check whether the default room SMTP values already work before asking the user for manual `SMTP_*` settings.
- Only ask for explicit SMTP overrides when the room's default username, token, domain, or port is known to be insufficient for the target provider.
- SMTP transport defaults do not define the sender email address. The sender address should come from the mailbox-backed workflow, not from the participant name.

## Verification rules

- Do not claim that inbound mail handling works until you verify the mailbox mapping and inspect the target queue.
- Do not claim that outbound mail delivery works until you distinguish message construction from SMTP/provider acceptance.
- Do not ask for generic SMTP credentials first if the task is using the room SMTP path. Check the default room values and observed failure mode first.
- If the workflow is a contact form or other room-hosted sender, verify that the sender identity is a real mailbox address before treating SMTP errors as provider-side issues.
- If the workflow also creates a public route, do not copy `.meshagent.app` from CLI examples when the current runtime maps to a different managed suffix.
- If tool calls fail because `meshagent webserver deploy` requires local route sources under the current working directory, move the local website project under that working directory instead of switching the deploy input to `/data`.
- Do not claim a contact-form website is complete until both the sender identity and the public site exposure path are verified, or until you report the exact blocking command and error.
- If SMTP rejects delivery, report the exact observed blocker.
- Do not stop at "the MeshAgent CLI is not logged in" unless an actual mailbox, room queue, or related MeshAgent command fails with an authentication or authorization error.
