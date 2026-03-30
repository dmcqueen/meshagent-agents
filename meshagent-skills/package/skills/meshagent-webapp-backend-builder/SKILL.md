---
name: meshagent-webapp-backend-builder
description: Build and verify deployable MeshAgent room web application backends, including Python web handlers, contact forms, room-database integration, and mailbox-backed outbound email flows.
metadata:
  short-description: Canonical backend path for room-hosted web apps, handlers, DB, and mail.
  references:
    bundled:
      - references/command_groups.md
      - references/meshagent_cli_help.md
      - references/contact_form_example.py
      - references/contact_submission_store.py
      - references/mailbox_backed_sender.md
      - references/minimal_webserver.yaml
      - references/verification_checklist.md
      - ../_shared/references/environment_profile_rules.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/managed_hostname_rules.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - cli_root
      - docs_root
      - api_root
      - server_root
    resolved_targets:
      - webserver CLI source
      - room mail implementation
      - room webserver database examples
      - Room API database client source
  related_skills:
    - skill: meshagent-workflow-orchestrator
      when: The web app is one piece of a larger end-to-end workflow.
    - skill: meshagent-cli-operator
      when: General room-context, managed-hostname, and deploy-command rules matter.
    - skill: meshagent-participant-token-operator
      when: The blocker is token-backed service environment wiring, participant-token discovery, or direct room API auth inside the handler runtime.
    - skill: meshagent-database-operator
      when: The site must persist form submissions or query the in-room database from handler code.
    - skill: meshagent-mail-operator
      when: The blocker is mailbox provisioning or room SMTP behavior.
    - skill: meshagent-webapp-dev-operator
      when: The task is active Python-handler iteration and the runtime must hot-reload backend changes.
    - skill: meshagent-webapp-release-operator
      when: The task is to cut, verify, promote, or roll back an image-backed release candidate for the webapp.
    - skill: meshagent-webmaster
      when: The main task is route and hostname administration rather than the web app itself.
    - skill: meshagent-webapp-frontend-builder
      when: The site needs a richer interactive Preact + htm frontend on top of this backend path.
  scope:
    owns:
      - room website and handler implementation
      - contact form and mailbox-backed sender integration
      - post-deploy HTTP verification
    excludes:
      - generic route administration
      - hot-reload dev-loop operation
      - image-backed release-candidate lifecycle
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

# MeshAgent Webapp Backend Builder

Use this skill when the task is to build, deploy, or debug the backend/runtime side of a room-hosted website or web handler.

## Use this skill when

- The user wants a website, contact form, landing page, or HTTP handler deployed from a room.
- The task involves `meshagent webserver ...` plus actual application code, not just route administration.
- The task includes form validation, sanitization, public URL delivery, or post-deploy smoke testing.
- The task needs the canonical backend stack for database-backed or email-featured sites.
- The task includes outbound email from a room-hosted website such as a contact form.
- The task is to diagnose a live `500`, `502`, or other public-site failure from a deployed room webserver.

## References

- Start with `references/command_groups.md` and `references/meshagent_cli_help.md` in this skill. They are local wrappers that point to the shared packaged CLI references in this package.
- Reuse the packaged implementation assets in this skill before inventing a fresh pattern:
  - `references/contact_form_example.py`
  - `references/contact_submission_store.py`
  - `references/mailbox_backed_sender.md`
  - `references/minimal_webserver.yaml`
  - `references/verification_checklist.md`
- Use `../_shared/references/live_room_cli_context.md` for shared room-context, path, and deploy workspace rules.
- Use `../_shared/references/managed_hostname_rules.md` for shared managed-hostname selection and validation rules.
- After root resolution, inspect the resolved webserver CLI source for actual runtime behavior.
- After root resolution, inspect the resolved room mail implementation for SMTP defaults and sender behavior.
- After root resolution, use these resolved database examples when the site must persist submissions:
  - `meshagent-docs/examples/python/webserver/contact_form_route.py`
  - `meshagent-docs/examples/python/webserver/contact_list_route.py`
  - `meshagent-api/meshagent/api/room_server_client.py`

## Related skills

