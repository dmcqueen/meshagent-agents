---
name: meshagent-core
description: Bare-minimum routing and verification rules for live MeshAgent room work. Use this skill to reduce decision confusion before choosing a narrower specialist skill.
metadata:
  short-description: Minimal high-signal rules for live room work.
  references:
    bundled:
      - ../_shared/references/workflow_accountability.md
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

# MeshAgent Core

Use this skill for the smallest set of MeshAgent room rules that prevent obvious decision mistakes before deeper skill selection.

## Use this skill when

- The task touches the MeshAgent CLI, a live room, or anything running inside it.
- The user wants a real outcome, not just a command suggestion.
- The task spans multiple possible specialist areas and needs a minimal routing rule first.

## Highest-priority rules

- Do not guess implementation behavior. When exact behavior matters, inspect the code repo directly first.
- If `MESHAGENT_ROOM` is already known, prefer room-scoped commands over broad discovery.
- Prefer the narrowest command path that matches the task.
- Prefer inspection before mutation.
- After any mutation, verify on the matching read surface: `show`, `list`, logs, queue receive, live HTTP, or real delivery evidence.

## Workflow ownership

- Keep exactly one owner for the user-visible outcome.
- Supporting skills return evidence, not “done”.
- Do not stop at an internal actionable blocker if the normal next fix is still available.
- Do not say “done” until the user-visible result is verified or the exact blocker is proven.

## Real-surface verification

- Verify on the real surface, not on a precursor.
- Route creation is not a working site.
- Service creation is not runtime health.
- Queue growth is not email delivery.
- For public sites, require live HTTP verification.
- For contact forms, require GET plus representative POST verification.
- If public DNS or live HTTP is unproven, report partial state, not completion.

## Managed hostname rules

- Resolve the active environment from `MESHAGENT_API_URL`.
- Use only the environment-correct managed public suffix.
- Managed public hostnames and managed mailbox domains are different surfaces.
- Do not derive a public hostname from the mailbox domain, SMTP hostname, or API hostname.
- In `.life`, managed minisites are still `.meshagent.dev`.
- Treat wrong-suffix hostnames as hard errors and fix them first.

## Webapp rules

- Default production website hosting path: `meshagent image build --pack ... --deploy`.
- Add `--domain` only when the deployed image-backed service has exactly one published port.
- For active Python iteration, the preferred dev loop is `meshagent webserver join --watch`.
- Use room-storage source paths like `/<site-dir>`; in the live shell they appear under `/data/<site-dir>`.
- For live handler work, keep changes narrow and verify that the changed behavior is actually live.

## Mail rules

- Treat “send an email” as real outbound email by default.
- Mailbox creation, queue creation, or queue enqueue is not email delivery.
- Use the environment-correct managed mailbox domain for MeshAgent mailbox-backed senders.
- Do not invent sender identities or default `From == To` when `To` is the user’s external inbox.
- Treat `550`, `553`, and similar SMTP failures first as sender identity or authorization problems.

## Service/runtime rules

- Use generated specs over handwritten YAML whenever the CLI can generate the runtime shape.
- Validate YAML before deploy when a file is involved.
- Use runtime inspection for live state: service list, developer watch, container list/logs, toolkit visibility.
- Do not rely on repeated `container exec` into another private container.

## Queue/database/storage/scheduler rules

- Queue: prove real dequeue or processing, not just queue size movement.
- Database: inspect the real `room.database.*` implementation in the repo; do not invent schema or API forms.
- Storage: verify the exact room path before assuming files are present or deployed.
- Scheduler: a scheduled-task record alone is not workflow success.

## Code-grounding rules

- When exact API shape or implementation behavior matters, inspect the code repo directly before guessing.
- Prefer implementation over memory for CLI flags, token behavior, runtime env vars, API shapes, and mail/runtime behavior.
- If the code still does not answer the question clearly, report the uncertainty instead of inventing behavior.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily to choose the correct MeshAgent execution path and avoid cross-surface mistakes.
- If a narrower specialist skill is needed, transfer execution there and keep accountability until that skill returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.
