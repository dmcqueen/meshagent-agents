#!/usr/bin/env python3
"""Validate that the packaged meshagent-skills files stay in sync with the target CLI."""

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
SKILLS_DIR = SKILLS_ROOT / "skills"
SKILL_REFERENCE_PATH_PATTERN = re.compile(r"\.\./meshagent-[^/\s]+/SKILL\.md")
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
NAME_PATTERN = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)
RELATIVE_RESOURCE_PATTERN = re.compile(
    r"(?P<path>(?:\.\./|references/)[A-Za-z0-9_./-]+\.(?:md|yaml|py))"
)
QUOTED_STRING_PATTERN = re.compile(r'^(?P<quote>["\'])(?P<value>.*)(?P=quote)$')
WORKFLOW_METADATA_PATTERN = re.compile(r"^  workflow:\s*$", re.MULTILINE)
WORKFLOW_SECTION_PATTERN = re.compile(r"^## Workflow accountability\s*$", re.MULTILINE)
EXPECTED_PLUGIN_DESCRIPTION = (
    "MeshAgent operator skill pack for CLI routing, room operations, runtime "
    "debugging, queues, services, storage, databases, memory, scheduling, and "
    "room-hosted web workflows."
)
WORKFLOW_REFERENCE_PATH = "../_shared/references/workflow_accountability.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate meshagent-skills consistency."
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
    return parser.parse_args()


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def discover_skill_files() -> dict[str, Path]:
    discovered: dict[str, Path] = {}
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        if skill_md.parent.name == "_shared":
            continue
        text = load_text(skill_md)
        frontmatter_match = FRONTMATTER_PATTERN.match(text)
        if frontmatter_match is None:
            raise ValueError(f"{skill_md} is missing YAML frontmatter")
        name_match = NAME_PATTERN.search(frontmatter_match.group(1))
        if name_match is None:
            raise ValueError(f"{skill_md} is missing frontmatter name")
        skill_name = name_match.group(1).strip().strip('"').strip("'")
        if not skill_name:
            raise ValueError(f"{skill_md} has an empty frontmatter name")
        discovered[skill_name] = skill_md
    return discovered


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


def parse_scalar_string(raw_value: str, field_name: str, source_path: Path) -> str:
    value = raw_value.strip()
    match = QUOTED_STRING_PATTERN.match(value)
    if match is not None:
        return match.group("value")
    if value and not value.startswith(("[", "{")):
        return value
    raise ValueError(f"{source_path} has an invalid string value for {field_name}")


def parse_openai_interface(openai_path: Path) -> dict[str, str]:
    lines = openai_path.read_text(encoding="utf-8").splitlines()
    interface_started = False
    interface_fields: dict[str, str] = {}

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not interface_started:
            if line != "interface:":
                raise ValueError(
                    f"{openai_path}:{line_number} must start with a top-level interface: mapping"
                )
            interface_started = True
            continue
        if not line.startswith("  "):
            raise ValueError(
                f"{openai_path}:{line_number} has unexpected top-level content outside interface"
            )
        if ":" not in stripped:
            raise ValueError(
                f"{openai_path}:{line_number} must define a key/value pair under interface"
            )
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        if key in interface_fields:
            raise ValueError(
                f"{openai_path}:{line_number} duplicates interface key {key}"
            )
        interface_fields[key] = parse_scalar_string(raw_value, key, openai_path)

    if not interface_started:
        raise ValueError(f"{openai_path} is missing top-level interface:")
    return interface_fields


def validate_openai_yaml(skill_name: str, skill_dir: Path, errors: list[str]) -> None:
    openai_path = skill_dir / "agents" / "openai.yaml"
    if not openai_path.is_file():
        errors.append(f"{skill_name} is missing agents/openai.yaml")
        return

    try:
        interface_fields = parse_openai_interface(openai_path)
    except ValueError as exc:
        errors.append(str(exc))
        return

    required_fields = ("display_name", "short_description", "default_prompt")
    for field in required_fields:
        value = interface_fields.get(field)
        if not value:
            errors.append(
                f"{skill_name} agents/openai.yaml is missing interface.{field}"
            )

    expected_prompt_token = f"${skill_name}"
    default_prompt = interface_fields.get("default_prompt", "")
    if expected_prompt_token not in default_prompt:
        errors.append(
            f"{skill_name} agents/openai.yaml default_prompt must mention {expected_prompt_token}"
        )


def validate_relative_resources(
    skill_name: str, skill_path: Path, skill_text: str, errors: list[str]
) -> None:
    for match in RELATIVE_RESOURCE_PATTERN.finditer(skill_text):
        relative_path = match.group("path")
        target_path = (skill_path.parent / relative_path).resolve()
        if not target_path.is_file():
            errors.append(
                f"{skill_name} references missing packaged resource {relative_path}"
            )


def validate_workflow_contract(
    skill_name: str, skill_text: str, errors: list[str]
) -> None:
    frontmatter_match = FRONTMATTER_PATTERN.match(skill_text)
    if frontmatter_match is None:
        errors.append(f"{skill_name} is missing YAML frontmatter")
        return

    frontmatter_text = frontmatter_match.group(1)
    required_frontmatter_fields = (
        "  workflow:",
        "    can_be_owner:",
        "    handoff_policy:",
        "    completion_gates:",
        "    evidence:",
    )
    if WORKFLOW_METADATA_PATTERN.search(frontmatter_text) is None:
        errors.append(f"{skill_name} is missing metadata.workflow")
    for field in required_frontmatter_fields[1:]:
        if field not in frontmatter_text:
            errors.append(f"{skill_name} metadata.workflow is missing {field.strip()}")

    if WORKFLOW_SECTION_PATTERN.search(skill_text) is None:
        errors.append(f"{skill_name} is missing a '## Workflow accountability' section")
    if WORKFLOW_REFERENCE_PATH not in skill_text:
        errors.append(
            f"{skill_name} does not reference the shared workflow accountability contract"
        )


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
    skill_files = discover_skill_files()

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
        errors.append(
            "meshagent_cli_help.md should render console examples with `meshagent`"
        )
    if "/.venv/bin/meshagent" in help_text:
        errors.append(
            "meshagent_cli_help.md should not embed repo-local meshagent paths"
        )
    plugin = json.loads(plugin_text)
    plugin_description = plugin.get("description")
    if plugin_description != EXPECTED_PLUGIN_DESCRIPTION:
        errors.append(
            "plugin.json description does not match the expected package description"
        )
    if missing:
        errors.append(
            "command_groups.md references commands not present in meshagent --help: "
            + ", ".join(missing)
        )
    if (
        "Use `meshagent-webapp-builder` for websites, contact forms, `meshagent webserver ...`, or room-hosted web handlers."
        not in command_groups_text
    ):
        errors.append(
            "command_groups.md is missing the required webapp-builder routing rule for websites and meshagent webserver work"
        )
    if (
        "Use `meshagent-webmaster` for explicit route management or public hostname exposure."
        not in command_groups_text
    ):
        errors.append(
            "command_groups.md is missing the required webmaster routing rule for explicit route management"
        )
    for skill_name, skill_path in skill_files.items():
        current_skill_text = load_text(skill_path)
        if SKILL_REFERENCE_PATH_PATTERN.search(current_skill_text):
            errors.append(f"{skill_name} references another skill by relative path")
        validate_openai_yaml(skill_name, skill_path.parent, errors)
        validate_relative_resources(skill_name, skill_path, current_skill_text, errors)
        validate_workflow_contract(skill_name, current_skill_text, errors)

    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated meshagent-skills against MeshAgent CLI {expected_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
