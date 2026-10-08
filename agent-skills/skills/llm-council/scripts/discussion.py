#!/usr/bin/env python3
"""Scaffold and validate version-controlled LLM Council discussion artifacts."""

from __future__ import annotations

import argparse
import hashlib
import random
import re
import sys
from pathlib import Path

ADVISORS = (
    "contrarian",
    "first-principles",
    "expansionist",
    "outsider",
    "executor",
)
REVIEWERS = tuple(f"reviewer-{number:02d}" for number in range(1, 6))
TODO_MARKER = "<!-- COUNCIL-TODO:"
PACKET_MARKER = "<!-- COUNCIL-GENERATED: run prepare-review to fill this file -->"
KEY_MARKER = "<!-- COUNCIL-GENERATED: run prepare-review to fill this file -->"
RESPONSE_START = "<!-- COUNCIL-RESPONSE-START -->"
RESPONSE_END = "<!-- COUNCIL-RESPONSE-END -->"

ADVISOR_PERSPECTIVES = {
    "contrarian": "Look for what is wrong, missing, or likely to fail. Assume the proposal may have a serious flaw and test it. Be rigorous, not reflexively negative.",
    "first-principles": "Identify the underlying problem, examine assumptions, and rebuild the question from its foundations. Say when the user may be asking the wrong question.",
    "expansionist": "Look for upside, overlooked opportunities, and what could become possible if the idea works. Focus on growth and potential.",
    "outsider": "Respond only to the supplied brief. Look for confusing assumptions, unexplained terms, and gaps that an informed newcomer would notice.",
    "executor": "Assess whether the idea can be carried out and identify the fastest concrete first step. Focus on practical action.",
}

ADVISOR_ANALYSIS_PROMPT = """Analyze the question independently from your assigned perspective. Do not assume another advisor will correct unsupported claims or fill gaps in your analysis. Do not stop at the first plausible answer. Examine the underlying decision, the assumptions in the brief, plausible alternatives, their material tradeoffs and failure modes, and the strongest objection to your preferred position. Consider what evidence or changed condition would alter your conclusion.

If the answer materially depends on current, specialized, or empirical facts that the brief does not supply, conduct focused research to resolve that gap. Prefer primary or authoritative sources where appropriate, cite sources for material factual claims, and distinguish what a source establishes from your inference. Do not research merely to decorate a judgment that does not depend on external facts. If research cannot resolve a gap, state the uncertainty.

Return a substantive analysis, not just a quick conclusion. There is no word limit: give enough reasoning to make the tradeoffs, assumptions, evidence, and limitations clear, while avoiding repetition. Do not identify yourself by role in the response; the coordinator tracks roles separately.

Write your response only between the response markers below, preserving all assignment instructions outside them. Return:
1. Position: your conclusion and confidence, with the conditions that matter.
2. Analysis: the strongest supporting reasons, comparison with plausible alternatives, material tradeoffs, and relevant failure modes.
3. Strongest counterargument: the best case against your position and what evidence or condition could change your conclusion.
4. Key risk or opportunity: the most important point from your perspective.
5. Evidence and assumptions: distinguish facts from inference; state material assumptions, missing information, and any research sources used."""

REVIEWER_PROMPT = """Independently review the council question and five anonymized advisor responses in the packet path listed below. Do not try to identify the advisors, and do not assume a response is correct because it is confident.

Answer all three questions specifically and refer to responses by letter:
1. Which response is strongest, and why?
2. Which response has the biggest blind spot, and what is it missing?
3. What did all five responses miss that the council should consider?

Keep the review under 200 words. Do not see or request other reviewers' files. Write your review only between the response markers below, preserving all assignment instructions outside them."""

