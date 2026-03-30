#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Build and deploy an image-backed webserver candidate from room storage.

Usage:
  image_release_pipeline.sh \
    --site-source /contact-site \
    --service-file ./service.yaml \
    --image-repo contact-site \
    --release 4.2 \
    --rc 1

Required:
  --site-source PATH   Absolute room-storage source path for the current site source.
                       Use the room subpath form such as /contact-site.
                       Do not pass the shell-visible mount path under /data.
  --service-file PATH  Local Service YAML used for `meshagent service update`.
                       This should be derived from a valid generated service spec
                       such as `meshagent webserver spec ...`, or from an
                       existing known-good service spec. Prefer a template with
                       __IMAGE_TAG__.
  --image-repo NAME    Image repo/name prefix, for example `contact-site`.
  --release VERSION    Stable release line, for example `4.2`.
  --rc N               Candidate number within the release line, for example `1`.

Optional:
  --room NAME               Room name. Defaults to $MESHAGENT_ROOM.
  --project-id ID           Explicit project id if needed.
  --release-context PATH    Absolute room-storage path to stage the candidate
                            build context into. Default:
                            /build-context/<image-repo>-<release>-rc<rc>
  --containerfile-source    Local or shell-visible path to a Containerfile or
                            Dockerfile to copy into the release context if the
                            site source does not already contain one.
  --dockerfile-name NAME    Dockerfile/Containerfile name inside the release context.
                            Default: Containerfile
  --mount-target PATH       Absolute build-container mount target.
                            Default: /workspace/site
  --create                  Pass --create to `meshagent service update`.

Notes:
  - The site source path can be named anything. The script stages a clean
    release context under room storage, then mounts that staged context into a
    fixed build path inside the build container.
  - In a live room shell, room storage may be visible at /data/<name>, but
    --site-source and --release-context must still use room subpath form /<name>.
  - The staged release context must contain the application code,
    webserver.yaml, and Dockerfile/Containerfile before the build starts.
  - This script builds and deploys a candidate tag like `contact-site:4.2-rc1`.
    Promotion to the plain stable tag `4.2` should happen only after verification.
  - The service YAML must describe an image-backed runtime. Candidate/release
    deploys must not keep running app code from a room-storage code mount.
  - Do not hand-author the candidate service manifest from memory. Start from
    `meshagent webserver spec ...` or an existing valid service spec, then
    mutate only the candidate-specific fields.
EOF
}

fail() {
  echo "error: $*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "required command not found: $1"
}

assert_room_subpath() {
  local value="$1"
  local flag_name="$2"
  [[ "$value" == /* ]] || fail "${flag_name} must be an absolute room-storage path"
  [[ "$value" != /data/* ]] || fail "${flag_name} must use a room subpath like /contact-david-site, not a shell mount path under /data"
}

shell_visible_room_path() {
  local room_path="$1"
  printf '/data%s' "$room_path"
}

assert_release_context_shape() {
  local service_path="$1"

  grep -Eq '^[[:space:]]*kind:[[:space:]]*Service[[:space:]]*$' "$service_path" \
    || fail "service file must be a concrete Service document"

  for required_field in metadata agents ports container; do
    grep -Eq "^[[:space:]]*${required_field}:[[:space:]]*$" "$service_path" \
      || fail "service file must contain top-level ${required_field}: from a valid generated or existing service spec"
  done

  grep -Eq '^[[:space:]]*image:[[:space:]]*' "$service_path" \
    || fail "service file must contain an image: field or __IMAGE_TAG__ placeholder"

  if grep -Eq '^[[:space:]]*spec:[[:space:]]*$' "$service_path"; then
    fail "service file contains a nested spec: block; derive the candidate service from meshagent webserver spec or an existing valid Service YAML instead"
  fi

  if grep -Eq '^[[:space:]]*-[[:space:]]*port:[[:space:]]*' "$service_path"; then
    fail "service file uses ports entries with port: ...; preserve the exact generated PortSpec shape from meshagent webserver spec or an existing valid service"
  fi

  if grep -Eq '^[[:space:]]*subpath:[[:space:]]*/' "$service_path"; then
    fail "service file still contains a room-storage subpath mount; candidate/release runtimes must keep app code in the image"
  fi

  if grep -Fq 'meshagent webserver join' "$service_path" && ! grep -Fq 'webserver.yaml' "$service_path"; then
    fail "service file runs meshagent webserver join but does not reference webserver.yaml"
  fi
}

prepare_release_context() {
  local site_source_room="$1"
  local release_context_room="$2"
  local dockerfile_name="$3"
  local containerfile_source="${4:-}"

  local site_source_shell
  local release_context_shell
  site_source_shell="$(shell_visible_room_path "$site_source_room")"
  release_context_shell="$(shell_visible_room_path "$release_context_room")"

  [[ -d /data ]] || fail "this script expects room storage to be mounted at /data in the current shell"
  [[ -d "$site_source_shell" ]] || fail "site source directory not found under room storage mount: $site_source_shell"

  mkdir -p "$(dirname "$release_context_shell")"
  rm -rf "$release_context_shell"
  mkdir -p "$release_context_shell"

  cp -R "${site_source_shell}/." "$release_context_shell/"

  if [[ ! -f "${release_context_shell}/${dockerfile_name}" ]]; then
    if [[ -n "$containerfile_source" ]]; then
      [[ -f "$containerfile_source" ]] || fail "--containerfile-source file not found: $containerfile_source"
      cp "$containerfile_source" "${release_context_shell}/${dockerfile_name}"
    else
      fail "release context is missing ${dockerfile_name}; add it to the site source or pass --containerfile-source"
    fi
  fi

  [[ -f "${release_context_shell}/webserver.yaml" ]] || fail "release context is missing webserver.yaml after staging: ${release_context_shell}/webserver.yaml"
}

meshagent_args=()
room="${MESHAGENT_ROOM:-}"
site_source=""
release_context=""
containerfile_source=""
service_file=""
image_repo=""
release_line=""
rc_number=""
dockerfile_name="Containerfile"
mount_target="/workspace/site"
create_service=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --room)
      room="${2:-}"
      shift 2
      ;;
    --project-id)
      meshagent_args+=(--project-id "${2:-}")
      shift 2
      ;;
    --site-source)
      site_source="${2:-}"
      shift 2
      ;;
    --release-context)
      release_context="${2:-}"
      shift 2
      ;;
    --containerfile-source)
      containerfile_source="${2:-}"
      shift 2
      ;;
    --service-file)
      service_file="${2:-}"
      shift 2
      ;;
    --image-repo)
      image_repo="${2:-}"
      shift 2
      ;;
    --release)
      release_line="${2:-}"
      shift 2
      ;;
    --rc)
      rc_number="${2:-}"
      shift 2
      ;;
    --dockerfile-name)
      dockerfile_name="${2:-}"
      shift 2
      ;;
    --mount-target)
      mount_target="${2:-}"
      shift 2
      ;;
    --create)
      create_service=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      fail "unknown argument: $1"
      ;;
  esac
