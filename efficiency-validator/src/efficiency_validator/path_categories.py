"""Conservative classification of observed filesystem paths."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Iterable, Literal, Mapping


PathCategory = Literal[
    "target",
    "skill",
    "other-repository",
    "external-context",
    "cache-dependency",
    "system",
    "evaluator",
    "sensitive-unknown",
]

_ROOT_PRIORITY: tuple[PathCategory, ...] = (
    "target",
    "skill",
    "evaluator",
    "external-context",
    "other-repository",
    "cache-dependency",
)
_SYSTEM_PREFIXES = (
    "/System",
    "/etc",
    "/usr",
    "/bin",
    "/sbin",
    "/opt",
    "/private/var",
    "/private/etc",
    "/Library",
)
_CACHE_MARKERS = ("/.cache/", "/.venv/", "/node_modules/", "/__pycache__/")


def classify_path(
    path: str,
    roots: Mapping[str, Iterable[str]],
) -> PathCategory:
    """Classify a path using explicit roots, then conservative host heuristics."""

    normalized = _normalize(path)
    for category in _ROOT_PRIORITY:
        if any(_under_root(normalized, _normalize(root)) for root in roots.get(category, ())):
            return category
    if any(_under_root(normalized, prefix) for prefix in _SYSTEM_PREFIXES):
        return "system"
    if "/agent-skills/" in normalized or normalized.endswith("/SKILL.md"):
        return "skill"
    if "/.codex/" in normalized:
        return "external-context"
    if "/context-lab-evaluator/" in normalized:
        return "evaluator"
    if any(marker in normalized for marker in _CACHE_MARKERS):
        return "cache-dependency"
    if "/skill-lab/" in normalized:
        return "other-repository"
    return "sensitive-unknown"


def _normalize(path: str) -> str:
    value = str(PurePosixPath(path))
    return value.rstrip("/") or "/"


def _under_root(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip("/") + "/")
