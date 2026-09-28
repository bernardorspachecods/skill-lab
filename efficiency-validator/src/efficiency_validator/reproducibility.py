"""Stable fingerprints for deterministic report/review artefacts."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def stable_json_digest(value: Any) -> str:
    """Hash JSON-compatible data with canonical ordering and encoding."""

    encoded = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"
