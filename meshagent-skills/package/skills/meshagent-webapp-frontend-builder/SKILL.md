---
name: meshagent-webapp-frontend-builder
description: Build interactive MeshAgent room web app frontends with Preact + htm, minimal tooling, and live public-URL verification on top of the canonical backend path.
metadata:
  short-description: Canonical frontend path for interactive room web apps using Preact + htm.
  references:
    bundled:
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - cli_root
      - docs_root
    resolved_targets:
      - shared live-room CLI context rules
      - webserver CLI source
      - room service command help
  related_skills:
    - skill: meshagent-webapp-backend-builder
      when: The app needs the canonical Python handler, DB, mail, deploy, or verification backend path.
    - skill: meshagent-webapp-dev-operator
      when: The frontend work depends on a hot-reload backend dev loop while Python handlers are still changing.
    - skill: meshagent-webapp-release-operator
      when: The frontend work must be delivered through an image-backed candidate or release of the room webapp.
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

# MeshAgent Webapp Frontend Builder

Use this skill when the task is to build or debug the frontend layer of an interactive MeshAgent room web app with Preact + htm, but without a heavy frontend toolchain.

## Use this skill when

- The user wants a mini site, small dashboard, landing page, creative UI, or interactive room webapp with component-style frontend state.
- The site can be served as static assets from `website/dist/` without a complex bundler pipeline.
- The task is frontend-heavy and benefits from `Preact + htm` rather than plain static HTML.
- The app benefits from a richer client-side interaction layer on top of a Python backend path.
- The current problem is a UI bug, interaction bug, caching issue, or deploy/verification issue on a room-hosted mini site.

## References

- After root resolution, inspect the resolved webserver CLI source for actual MeshAgent webserver behavior.
- Use `../meshagent-cli-operator/references/meshagent_cli_help.md` for exact `meshagent webserver ...` and room service command shapes.
- Use `../_shared/references/live_room_cli_context.md` when the frontend workflow runs in or targets a known live room.

## Related skills

- `meshagent-webapp-backend-builder`: Use it for the canonical Python backend, DB, mail, deploy, route, and verification workflow around this frontend specialization.
- `meshagent-webapp-dev-operator`: Use it when the backend side of the app must stay in a hot-reload dev loop while frontend work is still changing.
- `meshagent-webapp-release-operator`: Use it when the combined app is moving into an image-backed candidate or release workflow.
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
- Treat this skill as the canonical frontend path for interactive or creative room sites, but keep it layered over the backend conventions from `meshagent-webapp-backend-builder`.
- For DB-backed or email-featured apps, let the backend skill own Python handlers, `room.database.*`, and mail paths while this skill owns UI composition, state, and interactions.
- If the backend side of the app is actively iterating in a hot-reload loop, keep that runtime loop on `meshagent-webapp-dev-operator`.
- If the app is moving into an image-backed candidate or release flow, keep that packaging and deploy lifecycle on `meshagent-webapp-release-operator`.
- Prefer thin frontend calls into narrow backend endpoints over duplicating business logic or persistence logic in the browser.
- If a build step is unavoidable, keep it minimal and justify it from the actual requirements.
- When deploying frontend changes, add cache-busting query params to script and stylesheet tags so users do not see stale assets.

## UX and debugging rules

- Treat reported "broken" behavior as a possible UX mismatch, not just a code defect.
- If two UI actions look the same, users will expect them to behave the same.
- Before shipping, walk the flow from the user's perspective: what they see, what they click, and what label or outcome they expect.
- If a first UI fix fails, revisit the UX or interaction assumption before changing more code.

## Live room and service rules

- Apply `../_shared/references/live_room_cli_context.md` when the room is already known from runtime context or the user's request.
- If running inside a live MeshAgent room, use the existing room context first.
- Do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as prerequisite checks for room-scoped frontend deploy or verification work.
- For room service operations, use the actual command forms and flags. Do not assume positional service identifiers work.
- The website runs in a separate container context. Do not rely on `localhost` checks from the agent container to prove the public site works.
- Verify website behavior through the public URL after deploy.
- Use longer command timeouts for installs, builds, and MeshAgent operations when the environment is slow.

## Implementation rules

- Read before writing. Match the existing site structure and style.
- Apply the shared minimal change discipline from `../_shared/references/workflow_accountability.md`, then keep frontend changes simple and reversible.
- If the app needs DB, mail, or other server-backed behavior, keep the backend on the `meshagent-webapp-backend-builder` golden path instead of inventing a frontend-only or alternate-backend architecture here.
- If a change breaks the site, return to the last known working state before trying a different fix.
- Prefer rewriting a whole small file over brittle shell substitutions that span several lines when generating frontend assets.
- After writing or rewriting files, verify the contents and then verify the live behavior.
- If you emit JavaScript through shell heredocs, be careful with Unicode escape handling and other quoting pitfalls.

## Verification rules

- Apply the shared verification discipline from `../_shared/references/workflow_accountability.md`, then use the frontend-specific rules below for what counts as proof here.
- Apply the shared debugging discipline from `../_shared/references/workflow_accountability.md`, then use the frontend-specific rules below to separate frontend logic, deploy, cache, and public-URL failures.
- For frontend work, verify both build/deploy success and the live served output.
- Reproduce the original bug when possible, then confirm the fix on the live site.
- Use a Build -> Verify -> Build -> Verify loop instead of batching many unverified changes.

## Anti-patterns

- Do not introduce Vite or bundler complexity for a mini room site unless the requirements clearly need it.
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
- General backend architecture, room-database schema design, or mail-runtime design when `meshagent-webapp-backend-builder` is the better fit.