- `meshagent-workflow-orchestrator`: Use it when the web app is only one piece of a larger end-to-end workflow.
- `meshagent-cli-operator`: Reuse its general room-context, managed-hostname, and deploy-command rules instead of inventing environment behavior locally.
- `meshagent-sdk-researcher`: Resolve checkout roots before using codebase references outside this skill bundle.
- `meshagent-participant-token-operator`: Use it when the blocker is service token injection, participant-token discovery, or direct room API auth inside the handler runtime.
- `meshagent-database-operator`: Use it when the site must write to or read from the in-room database.
- `meshagent-mail-operator`: Use it when the blocker is mailbox provisioning, queue-backed mail intake, or SMTP behavior.
- `meshagent-webapp-dev-operator`: Use it when the task is active backend iteration and the runtime must hot-reload Python handler changes.
- `meshagent-webapp-release-operator`: Use it when the task is an image-backed candidate, release, promotion, or rollback-ready webapp deploy.
- `meshagent-webmaster`: Use it when the main task is route and hostname administration rather than the web app itself.
- `meshagent-webapp-frontend-builder`: Use it when the site needs a richer interactive frontend built with Preact + htm on top of this backend path.

## Live room execution

- Apply `../_shared/references/live_room_cli_context.md` for room context reuse, room-scoped command handling, and local-vs-room path rules.
- Do not enable room messaging as part of a normal site or contact-form workflow unless the user explicitly asked for room messaging behavior.
- Apply `../_shared/references/managed_hostname_rules.md` for managed hostname suffix selection and collision handling.
- For `meshagent webserver deploy`, the local source tree must live under the current working directory. Use `--website-path` as the room-storage destination for deployed files.
- In a live room shell where `cwd` is `/src`, author deployable webapp files under a subdirectory of `/src`, not directly under `/data`.
- Do not rely on `meshagent room container exec` into another participant's private container as the default way to inspect a deployed site. Prefer public HTTP checks, service state, developer watch, container logs, and deployed source artifacts first.

## Golden path architecture

- This skill is the canonical backend and runtime path for DB-backed or email-featured MeshAgent sites.
- Prefer Python `aiohttp` handlers as the backend default when a site needs room database writes, mailbox-backed email, or other live handler behavior.
- Prefer a typed helper-module pattern for backend state:
  - `handlers/<feature>_store.py` or another narrow helper for `room.database.*`
  - `handlers/<feature>.py` or other route handlers for request validation and response shaping
- For straightforward forms, lists, and admin views, prefer server-rendered HTML or small HTML-first interactions over a heavier client app.
- If the site needs richer interactivity, canvas-style UI, or component-heavy state, keep this backend path and layer `meshagent-webapp-frontend-builder` on top of it rather than inventing a separate backend stack.
- Do not switch backend languages or runtime models without a requirement that the Python golden path clearly cannot satisfy.

## Mode routing

- Keep this skill focused on backend implementation, handler behavior, DB integration, and mail integration.
- If the main need is a hot-reload dev loop for Python handlers, hand the runtime loop to `meshagent-webapp-dev-operator`.
- If the main need is an image-backed candidate, release, promotion, or rollback-ready artifact, hand the packaging and deploy lifecycle to `meshagent-webapp-release-operator`.
- If a website request spans backend implementation plus dev or release mechanics, keep backend behavior work here and use the narrower dev or release skill for that mode-specific part.

## Implementation rules

