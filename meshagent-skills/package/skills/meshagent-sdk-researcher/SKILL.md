---
name: meshagent-sdk-researcher
description: Use the preloaded MeshAgent SDK checkout and bundled docs/examples to research APIs and implementation patterns before writing code.
metadata:
  short-description: Resolve the MeshAgent checkout and research docs, examples, and source paths.
  references:
    resolved_targets:
      - sdk_root
      - docs_root
      - examples_root
      - room_api_root
      - cli_root
      - api_root
      - server_root
      - router_root
      - cloud_root
      - agents_root
  related_skills:
    - skill: meshagent-cli-operator
      when: The task is mainly about CLI flags or command execution rather than source-level research.
    - skill: meshagent-database-operator
      when: The problem has already narrowed to room database operations.
    - skill: meshagent-queue-worker-builder
      when: The research phase is done and the next step is authoring Worker YAML.
  scope:
    owns:
      - checkout root resolution
      - docs/example/source discovery
      - source-grounded API and pattern research
    excludes:
      - CLI flag discovery by itself
      - deployment workflow ownership
---

# MeshAgent SDK Researcher

Use this skill when the task is mainly about how to use the MeshAgent SDK in code.

## Use this skill when

- The user wants an example of how to use a MeshAgent SDK API.
- The task involves writing code against the MeshAgent room APIs, toolkits, queues, storage, or related SDK surfaces.
- The user needs to check how the MeshAgent docs or examples implement a pattern before coding it.
- The user wants to inspect the SDK source to confirm an API shape instead of guessing.

## References

- When this skill is available, treat it as the resolver for the MeshAgent codebase tree.
- In a live room image, the MeshAgent SDK checkout is commonly preloaded at `/src/meshagent-sdk`, but do not assume that path blindly in every environment.
- Resolve and expose these roots when available:
  - `sdk_root`: the MeshAgent checkout root
  - `docs_root`: the docs root, usually `<sdk_root>/meshagent-docs`
  - `examples_root`: the docs examples root, usually `<docs_root>/examples`
  - `room_api_root`: the room API docs root, usually `<docs_root>/room_api`
  - `cli_root`: the CLI source root, usually `<sdk_root>/meshagent-cli/meshagent/cli`
  - `api_root`: the SDK Room API source root, usually `<sdk_root>/meshagent-api/meshagent/api`
  - `server_root`: the server source root when it is available in the checkout
  - `router_root`, `cloud_root`, `agents_root`: other MeshAgent source roots when available
- Other skills in this bundle may refer to docs, examples, or source files conceptually. Use this skill first to turn those conceptual references into resolvable paths in the current environment.

## Related skills

- `meshagent-cli-operator`: Use it when the problem is mainly exact command paths, flags, or non-interactive execution.
- `meshagent-database-operator`: Use it after the research step when the task has narrowed to room database operations.
- `meshagent-queue-worker-builder`: Use it after the research step when the next job is authoring queue-backed Worker YAML.

## Operating rules

- Prefer the preloaded docs, examples, and source over guessing API names or method signatures.
- Resolve the codebase roots first before giving path-based guidance to another skill.
- Match the actual SDK that corresponds to the language being used.
- If the task is "how do we normally do this with MeshAgent?", search the preloaded docs/examples first.
- When an example exists, follow its structure before inventing a new integration pattern.
- Use the SDK source to confirm exact method names, argument shapes, and return types when the docs are ambiguous.
- If the expected checkout is not present, say that clearly and fall back to the best available docs or source tree instead of inventing paths.

## Out of scope

- This skill does not replace CLI help for command flags.
- This skill does not define deployment workflow by itself.
