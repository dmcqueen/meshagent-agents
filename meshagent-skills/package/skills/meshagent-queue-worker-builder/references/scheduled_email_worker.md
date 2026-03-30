# Scheduled Email Queue Agent

Use this reference when the user asks for a queue-consuming agent that receives a queue message and sends an email, especially when that runtime will later be triggered by a one-time scheduled task.

## Required sequence

1. Determine whether the user wants a real delivered test email now or only a generic payload-driven worker template.
2. If the workflow is supposed to send a real email, collect the recipient email address before treating the workflow as ready for smoke testing or scheduling.
3. If subject or body were not provided, either ask for them together with the recipient or use clearly stated defaults when the user has not asked for custom content.
4. If the room is already known from runtime context or from the user's request, start with room-scoped probes. Do not use broad auth or room-listing commands as the gatekeeper for whether the workflow can proceed.
5. In a known live room, do not run `meshagent auth whoami` as a prerequisite check for this workflow.
6. Inspect or provision the mailbox first.
7. If the workflow clearly needs real outbound email and no reusable mailbox exists yet, create one automatically as part of the workflow instead of asking the user whether mailbox creation is allowed.
8. Reuse the mailbox email address as the sender identity.
9. Prefer mailbox addresses under the environment-appropriate managed mail domain. Do not default to `@meshagent.local` for outbound scheduled email workflows.
10. Choose and prove one mail path before treating the workflow as viable:
   - the default pattern is one process runtime with both `--channel=queue:<QUEUE_NAME>` and `--channel=mail:<MAILBOX_ADDRESS>`
   - use external toolkit `email` publication only when that live publisher was already proven in the room and reusing it is intentional
11. For a new mailbox-backed mail path, route the mailbox to its own email address as the queue and let the mail runtime consume that same queue.
12. Do not invent a different mailbox queue or inbox queue name for a new mailbox-backed workflow.
13. If an existing room already uses different mailbox and inbox queue names, treat that as an explicit exception that must be verified before preserving it.
14. Choose the queue-consumer and mail-runtime image family from the actual MeshAgent environment. Do not copy one environment profile's docs image into a different environment without checking the environment first.
15. Generate the initial service asset from the real CLI when possible:
   - for new authored YAML, use `meshagent process spec`
   - use `meshagent worker spec` or `meshagent mailbot spec` only when the user explicitly wants that split runtime shape
   - use `meshagent service spec` only when the narrower agent-specific spec commands are not the right fit
16. Build or update a process service that consumes the intended queue with `--channel=queue:<QUEUE_NAME>` and, for new authored scheduled-email services, also includes `--channel=mail:<MAILBOX_ADDRESS>` on the same runtime.
17. Use a queue-only process that depends on external toolkit `email` publication only when that live publisher was already proven in the room and reusing it is intentional.
18. For non-trivial scheduled email behavior, prefer mounted or startup-generated rule files and pass them with `--room-rules` instead of relying only on a long inline rule string.
19. For new scheduled email workflows, prefer one process runtime with queue and mail channels. Use separate mail and Worker services only when the user explicitly asked for that split shape.
20. For non-trivial scheduled email workflows, follow the same behavioral pattern as the `industry-report` nightly-report flow, adapted to a process design:
   - the queue channel triggers a named workflow through durable rule files
   - the scheduled task prompt tells the agent to run that workflow
   - the mail channel or equivalent publisher is part of the same designed mail path
21. For the service YAML, validate the actual command flags and role composition. A process agent should use `meshagent process join` plus real `--channel=...` flags; the mail path must not be treated as the scheduled job consumer.
22. Reject a queue-only process plus `--require-toolkit=email` as incomplete by default for new scheduled-email services.
23. Validate the YAML or rendered service before deployment.
24. If validation fails, inspect the exact validation error, repair the asset, and rerun validation before deploying.
25. Create or update the service.
26. Verify the live room service appears in `meshagent room service list`.
27. Verify the runtime is actually alive with room developer output, container state, or container logs.
28. Enqueue an immediate test message now, before creating the scheduled task.
29. Confirm the queue item was consumed and inspect logs for email-send success or failure.
30. Design the scheduled payload so it explicitly requests email sending in the same style the queue consumer already expects:
   - prompt-style when the runtime rules define a named workflow to run
   - structured fields when the runtime rules already key off `to`, `subject`, `body`, and any required action field
