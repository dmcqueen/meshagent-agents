# Scheduled Email Worker

Use this reference when the user asks for a Worker that receives a queue message and sends an email, especially when that Worker will later be triggered by a one-time scheduled task.

## Required sequence

1. Determine whether the user wants a real delivered test email now or only a generic payload-driven worker template.
2. If the workflow is supposed to send a real email, collect the recipient email address before treating the workflow as ready for smoke testing or scheduling.
3. If subject or body were not provided, either ask for them together with the recipient or use clearly stated defaults when the user has not asked for custom content.
4. If the room is already known from runtime context or from the user's request, start with room-scoped probes. Do not use broad auth or room-listing commands as the gatekeeper for whether the workflow can proceed.
5. In a known live room, do not run `meshagent auth whoami` as a prerequisite check for this workflow.
6. Inspect or provision the mailbox first.
7. If the workflow clearly needs real outbound email and no reusable mailbox exists yet, create one automatically as part of the workflow instead of asking the user whether mailbox creation is allowed.
8. Reuse the mailbox email address as the sender identity.
9. In `.life` rooms, prefer mailbox addresses under `@mail.meshagent.life`; in production `.com` environments, prefer `@mail.meshagent.com`. Do not default to `@meshagent.local` for outbound scheduled email workflows.
10. Verify that toolkit `email` is already published in the room or create the MailBot or equivalent service that will publish it. The normal pattern is a MailBot with `--toolkit-name=email`.
11. For a mailbox-backed MailBot, keep the mailbox address, mailbox queue, and MailBot inbox queue aligned by default. The safest pattern is to route the mailbox to its own email address as the queue and let the MailBot consume that same queue, unless you have explicit evidence that an override is intentional and correctly wired.
12. Choose the Worker and MailBot runtime image family from the actual MeshAgent environment. Do not copy a production docs image into a `.life` room without checking the environment first.
13. Generate the initial service asset from the real CLI when possible:
   - `meshagent worker spec` for a dedicated Worker
   - `meshagent mailbot spec` for a dedicated MailBot
   - `meshagent service spec` only when the narrower agent-specific spec commands are not the right fit
14. Build or update a queue-backed Worker service that consumes the intended queue and uses `--require-toolkit=email` only when the `email` toolkit publisher is real.
15. For non-trivial scheduled email behavior, prefer mounted or startup-generated Worker rule files and pass them with `--room-rules` instead of relying only on a long inline rule string.
16. Prefer separate MailBot and Worker services for new scheduled email workflows. Only preserve a combined process when you are repairing an existing deployment that already depends on it.
17. For non-trivial scheduled email workflows, follow the same behavioral pattern as the `industry-report` nightly-report Worker:
   - the Worker queue owns a named workflow through durable rule files
   - the scheduled task prompt tells the Worker to run that workflow
   - the MailBot exists only to publish toolkit `email`
18. For the service YAML, validate the actual command flags and role composition. A Worker must use real worker flags such as `--rule` or `--room-rules`; a MailBot must not be treated as the scheduled job consumer.
19. Validate the YAML or rendered service before deployment.
20. If validation fails, inspect the exact validation error, repair the asset, and rerun validation before deploying.
21. Create or update the service.
22. Verify the live room service appears in `meshagent room service list`.
23. Verify the runtime is actually alive with room developer output, container state, or container logs.
24. Enqueue an immediate test message now, before creating the scheduled task.
25. Confirm the queue item was consumed and inspect logs for email-send success or failure.
26. Design the scheduled payload so it explicitly requests email sending in the same style the Worker already expects:
   - prompt-style when the Worker rules define a named workflow to run
   - structured fields when the Worker rules already key off `to`, `subject`, `body`, and any required action field
27. Only after the immediate smoke test passes should you create the one-time scheduled task.
28. Before creating the scheduled task, preflight scheduled-task access with `meshagent scheduled-task list --room <ROOM_NAME>` so you know whether scheduler permissions and visibility are actually available for the target room.
29. Do not pass a custom scheduled-task id unless it is already a real UUID. Otherwise omit `--id` and let the server generate it.
30. Before creating the scheduled task, make sure the requesting user's timezone is known from user-specific context or from direct user confirmation.
31. If the user asked for a relative time such as "one minute from now," calculate that relative time from the moment you are actually ready to run the scheduled-task create command, not from the start of the larger setup workflow.
32. Right before the create command, recompute the final absolute time and make sure it is still safely in the future instead of effectively at or before the current minute.

## Success criteria

Do not call the workflow complete until all of the following are true:

- the mailbox exists and its address is the sender identity used by the workflow
- toolkit `email` is visibly published in the room by a MailBot or equivalent service
- the recipient email address for the real smoke test and scheduled message is known, unless the user explicitly asked for a payload-only template
- the Worker service exists in the room
- a live runtime or container is visibly running
- an immediate test message is consumed from the queue
- runtime evidence shows the mail send succeeded or shows the exact blocker
- the scheduled payload explicitly maps to the Worker's email-sending behavior rather than relying on an implied side effect
- the scheduled time was computed from the requesting user's known timezone, not just the room or server timezone
- scheduler preflight showed that scheduled-task create and verification were actually available in this environment
- the scheduled task is set for a future absolute time with enough safety margin to avoid already being in the past

## Failure interpretation

