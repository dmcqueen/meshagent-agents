---
description: Inspect MeshAgent state, sessions, calls, tokens, versions, and other diagnostics without changing resources.
argument-hint: "<inspection or troubleshooting task>"
---

# /meshagent-inspect

Use this command for non-destructive MeshAgent inspection and troubleshooting.

## Primary command groups

- `meshagent version`
- `meshagent auth whoami`
- `meshagent session ...`
- `meshagent token ...`
- `meshagent call ...`
- `meshagent rooms ...`
- `meshagent room ...`
- `meshagent service show`
- `meshagent service list`
- `meshagent port ...`

## Operating rules

1. Prefer read-only commands first.
2. If the request escalates from inspection to mutation, switch to the more specific command file or keep following the skill.
3. Include the exact command path you used in the final summary.
