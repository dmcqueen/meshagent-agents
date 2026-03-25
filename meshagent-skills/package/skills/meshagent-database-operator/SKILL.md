---
name: meshagent-database-operator
description: Manage the MeshAgent in-room database. Use this skill for table creation, schema inspection, row CRUD, search, SQL queries, indexes, versions, namespaces, and RequiredTable-based installation.
metadata:
  short-description: Operate the in-room database for schema, CRUD, search, SQL, and indexes.
  references:
    bundled:
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - docs_root
      - room_api_root
      - cli_root
      - api_root
      - server_root
    resolved_targets:
      - room database docs
      - shared live-room CLI context rules
      - database CLI source
      - Room API database client source
      - server database toolkit
      - room webserver database examples
      - agent database examples
  related_skills:
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before using docs, examples, or source references.
    - skill: meshagent-cli-operator
      when: The main blocker is command discovery or exact CLI syntax.
    - skill: meshagent-participant-token-operator
      when: The real issue is whether the current runtime or service has a participant token and database API scope rather than table semantics.
    - skill: meshagent-queue-worker-builder
      when: Database schema must be wired into agent or service YAML.
    - skill: meshagent-memory-operator
      when: The workflow is really about memory graphs or recall rather than tables.
  scope:
    owns:
      - room database table inspection and mutation
      - row CRUD and query-path choice
      - namespaces, indexes, optimize, and RequiredTable installation
    excludes:
      - memory-store workflows
      - full agent or service template authoring
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

# MeshAgent Database Operator

Use this skill when the task is to inspect, create, change, or query the MeshAgent room database.

## Use this skill when

- The user wants to create or inspect a room database table.
- The task involves inserting, updating, deleting, merging, or searching rows in the in-room database.
- The user wants to run SQL against one or more room database tables.
- The task involves indexes, table versions, namespaces, or `RequiredTable` installation.
- The user needs code or CLI examples for `room.database.*` behavior grounded in the actual MeshAgent implementation.

## References

