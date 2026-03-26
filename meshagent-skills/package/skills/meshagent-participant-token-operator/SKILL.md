---
name: meshagent-participant-token-operator
description: Resolve, explain, mint, and verify MeshAgent participant tokens. Use this skill when the task is about where a room token comes from, how `MESHAGENT_TOKEN` behaves in a live room or service, how token-backed service environment variables work, how `--delegate-shell-token` populates shell env, or how API keys sign participant tokens.
metadata:
  short-description: Resolve and reason about participant tokens across runtimes, services, and shell delegation.
  references:
    bundled:
      - ../meshagent-cli-operator/references/command_groups.md
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - cli_root
      - docs_root
      - server_root
    resolved_targets:
      - participant token docs and implementation
      - RoomClient token initialization path
      - worker and mailbot delegate-shell-token behavior
      - service spec token-backed environment model
  related_skills:
    - skill: meshagent-workflow-orchestrator
      when: Token handling is one part of a larger end-to-end workflow.
    - skill: meshagent-cli-operator
      when: The remaining question is exact CLI command shape rather than token semantics.
    - skill: meshagent-service-operator
      when: The main task is fixing a service manifest or deployment lifecycle.
    - skill: meshagent-runtime-operator
      when: The question is whether a live runtime or shell actually received the token.
    - skill: meshagent-mail-operator
      when: The token question is specifically about room SMTP defaults or coded Python email sending.
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before using docs or source references.
  scope:
    owns:
      - participant token source discovery
      - service token-backed environment guidance
      - delegated shell token behavior
      - API-key-signed participant token guidance
    excludes:
      - generic service lifecycle without token-specific questions
      - non-token queue, storage, database, or web workflows
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

# MeshAgent Participant Token Operator

Use this skill when the task is about where a MeshAgent participant token comes from, how it is injected, how it is delegated into shells, or how it is minted and signed.

## Use this skill when

- The user asks where `MESHAGENT_TOKEN` comes from in a room, service, or local runtime.
- The task is about whether an environment variable contains a participant token or some other credential.
- The task involves token-backed `container.environment` entries in a `Service` or `ServiceTemplate`.
- The user needs to understand or verify `--delegate-shell-token`.
- The user needs to mint a participant token from an API key with `meshagent token generate` or SDK code.
- The user needs to distinguish API keys from participant tokens.

## References

- Use `../meshagent-cli-operator/references/command_groups.md` and `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact `meshagent token ...`, `api-key ...`, and join-command shapes.
- Use `../_shared/references/live_room_cli_context.md` when the token question is inside a known live room or room-scoped runtime.
- After root resolution, inspect the participant token implementation, RoomClient initialization path, service-spec token model, and worker/mailbot CLI token handling.

## Related skills

- `meshagent-workflow-orchestrator`: Use it when token handling is only one surface in a larger workflow.
- `meshagent-cli-operator`: Use it when the remaining problem is exact command composition.
- `meshagent-service-operator`: Use it when the fix belongs in a service manifest or service deployment flow.
- `meshagent-runtime-operator`: Use it when the question is whether a live runtime or shell actually received the token.
- `meshagent-mail-operator`: Use it when the token question is specifically about room SMTP defaults or coded Python email sending.
- `meshagent-sdk-researcher`: Resolve checkout roots before using docs or source references.

## Default workflow

1. Identify which token surface the user means: live room runtime, service manifest, delegated shell, minted JWT, or API key.
2. Prefer the narrowest source of truth for that surface: runtime env, service YAML, join-command flags, or token-generation code.
3. Distinguish participant tokens from API keys before suggesting any fix.
4. If a runtime already has a valid participant token, prefer reusing it over minting a new one.
5. If a service or shell path depends on a token in the environment, verify both the injection path and the environment variable name the process actually reads.
6. If the task is about minting a token, verify the signer source and grants rather than treating any JWT-like string as interchangeable.

## Token model

- A participant token is a JWT that identifies a participant and grants room, role, and API permissions.
- `room.protocol.token` on a live `RoomClient` is that client's participant token.
- `MESHAGENT_TOKEN` is a common convention for carrying a participant token, but it is not the only possible environment variable name.
- An API key is not a participant token. An API key is a project-scoped administrative credential that can be used to sign or mint participant tokens.

## Live room and runtime rules

- In a MeshAgent-launched room runtime, if `MESHAGENT_TOKEN` is present, treat it as the participant token for that runtime.
- `RoomClient()` auto-initializes from `MESHAGENT_ROOM` and `MESHAGENT_TOKEN` when no explicit protocol is provided.
- If code already has a live `RoomClient`, prefer `room.protocol.token` as the direct token source rather than re-reading unrelated auth state.
- Do not use `meshagent auth whoami` to decide whether a live room runtime already has a usable participant token.
- If the runtime reads a different env var for its token, that can still be valid; verify the code path instead of assuming `MESHAGENT_TOKEN` is mandatory.

## Service manifest rules

- In `container.environment`, any environment variable can request a participant token with a `token:` object.
- `MESHAGENT_TOKEN` is the common default env var name because many SDK and CLI runtimes look there automatically.
- The env var name is still arbitrary at the manifest layer. If the process expects `ROOM_TOKEN`, `MY_AGENT_TOKEN`, or another name, a token-backed entry on that name is valid too.
- Before deploying a service that needs room access, ensure the manifest includes a valid token-backed environment entry that the process actually reads.
- If the service process expects `MESHAGENT_TOKEN` specifically, ensure that exact env var is present before deployment.
- If the service process uses `RoomClient()` default initialization, it needs both `MESHAGENT_ROOM` and `MESHAGENT_TOKEN`, or an explicit protocol/token wiring path.

## Delegate-shell-token rules

- `--delegate-shell-token` copies the current room participant token into the shell-tool environment.
- In current CLI join paths, that delegated token is copied into:
  - `MESHAGENT_TOKEN`
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`
- This is a shell-tool convenience path, not a general service-manifest injection mechanism.
- If a shell command needs the room participant token and the agent was started with `--delegate-shell-token`, prefer the delegated shell environment over minting a fresh token.

## Minting and signing rules

- Use `meshagent token generate` or SDK `ParticipantToken(...).to_jwt(api_key=...)` when the task is to mint a participant token explicitly.
- Participant tokens are signed with a project API key.
- Project API keys are created in MeshAgent Studio or with `meshagent api-key create`.
- Treat API keys as developer/admin-side credentials for backend services, automation, and token minting. Do not treat them as room participant tokens.
- When a task already runs inside a room with a valid participant token, do not switch to an API-key signing flow unless the user explicitly needs a newly minted token.

## Verification rules

- Do not claim a runtime has a participant token until you identify the concrete source: runtime env, `room.protocol.token`, manifest token injection, or explicit minted JWT.
- Do not claim a service manifest is token-ready until the token-backed environment entry and the process's expected env-var name both match.
- Do not confuse a delegated shell token with a service-level environment token. They come from different paths and can fail independently.
- Do not ask for an API key if a valid in-room participant token already solves the user's problem.
- If minting fails, report whether the blocker is missing API key, missing room grant, missing API scope, or wrong env-var wiring.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily about participant-token source, injection, or minting behavior.
- If another skill already owns the workflow, return token-source evidence and exact blockers to that owner instead of declaring the whole job complete.
- If this skill hands off to another skill, keep accountability for the original token question until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.
