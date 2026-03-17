---
description: Project-scoped MeshAgent administration for auth, projects, api keys, secrets, webhooks, routes, mailboxes, and scheduled tasks.
argument-hint: "<project admin task>"
---

# /meshagent-project

Use this command when the request is primarily about project-level administration.

## Primary command groups

- `meshagent setup`
- `meshagent auth ...`
- `meshagent project ...`
- `meshagent api-key ...`
- `meshagent secret ...`
- `meshagent webhook ...`
- `meshagent mailbox ...`
- `meshagent route ...`
- `meshagent scheduled-task ...`

## Operating rules

1. Confirm the active project before making changes.
2. Never print secret values unless the user explicitly asks for them and the command returns them.
3. For create or update operations, restate the exact target resource first.
4. Verify changes with a read command immediately afterward.
