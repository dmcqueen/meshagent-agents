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
      when: Mail sending is part of a queue consumer or scheduled queue workflow.
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

Use this skill for mailbox administration, room SMTP behavior, outbound send debugging, and inbound mail queue inspection.

## Use this skill when

- The task involves `meshagent mailbox ...`.
- The user needs to send or troubleshoot real room email.
- The user needs SMTP details for code running inside a room.
- The workflow is a contact form, MailBot, mailbox-backed sender, or inbound mailbox queue.
- The user wants to inspect incoming mail in a room queue.

## Escalation model

- Start with the lightest real-email path that fits the request.
- Treat “send an email” as real outbound email by default, especially when the target looks like `name@example.com`.
- Do not substitute room messaging, chat, or broadcast unless the user asked for that medium.
- A simple one-off test email is usually a direct-send problem, not a mailbox-administration problem.
- Escalate to mailbox provisioning only when the workflow needs:
  - a durable sender identity
  - inbound mail routing
  - a MailBot or process `mail:` channel
  - a queue-backed or scheduled sender that must be reused
- For a simple test email, first try:
  - an existing `email` toolkit path
  - or raw SMTP / `RoomClient` code if the user asked for code or a live `RoomClient` already exists
- If the runtime lacks a real sender identity, provision or reuse the mailbox path automatically instead of asking the user for a sender address.
- If the current runtime cannot send real email, report the exact blocker. Do not silently switch media.

## References