CHAIRMAN_PROMPT = """Synthesize the council brief, five identified advisor responses, five independent peer reviews, and advisor-to-letter key listed above into a standalone report for the user.

The report is the user-facing deliverable and should answer the question without requiring the user to open the source files in most cases. Summarize each advisor's substantive position, strongest reasons, and material caveats; include relative links to all five response sections (for example, `02-advisors/contrarian.md#response`). Integrate useful peer-review findings into the synthesis, tradeoffs, recommendation, or caveats; do not present review feedback as a separate process-only section. Link peer-review findings to the relevant review section (for example, `03-peer-review/reviewer-01.md#response`) when their source matters. Links support the report and do not replace its analysis.

The chairman synthesizes the evidence; it does not count votes. Distinguish independent advisor agreement from reviewer agreement. Treat peer reviews as critiques to assess, not votes to follow. Preserve genuine disagreements, material assumptions, and limitations. Give a direct recommendation whose confidence matches the supplied reasoning and context. Make labels understandable: pair any A–E label with the mapped advisor perspective/name, and identify reviewer numbers as peer reviews with their finding. Prefer summarizing the substance or count of the five reviews when individual reviewer identity is immaterial.

Write the entire report only between the response markers below, preserving all assignment instructions outside them. Use these headings in order:

# Council Report: [Short topic]

## Executive Summary
[Direct answer and recommendation, with confidence and the main reason.]

## Advisor Perspectives
[Cover each advisor by perspective/name. Summarize their position, substantive reasons, and material risk, assumption, or caveat. Link each full response.]

## Synthesis and Tradeoffs
[Explain meaningful agreements and disagreements, compare the strongest considerations, and integrate material peer-review findings with links where useful. Do not narrate the review stage as an intermediate step.]

## Recommendation
[Give the recommendation, its rationale, relevant conditions, and practical implications. Include a next action only when it materially helps the user act.]

## Evidence, Assumptions, and Limits
[Distinguish sourced facts from inference and judgment. State material assumptions, uncertainty, and limits that affect the recommendation.]

Use relative Markdown links from the discussion-root report to advisor response sections in `02-advisors/` and peer-review sections in `03-peer-review/`."""

COMPLETENESS_PROMPT = """Compare the draft report with all source material listed above. This is a source-to-report fidelity check, not a request to rewrite or improve the recommendation.

Check whether the report omits or distorts any material advisor argument, independent agreement, disagreement, assumption, limitation, peer-review finding, or necessary context. Check for claims unsupported by sources. Peer-review findings may be integrated into the agreement, clashes, or recommendation; a separate section is not required. A synthesis need not preserve every sentence; it must preserve all material information needed to understand the council's reasoning and recommendation.

Check that every A–E advisor label is paired with its mapped advisor perspective/name, and every reviewer number is identified as a peer review with the relevant finding. A count must state that it refers to the five peer reviews. No letter or number should appear without a clear referent. Verify that each advisor's material position, strongest reasons, and important caveats are summarized in the report, with a working relative Markdown link to its response section. Verify source links and the incorporation of material peer-review findings. Links are for further inspection, not a substitute for missing analysis.

Write a compact coverage table with source, material point, report location, and status (`covered`, `distorted`, or `missing`). End with exactly one status line: `Status: PASS` or `Status: REVISE`. Write the audit only between the response markers below, preserving all assignment instructions outside them."""


def repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def with_response_section(assignment: str, scaffold: str) -> str:
    return (
        assignment.rstrip()
        + "\n\n"
        + "## Response\n\n"
        + RESPONSE_START
        + "\n"
        + f"{TODO_MARKER} Replace this scaffold with your assigned response. -->\n\n"
        + scaffold.strip()
        + "\n"
        + RESPONSE_END
        + "\n"
    )


def advisor_template(name: str) -> str:
    title = name.replace("-", " ").title()
    assignment = f"""# Advisor Assignment: The {title}

Artifact paths in this assignment are relative to the discussion folder (the parent of the phase folders). Read only this assignment and `01-brief/brief.md`. You may conduct focused external research as directed below. Do not inspect other agents' files or unrelated workspace files. You may write only in the response section of this file.

## Perspective

{ADVISOR_PERSPECTIVES[name]}

## Task

{ADVISOR_ANALYSIS_PROMPT}"""
    scaffold = (
        "## Position\n\n"
        "## Analysis\n\n"
        "## Strongest counterargument\n\n"
        "## Key risk or opportunity\n\n"
        "## Evidence and assumptions"
    )
    return with_response_section(assignment, scaffold)


def reviewer_template(number: int) -> str:
    assignment = f"""# Peer Review Assignment: Reviewer {number:02d}

Artifact paths in this assignment are relative to the discussion folder (the parent of the phase folders). Read only this assignment and `03-peer-review/anonymized-responses.md`. Do not inspect or request other reviewers' files. You may write only in the response section of this file.

## Task

{REVIEWER_PROMPT}

Packet path: `03-peer-review/anonymized-responses.md`"""
    scaffold = (
        "## Strongest response and why\n\n"
        "## Biggest blind spot\n\n"
        "## What all responses missed"
    )
    return with_response_section(assignment, scaffold)


