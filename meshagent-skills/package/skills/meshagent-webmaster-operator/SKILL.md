---
name: meshagent-webmaster-operator
description: Operate MeshAgent website, webserver, route, and public-hostname workflows in the current room. Use this skill for webserver routes files, site deployment, route management, and public URL verification.
---

# MeshAgent Webmaster Operator

Use this skill for `meshagent webserver ...`, `meshagent route ...`, and live room-site deployment.

## Use this skill when

- The user wants to make, update, or deploy a site in the current room.
- The task involves `meshagent webserver ...` routes files, handlers, static assets, local join, spec generation, or deploy flows.
- The task involves `meshagent route ...` creation, inspection, update, or deletion.
- The task requires a public URL, hostname, domain, or route-backed exposure for a room website.

## Shared runtime

Use the room runtime defined in `../meshagent-cli-operator/SKILL.md`.

- Use the companion references in `../meshagent-cli-operator/references/command_groups.md` and `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact command shapes and flags.

## Primary command groups

- `meshagent webserver check`
- `meshagent webserver init`
- `meshagent webserver add`
- `meshagent webserver join`
- `meshagent webserver spec`
- `meshagent webserver deploy`
- `meshagent route create`
- `meshagent route update`
- `meshagent route show`
- `meshagent route list`
- `meshagent route delete`

## Operating rules

- Treat a room-site request as complete only when the site is actually deployed in the current room and you can report the resulting public URL or the exact blocker.
- For website, route, and public hostname work, default to `*.__MESHAGENT_PUBLIC_DOMAIN__` hostnames unless the user explicitly asks for a different MeshAgent public domain.
- Create and modify site assets under `/data`.
- Do not stop at local file edits or a successful local `webserver check` when the requested outcome is a live room website.
- If the public URL returns a timeout, `502`, or another unsuccessful response after deploy, treat the task as still in progress. Inspect the deployed room service and related room state, repair the deployment, and retest instead of asking the user whether you should continue with normal debugging.
- Prefer `meshagent webserver deploy` when the goal is a deployed room website. Use `meshagent route ...` directly only when route management is explicitly requested or when you need manual routing without `--domain`.
- Use `meshagent webserver check` before deploy when the routes file or asset mapping may be invalid.
- Use `meshagent webserver spec` when the user explicitly wants the generated service spec or when inspecting deployment shape before mutating.
- Use `meshagent webserver join` only for local runtime validation or debugging, not as the completion state for a room-site deployment request.
- When deploying, set `--room "${MESHAGENT_ROOM}"` unless the user explicitly asks for a different room-scoped target.
- When deploying, provide a real `--website-path` that matches the room storage subpath where the routes file and referenced assets should live.
- Prefer `--domain` on `meshagent webserver deploy` when the site should be publicly reachable and the route should follow the deploy.
- If using `meshagent route create` or `update` manually, verify the domain, room, and published port exactly before mutating.
- If a route already exists and targets a different room, stop and report that conflict instead of silently repointing it.
- If the deployed site service is restarting, unhealthy, or failing to serve traffic, inspect the exact deployed service configuration, the room-visible site files under `/data`, and the relevant room service or container state before concluding. Repair the mismatch and redeploy when the issue is within the room workflow.
- Do not modify unrelated example apps, sample repos, bundled SDK examples, or maintainer reference projects to satisfy a room deployment request.
- After deploy or route mutation, verify the resulting service and route state with the corresponding read commands and report the live public URL.

## Default workflow

1. Resolve the room target, public hostname expectation, and desired site path.
2. Build or update the site assets under `/data`.
3. Validate the routes file with `meshagent webserver check`.
4. Deploy with `meshagent webserver deploy`, usually with `--room "${MESHAGENT_ROOM}"`, `--website-path`, and `--domain`.
5. Verify the resulting service state, route state, and public URL behavior.
6. If the site is not actually reachable or the service is unhealthy, inspect the deployed state, repair it, redeploy, and retest.
7. Return the exact public URL, or the exact remaining blocker if the site is not actually reachable yet.

## Command-specific guidance

### Webserver routes files

- `meshagent webserver init` creates a scaffold when no routes file exists.
- `meshagent webserver add` is the fastest way to add a static or python route entry.
- Route paths must start with `/`.
- `python` and `static` sources without a leading `/` resolve relative to the routes file.
- For Python handlers, use the supported handler signature documented by the CLI help: `handler(*, room: RoomClient, req: web.Request) -> web.StreamResponse`.

### Webserver deploy

- Prefer `meshagent webserver deploy` for room-site deployment.
- Use `--website-path` consistently so the deployed container can resolve the routes file and referenced assets.
- Use `--domain` when you want deploy to create or update the route automatically.
- If the request is specifically about a public website, do not call the task complete until deploy, route verification, and a successful public URL check are done.

### Route management

- Use `meshagent route list` or `show` before `create`, `update`, or `delete`.
- Default to hostnames under `__MESHAGENT_PUBLIC_DOMAIN__` unless the user asks otherwise.
- Treat route `update` and `delete` as destructive.
- Re-run a read command after any mutation to confirm the final room and port target.

## Out of scope

- Do not use this skill for mailbox, inbox, or MailBot workflows; use `meshagent-mail-operator` for those.
- Do not use this skill for scheduled-task workflows; use `meshagent-scheduling-operator` for those.
- Do not use this skill for generic room runtime work that is not about sites, routes, or public web exposure; use `meshagent-cli-operator` for that.
