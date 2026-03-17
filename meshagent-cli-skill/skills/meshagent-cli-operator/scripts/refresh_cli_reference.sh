#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUTPUT_PATH="${SKILL_DIR}/references/meshagent_cli_help.md"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python)"
else
  echo "python or python3 is required to regenerate MeshAgent CLI help" >&2
  exit 1
fi

TMP_FILE="$(mktemp)"
trap 'rm -f "${TMP_FILE}"' EXIT

"${PYTHON_BIN}" -m typer meshagent.cli.cli utils docs --name meshagent \
  | sed 's/{/\\&#123;/g; s/}/\\&#125;/g' \
  > "${TMP_FILE}"

{
  printf '%s\n' '# MeshAgent CLI Help' ''
  printf '%s\n' '_Generated from the installed MeshAgent CLI environment using `scripts/refresh_cli_reference.sh`._' ''
  cat "${TMP_FILE}"
} > "${OUTPUT_PATH}"

echo "Wrote ${OUTPUT_PATH}"
