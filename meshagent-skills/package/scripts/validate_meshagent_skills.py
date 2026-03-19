#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BIN = Path("meshagent")
DEFAULT_COMPAT = SKILLS_ROOT / "compat.json"
DEFAULT_README = SKILLS_ROOT / "README.md"
DEFAULT_PLUGIN = SKILLS_ROOT / ".claude-plugin" / "plugin.json"
DEFAULT_SKILL = SKILLS_ROOT / "skills" / "meshagent-cli-operator" / "SKILL.md"
DEFAULT_COMMAND_GROUPS = (
    SKILLS_ROOT
    / "skills"
    / "meshagent-cli-operator"
    / "references"
    / "command_groups.md"
)
DEFAULT_HELP = (
    SKILLS_ROOT
    / "skills"
    / "meshagent-cli-operator"
    / "references"
    / "meshagent_cli_help.md"
)
SPECIALIZED_SKILLS = {
    "meshagent-mail-operator": SKILLS_ROOT
    / "skills"
    / "meshagent-mail-operator"
    / "SKILL.md",
    "meshagent-scheduling-operator": SKILLS_ROOT
    / "skills"
    / "meshagent-scheduling-operator"
    / "SKILL.md",
    "meshagent-webmaster-operator": SKILLS_ROOT
    / "skills"
    / "meshagent-webmaster-operator"
    / "SKILL.md",
}
SHARED_RUNTIME_LINE = "Use the room runtime defined in `../meshagent-cli-operator/SKILL.md`."
SHARED_RUNTIME_DUPLICATES = (
    "The MeshAgent CLI is expected at `/usr/bin/meshagent`",
    "The current room is `MESHAGENT_ROOM`.",
    "The writable user-visible workspace is `/data`.",
    "The default public MeshAgent domain in this environment is `__MESHAGENT_PUBLIC_DOMAIN__`.",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate meshagent-skills consistency.")
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
    return parser.parse_args()


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_top_level_commands(help_text: str) -> set[str]:
    commands: set[str] = set()
    in_commands = False
    for line in help_text.splitlines():
        if re.match(r"^╭─ Commands ", line):
            in_commands = True
            continue
        if in_commands and line.startswith("╰"):
            break
        if not in_commands:
            continue
        stripped = line.strip()
        if not stripped.startswith("│"):
            continue
        inner = stripped.strip("│").strip()
        if not inner:
            continue
        commands.add(inner.split()[0])
    return commands


def referenced_top_level_commands(command_groups_text: str) -> set[str]:
    refs: set[str] = set()
    for match in re.finditer(r"`meshagent ([a-z0-9-]+)", command_groups_text):
        refs.add(match.group(1))
    return refs


def main() -> int:
    args = parse_args()
    meshagent_bin = args.meshagent_bin
    compat_path = Path(args.compat_json).resolve()

    if "/" in meshagent_bin:
        meshagent_path = Path(meshagent_bin).resolve()
        meshagent_bin = str(meshagent_path)
        if not meshagent_path.is_file():
            print(f"meshagent CLI not found: {meshagent_path}", file=sys.stderr)
            return 1

    compat = json.loads(compat_path.read_text(encoding="utf-8"))
    expected_version = compat.get("meshagent_cli_version")
    if not isinstance(expected_version, str) or not expected_version.strip():
        print("compat.json is missing meshagent_cli_version", file=sys.stderr)
        return 1
    expected_version = expected_version.strip()

    version_proc = subprocess.run(
        [meshagent_bin, "version"], capture_output=True, text=True
    )
    if version_proc.returncode != 0:
        print(version_proc.stderr or version_proc.stdout, file=sys.stderr)
        return 1
    actual_version = version_proc.stdout.strip()

    help_proc = subprocess.run(
        [meshagent_bin, "--help"], capture_output=True, text=True
    )
    if help_proc.returncode != 0:
        print(help_proc.stderr or help_proc.stdout, file=sys.stderr)
        return 1

    top_level = parse_top_level_commands(help_proc.stdout)
    command_groups_text = load_text(DEFAULT_COMMAND_GROUPS)
    referenced = referenced_top_level_commands(command_groups_text)
    missing = sorted(cmd for cmd in referenced if cmd not in top_level)

    readme_text = load_text(DEFAULT_README)
    plugin_text = load_text(DEFAULT_PLUGIN)
    skill_text = load_text(DEFAULT_SKILL)
    help_text = load_text(DEFAULT_HELP)

    errors: list[str] = []
    if actual_version != expected_version:
        errors.append(
            f"compat.json expects MeshAgent CLI {expected_version}, but installed version is {actual_version}"
        )
    if "compat.json" not in readme_text:
        errors.append("README.md does not reference compat.json")
    if "compat.json" not in skill_text:
        errors.append("SKILL.md does not reference compat.json")
    if "compat.json" not in command_groups_text:
        errors.append("command_groups.md does not reference compat.json")
    if expected_version not in help_text:
        errors.append(
            f"meshagent_cli_help.md does not mention MeshAgent CLI {expected_version}"
        )
    if "$ meshagent --help" not in help_text:
        errors.append("meshagent_cli_help.md should render console examples with `meshagent`")
    if "/.venv/bin/meshagent" in help_text:
        errors.append("meshagent_cli_help.md should not embed repo-local meshagent paths")
    if "MeshAgent CLI skill pack" not in plugin_text:
        errors.append("plugin.json description does not match the expected package label")
    if missing:
        errors.append(
            "command_groups.md references commands not present in meshagent --help: "
            + ", ".join(missing)
        )
    for skill_name, skill_path in SPECIALIZED_SKILLS.items():
        specialized_text = load_text(skill_path)
        if SHARED_RUNTIME_LINE not in specialized_text:
            errors.append(f"{skill_name} does not use the shared runtime reference")
        for duplicate_line in SHARED_RUNTIME_DUPLICATES:
            if duplicate_line in specialized_text:
                errors.append(
                    f"{skill_name} duplicates shared runtime detail: {duplicate_line}"
                )

    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated meshagent-skills against MeshAgent CLI {expected_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
