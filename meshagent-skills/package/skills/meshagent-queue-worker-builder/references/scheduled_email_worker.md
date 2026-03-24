# Scheduled Email Worker

Use this reference when the user asks for a Worker that receives a queue message and sends an email, especially when that Worker will later be triggered by a one-time scheduled task.

## Required sequence

1. Inspect or provision the mailbox first.
2. Reuse the mailbox email address as the sender identity.
3. Build or update a queue-backed Worker service that consumes the intended queue.
4. Validate the YAML or rendered service before deployment.
5. Create or update the service.
6. Verify the live room service appears in `meshagent room service list`.
7. Verify the runtime is actually alive with room developer output, container state, or container logs.
8. Enqueue an immediate test message now, before creating the scheduled task.
9. Confirm the queue item was consumed and inspect logs for email-send success or failure.
10. Only after the immediate smoke test passes should you create the one-time scheduled task.

## Success criteria

Do not call the workflow complete until all of the following are true:

- the mailbox exists and its address is the sender identity used by the workflow
- the Worker service exists in the room
- a live runtime or container is visibly running
- an immediate test message is consumed from the queue
- runtime evidence shows the mail send succeeded or shows the exact blocker
- the scheduled task is set for a future absolute time with enough safety margin to avoid already being in the past

## Failure interpretation

- A created mailbox does not prove outbound mail works.
- A created service record does not prove a Worker runtime is running.
- A queue size of `0` after the scheduled time does not prove success; it may also mean the job never enqueued or failed after dequeue.
- If the scheduled time is too close and setup is still incomplete, push the one-time run farther into the future instead of pretending the near-term run is still valid.
