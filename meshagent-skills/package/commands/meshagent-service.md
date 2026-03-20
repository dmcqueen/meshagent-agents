---
description: Service and deployment workflows in MeshAgent, including service specs, templates, MCP bridges, helper services, and webservers.
argument-hint: "<service or deployment task>"
---

# /meshagent-service

Use this command for MeshAgent service lifecycle and service-adjacent runtime operations.

## Primary command groups

- `meshagent service ...`
- `meshagent mcp ...`
- `meshagent helper ...`
- `meshagent webserver ...`
- `meshagent codex ...`

## Operating rules

1. Inspect or validate specs before create or update when possible.
2. Prefer `validate`, `render-template`, `show`, or `list` before destructive or state-changing commands.
3. After deploy or update, verify the resulting service state and surface any follow-up steps.
4. Use [SKILL.md](../skills/meshagent-webapp-builder/SKILL.md) for websites, contact forms, `meshagent webserver ...`, and room-hosted webapp deployment.
5. Use [SKILL.md](../skills/meshagent-webmaster/SKILL.md) for explicit route/domain administration or public hostname diagnostics.
