#!/usr/bin/env python3
"""Shared, repository-local allocator for plan and knowledge artifact IDs."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from contextlib import contextmanager
from pathlib import Path


PATTERNS = {
    "LR": re.compile(r"^LR-(\d{2,})$"),
    "SP": re.compile(r"^(LR-\d{2,})\.SP-(\d{2,})$"),
    "RES": re.compile(r"^(LR-\d{2,})\.RES-(\d{2,})$"),
    "REV": re.compile(r"^(LR-\d{2,})\.REV-(\d{2,})$"),
    "KNOW": re.compile(r"^(?:(LR-\d{2,})\.)?KNOW-(\d{2,})$"),
    "AUD": re.compile(r"^(KNOW-\d{2,})\.AUD-(\d{2,})$"),
    "WORK": re.compile(r"^(KNOW-\d{2,})\.WORK-(\d{2,})$"),
}
ARTIFACT_FILE_RE = re.compile(r"^(LR-\d{2,}\.(?:RES|REV)-\d{2,})\.(?:working|audit|assessment|perspective-\d{2,})$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)


def empty_registry() -> dict:
    return {
        "root_plans": [],
        "subplans": {},
        "research": {},
        "reviews": {},
        "knowledge": [],
        "plan_knowledge": {},
        "knowledge_audits": {},
        "knowledge_working": {},
    }


def _append_once(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def read_registry(path: Path) -> dict:
    if not path.exists():
        return empty_registry()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read ID reservation registry {path}: {error}") from error
    defaults = empty_registry()
    for key, default in defaults.items():
        data.setdefault(key, default)
    data["root_plans"] = list(dict.fromkeys(data["root_plans"]))
    data["knowledge"] = list(dict.fromkeys(data["knowledge"]))
    for key in ("subplans", "research", "reviews", "plan_knowledge", "knowledge_audits", "knowledge_working"):
        data[key] = {owner: list(dict.fromkeys(values)) for owner, values in data[key].items()}
    return data


def discover_existing_ids(repository: Path, registry: dict) -> None:
    ignored = {".git", "node_modules", ".plan-management"}
    for path in repository.rglob("*"):
        if ignored.intersection(path.relative_to(repository).parts):
            continue
        if path.is_dir():
            for part in path.relative_to(repository).parts:
                match = PATTERNS["LR"].fullmatch(part)
                if match:
                    _append_once(registry["root_plans"], part)
                match = PATTERNS["SP"].fullmatch(part)
                if match:
                    _append_once(registry["subplans"].setdefault(match.group(1), []), part)
        if not path.is_file() or path.suffix.lower() != ".md":
            continue
        stem = path.stem
        for kind, directory in (("AUD", "audit"), ("WORK", "working")):
            match = PATTERNS[kind].fullmatch(stem)
            if match and path.parent == repository / "knowledge" / directory:
                bucket = "knowledge_audits" if kind == "AUD" else "knowledge_working"
                _append_once(registry[bucket].setdefault(match.group(1), []), stem)
        artifact = ARTIFACT_FILE_RE.fullmatch(stem)
        if artifact:
            artifact_id = artifact.group(1)
            owner, _ = artifact_id.rsplit(".", 1)
            bucket = "research" if ".RES-" in artifact_id else "reviews"
            _append_once(registry[bucket].setdefault(owner, []), artifact_id)
        match = PATTERNS["KNOW"].fullmatch(stem)
        if match:
            plan_owner, _ = match.groups()
            if plan_owner:
                bucket = registry["plan_knowledge"].setdefault(plan_owner, [])
                _append_once(bucket, stem)
            # Bare KNOW IDs belong only to the repository's shared knowledge collection.
            elif path.parent == repository / "knowledge":
                _append_once(registry["knowledge"], stem)
        try:
            frontmatter = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            continue
        if frontmatter:
            source_artifact = re.search(r"^source_artifact_id:\s*['\"]?([A-Za-z0-9.-]+)", frontmatter.group(1), re.MULTILINE)
            if source_artifact:
                source_id = source_artifact.group(1)
                for kind, bucket_name in (("RES", "research"), ("REV", "reviews")):
                    match = PATTERNS[kind].fullmatch(source_id)
                    if match:
                        _append_once(registry[bucket_name].setdefault(match.group(1), []), source_id)
            plan_id = re.search(r"^plan_id:\s*['\"]?(LR-\d{2,}(?:\.SP-\d{2,})?)", frontmatter.group(1), re.MULTILINE)
            if plan_id:
                value = plan_id.group(1)
                match = PATTERNS["LR"].fullmatch(value)
                if match:
                    _append_once(registry["root_plans"], value)
                match = PATTERNS["SP"].fullmatch(value)
                if match:
                    _append_once(registry["subplans"].setdefault(match.group(1), []), value)


def _used(registry: dict, kind: str, root: str | None) -> list[str]:
    if kind == "LR":
        return registry["root_plans"]
    if kind == "KNOW" and root is None:
        return registry["knowledge"]
    if root is None:
        raise ValueError(f"{kind} IDs require an owner ID")
    if kind in {"AUD", "WORK"}:
        match = PATTERNS["KNOW"].fullmatch(root)
        if not match or match.group(1) is not None:
            raise ValueError(f"invalid repository knowledge ID: {root}")
        bucket = "knowledge_audits" if kind == "AUD" else "knowledge_working"
        return registry[bucket].setdefault(root, [])
    match = PATTERNS["LR"].fullmatch(root)
    if not match:
        raise ValueError(f"invalid root plan ID: {root}")
    bucket = {"SP": "subplans", "RES": "research", "REV": "reviews", "KNOW": "plan_knowledge"}[kind]
    return registry[bucket].setdefault(root, [])


def _format(kind: str, root: str | None, number: int) -> str:
    if kind == "LR":
        return f"LR-{number:02d}"
    if kind == "SP":
        return f"{root}.SP-{number:02d}"
    if kind in {"RES", "REV"}:
        return f"{root}.{kind}-{number:02d}"
    if kind in {"AUD", "WORK"}:
        return f"{root}.{kind}-{number:02d}"
    return f"{root + '.' if root else ''}KNOW-{number:02d}"


def _next_number(kind: str, root: str | None, values: list[str]) -> int:
    pattern = PATTERNS[kind]
    ord_group = 1 if kind == "LR" else 2
    numbers = []
    for value in values:
        match = pattern.fullmatch(value)
        if match and (kind == "LR" or match.group(1) == root):
            numbers.append(int(match.group(ord_group)))
    return max(numbers, default=0) + 1


@contextmanager
def reservation_lock(path: Path):
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise RuntimeError(f"another ID allocator holds the reservation lock: {path}") from error
    try:
        os.write(descriptor, f"pid={os.getpid()}\n".encode())
        yield
    finally:
        os.close(descriptor)
        path.unlink(missing_ok=True)


def write_registry(path: Path, registry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


class IdReservationSession:
    """A locked allocation session; reserve several IDs before one atomic ledger write."""

    def __init__(self, repository: Path):
        self.repository = repository.resolve()
        self.registry_path = self.repository / ".plan-management" / "id-reservations.json"
        self.lock_path = self.registry_path.with_suffix(".lock")
        self._lock = None
        self.registry = None

    def __enter__(self):
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = reservation_lock(self.lock_path)
        self._lock.__enter__()
        try:
            self.registry = read_registry(self.registry_path)
            discover_existing_ids(self.repository, self.registry)
        except Exception as error:
            self._lock.__exit__(type(error), error, error.__traceback__)
            raise
        return self

    def reserve(self, kind: str, root: str | None = None) -> str:
        kind = kind.upper()
        if kind not in PATTERNS:
            raise ValueError(f"unsupported ID type: {kind}")
        values = _used(self.registry, kind, root)
        value = _format(kind, root, _next_number(kind, root, values))
        values.append(value)
        return value

    def __exit__(self, exc_type, exc, traceback):
        try:
            if exc_type is None:
                write_registry(self.registry_path, self.registry)
        finally:
            self._lock.__exit__(exc_type, exc, traceback)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path, help="repository containing the shared reservation ledger")
    parser.add_argument("kind", choices=tuple(PATTERNS), help="ID namespace to allocate from")
    parser.add_argument("--root", help="owner ID for subplan, research, review, or knowledge artifact IDs")
    args = parser.parse_args()
    repository = args.repository.resolve()
    if not repository.is_dir():
        parser.error(f"repository does not exist or is not a directory: {repository}")
    try:
        with IdReservationSession(repository) as session:
            value = session.reserve(args.kind, args.root)
        print(value)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
