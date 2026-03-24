---
name: meshagent-webmaster
description: Manage MeshAgent domain mappings and use the sample MeshAgent static webserver YAML as a reference example.
metadata:
  short-description: Operate routes and managed hostnames for published room services.
  references:
    bundled:
      - ../meshagent-cli-operator/references/command_groups.md
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - references/static_webserver_example.yaml
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/managed_hostname_rules.md
    requires_roots:
      - router_root
      - server_root
      - cli_root
    resolved_targets:
      - route CLI help
      - static webserver YAML example
  related_skills:
    - skill: meshagent-cli-operator
      when: General room-context and managed-hostname rules matter.
    - skill: meshagent-sdk-researcher
      when: Checkout roots or the sample static webserver YAML path must be resolved.
    - skill: meshagent-webapp-builder
      when: The task is building or debugging the website, not just the route.
    - skill: meshagent-service-operator
      when: The target service itself must be created or repaired before routing it.
  scope:
    owns:
      - route creation and mutation
      - managed hostname verification
      - static webserver example lookup
    excludes:
      - website implementation
      - service lifecycle by itself
---

# MeshAgent Webmaster

Use this skill for domain mappings, what they do, and the sample static webserver YAML example.

## Use this skill when

- The task involves `meshagent route ...` creation, inspection, update, or deletion.
- The user needs to understand what a domain mapping does.
- The user needs the sample MeshAgent webserver YAML as an example of serving raw HTML and JavaScript statically.
- The user wants to verify which room and port a public hostname points to.

## References

- Use `../meshagent-cli-operator/references/command_groups.md` and `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact CLI command shapes and flags.
- Use `references/static_webserver_example.yaml` for the bundled static webserver example.
- Use `../_shared/references/live_room_cli_context.md` for shared room-context rules.
- Use `../_shared/references/managed_hostname_rules.md` for shared managed-hostname selection and validation rules.
- The sample static webserver YAML should be located by resolving the router/server tree through `meshagent-sdk-researcher`, not by assuming a fixed repo-relative path.

## Related skills

- `meshagent-cli-operator`: Reuse its general room-context and managed-hostname rules instead of inventing environment behavior locally.
- `meshagent-sdk-researcher`: Resolve checkout roots and the sample static webserver YAML path before using codebase references.
- `meshagent-webapp-builder`: Use it when the task is building or debugging the website rather than operating the route.
- `meshagent-service-operator`: Use it when the target service must be created, validated, or repaired before routing it.

## Live room execution

- Apply `../_shared/references/live_room_cli_context.md` before asking for login or room discovery.
- Apply `../_shared/references/managed_hostname_rules.md` for managed hostname suffix selection and collision handling.
- If route access is uncertain, try a read command such as `meshagent route list` or `meshagent route show` first and use the observed result.

## Primary command groups

- `meshagent route create`
- `meshagent route update`
- `meshagent route show`
- `meshagent route list`
- `meshagent route delete`

## Domain mapping model

- A route maps a public hostname to a published service port.
- Creating a route publishes an existing service; it does not build a website for you.
- Updating a route changes where the hostname points.
- Deleting a route removes public exposure for that hostname.
- Always verify the target room and port before mutating a route.

## Static webserver example

See `references/static_webserver_example.yaml` for the bundled static webserver YAML example.

This example is for serving static HTML, CSS, JavaScript, and similar assets. It is only a reference example, not a website-building guide.

## Route workflow

1. Inspect existing routes with `meshagent route list` or `meshagent route show`.
2. Confirm the exact hostname, room, and published port.
3. Create, update, or delete the route.
4. Verify that the hostname points to the intended room and service port.

## Verification rules

- Follow `../_shared/references/managed_hostname_rules.md` before reporting a managed URL or retrying a colliding hostname.
- Do not stop at "the MeshAgent CLI is not logged in" unless an actual route or related MeshAgent command fails with an authentication or authorization error.
