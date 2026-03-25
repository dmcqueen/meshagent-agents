# Managed Hostname Rules

Use these rules whenever a skill needs to choose, validate, or report a MeshAgent-managed public hostname for a room webserver, site, or public route.

- If `MESHAGENT_API_URL` is present, the managed suffix is fixed by that API environment: `.com` environments must use `*.meshagent.app` and `.life` environments must use `*.meshagent.dev`.
- If `MESHAGENT_API_URL` is absent or does not clearly identify the environment, inspect an existing route in the current project or ask before inventing a managed public hostname.
- Packaged help or example text that shows `.meshagent.app` is illustrative only. Do not copy that suffix blindly when the active runtime indicates a different environment.
- Before running a deploy with `--domain` or reporting a managed public URL, verify that the chosen hostname suffix matches `MESHAGENT_API_URL`.
- Treat a mismatched managed suffix as invalid, not as an acceptable variant. In a `.life` environment, do not deploy, return, or accept any managed hostname outside `.meshagent.dev`. In a `.com` environment, do not deploy, return, or accept any managed hostname outside `.meshagent.app`.
- If a deploy command warns that the hostname suffix is wrong for the current environment, treat that deploy result as failed for public-hostname purposes and fix the hostname before reporting success.
- If a candidate hostname collides, keep the same environment-specific suffix family and try additional candidates before asking the user to choose one.
- If `meshagent webserver deploy --domain ...` fails because the hostname is already in use and a follow-up route read is forbidden, treat that hostname as unavailable and try a different candidate before reporting a generic permissions blocker.
- Do not report a managed URL whose suffix contradicts the active API environment. Nothing else will work.
