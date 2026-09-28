#!/usr/bin/env python3
"""Shared discovery, validation, and generation logic for the skill catalog.

This module deliberately uses only the Python standard library.  Its public
functions are read-only except for ``write_catalog``, which has a narrow,
explicit output boundary.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlsplit


SCHEMA_VERSION = "SC1"
SKILL_ROOT_RELATIVE = Path("agent-skills/skills")
CATALOG_RELATIVE = Path("agent-skills/SKILL-ARCHITECTURE.md")
HTML_CATALOG_RELATIVE = Path("agent-skills/SKILL-ARCHITECTURE.html")
FRONTMATTER_START = re.compile(r"^---\s*$")
KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(
    r"!?(?:\[[^\]]*\])\((?:<([^>]+)>|([^\s)]+))(?:\s+(?:\"[^\"]*\"|'[^']*'))?\)"
)
MACHINE_PATH_RE = re.compile(
    r"(?:^|[\s(\[=])(?:/Users/|/home/|/private/var/|~/|[A-Za-z]:[\\/])"
)
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel"}
SUPPORTED_INTERFACE_FIELDS = {"display_name", "short_description", "default_prompt"}
SUPPORTED_POLICY_FIELDS = {"allow_implicit_invocation"}


@dataclass(frozen=True)
class ParsedDocument:
    data: dict[str, Any]
    body: str
    frontmatter_end_line: int


class ParseError(ValueError):
    """Raised when a supported, intentionally small YAML subset is invalid."""


def display_path(root: Path, path: Path) -> str:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return str(path)
    return relative.as_posix() or "."


def issue(
    code: str,
    severity: str,
    path: str,
    explanation: str,
    suggestion: str,
    *,
    line: int | None = None,
    status: str = "invalid",
    location: str | None = None,
) -> dict[str, Any]:
    return {
        "code": code,
        "severity": severity,
        "status": status,
        "path": path,
        "line": line,
        "location": location,
        "explanation": explanation,
        "suggestion": suggestion,
    }


def _strip_comment(value: str) -> str:
    quoted = None
    escaped = False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quoted == '"':
            escaped = True
            continue
        if char in {"'", '"'}:
            if quoted is None:
                quoted = char
            elif quoted == char:
                quoted = None
            continue
        if char == "#" and quoted is None and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
    return value.strip()


def _scalar(value: str) -> Any:
    value = _strip_comment(value.strip())
    if value in {"", "null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [_scalar(item) for item in inner.split(",")]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        if value[0] == '"':
            try:
                return json.loads(value)
            except json.JSONDecodeError as exc:
                raise ParseError(f"invalid quoted scalar: {value}") from exc
        return value[1:-1].replace("''", "'")
    return value


def parse_mapping(text: str) -> dict[str, Any]:
    """Parse the mapping subset used by frontmatter and openai.yaml.

    Supported values are scalars, inline lists, and nested mappings.  This is
    intentionally stricter than silently accepting YAML that the catalog does
    not know how to interpret.
    """

    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    lines = text.splitlines()
    number = 0
    while number < len(lines):
        raw = lines[number]
        number += 1
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise ParseError(f"tabs are not supported at line {number}")
        indent = len(raw) - len(raw.lstrip(" "))
        content = raw[indent:]
        if content.startswith("-"):
            raise ParseError(f"lists are not supported at line {number}")
        if ":" not in content:
            raise ParseError(f"expected key/value mapping at line {number}")
        key, raw_value = content.split(":", 1)
        key = key.strip()
        if not KEY_RE.fullmatch(key):
            raise ParseError(f"invalid key {key!r} at line {number}")
        while stack[-1][0] >= indent:
            stack.pop()
        if not stack:
            raise ParseError(f"invalid indentation at line {number}")
        current = stack[-1][1]
        if key in current:
            raise ParseError(f"duplicate key {key!r} at line {number}")
        raw_value = raw_value.strip()
        if raw_value in {">", ">-", ">+", "|", "|-", "|+"}:
            block: list[str] = []
            block_indent: int | None = None
            while number < len(lines):
                candidate = lines[number]
                candidate_indent = len(candidate) - len(candidate.lstrip(" "))
                if candidate.strip() and candidate_indent <= indent:
                    break
                number += 1
                if not candidate.strip():
                    block.append("")
                    continue
                if block_indent is None:
                    block_indent = candidate_indent
                if candidate_indent < block_indent:
                    raise ParseError(f"invalid block indentation at line {number}")
                block.append(candidate[block_indent:])
            value = (" " if raw_value.startswith(">") else "\n").join(block).strip()
        else:
            value = _scalar(raw_value)
        if value is None and not raw_value:
            value = {}
            current[key] = value
            stack.append((indent, value))
        else:
            current[key] = value
    return root


def parse_frontmatter(text: str) -> ParsedDocument:
    lines = text.splitlines(keepends=True)
    if not lines or not FRONTMATTER_START.match(lines[0].rstrip("\r\n")):
        raise ParseError("SKILL.md must start with YAML frontmatter")
    closing = None
    for index in range(1, len(lines)):
        if FRONTMATTER_START.match(lines[index].rstrip("\r\n")):
            closing = index
            break
    if closing is None:
        raise ParseError("frontmatter closing delimiter is missing")
    frontmatter = "".join(lines[1:closing])
    data = parse_mapping(frontmatter)
    return ParsedDocument(data, "".join(lines[closing + 1 :]), closing + 1)


def discover_packages(root: Path, skill_root: Path | None = None) -> list[Path]:
    root = root.resolve()
    skill_root = (skill_root or root / SKILL_ROOT_RELATIVE).resolve()
    if not skill_root.is_dir():
        return []
    return sorted((path for path in skill_root.iterdir() if path.is_dir()), key=lambda p: p.name)


def has_files(path: Path) -> bool:
    return any(candidate.is_file() for candidate in path.rglob("*"))


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _is_external(target: str) -> bool:
    parsed = urlsplit(target)
    return parsed.scheme.lower() in EXTERNAL_SCHEMES or target.startswith("//")


def _validate_links(root: Path, package: Path, text: str, issues: list[dict[str, Any]]) -> None:
    for match in LINK_RE.finditer(text):
        target = unquote(match.group(1) or match.group(2) or "").strip()
        line = _line_number(text, match.start())
        if not target or target.startswith("#") or _is_external(target):
            continue
        if (
            target.startswith("/")
            or target.startswith("~/")
            or re.match(r"^[A-Za-z]:[\\/]", target)
            or target.startswith("file:")
        ):
            issues.append(
                issue(
                    "ABSOLUTE_REFERENCE",
                    "error",
                    display_path(root, package / "SKILL.md"),
                    "a skill link uses an absolute or machine-specific path",
                    "Use a repository-relative link inside the skill package.",
                    line=line,
                    location=f"link target {target!r}",
                )
            )
            continue
        path_target = target.split("#", 1)[0].split("?", 1)[0]
        resolved = (package / path_target).resolve()
        try:
            resolved.relative_to(package.resolve())
        except ValueError:
            if not resolved.exists():
                issues.append(
                    issue(
                        "REFERENCE_MISSING",
                        "error",
                        display_path(root, package / "SKILL.md"),
                        f"referenced path does not exist: {target}",
                        "Create the referenced file or correct the relative link.",
                        line=line,
                        location=f"link target {target!r}",
                    )
                )
            continue
        if not resolved.exists():
            issues.append(
                issue(
                    "REFERENCE_MISSING",
                    "error",
                    display_path(root, package / "SKILL.md"),
                    f"referenced path does not exist: {target}",
                    "Create the referenced file or correct the relative link.",
                    line=line,
                    location=f"link target {target!r}",
                )
            )


def _validate_machine_paths(root: Path, package: Path, text: str, relative_file: Path, issues: list[dict[str, Any]]) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if MACHINE_PATH_RE.search(line):
            issues.append(
                issue(
                    "MACHINE_SPECIFIC_PATH",
                    "error",
                    display_path(root, package / relative_file),
                    "a machine-specific absolute path appears where repository-relative paths are expected",
                    "Use a repository-relative path or a documented symbolic placeholder.",
                    line=line_number,
                )
            )


def _validate_runtime_metadata(root: Path, package: Path, issues: list[dict[str, Any]]) -> dict[str, Any]:
    metadata_path = package / "agents" / "openai.yaml"
    if not metadata_path.exists():
        return {"status": "missing", "supported": {}}
    try:
        metadata_text = metadata_path.read_text(encoding="utf-8")
    except OSError as exc:
        issues.append(
            issue(
                "RUNTIME_METADATA_UNAVAILABLE",
                "error",
                display_path(root, metadata_path),
                f"agents/openai.yaml could not be read: {exc}",
                "Make the optional runtime metadata readable or remove it.",
                status="unavailable",
            )
        )
        return {"status": "unavailable", "supported": {}}
    except UnicodeDecodeError as exc:
        issues.append(
            issue(
                "RUNTIME_METADATA_INDETERMINATE",
                "error",
                display_path(root, metadata_path),
                f"agents/openai.yaml is not valid UTF-8: {exc}",
                "Rewrite the optional runtime metadata as UTF-8 YAML.",
                status="indeterminate",
            )
        )
        return {"status": "indeterminate", "supported": {}}
    try:
        metadata = parse_mapping(metadata_text)
    except ParseError as exc:
        issues.append(
            issue(
                "RUNTIME_METADATA_INVALID",
                "error",
                display_path(root, metadata_path),
                f"agents/openai.yaml cannot be parsed: {exc}",
                "Fix the YAML structure or remove the optional runtime metadata file.",
            )
        )
        return {"status": "invalid", "supported": {}}
    for key in sorted(set(metadata) - {"interface", "policy"}):
        issues.append(
            issue(
                "RUNTIME_METADATA_UNKNOWN",
                "warning",
                display_path(root, metadata_path),
                f"runtime metadata field is not supported by the catalog: {key}",
                "Document a supported field before relying on it in generated output.",
                status="unknown",
            )
        )
    interface = metadata.get("interface")
    if interface is None:
        issues.append(
            issue(
                "RUNTIME_INTERFACE_MISSING",
                "warning",
                display_path(root, metadata_path),
                "optional runtime metadata has no supported interface mapping",
                "Add interface metadata only when the runtime supports it; otherwise leave the file absent.",
                status="missing",
            )
        )
        return {"status": "present", "supported": {}}
    if not isinstance(interface, dict):
        issues.append(
            issue(
                "RUNTIME_INTERFACE_INVALID",
                "error",
                display_path(root, metadata_path),
                "the interface runtime metadata must be a mapping",
                "Use an interface mapping with supported scalar fields.",
            )
        )
        return {"status": "invalid", "supported": {}}
    supported: dict[str, str] = {}
    for key in sorted(set(interface) - SUPPORTED_INTERFACE_FIELDS):
        issues.append(
            issue(
                "RUNTIME_FIELD_UNKNOWN",
                "warning",
                display_path(root, metadata_path),
                f"runtime interface field is not supported by the catalog: interface.{key}",
                "Document a supported field before relying on it in generated output.",
                status="unknown",
            )
        )
    for key in sorted(SUPPORTED_INTERFACE_FIELDS):
        value = interface.get(key)
        if value is None:
            issues.append(
                issue(
                    "RUNTIME_FIELD_MISSING",
                    "warning",
                    display_path(root, metadata_path),
                    f"optional runtime field is missing: interface.{key}",
                    "Add the field if the runtime integration needs it; otherwise keep the supported metadata minimal.",
                    status="missing",
                )
            )
        elif not isinstance(value, str) or not value.strip():
            issues.append(
                issue(
                    "RUNTIME_FIELD_INVALID",
                    "error",
                    display_path(root, metadata_path),
                    f"interface.{key} must be a non-empty string",
                    "Set the runtime field to a non-empty string.",
                )
            )
        else:
            supported[key] = value.strip()
    policy = metadata.get("policy")
    if policy is not None:
        if not isinstance(policy, dict):
            issues.append(
                issue(
                    "RUNTIME_POLICY_INVALID",
                    "error",
                    display_path(root, metadata_path),
                    "the policy runtime metadata must be a mapping",
                    "Use a policy mapping with supported boolean fields.",
                )
            )
        else:
            for key in sorted(set(policy) - SUPPORTED_POLICY_FIELDS):
                issues.append(
                    issue(
                        "RUNTIME_POLICY_UNKNOWN",
                        "warning",
                        display_path(root, metadata_path),
                        f"runtime policy field is not supported by the catalog: policy.{key}",
                        "Document a supported policy field before relying on it in generated output.",
                        status="unknown",
                    )
                )
            value = policy.get("allow_implicit_invocation")
            if value is not None and not isinstance(value, bool):
                issues.append(
                    issue(
                        "RUNTIME_POLICY_INVALID",
                        "error",
                        display_path(root, metadata_path),
                        "policy.allow_implicit_invocation must be a boolean",
                        "Set policy.allow_implicit_invocation to true or false.",
                    )
                )
            elif isinstance(value, bool):
                supported["allow_implicit_invocation"] = value
    return {"status": "present", "supported": supported}


def validate_repository(root: Path, *, check_catalog: bool = False, catalog_path: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    skill_root = root / SKILL_ROOT_RELATIVE
    packages: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    seen_names: dict[str, Path] = {}
    resolved_packages: dict[Path, Path] = {}

    if not skill_root.is_dir():
        issues.append(
            issue(
                "SKILL_ROOT_UNAVAILABLE",
                "error",
                display_path(root, skill_root),
                "the configured skill root does not exist or is not a directory",
                "Provide the repository with agent-skills/skills/ or select the correct repository root.",
                status="unavailable",
            )
        )

    for package in discover_packages(root, skill_root):
        package_label = display_path(root, package)
        if not has_files(package):
            packages.append({"name": package.name, "path": package_label, "status": "empty"})
            issues.append(
                issue(
                    "SKILL_EMPTY",
                    "error",
                    package_label,
                    "candidate skill directory contains no files",
                    "Add SKILL.md and the package resources, or remove the empty directory.",
                    status="empty",
                )
            )
            continue

        try:
            canonical = package.resolve()
            previous = resolved_packages.get(canonical)
            if previous is not None and previous != package:
                issues.append(
                    issue(
                        "PACKAGE_PATH_AMBIGUOUS",
                        "error",
                        package_label,
                        f"package path resolves to the same directory as {display_path(root, previous)}",
                        "Keep one canonical package path under agent-skills/skills/.",
                    )
                )
            resolved_packages[canonical] = package
        except OSError:
            issues.append(
                issue(
                    "PACKAGE_UNAVAILABLE",
                    "error",
                    package_label,
                    "package path could not be resolved",
                    "Make the package path readable and resolve filesystem indirection.",
                    status="unavailable",
                )
            )

        skill_file = package / "SKILL.md"
        if not skill_file.is_file():
            packages.append({"name": package.name, "path": package_label, "status": "missing"})
            issues.append(
                issue(
                    "SKILL_MISSING",
                    "error",
                    package_label,
                    "candidate skill directory has no SKILL.md",
                    "Add SKILL.md with name and description frontmatter.",
                    status="missing",
                )
            )
            continue

        try:
            text = skill_file.read_text(encoding="utf-8")
        except OSError as exc:
            packages.append({"name": package.name, "path": package_label, "status": "unavailable"})
            issues.append(
                issue(
                    "SKILL_UNAVAILABLE",
                    "error",
                    display_path(root, skill_file),
                    f"SKILL.md could not be read: {exc}",
                    "Make SKILL.md readable and rerun the validator.",
                    status="unavailable",
                )
            )
            continue
        except UnicodeDecodeError as exc:
            packages.append({"name": package.name, "path": package_label, "status": "indeterminate"})
            issues.append(
                issue(
                    "FRONTMATTER_INDETERMINATE",
                    "error",
                    display_path(root, skill_file),
                    f"SKILL.md is not valid UTF-8: {exc}",
                    "Rewrite SKILL.md as UTF-8 and rerun the validator.",
                    status="indeterminate",
                )
            )
            continue
        try:
            parsed = parse_frontmatter(text)
        except ParseError as exc:
            packages.append({"name": package.name, "path": package_label, "status": "invalid"})
            issues.append(
                issue(
                    "FRONTMATTER_INVALID",
                    "error",
                    display_path(root, skill_file),
                    f"SKILL.md frontmatter cannot be parsed: {exc}",
                    "Add valid YAML frontmatter delimited by --- lines.",
                )
            )
            continue

        package_issues_before = len(issues)
        name = parsed.data.get("name")
        description = parsed.data.get("description")
        for key in sorted(set(parsed.data) - {"name", "description"}):
            issues.append(
                issue(
                    "FRONTMATTER_FIELD_UNKNOWN",
                    "warning",
                    display_path(root, skill_file),
                    f"frontmatter field is not supported by the catalog: {key}",
                    "Keep optional metadata in a supported runtime configuration or document its contract.",
                    status="unknown",
                )
            )
        if name is None:
            issues.append(
                issue(
                    "FRONTMATTER_NAME_MISSING",
                    "error",
                    display_path(root, skill_file),
                    "frontmatter is missing name",
                    "Add a lowercase hyphen-case name matching the package directory.",
                    line=1,
                    status="missing",
                )
            )
        elif not isinstance(name, str) or not name.strip():
            issues.append(
                issue(
                    "FRONTMATTER_NAME_INVALID",
                    "error",
                    display_path(root, skill_file),
                    "frontmatter name must be a non-empty string",
                    "Set name to the package directory name.",
                )
            )
        else:
            name = name.strip()
            if not NAME_RE.fullmatch(name):
                issues.append(
                    issue(
                        "SKILL_NAME_INVALID",
                        "error",
                        display_path(root, skill_file),
                        "skill name must use lowercase hyphen-case",
                        "Use only lowercase letters, digits, and single hyphens.",
                    )
                )
            if name != package.name:
                issues.append(
                    issue(
                        "SKILL_NAME_MISMATCH",
                        "error",
                        display_path(root, skill_file),
                        f"frontmatter name {name!r} does not match directory {package.name!r}",
                        "Rename the directory or set frontmatter name to the directory name.",
                    )
                )
            previous = seen_names.get(name)
            if previous is not None and previous != package:
                issues.append(
                    issue(
                        "DUPLICATE_SKILL_NAME",
                        "error",
                        package_label,
                        f"skill name {name!r} is also declared by {display_path(root, previous)}",
                        "Give each package a unique canonical skill name.",
                    )
                )
            seen_names[name] = package
        if description is None:
            issues.append(
                issue(
                    "FRONTMATTER_DESCRIPTION_MISSING",
                    "error",
                    display_path(root, skill_file),
                    "frontmatter is missing description",
                    "Add a concise description that states capability, trigger, and boundary.",
                    line=1,
                    status="missing",
                )
            )
        elif not isinstance(description, str) or not description.strip():
            issues.append(
                issue(
                    "FRONTMATTER_DESCRIPTION_INVALID",
                    "error",
                    display_path(root, skill_file),
                    "frontmatter description must be a non-empty string",
                    "Set description to a concise non-empty string.",
                )
            )

        _validate_links(root, package, text, issues)
        _validate_machine_paths(root, package, text, Path("SKILL.md"), issues)
        runtime = _validate_runtime_metadata(root, package, issues)
        metadata_path = package / "agents" / "openai.yaml"
        if metadata_path.is_file():
            try:
                metadata_text = metadata_path.read_text(encoding="utf-8")
            except OSError:
                metadata_text = None
            except UnicodeDecodeError:
                metadata_text = None
            if metadata_text is not None:
                _validate_machine_paths(root, package, metadata_text, Path("agents/openai.yaml"), issues)
        package_issues = issues[package_issues_before:]
        package_status = "valid" if not any(item["severity"] == "error" for item in package_issues) else "invalid"
        if runtime["status"] in {"unavailable", "indeterminate"}:
            package_status = runtime["status"]
        packages.append(
            {
                "name": package.name,
                "path": package_label,
                "status": package_status,
                "description": description.strip() if isinstance(description, str) else None,
                "runtime_metadata": runtime,
            }
        )

    catalog: dict[str, Any] = {"status": "not_checked", "path": display_path(root, catalog_path or root / CATALOG_RELATIVE)}
    if check_catalog:
        markdown_target = (catalog_path or root / CATALOG_RELATIVE).resolve()
        html_target = (root / HTML_CATALOG_RELATIVE).resolve()
        expected_markdown = generate_catalog(root)
        expected_html = generate_html_catalog(root)

        def check_generated_file(
            target: Path,
            expected: str,
            missing_code: str,
            drift_code: str,
            label: str,
        ) -> dict[str, Any]:
            if not target.exists():
                issues.append(
                    issue(
                        missing_code,
                        "error",
                        display_path(root, target),
                        f"generated {label} does not exist",
                        "Run generate_skill_catalog.py --write to create generated catalog outputs.",
                        status="missing",
                    )
                )
                return {"status": "missing", "expected_sha256": _sha256(expected)}
            try:
                actual = target.read_text(encoding="utf-8")
            except OSError as exc:
                issues.append(
                    issue(
                        "CATALOG_OUTPUT_UNAVAILABLE",
                        "error",
                        display_path(root, target),
                        f"generated {label} could not be read: {exc}",
                        "Make the generated output readable and rerun the check.",
                        status="unavailable",
                    )
                )
                return {"status": "unavailable"}
            except UnicodeDecodeError as exc:
                issues.append(
                    issue(
                        "CATALOG_OUTPUT_INDETERMINATE",
                        "error",
                        display_path(root, target),
                        f"generated {label} is not valid UTF-8: {exc}",
                        "Rewrite the generated output as UTF-8.",
                        status="indeterminate",
                    )
                )
                return {"status": "indeterminate"}
            if actual != expected:
                issues.append(
                    issue(
                        drift_code,
                        "error",
                        display_path(root, target),
                        f"committed generated {label} differs from deterministic output",
                        "Regenerate the catalog and commit only the generated result.",
                        status="drifted",
                    )
                )
                return {
                    "status": "drifted",
                    "expected_sha256": _sha256(expected),
                    "actual_sha256": _sha256(actual),
                }
            return {"status": "valid", "sha256": _sha256(actual)}

        markdown_result = check_generated_file(
            markdown_target,
            expected_markdown,
            "CATALOG_MISSING",
            "CATALOG_DRIFT",
            "Markdown catalog",
        )
        html_result = check_generated_file(
            html_target,
            expected_html,
            "CATALOG_HTML_MISSING",
            "CATALOG_HTML_DRIFT",
            "HTML catalog",
        )
        catalog["markdown"] = markdown_result
        catalog["html"] = html_result
        states = {markdown_result["status"], html_result["status"]}
        catalog["status"] = (
            "unavailable" if "unavailable" in states else
            "indeterminate" if "indeterminate" in states else
            "drifted" if "drifted" in states else
            "missing" if "missing" in states else
            "valid"
        )

    errors = [item for item in issues if item["severity"] == "error"]
    issue_statuses = {item["status"] for item in issues}
    if "unavailable" in issue_statuses:
        status = "unavailable"
    elif "indeterminate" in issue_statuses:
        status = "indeterminate"
    else:
        status = "invalid" if errors else "valid"
    if not errors and catalog["status"] in {"drifted", "missing"}:
        status = catalog["status"]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "skill_root": display_path(root, skill_root),
        "catalog": catalog,
        "packages": packages,
        "summary": {
            "packages": len(packages),
            "valid": sum(item["status"] == "valid" for item in packages),
            "invalid": sum(item["status"] == "invalid" for item in packages),
            "missing": sum(item["status"] == "missing" for item in packages),
            "empty": sum(item["status"] == "empty" for item in packages),
            "unavailable": sum(item["status"] == "unavailable" for item in packages),
            "indeterminate": sum(item["status"] == "indeterminate" for item in packages),
            "issues": len(issues),
        },
        "issues": issues,
    }


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _markdown_value(value: str | None) -> str:
    if value is None:
        return "unknown"
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _discover_references(package_name: str, text: str, known_names: set[str]) -> list[str]:
    references: set[str] = set()
    for match in re.finditer(r"\$([a-z0-9]+(?:-[a-z0-9]+)*)", text):
        candidate = match.group(1)
        if candidate in known_names and candidate != package_name:
            references.add(candidate)
    for match in LINK_RE.finditer(text):
        target = unquote(match.group(1) or match.group(2) or "").split("#", 1)[0]
        target_match = re.search(r"(?:^|/)skills/([^/]+)/SKILL\.md$", target)
        if target_match and target_match.group(1) in known_names and target_match.group(1) != package_name:
            references.add(target_match.group(1))
    return sorted(references)


def _catalog_entries(root: Path) -> list[dict[str, Any]]:
    root = root.resolve()
    entries: list[dict[str, Any]] = []
    packages = [
        package
        for package in discover_packages(root, root / SKILL_ROOT_RELATIVE)
        if has_files(package)
    ]
    known_names = {package.name for package in packages}
    for package in packages:
        skill_file = package / "SKILL.md"
        data: dict[str, Any] = {}
        skill_text = ""
        if skill_file.is_file():
            try:
                skill_text = skill_file.read_text(encoding="utf-8")
                data = parse_frontmatter(skill_text).data
            except (OSError, UnicodeDecodeError, ParseError):
                data = {}
        description = data.get("description") if isinstance(data.get("description"), str) else None
        metadata_file = package / "agents" / "openai.yaml"
        runtime_status = "missing"
        supported: dict[str, Any] = {}
        metadata_text = ""
        if metadata_file.is_file():
            try:
                metadata_text = metadata_file.read_text(encoding="utf-8")
                metadata = parse_mapping(metadata_text)
                runtime_status = "present"
                interface = metadata.get("interface")
                if isinstance(interface, dict):
                    for key in sorted(SUPPORTED_INTERFACE_FIELDS):
                        if isinstance(interface.get(key), str) and interface[key].strip():
                            supported[key] = interface[key].strip()
                policy = metadata.get("policy")
                if isinstance(policy, dict) and isinstance(policy.get("allow_implicit_invocation"), bool):
                    supported["allow_implicit_invocation"] = policy["allow_implicit_invocation"]
            except (OSError, UnicodeDecodeError, ParseError):
                runtime_status = "invalid"
        entries.append(
            {
                "name": package.name,
                "description": description,
                "package_path": display_path(root, package),
                "skill_link": f"skills/{package.name}/SKILL.md",
                "runtime_status": runtime_status,
                "supported": supported,
                "references": _discover_references(package.name, f"{skill_text}\n{metadata_text}", known_names),
            }
        )
    return entries


def generate_catalog(root: Path) -> str:
    entries = _catalog_entries(root)
    lines = [
        "<!-- Generated by agent-skills/scripts/generate_skill_catalog.py; do not edit manually. -->",
        "# Skill catalog",
        "",
        "This document is generated from the non-empty packages under `agent-skills/skills/`.",
        "It contains only package metadata and supported runtime metadata derived from the repository.",
        "",
    ]
    for entry in entries:
        description = entry["description"]
        supported = entry["supported"]
        lines.extend(
            [
                f"## {entry['name']}",
                "",
                f"- Description: {_markdown_value(description)}",
                f"- Package: [`{entry['package_path']}`]({entry['skill_link']})",
                f"- Runtime metadata: `{entry['runtime_status']}`",
            ]
        )
        if supported:
            lines.append("- Supported UI metadata:")
            for key in ("display_name", "short_description", "default_prompt"):
                if key in supported:
                    lines.append(f"  - `{key}`: {_markdown_value(supported[key])}")
        if "allow_implicit_invocation" in supported:
            policy_label = "implicit invocation allowed" if supported["allow_implicit_invocation"] else "explicit invocation required"
            lines.append(f"- Runtime policy: `{policy_label}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def generate_html_catalog(root: Path) -> str:
    """Generate a small, self-contained Obsidian-inspired catalog browser."""

    entries = _catalog_entries(root)
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    payload = payload.replace("</", "<\\/")
    return f'''<!doctype html>
<html lang="pt-PT">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="generated-by" content="agent-skills/scripts/generate_skill_catalog.py">
  <title>Skill catalog</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #191919;
      --surface: #202020;
      --surface-2: #262626;
      --border: #353535;
      --text: #dedede;
      --muted: #8f8f8f;
      --faint: #666;
      --accent: #a78bfa;
      --accent-soft: rgba(167, 139, 250, .12);
      --good: #8bc48b;
      --warn: #d7ad6b;
      --font: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ min-height: 100%; }}
    body {{ margin: 0; background: var(--bg); color: var(--text); font: 14px/1.55 var(--font); }}
    button, input {{ font: inherit; }}
    button {{ color: inherit; }}
    a {{ color: var(--accent); }}
    .shell {{ display: grid; grid-template-columns: 290px minmax(0, 1fr); min-height: 100vh; }}
    .sidebar {{ padding: 30px 18px 24px; border-right: 1px solid var(--border); background: #1c1c1c; }}
    .eyebrow {{ margin: 0 0 8px; color: var(--accent); font-size: 11px; letter-spacing: .14em; text-transform: uppercase; }}
    h1, h2, p {{ margin-top: 0; }}
    h1 {{ margin-bottom: 4px; font-size: 22px; font-weight: 500; letter-spacing: -.025em; }}
    .summary {{ margin-bottom: 22px; color: var(--muted); font-size: 12px; }}
    .search {{ display: block; margin-bottom: 13px; }}
    .search span {{ position: absolute; margin: 9px 0 0 10px; color: var(--faint); }}
    .search input {{ width: 100%; padding: 8px 10px 8px 29px; border: 1px solid var(--border); border-radius: 5px; outline: none; background: var(--surface); color: var(--text); }}
    .search input:focus {{ border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-soft); }}
    .filters {{ display: flex; gap: 5px; margin-bottom: 14px; }}
    .filters button {{ padding: 4px 7px; border: 0; border-radius: 4px; background: transparent; color: var(--muted); cursor: pointer; font-size: 12px; }}
    .filters button:hover, .filters button[aria-pressed="true"] {{ background: var(--accent-soft); color: var(--text); }}
    .skill-list {{ display: grid; gap: 2px; max-height: calc(100vh - 205px); margin: 0; padding: 0; overflow: auto; list-style: none; }}
    .skill-list button {{ position: relative; width: 100%; padding: 8px 10px 8px 21px; border: 0; border-radius: 4px; background: transparent; color: var(--muted); cursor: pointer; text-align: left; }}
    .skill-list button::before {{ position: absolute; top: 14px; left: 9px; width: 5px; height: 5px; border: 1px solid var(--faint); border-radius: 50%; content: ""; }}
    .skill-list button:hover, .skill-list button[aria-selected="true"] {{ background: var(--surface-2); color: var(--text); }}
    .skill-list button[aria-selected="true"]::before {{ border-color: var(--accent); background: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }}
    .skill-list .name {{ display: block; overflow: hidden; font-size: 13px; text-overflow: ellipsis; white-space: nowrap; }}
    .skill-list .status {{ display: block; margin-top: 1px; color: var(--faint); font-size: 11px; }}
    .empty-list {{ padding: 12px 10px; color: var(--muted); font-size: 12px; }}
    .content {{ min-width: 0; padding: 42px clamp(28px, 7vw, 110px); }}
    .content-inner {{ width: min(720px, 100%); }}
    .content-header {{ display: flex; justify-content: space-between; gap: 20px; margin-bottom: 72px; color: var(--muted); font-size: 12px; }}
    .content-header code {{ color: var(--faint); }}
    .view-switch {{ display: flex; gap: 4px; }}
    .view-switch button {{ padding: 3px 7px; border: 0; border-radius: 4px; background: transparent; color: var(--muted); cursor: pointer; font-size: 12px; }}
    .view-switch button:hover, .view-switch button[aria-pressed="true"] {{ background: var(--accent-soft); color: var(--text); }}
    .graph-view {{ margin: -20px 0 42px; border: 1px solid var(--border); background: #1c1c1c; }}
    .graph-note {{ margin: 0; padding: 10px 14px; border-top: 1px solid var(--border); color: var(--muted); font-size: 12px; }}
    .graph-canvas {{ width: 100%; overflow: hidden; background-image: radial-gradient(circle, rgba(255,255,255,.08) 1px, transparent 1px); background-size: 22px 22px; }}
    .graph-canvas svg {{ display: block; width: 100%; height: auto; min-height: 470px; }}
    .graph-line {{ stroke: rgba(167,139,250,.36); stroke-width: 1.3; }}
    .graph-line.selected {{ stroke: var(--accent); stroke-width: 2; }}
    .graph-node {{ cursor: pointer; }}
    .graph-node circle {{ fill: var(--surface-2); stroke: var(--border); stroke-width: 1.3; }}
    .graph-node:hover circle, .graph-node.selected circle {{ fill: var(--accent-soft); stroke: var(--accent); }}
    .graph-node text {{ fill: var(--muted); font-size: 11px; pointer-events: none; }}
    .graph-node.selected text {{ fill: var(--text); }}
    .graph-node .runtime-dot {{ stroke: var(--bg); stroke-width: 2; }}
    .graph-node .runtime-present {{ fill: var(--good); }}
    .graph-node .runtime-missing, .graph-node .runtime-invalid {{ fill: var(--warn); }}
    .graph-legend {{ padding: 10px 14px; color: var(--faint); font-size: 11px; }}
    .detail {{ min-height: 330px; }}
    .detail-kicker {{ margin-bottom: 12px; color: var(--accent); font-size: 11px; letter-spacing: .14em; text-transform: uppercase; }}
    h2 {{ margin-bottom: 18px; font-size: clamp(28px, 5vw, 46px); font-weight: 500; letter-spacing: -.045em; line-height: 1.08; }}
    .description {{ max-width: 650px; margin-bottom: 34px; color: var(--text); font-size: 17px; line-height: 1.6; }}
    .placeholder {{ max-width: 400px; color: var(--muted); }}
    .placeholder strong {{ display: block; margin-bottom: 8px; color: var(--text); font-size: 17px; font-weight: 500; }}
    dl {{ display: grid; grid-template-columns: 145px minmax(0, 1fr); gap: 11px 20px; margin: 0; padding-top: 22px; border-top: 1px solid var(--border); }}
    dt {{ color: var(--muted); font-size: 12px; }}
    dd {{ min-width: 0; margin: 0; color: var(--text); overflow-wrap: anywhere; }}
    dd code {{ color: var(--muted); font-size: 12px; }}
    .metadata {{ display: grid; gap: 7px; margin-top: 24px; padding: 15px; border-left: 2px solid var(--accent); background: var(--accent-soft); }}
    .metadata div {{ display: grid; grid-template-columns: 145px minmax(0, 1fr); gap: 20px; }}
    .metadata span:first-child {{ color: var(--muted); font-size: 12px; }}
    .metadata span:last-child {{ overflow-wrap: anywhere; }}
    .runtime-present {{ color: var(--good); }}
    .runtime-missing, .runtime-invalid {{ color: var(--warn); }}
    .footer {{ margin-top: 90px; color: var(--faint); font-size: 11px; }}
    @media (max-width: 720px) {{
      .shell {{ display: block; }}
      .sidebar {{ border-right: 0; border-bottom: 1px solid var(--border); }}
      .skill-list {{ max-height: 250px; }}
      .content {{ padding: 34px 22px 50px; }}
      .content-header {{ margin-bottom: 52px; }}
      .graph-view {{ margin-top: -8px; }}
      .graph-canvas svg {{ min-width: 620px; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <aside class="sidebar" aria-label="Skill catalog navigation">
      <p class="eyebrow">Agent skills</p>
      <h1>Catalog</h1>
      <p class="summary" id="summary"></p>
      <label class="search"><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="Find a skill…" autocomplete="off"></label>
      <div class="filters" aria-label="Runtime metadata filter">
        <button type="button" data-filter="all" aria-pressed="true">All</button>
        <button type="button" data-filter="present" aria-pressed="false">Configured</button>
        <button type="button" data-filter="missing" aria-pressed="false">Missing</button>
      </div>
      <ul class="skill-list" id="skill-list" role="listbox" aria-label="Skills"></ul>
    </aside>
    <main class="content">
      <div class="content-inner">
        <div class="content-header"><span id="visible-count"></span><div class="view-switch" role="group" aria-label="Catalog view"><button type="button" data-view="catalog" aria-pressed="true">Catalog</button><button type="button" data-view="graph" aria-pressed="false">Graph</button></div></div>
        <section class="graph-view" id="graph-view" hidden aria-label="Explicit skill references"><div class="graph-canvas" id="graph-canvas"></div><p class="graph-note">Only explicit references found in <code>SKILL.md</code> and <code>openai.yaml</code> are shown. No link does not mean no affinity.</p><div class="graph-legend">Each line is an explicit skill reference; disconnected nodes are still valid catalog packages.</div></section>
        <section class="detail" id="detail" aria-live="polite"></section>
        <p class="footer">Generated from <code>agent-skills/skills/</code>. Edit the packages, not this file.</p>
      </div>
    </main>
  </div>
  <script>
    const skills = {payload};
    const state = {{ query: '', filter: 'all', selected: skills[0]?.name || null, view: 'catalog' }};
    const list = document.getElementById('skill-list');
    const detail = document.getElementById('detail');
    const graphView = document.getElementById('graph-view');
    const graphCanvas = document.getElementById('graph-canvas');
    const search = document.getElementById('search');
    const summary = document.getElementById('summary');
    const count = document.getElementById('visible-count');
    const escapeHtml = value => String(value).replace(/[&<>\"']/g, char => ({{ '&': '&amp;', '<': '&lt;', '>': '&gt;', '\"': '&quot;', "'": '&#39;' }}[char]));
    const visible = skill => (!state.query || `${{skill.name}} ${{skill.description || ''}}`.toLowerCase().includes(state.query)) && (state.filter === 'all' || skill.runtime_status === state.filter);
    const label = status => status === 'present' ? 'configured' : status === 'missing' ? 'metadata missing' : status;

    function renderList() {{
      const shown = skills.filter(visible);
      summary.textContent = `${{skills.length}} packages`;
      count.textContent = `${{shown.length}} shown`;
      list.innerHTML = shown.length ? shown.map(skill => `<li><button type="button" role="option" data-name="${{escapeHtml(skill.name)}}" aria-selected="${{skill.name === state.selected}}"><span class="name">${{escapeHtml(skill.name)}}</span><span class="status">${{escapeHtml(label(skill.runtime_status))}}</span></button></li>`).join('') : '<li class="empty-list">No matching skills.</li>';
      list.querySelectorAll('button[data-name]').forEach(button => button.addEventListener('click', () => {{ state.selected = button.dataset.name; render(); }}));
    }}

    function renderDetail() {{
      const skill = skills.find(item => item.name === state.selected);
      if (!skill) {{ detail.innerHTML = '<div class="placeholder"><strong>No skill selected</strong>Select a skill from the catalog.</div>'; return; }}
      const supported = skill.supported || {{}};
      const metadata = Object.entries(supported).map(([key, value]) => `<div><span>${{escapeHtml(key)}}</span><span>${{escapeHtml(value === true ? 'true' : value === false ? 'false' : value)}}</span></div>`).join('');
      detail.innerHTML = `<p class="detail-kicker">Skill package</p><h2>${{escapeHtml(skill.name)}}</h2><p class="description">${{escapeHtml(skill.description || 'Description unavailable.')}}</p><dl><dt>Package</dt><dd><a href="${{escapeHtml(skill.skill_link)}}"><code>${{escapeHtml(skill.package_path)}}</code></a></dd><dt>Runtime metadata</dt><dd class="runtime-${{escapeHtml(skill.runtime_status)}}">${{escapeHtml(label(skill.runtime_status))}}</dd></dl>${{metadata ? `<div class="metadata">${{metadata}}</div>` : ''}}`;
    }}

    function renderGraph() {{
      const shown = skills.filter(visible);
      if (!shown.length) {{ graphCanvas.innerHTML = '<p class="graph-note">No matching skills.</p>'; return; }}
      const width = 900, height = 520, cx = width / 2, cy = height / 2, radius = Math.min(width * .39, height * .39);
      const positions = new Map(shown.map((skill, index) => {{
        const angle = -Math.PI / 2 + (index / shown.length) * Math.PI * 2;
        return [skill.name, {{ x: cx + Math.cos(angle) * radius, y: cy + Math.sin(angle) * radius }}];
      }}));
      const edges = [];
      shown.forEach(skill => (skill.references || []).forEach(reference => {{
        if (positions.has(reference)) edges.push([skill.name, reference]);
      }}));
      const lines = edges.map(([source, target]) => {{
        const from = positions.get(source), to = positions.get(target);
        const active = source === state.selected || target === state.selected ? ' selected' : '';
        return `<line class="graph-line${{active}}" x1="${{from.x}}" y1="${{from.y}}" x2="${{to.x}}" y2="${{to.y}}"><title>${{escapeHtml(source)}} references ${{escapeHtml(target)}}</title></line>`;
      }}).join('');
      const nodes = shown.map(skill => {{
        const point = positions.get(skill.name);
        const selected = skill.name === state.selected ? ' selected' : '';
        const runtime = skill.runtime_status === 'present' ? 'present' : skill.runtime_status === 'missing' ? 'missing' : 'invalid';
        return `<g class="graph-node${{selected}}" data-name="${{escapeHtml(skill.name)}}" role="button" tabindex="0" aria-label="${{escapeHtml(skill.name)}}"><circle cx="${{point.x}}" cy="${{point.y}}" r="7"><title>${{escapeHtml(skill.name)}}</title></circle><circle class="runtime-dot runtime-${{runtime}}" cx="${{point.x + 9}}" cy="${{point.y - 8}}" r="3"></circle><text x="${{point.x}}" y="${{point.y + 24}}" text-anchor="middle">${{escapeHtml(skill.name)}}</text></g>`;
      }}).join('');
      graphCanvas.innerHTML = `<svg viewBox="0 0 ${{width}} ${{height}}" role="img" aria-label="Graph of explicit skill references">${{lines}}${{nodes}}</svg>`;
      graphCanvas.querySelectorAll('.graph-node').forEach(node => {{
        node.addEventListener('click', () => {{ state.selected = node.dataset.name; render(); }});
        node.addEventListener('keydown', event => {{ if (event.key === 'Enter' || event.key === ' ') {{ event.preventDefault(); state.selected = node.dataset.name; render(); }} }});
      }});
    }}

    function render() {{
      renderList();
      renderDetail();
      graphView.hidden = state.view !== 'graph';
      if (state.view === 'graph') renderGraph();
    }}
    search.addEventListener('input', event => {{ state.query = event.target.value.trim().toLowerCase(); render(); }});
    document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {{ state.filter = button.dataset.filter; document.querySelectorAll('[data-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button))); render(); }}));
    document.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => {{ state.view = button.dataset.view; document.querySelectorAll('[data-view]').forEach(item => item.setAttribute('aria-pressed', String(item === button))); render(); }}));
    document.addEventListener('keydown', event => {{ if (event.target === search || !skills.length) return; if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') return; event.preventDefault(); const shown = skills.filter(visible); const index = Math.max(0, shown.findIndex(item => item.name === state.selected)); const next = shown[(index + (event.key === 'ArrowDown' ? 1 : shown.length - 1)) % shown.length]; if (next) {{ state.selected = next.name; render(); list.querySelector(`[data-name="${{CSS.escape(next.name)}}"]`)?.focus(); }} }});
    render();
  </script>
</body>
</html>
'''


def write_catalog(root: Path, output_path: Path | None = None) -> Path:
    root = root.resolve()
    target = (output_path or root / CATALOG_RELATIVE).resolve()
    canonical = (root / CATALOG_RELATIVE).resolve()
    if target != canonical:
        raise ValueError("write mode is limited to agent-skills/SKILL-ARCHITECTURE.md")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(generate_catalog(root), encoding="utf-8")
    return target


def write_html_catalog(root: Path, output_path: Path | None = None) -> Path:
    root = root.resolve()
    target = (output_path or root / HTML_CATALOG_RELATIVE).resolve()
    canonical = (root / HTML_CATALOG_RELATIVE).resolve()
    if target != canonical:
        raise ValueError("write mode is limited to agent-skills/SKILL-ARCHITECTURE.html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(generate_html_catalog(root), encoding="utf-8")
    return target
