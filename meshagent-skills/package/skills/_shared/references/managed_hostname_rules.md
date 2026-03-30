# Managed Hostname Rules

Use these rules whenever a skill needs to choose, validate, or report a MeshAgent-managed public hostname for a room webserver, site, or public route.

- Resolve the active API environment explicitly before choosing or reporting a managed hostname.
- The only valid managed public suffix is the environment-appropriate managed suffix from `environment_profile_rules.md`.
- The agent should be able to state the mapping it resolved before using or reporting a hostname.
- Managed public hostnames and managed mailbox domains are different surfaces. Do not derive a public site hostname from the mailbox domain, SMTP host, or mailbox address.
- Treat domains such as `mail.meshagent.life`, `mail.meshagent.com`, `.meshagent.life`, or `.meshagent.com` as mail or API evidence, not as valid managed minisite suffixes.
- The mapping in `environment_profile_rules.md` is explicit and overrides suffix guessing. Example: `api.meshagent.life` plus `mail.meshagent.life` still maps managed public minisites to `.meshagent.dev`.
- If `MESHAGENT_API_URL` is absent or does not clearly identify the environment, inspect an existing route in the current project or ask before inventing a managed public hostname.
- Packaged help or example text that shows `.meshagent.app` is illustrative only. Do not copy that suffix blindly when the active runtime indicates a different environment.
- Before running a deploy with `--domain` or reporting a managed public URL, verify that the chosen hostname suffix matches `MESHAGENT_API_URL` and state the expected suffix to yourself first.
- Treat a mismatched managed suffix as invalid, not as an acceptable variant. Do not deploy, return, or accept any managed hostname outside the environment-appropriate suffix from `environment_profile_rules.md`.
- A managed hostname with the wrong environment suffix is a hard error, not a debugging lead. Stop the public-site workflow immediately and correct the hostname before inspecting any edge, DNS, route, or application behavior behind that invalid hostname.
- A public hostname under the mail domain family or API domain family is a hard error for a managed minisite workflow. Stop immediately and correct the hostname before treating the deploy as meaningful.
- If a deploy command warns that the hostname suffix is wrong for the current environment, treat that deploy result as failed for public-hostname purposes and fix the hostname before reporting success.
- If a candidate hostname collides, keep the same environment-specific suffix family and try additional candidates before asking the user to choose one.
- When a workflow is creating a release candidate rather than promoting the main release, choose a separate candidate hostname in the same managed suffix family and leave the current dev or stable hostname unchanged unless the user explicitly asked to replace it.
- If the user did not specify a candidate hostname, derive it from the current dev or stable hostname label by appending `-rc` before the environment-correct managed suffix.
- If `meshagent webserver deploy --domain ...` fails because the hostname is already in use and a follow-up route read is forbidden, treat that hostname as unavailable and try a different candidate before reporting a generic permissions blocker.
- If a mailbox domain, API environment, and managed public hostname disagree about whether the room is `.life` or `.com`, treat that as unresolved environment evidence and do not report the public URL as valid yet.
- Do not report, test, or keep debugging a managed URL whose suffix contradicts the active API environment. Nothing behind that URL counts as valid workflow evidence until the hostname itself is corrected.
