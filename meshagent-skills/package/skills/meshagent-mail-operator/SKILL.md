---
name: meshagent-mail-operator
description: Operate MeshAgent mail workflows in the current room. Use this skill for contact forms, outbound email delivery, mailbox provisioning, MailBot deployment, toolkit wiring, and inbox evidence checks.
---

# MeshAgent Mail Operator

Use this skill for MeshAgent mail workflows.

## Use this skill when

- The user wants a contact form or room site that must send real email.
- The task involves `meshagent mailbox ...` provisioning or verification.
- The task involves `meshagent mailbot ...` join, spec, service, or deploy flows.
- The task needs MailBot toolkit discovery or `new_email_thread`.
- The user wants evidence about the room inbox or outbound mail activity.

## Shared runtime

Use the room runtime defined in `../meshagent-cli-operator/SKILL.md`.

- Use the companion references in `../meshagent-cli-operator/references/command_groups.md` and `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact command shapes and flags.
- For public room-site contact forms, also follow the deployment and verification discipline in `../meshagent-webmaster-operator/SKILL.md`.

## Primary command groups

- `meshagent mailbox create`
- `meshagent mailbox show`
- `meshagent mailbox list`
- `meshagent mailbox update`
- `meshagent mailbot join`
- `meshagent mailbot service`
- `meshagent mailbot spec`
- `meshagent mailbot deploy`

## Primary verification surfaces

- `meshagent room agent ...` for toolkit discovery and MailBot interaction checks
- `meshagent room storage ...` for persisted outbound mail artifacts such as `room://.emails`
- `meshagent room database ...` for `emails` table checks when the room stores mail evidence there
- room storage paths under `room://.emails`

## Default operating model

For simple contact-form and room-email workflows, prefer the smallest working room-local design:

- one site or backend in the current room
- one room mailbox whose email address is derived from the current room name plus the configured MeshAgent mail domain
- one room-local MailBot with `toolkit_name` bound to that mailbox
- no scheduled workers, subscriber systems, reporting pipelines, or broader multi-agent orchestration unless the user explicitly asks for them

## Operating rules

- Treat the requested outcome as a live room workflow plus working outbound email delivery when the prompt says the site should send email.
- Create site assets under `/data` and deploy into the current room. Do not stop at local file edits when the requested outcome is a live room site.
- If the site deploy returns a public URL but that URL responds with a timeout, `502`, or another unsuccessful status, treat the task as still in progress. Inspect the room site deployment state, repair the deployment, and retest instead of handing the next repair step back to the user.
- Provision the room mailbox explicitly instead of inventing an ad hoc sender identity.
- Derive the mailbox email address from `MESHAGENT_ROOM` plus the configured MeshAgent mail domain, and set the mailbox queue name to exactly that same mailbox email address unless the user explicitly asks for a different routing design.
- Prefer `meshagent mailbot deploy` or an equivalent room-local MailBot setup with `toolkit_name` enabled and `--email-address` set to the mailbox email address.
- Prefer the MailBot `new_email_thread` tool for outbound delivery. Set `to` to the exact requested external recipient.
- Do not satisfy "send an email" with `mailto:` unless the user explicitly asks for a client-side-only form or explicitly accepts local email composition instead of backend delivery.
- Do not invent custom MailBot URL or token bridges, placeholder HTTP services, or synthetic environment variables such as `MAILBOT_URL` or `MAILBOT_TOKEN` unless the user explicitly asks for that architecture and those values actually exist.
- If a Python backend needs to call room tools, use the supported MeshAgent SDK API shape: `room.agents.list_toolkits(...)` and `room.agents.invoke_tool(...)`. Do not invent unsupported properties such as `room.agent` or `room.tool`.
- If the room already has database tables or room-database storage for email or submission tracking, prefer that existing room database for durable audit state instead of inventing a parallel mechanism.
- For a simple contact-form workflow, do not create custom tables unless the user explicitly asks for application-level tracking. Prefer the built-in MailBot artifacts and `emails` table as the default evidence surface.
- If outbound send fails with an SMTP rejection such as `SMTPDataError` `550 5.7.1 Permission denied`, treat that as a real mail-delivery blocker from the SMTP side, not as evidence that the site deployment itself is broken.
- Do not expose raw SMTP/provider exception text directly in a public form response unless the user explicitly asks for that behavior. Log the exact failure server-side, return a safe user-facing error, and report the exact blocker to the operator.
- Do not expose secret values unless the user explicitly asks for them.
- If SMTP or provider credentials are missing, stop and report the exact missing configuration instead of claiming the workflow is operational.