- Apply the shared minimal change discipline from `../_shared/references/workflow_accountability.md`, then use the web-specific modularity rules below for live handler changes.
- Apply the shared isolation-before-integration discipline from `../_shared/references/workflow_accountability.md` before blending DB, mail, and response changes into an existing live handler.
- Apply the shared artifact-integrity discipline from `../_shared/references/workflow_accountability.md` before debugging behavior inside a newly changed deployed site.
- When a live webapp change is driven by review or external implementation feedback, apply the shared review discipline from `../_shared/references/workflow_accountability.md` before accepting the suggested patch shape.
- Use relative route sources like `handlers/contact.py` and `public` so the deploy stays portable.
- For public webserver configs, set `host: 0.0.0.0` unless there is a concrete reason not to.
- Treat a public site as designed output, not just working markup.
- For contact forms, ship an intentional visual system: hierarchy, spacing, styled fields, a deliberate button treatment, and success/error states that feel part of the site.
- Do not ship raw browser-default form controls, default Arial-on-white layouts, or full-width utility forms unless the user explicitly asked for that austere style.
- Keep handler modules simple at import time. A module that raises during import can surface to the public site as a generic `500`.
- Do not invent runtime environment variables. Use the actual implementation and currently configured environment. If a sender or SMTP env var is not documented in the implementation, do not assume it exists.
- For DB-backed or email-featured sites, default to the Python backend golden path in this skill before considering other backend approaches.
- If the site must write submissions into the room database, treat `meshagent-database-operator` as the canonical source for the exact `room.database.*` API shape and schema objects, then copy only that proven pattern into the handler.
- If the site must show stored submissions, reuse the proven repo read path from `contact_list_route.py`: `await room.database.search(table=...)`.
- For live sites with multiple side effects, keep the handler modular: validation, DB write, email send, and user response should be separate steps or helper functions rather than one mixed block.
- For existing handlers, prefer extracting new DB behavior into a separate helper module and changing the live handler by an import plus one narrow call site whenever that is practical.
- If a live handler already has a working GET or submit path, adding one new capability must not leave that existing path worse at the end of the run. Repair it before stopping, or explicitly restore the last known working handler state and report the new capability as still incomplete.
- If a handler starts importing a new helper module, verify that the helper file lives under the same deployable source tree and will be importable from the actual webserver `--app-dir` before treating later failures as DB, mail, or response bugs.
- Do not improvise `create_table_with_schema` schema entries inside a web handler. If DB-backed handler code needs types or schema shape, copy the exact proven `DataType`-based pattern from `meshagent-database-operator` and the resolved repo examples.
- Do not switch a handler to CLI-backed database writes when direct `room.database.*` calls are available in the runtime.
- For room-hosted contact forms, the sender address must come from a successful `meshagent mailbox list`, `meshagent mailbox show`, or `meshagent mailbox create` result in the current project.
- For a contact form that should email an external destination, the requested destination address is the `To` target, not the sender mailbox identity to provision.
- Do not provision or reuse a sender mailbox whose address equals the destination recipient by default. Only do that when the user explicitly asked for that exact sender identity and the runtime already proves it is authorized and intended.
- For a new mailbox provisioned for a contact form, do not accept a generic mailbox queue name such as `inbound-mail`, `mail`, or `inbox`. The mailbox queue should normally match the mailbox address unless the room already proves an intentional exception.
- A mailbox-backed sender address alone is not proof that the form has a working outbound mail path.
- Do not synthesize sender identities from the participant name or mail domain. In particular, do not invent `FROM_ADDRESS`, `MAIL_FROM`, `SMTP_FROM`, or `MESHAGENT_PARTICIPANT_NAME`.
- Do not default a contact form to ad hoc direct SMTP when a mailbox-backed room mail path is the real workflow.
- If the handler uses direct SMTP, use only the real room SMTP defaults documented in `mail_common.py`: `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_HOSTNAME`, and `SMTP_PORT`.
- Treat direct SMTP as an explicit fallback path, not the normal contact-form mail path. Use it only when the user asked for it or the runtime has already proven that SMTP configuration exists.
- Room containers do expose `MESHAGENT_API_URL`, but raw SMTP code must add its own hostname fallback if it wants to derive `SMTP_HOSTNAME` from that environment.
- If generated direct-SMTP code needs a hostname fallback because `SMTP_HOSTNAME` is null, derive it explicitly from `MESHAGENT_API_URL` using the environment-appropriate mail host from `../_shared/references/environment_profile_rules.md`.
- For Python handlers that render inline HTML, avoid `str.format()` across raw HTML, CSS, or regex-heavy strings unless every literal brace is escaped. CSS blocks and patterns like `{1,80}` otherwise break rendering at runtime.
- Prefer safer rendering approaches for generated handlers: placeholder replacement, `string.Template`, or another approach that does not reinterpret every `{...}` in the whole document.
- Validate on both client and server when the task includes user input, but treat server-side validation as authoritative.
- Sanitize submitted values before including them in responses, logs, or email bodies.

## Contact form workflow

