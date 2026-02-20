# meshagent-agents

Repository of MeshAgent project manifests used for install links and publishing.

## Files per project

Typical project files:

- `agents.prod.yaml`: canonical publish manifest for prod installs.
- `agents.yaml`, `agents.dev.yaml`, or `agent.yaml`: source/dev variants.
- `manifest.json`: metadata sidecar used by publish and Webflow flows.
- `README.md`: human-readable project summary generated from `manifest.json`.

Optional project-specific artifacts may also exist (for example request templates like `submit-resume.json`).

## manifest.json contract

Expected fields:

- `id`: stable machine identifier.
- `name`: human-readable title for display.
- `description`: short summary for cards/lists.
- `long_description`: detailed intent and workflow summary.
- `dev.install_link`, `dev.raw_sha_link`: dev links when applicable.
- `prod.install_link`, `prod.raw_sha_link`: prod links (SHA-pinned).

Notes:

- `name` should be clean title-case text suitable for UI display.
- `long_description` should describe intent and outcomes from YAML behavior, not generic boilerplate.
- name references inside `long_description` should match `name` formatting.

## Image conventions

- Prod manifests should use the prod registry prefix:
  - `us-central1-docker.pkg.dev/meshagent-public/images/`
- Dev/source manifests may use the life/dev prefix:
  - `us-central1-docker.pkg.dev/meshagent-life/meshagent-public/`

When a project has no prod manifest, pipeline tooling materializes `agents.prod.yaml` from best available source YAML.

## Editing guidance

- Edit YAML manifests as source of truth.
- Treat `manifest.json` and project `README.md` as generated outputs unless you are intentionally patching metadata.
- Keep one project per directory and keep identifiers stable to avoid broken links and duplicate catalog entries.
