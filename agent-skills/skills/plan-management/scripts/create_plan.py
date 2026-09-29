#!/usr/bin/env python3
"""Scaffold a durable plan and its selected workflow artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from artifact_ids import IdReservationSession


def yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def plan_frontmatter(plan_id: str, kind: str, parent: str | None, phase: str, execution: dict | None = None) -> str:
    lines = [
        "---",
        f"plan_id: {plan_id}",
        f"kind: {kind}",
        f"parent: {parent if parent else 'null'}",
        f"phase: {phase}",
        "status: not_started",
        "depends_on: []",
        "consumers: []",
    ]
    if execution is not None:
        lines.append("execution:")
        lines.append(f"  research: {yaml_scalar(execution['research']) if isinstance(execution['research'], str) else str(execution['research']).lower()}")
        lines.append(f"  review: {str(execution['review']).lower()}")
        lines.append(f"  delegation: {str(execution['delegation']).lower()}")
    lines.append("---")
    return "\n".join(lines)


def sequence_section(count: int) -> str:
    steps = []
    for index in range(1, max(count, 1) + 1):
        steps.append(
            f"{index}. **S{index} — [phase name]**\n"
            "   - **Action:** [to be completed]\n"
            "   - **Output:** [to be completed]\n"
            "   - **Exit check:** [to be completed]"
        )
    return "\n\n".join(steps)


def plan_document(plan_id: str, kind: str, parent: str | None, phase: str, execution: dict | None,
                  subplans: list[tuple[str, str]] | None = None) -> str:
    subplans = subplans or []
    sections = [
        ("Objective", "[To be completed by the coordinating agent.]"),
        ("Scope", "[To be completed by the coordinating agent.]"),
        ("Output", "[To be completed by the coordinating agent.]"),
        ("Plan tree", "\n".join(f"- [{child_id}](subplans/{folder}/PLAN.md)" for child_id, folder in subplans)
         if subplans else "No subplans are scaffolded."),
        ("Sequence", sequence_section(len(subplans)) if subplans else sequence_section(1)),
        ("Completion criteria", "[To be completed by the coordinating agent.]"),
    ]
    if kind == "root":
        sections.insert(4, ("Current phase", "[To be completed by the coordinating agent.]"))
    else:
        sections.append(("Outcome", "[Record completion, verification, and material differences when the unit is complete.]"))
    body = "\n\n".join(f"## {heading}\n\n{content}" for heading, content in sections)
    return f"{plan_frontmatter(plan_id, kind, parent, phase, execution)}\n\n# {plan_id}\n\n{body}\n"


def research_artifacts(unit_dir: Path, research_id: str, requested_by: str) -> dict[Path, str]:
    base = unit_dir / "research"
    belongs_to = f"{research_id}"
    working = f"---\nbelongs_to: {belongs_to}\n---\n\n# Working\n"
    audit = (
        f"---\nbelongs_to: {belongs_to}\nrequested_by: {requested_by}\n---\n\n"
        "# Audit\n\n## Question\n\n## Claims and evidence\n\n## Sources\n\n## Conflicts and limitations\n\n## Validation\n"
    )
    return {base / f"{research_id}.working.md": working, base / f"{research_id}.audit.md": audit}


def review_artifact(unit_dir: Path, review_id: str, requested_by: str) -> dict[Path, str]:
    base = unit_dir / "reviews"
    assessment = (
        f"---\nbelongs_to: {review_id}\nrequested_by: {requested_by}\n"
        "targets: []\ncriteria_refs: []\n---\n\n"
        "# Assessment\n\n## Conclusions\n\n## Evidence\n\n## Uncertainties\n\n## Recommendations\n"
    )
    return {base / f"{review_id}.assessment.md": assessment}


def scaffold(repository: Path, destination: Path, subplan_count: int, execution: dict) -> Path:
    with IdReservationSession(repository) as ids:
        root_id = ids.reserve("LR")
        child_records = []
        for _ in range(subplan_count):
            child_id = ids.reserve("SP", root_id)
            child_records.append((child_id, child_id))
        unit_records = [(root_id, destination / root_id)]
        unit_records.extend((child_id, destination / root_id / "subplans" / folder) for child_id, folder in child_records)
        generated: dict[Path, str] = {}
        root_dir = destination / root_id
        generated[root_dir / "PLAN.md"] = plan_document(root_id, "root", None, "root", execution, child_records)
        generated[root_dir / "knowledge" / ".keep"] = ""
        for index, (child_id, folder) in enumerate(child_records, start=1):
            child_dir = root_dir / "subplans" / folder
            generated[child_dir / "PLAN.md"] = plan_document(child_id, "subplan", root_id, f"S{index}", None)
        for unit_id, unit_dir in unit_records:
            if execution["research"] is not False:
                research_id = ids.reserve("RES", root_id)
                generated.update(research_artifacts(unit_dir, research_id, unit_id))
            if execution["review"]:
                review_id = ids.reserve("REV", root_id)
                generated.update(review_artifact(unit_dir, review_id, unit_id))
        destination.mkdir(parents=True, exist_ok=True)
        collisions = [str(path) for path in generated if path.exists()]
        if root_dir.exists():
            collisions.append(str(root_dir))
        if collisions:
            raise FileExistsError("refusing to overwrite existing files: " + ", ".join(collisions))
        for path, content in generated.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return root_dir


def parse_bool(value: str) -> bool:
    if value == "true":
        return True
    if value == "false":
        return False
    raise argparse.ArgumentTypeError("choose true or false")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path, help="repository where the plan will live")
    parser.add_argument("--destination", type=Path, help="plan parent directory; defaults to <repository>/plans")
    parser.add_argument("--subplans", type=int, required=True, help="number of subplans to scaffold")
    parser.add_argument("--research", required=True, help="false or a research setting defined by the research skill")
    parser.add_argument("--review", type=parse_bool, required=True, help="whether review gates are enabled")
    parser.add_argument("--delegation", type=parse_bool, required=True, help="whether delegation is enabled")
    args = parser.parse_args()
    repository = args.repository.resolve()
    if not repository.is_dir():
        parser.error(f"repository does not exist or is not a directory: {repository}")
    if args.subplans < 0:
        parser.error("--subplans must be zero or greater")
    if not args.research.strip():
        parser.error("--research must be false or a non-empty setting defined by the research skill")
    destination = (args.destination or repository / "plans").resolve()
    try:
        root_dir = scaffold(repository, destination, args.subplans, {
            "research": False if args.research == "false" else args.research,
            "review": args.review,
            "delegation": args.delegation,
        })
    except (FileExistsError, OSError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Created plan scaffold: {root_dir}")
    print("Complete the TODO content and review targets/criteria before validating.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
