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

## Verification discipline

- Do not claim completion without fresh verification evidence from the actual workflow surface.
- Verify on the real user-facing or workflow-facing surface, not just on an internal precursor such as object creation, route creation, queue growth, or local file generation.
- If one stage is proven and a later stage fails, report them separately. Do not collapse a verified DB write, queue enqueue, or deploy into a vague “still broken” status when the remaining bug is later in the flow.
- If only part of the workflow is proven, label it as partial. Do not present partial success as completed work.
- After a new mutation, redeploy, or retry, use fresh evidence. Earlier proof does not automatically carry forward to the new state.

## Debugging discipline

- Reproduce the failure on the real workflow surface before proposing a fix.
- Treat the visible symptom and the root cause as different things until evidence connects them.
- Narrow the failing stage before editing. Identify whether the break is in load, configuration, runtime behavior, downstream integration, or verification.
- Do not stack multiple speculative fixes at once when one narrower probe or smaller intervention can identify the cause.
- After each intervention, verify that the observed symptom actually changed before declaring progress.
- If two or three attempted fixes on the same problem fail, stop stacking more patches. Summarize what changed, what evidence moved, and whether the current design or execution path should be reconsidered.
- After repeated failed fixes, prefer a simpler path, a different integration boundary, or an architectural rethink over a fourth speculative patch.

## Minimal change discipline

- Prove a new behavior or hypothesis with the smallest safe code or configuration change before attempting broader cleanup or rewrite.
- Change one thing at a time. Do not bundle refactors, cleanup, or "while I'm here" improvements into the first proving patch.
- If the narrow change works, keep the scope narrow unless a broader cleanup is clearly needed next.
- If the narrow change fails, use what you learned to choose the next smallest change rather than widening the patch speculatively.
- Prefer existing patterns and local abstractions over introducing a new configuration model, helper stack, or architecture for a small change.

## Isolation before integration

- Prove a new behavior in isolation before blending it into an existing working flow.
- Verify the isolated behavior on its own surface first, then integrate it into the larger workflow.
- If isolated proof fails, keep the investigation local to that behavior instead of widening the patch into adjacent surfaces.
- When integration starts, keep the first integration patch narrow and confirm that the previously proven behavior still works in context.

## Artifact integrity discipline

- Before debugging runtime behavior inside a newly changed deployed artifact, prove that the deployed artifact still contains the expected files, paths, and import roots.
- If a route, handler, or runtime now depends on a new helper file or module, verify that the helper is present in the deployable source tree and loadable from the actual runtime import root before treating later failures as business-logic bugs.
- Treat missing files, wrong upload paths, wrong app roots, stale mounted files, or module-load errors as artifact-integrity failures first, not as evidence that the downstream database, mail, or business logic is wrong.
- For a newly mutated deployed artifact, prove load and import integrity before moving on to end-to-end behavior verification.

## Review discipline

- When responding to review feedback, verify the suggestion against the real implementation, runtime behavior, and current workflow evidence before changing code or configuration.
- Do not treat reviewer confidence, tone, or repetition as evidence. Inspect the actual code, command behavior, or live state first.
- If review feedback conflicts with observed evidence, explicit user direction, or a proven platform constraint, say so clearly and explain the conflict technically instead of blindly applying the suggestion.
- When practical, implement accepted review items one at a time and verify each accepted item on the relevant surface before stacking the next one.

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
- Do not ask the user for permission to create ordinary workflow prerequisites that the requested workflow clearly needs and the current skill is already allowed to create, such as a room mailbox for a mailbox-backed email workflow.
- Treat room resources that can be safely provisioned as implementation work, not as user input, unless the user asked to control that choice directly.
- If the user's original request is already an obvious end-to-end outcome such as "schedule a test email," do not stop at "I can set it up" or "reply yes and I'll proceed." Continue the ordinary prerequisite setup automatically unless a true missing input or hard blocker appears.
- Ask for all clearly blocking user inputs together when possible rather than discovering them one at a time across multiple turns.
- After the user confirms they want the workflow completed, continue the workflow unless a new concrete blocker appears.
- Do not make the user restate the original goal just because a sub-step was incomplete or partially verified.

