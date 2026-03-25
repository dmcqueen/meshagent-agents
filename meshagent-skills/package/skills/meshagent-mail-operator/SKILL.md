---
name: meshagent-mail-operator
description: Manage MeshAgent mailboxes, explain room SMTP behavior, and inspect inbound mail queues with the CLI and room APIs.
metadata:
  short-description: Operate mailboxes, room SMTP behavior, and inbound mail queue inspection.
  references:
    bundled:
      - ../meshagent-cli-operator/references/command_groups.md
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/managed_hostname_rules.md
      - ../_shared/references/service_yaml_correctness.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - cli_root
      - server_root
    resolved_targets:
      - room mail implementation
      - mailbox CLI help
  related_skills:
    - skill: meshagent-workflow-orchestrator
      when: Mail behavior is one piece of a larger end-to-end room workflow.
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before using server or CLI source references.
    - skill: meshagent-participant-token-operator
      when: The main question is where the room participant token comes from or how raw SMTP code should obtain the in-room token.
    - skill: meshagent-queue-operator
      when: The main task is generic queue inspection or queue injection rather than mailbox behavior.
    - skill: meshagent-queue-worker-builder
      when: Mail sending is part of a queue-backed Worker or scheduled queue workflow.
    - skill: meshagent-webapp-builder
      when: Mail is one part of a room-hosted contact form or website workflow.
    - skill: meshagent-cli-operator
      when: Managed hostname and general room-scoped CLI rules matter.
  scope:
    owns:
      - mailbox administration
      - mailbox-backed sender identity rules
      - inbound mail queue inspection
      - room SMTP default behavior
    excludes:
      - generic queue workflows without mailbox context
      - full website authoring
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

# MeshAgent Mail Operator

Use this skill for mailbox administration, SMTP behavior, and inbound mail queue inspection.

## Use this skill when

- The task involves `meshagent mailbox ...` provisioning, inspection, update, or deletion.
- The user needs to understand how inbound email is routed into a room queue.
- The user needs enough SMTP detail to write code that sends email from a room workflow.
- The user already has a room client in the room and wants to send email from coded Python using raw SMTP variables.
- The user wants a coded Python path that sends mail directly from an in-room `RoomClient` without first standing up a MailBot.
- The user wants a room-hosted workflow such as a contact form to send email correctly.
- The user wants to inspect or consume incoming mail messages through the CLI or room API.

## Escalation model

- Start with the lightest mail path that fits the user's actual request.
- Do not provision a mailbox just because the task mentions sending one email.
- A simple one-off outbound test email is usually a direct-send problem, not a mailbox-administration problem.
- Escalate to mailbox provisioning only when the request actually needs mailbox features such as:
  - a durable sender identity that should be reused by agents or services
  - inbound mail routing into a room queue
  - a MailBot or process `mail:` channel
  - a room-hosted contact form or mailbox-backed workflow that must keep a stable sender address
  - a queue-backed or scheduled workflow whose sender identity must be provisioned and reused later
- If the user only asked to send a simple test email, first try the narrow direct-send path that matches the current runtime:
  - a real `email` toolkit send path if one is already present
  - or the explicit raw SMTP / `RoomClient` code path when the user asked for code or a live room client already exists
- Only provision a mailbox for a simple test email when the observed runtime path proves a mailbox-backed sender is actually required for the requested send.

## References

