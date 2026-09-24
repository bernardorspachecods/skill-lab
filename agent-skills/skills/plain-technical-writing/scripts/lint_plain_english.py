#!/usr/bin/env python3
"""Advisory checks for plain technical prose.

The script deliberately ignores document structure and exact-content regions.
It is a review aid, not a compliance checker.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_LIMITS = {"procedural": 20, "descriptive": 25}
MODAL_RE = re.compile(r"\b(should|would|may|might|could)\b", re.IGNORECASE)
SLOP_RE = re.compile(
    r"\b(simply|just|easily|seamlessly|robust|powerful|comprehensive|obviously)\b",
    re.IGNORECASE,
)
CONTRACTION_RE = re.compile(r"\b\w+(?:n’t|n't|’re|'re|’ve|'ve|’ll|'ll|’d|'d|’m|'m)\b", re.IGNORECASE)
SENTENCE_RE = re.compile(r"[^.!?]+(?:[.!?]+|$)")
WORD_RE = re.compile(r"\b[\w’'-]+\b")
COMMAND_RE = re.compile(
    r"^\s*(?:\$|(?:bash|cargo|curl|git|go|make|node|npm|npx|pip|pnpm|python3?|pytest|uv)\s+)"
)


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def prose_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    in_frontmatter = False
    in_code = False
    for number, raw in enumerate(text.splitlines(), 1):
        stripped = raw.strip()
        if number == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code or not stripped or stripped.startswith("#") or COMMAND_RE.match(raw):
            continue
        if re.fullmatch(r"\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*", raw):
            continue
        if stripped.startswith("|") or stripped.startswith(">"):
            content = re.sub(r"^\s*[|>]\s?", "", raw)
        else:
            content = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", "", raw)
        content = re.sub(r"`[^`]*`", "", content)
        content = re.sub(r"!?\[[^]]*\]\([^)]*\)", "", content)
        content = re.sub(r"https?://\S+", "", content)
        if content.strip():
            lines.append((number, content))
    return lines


def lint(text: str, kind: str) -> dict[str, object]:
    limit = DEFAULT_LIMITS[kind]
    findings: list[dict[str, object]] = []
    total_words = 0
    for line_number, line in prose_lines(text):
        total_words += len(WORD_RE.findall(line))
        checks = [
            ("modal", MODAL_RE.search(line), "modal may hide the requirement or certainty"),
            ("slop", SLOP_RE.search(line), "vague or promotional wording"),
            ("contraction", CONTRACTION_RE.search(line), "use complete forms in formal documentation"),
            ("semicolon", ";" in line, "split the sentence or show the relationship explicitly"),
            ("em_dash", "—" in line, "use a full stop or a precise connector"),
        ]
        for code, match, message in checks:
            if match:
                findings.append({"line": line_number, "code": code, "message": message})
        for sentence in SENTENCE_RE.findall(line):
            words = len(WORD_RE.findall(sentence))
            if words > limit:
                findings.append(
                    {
                        "line": line_number,
                        "code": "long_sentence",
                        "message": f"{words} words; review against the {limit}-word signal",
                    }
                )
    counts: dict[str, int] = {}
    for finding in findings:
        code = str(finding["code"])
        counts[code] = counts.get(code, 0) + 1
    return {
        "kind": kind,
        "word_count": total_words,
        "violations_total": len(findings),
        "violations_per_100_words": round(len(findings) * 100 / max(total_words, 1), 2),
        "counts": counts,
        "findings": findings,
    }


def self_test() -> None:
    sample = """---\nname: sample\n---\n\n# Heading\n\n- If the service is unavailable, restart it.\n- This is simply a very long sentence that contains enough words to trigger the procedural review signal because readers need a clearer sequence.\n\n```sh\nshould remain untouched; do not lint this\n```\n"""
    report = lint(sample, "procedural")
    assert report["word_count"] > 0
    assert report["counts"].get("slop") == 1
    assert report["counts"].get("semicolon") is None
    assert report["violations_total"] >= 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="Markdown or text file; use '-' for stdin")
    parser.add_argument("--type", choices=sorted(DEFAULT_LIMITS), default="descriptive")
    parser.add_argument("--gate", action="store_true", help="return 1 when findings exist")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("self-test: pass")
        return 0
    if not args.path:
        parser.error("path is required unless --self-test is used")
    report = lint(read_text(args.path), args.type)
    print(f"{args.path}: {report['violations_total']} advisory findings in {report['word_count']} words")
    for finding in report["findings"]:
        print(f"  line {finding['line']}: {finding['code']}: {finding['message']}")
    return int(bool(args.gate and report["violations_total"]))


if __name__ == "__main__":
    raise SystemExit(main())
