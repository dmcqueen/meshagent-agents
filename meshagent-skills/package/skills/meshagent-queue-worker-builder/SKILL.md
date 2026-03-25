---
name: meshagent-queue-worker-builder
description: Build or update MeshAgent room queue-backed agent YAML, defaulting to process services that dequeue tasks in a room and process scheduled or queued jobs.
metadata:
  short-description: Build queue-backed process agent and service YAML for room jobs.
  references:
    bundled:
      - references/scheduled_email_worker.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/process_agent_design.md
      - ../_shared/references/runtime_image_environment_rules.md
      - ../_shared/references/service_yaml_correctness.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - docs_root
      - examples_root
      - cli_root
    resolved_targets:
      - queue agent examples
      - shared live-room CLI context rules
      - shared process-agent design rules
      - shared runtime image environment rules
      - shared service YAML correctness rules
      - packaging docs
      - process and worker CLI source
  related_skills:
    - skill: meshagent-workflow-orchestrator
      when: The request spans queue-consumer build, mail, runtime proof, and scheduling as one end-to-end workflow.
    - skill: meshagent-sdk-researcher
      when: Resolve checkout roots before following example or source references.
    - skill: meshagent-participant-token-operator
      when: The remaining issue is token-backed environment wiring, delegated shell token behavior, or participant-token scope inside the queue consumer or mail runtime.
    - skill: meshagent-scheduler
      when: The remaining task is to create or verify a scheduled task after the queue consumer exists.
    - skill: meshagent-mail-operator
      when: The queued job sends email or depends on mailbox-backed sender identity.
    - skill: meshagent-service-operator
      when: The main task is service lifecycle rather than queue-consumer YAML authoring.
    - skill: meshagent-runtime-operator
      when: The YAML exists but the remaining work is proving that the live queue-consuming runtime actually dequeues and completes jobs.
  scope:
    owns:
      - queue-backed agent YAML authoring
      - queue and schedule alignment in agent definitions
      - queue-consuming service template adaptation from examples
    excludes:
      - scheduled-task CRUD
      - generic process-agent design across chat, mail, toolkit, and queue channels
      - low-level CLI command discovery
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

# MeshAgent Queue Worker Builder

Use this skill to create or repair queue-backed room service YAML. Default to a process agent with `--channel=queue:...`.

## Use this skill when

- The workflow needs a real queue consumer before scheduling or sending jobs.
- The task is to write or repair queue-related `meshagent.yaml`.
- The user needs a room service that dequeues payloads and completes work with storage, tools, or mail.

## References

- Start with the nearest working example:
  - `examples/cli/process-news-agent/meshagent.yaml` for a process agent with queue plus other channels
  - `meshagent-router/meshagent/router/templates/assistant.yaml` for a process room assistant service template
- Use `references/scheduled_email_worker.md` for queued email jobs.
- Use `../_shared/references/live_room_cli_context.md` for known live rooms.
- Use `../_shared/references/process_agent_design.md` for process channel design.
- Use `../_shared/references/runtime_image_environment_rules.md` for image selection.
- Use `../_shared/references/service_yaml_correctness.md` for validation and repair rules.

## Related skills

- `meshagent-workflow-orchestrator`: end-to-end queue, mail, runtime, and scheduling workflows
- `meshagent-sdk-researcher`: resolve roots and locate the best example
- `meshagent-participant-token-operator`: token-backed env and delegated shell token issues
- `meshagent-scheduler`: scheduled-task creation after the consumer is proven
- `meshagent-mail-operator`: mailbox-backed senders and email-toolkit publication
- `meshagent-service-operator`: service lifecycle after YAML authoring
- `meshagent-runtime-operator`: proving the live runtime dequeues and finishes jobs

## Core model

- New authored YAML should use `meshagent process`.
- Assume current rooms are not legacy unless the user or observed room state proves otherwise.
- The default queue runtime is `meshagent process join --channel=queue:<QUEUE_NAME>`.
- Treat the queue as one channel into the agent, not as a standalone workflow by itself.
- Use a dedicated `Worker` shape only when the user explicitly asks for it.
- If the queued job sends email, a mailbox alone is not enough.
- For new authored scheduled-email services, the default process shape is `meshagent process join --channel=queue:<QUEUE_NAME> --channel=mail:<MAILBOX_ADDRESS>`.
- Use a queue-only process plus `--require-toolkit=email` only when a live `email` publisher was already proven in the room and reusing it is intentional.

