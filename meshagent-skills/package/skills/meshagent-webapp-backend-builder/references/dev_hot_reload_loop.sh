#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Run the preferred Python-handler dev loop for a room-hosted webserver.

Usage:
  dev_hot_reload_loop.sh \
    --room-source /contact-site \
    --agent-name contact-site-dev

Required:
  --room-source PATH   Room-storage subpath for the site source, for example
                       /contact-site. In the live room shell this is expected
                       to be visible under /data/contact-site.
  --agent-name NAME    Agent identity to use for the dev runtime.

Optional:
  --room NAME          Room name. Defaults to $MESHAGENT_ROOM.
  --routes-file NAME   Routes file under the site root. Default: webserver.yaml
  --host HOST          Explicit bind host passed to meshagent webserver join.
  --port PORT          Explicit bind port passed to meshagent webserver join.

Notes:
  - This is the preferred dev loop for Python handlers because it uses
    `meshagent webserver join --watch`.
  - It is intended for live-room development, not release candidates.
  - It reads source from the room-storage mount under /data and reloads route
    and handler changes as files change.
EOF
}

fail() {
  echo "error: $*" >&2
  exit 1
}

room="${MESHAGENT_ROOM:-}"
room_source=""
agent_name=""
routes_file="webserver.yaml"
host=""
port=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --room)
      room="${2:-}"
      shift 2
      ;;
    --room-source)
      room_source="${2:-}"
      shift 2
      ;;
    --agent-name)
      agent_name="${2:-}"
      shift 2
      ;;
    --routes-file)
      routes_file="${2:-}"
      shift 2
      ;;
    --host)
      host="${2:-}"
      shift 2
      ;;
    --port)
      port="${2:-}"
      shift 2
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

command -v meshagent >/dev/null 2>&1 || fail "required command not found: meshagent"

[[ -n "$room" ]] || fail "--room is required unless MESHAGENT_ROOM is already set"
[[ -n "$room_source" ]] || fail "--room-source is required"
[[ -n "$agent_name" ]] || fail "--agent-name is required"
[[ "$room_source" == /* ]] || fail "--room-source must be a room subpath like /contact-site"
[[ "$room_source" != /data/* ]] || fail "--room-source must be a room subpath like /contact-site, not /data/contact-site"

site_root="/data${room_source}"
routes_path="${site_root}/${routes_file}"

[[ -d /data ]] || fail "this script expects room storage to be mounted at /data in the current shell"
[[ -d "$site_root" ]] || fail "site source directory not found under /data: $site_root"
[[ -f "$routes_path" ]] || fail "routes file not found: $routes_path"

cmd=(
  meshagent webserver join
  --room "$room"
  --agent-name "$agent_name"
  -f "$routes_path"
  --app-dir "$site_root"
  --watch
)

if [[ -n "$host" ]]; then
  cmd+=(--host "$host")
fi
if [[ -n "$port" ]]; then
  cmd+=(--port "$port")
fi

echo "Starting hot-reload dev loop from: $site_root"
echo "Command: ${cmd[*]}"
exec "${cmd[@]}"