def chairman_template() -> str:
    assignment = f"""# Chairman Assignment

Artifact paths in this assignment are relative to the discussion folder (the parent of the phase folders). Read only this assignment and the following source files: `01-brief/brief.md`, all five files in `02-advisors/`, all five files in `03-peer-review/`, and `04-chairman/advisor-key.md`. Each agent file contains instructions and a response section; use only the response section as source material. You may write only in the response section of this file.

## Task

{CHAIRMAN_PROMPT}

## Advisor and review source paths

- `02-advisors/contrarian.md`
- `02-advisors/first-principles.md`
- `02-advisors/expansionist.md`
- `02-advisors/outsider.md`
- `02-advisors/executor.md`
- `03-peer-review/reviewer-01.md` through `03-peer-review/reviewer-05.md`
- `04-chairman/advisor-key.md`"""
    return with_response_section(assignment, "# Council Report: [Short topic]")


def completeness_template() -> str:
    assignment = f"""# Completeness Review Assignment

Artifact paths in this assignment are relative to the discussion folder (the parent of the phase folders). Read only this assignment, the discussion-root `results.md`, and these sources: `01-brief/brief.md`, all five files in `02-advisors/`, all five files in `03-peer-review/`, and `04-chairman/advisor-key.md`. In agent files, use only the response section as source material. Do not rewrite the report. You may write only in the response section of this file.

## Task

{COMPLETENESS_PROMPT}

## Source paths

- `results.md`
- `01-brief/brief.md`
- `02-advisors/contrarian.md`, `first-principles.md`, `expansionist.md`, `outsider.md`, and `executor.md`
- `03-peer-review/reviewer-01.md` through `reviewer-05.md`
- `04-chairman/advisor-key.md`"""
    scaffold = (
        "## Audit\n\n"
        "| Source | Material point | Report location | Status |\n"
        "|---|---|---|---|\n\n"
        "Status: REVISE"
    )
    return with_response_section(assignment, scaffold)


def scaffold_files() -> dict[Path, str]:
    files: dict[Path, str] = {
        Path("01-brief/brief.md"): (
            "---\n"
            "approval_status: pending\n"
            "approved_sha256: null\n"
            "---\n\n"
            "# Council Brief\n\n"
            f"{TODO_MARKER} Coordinator: complete the neutral question and relevant context. -->\n\n"
            "## Question\n\n"
            "## Context\n\n"
            "## Stakes\n\n"
            "## Assumptions and unresolved context\n"
        ),
        Path("03-peer-review/anonymized-responses.md"): (
            f"{PACKET_MARKER}\n"
        ),
        Path("04-chairman/advisor-key.md"): (
            f"{KEY_MARKER}\n"
        ),
        Path("results.md"): (
            "# Council Report: [Short topic]\n\n"
            f"{TODO_MARKER} Run publish-report after the chairman completes 04-chairman/chairman.md. -->\n"
        ),
        Path("04-chairman/chairman.md"): chairman_template(),
        Path("04-chairman/completeness-review.md"): completeness_template(),
    }
    files.update({Path("02-advisors") / f"{name}.md": advisor_template(name) for name in ADVISORS})
    files.update({Path("03-peer-review") / f"{name}.md": reviewer_template(i) for i, name in enumerate(REVIEWERS, start=1)})
    return files


def init_discussion(args: argparse.Namespace) -> int:
    root = (args.root or repository_root()).resolve()
    discussions = root / "discussions"
    name = args.discussion_name.strip()
    if not name or name in {".", ".."} or "/" in name or "\\" in name:
        print("ERROR: provide a discussion name without path separators.", file=sys.stderr)
        return 1
    target = discussions / name
    if target.exists():
        print(f"ERROR: discussion folder already exists: {target}; choose a distinct discussion name.", file=sys.stderr)
        return 1

    generated = {target / relative: content for relative, content in scaffold_files().items()}
    collisions = [str(path) for path in generated if path.exists()]
    if target.exists() or collisions:
        print("Refusing to overwrite existing discussion artifacts: " + ", ".join(collisions or [str(target)]), file=sys.stderr)
        return 1

    try:
        for path, content in generated.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    except OSError as error:
        print(f"ERROR: could not create discussion scaffold: {error}", file=sys.stderr)
        return 1

    print(f"Created council scaffold: {target}")
    print("Complete 01-brief/brief.md, link it for the user to read and approve, record approval in its frontmatter, and pass the brief gate before dispatching advisors.")
    print("Then assign agents using their prefilled brief files. Agents write only between response markers.")
    return 0


