# Scheduled Email Worker

Use this reference when the user asks for a Worker that receives a queue message and sends an email, especially when that Worker will later be triggered by a one-time scheduled task.

## Required sequence

1. Determine whether the user wants a real delivered test email now or only a generic payload-driven worker template.
2. If the workflow is supposed to send a real email, collect the recipient email address before treating the workflow as ready for smoke testing or scheduling.
3. If subject or body were not provided, either ask for them together with the recipient or use clearly stated defaults when the user has not asked for custom content.
4. If the room is already known from runtime context or from the user's request, start with room-scoped probes. Do not use broad auth or room-listing commands as the gatekeeper for whether the workflow can proceed.
5. Inspect or provision the mailbox first.
6. Reuse the mailbox email address as the sender identity.
7. Verify that toolkit `email` is already published in the room or create the MailBot or equivalent service that will publish it. The normal pattern is a MailBot with `--toolkit-name=email`.
8. Build or update a queue-backed Worker service that consumes the intended queue and uses `--require-toolkit=email` only when the `email` toolkit publisher is real.
9. Validate the YAML or rendered service before deployment.
10. Create or update the service.
11. Verify the live room service appears in `meshagent room service list`.
12. Verify the runtime is actually alive with room developer output, container state, or container logs.
13. Enqueue an immediate test message now, before creating the scheduled task.
14. Confirm the queue item was consumed and inspect logs for email-send success or failure.
15. Design the scheduled payload so it explicitly requests email sending, either through a prompt like "send an email using the email toolkit" or through the exact structured fields the Worker rules require.
16. Only after the immediate smoke test passes should you create the one-time scheduled task.
17. Before creating the scheduled task, preflight scheduled-task access with `meshagent scheduled-task list --room <ROOM_NAME>` so you know whether scheduler permissions and visibility are actually available for the target room.
18. Before creating the scheduled task, make sure the requesting user's timezone is known from user-specific context or from direct user confirmation.
19. If the user asked for a relative time such as "one minute from now," calculate that relative time from the moment you are actually ready to run the scheduled-task create command, not from the start of the larger setup workflow.
20. Right before the create command, recompute the final absolute time and make sure it is still safely in the future instead of effectively at or before the current minute.

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
- A created service record does not prove a Worker runtime is running.
- A scheduled task payload that does not explicitly request email sending may enqueue successfully while never causing an email to be sent.
- If the user asked for a real scheduled email and no recipient address has been collected yet, the workflow is still blocked on required user input. Do not pretend the remaining setup is complete.
- A queue size of `0` after the scheduled time does not prove success; it may also mean the job never enqueued or failed after dequeue.
- A consumed smoke-test queue message does not prove email delivery by itself. Delivery still needs runtime send evidence or an exact mail blocker.
- If the scheduled time is too close and setup is still incomplete, push the one-time run farther into the future instead of pretending the near-term run is still valid.
- If the user asked for a relative run time and setup consumed part of that window, recompute the relative schedule from the current moment before creating the scheduled task.
- If the requesting user's timezone is unknown, do not schedule yet. First determine it from reliable user-specific context or ask the user directly.
- If broad auth or room-listing commands fail but a narrower room-scoped workflow is still possible, continue with the room-scoped path instead of stopping early.
- If `meshagent scheduled-task list` or `meshagent scheduled-task add` fails with `403` or unexpected `5xx`, treat the scheduler as blocked or unhealthy and do not claim the end-to-end scheduled workflow is complete.
- If an unfiltered project-wide `meshagent scheduled-task list` fails with `403`, do not assume the room-scoped create path is blocked. Retry with `--room <ROOM_NAME>` before concluding that scheduling is unavailable for the target room.
- If the scheduler is blocked or unhealthy, do not silently continue as if only the Worker matters. Either stop or clearly mark Worker and MailBot creation as partial preparation pending scheduler recovery.

## Input collection rules

- When the user asked for a worker that actually sends an email, treat the recipient address as required input unless it is already present in the request or in a clearly reusable existing workflow.
- Ask for all obviously blocking user-provided mail inputs in one message when possible: recipient first, then optional subject/body if needed.
- Do not ask a generic "should I continue?" question when the real blocker is a specific missing input such as the recipient address.
- If the user says "yes" or otherwise confirms they want the workflow completed, continue the build and verification flow without making them repeat the high-level request.
- If the user did not provide subject or body, you may continue with explicit defaults once the recipient is known, but say what defaults you are using.

## Payload examples

- Prompt-style payload example:
  - `{"prompt":"Send an email to david.mcqueen@timu.com using the email toolkit. Subject: Scheduled test. Body: This is a scheduled test email."}`
- Structured payload example:
  - `{"to":"david.mcqueen@timu.com","subject":"Scheduled test","body":"This is a scheduled test email.","action":"send_email"}`
- Match the payload style to the Worker's rules. If the Worker was built around prompt-driven instructions, keep using a prompt. If it was built around structured fields, use those exact fields.
