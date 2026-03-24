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

## Forbidden shortcuts

- Do not treat object creation alone as end-to-end success.
- Do not treat YAML generation alone as deployment success.
- Do not treat queue size changes alone as business workflow success.
- Do not treat a scheduled task record alone as proof that the future workflow will work.
- Do not hand the user an unresolved truncation, noise, or parsing problem for a simple inspection task. Rerun the narrow command and return the exact result.
