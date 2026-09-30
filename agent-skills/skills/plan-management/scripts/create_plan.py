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
        root_research = execution.get("root_research", False)
        root_research_value = (
            yaml_scalar(root_research)
            if isinstance(root_research, str)
            else str(root_research).lower()
        )
        lines.append(f"  root_research: {root_research_value}")
        lines.append(f"  research_working: {str(execution.get('research_working', False)).lower()}")
        lines.append(f"  review: {str(execution['review']).lower()}")
        lines.append(f"  user_checkpoints: {execution['user_checkpoints']}")
    lines.append("---")
    return "\n".join(lines)


def sequence_section(subplans: list[tuple[str, str]] | None = None) -> str:
    subplans = subplans or []
    steps = []
    for index in range(1, max(len(subplans), 1) + 1):
        phase_link = ""
        if index <= len(subplans):
            child_id, folder = subplans[index - 1]
            phase_link = f" ([{child_id}](subplans/{folder}/PLAN.md))"
        steps.append(
            f"{index}. **S{index} — [phase name]**{phase_link}\n"
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
        ("Sequence", sequence_section(subplans)),
        ("Completion criteria", "[To be completed by the coordinating agent.]"),
    ]
    if kind == "root":
        current_phase_prompt = (
            "[Active phase; pending decision or handoff; next action. "
            "If blocked, name what will unblock it.]"
        )
        sections.insert(
            3,
            ("Current phase", current_phase_prompt),
        )
    else:
        sections.append(("Outcome", "[Record completion, verification, and material differences when the unit is complete.]"))
    body = "\n\n".join(f"## {heading}\n\n{content}" for heading, content in sections)
    return f"{plan_frontmatter(plan_id, kind, parent, phase, execution)}\n\n# {plan_id}\n\n{body}\n"


def research_artifacts(unit_dir: Path, research_id: str, requested_by: str,
                       retain_working: bool = False) -> dict[Path, str]:
    base = unit_dir
    audit = (
        f"---\nbelongs_to: {research_id}\nrequested_by: {requested_by}\n---\n\n"
        "# Audit\n\n## Question\n\n## Claims and evidence\n\n## Sources\n\n## Conflicts and limitations\n\n## Validation\n"
    )
    artifacts = {base / f"{research_id}.audit.md": audit}
    if retain_working:
        working = f"---\nbelongs_to: {research_id}\n---\n\n# Working\n"
        artifacts[base / f"{research_id}.working.md"] = working
    return artifacts


def review_artifact(unit_dir: Path, review_id: str, requested_by: str) -> dict[Path, str]:
    base = unit_dir
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
        generated: dict[Path, str] = {}
        root_dir = destination / root_id
        generated[root_dir / "PLAN.md"] = plan_document(root_id, "root", None, "root", execution, child_records)
        generated[root_dir / "knowledge" / ".keep"] = ""
        for index, (child_id, folder) in enumerate(child_records, start=1):
            child_dir = root_dir / "subplans" / folder
            generated[child_dir / "PLAN.md"] = plan_document(child_id, "subplan", root_id, f"S{index}", None)
        if execution.get("root_research", False) is not False:
            research_id = ids.reserve("RES", root_id)
            generated.update(research_artifacts(
                root_dir, research_id, root_id, execution.get("research_working", False)
            ))
        for child_id, folder in child_records:
            unit_dir = root_dir / "subplans" / folder
            if execution["research"] is not False:
                research_id = ids.reserve("RES", root_id)
                generated.update(research_artifacts(
                    unit_dir, research_id, child_id, execution.get("research_working", False)
                ))
            if execution["review"]:
                review_id = ids.reserve("REV", root_id)
                generated.update(review_artifact(unit_dir, review_id, child_id))
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
    parser.add_argument(
        "--research",
        required=True,
        help="false or a research setting defined by the research skill, for subplans",
    )
    parser.add_argument(
        "--root-research",
        default="false",
        help="false unless root research was explicitly requested; otherwise a research setting",
    )
    parser.add_argument(
        "--research-working",
        type=parse_bool,
        required=True,
        help="whether to retain a working log artifact for each research assignment",
    )
    parser.add_argument(
        "--review",
        type=parse_bool,
        required=True,
        help="whether completed subplan outputs receive formal review",
    )
    parser.add_argument(
        "--user-checkpoints",
        choices=("each_handoff", "each_subplan", "plan_completion"),
        required=True,
        help="when to pause for user review of delegated work",
    )
    args = parser.parse_args()
    repository = args.repository.resolve()
    if not repository.is_dir():
        parser.error(f"repository does not exist or is not a directory: {repository}")
    if args.subplans < 0:
        parser.error("--subplans must be zero or greater")
    if not args.research.strip():
        parser.error("--research must be false or a non-empty setting defined by the research skill")
    if not args.root_research.strip():
        parser.error("--root-research must be false or a non-empty setting defined by the research skill")
    if args.research == "false" and args.root_research == "false" and args.research_working:
        parser.error("--research-working must be false when research is disabled for the root and subplans")
    destination = (args.destination or repository / "plans").resolve()
    try:
        root_dir = scaffold(repository, destination, args.subplans, {
            "research": False if args.research == "false" else args.research,
            "root_research": False if args.root_research == "false" else args.root_research,
            "research_working": args.research_working,
            "review": args.review,
            "user_checkpoints": args.user_checkpoints,
        })
    except (FileExistsError, OSError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Created plan scaffold: {root_dir}")
    print("Complete the TODO content and review targets/criteria before validating.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