- After root resolution, use the resolved room database docs for the API model and examples.
- Use `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact `meshagent room database ...` command shapes.
- Use `../_shared/references/live_room_cli_context.md` when the database workflow runs in or targets a known live room.
- Inspect the resolved database CLI source for the real CLI behavior, including schema parsing, JSON formats, and SQL/search options.
- Inspect the resolved Room API client source for `RequiredTable`, `SqlTableReference`, namespaces, and `DatabaseClient`.
- Inspect the resolved server database toolkit when you need the server-side toolkit operations or permission model.
- Use these resolved examples when the task is to write or debug room-database code:
  - `meshagent-docs/examples/python/webserver/contact_form_route.py` for a working form handler that creates a table and inserts a row with `room.database.create_table_with_schema(...)` and `room.database.insert(...)`.
  - `meshagent-docs/examples/python/webserver/contact_list_route.py` for a working read path that verifies writes with `room.database.search(...)`.
  - `meshagent-docs/examples/python/getting-started/agent-with-custom-tools/main.py` for the minimal `context.room.database.insert(table=..., records=[...])` pattern inside tool code.
  - `meshagent-api/meshagent/api/room_server_client.py` for the exact `create_table_with_schema`, `insert`, and `search` signatures.

## Related skills

- `meshagent-sdk-researcher`: Resolve checkout roots and turn conceptual codebase references into actual paths in the current environment.
- `meshagent-cli-operator`: Use it when the task is mainly about command selection, flags, or execution.
- `meshagent-participant-token-operator`: Use it when the blocker is participant-token source, missing room API grants, or token wiring rather than database behavior.
- `meshagent-queue-worker-builder`: Use it when database configuration must be added to `meshagent.yaml` or service YAML.
- `meshagent-memory-operator`: Use it when the task is about memory ingestion, recall, or graph-style data rather than tables.

## Live room execution

- Apply `../_shared/references/live_room_cli_context.md` when the room is already known from runtime context or the user's request.
- If this skill is running inside a live MeshAgent room workflow, first use the current room context instead of asking the user to reconnect.
- Resolve the active room and inspect the existing tables before creating or mutating anything.
- Do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as prerequisite checks for room-scoped database work.
- If permissions are uncertain, start with a read path such as table listing or schema inspection before claiming the database is unavailable.

## Default workflow

1. Resolve the active room, namespace, and target table names.
2. Inspect existing tables with `meshagent room database table` or `room.database.list_tables()`.
3. Inspect the current schema with `meshagent room database inspect` or `room.database.inspect()` before proposing mutations or queries.
4. Choose the narrowest operation: create, add columns, insert, merge, search, SQL, index management, or version restore.
5. If the table does not exist yet, create it from an explicit schema, explicit seed data, or a `RequiredTable` definition.
6. If the task is handler or agent code, prove the database call in isolation before mixing it with email sending, response rendering, or other handler changes.
7. Copy the proven repo call shape instead of inventing a CLI-backed write path inside the runtime.
8. Verify the result with a follow-up inspect/search/list command.

## Choosing the query path

- Prefer `search` for single-table lookups, filtering, text search, vector search, pagination, and column selection.
- Prefer `search --where-json` or `room.database.search(where={...})` for simple equality filters.
- Prefer `search --where` or `room.database.search(where=\"...\")` when the filter is more complex than equality-by-example.
- Prefer `sql` only when the user needs joins, aggregates, aliases, or more complex projections.
- For CLI SQL, register the tables explicitly with `--table` or `--tables-json`; SQL does not infer table context automatically.

## Table construction rules

- Do not invent columns or data types. Inspect the actual workflow requirements or an existing schema first.
- For form-style row capture, the grounded repo pattern is:
  - `await room.database.create_table_with_schema(name=..., schema={...}, mode="create_if_not_exists", data=None)`
  - then `await room.database.insert(table=..., records=[{...}])`
- For live handler work, keep the DB path modular:
  - one function or code block that validates and shapes the record
  - one function or code block that performs the DB write
  - a separate read-back or search step that proves the row exists
- For existing live handlers, prefer the fewest-line additive change that can prove the DB write path before attempting a larger refactor.
- For handler-side writes, prefer direct `room.database.*` calls over shelling out to `meshagent room database ...` from inside the handler runtime.
- Do not discover whether the DB call shape works by embedding a first attempt directly into a larger live handler patch that also changes mail or response logic.
- The CLI `--columns` path supports `int`, `bool`, `date`, `timestamp`, `float`, `text`, `binary`, `vector`, `list`, and `struct`.
- Use `--columns` for compact schemas, `--schema-json` or `--schema-file` for nested types, and `--data-json` or `--data-file` when creating from seed rows.
- If the workflow is defined as a reusable requirement, prefer a `RequiredTable` and the install path rather than retyping ad hoc create/index commands.
- When the schema already exists and only new fields are needed, prefer `add-columns` over dropping and recreating the table.

## Namespaces and registration

- Namespaces are real database scope segments. Reuse the actual namespace from the current room, agent, or service configuration instead of defaulting to root.
- If an agent or service already declares a database namespace, keep your CLI and SDK calls aligned with that namespace.
- When running SQL across namespaced tables, pass full `SqlTableReference` data when aliases or per-table namespaces matter.

## Indexes and optimization

- Add scalar indexes for exact-match/filter-heavy columns.
- Add full-text indexes before relying on text search.
- Add vector indexes before relying on vector similarity search.
- After major writes or required-table installation, use `optimize` when the workflow depends on query performance or freshly built indexes.

## Agent and service integration

- If the task is only about operating the room database, stay in this skill.
- If the task is to wire database schema into agent or service YAML, inspect `meshagent.agent.database.schema` usage in the repo and hand off YAML authoring to `meshagent-queue-worker-builder`.
- If the task is mainly about running CLI commands, combine with `meshagent-cli-operator`.
- If the task is mainly about writing SDK code or resolving implementation paths, combine with `meshagent-sdk-researcher`.

## Operating rules

- Do not assume an external database; this skill is for the MeshAgent room database.
- Do not claim a table exists until you list or inspect it.
- Do not describe handler-side room-database writes as speculative when the repo already has working `create_table_with_schema`, `insert`, and `search` patterns.
- Do not treat integrated handler success as the first proof that the DB write works. Prove insert plus read-back first, then integrate.
- Do not use SQL when `search` is enough.
- Do not use `search` for joins or aggregate reporting that clearly requires SQL.
- Do not invent namespace paths, index names, or schema annotations.
- Verify destructive operations like `drop`, `drop-columns`, `restore`, and bulk `delete` carefully before executing them.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return database evidence and observed state to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- This skill does not design a complete agent or service template by itself.
- This skill does not replace the memory API or memory-query workflows.
