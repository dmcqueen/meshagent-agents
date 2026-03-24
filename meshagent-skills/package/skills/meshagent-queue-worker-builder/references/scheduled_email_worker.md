# Scheduled Email Worker

Use this reference when the user asks for a Worker that receives a queue message and sends an email, especially when that Worker will later be triggered by a one-time scheduled task.

## Required sequence

1. Inspect or provision the mailbox first.
2. Reuse the mailbox email address as the sender identity.
3. Verify that toolkit `email` is already published in the room or create the MailBot or equivalent service that will publish it. The normal pattern is a MailBot with `--toolkit-name=email`.
4. Build or update a queue-backed Worker service that consumes the intended queue and uses `--require-toolkit=email` only when the `email` toolkit publisher is real.
5. Validate the YAML or rendered service before deployment.
6. Create or update the service.
7. Verify the live room service appears in `meshagent room service list`.
8. Verify the runtime is actually alive with room developer output, container state, or container logs.
9. Enqueue an immediate test message now, before creating the scheduled task.
10. Confirm the queue item was consumed and inspect logs for email-send success or failure.
11. Only after the immediate smoke test passes should you create the one-time scheduled task.
12. Before creating the scheduled task, make sure the requesting user's timezone is known from user-specific context or from direct user confirmation.
13. If the user asked for a relative time such as "one minute from now," calculate that relative time from the moment you are actually ready to run the scheduled-task create command, not from the start of the larger setup workflow.

## Success criteria

Do not call the workflow complete until all of the following are true:

- the mailbox exists and its address is the sender identity used by the workflow
- toolkit `email` is visibly published in the room by a MailBot or equivalent service
- the Worker service exists in the room
- a live runtime or container is visibly running
- an immediate test message is consumed from the queue
- runtime evidence shows the mail send succeeded or shows the exact blocker
- the scheduled time was computed from the requesting user's known timezone, not just the room or server timezone
- the scheduled task is set for a future absolute time with enough safety margin to avoid already being in the past

## Failure interpretation

- A created mailbox does not prove outbound mail works.
- A created mailbox does not create toolkit `email`. If the Worker depends on `--require-toolkit=email`, prove that some live room participant publishes toolkit `email`.
- A created service record does not prove a Worker runtime is running.
- A queue size of `0` after the scheduled time does not prove success; it may also mean the job never enqueued or failed after dequeue.
- If the scheduled time is too close and setup is still incomplete, push the one-time run farther into the future instead of pretending the near-term run is still valid.
- If the user asked for a relative run time and setup consumed part of that window, recompute the relative schedule from the current moment before creating the scheduled task.
- If the requesting user's timezone is unknown, do not schedule yet. First determine it from reliable user-specific context or ask the user directly.