## Progressive disclosure rules

- Start with the narrowest safe action or probe that could directly satisfy the user's request or prove the next blocker.
- Separate checks that are required before acting from checks that are required before claiming success.
- Do not front-load broad environment surveys, project-wide discovery, or admin-style checks when one narrow task-matching room or runtime action would answer the question faster.
- Defer deeper preflights until the chosen execution path actually depends on that surface, the first narrow path fails, or the workflow is about to cross a mutation boundary that makes the extra check necessary.
- For simple requests, prefer one direct task-matching action first and expand only if that action fails or reveals ambiguity.

## Preflight rules

- If the workflow depends on a specific backend surface such as scheduled tasks, room services, mail delivery, or toolkit publication, preflight the required capability before presenting the workflow as end-to-end ready.
- Do not read the preflight rule as "survey everything up front." Preflight only the surfaces that the current chosen path actually needs before the next risky or user-visible step.
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
- Do not present a created route record, deploy result, or hostname string as the achieved public URL until DNS and the required live HTTP checks have passed.
- For a normal public website or contact form, do not treat DNS resolution, a TCP connection, or a redirect alone as sufficient verification. The live GET must reach the intended page with the expected final success status, normally `200`.
- If a public URL has not been verified yet, label it explicitly as an unverified candidate or partial preparation, not as the finished output.
- Do not lead with "done", "deployed", "created route", or similar completion language when the public-site outcome is still blocked on DNS or live HTTP verification.
- Do not summarize a site request as "built", "deployed", or "created in the room" when the actual requested outcome is still a non-working public site.
- Do not use the room, server, or runtime timezone as a substitute for the requesting user's timezone when the workflow is about scheduling in the user's local time.
- Do not anchor a relative scheduling request such as "one minute from now" to the start of a longer setup workflow when the user intent is relative to the actual task-creation moment.
- Do not hand the user an unresolved truncation, noise, or parsing problem for a simple inspection task. Rerun the narrow command and return the exact result.
- Do not leave an obviously required user input such as the recipient email unasked in a workflow whose purpose is to send a real email.
- Do not wait until the final step to discover that a required backend surface such as scheduled-task create is blocked when a cheap preflight could have shown that earlier.
- Do not use broad auth or project-listing failures as proof that a room-scoped workflow cannot proceed when a narrower room-scoped probe was available.
- Do not use `meshagent auth whoami` as a prerequisite gatekeeper for a known-room workflow.
- Do not treat room messaging enablement as a setup task for workflows that do not actually require room messaging. If a command reports that messaging is already enabled, treat that as non-blocking room state rather than a failure to repair.
- Do not keep retrying `meshagent room container exec` against another participant's private container after an isolation denial. Switch to container logs, developer watch, service state, public HTTP checks, or deployed artifacts instead.
- Do not pass arbitrary human-readable ids into workflow surfaces that are UUID-backed. If a skill has not proven the id format is accepted, omit the custom id rather than guessing.
- Do not treat queue drain, service creation, or scheduled-task creation as proof that a requested email was actually delivered.
- Do not assume that a scheduled task payload implicitly means "send an email" unless the payload explicitly maps to the Worker's email-sending rules.
- Do not satisfy a user request for email by sending a room message, participant message, or broadcast unless the user explicitly asked for that communication medium instead of real email.
- Do not stall a simple workflow by starting with broad project, room, or service surveys when one narrow task-matching action could have answered the request or revealed the blocker directly.
- Do not turn an obvious end-to-end request into a two-step consent dance by asking the user to approve ordinary prerequisite setup that is already inside the requested workflow.
- Do not stop at an internal actionable blocker such as a crashing service, wrong hostname suffix, missing toolkit publisher, or failed smoke test and ask "if you want, I'll keep going." Continue the normal fix path until the workflow is complete or a true external blocker remains.
- Do not blindly retry one-time scheduled-task creation after an uncertain add result. First check whether the task was already created or whether an equivalent near-future task already exists for the same queue and payload.