## Contact-form workflow

When the user asks for a room site that should send email:

1. Treat the requested outcome as a live site plus working outbound email delivery.
2. Create the site in `/data` and deploy it in the current room.
3. Validate required inputs in the backend. If the prompt requires "valid email and/or phone number", enforce that at least one valid contact method is present and sanitize all user-supplied fields before constructing the outgoing message.
4. Provision the room mailbox first.
5. Derive the mailbox email address from `MESHAGENT_ROOM` plus the configured MeshAgent mail domain, and configure the mailbox queue name to exactly match that mailbox email address.
6. Deploy a room-local MailBot bound to that mailbox address and expose it with `toolkit_name`.
7. Expose the MailBot toolkit and send the message through `new_email_thread` with the exact requested external recipient in `to`.
8. Keep the architecture minimal for this use case.
9. Verify that the public URL serves successfully and that the site service is healthy. If the site is unhealthy, inspect the deployed service configuration and room state, repair it, redeploy, and retest before responding.
10. Exercise the submit path with a controlled test message when the workflow requires real outbound email, and distinguish clearly between site health, MailBot/toolkit success, and SMTP/provider acceptance.
11. Return the live public URL only after the site is deployed and the outbound email path has been verified as far as MeshAgent can actually assess it.

## Inbox and evidence rules

Treat the MeshAgent mailbox and inbox system as the source of truth for what is actually assessable:

- verify mailbox state with `meshagent mailbox list`, `show`, or the corresponding room-scoped verification command
- verify toolkit exposure with the room toolkit listing
- verify persisted mail evidence with room storage checks such as `room://.emails`
- if the room already stores application-level audit data, reconcile it with the MailBot result instead of inventing a second parallel status story

Use the MeshAgent mail codepath as the source of truth for outbound delivery claims:

- `MailBot` and `MailChannel` save outbound mail into `.emails/.../message.eml` and `.emails/.../message.json`, and insert rows into the `emails` table, before SMTP send is attempted
- then they call `aiosmtplib.send(...)`
- therefore a `.emails/` artifact alone means the outbound message was constructed and persisted, not that SMTP handoff succeeded
- an `SMTPDataError` such as `550 5.7.1 Permission denied` means the SMTP server rejected delivery after message construction; treat that as a provider authorization or relay-policy blocker unless stronger evidence shows otherwise

## Claiming success

- Do not claim success from a form 200 response, queue acceptance, a `new_email_thread` success response, service startup, or a `.emails/` artifact by itself.
- Verify the strongest outcome that MeshAgent can actually assess from the current implementation, or state the exact remaining blocker.
- If the user asked you to make the room site work, do not stop at "the service is unhealthy" or "the route returns 502" and then ask whether you should continue. Continue debugging and repairing the site unless you hit an external blocker such as missing credentials, missing permissions, or a platform failure outside the room workflow.
- If you did not explicitly record whether the MailBot or toolkit call returned success or raised an exception, only claim that the submission was accepted and outbound mail was constructed and persisted.
- If the site loads but the submit action fails with an SMTP rejection, do not describe the website as broken or the email as sent. Report that the site is deployed, the form submission reached the mail workflow, and the SMTP provider rejected delivery with the exact observed error.
- If there is no matching outbound `.emails/...` path or `emails` table row for a submission, do not claim that MeshAgent made any outbound email attempt for that submission.
