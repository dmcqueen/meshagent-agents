# Runtime Image Environment Rules

Use these rules whenever a skill needs to choose a MeshAgent runtime image for a `Service` or `ServiceTemplate`.

- If `MESHAGENT_API_URL` is present, derive the runtime image family from that environment before copying an example image.
- Use the environment-appropriate registry-backed CLI runtime image family from `environment_profile_rules.md`.
- Do not copy a docs example image blindly just because it appears in `meshagent-docs`. Most docs examples use the production image family as illustrative defaults.
- If the environment is unclear, inspect an existing working room service or ask before inventing an image registry path.
- When reusing or repairing an existing room workflow, prefer the same image family already used by healthy services in that room or project.
- Keep the image family and the API environment aligned. Do not generate a service that points at the wrong environment's registry-backed runtime image family unless you have explicit evidence that this environment expects it.
- Generic images such as `meshagent/cli:default` or `meshagent/shell-codex:default` are separate defaults with their own behavior. Do not silently switch between those and the environment-specific registry-backed runtime images without a reason grounded in the workflow.
