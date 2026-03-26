#!/usr/bin/env python3
"""Audit meshagent command references in the packaged skills against the live CLI tree."""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BIN = Path("meshagent")
SKILLS_DIR = SKILLS_ROOT / "skills"
COMMANDS_DIR = SKILLS_ROOT / "commands"
INLINE_COMMAND_PATTERN = re.compile(r"`(?P<command>\$?\s*meshagent[^`\n]*)`")
COMMAND_WORD_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
EXCLUDED_PATHS = {
    SKILLS_DIR / "meshagent-cli-operator" / "references" / "meshagent_cli_help.md",
}


@dataclass(frozen=True)
class CommandReference:
    file_path: Path
    line_number: int
    text: str


@dataclass(frozen=True)
class AuditIssue:
    severity: str
    file_path: Path
    line_number: int
    command: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit meshagent command references in packaged skills."
    )
    parser.add_argument(
        "--meshagent-bin",
        default=str(DEFAULT_BIN),
        help=f"Path to meshagent CLI. Default: {DEFAULT_BIN}",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=4,
        help="Maximum command depth to crawl from the root. Default: 4",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=2,
        help="Per-command help timeout in seconds. Default: 2",
    )
    return parser.parse_args()


def parse_commands(help_text: str) -> list[str]:
    commands: list[str] = []
    in_commands = False
    for line in help_text.splitlines():
        if re.match(r"^╭─ Commands ", line):
            in_commands = True
            continue
        if in_commands and line.startswith("╰"):
            in_commands = False
            continue
        if not in_commands:
            continue
        stripped = line.strip()
        if not stripped.startswith("│"):
            continue
        inner = stripped.strip("│").strip()
        if not inner:
            continue
        name = inner.split()[0]
        if COMMAND_WORD_PATTERN.match(name):
            commands.append(name)
    return commands


def run_help(
    *,
    meshagent_bin: str,
    path: tuple[str, ...],
    timeout_seconds: int,
) -> str:
    cmd = [meshagent_bin, *path, "--help"]
    completed = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
    if completed.returncode != 0:
        output = completed.stdout or completed.stderr
        raise RuntimeError(
            f"help command failed for {' '.join(cmd)}: {output.strip() or completed.returncode}"
        )
    return completed.stdout


class CliHelpCache:
    def __init__(self, *, meshagent_bin: str, timeout_seconds: int, max_depth: int):
        self._meshagent_bin = meshagent_bin
        self._timeout_seconds = timeout_seconds
        self._max_depth = max_depth
        self._children_by_path: dict[tuple[str, ...], set[str]] = {}

    def children(self, path: tuple[str, ...]) -> set[str]:
        if len(path) > self._max_depth:
            return set()
        cached = self._children_by_path.get(path)
        if cached is not None:
            return cached
        help_text = run_help(
            meshagent_bin=self._meshagent_bin,
            path=path,
            timeout_seconds=self._timeout_seconds,
        )
        children = set(parse_commands(help_text))
        self._children_by_path[path] = children
        return children


def iter_audit_files() -> list[Path]:
    files: list[Path] = []
    files.extend(sorted(SKILLS_DIR.glob("*/SKILL.md")))
    files.extend(sorted(SKILLS_DIR.glob("*/references/**/*.md")))
    files.extend(sorted(SKILLS_DIR.glob("_shared/references/**/*.md")))
    files.extend(sorted(COMMANDS_DIR.glob("*.md")))
    return [path for path in files if path not in EXCLUDED_PATHS]


def extract_command_references(path: Path) -> list[CommandReference]:
    references: list[CommandReference] = []
    seen: set[tuple[int, str]] = set()

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        for match in INLINE_COMMAND_PATTERN.finditer(line):
            command = match.group("command").strip()
            key = (line_number, command)
            if key not in seen:
                seen.add(key)
                references.append(
                    CommandReference(
                        file_path=path,
                        line_number=line_number,
                        text=command,
                    )
                )

        stripped = line.strip()
        for prefix in ("$ meshagent ", "meshagent "):
            if stripped.startswith(prefix):
                key = (line_number, stripped)
                if key in seen:
                    continue
                seen.add(key)
                references.append(
                    CommandReference(
                        file_path=path,
                        line_number=line_number,
                        text=stripped,
                    )
                )
                break

    return references


def parse_command_tokens(command: str) -> list[str] | None:
    normalized = command.strip()
    if normalized.startswith("$"):
        normalized = normalized[1:].strip()
    try:
        tokens = shlex.split(normalized)
    except ValueError:
        return None
    if not tokens or tokens[0] != "meshagent":
        return None
    return tokens


def audit_reference(
    *,
    reference: CommandReference,
    cli_help: CliHelpCache,
) -> list[AuditIssue]:
    tokens = parse_command_tokens(reference.text)
    if tokens is None:
        return []

    issues: list[AuditIssue] = []
    current: tuple[str, ...] = ()

    for token in tokens[1:]:
        if token.startswith("-"):
            break
        if not COMMAND_WORD_PATTERN.match(token):
            break

        children = cli_help.children(current)
        if token in children:
            current = (*current, token)
            continue

        severity = "error" if children else "warning"
        if current:
            message = f"unrecognized command noun '{token}' after `meshagent {' '.join(current)}`"
        else:
            message = f"unrecognized top-level command noun '{token}'"

        issues.append(
            AuditIssue(
                severity=severity,
                file_path=reference.file_path,
                line_number=reference.line_number,
                command=reference.text,
                message=message,
            )
        )
        break

    return issues


def main() -> int:
    args = parse_args()
    meshagent_bin = args.meshagent_bin

    if "/" in meshagent_bin:
        meshagent_path = Path(meshagent_bin).resolve()
        meshagent_bin = str(meshagent_path)
        if not meshagent_path.is_file():
            print(f"meshagent CLI not found: {meshagent_path}", file=sys.stderr)
            return 1

    audit_files = iter_audit_files()
    references: list[CommandReference] = []
    for path in audit_files:
        references.extend(extract_command_references(path))

    cli_help = CliHelpCache(
        meshagent_bin=meshagent_bin,
        timeout_seconds=args.timeout_seconds,
        max_depth=args.max_depth,
    )
    issues: list[AuditIssue] = []
    for reference in references:
        issues.extend(audit_reference(reference=reference, cli_help=cli_help))

    if issues:
        for issue in issues:
            print(
                f"{issue.severity.upper()}: {issue.file_path}:{issue.line_number}: "
                f"{issue.message} in `{issue.command}`",
                file=sys.stderr,
            )
        return 1

    print(
        "Audited "
        f"{len(references)} meshagent command references across {len(audit_files)} files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