1. Create the local webapp project under the current working directory.
2. Add a GET route that renders the form and a POST route that validates and handles submission.
3. Give the page a deliberate layout and visual identity before deploy; a plain stack of unlabeled browser-default controls is not enough.
4. Restrict email and phone fields with browser-side input types and patterns when helpful.
5. Re-validate all submitted fields on the server.
6. If the form persists submissions, route the DB API shape to `meshagent-database-operator`, then use that proven direct `room.database.*` pattern instead of inventing a handler-local CLI workflow or ad hoc schema objects.
7. Prefer implementing the DB write in a helper module first, then wire it into the live handler with the smallest practical import-and-call change.
8. Prove the DB insert path with a read-back before combining it with mail-send and response-handling changes.
9. If the DB change breaks a previously working submit path, fix that regression first or roll back to the last working handler before continuing DB debugging.
10. If the form sends outbound email from the room, inspect existing room mailboxes first.
11. If no suitable mailbox exists, create collision-resistant mailbox candidates derived from the room and workflow purpose.
12. If mailbox creation returns `409` and mailbox inspection is forbidden, treat that candidate as unavailable and try another candidate before asking for help.
13. After mailbox provisioning, verify that the mailbox queue wiring is valid for a new workflow. If the returned mailbox points at an invented or unverified generic queue name, treat that as a blocker and repair it before continuing.
14. For contact-form delivery to an external recipient, keep the addresses separate by default:
  - `From`: the MeshAgent-managed mailbox sender
  - `To`: the requested external recipient
  - `Reply-To`: the visitor email when present
15. Do not default a contact form to `From == To` when the `To` address is the user's external inbox.
16. Use the exact mailbox address returned by the CLI as the `From` address and use the visitor email only as `Reply-To` when present.
17. Prefer the room mail path and real mailbox-backed sender identity over ad hoc SMTP guesses.
18. Do not treat mailbox creation as proof that direct SMTP is configured or that a mailbox queue is visible in generic queue inspection.
19. Only fall back to custom raw SMTP code when the user explicitly asks for it or the mailbox-backed path is unavailable.
20. Before deploying a raw-SMTP form, prove that the runtime actually has a usable SMTP configuration instead of assuming the mailbox implies one.
21. When using direct SMTP, use the real room SMTP defaults from `mail_common.py`, explicitly add a hostname fallback from `MESHAGENT_API_URL` when `SMTP_HOSTNAME` is null, and use the mailbox-backed sender address from the CLI result.
22. If the user needs a hot-reload dev loop for Python handlers, hand the runtime loop to `meshagent-webapp-dev-operator` once the backend shape is clear.
23. If the user asks for a release candidate, release, promotion, or rollback-ready artifact, hand packaging and release lifecycle to `meshagent-webapp-release-operator` after the backend behavior is ready.
24. Verify the live site with actual GET and POST requests after deploy.

## Managed hostname selection

- Follow `../_shared/references/managed_hostname_rules.md` for suffix selection, collision handling, and validity checks.
- Managed hostname suffix is absolute: use only the environment-appropriate managed suffix from `../_shared/references/environment_profile_rules.md`.
- Before choosing, deploying, or reporting a managed hostname, resolve the active environment from `MESHAGENT_API_URL` and state the expected public suffix from `../_shared/references/environment_profile_rules.md`.
- In a `.life` room, `api.meshagent.life` and `mail.meshagent.life` still mean the public minisite suffix is `.meshagent.dev`. Do not reinterpret that mapping into `.meshagent.life`.
- Do not derive the public hostname from the mailbox address, mailbox domain, SMTP host, or API domain. Managed minisites use the managed public suffix, not the mail domain.
- Prefer collision-resistant hostname candidates derived from the room name plus the site purpose.
- If the user did not request a specific hostname, automatically try a small set of candidates before asking for naming input.
- Do not deploy with, report, or accept a managed hostname whose suffix does not match the active API environment.
- If the mailbox domain or other room evidence points at one environment profile but the chosen public hostname uses a different managed suffix family, treat that as an environment-resolution failure and stop before reporting the URL as valid.
- If a deploy command warns that the hostname uses the wrong managed suffix, treat that as a blocker and correct the hostname before reporting a deployed public site.
- If the room has a managed hostname whose suffix does not match the active environment profile, stop immediately. Do not continue with route debugging, edge debugging, DNS debugging, or app debugging behind that invalid hostname.
- If the chosen public hostname falls under a mail-domain family such as `mail.meshagent.life` or `mail.meshagent.com`, treat that as a hard construction error, not as a variant to test.

## Verification rules

