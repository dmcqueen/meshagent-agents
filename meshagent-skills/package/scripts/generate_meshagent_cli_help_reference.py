#!/usr/bin/env python3
"""Generate the packaged MeshAgent CLI help reference from an installed meshagent binary."""

import argparse
import json
import re
import subprocess
import sys
from collections import deque
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BIN = Path("meshagent")
DEFAULT_COMPAT = SKILLS_ROOT / "compat.json"
DEFAULT_OUTPUT = (
    SKILLS_ROOT
    / "skills"
    / "meshagent-cli-operator"
    / "references"
    / "meshagent_cli_help.md"
)
DEFAULT_DISPLAY_BIN = "meshagent"
SKILLS_DIR = SKILLS_ROOT / "skills"
COMMANDS_DIR = SKILLS_ROOT / "commands"
EXCLUDED_REFERENCE_PATHS = {
    SKILLS_DIR / "meshagent-cli-operator" / "references" / "meshagent_cli_help.md",
}
INLINE_COMMAND_PATTERN = re.compile(r"`(?P<command>\$?\s*meshagent[^`\n]*)`")
COMMAND_WORD_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the packaged MeshAgent CLI help reference."
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


def load_cli_version(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    version = payload.get("meshagent_cli_version")
    if not isinstance(version, str) or not version.strip():
        raise ValueError(f"meshagent_cli_version missing in {path}")
    return version.strip()


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
        if name.startswith("-"):
            continue
        commands.append(name)
    return commands


def iter_reference_files() -> list[Path]:
    files: list[Path] = []
    files.extend(sorted(SKILLS_DIR.glob("*/SKILL.md")))
    files.extend(sorted(SKILLS_DIR.glob("*/references/**/*.md")))
    files.extend(sorted(SKILLS_DIR.glob("_shared/references/**/*.md")))
    files.extend(sorted(COMMANDS_DIR.glob("*.md")))
    return [path for path in files if path not in EXCLUDED_REFERENCE_PATHS]


def extract_referenced_command_paths() -> set[tuple[str, ...]]:
    paths: set[tuple[str, ...]] = set()

    for path in iter_reference_files():
        for line in path.read_text(encoding="utf-8").splitlines():
            for match in INLINE_COMMAND_PATTERN.finditer(line):
                referenced = match.group("command").strip()
                parsed = parse_command_path(referenced)
                if parsed:
                    paths.add(parsed)

            stripped = line.strip()
            if stripped.startswith("$ meshagent ") or stripped.startswith("meshagent "):
                parsed = parse_command_path(stripped)
                if parsed:
                    paths.add(parsed)

    return paths


def parse_command_path(command: str) -> tuple[str, ...] | None:
    normalized = command.strip()
    if normalized.startswith("$"):
        normalized = normalized[1:].strip()
    tokens = normalized.split()
    if not tokens or tokens[0] != "meshagent":
        return None

    path: list[str] = []
    for token in tokens[1:]:
        if token.startswith("-"):
            break
        if not COMMAND_WORD_PATTERN.match(token):
            break
        path.append(token)

    return tuple(path) if path else None


def run_help(
    meshagent_bin: str, path: list[str], timeout_seconds: int
) -> tuple[int, str, bool]:
    cmd = [meshagent_bin] + path + ["--help"]
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        output = completed.stdout if completed.stdout else completed.stderr
        return completed.returncode, output.rstrip(), False
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or "") or (exc.stderr or "")
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        output = output.rstrip()
        return 124, output, True


def sanitize_help_output(*, output: str, meshagent_bin: str, display_bin: str) -> str:
    workspace_root = str(Path.cwd().resolve())
    if workspace_root:
        output = output.replace(workspace_root, "<workspace>")
    if "/" in meshagent_bin:
        resolved_bin = str(Path(meshagent_bin).resolve())
        output = output.replace(meshagent_bin, display_bin)
        output = output.replace(resolved_bin, display_bin)
    return output


def heading_for(path: list[str]) -> str:
    level = 2 + max(len(path) - 1, 0)
    hashes = "#" * min(level, 6)
    command = "meshagent" if not path else "meshagent " + " ".join(path)
    return f"{hashes} `{command}`"


def render_reference(
    meshagent_bin: str,
    display_bin: str,
    cli_version: str,
    max_depth: int,
    timeout_seconds: int,
) -> str:
    referenced_paths = extract_referenced_command_paths()
    queue: deque[list[str]] = deque([[]])
    for path in sorted(referenced_paths):
        queue.append(list(path))
    seen: set[tuple[str, ...]] = set()
    sections: list[str] = []

    while queue:
        path = queue.popleft()
        key = tuple(path)
        if key in seen:
            continue
        seen.add(key)

        returncode, output, timed_out = run_help(meshagent_bin, path, timeout_seconds)
        output = sanitize_help_output(
            output=output,
            meshagent_bin=meshagent_bin,
            display_bin=display_bin,
        )
        sections.append(heading_for(path))
        sections.append("")
        cmd = "$ " + " ".join([display_bin] + path + ["--help"])
        sections.append("```console")
        sections.append(cmd)
        if output:
            sections.append(output)
        sections.append("```")
        if returncode != 0:
            status = "timed out" if timed_out else f"exited with code {returncode}"
            sections.append("")
            sections.append(f"_Help capture {status} for this command path._")
            sections.append("")
            continue
        sections.append("")

        if len(path) >= max_depth:
            continue

        for command in parse_commands(output):
            queue.append(path + [command])

    lines = [
        "# MeshAgent CLI Help",
        "",
        f"_Packaged CLI help reference for MeshAgent CLI `{cli_version}`._",
        "",
        (
            f"_Generated from the installed `meshagent` binary with recursive `--help` capture "
            f"up to depth {max_depth} and timeout {timeout_seconds}s per command._"
        ),
        "",
    ]
    lines.extend(sections)
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    compat_path = Path(args.compat_json).resolve()
    output_path = Path(args.output).resolve()
    meshagent_bin = args.meshagent_bin

    if "/" in meshagent_bin:
        meshagent_path = Path(meshagent_bin).resolve()
        meshagent_bin = str(meshagent_path)
        if not meshagent_path.is_file():
            print(f"meshagent CLI not found: {meshagent_path}", file=sys.stderr)
            return 1

    cli_version = load_cli_version(compat_path)
    rendered = render_reference(
        meshagent_bin=meshagent_bin,
        display_bin=args.display_bin,
        cli_version=cli_version,
        max_depth=args.max_depth,
        timeout_seconds=args.timeout_seconds,
    )
    output_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
