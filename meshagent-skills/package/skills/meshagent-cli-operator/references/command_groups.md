# MeshAgent CLI command groups

Use this file to choose the narrowest MeshAgent CLI area before reading the full help reference.
This reference set is anchored to the MeshAgent CLI version recorded in `compat.json`.

Room-runtime default: when executing commands inside `meshagent/shell-codex:default`, prefer `/usr/bin/meshagent ...`.
For room-visible runtime data, use `/data`.
If the user asks to create or write a room-visible file and does not give a more specific path, default to `/data/<filename>`.
For `meshagent webserver deploy`, keep the local website source tree under the current working directory and use `--website-path` as the room-storage destination.
For this skill, the current room is the value of `MESHAGENT_ROOM`.
For website, route, and public hostname work in this environment, the managed hostname suffix is fixed by `MESHAGENT_API_URL` and the shared environment profile rules. If the environment is still unclear, inspect an existing route or ask before inventing a hostname.
Do not derive a public minisite hostname from the mailbox domain, SMTP hostname, or API hostname. A mail domain such as `mail.meshagent.life` is not a public site suffix.
Example: `api.meshagent.life` and `mail.meshagent.life` still map public minisites to `.meshagent.dev`, not `.meshagent.life`.
The packaged CLI help may show `.meshagent.app` in examples. Treat those as static examples, not as the environment-specific suffix to use in the current runtime.
Before using or returning a managed hostname, validate that its suffix matches `MESHAGENT_API_URL` and the environment-appropriate managed suffix.

## Top-level command policy

Use the following status values exactly:

- `USE`: normal command family for this skill.
- `USE WITH CAUTION`: allowed only when clearly needed and with tight scope.
- `DON'T USE`: out of scope for this skill.

### `USE`

- `meshagent call`
  Use for room-scoped inspection, verification, or targeted invocation when the task is about the current room or a room-local agent/tool.
- `meshagent session`
  Use for diagnostics, active session inspection, and troubleshooting related to the current room workflow.
- `meshagent token`
  Use for token inspection or troubleshooting when it is directly relevant to the current room task. Do not use `meshagent token generate`.
- `meshagent service`
  Use for service validation, rendering, inspection, and deployment when the target is the current room or a room-specific service flow. If a `--room` flag is used, it must match the current room. Do not use project-global service modes.
- `meshagent mcp`
  Use for room-relevant MCP bridge or connector work when it supports the current room workflow.
- `meshagent rooms`
  Use for room listing, inspection, and room creation/update/delete only when the user explicitly wants room lifecycle work in the current project. If a command targets a room by name or ID, do not use it for a room other than the current room unless the user explicitly asks for room lifecycle work.
- `meshagent meeting-transcriber`
  Use for transcriber runtime flows when the task is clearly about deploying or operating that runtime.
- `meshagent port`
  Use for room port inspection and exposure work tied to the current room. If a `--room` flag is used, it must match the current room.
- `meshagent webserver`
  Use for room webserver deployment and web content hosting tasks. If a `--room` flag is used, it must match the current room. Prefer the managed hostname suffix derived from `MESHAGENT_API_URL` by default in this environment.
- `meshagent codex`
  Use for Codex-backed runtime operations that stay within room scope.
- `meshagent voicebot`
  Use for voicebot runtime deployment and operation in the current room. If a `--room` flag is used, it must match the current room.
- `meshagent chatbot`
  Use for chatbot runtime deployment and operation in the current room. If a `--room` flag is used, it must match the current room.
- `meshagent process`
  Use for process room agents in the current room. If a `--room` flag is used, it must match the current room.
- `meshagent mailbot`
  Use for mailbot runtime deployment and operation in the current room. If a `--room` flag is used, it must match the current room.
- `meshagent task-runner`
  Use for task-runner deployment and operation in the current room. If a `--room` flag is used, it must match the current room.
- `meshagent worker`
  Use for worker runtime deployment and operation in the current room. If a `--room` flag is used, it must match the current room.
- `meshagent room`
  Use first for room-scoped agents, services, storage, messaging, database, memory, containers, sync, and developer operations in the current room.

### `USE WITH CAUTION`

- `meshagent version`
  Use only when the user explicitly asks about the installed CLI version or version-specific behavior.
- `meshagent project`
  Use only for project context needed to complete room work. Subcommand policy:
  - `meshagent project list`: allowed for read-only discovery of available projects.
  - `meshagent project activate PROJECT_ID`: allowed only when a room task clearly requires switching to a specific existing project first.
  - `meshagent project activate -i`: don't use, because the interactive flow can create a new project.
  - `meshagent project create`: don't use, because creating new projects is broader than this skill's room-focused scope.
- `meshagent webhook`
  Use only when the room task requires project-level webhook configuration tied to the room's workflow.