done

require_cmd meshagent
require_cmd awk
require_cmd grep
require_cmd mktemp

[[ -n "$room" ]] || fail "--room is required unless MESHAGENT_ROOM is already set"
[[ -n "$site_source" ]] || fail "--site-source is required"
[[ -n "$service_file" ]] || fail "--service-file is required"
[[ -n "$image_repo" ]] || fail "--image-repo is required"
[[ -n "$release_line" ]] || fail "--release is required"
[[ -n "$rc_number" ]] || fail "--rc is required"
[[ -f "$service_file" ]] || fail "service file not found: $service_file"
[[ "$mount_target" == /* ]] || fail "--mount-target must be an absolute path"
assert_room_subpath "$site_source" "--site-source"

assert_release_context_shape "$service_file"

candidate_tag="${image_repo}:${release_line}-rc${rc_number}"
if [[ -z "$release_context" ]]; then
  release_context="/build-context/${image_repo}-${release_line}-rc${rc_number}"
fi
assert_room_subpath "$release_context" "--release-context"
dockerfile_path="${mount_target}/${dockerfile_name}"
tmp_service="$(mktemp "${TMPDIR:-/tmp}/meshagent-service.XXXXXX.yaml")"
cleanup() {
  rm -f "$tmp_service"
}
trap cleanup EXIT

echo "Preparing staged release context: ${release_context}"
prepare_release_context "$site_source" "$release_context" "$dockerfile_name" "$containerfile_source"

echo "Building candidate image: ${candidate_tag}"
meshagent room container image build \
  "${meshagent_args[@]}" \
  --room "$room" \
  --tag "$candidate_tag" \
  --mount-room-path "${release_context}:${mount_target}:ro" \
  --context-path "$mount_target" \
  --dockerfile-path "$dockerfile_path"

echo "Verifying built image exists in room: ${candidate_tag}"
if ! meshagent room container image list "${meshagent_args[@]}" --room "$room" | grep -Fq "$candidate_tag"; then
  fail "built image tag not found in room image list: ${candidate_tag}"
fi

if grep -Fq "__IMAGE_TAG__" "$service_file"; then
  sed "s|__IMAGE_TAG__|${candidate_tag}|g" "$service_file" >"$tmp_service"
else
  awk -v image_tag="$candidate_tag" '
    !done && $0 ~ /^[[:space:]]*image:[[:space:]]*/ {
      sub(/image:[[:space:]].*/, "image: " image_tag)
      done = 1
    }
    { print }
    END {
      if (!done) {
        exit 41
      }
    }
  ' "$service_file" >"$tmp_service" || fail "service file must contain __IMAGE_TAG__ or at least one image: line"
fi

assert_release_context_shape "$tmp_service"

echo "Updating service to candidate image: ${candidate_tag}"
service_update_args=(
  service update
  "${meshagent_args[@]}"
  --room "$room"
  --file "$tmp_service"
)
if [[ "$create_service" -eq 1 ]]; then
  service_update_args+=(--create)
fi
meshagent "${service_update_args[@]}"

cat <<EOF
Candidate deployed: ${candidate_tag}
Staged release context: ${release_context}

Next steps:
  1. Verify service health and the real user-facing surface.
  2. If the candidate passes, promote the exact image to the plain stable tag:
       ${image_repo}:${release_line}
  3. If the user later asks for rollback, roll back to the previous plain stable tag,
     not to a release-candidate tag.
EOF
