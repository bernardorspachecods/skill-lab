#!/usr/bin/env python3
"""Audit a repository against the context-architecture conventions.

The auditor reports actionable findings and never edits the repository. It is
deliberately dependency-free so it can be copied or run from any repository.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence
from urllib.parse import unquote, urlsplit


DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".cache",
    ".next",
    ".nuxt",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "generated",
    "node_modules",
    "out",
    "target",
    "temp",
    "tmp",
    "vendor",
}

DOCUMENTATION_DIR_NAMES = {"docs", "documentation"}
CURRENT_STATE_FILENAME = "CURRENT-STATE.json"
CURRENT_STATE_KEYS = {"plan", "phase", "status"}
CURRENT_STATE_REQUIRED_KEYS = {"plan", "status"}
CURRENT_STATE_STATUSES = {"not_started", "in_progress", "blocked", "complete"}

PUBLIC_MARKDOWN_NAMES = {
    "README.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE.md",
}

MAP_HEADINGS = {
    "mapa de navegacao",
    "navigation map",
}

ROUTER_HEADER_GROUPS = (
    {
        "pedido",
        "request",
        "task",
        "tarefa",
        "necessidade",
        "tipo",
        "problema",
        "problem",
        "goal",
        "objetivo",
    },
    {
        "entrada",
        "area",
        "first",
        "open",
        "entry",
        "primeira",
        "start",
        "comecar",
        "where",
        "onde",
        "branch",
        "ramo",
    },
)

ROUTER_HEADINGS = {
    "task router",
    "work router",
    "router de trabalho",
    "router de tarefas",
}

MARKDOWN_LINK_RE = re.compile(
    r"!?\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+(?:\"[^\"]*\"|'[^']*'))?\)"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*$")
WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    path: str
    line: int | None
    title: str
    why: str
    suggestion: str


@dataclass(frozen=True)
class Heading:
    level: int
    text: str
    line: int
    anchor: str


@dataclass(frozen=True)
class Link:
    target: str
    line: int


class Auditor:
    def __init__(self, root: Path, args: argparse.Namespace) -> None:
        self.root = root.resolve()
        self.args = args
        self.exclude_patterns = list(args.exclude) + self.load_contextignore()
        self.findings: list[Finding] = []
        self._finding_keys: set[tuple[str, str, int | None, str]] = set()
        self.files = self._discover_files()
        self.context_files = {
            path for path in self.files if path.name == "CONTEXT.md"
        }
        self.current_state_files = {
            path for path in self.files if path.name == CURRENT_STATE_FILENAME
        }
        self._text_cache: dict[Path, str] = {}
        self._headings_cache: dict[Path, list[Heading]] = {}
        self.directories = self._discover_directories()
        self.markdown_files = {
            path
            for path in self.files
            if path.suffix.lower() in {".md", ".markdown"}
        }

    def run(self) -> list[Finding]:
        self.check_context_coverage()
        self.check_agents_links()
        self.check_root_router()
        self.check_current_state_files()
        self.check_navigation_maps()
        self.check_markdown_links()
        return self.findings

    def add(
        self,
        code: str,
        severity: str,
        path: Path,
        title: str,
        why: str,
        suggestion: str,
        line: int | None = None,
    ) -> None:
        key = (code, self.display_path(path), line, title)
        if key in self._finding_keys:
            return
        self._finding_keys.add(key)
        self.findings.append(
            Finding(
                code=code,
                severity=severity,
                path=self.display_path(path),
                line=line,
                title=title,
                why=why,
                suggestion=suggestion,
            )
        )

    def display_path(self, path: Path) -> str:
        try:
            relative = path.resolve().relative_to(self.root)
        except ValueError:
            return str(path)
        return "." if str(relative) == "." else relative.as_posix()

    def path_is_excluded(self, path: Path) -> bool:
        try:
            relative = path.resolve().relative_to(self.root)
        except ValueError:
            return True

        parts = relative.parts
        for part in parts:
            if part in DEFAULT_EXCLUDED_DIRS:
                return True

        relative_posix = PurePosixPath(*parts).as_posix() if parts else "."
        for pattern in self.exclude_patterns:
            normalized = pattern.strip("/")
            if not normalized:
                continue
            if relative_posix == normalized or relative_posix.startswith(normalized + "/"):
                return True
            if any(fnmatch.fnmatch(part, normalized) for part in parts):
                return True
            if fnmatch.fnmatch(relative_posix, normalized):
                return True
        return False

    def load_contextignore(self) -> list[str]:
        path = self.root / ".contextignore"
        if not path.is_file():
            return []
        patterns = []
        for line in path.read_text(encoding="utf-8").splitlines():
            pattern = line.strip()
            if pattern and not pattern.startswith("#"):
                patterns.append(pattern)
        return patterns

    def _discover_files(self) -> set[Path]:
        tracked = self._git_files()
        if tracked is not None:
            return {
                path
                for path in tracked
                if path.is_file() and not self.path_is_excluded(path)
            }

        files: set[Path] = set()
        for path in self.root.rglob("*"):
            if path.is_file() and not self.path_is_excluded(path):
                files.add(path.resolve())
        return files

    def _git_files(self) -> set[Path] | None:
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(self.root),
                    "ls-files",
                    "--cached",
                    "--others",
                    "--exclude-standard",
                    "-z",
                ],
                check=False,
                capture_output=True,
                text=False,
            )
        except OSError:
            return None
        if result.returncode != 0:
            return None
        paths = set()
        for raw_path in result.stdout.split(b"\0"):
            if raw_path:
                paths.add((self.root / raw_path.decode("utf-8")).resolve())
        return paths

    def _discover_directories(self) -> set[Path]:
        directories: set[Path] = {self.root}

        for directory in self._all_directories():
            if self.is_documentation_directory(directory):
                directories.add(directory)

        if self.args.require_context:
            for directory in self._all_directories():
                if self.matches_any_pattern(directory, self.args.require_context):
                    directories.add(directory)

        return directories

    def is_documentation_directory(self, path: Path) -> bool:
        return path.name.lower() in DOCUMENTATION_DIR_NAMES

    def _all_directories(self) -> set[Path]:
        directories: set[Path] = {self.root}
        for file_path in self.files:
            current = file_path.parent
            while True:
                if self.path_is_excluded(current):
                    break
                directories.add(current)
                if current == self.root:
                    break
                current = current.parent
        return directories

    def matches_any_pattern(self, path: Path, patterns: Sequence[str]) -> bool:
        try:
            relative = path.resolve().relative_to(self.root)
        except ValueError:
            return False
        relative_posix = PurePosixPath(*relative.parts).as_posix() if relative.parts else "."
        return any(
            fnmatch.fnmatch(relative_posix, pattern.strip("/"))
            or relative_posix == pattern.strip("/")
            for pattern in patterns
            if pattern.strip("/")
        )

    def read_text(self, path: Path) -> str:
        if path not in self._text_cache:
            try:
                self._text_cache[path] = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                self._text_cache[path] = path.read_text(
                    encoding="utf-8", errors="replace"
                )
        return self._text_cache[path]

    def lines(self, path: Path) -> list[str]:
        return self.read_text(path).splitlines()

    def check_context_coverage(self) -> None:
        root_context = self.root / "CONTEXT.md"
        if not root_context.is_file():
            self.add(
                "CTX001",
                "error",
                root_context,
                "Root CONTEXT.md is missing",
                "The repository has no canonical root map for orientation and task routing.",
                "Create CONTEXT.md at the repository root with direct destinations and the task-intent router.",
            )

        for directory in sorted(self.directories):
            if directory == self.root:
                continue
            context = directory / "CONTEXT.md"
            if context.is_file():
                continue
            self.add(
                "CTX002",
                "warning",
                directory,
                "CONTEXT.md is missing from a selected context boundary",
                "This directory is a documentation area or was explicitly selected for local context. Other directories inherit the nearest ancestor map and are not reported merely because they contain files.",
                "Create a local CONTEXT.md if this boundary has durable independent guidance; otherwise remove the explicit requirement or rename the directory if it is not a documentation area.",
            )

    def check_agents_links(self) -> None:
        agents_files = {path for path in self.files if path.name == "AGENTS.md"}
        for agents_path in sorted(agents_files):
            expected = self.nearest_context(agents_path.parent)
            if expected is None:
                self.add(
                    "AGT001",
                    "error",
                    agents_path,
                    "AGENTS.md cannot point to a context map",
                    "No CONTEXT.md exists in this scope or any parent scope.",
                    "Create the applicable CONTEXT.md, then add an explicit Markdown link to it near the beginning of AGENTS.md.",
                )
                continue

            links = self.links_in(agents_path)
            resolved_targets = {
                self.resolve_link_target(agents_path, link.target)[0]
                for link in links
                if self.resolve_link_target(agents_path, link.target)[0] is not None
            }
            if expected not in resolved_targets:
                self.add(
                    "AGT001",
                    "error",
                    agents_path,
                    "AGENTS.md does not link to its applicable CONTEXT.md",
                    f"The applicable context map is {self.display_path(expected)}, but no explicit Markdown link to that file was found.",
                    f"Add a visible link to [{expected.name}]({self.relative_link(agents_path.parent, expected)}) near the beginning of AGENTS.md.",
                )

    def check_root_router(self) -> None:
        root_context = self.root / "CONTEXT.md"
        if not root_context.is_file():
            return

        lines = self.lines(root_context)
        tables = self.markdown_tables(lines)
        router_table = None
        explicit_router = any(
            self.is_router_heading(heading.text)
            for heading in self.headings(root_context)
        )
        for header, rows in tables:
            normalized_header = set().union(
                *(self.normalize_header_words(cell) for cell in header)
            )
            recognizable_headers = all(
                any(word in normalized_header for word in group)
                for group in ROUTER_HEADER_GROUPS
            )
            if recognizable_headers or explicit_router:
                router_table = (header, rows)
                break

        if router_table is None:
            self.add(
                "RTR001",
                "error",
                root_context,
                "Root task-intent router was not detected",
                "The root CONTEXT.md must contain a compact router that maps request types to a first area to open.",
                "Add a Markdown table with recognizable request/area headers, or place the table under an explicit heading such as ## Task router.",
            )
            return

        _, rows = router_table
        if not any(self.links_in_text("\n".join(row), 1) for row in rows):
            self.add(
                "RTR002",
                "warning",
                root_context,
                "Root task-intent router has no Markdown links",
                "A router without links cannot reliably take an agent to the first area of investigation.",
                "Link the first-area entries directly to the relevant CONTEXT.md files.",
            )

    def check_current_state_files(self) -> None:
        for path in sorted(self.current_state_files):
            try:
                value = json.loads(self.read_text(path))
            except json.JSONDecodeError as error:
                self.add(
                    "STATE001",
                    "error",
                    path,
                    "CURRENT-STATE.json is not valid JSON",
                    f"The JSON parser failed at line {error.lineno}, column {error.colno}.",
                    "Fix the JSON syntax before using the file as a resume pointer.",
                    line=error.lineno,
                )
                continue

            if not isinstance(value, dict):
                self.add(
                    "STATE002",
                    "error",
                    path,
                    "CURRENT-STATE.json must contain an object",
                    "The state contract is a small object with plan, status, and optional phase fields.",
                    "Replace the top-level value with a JSON object.",
                )
                continue

            keys = set(value)
            missing = CURRENT_STATE_REQUIRED_KEYS - keys
            extra = keys - CURRENT_STATE_KEYS
            if missing:
                self.add(
                    "STATE003",
                    "error",
                    path,
                    "CURRENT-STATE.json is missing required fields",
                    f"Required fields are: {', '.join(sorted(CURRENT_STATE_REQUIRED_KEYS))}.",
                    f"Add the missing field(s): {', '.join(sorted(missing))}.",
                )
            if extra:
                self.add(
                    "STATE004",
                    "error",
                    path,
                    "CURRENT-STATE.json contains unsupported fields",
                    f"The state contract allows only plan, status, and optional phase; found {', '.join(sorted(extra))}.",
                    "Move explanations, decisions, evidence, or next steps to the linked Markdown documents.",
                )

            plan = value.get("plan")
            if not isinstance(plan, str) or not plan.strip():
                self.add(
                    "STATE005",
                    "error",
                    path,
                    "CURRENT-STATE.json has an invalid plan field",
                    "The plan field must be a non-empty relative path to a Markdown plan.",
                    "Set plan to an existing relative .md or .markdown path.",
                )
            else:
                target, _ = self.resolve_link_target(path, plan)
                if target is None or not target.exists():
                    self.add(
                        "STATE006",
                        "error",
                        path,
                        "CURRENT-STATE.json points to a missing plan",
                        f"The plan path {plan!r} does not resolve from {self.display_path(path)}.",
                        "Update plan to point to an existing Markdown plan.",
                    )
                elif target.suffix.lower() not in {".md", ".markdown"}:
                    self.add(
                        "STATE007",
                        "error",
                        path,
                        "CURRENT-STATE.json points to a non-Markdown plan",
                        f"The plan path {plan!r} resolves to {self.display_path(target)}.",
                        "Point plan to the Markdown document that owns the detailed work state.",
                    )

            status = value.get("status")
            if status not in CURRENT_STATE_STATUSES:
                self.add(
                    "STATE008",
                    "error",
                    path,
                    "CURRENT-STATE.json has an invalid status",
                    f"Allowed statuses are: {', '.join(sorted(CURRENT_STATE_STATUSES))}.",
                    "Use one allowed status and keep explanations in the linked plan.",
                )

            if "phase" in value and (
                not isinstance(value["phase"], str) or not value["phase"].strip()
            ):
                self.add(
                    "STATE009",
                    "error",
                    path,
                    "CURRENT-STATE.json has an invalid phase",
                    "The optional phase field must be a non-empty string when present.",
                    "Omit phase for a simple plan or provide its current phase as a short string.",
                )

            context = self.nearest_context(path.parent)
            if context is None:
                self.add(
                    "STATE010",
                    "error",
                    path,
                    "CURRENT-STATE.json has no applicable CONTEXT.md",
                    "A state file must belong to a context boundary so an agent can discover its scope.",
                    "Create or link the applicable CONTEXT.md before keeping this state file.",
                )
                continue

            linked_targets = {
                self.resolve_link_target(context, link.target)[0]
                for link in self.links_in(context)
                if self.resolve_link_target(context, link.target)[0] is not None
            }
            if path not in linked_targets:
                self.add(
                    "STATE011",
                    "error",
                    path,
                    "CURRENT-STATE.json is not linked from its CONTEXT.md",
                    f"The applicable context map is {self.display_path(context)}, but it does not link to this state file.",
                    f"Add a direct link to {self.display_path(path)} from {self.display_path(context)}.",
                )

    def check_navigation_maps(self) -> None:
        for path in sorted(self.markdown_files):
            if not self.args.include_public and path.name in PUBLIC_MARKDOWN_NAMES:
                continue

            lines = self.lines(path)
            line_count = len(lines)
            word_count = len(WORD_RE.findall(self.read_text(path)))
            headings = self.headings(path)
            h2_count = sum(heading.level == 2 for heading in headings)
            map_heading = next(
                (heading for heading in headings if self.is_map_heading(heading.text)),
                None,
            )
            threshold_triggered = (
                line_count > self.args.min_lines
                or word_count > self.args.min_words
            )

            if threshold_triggered and map_heading is None:
                self.add(
                    "NAV001",
                    "error",
                    path,
                    "Document is large but has no navigation map",
                    f"The document has {line_count} lines and {word_count} words; large documents need task-oriented navigation near the beginning.",
                    "Add a concise navigation map with task questions or needs linked to real section headings.",
                )
            elif h2_count >= 3 and map_heading is None and not threshold_triggered:
                self.add(
                    "NAV002",
                    "warning",
                    path,
                    "Document may contain multiple independent areas without a navigation map",
                    f"The document has {h2_count} level-two sections. Section count cannot prove that the areas are independent, so this is a review prompt rather than an automatic violation.",
                    "If these sections answer distinct task questions, add a task-oriented navigation map near the beginning.",
                )

            if map_heading is None:
                continue

            if map_heading.line > self.args.map_max_lines:
                self.add(
                    "NAV003",
                    "error",
                    path,
                    "Navigation map is too far from the beginning",
                    f"The map starts at line {map_heading.line}; it should be available before an agent has to read the document body.",
                    f"Move the map to the first {self.args.map_max_lines} lines, after only minimal document metadata or purpose text.",
                    line=map_heading.line,
                )

            map_body = self.section_body(path, map_heading)
            map_links = self.links_in_text(map_body, map_heading.line + 1)
            if not map_links:
                self.add(
                    "NAV004",
                    "error",
                    path,
                    "Navigation map contains no direct links",
                    "The map describes navigation but provides no anchors or document links for selective loading.",
                    "Link each task-oriented entry directly to the relevant heading, preferably with a local anchor.",
                    line=map_heading.line,
                )
                continue

            for link in map_links:
                target_path, fragment = self.resolve_link_target(path, link.target)
                if target_path is None or not fragment:
                    self.add(
                        "NAV005",
                        "warning",
                        path,
                        "Navigation entry does not target a specific heading",
                        f"The map entry links to {link.target!r} without a verifiable section anchor.",
                        "Point the entry to a real heading anchor so the agent can load only the relevant section.",
                        line=link.line,
                    )
                    continue
                if target_path.suffix.lower() not in {".md", ".markdown"}:
                    continue
                anchors = {heading.anchor for heading in self.headings(target_path)}
                if fragment not in anchors:
                    self.add(
                        "ANC001",
                        "error",
                        path,
                        "Navigation map points to a missing heading anchor",
                        f"The anchor #{fragment} does not exist in {self.display_path(target_path)}.",
                        "Update the anchor to match an existing heading or add the intended heading.",
                        line=link.line,
                    )

    def check_markdown_links(self) -> None:
        for path in sorted(self.markdown_files):
            for link in self.links_in(path):
                target_path, fragment = self.resolve_link_target(path, link.target)
                if target_path is None:
                    continue
                if not target_path.exists():
                    self.add(
                        "LNK001",
                        "error",
                        path,
                        "Internal Markdown link is broken",
                        f"The link target {link.target!r} does not resolve from {self.display_path(path)}.",
                        "Update the path, create the missing destination, or remove the obsolete link.",
                        line=link.line,
                    )
                    continue
                if fragment and target_path.suffix.lower() in {".md", ".markdown"}:
                    anchors = {heading.anchor for heading in self.headings(target_path)}
                    if fragment not in anchors:
                        self.add(
                            "ANC001",
                            "error",
                            path,
                            "Internal link points to a missing heading anchor",
                            f"The anchor #{fragment} does not exist in {self.display_path(target_path)}.",
                            "Update the anchor to match an existing heading or add the intended heading.",
                            line=link.line,
                        )

    def nearest_context(self, directory: Path) -> Path | None:
        current = directory.resolve()
        while True:
            candidate = current / "CONTEXT.md"
            if candidate in self.context_files or candidate.is_file():
                return candidate
            if current == self.root:
                return None
            current = current.parent

    def headings(self, path: Path) -> list[Heading]:
        if path in self._headings_cache:
            return self._headings_cache[path]

        headings: list[Heading] = []
        used_anchors: Counter[str] = Counter()
        in_fence = False
        for line_number, line in enumerate(self.lines(path), start=1):
            if line.strip().startswith("```") or line.strip().startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            match = HEADING_RE.match(line)
            if not match:
                continue
            text = match.group(2).strip()
            base_anchor = self.slugify(text)
            suffix = used_anchors[base_anchor]
            anchor = base_anchor if suffix == 0 else f"{base_anchor}-{suffix}"
            used_anchors[base_anchor] += 1
            headings.append(Heading(len(match.group(1)), text, line_number, anchor))

        self._headings_cache[path] = headings
        return headings

    def section_body(self, path: Path, heading: Heading) -> str:
        lines = self.lines(path)
        start = heading.line
        for index in range(start, len(lines)):
            match = HEADING_RE.match(lines[index])
            if match and len(match.group(1)) <= heading.level:
                return "\n".join(lines[start:index])
        return "\n".join(lines[start:])

    def links_in(self, path: Path) -> list[Link]:
        return self.links_in_text(self.read_text(path), 1)

    def links_in_text(self, text: str, start_line: int) -> list[Link]:
        links: list[Link] = []
        in_fence = False
        for offset, line in enumerate(text.splitlines(), start=start_line):
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in MARKDOWN_LINK_RE.finditer(line):
                if match.group(0).startswith("!"):
                    continue
                target = match.group(1) or match.group(2)
                if target:
                    links.append(Link(target=target, line=offset))
        return links

    def resolve_link_target(self, source: Path, target: str) -> tuple[Path | None, str | None]:
        target = unquote(target.strip())
        if not target or target.startswith("#"):
            fragment = target[1:] if target.startswith("#") else None
            return source, fragment

        split = urlsplit(target)
        if split.scheme or split.netloc:
            return None, None
        fragment = split.fragment or None
        raw_path = split.path
        if not raw_path:
            return source, fragment

        if raw_path.startswith("/"):
            candidate = (self.root / raw_path.lstrip("/")).resolve()
        else:
            candidate = (source.parent / raw_path).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError:
            return None, fragment
        return candidate, fragment

    def relative_link(self, source_directory: Path, target: Path) -> str:
        return Path(os.path.relpath(target, source_directory)).as_posix()

    def markdown_tables(self, lines: Sequence[str]) -> list[tuple[list[str], list[list[str]]]]:
        tables: list[tuple[list[str], list[list[str]]]] = []
        index = 0
        while index + 1 < len(lines):
            if "|" not in lines[index] or not TABLE_SEPARATOR_RE.match(lines[index + 1]):
                index += 1
                continue
            header = self.split_table_row(lines[index])
            rows: list[list[str]] = []
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append(self.split_table_row(lines[index]))
                index += 1
            tables.append((header, rows))
        return tables

    @staticmethod
    def split_table_row(line: str) -> list[str]:
        stripped = line.strip().strip("|")
        return [cell.strip() for cell in stripped.split("|")]

    @staticmethod
    def normalize_word(value: str) -> str:
        value = unicodedata.normalize("NFKD", value)
        value = "".join(char for char in value if not unicodedata.combining(char))
        return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

    @classmethod
    def normalize_header_words(cls, value: str) -> set[str]:
        return set(cls.normalize_word(value).split())

    @classmethod
    def is_map_heading(cls, text: str) -> bool:
        normalized = cls.normalize_word(text)
        return normalized in MAP_HEADINGS

    @classmethod
    def is_router_heading(cls, text: str) -> bool:
        normalized = cls.normalize_word(text)
        return normalized in ROUTER_HEADINGS

    @staticmethod
    def slugify(text: str) -> str:
        text = unicodedata.normalize("NFKC", text.lower())
        text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
        return re.sub(r"[-\s]+", "-", text).strip("-")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit repository context architecture and report actionable findings."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root to audit (default: current directory).",
    )
    parser.add_argument(
        "--min-lines",
        type=int,
        default=350,
        help="Line threshold for requiring navigation maps (default: 350).",
    )
    parser.add_argument(
        "--min-words",
        type=int,
        default=2000,
        help="Word threshold for requiring navigation maps (default: 2000).",
    )
    parser.add_argument(
        "--map-max-lines",
        type=int,
        default=60,
        help="Latest line at which a navigation map should begin (default: 60).",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Additional directory or path pattern to exclude; repeatable. Recurring exclusions can be stored in .contextignore.",
    )
    parser.add_argument(
        "--require-context",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Explicit directory pattern that must have CONTEXT.md; repeatable.",
    )
    parser.add_argument(
        "--include-public",
        action="store_true",
        help="Also require navigation maps in common public Markdown files such as README.md.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Report format (default: text).",
    )
    return parser.parse_args(argv)


def print_text_report(
    root: Path,
    findings: Sequence[Finding],
    exclude_patterns: Sequence[str],
) -> None:
    print(f"Context architecture audit: {root}")
    print("No files were modified.")
    if exclude_patterns:
        print(f"Exclusions loaded: {', '.join(exclude_patterns)}")
    print()

    if not findings:
        print("No findings.")
        return

    for finding in findings:
        location = finding.path
        if finding.line is not None:
            location += f":{finding.line}"
        print(f"[{finding.severity.upper()}] {finding.code} {location}")
        print(f"  {finding.title}")
        print(f"  Why: {finding.why}")
        print(f"  Suggested action: {finding.suggestion}")
        print()

    counts = Counter(finding.severity for finding in findings)
    summary = ", ".join(
        f"{severity}={counts[severity]}"
        for severity in ("error", "warning", "info")
        if counts[severity]
    )
    print(f"Summary: {len(findings)} finding(s) ({summary}).")
    print("Review findings with the repository owner before deciding which changes to apply.")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = args.root.resolve()
    if not root.is_dir():
        print(f"error: repository root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    auditor = Auditor(root, args)
    findings = auditor.run()
    if args.format == "json":
        print(json.dumps([asdict(finding) for finding in findings], ensure_ascii=False, indent=2))
    else:
        print_text_report(root, findings, auditor.exclude_patterns)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
