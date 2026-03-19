---
name: meshagent-webmaster-operator
description: Manage MeshAgent domain mappings and use the standard static webserver template as a reference example.
---

# MeshAgent Webmaster Operator

Use this skill for domain mappings, route inspection, and a static webserver reference example.

## Use this skill when

- The task involves `meshagent route ...` creation, inspection, update, or deletion.
- The user needs to understand what a domain mapping does.
- The user needs a simple reference for exposing raw HTML and JavaScript through a static webserver service.
- The user wants to verify which room and port a public hostname points to.

## References

- Use `references/command_groups.md` and `references/meshagent_cli_help.md` for exact CLI command shapes and flags.
- The standard static webserver example lives at `meshagent-router/meshagent/router/templates/webserver.yaml`.

## Primary command groups

- `meshagent route create`
- `meshagent route update`
- `meshagent route show`
- `meshagent route list`
- `meshagent route delete`

## Domain mapping model

- A route maps a public hostname to a published service port.
- Creating a route publishes an existing service; it does not build a website.
- Updating a route changes where the hostname points.
- Deleting a route removes public exposure for that hostname.
- Always verify the target room and port before mutating a route.

## Static webserver example

The standard static example is a service template that runs a basic HTTP server and exposes raw files from room storage:

```yaml
version: v1
kind: ServiceTemplate
metadata:
  name: web server
variables:
  - name: url
    type: route
    annotations:
      meshagent.route.port: "5002"
container:
  image: busybox
  command: sh -c "httpd -f -p 5002 -h /data"
  storage:
    room:
      - path: /data
        subpath: /website
ports:
  - num: 5002
    type: http
    public: true
    published: true
    liveness: /
```

This example is for serving static HTML, CSS, JavaScript, and similar assets. It is a reference example, not a website-building or deployment guide.

## Route workflow

1. Inspect existing routes with `meshagent route list` or `meshagent route show`.
2. Confirm the exact hostname, room, and published port.
3. Create, update, or delete the route.
4. Verify that the hostname points to the intended room and service port.

## Out of scope

- Designing or building websites.
- Contact forms, mail delivery, application backends, or agent logic.
- General room runtime troubleshooting unrelated to route/domain mapping.