def prepare_review(args: argparse.Namespace) -> int:
    discussion = args.discussion.resolve()
    brief = discussion / "01-brief" / "brief.md"
    inputs = {name: discussion / "02-advisors" / f"{name}.md" for name in ADVISORS}
    missing = [str(path) for path in (brief, *inputs.values()) if not usable(path)]
    packet = discussion / "03-peer-review" / "anonymized-responses.md"
    key = discussion / "04-chairman" / "advisor-key.md"
    if missing:
        print("Missing, empty, or unfinished required files:", file=sys.stderr)
        print("\n".join(missing), file=sys.stderr)
        return 1
    if not brief_approval_matches(brief):
        print("Refusing to prepare review packet; the current brief has no matching explicit user approval.", file=sys.stderr)
        return 1
    if not is_scaffold(packet, PACKET_MARKER) or not is_scaffold(key, KEY_MARKER):
        print("Refusing to replace a reviewer packet or advisor key that is not an untouched scaffold.", file=sys.stderr)
        return 1

    roles = list(ADVISORS)
    random.SystemRandom().shuffle(roles)
    lines = ["# Anonymized advisor responses", "", brief_body(brief).strip(), ""]
    key_lines = ["# Advisor response key", "", "Use only for chairman synthesis and completeness review.", ""]
    for letter, role in zip("ABCDE", roles, strict=True):
        response = response_text(inputs[role])
        lines.extend((f"## Response {letter}", "", response, ""))
        key_lines.append(f"- Response {letter}: The {role.replace('-', ' ').title()}")

    packet.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    key.write_text("\n".join(key_lines) + "\n", encoding="utf-8")
    print(f"Created reviewer packet: {packet}")
    print(f"Created private advisor key: {key}")
    return 0


