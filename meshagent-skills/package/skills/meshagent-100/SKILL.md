---
name: meshagent-core-operator
description: Run MeshAgent room workflows safely: choose the right CLI path, use the current room context, build/debug room webapps, operate mail/queues/services/storage/database, and verify real user-visible outcomes.
metadata:
  short-description: Highest-signal MeshAgent rules for live room work.
---

# MeshAgent Core Operator

## Use this skill when

- The task touches the MeshAgent CLI, a live room, or anything running inside it.
- The user wants an end-to-end outcome, not just one command.
- The workflow involves websites, mail, queues, services, runtime, scheduling, database, storage, or routes.

## Core rules

- Prefer the current live room context. Use `MESHAGENT_ROOM` when it already exists.
- For room-scoped work, prefer `meshagent room ...` over broader project-scoped commands.
- Do not start with `meshagent auth whoami`, `meshagent project list`, or broad room discovery for a known-room task.
- Use packaged CLI references first; only use live `--help` when needed.
- Prefer the narrowest command path that matches the task.
- Prefer inspection before mutation.
- After any mutation, verify with the matching read surface: `show`, `list`, logs, queue receive, live HTTP, or real delivery evidence.

## Workflow ownership

- Keep exactly one owner for the user-visible outcome.
- Supporting skills return evidence, not “done”.
- Do not stop at an internal actionable blocker if the normal next fix is still available.
- Do not say “done” until the user-visible result is verified or the exact blocker is proven.

## Verification rules

- Verify on the real surface, not on a precursor.
- Object creation is not success.
- YAML generation is not deployment.
- Route creation is not a working site.
- Queue growth is not email delivery.
- For public sites, require live HTTP verification.
- For contact forms, require GET plus representative POST verification.
- If public DNS or live HTTP is unproven, report partial/incomplete state, not completion.
- If the managed hostname suffix is wrong for the environment, stop immediately and fix that first.

## Managed hostname rules

- Resolve the active environment from `MESHAGENT_API_URL`.
- Use only the environment-correct managed public suffix.
- Do not derive a public hostname from the mailbox domain, SMTP hostname, or API hostname.
- In `.life`, managed minisites are still `.meshagent.dev`.
- Treat wrong-suffix hostnames as hard errors, not debugging leads.

## Webapp rules

- Default backend path: Python `aiohttp` handlers with `meshagent webserver`.
- Use the backend skill for handlers, DB integration, mail integration, deploy shape, and public verification.
- Use the frontend skill only for richer interactive UI on top of that backend path.
- For active Python iteration, the preferred dev loop is `meshagent webserver join --watch`.
- Do not treat `meshagent webserver deploy` as Python hot reload.
- Use room-storage source paths like `/<site-dir>`; in the live shell they appear under `/data/<site-dir>`.

## Mail rules

- Default contact-form pattern:
  - `From`: MeshAgent-managed mailbox sender
  - `To`: requested external recipient
  - `Reply-To`: visitor email when present
- Do not default `From == To` when `To` is the user’s external inbox.
- Do not invent sender identities from participant names or mail domains.
- Use mailbox-backed sender addresses returned by real mailbox commands.
- For new mailbox-backed workflows, mailbox address and mailbox queue should normally match.
- Treat `550`, `553`, and similar SMTP failures first as sender identity or authorization problems.
- `550 5.7.1 Permission denied` means the runtime is not authorized to send from that sender identity.

## Service/runtime rules

- Use generated specs over handwritten YAML whenever the CLI can generate the runtime shape.
- Validate YAML before deploy when a file is involved.
- Use runtime inspection for live state: service list, developer watch, container list/logs, toolkit visibility.
- Do not rely on repeated `container exec` into another private container.
- If a runtime issue is really a webapp behavior issue, move back to the webapp path instead of treating it as generic container debugging.

## Queue/database/storage/scheduler rules

- Queue: prove real dequeue/processing, not just queue size movement.
- Database: use the proven `room.database.*` shape from docs/examples; do not invent schema/API forms.
- Storage: verify the exact room path before assuming files are present or deployed.
- Scheduler: timezone and future-run correctness matter; a scheduled-task record alone is not workflow success.

## Research rules

- When exact API shape or implementation behavior matters, resolve the checkout roots first and inspect docs/examples/source.
- Do not guess SDK shapes, CLI flags, token behavior, or runtime environment variables when the repo already contains the answer.
