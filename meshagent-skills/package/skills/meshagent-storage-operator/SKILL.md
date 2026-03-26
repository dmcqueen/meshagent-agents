---
name: meshagent-storage-operator
description: Operate MeshAgent room storage. Use this skill for checking existence, copying files between local disk and room storage, reading files, listing paths, and removing room-storage content safely.
metadata:
  short-description: Operate room storage paths and file transfers safely.
  references:
    bundled:
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - docs_root
      - cli_root
      - api_root
    resolved_targets:
      - room storage docs
      - shared live-room CLI context rules
      - storage CLI source
      - room storage API examples
  related_skills:
    - skill: meshagent-workflow-orchestrator
      when: Storage work is only one part of a larger end-to-end workflow.
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before using docs or source references.
    - skill: meshagent-participant-token-operator
      when: The real issue is whether the runtime or service has a participant token and storage API scope rather than storage path behavior.
    - skill: meshagent-webapp-builder
      when: Storage is one part of a website deploy workflow.
    - skill: meshagent-runtime-operator
      when: The real issue is a mount or live runtime visibility problem.
  scope:
    owns:
      - room storage listing and inspection
      - local-to-room and room-to-local copies
      - safe removal and path verification
    excludes:
      - website deployment by itself
      - general runtime debugging
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

# MeshAgent Storage Operator

Use this skill when the task is about room storage paths or copying data into or out of a room.

## Use this skill when

- The user wants to inspect files under room storage.
- The task involves `meshagent room storage exists`, `cp`, `show`, `rm`, or `ls`.
- The workflow needs to copy local assets into a room or retrieve room-owned output locally.
- Another skill depends on `/data` or room-visible files and the main blocker is storage manipulation.

## References

- Use `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact `meshagent room storage ...` command shapes.
- Use `../_shared/references/live_room_cli_context.md` when the storage workflow runs in or targets a known live room.
- Use the resolved room storage docs for the storage model.
- Inspect the resolved storage CLI source for the actual path parsing and copy behavior.

## Related skills

- `meshagent-workflow-orchestrator`: Use it when storage work is only one part of a larger end-to-end workflow.
- `meshagent-sdk-researcher`: Resolve checkout roots before using docs or source references.
- `meshagent-participant-token-operator`: Use it when the blocker is participant-token source, missing storage API grants, or token wiring rather than storage path behavior.
- `meshagent-webapp-builder`: Use it when storage is only one part of deploying a website.
- `meshagent-runtime-operator`: Use it when the real issue is a live container mount or runtime visibility problem rather than storage commands themselves.

## Default workflow

1. Resolve whether the source and destination are local paths or room paths.
2. Prefer `exists`, `ls`, or `show` before mutating storage.
3. Use `cp` for transfers between local disk and room storage.
4. Use `show` for content inspection and `ls` for structure inspection.
5. Treat `rm` as destructive and verify the exact target path first.

## Live room execution

- Apply `../_shared/references/live_room_cli_context.md` when the room is already known from runtime context or the user's request.
- Do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as prerequisite checks for room-scoped storage work.
- If permissions are uncertain, start with `exists`, `ls`, or `show` against the concrete room path before claiming the storage surface is unavailable.

## Path rules

- Distinguish local paths from room paths explicitly.
- Use room-visible paths that match the workflow, typically under `/data` inside room-mounted services.
- If the user asks to create or write a room file without specifying a concrete room path, default to `/data/<filename>` rather than `.` or another current-working-directory path.
- Do not confuse deployable local source trees with room-owned runtime storage.
- When another skill depends on a room file, verify the exact path instead of assuming the file is mounted where you expect.

## Verification rules

- Do not claim a file is available in room storage until `exists`, `ls`, or `show` confirms it.
- After `cp`, verify the destination path rather than assuming the transfer succeeded.
- After `rm`, verify that the path is actually gone.
- If a file is present in room storage but not visible in a running container, treat that as a runtime or mount issue and hand off appropriately.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return storage-path evidence and observed state to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- Website deployment flow by itself.
- General runtime debugging inside containers.