31. Only after the immediate smoke test passes should you create the one-time scheduled task.
32. Before creating the scheduled task, preflight scheduled-task access with `meshagent scheduled-task list --room <ROOM_NAME>` so you know whether scheduler permissions and visibility are actually available for the target room.
33. Before creating the scheduled task, check whether an equivalent near-future one-time task already exists for the same queue and payload so you do not create duplicates after an uncertain retry.
34. Do not pass a custom scheduled-task id unless it is already a real UUID. Otherwise omit `--id` and let the server generate it.
35. Before creating the scheduled task, make sure the requesting user's timezone is known from user-specific context or from direct user confirmation.
36. If the user asked for a relative time such as "one minute from now," calculate that relative time from the moment you are actually ready to run the scheduled-task create command, not from the start of the larger setup workflow.
37. Right before the create command, recompute the final absolute time and make sure it is still safely in the future instead of effectively at or before the current minute.
38. After creation, verify that the stored cron or UI-visible GMT schedule matches the computed UTC time rather than the user's local wall-clock time.

## Success criteria

Do not call the workflow complete until all of the following are true:

- the mailbox exists and its address is the sender identity used by the workflow
- the chosen mail path is proven:
  - either the runtime includes its own `mail:` channel and the live send path works
  - or the runtime intentionally depends on external toolkit `email` publication and that publisher is visibly present
- the recipient email address for the real smoke test and scheduled message is known, unless the user explicitly asked for a payload-only template
- the queue-consuming service exists in the room
- a live runtime or container is visibly running
- an immediate test message is consumed from the queue
- runtime evidence shows the mail send succeeded or shows the exact blocker
- the scheduled payload explicitly maps to the Worker's email-sending behavior rather than relying on an implied side effect
- the scheduled time was computed from the requesting user's known timezone, not just the room or server timezone
- the stored cron or UI-visible GMT schedule matches that computed UTC time rather than repeating the user's local clock fields
- scheduler preflight showed that scheduled-task create and verification were actually available in this environment
- the scheduled task is set for a future absolute time with enough safety margin to avoid already being in the past

## Failure interpretation

