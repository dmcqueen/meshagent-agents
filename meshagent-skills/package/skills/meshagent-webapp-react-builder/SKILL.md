---
name: meshagent-webapp-react-builder
description: Build small MeshAgent room web apps with a React-style UI using Preact + htm, minimal or zero build tooling, and live public-URL verification after deploy.
metadata:
  short-description: Build small React-style room webapps with Preact + htm and live verification.
  references:
    bundled:
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - cli_root
      - docs_root
    resolved_targets:
      - webserver CLI source
      - room service command help
  related_skills:
    - skill: meshagent-webapp-builder
      when: The task is a broader room webapp workflow, public deploy path, or contact-form implementation.
    - skill: meshagent-sdk-researcher
      when: Checkout roots or codebase references must be resolved first.
    - skill: meshagent-service-operator
      when: The main task is room service lifecycle rather than frontend implementation.
  scope:
    owns:
      - small React-style room webapps
      - Preact plus htm frontend implementation
      - live frontend verification after deploy
    excludes:
      - large SPA or bundler-heavy frontend architecture
      - generic non-React room webapps
  workflow:
    can_be_owner: true
    handoff_policy: retain_accountability_until_owner_transfer
    completion_gates:
      - mutation_target_confirmed_when_relevant
      - observed_state_matches_claim
      - user_visible_result_verified_or_exact_blocker_reported
    evidence:
      - exact_commands_or_artifacts_used
      - observed_room_or_runtime_state
      - user_visible_result_or_exact_blocker
---

# MeshAgent Webapp React Builder

Use this skill when the task is to build or debug a small MeshAgent room website with a React-style component model, but without a heavy frontend toolchain.

## Use this skill when

- The user wants a mini site, small dashboard, landing page, or interactive room webapp with React-style components.
- The site can be served as static assets from `website/dist/` without a complex bundler pipeline.
- The task is frontend-heavy and benefits from `Preact + htm` rather than plain static HTML.
- The current problem is a UI bug, interaction bug, caching issue, or deploy/verification issue on a room-hosted mini site.

## References

- After root resolution, inspect the resolved webserver CLI source for actual MeshAgent webserver behavior.
- Use `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact `meshagent webserver ...` and room service command shapes.

## Related skills

- `meshagent-webapp-builder`: Use it for the broader room webapp, deploy, route, and verification workflow around this frontend specialization.
- `meshagent-sdk-researcher`: Resolve checkout roots before using codebase references outside this skill bundle.
- `meshagent-service-operator`: Use it when the main task is room service lifecycle rather than frontend implementation.

## Default workflow

1. Understand the user-visible problem before changing code. Ask what the user expected if the reported bug could be UX rather than implementation.
2. Read the existing site files and deployment shape before editing.
3. For non-trivial work, write a short plan before building and re-plan if the first assumption fails.
4. Prefer the lightest frontend stack that satisfies the request.
5. Build incrementally and verify after each meaningful change.
6. After deploy, verify the live public URL, not just local files or build output.

## Frontend stack

- Prefer `Preact + htm + esm.sh` imports for mini sites.
- Prefer plain `<script type="module">` over Vite, webpack, or a custom bundler when the site can stay simple.
- Put deployable static frontend assets in `website/dist/`.
- If a build step is unavoidable, keep it minimal and justify it from the actual requirements.
- When deploying frontend changes, add cache-busting query params to script and stylesheet tags so users do not see stale assets.

## UX and debugging rules

- Treat reported "broken" behavior as a possible UX mismatch, not just a code defect.
- If two UI actions look the same, users will expect them to behave the same.
- Before shipping, walk the flow from the user's perspective: what they see, what they click, and what label or outcome they expect.
- If a first fix fails, stop and revisit the assumption instead of stacking speculative changes.

## Live room and service rules

- If running inside a live MeshAgent room, use the existing room context first.
- For room service operations, use the actual command forms and flags. Do not assume positional service identifiers work.
- The website runs in a separate container context. Do not rely on `localhost` checks from the agent container to prove the public site works.
- Verify website behavior through the public URL after deploy.
- Use longer command timeouts for installs, builds, and MeshAgent operations when the environment is slow.

## Implementation rules

- Read before writing. Match the existing site structure and style.
- Keep the implementation simple and reversible.
- If a change breaks the site, return to the last known working state before trying a different fix.
- Prefer rewriting a whole small file over brittle multi-line shell substitutions when generating frontend assets.
- After writing or rewriting files, verify the contents and then verify the live behavior.
- If you emit JavaScript through shell heredocs, be careful with Unicode escape handling and other quoting pitfalls.

## Verification rules

- Do not mark the task complete based only on file creation or a successful deploy command.
- For frontend work, verify both build/deploy success and the live served output.
- Reproduce the original bug when possible, then confirm the fix on the live site.
- Use a Build -> Verify -> Build -> Verify loop instead of batching many unverified changes.

## Anti-patterns

- Do not introduce Vite or bundler complexity for a mini room site unless the requirements clearly need it.
- Do not stack multiple speculative fixes onto the same bug.
- Do not assume a user-reported bug is purely technical when the UI model may be the real problem.
- Do not test the room-hosted website only via container-local `localhost`.
- Do not deploy frontend changes without accounting for browser caching.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return frontend, deploy, and live-URL evidence to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- Large SPA architecture, complex build pipelines, or frontend platform design beyond what a room mini site needs.
- General non-React room webapps when the plain `meshagent-webapp-builder` skill is a better fit.
