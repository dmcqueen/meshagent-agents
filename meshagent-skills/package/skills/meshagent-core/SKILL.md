---
name: meshagent-core-operator
description: Core rules for MeshAgent room work. Use this skill to choose safe command paths, ground behavior in the code repo, and verify real user-visible outcomes.
metadata:
  short-description: Standalone highest-signal rules for live room work.
---

# MeshAgent Core Operator

## Use this skill when

- The task touches the MeshAgent CLI, a live room, or anything running inside it.
- The user wants a real outcome, not just a command suggestion.
- The workflow involves websites, mail, queues, services, runtime, scheduling, database, storage, or routes.

## Highest-priority rules

- Do not guess implementation behavior. When exact behavior matters, inspect the code repo directly first.
- Use the current room/runtime context first. If `MESHAGENT_ROOM` is already known, prefer room-scoped commands over broad discovery.
- Prefer the narrowest command path that matches the task.
- Prefer inspection before mutation.
- After any mutation, verify on the matching read surface: `show`, `list`, logs, queue receive, live HTTP, or real delivery evidence.

## Workflow ownership

- Keep exactly one owner for the user-visible outcome.
- Supporting skills return evidence, not “done”.
- Do not stop at an internal actionable blocker if the normal next fix is still available.
- Do not say “done” until the user-visible result is verified or the exact blocker is proven.

## Real-surface verification

- Verify on the real surface, not on a precursor.
- Object creation is not success.
- YAML generation is not deployment.
- Route creation is not a working site.
- Queue growth is not email delivery.
- Service creation is not runtime health.
- For public sites, require live HTTP verification.
- For contact forms, require GET plus representative POST verification.
- If public DNS or live HTTP is unproven, report partial/incomplete state, not completion.

## Managed hostname rules

- Resolve the active environment from `MESHAGENT_API_URL`.
- Use only the environment-correct managed public suffix.
- Managed public hostnames and managed mailbox domains are different surfaces.
- Do not derive a public hostname from the mailbox domain, SMTP hostname, or API hostname.
- In `.life`, managed minisites are still `.meshagent.dev`.
- Treat wrong-suffix hostnames as hard errors, not debugging leads.
- If the hostname suffix is wrong for the environment, stop immediately and fix that first.

## Webapp rules

- Default backend path: Python `aiohttp` handlers with `meshagent webserver`.
- For active Python iteration, the preferred dev loop is `meshagent webserver join --watch`.
- Do not treat `meshagent webserver deploy` as Python hot reload.
- Use room-storage source paths like `/<site-dir>`; in the live shell they appear under `/data/<site-dir>`.
- For live handler work, keep changes narrow and verify that the changed behavior is actually live.

## Mail rules

- Treat “send an email” as real outbound email by default.
- Do not treat mailbox creation, queue creation, or queue enqueue as success for an email-send request.
- `MESHAGENT_TOKEN` should be used as the `SMTP_PASSWORD`.
- Use the environment-correct managed mailbox domain for MeshAgent mailbox-backed senders.
- Mailbox addresses MUST be derived from the room name and `MESHAGENT_MAIL_DOMAIN`.
- Default contact-form pattern:
  - `From`: MeshAgent-managed mailbox sender
  - `To`: requested external recipient
  - `Reply-To`: visitor email when present
- Do not default `From == To` when `To` is the user’s external inbox.
- Do not invent sender identities from participant names or mail domains.
- For new mailboxes, mailbox address and mailbox queue MUST be a full match.
- Treat sender addresses outside the expected managed mailbox domain family as suspect unless the runtime already proves they are authorized.
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
- Database: inspect the real `room.database.*` implementation in the repo; do not invent schema/API forms.
- Storage: verify the exact room path before assuming files are present or deployed.
- Scheduler: timezone and future-run correctness matter; a scheduled-task record alone is not workflow success.

## Code-grounding rules

- When exact API shape or implementation behavior matters, inspect the code repo directly before guessing.
- Prefer implementation over memory for CLI flags, token behavior, runtime env vars, API shapes, and mail/runtime behavior.
- If the code still does not answer the question clearly, report the uncertainty instead of inventing behavior.