- Apply the shared verification discipline from `../_shared/references/workflow_accountability.md`, then use the web-specific rules below for what counts as proof here.
- Apply the shared debugging discipline from `../_shared/references/workflow_accountability.md`, then use the web-specific rules below to isolate where the site is failing.
- For every website task, perform at least one live HTTP GET against the public URL and confirm that the final response is the expected successful page.
- For a normal HTML page or contact form, the final GET must succeed with the expected final status, normally `200`, after following any expected redirect.
- Confirm that the final page content matches the intended site, not just that some page responded.
- For form-backed sites, also exercise representative POST paths after deploy.
- For contact forms that write to the room database, verify the write with a follow-up `room.database.search(...)`, `meshagent room database search`, or a live list/read route that uses the same table.
- If a deploy starts failing with `ModuleNotFoundError`, `ImportError`, stale-file-handle errors, or route-load errors, treat that first as a deploy tree, app-dir, or mounted-file integrity problem before debugging DB or mail behavior.
- For contact forms that send mail, include one invalid POST and one valid POST in the verification flow.
- For contact forms that send mail, the valid POST must reach the success path or the exact mail blocker. A rendered form plus a failing submission is not a completed site.
- If a contact form used the external destination recipient as the sender mailbox or `From` address by default, treat that as a mail-path construction bug and repair it before reporting success.
- If a contact form claims to store submissions but the follow-up read path stays empty, treat that as a still-broken database workflow even if mail send succeeds.
- If the current deployed handler already works for other behavior, do not replace large working sections just to add one new capability unless the small additive change has already been proven insufficient.
- If the resulting public hostname uses the wrong managed suffix for the current environment, treat that as a failed deploy output and fix the hostname before reporting success.
- If the agent cannot state the resolved environment and its matching managed suffix before reporting the URL, the public-site verification is incomplete.
- A wrong-suffix managed hostname is not partial success and not useful evidence. It is an immediate hard failure of the public-site workflow.
- If DNS lookup fails for the public hostname, treat the public-site workflow as still blocked. Do not report the URL as working or deployed for user-visible purposes.
- If DNS or live HTTP reachability is still unproven, do not summarize the site as `Done`, `deployment complete`, or `public URL created successfully`. Report the deploy state as incomplete pending public verification.
- If the live GET does not reach the intended page with the expected final success status, normally `200`, treat the public-site workflow as still blocked even if DNS or an HTTP redirect works.
- If a live GET or POST returns `500`, inspect handler import/render/runtime failures before blaming room routing or platform infrastructure.
- Do not report a speculative "most likely cause" for a live `500` when the exact traceback, import error, or route-load failure can still be retrieved from logs or other room-visible evidence.
- If the first diagnosis attempt hits a private-container exec denial, do not keep retrying container exec. Switch to logs, service definition, room-visible source, or public behavior.
- If a public request returns `502` or another upstream-style error, inspect the deployed bind host, service port, and public route configuration before concluding the room is unhealthy.
- If the service is crashing or failing liveness checks, diagnose the service/runtime before continuing public-site verification.
- If repeated site patches fail to improve the same symptom, stop widening the handler patch and reassess the deploy shape, integration boundary, or send path.
- If a DB integration patch turns a previously working submit path into a `500`, repair or roll back that regression before summarizing the DB work as partial progress.
- If a contact-form task asks for emailed submissions, do not report success while live submission still fails to send mail.
- If a generated contact-form handler uses direct SMTP and `SMTP_HOSTNAME` is null, add an explicit fallback from `MESHAGENT_API_URL` using the environment-appropriate mail host from `../_shared/references/environment_profile_rules.md`.
- If a contact-form handler still cannot prove a usable SMTP hostname after that environment fallback, treat it as a blocker and switch back to the mailbox-backed room mail path or report the exact mail-configuration blocker.
- Distinguish SMTP transport from sender authorization. A form that renders but fails with `SMTPDataError`, `550`, `553`, or similar on valid submission is not complete.
- If outbound mail fails with an authorization error such as `550 5.7.1 Permission denied`, switch to mailbox-backed sender provisioning if permissions allow, then re-test.
- If code still references a synthesized sender address after mailbox provisioning fails, treat that as an implementation bug and replace it with a real mailbox-backed address or report the exact mailbox blocker.
- Only stop and ask the user for help after mailbox provisioning, route creation, or deploy verification is blocked by a concrete error you can report exactly.

## Workflow accountability

- If another skill already owns the workflow, return deploy, HTTP, and mail evidence to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.