def brief_digest(path: Path) -> str:
    body = brief_body(path)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def brief_body(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(?P<metadata>.*?)\r?\n---\r?\n", content, re.DOTALL)
    if not match:
        raise ValueError(f"Brief is missing valid frontmatter: {path}")
    return content[match.end():]


def brief_frontmatter(path: Path) -> tuple[list[str], str]:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(?P<metadata>.*?)\r?\n---\r?\n", content, re.DOTALL)
    if not match:
        raise ValueError(f"Brief is missing valid frontmatter: {path}")
    return match.group("metadata").splitlines(), content[match.end():]


def update_brief_approval(path: Path, status: str, digest: str | None) -> None:
    metadata, body = brief_frontmatter(path)
    values = {
        "approval_status": status,
        "approved_sha256": digest if digest else "null",
    }
    updated: list[str] = []
    seen: set[str] = set()
    for line in metadata:
        key, separator, _ = line.partition(":")
        key = key.strip()
        if separator and key in values:
            updated.append(f"{key}: {values[key]}")
            seen.add(key)
        else:
            updated.append(line)
    for key, value in values.items():
        if key not in seen:
            updated.append(f"{key}: {value}")
    path.write_text("---\n" + "\n".join(updated) + "\n---\n" + body, encoding="utf-8")


def brief_approval_matches(brief: Path) -> bool:
    if not brief.is_file():
        return False
    try:
        metadata, _ = brief_frontmatter(brief)
        values = {}
        for line in metadata:
            key, separator, value = line.partition(":")
            if separator:
                values[key.strip()] = value.strip().strip("'\"")
        return (
            values.get("approval_status") == "approved"
            and values.get("approved_sha256") == brief_digest(brief)
        )
    except (OSError, ValueError):
        return False


def approve_brief(args: argparse.Namespace) -> int:
    discussion = args.discussion.resolve()
    brief = discussion / "01-brief" / "brief.md"
    if not usable(brief):
        print(f"Missing, empty, or unfinished brief: {brief}", file=sys.stderr)
        return 1
    try:
        digest = brief_digest(brief)
        update_brief_approval(brief, "approved", digest)
    except (OSError, ValueError) as error:
        print(f"ERROR: could not record brief approval: {error}", file=sys.stderr)
        return 1
    print(f"Recorded user approval in brief frontmatter: {brief}")
    return 0


def is_scaffold(path: Path, marker: str) -> bool:
    return path.is_file() and path.read_text(encoding="utf-8").strip() == marker


def usable(path: Path) -> bool:
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8").strip()
    if PACKET_MARKER in content or KEY_MARKER in content:
        return False
    if RESPONSE_START in content or RESPONSE_END in content:
        try:
            response = response_text(path)
        except ValueError:
            return False
        return bool(response) and TODO_MARKER not in response
    return bool(content) and TODO_MARKER not in content


def response_text(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    if content.count(RESPONSE_START) != 1 or content.count(RESPONSE_END) != 1:
        raise ValueError(f"Expected exactly one response section in {path}")
    before, remainder = content.split(RESPONSE_START, 1)
    response, after = remainder.split(RESPONSE_END, 1)
    if RESPONSE_START in remainder or RESPONSE_END in after:
        raise ValueError(f"Nested or repeated response markers in {path}")
    if TODO_MARKER in response:
        raise ValueError(f"Unfinished response scaffold in {path}")
    return response.strip()


def publish_report(args: argparse.Namespace) -> int:
    discussion = args.discussion.resolve()
    chairman = discussion / "04-chairman" / "chairman.md"
    report = discussion / "results.md"
    if not usable(chairman):
        print(f"Missing, empty, or unfinished chairman response: {chairman}", file=sys.stderr)
        return 1
    try:
        content = response_text(chairman).rstrip() + "\n"
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    report.write_text(content, encoding="utf-8")
    print(f"Published chairman response to user-facing report: {report}")
    return 0


def check_discussion(args: argparse.Namespace) -> int:
    discussion = args.discussion.resolve()
    brief = discussion / "01-brief" / "brief.md"
    required: list[Path] = [brief]
    if args.through in {"advisors", "review", "chairman"}:
        required.extend(discussion / "02-advisors" / f"{name}.md" for name in ADVISORS)
    if args.through in {"review", "chairman"}:
        required.extend(
            (
                discussion / "03-peer-review" / "anonymized-responses.md",
                discussion / "04-chairman" / "advisor-key.md",
            )
        )
        required.extend(discussion / "03-peer-review" / f"{name}.md" for name in REVIEWERS)
    if args.through == "chairman":
        required.extend(
            (
                discussion / "04-chairman" / "chairman.md",
                discussion / "results.md",
                discussion / "04-chairman" / "completeness-review.md",
            )
        )

    unfinished = [path for path in required if not usable(path)]
    if unfinished:
        print("Gate failed; missing, empty, or unfinished files:", file=sys.stderr)
        for path in unfinished:
            print(f"- {path}", file=sys.stderr)
        return 1

    if not brief_approval_matches(brief):
        print(
            "Gate failed; the current brief has no matching user approval. "
            "Present it to the user, wait for explicit approval, then run approve-brief.",
            file=sys.stderr,
        )
        return 1

    if args.through == "chairman":
        review_text = response_text(discussion / "04-chairman" / "completeness-review.md")
        status_lines = [line.strip() for line in review_text.splitlines() if line.strip().startswith("Status:")]
        if status_lines != ["Status: PASS"]:
            print("Gate failed; completeness review must contain the exact line 'Status: PASS'.", file=sys.stderr)
            return 1

    print(f"Gate passed through {args.through}: {discussion}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="create all phase folders and output scaffolds")
    init.add_argument("discussion_name", help="the exact discussion folder name to create")
    init.add_argument("--root", type=Path, help="repository root; defaults to the skill-lab repository")
    init.set_defaults(run=init_discussion)

    prepare = commands.add_parser("prepare-review", help="randomize response labels and fill the reviewer packet and key")
    prepare.add_argument("discussion", type=Path)
    prepare.set_defaults(run=prepare_review)

    approve = commands.add_parser("approve-brief", help="record explicit user approval of the current brief version")
    approve.add_argument("discussion", type=Path)
    approve.set_defaults(run=approve_brief)

    publish = commands.add_parser("publish-report", help="publish the chairman response section to root results.md")
    publish.add_argument("discussion", type=Path)
    publish.set_defaults(run=publish_report)

    check = commands.add_parser("check", help="check required filled artifacts through a phase gate")
    check.add_argument("discussion", type=Path)
    check.add_argument("--through", choices=("brief", "advisors", "review", "chairman"), required=True)
    check.set_defaults(run=check_discussion)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())
