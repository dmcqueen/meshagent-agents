#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Build and deploy an image-backed webserver candidate from room storage.

Usage:
  image_release_pipeline.sh \
    --room-source /contact-site \
    --service-file ./service.yaml \
    --image-repo contact-site \
    --release 4.2 \
    --rc 1

Required:
  --room-source PATH   Absolute room-storage source path containing the release context.
                       Use the room subpath form such as /contact-site.
                       Do not pass the shell-visible mount path under /data.
  --service-file PATH  Local Service YAML used for `meshagent service update`.
                       Prefer a template with __IMAGE_TAG__.
  --image-repo NAME    Image repo/name prefix, for example `contact-site`.
  --release VERSION    Stable release line, for example `4.2`.
  --rc N               Candidate number within the release line, for example `1`.

Optional:
  --room NAME               Room name. Defaults to $MESHAGENT_ROOM.
  --project-id ID           Explicit project id if needed.
  --dockerfile-name NAME    Dockerfile/Containerfile name inside the release context.
                            Default: Containerfile
  --mount-target PATH       Absolute build-container mount target.
                            Default: /workspace/site
  --create                  Pass --create to `meshagent service update`.

Notes:
  - The room source path can be named anything. The script always mounts it into
    a fixed build path inside the build container.
  - In a live room shell, room storage may be visible at /data/<name>, but
    --room-source must still use the room subpath form /<name>.
  - The release context should already contain the application code,
    webserver.yaml, and Dockerfile/Containerfile.
  - This script builds and deploys a candidate tag like `contact-site:4.2-rc1`.
    Promotion to the plain stable tag `4.2` should happen only after verification.
  - The service YAML must describe an image-backed runtime. Candidate/release
    deploys must not keep running app code from a room-storage code mount.
EOF
}

fail() {
  echo "error: $*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "required command not found: $1"
}

assert_release_context_shape() {
  local service_path="$1"

  grep -Eq '^[[:space:]]*image:[[:space:]]*' "$service_path" \
    || fail "service file must contain an image: field or __IMAGE_TAG__ placeholder"

  if grep -Eq '^[[:space:]]*subpath:[[:space:]]*/' "$service_path"; then
    fail "service file still contains a room-storage subpath mount; candidate/release runtimes must keep app code in the image"
  fi

  if grep -Fq 'meshagent webserver join' "$service_path" && ! grep -Fq 'webserver.yaml' "$service_path"; then
    fail "service file runs meshagent webserver join but does not reference webserver.yaml"
  fi
}

meshagent_args=()
room="${MESHAGENT_ROOM:-}"
room_source=""
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
    --room-source)
      room_source="${2:-}"
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
[[ -n "$room_source" ]] || fail "--room-source is required"
[[ -n "$service_file" ]] || fail "--service-file is required"
[[ -n "$image_repo" ]] || fail "--image-repo is required"
[[ -n "$release_line" ]] || fail "--release is required"
[[ -n "$rc_number" ]] || fail "--rc is required"
[[ -f "$service_file" ]] || fail "service file not found: $service_file"
[[ "$room_source" == /* ]] || fail "--room-source must be an absolute room-storage path"
[[ "$mount_target" == /* ]] || fail "--mount-target must be an absolute path"
[[ "$room_source" != /data/* ]] || fail "--room-source must be a room subpath like /contact-david-site, not a shell mount path under /data"

assert_release_context_shape "$service_file"

candidate_tag="${image_repo}:${release_line}-rc${rc_number}"
dockerfile_path="${mount_target}/${dockerfile_name}"
tmp_service="$(mktemp "${TMPDIR:-/tmp}/meshagent-service.XXXXXX.yaml")"
cleanup() {
  rm -f "$tmp_service"
}
trap cleanup EXIT

echo "Building candidate image: ${candidate_tag}"
meshagent room container image build \
  "${meshagent_args[@]}" \
  --room "$room" \
  --tag "$candidate_tag" \
  --mount-room-path "${room_source}:${mount_target}:ro" \
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

Next steps:
  1. Verify service health and the real user-facing surface.
  2. If the candidate passes, promote the exact image to the plain stable tag:
       ${image_repo}:${release_line}
  3. If the user later asks for rollback, roll back to the previous plain stable tag,
     not to a release-candidate tag.
EOF