- A created mailbox does not prove outbound mail works.
- A created mailbox does not create toolkit `email`. Prove toolkit `email` publication only when the queue consumer actually depends on external `--require-toolkit=email`.
- A queue-only process that requires toolkit `email` but has no already-proven live email publisher is not a complete scheduled-email design.
- A process runtime with its own `mail:` channel should be verified through its live mail-send path, not by insisting on a separate external `email` publisher.
- A mailbox-backed mail runtime can misbehave if the mailbox address, mailbox queue, and inbox queue do not line up. For new workflows, those names should be the same. Any existing override must be treated as an exception that needs explicit verification.
- A mailbox address under `@meshagent.local` is a bad default for outbound managed-mail workflows. In managed environments, first suspect the mailbox domain if SMTP rejects send with authorization errors such as `550 5.7.1`.
- A created service record does not prove the queue-consuming runtime is running.
- A copied docs image does not prove the runtime image matches the current MeshAgent environment. One environment profile may need a different runtime image family than the docs examples for another profile.
- A mail runtime by itself does not satisfy a scheduled email workflow. The mail path publishes or owns the sender identity; the queue-consuming runtime must handle the scheduled job queue.
- A manifest that declares multiple roles but starts only one runtime path is incorrect even if the YAML shape validates.
- A new scheduled email workflow should not default to separate mail and Worker YAMLs when one process design would express the queue-plus-mail behavior more directly.
- A queue-consuming runtime command that uses unsupported or mismatched flags is invalid YAML content even if the surrounding service shape looks correct.
- A mailbox-looking sender such as `something@meshagent.local` is not a proven mailbox-backed sender identity.
- A scheduled task payload that does not explicitly request email sending may enqueue successfully while never causing an email to be sent.
- A scheduled task payload that uses structured fields can still fail if the process or dedicated Worker runtime was only taught to react to prompt-style instructions from its rules file or room-rules. Match the payload to the actual runtime design.
- For non-trivial scheduled email workflows, a prompt that triggers the durable queue-handling workflow is often more reliable than ad hoc `to`/`subject`/`body` JSON fields.
- If the user asked for a real scheduled email and no recipient address has been collected yet, the workflow is still blocked on required user input. Do not pretend the remaining setup is complete.
- A queue size of `0` after the scheduled time does not prove success; it may also mean the job never enqueued or failed after dequeue.
- A consumed smoke-test queue message does not prove email delivery by itself. Delivery still needs runtime send evidence or an exact mail blocker.
- If the scheduled time is too close and setup is still incomplete, push the one-time run farther into the future instead of pretending the near-term run is still valid.
- If the user asked for a relative run time and setup consumed part of that window, recompute the relative schedule from the current moment before creating the scheduled task.
- If the stored cron shows the user's local hour or minute inside a GMT-scheduled task, the schedule was created incorrectly even if the task record exists.
- If the requesting user's timezone is unknown, do not schedule yet. First determine it from reliable user-specific context or ask the user directly.
- If broad auth or room-listing commands fail but a narrower room-scoped workflow is still possible, continue with the room-scoped path instead of stopping early.
- In a known live room, `meshagent auth whoami` failing or reporting "Not logged in" does not by itself block this workflow. Use a room-scoped probe instead.
- If `meshagent scheduled-task list` or `meshagent scheduled-task add` fails with `403` or unexpected `5xx`, treat the scheduler as blocked or unhealthy and do not claim the end-to-end scheduled workflow is complete.
- If `meshagent scheduled-task add` fails after passing a human-readable `--id`, suspect invalid task-id format first. Scheduled-task ids are UUID-backed; omit `--id` or pass a real UUID.
- If an unfiltered project-wide `meshagent scheduled-task list` fails with `403`, do not assume the room-scoped create path is blocked. Retry with `--room <ROOM_NAME>` before concluding that scheduling is unavailable for the target room.
- If the scheduler is blocked or unhealthy, do not silently continue as if only the queue consumer matters.
- If a one-time `scheduled-task add` was retried after an uncertain first result, first inspect for an already-created equivalent task before issuing a second add.
- Two near-future tasks with the same queue, same payload intent, and same delivery window are usually a duplicate-creation bug, not a valid success case.

## Input collection rules

- When the user asked for a worker that actually sends an email, treat the recipient address as required input unless it is already present in the request or in a clearly reusable existing workflow.
- Do not treat sender-address selection as required user input for a straightforward room scheduled-email workflow when the skill can safely provision a mailbox-backed sender itself.
- Ask for all obviously blocking user-provided mail inputs in one message when possible: recipient first, then optional subject/body if needed.
- Do not ask a generic "should I continue?" question when the real blocker is a specific missing input such as the recipient address.
- If the user's original request already implies full setup plus scheduling, do not ask them to confirm ordinary prerequisite setup separately.
- If the user says "yes" or otherwise confirms they want the workflow completed, continue the build and verification flow without making them repeat the high-level request.
- If the user did not provide subject or body, you may continue with explicit defaults once the recipient is known, but say what defaults you are using.

## Payload examples

- Prompt-style payload example:
  - `{"prompt":"Send an email to recipient@example.com using the email toolkit. Subject: Scheduled test. Body: This is a scheduled test email."}`
- Prompt-style workflow-trigger example:
  - `{"prompt":"Run the scheduled email workflow and send the email using the email toolkit to recipient@example.com. Subject: Scheduled test. Body: This is a scheduled test email."}`
- Rule-file workflow-trigger example:
  - `{"prompt":"Run the nightly report workflow from /data/agents/<AGENT_NAME>/rules-worker-report.txt and send the email using the email toolkit."}`
- Structured payload example:
  - `{"to":"recipient@example.com","subject":"Scheduled test","body":"This is a scheduled test email.","action":"send_email"}`
- Match the payload style to the queue consumer's rules. If the runtime was built around prompt-driven instructions or a named room-rules workflow, keep using a prompt. If it was built around structured fields, use those exact fields.