- A created mailbox does not prove outbound mail works.
- A created mailbox does not create toolkit `email`. If the Worker depends on `--require-toolkit=email`, prove that some live room participant publishes toolkit `email`.
- A mailbox-backed MailBot can misbehave if the mailbox address, mailbox queue, and MailBot inbox queue do not line up. The safest default is to keep those names the same, but code-level overrides are possible and must be checked explicitly.
- A mailbox address under `@meshagent.local` is a bad default for outbound managed-mail workflows. In `.life` or production environments, first suspect the mailbox domain if SMTP rejects send with authorization errors such as `550 5.7.1`.
- A created service record does not prove a Worker runtime is running.
- A copied docs image does not prove the runtime image matches the current MeshAgent environment. A `.life` room may need a different runtime image family than the production docs examples.
- A MailBot service by itself does not satisfy a scheduled email worker workflow. The MailBot publishes toolkit `email`; the Worker must consume the scheduled job queue.
- A manifest that declares both `MailBot` and `Worker` roles but starts only one runtime path is incorrect even if the YAML shape validates.
- A new scheduled email workflow should not default to a combined MailBot+Worker process when separate services would express the design more clearly.
- A worker command that uses unsupported flags such as `--prompt` is invalid YAML content even if the surrounding service shape looks correct.
- A mailbox-looking sender such as `something@meshagent.local` is not a proven mailbox-backed sender identity.
- A scheduled task payload that does not explicitly request email sending may enqueue successfully while never causing an email to be sent.
- A scheduled task payload that uses structured fields can still fail if the Worker was only taught to react to prompt-style instructions from its rules file or room-rules. Match the payload to the Worker design.
- For non-trivial scheduled email workflows, a prompt that triggers the durable Worker workflow is often more reliable than ad hoc `to`/`subject`/`body` JSON fields.
- If the user asked for a real scheduled email and no recipient address has been collected yet, the workflow is still blocked on required user input. Do not pretend the remaining setup is complete.
- A queue size of `0` after the scheduled time does not prove success; it may also mean the job never enqueued or failed after dequeue.
- A consumed smoke-test queue message does not prove email delivery by itself. Delivery still needs runtime send evidence or an exact mail blocker.
- If the scheduled time is too close and setup is still incomplete, push the one-time run farther into the future instead of pretending the near-term run is still valid.
- If the user asked for a relative run time and setup consumed part of that window, recompute the relative schedule from the current moment before creating the scheduled task.
- If the requesting user's timezone is unknown, do not schedule yet. First determine it from reliable user-specific context or ask the user directly.
- If broad auth or room-listing commands fail but a narrower room-scoped workflow is still possible, continue with the room-scoped path instead of stopping early.
- In a known live room, `meshagent auth whoami` failing or reporting "Not logged in" does not by itself block this workflow. Use a room-scoped probe instead.
- If `meshagent scheduled-task list` or `meshagent scheduled-task add` fails with `403` or unexpected `5xx`, treat the scheduler as blocked or unhealthy and do not claim the end-to-end scheduled workflow is complete.
- If `meshagent scheduled-task add` fails after passing a human-readable `--id`, suspect invalid task-id format first. Scheduled-task ids are UUID-backed; omit `--id` or pass a real UUID.
- If an unfiltered project-wide `meshagent scheduled-task list` fails with `403`, do not assume the room-scoped create path is blocked. Retry with `--room <ROOM_NAME>` before concluding that scheduling is unavailable for the target room.
- If the scheduler is blocked or unhealthy, do not silently continue as if only the Worker matters. Either stop or clearly mark Worker and MailBot creation as partial preparation pending scheduler recovery.

## Input collection rules

- When the user asked for a worker that actually sends an email, treat the recipient address as required input unless it is already present in the request or in a clearly reusable existing workflow.
- Do not treat sender-address selection as required user input for a straightforward room scheduled-email workflow when the skill can safely provision a mailbox-backed sender itself.
- Ask for all obviously blocking user-provided mail inputs in one message when possible: recipient first, then optional subject/body if needed.
- Do not ask a generic "should I continue?" question when the real blocker is a specific missing input such as the recipient address.
- If the user says "yes" or otherwise confirms they want the workflow completed, continue the build and verification flow without making them repeat the high-level request.
- If the user did not provide subject or body, you may continue with explicit defaults once the recipient is known, but say what defaults you are using.

## Payload examples

- Prompt-style payload example:
  - `{"prompt":"Send an email to david.mcqueen@timu.com using the email toolkit. Subject: Scheduled test. Body: This is a scheduled test email."}`
- Prompt-style workflow-trigger example:
  - `{"prompt":"Run the scheduled email workflow and send the email using the email toolkit to david.mcqueen@timu.com. Subject: Scheduled test. Body: This is a scheduled test email."}`
- Rule-file workflow-trigger example:
  - `{"prompt":"Run the nightly report workflow from /data/agents/<AGENT_NAME>/rules-worker-report.txt and send the email using the email toolkit."}`
- Structured payload example:
  - `{"to":"david.mcqueen@timu.com","subject":"Scheduled test","body":"This is a scheduled test email.","action":"send_email"}`
- Match the payload style to the Worker's rules. If the Worker was built around prompt-driven instructions or a named room-rules workflow, keep using a prompt. If it was built around structured fields, use those exact fields.
