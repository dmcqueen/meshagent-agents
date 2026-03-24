---
name: meshagent-webapp-builder
description: Build and verify deployable MeshAgent room web applications, including contact forms, public web handlers, and mailbox-backed outbound email flows.
metadata:
  short-description: Build, deploy, and verify room-hosted websites and handlers.
  references:
    bundled:
      - references/command_groups.md
      - references/meshagent_cli_help.md
      - references/contact_form_example.py
      - references/mailbox_backed_sender.md
      - references/minimal_webserver.yaml
      - references/verification_checklist.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/managed_hostname_rules.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - cli_root
      - server_root
    resolved_targets:
      - webserver CLI source
      - room mail implementation
  related_skills:
    - skill: meshagent-cli-operator
      when: General room-context, managed-hostname, and deploy-command rules matter.
    - skill: meshagent-mail-operator
      when: The blocker is mailbox provisioning or room SMTP behavior.
    - skill: meshagent-webmaster
      when: The main task is route and hostname administration rather than the web app itself.
    - skill: meshagent-webapp-react-builder
      when: The site is a small React-style UI built with Preact + htm.
  scope:
    owns:
      - room website and handler implementation
      - public deploy workflow
      - contact form and mailbox-backed sender integration
      - post-deploy HTTP verification
    excludes:
      - generic route administration
      - deep frontend platform design beyond room webapps
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
- Use `../_shared/references/live_room_cli_context.md` for shared room-context, path, and deploy workspace rules.
- Use `../_shared/references/managed_hostname_rules.md` for shared managed-hostname selection and validation rules.
- After root resolution, inspect the resolved webserver CLI source for actual runtime behavior.
- After root resolution, inspect the resolved room mail implementation for SMTP defaults and sender behavior.

## Related skills

- `meshagent-cli-operator`: Reuse its general room-context, managed-hostname, and deploy-command rules instead of inventing environment behavior locally.
- `meshagent-sdk-researcher`: Resolve checkout roots before using codebase references outside this skill bundle.
- `meshagent-mail-operator`: Use it when the blocker is mailbox provisioning, queue-backed mail intake, or SMTP behavior.
- `meshagent-webmaster`: Use it when the main task is route and hostname administration rather than the web app itself.
- `meshagent-webapp-react-builder`: Use it when the site is a small React-style UI built with Preact + htm.

## Live room execution

- Apply `../_shared/references/live_room_cli_context.md` for room context reuse, room-scoped command handling, and local-vs-room path rules.
- Apply `../_shared/references/managed_hostname_rules.md` for managed hostname suffix selection and collision handling.
- For `meshagent webserver deploy`, the local source tree must live under the current working directory. Use `--website-path` as the room-storage destination for deployed files.
- In a live room shell where `cwd` is `/src`, author deployable webapp files under a subdirectory of `/src`, not directly under `/data`.

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

- Follow `../_shared/references/managed_hostname_rules.md` for suffix selection, collision handling, and validity checks.
- Prefer collision-resistant hostname candidates derived from the room name plus the site purpose.
- If the user did not request a specific hostname, automatically try a small set of candidates before asking for naming input.

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

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return deploy, HTTP, and mail evidence to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.
