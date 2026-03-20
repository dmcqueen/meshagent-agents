---
name: meshagent-webmaster-operator
description: Manage MeshAgent domain mappings and use the sample MeshAgent static webserver YAML as a reference example.
---

# MeshAgent Webmaster Operator

Use this skill for domain mappings, what they do, and the sample static webserver YAML example.

## Use this skill when

- The task involves `meshagent route ...` creation, inspection, update, or deletion.
- The user needs to understand what a domain mapping does.
- The user needs the sample MeshAgent webserver YAML as an example of serving raw HTML and JavaScript statically.
- The user wants to verify which room and port a public hostname points to.

## References

- Use `references/command_groups.md` and `references/meshagent_cli_help.md` for exact CLI command shapes and flags.
- The sample static webserver YAML in the MeshAgent server repository lives at `meshagent-router/meshagent/router/templates/webserver.yaml`.

## Live room execution

- If this skill is running inside a live MeshAgent room runtime, first use the existing MeshAgent CLI session and room context before asking the user to log in again.
- If `MESHAGENT_API_URL` is present and the user wants a default MeshAgent-managed hostname, derive it from the API environment: use `*.meshagent.app` for `.com` environments and `*.meshagent.dev` for `.life` environments.
- If `MESHAGENT_API_URL` is absent or ambiguous, inspect existing routes or ask before choosing a managed public hostname.
- Do not copy `.meshagent.app` from generic CLI examples when `MESHAGENT_API_URL` indicates a `.life` environment. The route hostname suffix must follow the current API environment, not the example text.
- Before deploy or reply, validate the final managed hostname against `MESHAGENT_API_URL`. For `https://api.meshagent.life`, a reported `.meshagent.app` hostname is invalid and must be corrected or redeployed as `.meshagent.dev`.
- If route access is uncertain, try a read command such as `meshagent route list` or `meshagent route show` first and use the observed result.
- If `MESHAGENT_ROOM` is already present, do not block on room-listing commands before attempting a room-scoped webserver deploy.

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

This is the sample static webserver YAML from the MeshAgent server repository. It shows a simple static HTTP server that exposes raw files from room storage:

```yaml
version: v1
kind: ServiceTemplate
metadata:
  name: web server
  description: Publish a website for this room with the contents of the "website" folder. 
  annotations:
    meshagent.service.id: meshagent.webserver
variables:
  - name: url
    type: route
    optional: false
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

This example is for serving static HTML, CSS, JavaScript, and similar assets. It is only a reference example, not a website-building guide.

## Route workflow

1. Inspect existing routes with `meshagent route list` or `meshagent route show`.
2. Confirm the exact hostname, room, and published port.
3. Create, update, or delete the route.
4. Verify that the hostname points to the intended room and service port.

## Verification rules

- If a derived managed hostname collides with an existing route, keep the same environment-specific suffix and choose a different subdomain. Do not switch to the wrong suffix family to avoid the collision.
- If `meshagent webserver deploy --domain ...` fails with a collision and a follow-up route read returns 403, treat that hostname as unavailable and try a different candidate before concluding that public route permissions are blocked.
- Do not report success with a live URL unless the hostname suffix is valid for the active API environment.
- Do not stop at "the MeshAgent CLI is not logged in" unless an actual route or related MeshAgent command fails with an authentication or authorization error.
