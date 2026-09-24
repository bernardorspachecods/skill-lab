#!/usr/bin/env python3
"""Validate a temporary delegation execution plan or complete run packet."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED_KEYS = {
    "delegation_id",
    "kind",
    "lifecycle",
    "parent_plan",
    "parent_phase",
    "status",
    "depends_on",
    "consumers",
    "coordinator",
    "review_owner",
}
REQUIRED_SECTIONS = [
    "Objective",
    "Scope",
    "Output",
    "Sequence",
    "Participants and file ownership",
    "Completion criteria",
    "Review contract",
    "Cleanup",
]
ALLOWED_STATUSES = {
    "awaiting_launch",
    "in_progress",
    "awaiting_review",
    "awaiting_application",
    "complete",
    "blocked",
    "cancelled",
}
FINDING_KEYS = {"delegation_id", "kind", "agent_id", "role", "status"}
FINDING_SECTIONS = [
    "Assignment",
    "Assessment",
    "Evidence",
    "Uncertainties",
    "Recommendations",
    "Open questions",
]
FINDING_STATUSES = {
    "awaiting_launch",
    "in_progress",
    "awaiting_phase2",
    "provisional",
    "complete",
    "blocked",
    "cancelled",
}
REVIEW_KEYS = {"delegation_id", "kind", "status", "coordinator"}
REVIEW_SECTIONS = [
    "Coordinator audit",
    "Joint decisions",
    "Applied changes",
    "Unresolved items",
    "Cleanup",
]
REVIEW_STATUSES = {"awaiting_review", "awaiting_application", "complete", "blocked", "cancelled"}


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


def read_document(path: Path, issues):
    label = str(path)
    if not path.exists():
        issues.append(f"ERROR: {label}: file does not exist")
        return None, None
    try:
        raw = path.read_text(encoding="utf-8")
        return parse_frontmatter(raw)
    except (OSError, UnicodeDecodeError, ValueError) as error:
        issues.append(f"ERROR: {label}: {error}")
        return None, None


def validate_sections(path: Path, markdown: str, required_sections, issues):
    label = str(path)
    positions = []
    for title in required_sections:
        body = section_body(markdown, title)
        if body is None:
            issues.append(f"ERROR: {label}: missing required section: {title}")
        elif not body.strip():
            issues.append(f"ERROR: {label}: required section is empty: {title}")
        position = section_position(markdown, title)
        if position is not None:
            positions.append(position)
    if positions != sorted(positions):
        issues.append(f"ERROR: {label}: required sections are out of order")


def validate_links(path: Path, markdown: str, issues):
    label = str(path)
    for target in LINK_RE.findall(markdown):
        clean_target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not clean_target or clean_target.startswith(("http://", "https://", "mailto:")):
            continue
        target_path = (path.parent / clean_target).resolve()
        if not target_path.exists():
            issues.append(f"ERROR: {label}: broken relative link: {target}")


def validate_plan_document(path: Path, issues):
    frontmatter, markdown = read_document(path, issues)
    if frontmatter is None:
        if path.exists():
            issues.append(f"ERROR: {path}: missing YAML frontmatter")
        return None

    label = str(path)
    for key in sorted(REQUIRED_KEYS - set(frontmatter)):
        issues.append(f"ERROR: {label}: missing frontmatter key: {key}")
    if frontmatter.get("kind") != "temporary-execution-plan":
        issues.append(f"ERROR: {label}: kind must be temporary-execution-plan")
    if frontmatter.get("lifecycle") != "temporary":
        issues.append(f"ERROR: {label}: lifecycle must be temporary")
    if frontmatter.get("status") not in ALLOWED_STATUSES:
        issues.append(f"ERROR: {label}: status must be one of {sorted(ALLOWED_STATUSES)}")
    for key in ("depends_on", "consumers"):
        if not isinstance(frontmatter.get(key), list):
            issues.append(f"ERROR: {label}: {key} must be a list")

    validate_sections(path, markdown, REQUIRED_SECTIONS, issues)
    sequence = section_body(markdown, "Sequence")
    if sequence:
        steps = re.findall(r"^\s*\d+\.\s+", sequence, re.MULTILINE)
        outputs = re.findall(r"\*\*Output:\*\*", sequence, re.IGNORECASE)
        checks = re.findall(r"\*\*Exit check:\*\*", sequence, re.IGNORECASE)
        if not steps:
            issues.append(f"ERROR: {label}: Sequence must contain an ordered list")
        if len(outputs) != len(steps):
            issues.append(f"ERROR: {label}: each sequence step needs one Output")
        if len(checks) != len(steps):
            issues.append(f"ERROR: {label}: each sequence step needs one Exit check")
    validate_links(path, markdown, issues)
    return frontmatter


def validate_findings_document(path: Path, delegation_id: str | None, issues):
    frontmatter, markdown = read_document(path, issues)
    if frontmatter is None:
        if path.exists():
            issues.append(f"ERROR: {path}: missing YAML frontmatter")
        return
    label = str(path)
    for key in sorted(FINDING_KEYS - set(frontmatter)):
        issues.append(f"ERROR: {label}: missing frontmatter key: {key}")
    if frontmatter.get("kind") != "finding":
        issues.append(f"ERROR: {label}: kind must be finding")
    if frontmatter.get("status") not in FINDING_STATUSES:
        issues.append(f"ERROR: {label}: status must be one of {sorted(FINDING_STATUSES)}")
    if delegation_id and frontmatter.get("delegation_id") != delegation_id:
        issues.append(f"ERROR: {label}: delegation_id does not match execution plan")
    validate_sections(path, markdown, FINDING_SECTIONS, issues)
    validate_links(path, markdown, issues)


def validate_review_document(path: Path, delegation_id: str | None, issues):
    frontmatter, markdown = read_document(path, issues)
    if frontmatter is None:
        if path.exists():
            issues.append(f"ERROR: {path}: missing YAML frontmatter")
        return
    label = str(path)
    for key in sorted(REVIEW_KEYS - set(frontmatter)):
        issues.append(f"ERROR: {label}: missing frontmatter key: {key}")
    if frontmatter.get("kind") != "review":
        issues.append(f"ERROR: {label}: kind must be review")
    if frontmatter.get("status") not in REVIEW_STATUSES:
        issues.append(f"ERROR: {label}: status must be one of {sorted(REVIEW_STATUSES)}")
    if delegation_id and frontmatter.get("delegation_id") != delegation_id:
        issues.append(f"ERROR: {label}: delegation_id does not match execution plan")
    validate_sections(path, markdown, REVIEW_SECTIONS, issues)
    validate_links(path, markdown, issues)


def validate(path: Path) -> int:
    issues = []
    run_root = path if path.is_dir() else path.parent
    plan_path = run_root / "execution-plan.md" if path.is_dir() else path
    plan_frontmatter = validate_plan_document(plan_path, issues)
    delegation_id = plan_frontmatter.get("delegation_id") if plan_frontmatter else None

    if path.is_dir():
        findings_dir = run_root / "findings"
        if not findings_dir.is_dir():
            issues.append(f"ERROR: {findings_dir}: findings directory does not exist")
        else:
            finding_paths = sorted(findings_dir.glob("*.md"))
            if not finding_paths:
                issues.append(f"ERROR: {findings_dir}: no findings files found")
            for finding_path in finding_paths:
                validate_findings_document(finding_path, delegation_id, issues)
        validate_review_document(run_root / "review.md", delegation_id, issues)

    for issue in sorted(issues):
        print(issue)
    errors = sum(issue.startswith("ERROR:") for issue in issues)
    label = "temporary delegation packet" if path.is_dir() else "temporary delegation plan"
    print(f"Checked {label}: {errors} error(s)")
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="execution-plan.md or its run directory")
    args = parser.parse_args()
    path = Path(args.path).resolve()
    return validate(path)


if __name__ == "__main__":
    sys.exit(main())
