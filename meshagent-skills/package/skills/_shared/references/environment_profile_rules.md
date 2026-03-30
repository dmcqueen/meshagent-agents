# Environment Profile Rules

Use this reference as the single source of truth for environment-specific MeshAgent values that vary between `.life` and `.com` runtimes.

- Shared skill logic should stay environment-neutral whenever possible.
- When a skill needs a concrete public suffix, mailbox domain, SMTP fallback host, or runtime image family, resolve the active environment first and then use the mapping in this file.
- If the published environment mapping changes later, update this file first and keep downstream skills phrased in terms of the environment-appropriate value instead of restating old literals.

## Current mapping

- `.life` API environments
  - managed public hostname suffix: `.meshagent.dev`
  - managed mailbox domain: `mail.meshagent.life`
  - direct-SMTP fallback host: `mail.meshagent.life`
  - preferred registry-backed CLI runtime image family: `us-central1-docker.pkg.dev/meshagent-life/meshagent-public/cli:{SERVER_VERSION}-esgz`
- `.com` API environments
  - managed public hostname suffix: `.meshagent.app`
  - managed mailbox domain: `mail.meshagent.com`
  - direct-SMTP fallback host: `mail.meshagent.com`
  - preferred registry-backed CLI runtime image family: `us-central1-docker.pkg.dev/meshagent-public/images/cli:{SERVER_VERSION}-esgz`

## Usage rules

- Treat this file as environment configuration, not as permission to hardcode one environment's values throughout unrelated skills.
- Downstream references should normally say "use the environment-appropriate managed suffix/mail domain/runtime image family from `environment_profile_rules.md`."
- Keep executable examples or generated code environment-aware only when they genuinely need runtime branching logic.
