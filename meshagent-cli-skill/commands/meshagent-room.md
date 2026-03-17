---
description: Room lifecycle and room API operations in MeshAgent, including agents, storage, messaging, containers, services, database, memory, and sync.
argument-hint: "<room task>"
---

# /meshagent-room

Use this command when the request targets a room or something running inside a room.

## Primary command groups

- `meshagent rooms ...`
- `meshagent room agent ...`
- `meshagent room secret ...`
- `meshagent room queue ...`
- `meshagent room messaging ...`
- `meshagent room storage ...`
- `meshagent room service ...`
- `meshagent room developer ...`
- `meshagent room database ...`
- `meshagent room memory ...`
- `meshagent room container ...`
- `meshagent room sync ...`
- `meshagent port ...`

## Operating rules

1. Resolve the room name first.
2. Inspect current room state before changing it.
3. Use the room-scoped command instead of the project-scoped equivalent when the request is clearly about a single room.
