# Managed Hostname Rules

Use these rules whenever a skill needs to choose, validate, or report a MeshAgent-managed public hostname.

- If `MESHAGENT_API_URL` is present, derive the managed suffix from that API environment: use `*.meshagent.app` for `.com` environments and `*.meshagent.dev` for `.life` environments.
- If `MESHAGENT_API_URL` is absent or does not clearly identify the environment, inspect an existing route in the current project or ask before inventing a managed public hostname.
- Packaged help or example text that shows `.meshagent.app` is illustrative only. Do not copy that suffix blindly when the active runtime indicates a different environment.
- Before running a deploy with `--domain` or reporting a managed public URL, verify that the chosen hostname suffix matches `MESHAGENT_API_URL`.
- Treat a mismatched managed suffix as invalid, not as an acceptable variant. In a `.life` environment, do not deploy, return, or accept a managed hostname outside `.meshagent.dev`. In a `.com` environment, do not deploy, return, or accept a managed hostname outside `.meshagent.app`.
- If a candidate hostname collides, keep the same environment-specific suffix family and try additional candidates before asking the user to choose one.
- If `meshagent webserver deploy --domain ...` fails because the hostname is already in use and a follow-up route read is forbidden, treat that hostname as unavailable and try a different candidate before reporting a generic permissions blocker.
- Do not report a managed URL whose suffix contradicts the active API environment.