## Default workflow

1. Confirm whether this is new YAML, a template update, or an explicit request to modify an existing asset.
2. Resolve the closest working example before drafting.
3. In a known live room, use narrow room-scoped probes first. Do not start with broad auth or project checks.
4. Reuse real room names when possible: queue names, service names, sender identities, mounted paths.
5. If the queued job sends email, inspect or provision the mailbox first and reuse its real sender identity.
6. For new authored scheduled-email services, include the mailbox as a `mail:` channel on the same process service by default.
7. If the runtime instead depends on toolkit `email` from some other runtime, prove that live publisher exists before treating the YAML as viable.
8. Generate the base shape instead of freehanding YAML:
   - `meshagent process spec` for new queue-consuming services
   - `meshagent worker spec` only when the user explicitly wants a Worker runtime
   - `meshagent mailbot spec` only when the user explicitly wants a split mail runtime
   - `meshagent service spec` only when the narrower specs do not fit
9. Adapt the nearest example only after the generated shape is in hand.
10. Match the runtime image family to the actual MeshAgent environment.
11. Make the startup command show the real queue-consuming path:
   - scheduled email process: `meshagent process join --channel=queue:<QUEUE_NAME> --channel=mail:<MAILBOX_ADDRESS>`
   - queue-only process: `meshagent process join --channel=queue:<QUEUE_NAME>` only when a separate live email publisher is already proven
   - dedicated Worker: `meshagent worker join --queue=<QUEUE_NAME>`
12. If the workflow will be scheduled, keep the scheduled queue and consumer queue identical.
13. Validate the YAML structurally and semantically.
14. If validation fails, fix the exact error and rerun validation before deployment.
15. Hand off to service/runtime workflows to deploy and prove the live consumer.
16. Send an immediate smoke-test message and confirm dequeue plus job completion before treating the runtime as ready.
17. Only then hand off to the scheduler skill.

## Queue and payload rules

- Do not create a schedule for a queue that has no matching live consumer.
- A queue-looking annotation is not enough. The container command must show the actual queue-consuming path.
- Reuse an existing queue when it already represents the workflow; otherwise define one name and keep it consistent across sender, scheduler, and runtime.
- Smoke-test with the same payload style the scheduled run will use.
- If the runtime is rule-driven or prompt-driven, keep scheduled payloads thin and let the established rules do the work.
- If the runtime expects structured fields, the scheduled payload must use those exact fields.

## Scheduled email rules

- Use a real mailbox-backed sender from the room. Do not invent one.
- Do not assume mailbox creation publishes toolkit `email`.
- Do not treat a queue-only process plus `--require-toolkit=email` as complete scheduled-email design unless a live external email publisher was already proven.
- Do not point a standalone MailBot at the scheduled job queue and call that complete.
- Keep the mail path or equivalent toolkit publisher that makes `email` visible to the queue consumer.
- For new authored scheduled-email services, prefer one process with both queue and mail channels so the mail path is part of the service itself.
- For non-trivial email jobs, prefer durable `--room-rules` or mounted rules over inline ad hoc instructions.

## Verification rules

- YAML generation alone is not success.
- Service creation alone is not success.
- Success requires:
  - live room service evidence
  - live runtime evidence
  - successful immediate dequeue smoke test
- If the runtime requires toolkit `email`, verify that toolkit is visible before assuming the consumer is healthy.
- If the queued job sends email, do not call the workflow complete until runtime evidence shows a successful send or the exact blocker.
- If the smoke test fails, do not create the scheduled task yet.

## Operating rules

- Do not invent undocumented flags, annotations, or env vars.
- Prefer the smallest process example that fits the job.
- In a live room, do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as prerequisites.
- Do not copy a docs image blindly across environments.
- For dedicated Worker cases, use only supported flags. Do not invent flags like `--prompt`.
- If the user only asked to schedule an already running agent and no queue consumer exists, stop the scheduling path and switch to this skill.

## Workflow accountability

- This skill may own queue-consumer authoring when that is the main goal.
- If another skill owns the end-to-end workflow, return YAML, runtime, and smoke-test evidence to that owner.
- Follow `../_shared/references/workflow_accountability.md` for ownership, evidence, and forbidden shortcuts.

## Out of scope

- scheduled-task CRUD
- generic multi-channel process design beyond queue-centric authoring
- low-level CLI discovery
