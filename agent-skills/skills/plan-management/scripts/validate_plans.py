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
    "Sequence",
    "Completion criteria",
]
ALLOWED_KINDS = {"root", "subplan"}
ALLOWED_STATUSES = {"not_started", "in_progress", "blocked", "complete"}
EXECUTION_DIMENSIONS = {
    "research",
    "root_research",
    "research_working",
    "review",
    # Accept the legacy field while old plans are migrated. New plans omit it.
    "delegation",
    "user_checkpoints",
}
REQUIRED_EXECUTION_DIMENSIONS = EXECUTION_DIMENSIONS - {
    "research_working",
    "root_research",
    "delegation",
}
USER_CHECKPOINTS = {"each_handoff", "each_subplan", "plan_completion"}
ARTIFACT_FILENAME_RE = re.compile(
    r"^(?P<entity>(?:LR-\d{2,}\.)?(?:RES|REV)-\d{2,})\.(?P<role>working|audit|assessment|perspective-\d{2,})$"
)
PLAN_ID_RE = re.compile(r"^LR-\d{2,}(?:\.SP-\d{2,})?$")
SUBPLAN_ID_RE = re.compile(r"^LR-\d{2,}\.SP-\d{2,}$")
STABLE_ID_RE = re.compile(r"^(?:LR-\d{2,}(?:\.SP-\d{2,})?(?:\.[A-Za-z][A-Za-z0-9-]*)?|(?:LR-\d{2,}\.)?KNOW-\d{2,})$")
ID_REFERENCE_RE = re.compile(r"(?<![A-Za-z0-9_-])((?:LR-\d{2,}(?:\.SP-\d{2,})?(?:\.[A-Za-z][A-Za-z0-9-]*)?|(?:LR-\d{2,}\.)?KNOW-\d{2,}))(?:#([A-Za-z0-9_-]+))?")


