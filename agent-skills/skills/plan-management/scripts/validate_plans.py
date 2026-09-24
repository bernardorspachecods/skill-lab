#!/usr/bin/env python3
"""Validate the structural contract for hierarchical Markdown plans."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED_KEYS = {
    "plan_id",
    "kind",
    "parent",
    "phase",
    "status",
    "depends_on",
    "consumers",
}
REQUIRED_SECTIONS = [
    "Objective",
    "Scope",
    "Output",
    "Dependencies",
    "Sequence",
    "Consumers",
    "Completion criteria",
]
ALLOWED_KINDS = {"root", "subplan"}
ALLOWED_STATUSES = {"not_started", "in_progress", "blocked", "complete"}


def parse_scalar(value: str):
    value = value.strip()
    if value in {"", "null", "Null", "NULL", "~"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
    return value.strip("'\"")


def parse_frontmatter(text: str):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    data = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = parse_scalar(value)
    return data, text[match.end() :]


def discover_documents(root: Path, explicit_paths: list[str] | None):
    if explicit_paths:
        documents = []
        for raw_path in explicit_paths:
            path = Path(raw_path)
            if not path.is_absolute():
                path = root / path
            documents.append(path.resolve())
        return sorted(set(documents))

    documents = []
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        lower_parts = {part.lower() for part in relative.parts[:-1]}
        stem = path.stem.lower()
        if "plans" in lower_parts or "plan" in lower_parts or stem == "plan" or stem.startswith("plan_"):
            documents.append(path)
            continue
        try:
            frontmatter, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError):
            continue
        if frontmatter and "plan_id" in frontmatter:
            documents.append(path)
    return sorted(set(documents))


def section_body(markdown: str, title: str):
    heading = re.compile(rf"^##\s+{re.escape(title)}\s*$", re.IGNORECASE | re.MULTILINE)
    match = heading.search(markdown)
    if not match:
        return None
    next_heading = re.search(r"^##\s+", markdown[match.end() :], re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(markdown)
    return markdown[match.end() : end].strip()


def section_position(markdown: str, title: str):
    heading = re.compile(rf"^##\s+{re.escape(title)}\s*$", re.IGNORECASE | re.MULTILINE)
    match = heading.search(markdown)
    return match.start() if match else None


def add_issue(issues, severity, path, message):
    issues.append((severity, path, message))


def normalized_paragraphs(markdown: str):
    without_code = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
    paragraphs = re.split(r"\n\s*\n", without_code)
    results = []
    for paragraph in paragraphs:
        lines = [line.strip() for line in paragraph.splitlines()]
        if not lines or any(line.startswith(("#", "- ", "* ", ">", "|")) for line in lines):
            continue
        value = re.sub(r"\s+", " ", " ".join(lines)).strip().lower()
        if len(value.split()) >= 12:
            results.append(value)
    return results


def validate(root: Path, paths: list[str] | None, strict: bool):
    issues = []
    documents = discover_documents(root, paths)
    if not documents:
        print(f"No plan documents found under {root}")
        return 0

    records = {}
    content_by_path = {}
    paragraphs = defaultdict(list)

    for path in documents:
        label = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
        if not path.exists():
            add_issue(issues, "ERROR", label, "file does not exist")
            continue
        try:
            raw = path.read_text(encoding="utf-8")
            frontmatter, markdown = parse_frontmatter(raw)
        except (OSError, UnicodeDecodeError, ValueError) as error:
            add_issue(issues, "ERROR", label, str(error))
            continue
        content_by_path[path] = markdown
        if frontmatter is None:
            severity = "ERROR" if strict or paths else "WARNING"
            add_issue(issues, severity, label, "missing YAML frontmatter; plan is not using the plan-management contract")
            continue
        missing = REQUIRED_KEYS - set(frontmatter)
        for key in sorted(missing):
            add_issue(issues, "ERROR", label, f"missing frontmatter key: {key}")
        if missing:
            continue

        plan_id = frontmatter["plan_id"]
        if not isinstance(plan_id, str) or not plan_id.strip():
            add_issue(issues, "ERROR", label, "plan_id must be a non-empty string")
            continue
        if plan_id in records:
            add_issue(issues, "ERROR", label, f"duplicate plan_id: {plan_id}")
        records[plan_id] = {"path": path, "label": label, "meta": frontmatter, "markdown": markdown}

        kind = frontmatter["kind"]
        if kind not in ALLOWED_KINDS:
            add_issue(issues, "ERROR", label, f"kind must be one of {sorted(ALLOWED_KINDS)}")
        status = frontmatter["status"]
        if status not in ALLOWED_STATUSES:
            add_issue(issues, "ERROR", label, f"status must be one of {sorted(ALLOWED_STATUSES)}")
        if not isinstance(frontmatter["depends_on"], list):
            add_issue(issues, "ERROR", label, "depends_on must be a list")
        if not isinstance(frontmatter["consumers"], list):
            add_issue(issues, "ERROR", label, "consumers must be a list")
        if kind == "root" and frontmatter["parent"] is not None:
            add_issue(issues, "ERROR", label, "root plans must have parent: null")
        if kind == "subplan" and not isinstance(frontmatter["parent"], str):
            add_issue(issues, "ERROR", label, "subplans must name a parent plan_id")

        for title in REQUIRED_SECTIONS:
            body = section_body(markdown, title)
            if body is None:
                add_issue(issues, "ERROR", label, f"missing required section: {title}")
            elif not body.strip():
                add_issue(issues, "ERROR", label, f"required section is empty: {title}")

        positions = [section_position(markdown, title) for title in REQUIRED_SECTIONS]
        present_positions = [position for position in positions if position is not None]
        if present_positions != sorted(present_positions):
            add_issue(issues, "ERROR", label, "required sections are out of order")

        for target in LINK_RE.findall(markdown):
            clean_target = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not clean_target or clean_target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path = (path.parent / clean_target).resolve()
            if not target_path.exists():
                add_issue(issues, "ERROR", label, f"broken relative link: {target}")

        sequence = section_body(markdown, "Sequence")
        if sequence:
            steps = re.findall(r"^\s*\d+\.\s+", sequence, re.MULTILINE)
            outputs = re.findall(r"\*\*Output:\*\*", sequence, re.IGNORECASE)
            checks = re.findall(r"\*\*Exit check:\*\*", sequence, re.IGNORECASE)
            if not steps:
                add_issue(issues, "ERROR", label, "Sequence must contain an ordered list")
            if len(outputs) != len(steps):
                add_issue(issues, "ERROR", label, "each sequence step must define one Output")
            if len(checks) != len(steps):
                add_issue(issues, "ERROR", label, "each sequence step must define one Exit check")

        for paragraph in normalized_paragraphs(markdown):
            paragraphs[paragraph].append(label)

    children = defaultdict(list)
    for plan_id, record in records.items():
        meta = record["meta"]
        parent = meta["parent"]
        if parent is not None:
            if parent not in records:
                add_issue(issues, "ERROR", record["label"], f"parent plan does not exist: {parent}")
            else:
                children[parent].append(plan_id)
        for dependency in meta["depends_on"] if isinstance(meta["depends_on"], list) else []:
            if isinstance(dependency, str) and dependency.startswith("P") and dependency not in records:
                add_issue(issues, "ERROR", record["label"], f"dependency plan does not exist: {dependency}")

    for plan_id, child_ids in children.items():
        parent = records[plan_id]
        if parent["meta"]["kind"] == "root" and section_body(parent["markdown"], "Plan tree") is None:
            add_issue(issues, "ERROR", parent["label"], "root with subplans must have a Plan tree section")
        for child_id in child_ids:
            child = records[child_id]
            links_to_child = False
            for target in LINK_RE.findall(parent["markdown"]):
                clean_target = target.split("#", 1)[0].split("?", 1)[0]
                if not clean_target:
                    continue
                target_path = (parent["path"].parent / clean_target).resolve()
                if target_path == child["path"].resolve():
                    links_to_child = True
                    break
            if not links_to_child:
                add_issue(issues, "ERROR", parent["label"], f"parent does not link to child {child_id}")

    def visit(plan_id, stack):
        if plan_id in stack:
            cycle = " -> ".join(stack + [plan_id])
            add_issue(issues, "ERROR", records[plan_id]["label"], f"parent cycle: {cycle}")
            return
        for child_id in children.get(plan_id, []):
            visit(child_id, stack + [plan_id])

    for root_id, record in records.items():
        if record["meta"]["kind"] == "root":
            visit(root_id, [])

    for paragraph, labels in paragraphs.items():
        unique_labels = sorted(set(labels))
        if len(unique_labels) > 1:
            add_issue(issues, "WARNING", ", ".join(unique_labels), "repeated paragraph across plans; replace duplication with a link")

    for severity, label, message in sorted(issues):
        print(f"{severity}: {label}: {message}")
    errors = sum(severity == "ERROR" for severity, _, _ in issues)
    warnings = sum(severity == "WARNING" for severity, _, _ in issues)
    print(f"Checked {len(documents)} plan document(s): {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="repository root to inspect")
    parser.add_argument("--path", action="append", help="specific Markdown plan path; repeat as needed")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat existing plan documents without the contract as errors",
    )
    args = parser.parse_args()
    return validate(Path(args.root).resolve(), args.path, args.strict)


if __name__ == "__main__":
    sys.exit(main())
