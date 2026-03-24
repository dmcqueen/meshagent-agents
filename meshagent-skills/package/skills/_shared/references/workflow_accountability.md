# Workflow Accountability

Use this reference when the user asked for an end-to-end outcome that may require multiple skills.

## Core model

Every workflow must have exactly one current workflow owner.

- The workflow owner is the skill currently responsible for the user-visible outcome.
- Supporting skills may execute part of the work, but they do not get to declare the overall workflow complete unless ownership is explicitly transferred.
- Ownership may transfer to a narrower or more appropriate skill, but the transfer must be explicit in the reasoning and the new owner must continue tracking completion gates and evidence.

## Completion gates

Do not say "done" until all relevant gates have passed.

Minimum gates for any workflow:

1. The mutation target or inspection target was identified correctly.
2. The claimed state change or observed result was verified against real room/runtime state.
3. The user-visible outcome was verified, or the exact blocker was identified.

Skill-specific gates may add stricter requirements such as live runtime proof, queue dequeue proof, mailbox identity proof, HTTP smoke tests, or log evidence.

## Evidence rules

The workflow owner must collect concrete evidence for each gate, such as:

- exact commands or packaged references used
- observed room state, service state, queue state, log lines, or runtime signals
- user-visible outputs such as a live URL, delivered queue message, or confirmed mail-send result
- if the workflow failed, the exact blocker instead of a generic "not working"

## Handoff rules

- Handoffs transfer execution work, not accountability, unless ownership is explicitly transferred.
- A supporting skill should return evidence, not a success claim for the whole workflow.
- If the current owner cannot complete the workflow without another skill, it should call that handoff and then continue evaluating the remaining gates.

## Missing-input rules

- If the workflow is blocked on specific user input, identify the exact missing input instead of asking a generic permission-to-continue question.
- Ask for all clearly blocking user inputs together when possible rather than discovering them one at a time across multiple turns.
- After the user confirms they want the workflow completed, continue the workflow unless a new concrete blocker appears.
- Do not make the user restate the original goal just because a sub-step was incomplete or partially verified.

## Preflight rules

- If the workflow depends on a specific backend surface such as scheduled tasks, room services, mail delivery, or toolkit publication, preflight the required capability before presenting the workflow as end-to-end ready.
- For room-scoped workflows, preflight with the narrowest room-scoped command that matches the actual task before trying broader project-scoped discovery or admin-style checks.
- Treat `403` responses as permission blockers, not as a cue to keep promising the blocked step later.
- If a broad project-scoped probe returns `403`, do not declare the room-scoped workflow blocked until the narrower room-scoped probe also fails.
- Treat unexpected `5xx` responses on required workflow surfaces as backend health blockers until a retry or narrower probe proves otherwise.
- When a required backend surface is blocked, either stop before creating a half-complete workflow or clearly mark any continued setup as partial preparation only.

## Forbidden shortcuts

- Do not treat object creation alone as end-to-end success.
- Do not treat YAML generation alone as deployment success.
- Do not treat queue size changes alone as business workflow success.
- Do not treat a scheduled task record alone as proof that the future workflow will work.
- Do not use the room, server, or runtime timezone as a substitute for the requesting user's timezone when the workflow is about scheduling in the user's local time.
- Do not anchor a relative scheduling request such as "one minute from now" to the start of a longer setup workflow when the user intent is relative to the actual task-creation moment.
- Do not hand the user an unresolved truncation, noise, or parsing problem for a simple inspection task. Rerun the narrow command and return the exact result.
- Do not leave an obviously required user input such as the recipient email unasked in a workflow whose purpose is to send a real email.
- Do not wait until the final step to discover that a required backend surface such as scheduled-task create is blocked when a cheap preflight could have shown that earlier.
- Do not use broad auth or project-listing failures as proof that a room-scoped workflow cannot proceed when a narrower room-scoped probe was available.
- Do not treat queue drain, service creation, or scheduled-task creation as proof that a requested email was actually delivered.
