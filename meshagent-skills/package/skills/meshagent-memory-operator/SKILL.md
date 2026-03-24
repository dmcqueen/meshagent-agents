---
name: meshagent-memory-operator
description: Operate MeshAgent room memory stores. Use this skill for memory creation, inspection, query, ingestion, recall, entity and relationship updates, and optimization.
metadata:
  short-description: Operate room memory stores for recall, ingestion, and graph-style queries.
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
      - room memory docs
      - shared live-room CLI context rules
      - memory CLI source
      - room memory API examples
  related_skills:
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before using docs or source references.
    - skill: meshagent-database-operator
      when: The task is actually about structured tables and SQL/search rather than memory recall.
    - skill: meshagent-storage-operator
      when: The blocker is preparing files or room paths for ingestion.
  scope:
    owns:
      - room memory store creation and inspection
      - memory query, recall, and ingestion flows
      - entity and relationship updates
    excludes:
      - database table design
      - general SDK research outside memory workflows
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

# MeshAgent Memory Operator

Use this skill when the task is about the room memory API rather than the room database.

## Use this skill when

- The user wants to create, inspect, query, or delete a room memory store.
- The task involves `meshagent room memory ...` commands.
- The workflow needs ingesting text, images, files, storage paths, or table rows into memory.
- The user wants to recall entities and relationships from memory rather than query a plain database table.

## References

- Use `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact `meshagent room memory ...` command shapes.
- Use `../_shared/references/live_room_cli_context.md` when the memory workflow runs in or targets a known live room.
- Use the resolved room memory docs for the conceptual memory model and examples.
- Inspect the resolved memory CLI source for the real command surface and payload formats.

## Related skills

- `meshagent-sdk-researcher`: Resolve checkout roots before using docs, examples, or source references.
- `meshagent-database-operator`: Use it when the task is really about structured room tables rather than memory graphs and recall workflows.
- `meshagent-storage-operator`: Use it when the main job is preparing files or storage paths for ingestion.

## Default workflow

1. Resolve the room, namespace, and memory name.
2. Inspect existing memory stores before creating or dropping anything.
3. Choose the narrowest operation: `create`, `inspect`, `query`, `recall`, `upsert-*`, `ingest-*`, `delete-*`, or `optimize`.
4. If the workflow depends on imported data, verify the source text, file, storage path, or table before ingestion.
5. After mutation or ingestion, verify with `inspect`, `query`, or `recall`.

## Live room execution

- Apply `../_shared/references/live_room_cli_context.md` when the room is already known from runtime context or the user's request.
- Do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as prerequisite checks for room-scoped memory work.
- If permissions are uncertain, start with a room-scoped read path such as store listing, `inspect`, or `query` before claiming the memory surface is unavailable.

## Memory model rules

- Treat memory as a separate surface from the room database.
- Use `query` for SQL-like graph and dataset inspection.
- Use `recall` for semantic/entity retrieval workflows.
- Use `upsert-table`, `upsert-nodes`, and relationship commands when the structure is already known.
- Use `ingest-*` commands when the source is unstructured or semi-structured content.

## Verification rules

- Do not claim a memory ingestion worked until you inspect or query the resulting memory.
- Do not treat database-table existence as proof that memory ingestion succeeded.
- If recall results are poor, inspect the ingested memory shape before changing prompts or retrieval logic.
- Treat `drop`, entity deletion, and relationship deletion as destructive.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return memory-store evidence and observed state to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- Designing database tables or database indexes.
- General SDK research unrelated to memory workflows.
