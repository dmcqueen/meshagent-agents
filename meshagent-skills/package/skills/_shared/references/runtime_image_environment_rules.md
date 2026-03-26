# Runtime Image Environment Rules

Use these rules whenever a skill needs to choose a MeshAgent runtime image for a `Service` or `ServiceTemplate`.

- If `MESHAGENT_API_URL` is present, derive the runtime image family from that environment before copying an example image.
- For `.com` environments, the standard CLI runtime example image family is `us-central1-docker.pkg.dev/meshagent-public/images/cli:{SERVER_VERSION}-esgz`.
- For `.life` environments, prefer the corresponding `.life` runtime image family instead of the production one, for example `us-central1-docker.pkg.dev/meshagent-life/meshagent-public/cli:{SERVER_VERSION}-esgz`.
- Do not copy a docs example image blindly just because it appears in `meshagent-docs`. Most docs examples use the production image family as illustrative defaults.
- If the environment is unclear, inspect an existing working room service or ask before inventing an image registry path.
- When reusing or repairing an existing room workflow, prefer the same image family already used by healthy services in that room or project.
- Keep the image family and the API environment aligned. Do not generate a `.life` room service that points at the production `meshagent-public/images/...` runtime image family unless you have explicit evidence that this environment expects it.
- Generic images such as `meshagent/cli:default` or `meshagent/shell-codex:default` are separate defaults with their own behavior. Do not silently switch between those and the environment-specific registry-backed runtime images without a reason grounded in the workflow.