- Use `../meshagent-cli-operator/references/command_groups.md` and `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact CLI usage.
- Use `../_shared/references/live_room_cli_context.md` for live-room rules.
- Use `../_shared/references/managed_hostname_rules.md` when a mail workflow also creates or validates a managed public hostname.
- Use `../_shared/references/service_yaml_correctness.md` when mail is wired into service YAML.
- Inspect the room mail implementation after root resolution when SMTP behavior matters.

## Related skills

- `meshagent-workflow-orchestrator`: mail is only one part of a larger workflow
- `meshagent-sdk-researcher`: root resolution and source lookup
- `meshagent-participant-token-operator`: participant-token sourcing or SMTP code using the in-room token
- `meshagent-queue-operator`: generic queue work without mailbox logic
- `meshagent-queue-worker-builder`: queue-backed or scheduled mail senders
- `meshagent-webapp-builder`: contact forms and site workflows
- `meshagent-cli-operator`: room-scoped CLI rules and managed hostname context

## Live room rules

- Apply `../_shared/references/live_room_cli_context.md`.
- Do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as prerequisites for room-scoped mail work.
- Only inspect mailbox or queue state after the chosen send path actually needs it.
- If the workflow publishes a public site, use `../_shared/references/managed_hostname_rules.md` instead of inventing hostname suffixes.

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
- Inbound mail goes to that configured queue.
- Creating a mailbox does not create a consumer, service, or toolkit publisher.
- Creating a mailbox does not publish toolkit `email`.
- If another runtime depends on toolkit `email`, a live participant must publish it, commonly a MailBot with `--toolkit-name=email`.
- For mailbox-backed outbound workflows, the mailbox email address is the sender identity. Do not synthesize one from participant name or mail domain.
- Do not use `MESHAGENT_MAIL_DOMAIN` alone to invent mailbox addresses.
- For new mailbox-backed MailBot workflows, use this naming convention:
  - mailbox address
  - mailbox queue
  - MailBot inbox queue
  all aligned to the same email address.
- Do not invent a different mailbox queue name for a new mailbox-backed workflow.
- Treat any existing room that already uses different mailbox and inbox queue names as an explicit exception that must be verified, not as a design choice to repeat by default.

## Outbound send model

- Before provisioning a mailbox, decide whether the request is mailbox-backed or just a one-off send.
- For a one-off send, first check whether the runtime already has an authorized sender identity.
- If no usable sender exists and real outbound email is still the goal, provision or reuse the mailbox path automatically unless the user explicitly wants to choose the sender.
- If a mailbox already exists for the workflow, reuse its address and queue.
- If another agent or runtime will call toolkit `email`, verify that toolkit `email` is actually published in the room.
- For managed mailbox addresses:
  - `.life` environments should use `@mail.meshagent.life`
  - production `.com` environments should use `@mail.meshagent.com`
- Treat addresses like `...@meshagent.local` as suspect for outbound delivery unless the environment proves they are authorized.
- If mailbox creation returns `409` and mailbox inspection returns `403`, treat that candidate as unavailable and try another address.
- Do not construct `From` as `<participant-name>@<mail-domain>`. Use the provisioned mailbox address.
- Only use custom raw SMTP code when the user explicitly asks for it or the mailbox-backed path is unavailable.

## Raw SMTP / RoomClient path

- If the user explicitly asks for coded Python with a live `RoomClient`, allow that path.
- Reuse a real provisioned sender identity if one exists. If none exists, obtain one instead of inventing a `From` address.
- Mirror the implementation’s fallback chain:
  - `SMTP_USERNAME` else `room.local_participant.get_attribute("name")`
  - `SMTP_PASSWORD` else `room.protocol.token`
  - `SMTP_HOSTNAME` else the runtime mail domain
  - `SMTP_PORT` else `587`
- `room.protocol.token` is the room client’s participant token. It is the same room credential carried through `MESHAGENT_TOKEN` or passed to `WebSocketClientProtocol(token=...)`.
- Keep this path narrow:
  - use the existing `RoomClient`
  - use the mailbox-backed sender
  - use the implementation’s SMTP defaults
  - do not invent a second configuration model

## Queue inspection

- Use `meshagent room queue size --queue <QUEUE_NAME>` to check buildup.
- Use `meshagent room queue receive --queue <QUEUE_NAME>` to inspect the next message.
- In code, use the room queues client directly.
- Queue inspection does not require introducing another runtime.

## Verification rules

- Inbound mail is not proven until mailbox mapping and target queue behavior are verified.
- Outbound mail is not proven until SMTP/provider acceptance is distinguished from local message construction.
- For simple test-email requests, do not add mailbox provisioning as hidden scope creep unless the direct-send path actually needs it.
- For simple test-email requests, do not satisfy the ask with room messaging or chat.
- For queue-backed mail senders, do not call the workflow complete until a real queued message is consumed and runtime evidence shows success or the exact SMTP/provider blocker.
- If a runtime uses `--require-toolkit=email`, a mailbox is not proof that the toolkit exists. Verify a live publisher.
- If mailbox-backed behavior is inconsistent, check whether mailbox address, mailbox queue, and MailBot queue diverged.
- If the mailbox address is outside the expected managed domain family for the environment, treat that as a likely sender-authorization problem.
- Do not ask for generic SMTP credentials first when the room SMTP path is in use. Check the room defaults and observed failure first.
- For room-hosted senders such as contact forms, verify that the sender is a real mailbox address before blaming the provider.
- Treat `SMTPDataError`, `550`, `553`, and similar failures first as sender identity or authorization problems unless evidence shows otherwise.
- `550 5.7.1 Permission denied` means the current runtime is not authorized to send from the mailbox or sender identity it attempted to use.
- `550 5.7.1 Relaying denied` strongly suggests the attempted `From` address did not match the provisioned mailbox email address.
- If SMTP rejects delivery, report the exact blocker.
- If the task uses raw SMTP code with a live `RoomClient`, report the exact sender, host, port, and SMTP/provider response used.
- Do not stop at “the CLI is not logged in” unless an actual mailbox, queue, or related command failed with auth or authz.

## Workflow accountability

- This skill may own the workflow when mail is the main goal.
- If another skill owns the end-to-end result, return mailbox, queue, and SMTP evidence to that owner.
- Follow `../_shared/references/workflow_accountability.md` for ownership, evidence, and forbidden shortcuts.
