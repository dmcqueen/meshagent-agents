#!/usr/bin/env python3
"""Update compat.json, regenerate CLI help, and validate the meshagent-skills package."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BIN = Path("meshagent")
DEFAULT_COMPAT = SKILLS_ROOT / "compat.json"
DEFAULT_SYNC_SCRIPT = (
    SKILLS_ROOT / "scripts" / "generate_meshagent_cli_help_reference.py"
)
DEFAULT_VALIDATE_SCRIPT = (
    SKILLS_ROOT / "scripts" / "validate_meshagent_skills_package.py"
)
DEFAULT_OUTPUT = (
    SKILLS_ROOT
    / "skills"
    / "meshagent-cli-operator"
    / "references"
    / "meshagent_cli_help.md"
)
DEFAULT_DISPLAY_BIN = "meshagent"


def log(message: str) -> None:
    print(f"[meshagent-skills] {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh meshagent-skills for the installed MeshAgent CLI."
    )
    parser.add_argument(
        "--meshagent-bin",
        default=str(DEFAULT_BIN),
        help=f"Path to meshagent CLI. Default: {DEFAULT_BIN}",
    )
    parser.add_argument(
        "--compat-json",
        default=str(DEFAULT_COMPAT),
        help=f"Path to compat.json. Default: {DEFAULT_COMPAT}",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help=f"Path to meshagent_cli_help.md. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--display-bin",
        default=DEFAULT_DISPLAY_BIN,
        help=f"Command label to render in console examples. Default: {DEFAULT_DISPLAY_BIN}",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=1,
        help="Maximum command depth to crawl from the root. Default: 1",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=2,
        help="Per-command help timeout in seconds. Default: 2",
    )
    return parser.parse_args()


def resolve_meshagent_bin(meshagent_bin: str) -> str:
    if "/" not in meshagent_bin:
        return meshagent_bin

    meshagent_path = Path(meshagent_bin).resolve()
    if not meshagent_path.is_file():
        raise FileNotFoundError(f"meshagent CLI not found: {meshagent_path}")
    return str(meshagent_path)


def run_checked(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    log("running: " + " ".join(cmd))
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.stdout:
        sys.stdout.write(completed.stdout)
    if completed.returncode != 0:
        if completed.stderr:
            sys.stderr.write(completed.stderr)
        raise subprocess.CalledProcessError(
            completed.returncode,
            cmd,
            output=completed.stdout,
            stderr=completed.stderr,
        )
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    return completed


def detect_cli_version(meshagent_bin: str) -> str:
    completed = run_checked([meshagent_bin, "version"])
    version = completed.stdout.strip()
    if not version:
        raise ValueError("meshagent version returned an empty version string")
    return version


def load_compat_version(path: Path) -> str | None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    version = payload.get("meshagent_cli_version")
    return version.strip() if isinstance(version, str) and version.strip() else None


def update_compat_json(path: Path, cli_version: str) -> bool:
    payload = json.loads(path.read_text(encoding="utf-8"))
    current_version = payload.get("meshagent_cli_version")
    if current_version == cli_version:
        return False
    payload["meshagent_cli_version"] = cli_version
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return True


def main() -> int:
    args = parse_args()
    compat_path = Path(args.compat_json).resolve()
    output_path = Path(args.output).resolve()
    sync_script = DEFAULT_SYNC_SCRIPT.resolve()
    validate_script = DEFAULT_VALIDATE_SCRIPT.resolve()

    try:
        log("resolving meshagent binary")
        meshagent_bin = resolve_meshagent_bin(args.meshagent_bin)
        log(f"using meshagent binary: {meshagent_bin}")

        log("detecting installed MeshAgent CLI version")
        cli_version = detect_cli_version(meshagent_bin)
        log(f"detected MeshAgent CLI version: {cli_version}")

        current_compat_version = load_compat_version(compat_path)
        if current_compat_version == cli_version:
            log(
                f"compat.json already matches installed CLI version: {current_compat_version}"
            )
        else:
            log(f"updating compat.json: {compat_path}")
            update_compat_json(compat_path, cli_version)
            log("compat.json updated")

        log(f"regenerating CLI help reference: {output_path}")
        run_checked(
            [
                sys.executable,
                str(sync_script),
                "--meshagent-bin",
                meshagent_bin,
                "--compat-json",
                str(compat_path),
                "--output",
                str(output_path),
                "--display-bin",
                args.display_bin,
                "--max-depth",
                str(args.max_depth),
                "--timeout-seconds",
                str(args.timeout_seconds),
            ]
        )
        log("CLI help reference regenerated")

        log("running meshagent-skills validator")
        run_checked(
            [
                sys.executable,
                str(validate_script),
                "--meshagent-bin",
                meshagent_bin,
                "--compat-json",
                str(compat_path),
            ]
        )
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as exc:
        if isinstance(exc, (FileNotFoundError, ValueError)):
            print(str(exc), file=sys.stderr)
        return 1

    log(f"updated meshagent-skills for MeshAgent CLI {cli_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
