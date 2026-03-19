---
name: meshagent-sdk-operator
description: Use the preloaded MeshAgent SDK checkout and bundled docs/examples to look up APIs and implementation patterns before writing code.
---

# MeshAgent SDK Operator

Use this skill when the task is mainly about how to use the MeshAgent SDK in code.

## Use this skill when

- The user wants an example of how to use a MeshAgent SDK API.
- The task involves writing code against the MeshAgent room APIs, toolkits, queues, storage, or related SDK surfaces.
- The user needs to check how the MeshAgent docs or examples implement a pattern before coding it.
- The user wants to inspect the SDK source to confirm an API shape instead of guessing.

## References

- In the live room image, the MeshAgent SDK checkout is preloaded at `/src/meshagent-sdk`.
- Start with `/src/meshagent-sdk/meshagent-docs` for documentation.
- Use `/src/meshagent-sdk/meshagent-docs/examples` when you need concrete implementation examples.
- Use `/src/meshagent-sdk/meshagent-docs/room_api` when the question is about room client APIs such as agents, queues, storage, messaging, database, or services.
- If the docs and examples are unclear, inspect the actual SDK source under `/src/meshagent-sdk`.

## Operating rules

- Prefer the preloaded docs, examples, and source over guessing API names or method signatures.
- Match the actual SDK that corresponds to the language being used.
- If the task is "how do we normally do this with MeshAgent?", search the preloaded docs/examples first.
- When an example exists, follow its structure before inventing a new integration pattern.
- Use the SDK source to confirm exact method names, argument shapes, and return types when the docs are ambiguous.

## Out of scope

- This skill does not replace CLI help for command flags.
- This skill does not define deployment workflow by itself.
