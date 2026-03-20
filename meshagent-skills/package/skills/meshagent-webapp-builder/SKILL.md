---
name: meshagent-webapp-builder
description: Build and verify deployable MeshAgent room web applications, including contact forms, public web handlers, and mailbox-backed outbound email flows.
---

# MeshAgent Webapp Builder

Use this skill when the task is to build, deploy, or debug a room-hosted website or web handler.

## Use this skill when

- The user wants a website, contact form, landing page, or HTTP handler deployed from a room.
- The task involves `meshagent webserver ...` plus actual application code, not just route administration.
- The task includes form validation, sanitization, public URL delivery, or post-deploy smoke testing.
- The task includes outbound email from a room-hosted website such as a contact form.
- The task is to diagnose a live `500`, `502`, or other public-site failure from a deployed room webserver.

## References

- Start with `references/command_groups.md` and `references/meshagent_cli_help.md` in this skill. They are local wrappers that point to the shared packaged CLI references in this package.
- Reuse the packaged implementation assets in this skill before inventing a fresh pattern:
  - `references/contact_form_example.py`
  - `references/mailbox_backed_sender.md`
  - `references/minimal_webserver.yaml`
  - `references/verification_checklist.md`
- For actual webserver runtime behavior, inspect `/src/meshagent-sdk/meshagent-cli/meshagent/cli/webserver.py`.
- For room mail behavior and SMTP defaults, inspect `/src/meshagent-sdk/meshagent-agents/meshagent/agents/mail.py` and `/src/meshagent-sdk/meshagent-agents/meshagent/agents/mail_common.py`.

## Live room execution

- First use the existing MeshAgent CLI session and room context before asking the user to log in again.
- If `MESHAGENT_ROOM` is present, prefer room-scoped commands and pass `--room "${MESHAGENT_ROOM}"` when required.
- If `MESHAGENT_API_URL` is present, derive the managed hostname suffix from that API environment: use `*.meshagent.app` for `.com` environments and `*.meshagent.dev` for `.life` environments.
- If `MESHAGENT_API_URL` is absent or ambiguous, inspect existing routes or ask before inventing a managed public hostname.
- Packaged `.meshagent.app` examples are illustrative only. Do not copy that suffix when the runtime indicates `.meshagent.dev`.
- For `meshagent webserver deploy`, the local source tree must live under the current working directory. Use `--website-path` as the room-storage destination for deployed files.
- In a live room shell where `cwd` is `/src`, author deployable webapp files under a subdirectory of `/src`, not directly under `/data`.
- If `MESHAGENT_ROOM` is already present, do not block on room-listing commands before deploy.

## Implementation rules

- Use relative route sources like `handlers/contact.py` and `public` so the deploy stays portable.
- For public webserver configs, set `host: 0.0.0.0` unless there is a concrete reason not to.
- Keep handler modules simple at import time. A module that raises during import can surface to the public site as a generic `500`.
- Do not invent runtime environment variables. Use the actual implementation and currently configured environment. If a sender or SMTP env var is not documented in the implementation, do not assume it exists.
- For room-hosted contact forms, the sender address must come from a successful `meshagent mailbox list`, `meshagent mailbox show`, or `meshagent mailbox create` result in the current project.
- Do not synthesize sender identities from the participant name or mail domain. In particular, do not invent `FROM_ADDRESS`, `MAIL_FROM`, `SMTP_FROM`, or `MESHAGENT_PARTICIPANT_NAME`.
- If the handler uses direct SMTP, use only the real room SMTP defaults documented in `mail_common.py`: `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_HOSTNAME`, and `SMTP_PORT`.
- For Python handlers that render inline HTML, avoid `str.format()` across raw HTML, CSS, or regex-heavy strings unless every literal brace is escaped. CSS blocks and patterns like `{1,80}` otherwise break rendering at runtime.
- Prefer safer rendering approaches for generated handlers: placeholder replacement, `string.Template`, or another approach that does not reinterpret every `{...}` in the whole document.
- Validate on both client and server when the task includes user input, but treat server-side validation as authoritative.
- Sanitize submitted values before including them in responses, logs, or email bodies.

## Contact form workflow

1. Create the local webapp project under the current working directory.
2. Add a GET route that renders the form and a POST route that validates and handles submission.
3. Restrict email and phone fields with browser-side input types and patterns when helpful.
4. Re-validate all submitted fields on the server.
5. If the form sends outbound email from the room, inspect existing room mailboxes first.
6. If no suitable mailbox exists, create collision-resistant mailbox candidates derived from the room and workflow purpose.
7. If mailbox creation returns `409` and mailbox inspection is forbidden, treat that candidate as unavailable and try another candidate before asking the user for help.
8. Use the exact mailbox address returned by the CLI as the `From` address and use the visitor email only as `Reply-To` when present.
9. Prefer the room mail path and real mailbox-backed sender identity over ad hoc SMTP guesses.
10. Only fall back to custom raw SMTP code when the user explicitly asks for it or the mailbox-backed path is unavailable.
11. When using direct SMTP, use the real room SMTP defaults from `mail_common.py` and the mailbox-backed sender address from the CLI result.
12. Deploy with `meshagent webserver deploy --room "$MESHAGENT_ROOM" --website-path /<site-subpath> ...`.
13. Verify the live site with actual GET and POST requests after deploy.

## Managed hostname selection

- Prefer collision-resistant hostname candidates derived from the room name plus the site purpose.
- If the user did not request a specific hostname, automatically try a small set of candidates before asking for naming input.
- Keep retries within the same environment-specific suffix family.
- If a candidate collides and follow-up route inspection is forbidden, treat that hostname as unavailable and try another candidate before reporting a permissions blocker.
- Do not report a managed URL whose suffix contradicts the active API environment.

## Verification rules

- Do not treat `meshagent webserver check`, local file generation, or deploy success alone as completion.
- For every website task, perform at least one live HTTP GET against the public URL before reporting success.
- For form-backed sites, also exercise representative POST paths after deploy.
- For contact forms that send mail, include one invalid POST and one valid POST in the verification flow.
- If a live GET or POST returns `500`, inspect handler import/render/runtime failures before blaming room routing or platform infrastructure.
- If a public request returns `502` or another upstream-style error, inspect the deployed bind host, service port, and public route configuration before concluding the room is unhealthy.
- If a contact-form task asks for emailed submissions, do not report success while live submission still fails to send mail.
- Distinguish SMTP transport from sender authorization. A form that renders but fails with `SMTPDataError`, `550`, `553`, or similar on valid submission is not complete.
- If outbound mail fails with an authorization error such as `550 5.7.1 Permission denied`, switch to mailbox-backed sender provisioning if permissions allow, then re-test.
- If code still references a synthesized sender address after mailbox provisioning fails, treat that as an implementation bug and replace it with a real mailbox-backed address or report the exact mailbox blocker.
- Only stop and ask the user for help after mailbox provisioning, route creation, or deploy verification is blocked by a concrete error you can report exactly.