- `meshagent secret`
  Don't use. Project secret management is broader than this skill's room-focused scope.
- `meshagent mailbox`
  Use for mailbox provisioning or inspection when a room workflow needs it.
- `meshagent route`
  Use only when the room task requires route configuration backing the current room's service exposure. Prefer the managed hostname suffix derived from `MESHAGENT_API_URL` by default in this environment.
- `meshagent scheduled-task`
  Use only when the room task requires scheduled execution tied to the current room's workflow.
- `meshagent helper`
  Use only when the user explicitly needs developer helper HTTP services such as hosted schemas or toolkits.

### `DON'T USE`

- `meshagent setup`
  Do not use. Initial CLI setup is out of scope for this skill.
- `meshagent auth`
  Do not use. Interactive auth and user-session management are out of scope for this skill.
- `meshagent api-key`
  Do not use. API key creation and management are out of scope for this skill.
- `meshagent token generate`
  Do not use. Minting participant tokens is broader than this skill's room-focused scope.
- `meshagent project create`
  Do not use. Creating new projects is broader than this skill's room-focused scope.
- `meshagent project activate -i`
  Do not use. The interactive activation flow can create new projects and is too broad for this skill.
- `meshagent secret`
  Do not use. Project secret management is broader than this skill's room-focused scope.

## Preferred routing

- For room-scoped tasks, start with `meshagent room ...`.
- When the task is room service discovery, prefer `meshagent room service list` over generic `meshagent room agent invoke-tool` calls.
- For runtime deployment tasks, prefer the specific runtime family such as `meshagent process ...`, `meshagent chatbot ...`, `meshagent worker ...`, or `meshagent webserver ...`.
- Use `meshagent service ...` when the task is specifically about service specs, templates, validation, rendering, or deployment mechanics.
- Use `meshagent rooms ...` only when the user explicitly wants room lifecycle changes such as create/list/update/delete.
- If a command accepts `--room`, do not target any room other than `MESHAGENT_ROOM`.
- For room-site requests, deploy in the current room and return the public URL only after live verification succeeds. Do not treat local example-app edits, local build output, route creation, deploy success, DNS resolution, or a redirect alone as completion of a room deployment request.
- For room-site requests that use `meshagent webserver deploy`, create the local app under the current working directory, keep route sources relative to the routes file when possible, and upload to room storage with `--website-path`.
- If `MESHAGENT_ROOM` is already available, do not block on `meshagent rooms list` before attempting the room-scoped deploy.
- Do not add room-messaging enablement to a site, contact-form, mail, or runtime workflow unless the user explicitly asked for room messaging itself.
- For deployed websites, verify the live URL with a real HTTP GET and confirm the final response is the intended page with the expected final success status, normally `200`, before replying with success.
- For contact forms, verify both the GET render path and at least one POST path after deploy. A live 500 is not an acceptable final state.
- For deployed sites, do not use repeated `meshagent room container exec` attempts against another participant's private container as the primary debug path. Prefer service list, developer watch, container logs, public HTTP checks, and deployed artifacts first.
- For managed public hostnames, prefer collision-resistant candidates that include the room name or another room-specific suffix instead of generic names like `contact-site`.
- If the first hostname candidate collides, retry additional candidates automatically and keep the same environment-specific suffix family.
- If `meshagent webserver deploy --domain ...` returns a collision and route inspection is forbidden, do not stop there. Treat the hostname as unavailable and try a different candidate before reporting a permissions blocker.
- Managed hostname suffix is absolute, not advisory: never return anything except the environment-appropriate managed suffix, even if packaged examples or previous failed attempts used the wrong suffix.
- If a deployed webserver returns 500, inspect the route handler code and runtime assumptions before declaring a room or platform routing issue.
- Use `meshagent-mail-operator` for mailbox, inbox, process `mail:` channel, or contact-form email workflows.
- Use `meshagent-scheduler` for scheduled-task creation, update, pause, resume, or deletion.
- Use `meshagent-webapp-backend-builder` for websites, contact forms, `meshagent webserver ...`, or room-hosted web handlers.
- Use `meshagent-webapp-dev-operator` when the main need is a hot-reload dev loop for a room-hosted webapp backend.
- Use `meshagent-webapp-release-operator` when the main need is an image-backed candidate or release for a room-hosted webapp.
- Use `meshagent-webmaster` for explicit route management or public hostname exposure.
- Escalate to `USE WITH CAUTION` command families only when room-scoped commands are insufficient.

## Notes

- `meshagent room ...` is the deepest public area. Use it for room-scoped agents, storage, messaging, services, database tables, memories, containers, and sync.
- For this skill, prefer room-scoped commands over project-scoped commands whenever both could satisfy the request.
- The help reference documents command names and flags. In this runtime, prefer `/usr/bin/meshagent` as the executable path.
