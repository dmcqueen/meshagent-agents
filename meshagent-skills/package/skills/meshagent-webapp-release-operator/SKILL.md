---
name: meshagent-webapp-release-operator
description: Build and verify image-backed release candidates and releases for MeshAgent room webapps. Use this skill for staged release contexts, candidate image tags, side-by-side candidate services, promotion, and rollback-ready release lifecycle.
metadata:
  short-description: Image-backed candidate and release workflow for room webapps.
  references:
    bundled:
      - ../meshagent-cli-operator/references/meshagent_cli_help.md
      - ../meshagent-webapp-backend-builder/references/image_release_pipeline.sh
      - ../meshagent-webapp-backend-builder/references/webserver_image_Containerfile.example
      - ../_shared/references/environment_profile_rules.md
      - ../_shared/references/image_backed_service_iteration.md
      - ../_shared/references/live_room_cli_context.md
      - ../_shared/references/managed_hostname_rules.md
      - ../_shared/references/service_yaml_correctness.md
      - ../_shared/references/workflow_accountability.md
    requires_roots:
      - cli_root
      - docs_root
      - server_root
    resolved_targets:
      - webserver CLI source
      - services CLI source
      - shared image-backed service iteration rules
      - shared managed-hostname rules
      - shared service YAML correctness rules
  related_skills:
    - skill: meshagent-workflow-orchestrator
      when: Release work is one part of a larger end-to-end workflow.
    - skill: meshagent-webapp-backend-builder
      when: The backend behavior or handler code still needs to be built or repaired before packaging.
    - skill: meshagent-service-operator
      when: The remaining issue is generic service lifecycle rather than website-specific release flow.
    - skill: meshagent-runtime-operator
      when: The image candidate is deployed and the remaining question is live runtime state or logs.
    - skill: meshagent-webmaster
      when: The remaining work is route administration or public hostname repair.
  scope:
    owns:
      - staged release-context preparation
      - image-backed candidate and release workflow
      - side-by-side candidate service and hostname defaults
      - promotion and rollback-ready release lifecycle
    excludes:
      - backend feature implementation by itself
      - Python hot-reload dev loops
      - generic route administration
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

# MeshAgent Webapp Release Operator

Use this skill when the task is to turn a room-hosted webapp into a release candidate or release artifact that runs from a built image instead of a file-backed preview.

## Use this skill when

- The user asks for a release candidate, release, promotion, or rollback-ready image-backed deploy.
- The task is to build a versioned image for a room webapp and run it as a separate candidate service.
- The workflow needs a side-by-side candidate URL that leaves the current dev or stable site unchanged.
- The blocker is service-manifest derivation, release-context staging, or candidate image/service naming for a webserver-backed site.

## References

- Use `../meshagent-webapp-backend-builder/references/image_release_pipeline.sh` as the default in-room release pipeline asset.
- Use `../meshagent-webapp-backend-builder/references/webserver_image_Containerfile.example` as the base image pattern when a webserver-backed site needs a release image.
- Use `../_shared/references/image_backed_service_iteration.md` for the candidate/release tagging model and release-line rules.
- Use `../_shared/references/service_yaml_correctness.md` when the workflow depends on authored or derived `Service` YAML.
- Use `../_shared/references/managed_hostname_rules.md` for candidate hostname selection and validation.

## Related skills

- `meshagent-workflow-orchestrator`: release work is only one part of a larger workflow
- `meshagent-webapp-backend-builder`: backend implementation and handler behavior
- `meshagent-service-operator`: generic service lifecycle mechanics
- `meshagent-runtime-operator`: live runtime inspection after candidate deploy
- `meshagent-webmaster`: route administration and hostname repair

## Default workflow

1. Confirm that the task is `candidate` or `release` mode rather than `dev`.
2. Start from a proven backend behavior or an exact backend blocker from `meshagent-webapp-backend-builder`.
3. Stage a clean release context that contains `webserver.yaml`, the route-referenced files, and the image build file.
4. Build a versioned candidate image.
5. Derive a candidate service from a valid generated or existing service spec.
6. Deploy the candidate side-by-side and verify the candidate URL live.
7. Promote to the plain stable tag only after the candidate is proven.

## Release rules

- In `candidate` or `release` mode, the code must run from a built image. Do not treat a file-backed `webserver deploy` preview as the release artifact.
- The image should contain the code, `webserver.yaml`, and supporting assets rather than relying on a room-storage code mount.
- Use `../meshagent-webapp-backend-builder/references/image_release_pipeline.sh` as the starting point for the release pipeline instead of inventing the build flow from scratch.
- Before image build, prove that the staged release context root contains `webserver.yaml`, `Containerfile`, and the route-referenced files the build actually needs.
- When building from room storage, use room subpaths such as `/<site-dir>` as the build source, not shell-visible `/data/...` paths.
- Default to a separate candidate service and separate candidate hostname. Do not replace the current dev or stable site unless the user explicitly asked for promotion, replacement, or rollback.
- If the user did not specify naming, derive deterministic defaults from the current site:
  - candidate image tag: start at `1.0-rc1` for a new release line, then advance within that line
  - candidate service: `<base-service>-rc`
  - candidate hostname: `<base-host>-rc` in the environment-correct managed suffix family
- For a webserver-backed candidate, derive the candidate `Service` manifest from `meshagent webserver spec` or an existing valid live service spec. Do not hand-author the candidate service YAML from memory.
- Only a verified candidate should be promoted to the plain stable release tag.
- Rollback readiness means keeping the previous stable plain tag available. Do not roll back automatically unless the user explicitly asked for rollback.

## Verification rules

- Do not claim a release candidate exists until the candidate service record exists, the candidate image tag is the one actually referenced, and the candidate URL or candidate service behavior is verified.
- If the resulting managed hostname uses the wrong suffix for the active environment, treat the candidate deploy as invalid and repair the hostname before inspecting anything behind it.
- If DNS or live HTTP reachability is still unproven, report the candidate or release as incomplete rather than summarizing it as done.
- If the candidate service YAML fails validation, repair the derived manifest and rerun validation before treating the issue as a runtime problem.
- If the candidate image is built successfully but the candidate service does not exist, report that as a deploy-stage blocker, not a completed release workflow.

## Workflow accountability

- This skill may own the workflow outcome when the user's goal is primarily within this skill's scope.
- If another skill already owns the workflow, return release-stage evidence and observed state to that owner instead of declaring the overall job complete.
- If this skill hands off to another skill, keep accountability for the original goal until the handoff returns evidence or ownership is explicitly transferred.
- Follow `../_shared/references/workflow_accountability.md` for owner selection, completion gates, evidence, and forbidden shortcuts.

## Out of scope

- Python hot-reload development loops.
- Backend feature implementation by itself.
- Generic route administration.
