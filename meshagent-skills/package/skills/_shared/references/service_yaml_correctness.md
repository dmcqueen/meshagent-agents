# Service YAML Correctness

Use these rules whenever a skill authors or rewrites `Service` or `ServiceTemplate` YAML.

- Prefer generated specs over handwritten YAML when the CLI already has a generator for the runtime shape you need. Start from `meshagent worker spec`, `meshagent mailbot spec`, `meshagent multi spec`, or `meshagent service spec` before hand-editing fields.
- If you must hand-author YAML, start from the nearest working example or a rendered/generated spec. Do not invent a manifest structure from memory.
- Treat the container `command` as code that must match the real CLI. Validate agent command flags against the packaged CLI help or the actual CLI source before treating the YAML as deployable.
- Do not invent flags that the target command does not support. For example, `meshagent worker join` uses `--rule` and `--room-rules`; do not substitute unsupported flags such as `--prompt`.
- Make the declared agent roles match the runtime command. If the manifest says it contains a `Worker`, the command must actually start a worker path. If it says it contains a `MailBot`, the command must start a mailbot path. Do not declare two roles and only start one of them.
- For scheduled email workflows, only use these composition patterns:
  - a dedicated MailBot publishes toolkit `email` using a real mailbox-backed sender identity, and a dedicated Worker consumes the scheduled job queue and uses toolkit `email`
  - one `meshagent multi join` service runs both the MailBot and Worker roles explicitly
- For scheduled email workflows, reject these patterns as incorrect:
  - a standalone MailBot pointed at the scheduled job queue
  - a Worker with no explicit rule telling it to send the email
  - a MailBot with an invented mailbox-looking sender identity
- Keep mailbox and job queues distinct unless the implementation clearly requires them to be the same. A MailBot queue should match the mailbox or inbound mail path; a Worker queue should match the scheduled job queue.
- Do not use invented sender identities such as `something@meshagent.local` for room email workflows. Use a real mailbox-backed address from the current project and room.
- If the YAML embeds room rules files or startup scripts, make sure the files are actually mounted or written into the container before the command references them.
- Before deployment, run the narrowest validation path that matches the asset:
  - `meshagent service validate` for a concrete `Service`
  - `meshagent service validate-template` and `meshagent service render-template` for a `ServiceTemplate`
- If validation fails, do not deploy and do not just rerun the same command blindly. Read the exact validation error, repair the YAML or template, and rerun validation. Repeat that fix-and-revalidate loop until validation passes or the remaining blocker is clearly external to the asset itself.
- Before treating YAML as correct, verify all of these:
  - structural correctness: valid service or template shape
  - command correctness: every runtime flag is actually supported
  - role correctness: declared agent roles match the command that will run
  - wiring correctness: queue names, toolkit publication, mailbox identity, and mounted files all match the intended behavior