def parse_scalar(value: str):
    value = value.strip()
    if value in {"", "null", "Null", "NULL", "~"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return value.strip("'\"")


def parse_frontmatter(text: str):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    data = {}
    stack = [(-1, data, None, None)]
    for line_number, line in enumerate(match.group(1).splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        sequence_item = re.match(r"^\s*-\s+(.*)$", line)
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise ValueError(f"invalid frontmatter indentation on line {line_number}")
        container = stack[-1][1]
        if container is None:
            _, _, parent, key = stack[-1]
            container = [] if sequence_item else {}
            parent[key] = container
            stack[-1] = (stack[-1][0], container, parent, key)
        if sequence_item:
            if not isinstance(container, list):
                raise ValueError(f"unexpected sequence item on frontmatter line {line_number}")
            container.append(parse_scalar(sequence_item.group(1)))
            continue
        if ":" not in line or not isinstance(container, dict):
            raise ValueError(f"invalid frontmatter line {line_number}: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        parent = container
        if key in parent:
            raise ValueError(f"duplicate frontmatter key on line {line_number}: {key}")
        parsed = parse_scalar(value)
        parent[key] = None if parsed is None and not value.strip() else parsed
        if parent[key] is None or isinstance(parent[key], dict):
            stack.append((indent, parent[key], parent, key))
    return data, text[match.end() :]


def validate_execution(value, label, field, issues, *, root):
    if not isinstance(value, dict):
        add_issue(issues, "ERROR", label, f"{field} must be a mapping")
        return
    keys = set(value)
    unknown = keys - EXECUTION_DIMENSIONS
    if unknown:
        add_issue(issues, "ERROR", label, f"{field} has unknown dimension(s): {', '.join(sorted(unknown))}")
    if root:
        missing = REQUIRED_EXECUTION_DIMENSIONS - keys
        if missing:
            add_issue(issues, "ERROR", label, f"execution is missing dimension(s): {', '.join(sorted(missing))}")
    elif not keys:
        add_issue(issues, "ERROR", label, "execution_exception must name at least one local override")
    for dimension, setting in value.items():
        if not root and dimension == "root_research":
            add_issue(issues, "ERROR", label, "execution_exception cannot override root_research")
        if dimension == "research":
            valid = setting is False or (isinstance(setting, str) and bool(setting.strip()))
            expected = "false or a non-empty string (setting names are owned by the research skill)"
        elif dimension == "root_research":
            valid = setting is False or (isinstance(setting, str) and bool(setting.strip()))
            expected = "false or a non-empty string (setting names are owned by the research skill)"
        elif dimension == "user_checkpoints":
            valid = isinstance(setting, str) and setting in USER_CHECKPOINTS
            expected = f"one of {', '.join(sorted(USER_CHECKPOINTS))}"
        elif dimension == "delegation":
            valid = setting is True
            expected = "true (implementation is always assigned to agents)"
        else:
            valid = isinstance(setting, bool)
            expected = "a boolean"
        if not valid:
            add_issue(issues, "ERROR", label, f"{field}.{dimension} must be {expected}")


def heading_anchors(markdown: str) -> set[str]:
    anchors = set()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", markdown, re.MULTILINE):
        plain = re.sub(r"`([^`]*)`", r"\1", heading)
        plain = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", plain)
        anchor = re.sub(r"[^\w -]", "", plain.lower(), flags=re.UNICODE)
        anchor = re.sub(r"\s+", "-", anchor.strip())
        anchors.add(anchor)
    return anchors


def build_id_index(root: Path, issues):
    """Index plan, artifact, and knowledge IDs without writing a location map."""
    index = defaultdict(list)
    for path in root.rglob("*.md"):
        relative_parts = {part.lower() for part in path.relative_to(root).parts[:-1]}
        if relative_parts & {".git", "node_modules"}:
            continue
        try:
            raw = path.read_text(encoding="utf-8")
            frontmatter, markdown = parse_frontmatter(raw)
        except (OSError, UnicodeDecodeError, ValueError):
            continue
        ids = set()
        if frontmatter and isinstance(frontmatter.get("plan_id"), str):
            ids.add(frontmatter["plan_id"])
        stem = path.stem
        if STABLE_ID_RE.fullmatch(stem):
            ids.add(stem)
        for suffix in (".PLAN",):
            if stem.endswith(suffix) and STABLE_ID_RE.fullmatch(stem[:-len(suffix)]):
                ids.add(stem[:-len(suffix)])
        artifact_match = ARTIFACT_FILENAME_RE.match(stem)
        if artifact_match:
            ids.add(artifact_match.group("entity"))
        anchors = heading_anchors(markdown)
        for stable_id in ids:
            index[stable_id].append((path, anchors))
    return index


def validate_reference(reference: str, label: str, index, issues, *, require_anchor_exists=True):
    match = ID_REFERENCE_RE.fullmatch(reference)
    if not match:
        add_issue(issues, "ERROR", label, f"invalid stable ID reference: {reference}")
        return
    stable_id, anchor = match.groups()
    targets = index.get(stable_id, [])
    if not targets:
        add_issue(issues, "ERROR", label, f"stable ID does not resolve: {stable_id}")
    elif anchor and require_anchor_exists and not any(anchor in anchors for _, anchors in targets):
        add_issue(issues, "ERROR", label, f"anchor does not resolve for {stable_id}: #{anchor}")


def validate_artifacts(root: Path, records, issues, id_index, known_plan_ids, scan_roots=None):
    artifact_records = {}
    paths = root.rglob("*.md")
    if scan_roots:
        paths = (path for path in paths if any(path.is_relative_to(scan_root) for scan_root in scan_roots))
    for path in paths:
        match = ARTIFACT_FILENAME_RE.match(path.stem)
        relative_parts = {part.lower() for part in path.relative_to(root).parts[:-1]}
        in_workflow_area = bool(relative_parts & {"research", "reviews", "knowledge"})
        if not match and not in_workflow_area:
            continue
        label = str(path.relative_to(root))
        try:
            raw = path.read_text(encoding="utf-8")
            frontmatter, _ = parse_frontmatter(raw)
        except (OSError, UnicodeDecodeError, ValueError) as error:
            add_issue(issues, "ERROR", label, str(error))
            continue
        if match:
            artifact_id = path.stem
            if artifact_id in artifact_records:
                add_issue(issues, "ERROR", label, f"duplicate artifact ID: {artifact_id}")
            artifact_records[artifact_id] = label
            if frontmatter is None:
                add_issue(issues, "ERROR", label, "workflow artifact is missing YAML frontmatter")
                continue
            role = match.group("role")
            expected_owner = match.group("entity")
            owner = frontmatter.get("belongs_to")
            if owner != expected_owner:
                add_issue(issues, "ERROR", label, f"belongs_to must be {expected_owner} for this artifact")
            requester_required = role in {"audit", "assessment"}
            requester = frontmatter.get("requested_by")
            if requester_required:
                if not isinstance(requester, str) or not requester:
                    add_issue(issues, "ERROR", label, "requested_by must name the requesting plan")
                elif requester not in known_plan_ids:
                    add_issue(issues, "ERROR", label, f"requested_by plan does not exist: {requester}")
                elif expected_owner.startswith("LR-") and requester.split(".", 1)[0] != expected_owner.split(".", 1)[0]:
                    add_issue(issues, "ERROR", label, "requested_by and artifact identity must belong to the same root plan")
                elif requester in records:
                    requester_meta = records[requester]["meta"]
                    requester_path = records[requester]["path"]
                    expected_area = "research" if expected_owner.split(".")[-1].startswith("RES-") else "reviews"
                    valid_locations = {
                        requester_path.parent.resolve(),
                        (requester_path.parent / expected_area).resolve(),  # legacy layout
                    }
                    if path.parent.resolve() not in valid_locations:
                        add_issue(issues, "ERROR", label, "workflow artifacts must be stored beside the requesting plan")
                    if requester_meta.get("kind") == "root":
                        execution = requester_meta.get("execution") or {}
                        if "root_research" in execution and role == "audit" and execution.get("root_research") is False:
                            add_issue(issues, "ERROR", label, "root research artifacts require an explicit root_research setting")
                        if "root_research" in execution and role == "assessment":
                            add_issue(issues, "ERROR", label, "formal reviews belong to subplan outputs; root plan integrity checks are temporary")
            if role == "assessment":
                for key in ("targets", "criteria_refs"):
                    value = frontmatter.get(key)
                    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item for item in value):
                        add_issue(issues, "ERROR", label, f"{key} must be a non-empty list of stable IDs or ID#anchor references")
                    elif isinstance(value, list):
                        for reference in value:
                            if isinstance(reference, str) and reference:
                                validate_reference(reference, label, id_index, issues)
        elif "knowledge" in relative_parts and path.name.lower() not in {"index.md", "readme.md"}:
            subplan_ancestor = next(
                (part for part in path.relative_to(root).parts[:-1] if SUBPLAN_ID_RE.fullmatch(part)),
                None,
            )
            if subplan_ancestor:
                add_issue(issues, "ERROR", label, "plan-local knowledge belongs in the root plan's knowledge/ directory, shared with its subplans")
            sources = frontmatter.get("derived_from") if frontmatter else None
            if not isinstance(sources, list) or not sources or any(not isinstance(item, str) or not item for item in sources):
                add_issue(issues, "ERROR", label, "knowledge entries must declare derived_from as a non-empty list of source artifact IDs")
            elif isinstance(sources, list):
                for reference in sources:
                    if isinstance(reference, str) and reference:
                        validate_reference(reference, label, id_index, issues)
    return artifact_records


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
        in_workflow_area = bool(lower_parts & {"research", "reviews", "knowledge"})
        is_workflow_artifact = ARTIFACT_FILENAME_RE.fullmatch(path.stem) is not None
        if stem == "plan-integrity-check":
            continue
        if not in_workflow_area and not is_workflow_artifact and (
            "plans" in lower_parts or "plan" in lower_parts or stem == "plan" or stem.startswith("plan_")
        ):
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
    id_index = build_id_index(root, issues)
    known_plan_ids = {stable_id for stable_id in id_index if PLAN_ID_RE.fullmatch(stable_id)}

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
        if kind == "root":
            execution = frontmatter.get("execution")
            if execution is None:
                severity = "ERROR" if PLAN_ID_RE.fullmatch(plan_id) else "WARNING"
                add_issue(issues, severity, label, "root plan is missing execution defaults")
            else:
                validate_execution(execution, label, "execution", issues, root=True)
            if "execution_exception" in frontmatter:
                add_issue(issues, "ERROR", label, "root plans must use execution, not execution_exception")
        else:
            if "execution" in frontmatter:
                add_issue(issues, "ERROR", label, "subplans inherit execution; use execution_exception for local overrides")
            if "execution_exception" in frontmatter:
                validate_execution(frontmatter["execution_exception"], label, "execution_exception", issues, root=False)

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
            link_path, separator, raw_anchor = target.partition("#")
            clean_target = unquote(link_path.split("?", 1)[0])
            if clean_target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path = (path.parent / clean_target).resolve() if clean_target else path.resolve()
            if not target_path.exists():
                add_issue(issues, "ERROR", label, f"broken relative link: {target}")
            elif separator and raw_anchor:
                try:
                    target_markdown = target_path.read_text(encoding="utf-8")
                    _, target_body = parse_frontmatter(target_markdown)
                    if unquote(raw_anchor) not in heading_anchors(target_body):
                        add_issue(issues, "ERROR", label, f"broken relative link anchor: {target}")
                except (OSError, UnicodeDecodeError, ValueError):
                    add_issue(issues, "ERROR", label, f"cannot inspect link target: {target}")

        reference_body = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
        reference_body = re.sub(r"`[^`]*`", "", reference_body)
        for reference in ID_REFERENCE_RE.finditer(reference_body):
            validate_reference(reference.group(0), label, id_index, issues)

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
            if parent not in known_plan_ids:
                add_issue(issues, "ERROR", record["label"], f"parent plan does not exist: {parent}")
            elif parent in records:
                children[parent].append(plan_id)
        for dependency in meta["depends_on"] if isinstance(meta["depends_on"], list) else []:
            if not isinstance(dependency, str) or not dependency.strip():
                add_issue(issues, "ERROR", record["label"], "depends_on entries must be non-empty output artifact IDs")
            elif dependency in records:
                add_issue(issues, "ERROR", record["label"], f"depends_on must reference an output artifact ID, not a plan ID: {dependency}")
            else:
                validate_reference(dependency, record["label"], id_index, issues)

    artifact_scan_roots = None
    if paths:
        artifact_scan_roots = set()
        for document in documents:
            ancestors = (document.parent, *document.parent.parents)
            plan_root = next(
                (ancestor for ancestor in ancestors if ancestor != root.parent and re.fullmatch(r"LR-\d{2,}", ancestor.name)),
                document.parent,
            )
            artifact_scan_roots.add(plan_root)
    validate_artifacts(root, records, issues, id_index, known_plan_ids, artifact_scan_roots)

    for plan_id, child_ids in children.items():
        parent = records[plan_id]
        sequence = section_body(parent["markdown"], "Sequence") or ""
        for child_id in child_ids:
            child = records[child_id]
            links_to_child = False
            for target in LINK_RE.findall(sequence):
                clean_target = target.split("#", 1)[0].split("?", 1)[0]
                if not clean_target:
                    continue
                target_path = (parent["path"].parent / clean_target).resolve()
                if target_path == child["path"].resolve():
                    links_to_child = True
                    break
            if not links_to_child:
                add_issue(issues, "ERROR", parent["label"], f"Sequence does not link to child {child_id}")

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
