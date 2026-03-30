---
name: meshagent-webapp-dev-operator
description: Run and debug the development loop for MeshAgent room webapp backends. Use this skill for Python handler hot reload, preview-style room webserver iteration, and proving that live dev changes are actually taking effect.
metadata:
  short-description: Hot-reload dev loop for room-hosted webapp backends.
  references:
    bundled:
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../meshagent-webapp-backend-builder/references/dev_hot_reload_loop.sh
      - ../meshagent-webapp-backend-builder/references/verification_checklist.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/managed_hostname_rules.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - cli_root
      - server_root
    resolved_targets:
      - webserver CLI source
      - developer CLI source
      - shared live-room CLI context rules
      - shared managed-hostname rules
      - shared workflow accountability rules
  related_skills:
    - skill: meshagent-workflow-orchestrator
      when: The dev loop is one piece of a larger end-to-end workflow.
    - skill: meshagent-webapp-backend-builder
      when: The task also needs backend code changes, DB integration, or mail integration.
    - skill: meshagent-runtime-operator
      when: The remaining issue is container state, logs, or runtime visibility rather than the dev loop shape.
    - skill: meshagent-webapp-release-operator
      when: The task changes from development iteration to image-backed candidate or release work.
    - skill: meshagent-webmaster
      when: The main task is route administration or managed-hostname diagnostics rather than the dev loop itself.
  scope:
    owns:
      - Python handler hot-reload dev loops
      - preview-style room webserver iteration
      - proof that dev changes are actually live
    excludes:
      - image-backed candidate and release packaging
      - backend feature implementation by itself
      - generic route administration
  workflow:
    can_be_owner: true
    handoff_policy: retain_accountability_until_owner_transfer
    completion_gates:
      - mutation_target_confirmed_when_relevant
      - observed_state_matches_claim
      - user_visible_result_verified_or_exact_blocker_reported
    evidence:
      - exact_commands_or_artifacts_used
      - observed_room_or_runtime_state
      - user_visible_result_or_exact_blocker
---

# MeshAgent Webapp Dev Operator

Use this skill when the task is to iterate on a room-hosted webapp backend in development mode and the key question is whether code changes are actually taking effect in a hot-reload loop.

## Use this skill when

- The user is actively iterating on a Python handler and needs hot reload.
- The task is to keep a dev-only room webserver loop responsive while changing backend code.
- The current problem is that synced file edits do not seem to change live Python handler behavior.
- The user wants a preview or dev-only public URL without turning that runtime into a release artifact.

## References

- Use `../meshagent-webapp-backend-builder/references/dev_hot_reload_loop.sh` as the default live-room dev loop asset.
- Use `../meshagent-webapp-backend-builder/references/verification_checklist.md` for short HTTP verification after the loop is up.
- Use `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact command shapes.
- Use `../_shared/references/live_room_cli_context.md` for room context, path handling, and room-scoped command rules.
- Use `../_shared/references/managed_hostname_rules.md` if the dev loop also needs a managed public hostname.

## Related skills

- `meshagent-workflow-orchestrator`: dev iteration is only one part of a larger workflow
- `meshagent-webapp-backend-builder`: backend code shape, DB integration, mail integration, and handler implementation
- `meshagent-runtime-operator`: live container state, logs, or runtime visibility debugging
- `meshagent-webapp-release-operator`: release-candidate or release packaging
- `meshagent-webmaster`: route administration and hostname diagnostics

## Default workflow

1. Confirm that the task is `dev` mode rather than candidate or release work.
2. Inspect the current runtime and source-tree layout before changing the loop.
3. Prefer `meshagent webserver join --watch` for Python handler iteration.
4. Verify that the source path and the watched runtime path actually line up.
5. After changes, prove the new behavior with a visible marker or other direct evidence.

## Dev-loop rules

- `meshagent webserver join --watch` is the preferred Python handler dev loop.
- Do not treat `meshagent webserver deploy` as a hot-reload path for Python code.
- Use `../meshagent-webapp-backend-builder/references/dev_hot_reload_loop.sh` when the room source lives under room storage and the runtime should watch that source directly.
- Distinguish room-storage source paths such as `/<site-dir>` from shell-visible mount paths such as `/data/<site-dir>`.
- If a public dev URL is needed while preserving hot reload, prefer a separate dev-only runtime whose command explicitly runs `meshagent webserver join --watch` against room-mounted source.
- A dev preview runtime is not a release artifact and is not a rollback-ready candidate.
- If the task becomes image-backed candidate or release work, hand off to `meshagent-webapp-release-operator`.

## Verification rules

- Do not claim a Python handler change is live until a request proves the changed behavior, not just a file sync or deploy command.
- If a file-backed dev site keeps serving old Python behavior after file sync, treat that as a dev-loop/runtime-reload issue before debugging DB, mail, or routing.
- If the dev loop has a public URL, still verify the live page with a real HTTP GET and any relevant POST path.
- If the current managed hostname uses the wrong suffix for the active environment, stop and correct the hostname before treating the dev URL as meaningful evidence.
- If live HTTP reachability is still unproven, report the dev loop as incomplete rather than summarizing it as done.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return dev-loop evidence and observed state to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- Image-backed candidate and release packaging.
- Backend feature design or DB schema design by itself.
- Generic route administration.