- Use `../meshagent-cli-operator/references/command_groups.md` and `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact CLI command shapes and flags.
- Use `../_shared/references/live_room_cli_context.md` for shared live-room CLI context rules.
- Use `../_shared/references/managed_hostname_rules.md` when the mail workflow also creates or validates a managed public hostname.
- Use `../_shared/references/service_yaml_correctness.md` when mailbox-backed mail must be wired into authored service YAML.
- After root resolution, inspect the resolved room mail implementation for SMTP sending behavior and defaults.

## Related skills

- `meshagent-workflow-orchestrator`: Use it when mail behavior is only one piece of a larger end-to-end workflow.
- `meshagent-sdk-researcher`: Resolve checkout roots before using codebase references for mail implementation details.
- `meshagent-participant-token-operator`: Use it when the main issue is participant-token discovery, service token injection, or raw SMTP code using the in-room room token.
- `meshagent-queue-operator`: Use it when the queue work is independent of mailbox provisioning or SMTP behavior.
- `meshagent-queue-worker-builder`: Use it when the mailbox-backed sender must be wired into a queue-consuming Worker or scheduled queue workflow.
- `meshagent-webapp-builder`: Use it when mailbox-backed mail is part of a room website or contact form workflow.
- `meshagent-cli-operator`: Reuse its managed-hostname and room-context rules when a mail workflow also creates or verifies a public site.

## Live room execution

- Apply `../_shared/references/live_room_cli_context.md` before asking for login or reconnecting.
- Do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as prerequisite checks for room-scoped mail workflows.
- If mailbox or queue access is uncertain, try the corresponding room-scoped or mailbox read command first and use the observed result.
- If the workflow also publishes a public contact-form site, apply `../_shared/references/managed_hostname_rules.md` instead of inventing a suffix from examples.

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
- Creating a mailbox does not by itself publish toolkit `email` into the room.
- When other agents depend on toolkit `email`, that toolkit must come from a running participant that publishes it, commonly a MailBot started with `--toolkit-name=email`.
- For room-hosted outbound email workflows, the mailbox email address is the sender identity to use. Do not synthesize a sender address from the participant name and mail domain.
- Do not use `MESHAGENT_MAIL_DOMAIN` by itself to invent mailbox addresses. It is a runtime mail-domain default, not proof that a synthesized mailbox address is provisioned or authorized to send.
- For mailbox-backed MailBot workflows, prefer routing the mailbox to a queue with the same name as the mailbox email address. The MailBot runtime also defaults its queue to `email_address` when no explicit queue is given, so keeping those names aligned is the safest default, not a hard requirement.

## Outbound delivery workflow

- Before provisioning a mailbox, decide whether the user's requested send is actually a mailbox-backed workflow or just a one-off outbound send.
- For a room-hosted mailbox-backed email workflow, first inspect or provision the mailbox that will own the sender address.
- If a mailbox already exists for the room workflow, reuse its email address and queue configuration.
- If no mailbox exists and the task specifically requires mailbox-backed send or inbound routing, create one before claiming the workflow is complete.
- If another agent will call toolkit `email`, separately verify that toolkit `email` is published in the room. Mailbox provisioning alone is not enough.
- The common room pattern is a MailBot that owns the mailbox-backed sender identity and publishes toolkit `email` for chatbots or Workers that require it.
- When provisioning a new mailbox-backed MailBot, the safest default is to keep all three aligned:
  - mailbox address
  - mailbox queue
  - MailBot inbox queue
- If you intentionally override the MailBot queue away from the mailbox address, do it only with clear evidence that the mailbox routing was updated to match. The code supports intentional overrides; the risk is assuming alignment when it no longer exists.
- If authored service YAML is involved, make sure the MailBot queue matches the mailbox or inbound mail path rather than a separate scheduled job queue unless the implementation explicitly requires both to be the same.
- When creating a mailbox for a room-hosted workflow, use collision-resistant address candidates derived from the room and workflow purpose instead of generic names like `contact-form@...`.
- For managed MeshAgent mailbox addresses, use the environment-appropriate mailbox domain family:
  - `.life` environments should use addresses under `@mail.meshagent.life`
  - production `.com` environments should use addresses under `@mail.meshagent.com`
- Treat addresses like `...@meshagent.local` as suspect for outbound delivery unless the current environment explicitly proves they are authorized.
- If mailbox creation returns `409` and mailbox inspection returns `403`, treat that address as unavailable and try another candidate before asking the user for mailbox help.
- Do not construct `From` as `<participant-name>@<mail-domain>`. Use the provisioned mailbox email address as the sender identity.
- Do not treat a hardcoded mailbox-looking string as provisioned unless it came from a successful mailbox CLI result in the current project.
- If the implementation uses the room mail agent path, let it keep the mailbox address as the default sender instead of overriding it with a synthesized address.
- If the user explicitly asks for coded Python with a live `RoomClient` and raw SMTP variables, allow that path. In that case:
  - reuse the provisioned mailbox address as the sender identity
  - mirror the room SMTP defaults from the implementation instead of inventing your own variable names or lookup path
  - use the same fallback chain as the room mail implementation: `SMTP_USERNAME` else `room.local_participant.get_attribute("name")`, `SMTP_PASSWORD` else `room.protocol.token`, `SMTP_HOSTNAME` else the runtime mail domain, `SMTP_PORT` else `587`
  - allow a direct `aiosmtplib.send(...)` Python path when the user explicitly asked for coded SMTP sending or already has a `RoomClient` and does not need MailBot behavior
  - treat this as an advanced fallback or explicit user-directed path, not the default replacement for mailbox-backed toolkit workflows
- Only fall back to a custom raw SMTP implementation when the user explicitly asks for it or the MeshAgent mailbox-backed path is unavailable.
- If the mail sender lives inside a queue-backed Worker, verify that the Worker runtime actually uses the provisioned mailbox address before treating mailbox creation as sufficient.
- For a simple one-off test send, do not provision a mailbox first unless the requested runtime path clearly depends on mailbox ownership or inbound routing.

## Queue inspection

- Use `meshagent room queue size --queue <QUEUE_NAME>` to check whether messages are accumulating.
- Use `meshagent room queue receive --queue <QUEUE_NAME>` to read the next queued message.
- In code, use the room queues client to consume messages, for example `message = await room.queues.receive(name="my-queue")`.
- Queue inspection is different from agent design. Reading the queue does not require introducing another runtime.

## Room SMTP sending behavior

- The current room mail implementation uses `SmtpConfiguration` from `meshagent.agents.mail_common`.
- If `SMTP_USERNAME` is unset, the room mail implementation uses `room.local_participant.get_attribute("name")` as the SMTP username.
- If `SMTP_PASSWORD` is unset, the room mail implementation uses `room.protocol.token` as the SMTP password.
- `room.protocol.token` is the room client's participant token, the same connection token passed through `MESHAGENT_TOKEN` or supplied to `WebSocketClientProtocol(token=...)`.
- Treat that participant token as the current participant's room credential and API grant carrier. It says who the participant is and what the participant is allowed to do in the room.
- If `SMTP_HOSTNAME` is unset, the room mail implementation uses its configured mail domain from the runtime configuration.
- If `SMTP_PORT` is unset, the room mail implementation uses port `587`.
- The current implementation reads those values when sending in `start_thread` and `send_reply_message`. Do not invent a different SMTP retrieval path.
- Do not hardcode or assume a production-only or development-only mail hostname. Use the domain configured for the current runtime.
- In a live room workflow, first check whether the default room SMTP values already work before asking the user for manual `SMTP_*` settings.
- Only ask for explicit SMTP overrides when the room's default username, token, domain, or port is known to be insufficient for the target provider.
- SMTP transport defaults do not define the sender email address. The sender address should come from the mailbox-backed workflow, not from the participant name.
- If the user wants raw Python SMTP code inside a room runtime, use the same defaults the room mail implementation uses:
  - `SMTP_USERNAME` else `room.local_participant.get_attribute(\"name\")`
  - `SMTP_PASSWORD` else the room client's participant token at `room.protocol.token`
  - `SMTP_HOSTNAME` else the runtime mail domain
  - `SMTP_PORT` else `587`
- If a live `RoomClient` already exists in the room runtime, you may write direct Python SMTP code against that client and the room defaults instead of forcing the task through MailBot setup first.
- When using the coded Python/raw SMTP path, keep it narrow:
  - use the existing `RoomClient`
  - use the provisioned mailbox-backed sender address
  - use the implementation's SMTP fallback chain
  - do not invent a second configuration model

## Verification rules

- Do not claim that inbound mail handling works until you verify the mailbox mapping and inspect the target queue.
- Do not claim that outbound mail delivery works until you distinguish message construction from SMTP/provider acceptance.
- For simple test-email requests, do not add mailbox provisioning as hidden scope creep unless the direct-send path actually fails for a mailbox-backed reason.
- For queue-backed mail workers, do not claim success until the Worker has consumed a real test message and runtime evidence shows the send succeeded or shows the exact SMTP/provider blocker.
- For Workers or chat agents that use `--require-toolkit=email`, do not treat a mailbox as proof that the toolkit exists. Verify that toolkit `email` is visible in the room from a live publisher such as a MailBot.
- If a mailbox-backed MailBot exists but inbound or outbound behavior is inconsistent, check whether the mailbox address, mailbox queue, and MailBot queue diverged. That alignment is the default working pattern in the codebase, but overrides are possible and must be verified explicitly.
- If outbound send fails and the mailbox address is outside the expected managed mailbox domain family for the current environment, treat that as a likely sender-authorization problem before blaming queue wiring or toolkit publication.
- Do not ask for generic SMTP credentials first if the task is using the room SMTP path. Check the default room values and observed failure mode first.
- If the workflow is a contact form or other room-hosted sender, verify that the sender identity is a real mailbox address before treating SMTP errors as provider-side issues.
- If a valid form submission fails with `SMTPDataError`, `550`, `553`, or similar, treat that first as sender identity or authorization failure, not just generic SMTP transport failure.
- If outbound SMTP fails with `550 5.7.1 Permission denied`, treat that as proof that the current runtime is not authorized to send from the mailbox or sender identity it attempted to use.
- For `550 5.7.1 Permission denied`, do not summarize the problem only as "the user lacks permission." The failing principal may be the MailBot, Worker, room participant token, or SMTP auth identity behind the send.
- If outbound SMTP fails with `550 5.7.1 Relaying denied`, treat that as a strong sign that the send attempted to use a `From` address other than the provisioned mailbox email address.
- For `550 5.7.1 Relaying denied`, first compare the attempted sender address against the mailbox email address before blaming queue wiring, toolkit publication, or recipient-side issues.
- If the workflow also creates a public route, follow `../_shared/references/managed_hostname_rules.md` before reporting a managed URL.
- If SMTP rejects delivery, report the exact observed blocker.
- If the task uses coded Python/raw SMTP with a live `RoomClient`, report the exact sender address, hostname, port, and SMTP/provider response that the code used.
- Do not stop at "the MeshAgent CLI is not logged in" unless an actual mailbox, room queue, or related MeshAgent command fails with an authentication or authorization error.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return mailbox, queue, and SMTP evidence to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.
