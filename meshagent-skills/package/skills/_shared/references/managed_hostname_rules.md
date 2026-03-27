# Managed Hostname Rules

Use these rules whenever a skill needs to choose, validate, or report a MeshAgent-managed public hostname for a room webserver, site, or public route.

- If `MESHAGENT_API_URL` is present, the managed suffix is fixed by that API environment: `.com` environments must use `*.meshagent.app` and `.life` environments must use `*.meshagent.dev`.
- Resolve the active API environment explicitly before choosing or reporting a managed hostname. The agent should be able to state both sides of the mapping, for example: `MESHAGENT_API_URL` is a `.life` environment, so the only valid managed public suffix is `.meshagent.dev`.
- If `MESHAGENT_API_URL` is absent or does not clearly identify the environment, inspect an existing route in the current project or ask before inventing a managed public hostname.
- Packaged help or example text that shows `.meshagent.app` is illustrative only. Do not copy that suffix blindly when the active runtime indicates a different environment.
- Before running a deploy with `--domain` or reporting a managed public URL, verify that the chosen hostname suffix matches `MESHAGENT_API_URL` and state the expected suffix to yourself first.
- Treat a mismatched managed suffix as invalid, not as an acceptable variant. In a `.life` environment, do not deploy, return, or accept any managed hostname outside `.meshagent.dev`. In a `.com` environment, do not deploy, return, or accept any managed hostname outside `.meshagent.app`.
- A managed hostname with the wrong environment suffix is a hard error, not a debugging lead. Stop the public-site workflow immediately and correct the hostname before inspecting any edge, DNS, route, or application behavior behind that invalid hostname.
- If a deploy command warns that the hostname suffix is wrong for the current environment, treat that deploy result as failed for public-hostname purposes and fix the hostname before reporting success.
- If a candidate hostname collides, keep the same environment-specific suffix family and try additional candidates before asking the user to choose one.
- When a workflow is creating a release candidate rather than promoting the main release, choose a separate candidate hostname in the same managed suffix family and leave the current dev or stable hostname unchanged unless the user explicitly asked to replace it.
- If the user did not specify a candidate hostname, derive it from the current dev or stable hostname label by appending `-rc` before the environment-correct managed suffix, for example `contact-david` -> `contact-david-rc.meshagent.dev`.
- If `meshagent webserver deploy --domain ...` fails because the hostname is already in use and a follow-up route read is forbidden, treat that hostname as unavailable and try a different candidate before reporting a generic permissions blocker.
- If a mailbox domain, API environment, and managed public hostname disagree about whether the room is `.life` or `.com`, treat that as unresolved environment evidence and do not report the public URL as valid yet.
- Do not report, test, or keep debugging a managed URL whose suffix contradicts the active API environment. Nothing behind that URL counts as valid workflow evidence until the hostname itself is corrected.
