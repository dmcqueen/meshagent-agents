---
name: meshagent-runtime-operator
description: Operate and debug live MeshAgent room runtime state. Use this skill for developer log streaming, container listing/logs/exec/run/image operations, and local port forwarding into room containers.
metadata:
  short-description: Debug live room runtime state, containers, logs, and port forwarding.
  references:
    bundled:
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
    requires_roots:
      - cli_root
      - server_root
    resolved_targets:
      - developer CLI source
      - containers CLI source
      - port-forward CLI source
  related_skills:
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before using CLI or server source references.
    - skill: meshagent-service-operator
      when: The fix belongs in service definition or room service lifecycle rather than runtime debugging.
    - skill: meshagent-webapp-builder
      when: The remaining issue is public web behavior rather than container state.
  scope:
    owns:
      - live runtime inspection
      - developer watch and container operations
      - local-to-container port forwarding
    excludes:
      - full service-template authoring
      - non-runtime queue, memory, database, or storage workflows
---

# MeshAgent Runtime Operator

Use this skill when the task is about the live runtime state inside a room rather than declarative YAML authoring.

## Use this skill when

- The user wants to inspect running containers in a room.
- The task involves `meshagent room developer watch`, `meshagent room container ...`, or `meshagent port forward`.
- The user needs container logs, container exec access, temporary container runs, image operations, or port forwarding for debugging.
- The workflow needs runtime diagnosis of a deployed service, worker, or website.

## References

- Use `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact command shapes.
- Inspect the resolved developer CLI source for log-streaming behavior.
- Inspect the resolved containers CLI source for container and image operations.
- Inspect the resolved port CLI source for local-to-container port forwarding.

## Related skills

- `meshagent-sdk-researcher`: Resolve checkout roots before using CLI or server source references.
- `meshagent-service-operator`: Use it when the main task is changing a service definition or room service record rather than debugging the live runtime.
- `meshagent-webapp-builder`: Use it when runtime checks pass but the remaining issue is public site behavior.

## Default workflow

1. Resolve the room and identify the runtime target: service, container, port, or log stream.
2. Start with read-only inspection: developer logs, container list, container logs, or port-forward target discovery.
3. Use `exec`, `run`, or image operations only after you understand the live state.
4. If local inspection is needed, use port forwarding with an explicit target container and port mapping.
5. Verify that the runtime symptom changed after any intervention.

## Runtime rules

- Prefer `meshagent room developer watch` for room-wide developer telemetry and `meshagent room container log` for one container’s logs.
- Prefer `container list` before `log`, `exec`, `stop`, or `port forward` so you target the right container.
- Treat `container stop` as disruptive.
- Treat `container exec` as a live-room debugging operation, not a substitute for fixing the service definition.
- Use image build/pull/push/load/save only when the runtime problem or deployment workflow actually requires image operations.

## Verification rules

- Do not conclude that the runtime is healthy based only on service metadata.
- Use logs, running container state, and port-forwarded behavior to confirm what is actually happening.
- If a container-local check passes but the public behavior is still broken, hand off to the appropriate website or route skill rather than stopping at the runtime layer.
- If a runtime issue persists after restart or stop/start behavior, inspect the declarative service definition before repeating the same action.

## Out of scope

- Full service-template authoring.
- Queue, memory, database, or storage workflows except where needed to debug the runtime symptom.
