from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any


VALIDATOR_VERSION = "0.5.0"


@dataclass(frozen=True)
class RunManifest:
    """Metadata required to compare one captured run with another."""

    run_id: str
    case_id: str
    repo_revision: str
    runtime_revision: str
    task_hash: str
    model: str
    codex_version: str
    # Legacy wire name retained so historical run manifests remain readable.
    observer_version: str
    launch_mode: str
    sandbox: str
    ephemeral: bool
    started_at: str
    finished_at: str
    exit_code: int
    complete: bool
    sidecar_revision: str
    observability_schema: str = "observability-1"
    token_usage_source: str = "codex-exec-json"
    filesystem_trace_source: str = "unavailable"
    network_trace_source: str = "unavailable"
    exact_read_required: bool = False
    exact_read_trace_source: str = "unavailable"
    variation: str = "unspecified"
    prompt: str | None = None
    prompt_hash: str | None = None
    oracle: dict[str, str] | None = None
    controlled_variation: dict[str, Any] | None = None
    provenance_status: str = "legacy"

    def __post_init__(self) -> None:
        for field_name in (
            "run_id",
            "case_id",
            "repo_revision",
            "runtime_revision",
            "task_hash",
            "model",
            "codex_version",
            "observer_version",
            "launch_mode",
            "sandbox",
            "started_at",
            "finished_at",
            "sidecar_revision",
            "observability_schema",
            "token_usage_source",
            "filesystem_trace_source",
            "exact_read_trace_source",
            "variation",
        ):
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} must not be empty")
        if self.prompt is not None and not self.prompt:
            raise ValueError("prompt must not be empty when supplied")
        if self.prompt_hash is not None and not self.prompt_hash:
            raise ValueError("prompt_hash must not be empty when supplied")
        if self.oracle is not None and not self.oracle:
            raise ValueError("oracle must not be empty when supplied")
        if self.controlled_variation is not None and not self.controlled_variation:
            raise ValueError(
                "controlled_variation must not be empty when supplied"
            )
        if not self.provenance_status:
            raise ValueError("provenance_status must not be empty")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RunManifest":
        required = {
            "run_id",
            "case_id",
            "repo_revision",
            "runtime_revision",
            "task_hash",
            "model",
            "codex_version",
            "observer_version",
            "launch_mode",
            "sandbox",
            "ephemeral",
            "started_at",
            "finished_at",
            "exit_code",
            "complete",
            "sidecar_revision",
        }
        missing = sorted(required - payload.keys())
        if missing:
            raise ValueError(f"Manifest is missing fields: {', '.join(missing)}")
        return cls(
            run_id=str(payload["run_id"]),
            case_id=str(payload["case_id"]),
            repo_revision=str(payload["repo_revision"]),
            runtime_revision=str(payload["runtime_revision"]),
            task_hash=str(payload["task_hash"]),
            model=str(payload["model"]),
            codex_version=str(payload["codex_version"]),
            observer_version=str(payload["observer_version"]),
            launch_mode=str(payload["launch_mode"]),
            sandbox=str(payload["sandbox"]),
            ephemeral=bool(payload["ephemeral"]),
            started_at=str(payload["started_at"]),
            finished_at=str(payload["finished_at"]),
            exit_code=int(payload["exit_code"]),
            complete=bool(payload["complete"]),
            sidecar_revision=str(payload["sidecar_revision"]),
            observability_schema=str(
                payload.get("observability_schema", "legacy-command-only")
            ),
            token_usage_source=str(
                payload.get("token_usage_source", "not-captured")
            ),
            filesystem_trace_source=str(
                payload.get("filesystem_trace_source", "unavailable")
            ),
            network_trace_source=str(
                payload.get("network_trace_source", "unavailable")
            ),
            exact_read_required=bool(payload.get("exact_read_required", False)),
            exact_read_trace_source=str(
                payload.get("exact_read_trace_source", "unavailable")
            ),
            variation=str(payload.get("variation", "unspecified")),
            prompt=(
                str(payload["prompt"])
                if payload.get("prompt") is not None
                else None
            ),
            prompt_hash=(
                str(payload["prompt_hash"])
                if payload.get("prompt_hash") is not None
                else None
            ),
            oracle=(
                dict(payload["oracle"])
                if isinstance(payload.get("oracle"), dict)
                else None
            ),
            controlled_variation=(
                dict(payload["controlled_variation"])
                if isinstance(payload.get("controlled_variation"), dict)
                else None
            ),
            provenance_status=str(
                payload.get(
                    "provenance_status",
                    "complete"
                    if all(
                        key in payload
                        for key in (
                            "prompt",
                            "prompt_hash",
                            "oracle",
                            "controlled_variation",
                        )
                    )
                    else "legacy",
                )
            ),
        )


def build_run_provenance(
    *,
    prompt: str,
    oracle_path: Path | None,
    evaluator_root: Path,
    variation: str,
    task_hash: str,
    case_id: str | None = None,
) -> dict[str, object]:
    """Build immutable, inspectable provenance for a newly captured run."""

    prompt_hash = _sha256_bytes(prompt.encode("utf-8"))
    if oracle_path is None:
        oracle: dict[str, str] = {
            "status": "unavailable",
            "reason": "oracle_path_not_supplied",
        }
        provenance_status = "partial"
    else:
        resolved_oracle = oracle_path.resolve()
        if not resolved_oracle.is_file():
            raise FileNotFoundError(f"Oracle does not exist: {resolved_oracle}")
        oracle_payload = json.loads(resolved_oracle.read_text(encoding="utf-8"))
        oracle_case_id = case_id or str(oracle_payload.get("case_id", ""))
        if not oracle_case_id:
            raise ValueError("Oracle must declare case_id")
        oracle = {
            "case_id": oracle_case_id,
            "path": _relative_path(resolved_oracle, evaluator_root),
            "sha256": _sha256_bytes(resolved_oracle.read_bytes()),
            "status": "available",
        }
        provenance_status = "complete"

    controlled_variation = {
        "label": variation,
        "prompt_hash": prompt_hash,
        "status": "declared" if variation != "unspecified" else "unspecified",
        "task_hash": task_hash,
    }
    return {
        "prompt": prompt,
        "prompt_hash": prompt_hash,
        "oracle": oracle,
        "controlled_variation": controlled_variation,
        "provenance_status": provenance_status,
    }


def _sha256_bytes(value: bytes) -> str:
    return f"sha256:{hashlib.sha256(value).hexdigest()}"


def _relative_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name
