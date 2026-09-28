from dataclasses import dataclass, field
from typing import Literal


Operation = Literal["search", "list", "read", "follow_link"]


@dataclass(frozen=True)
class TraceEvent:
    run_id: str
    case_id: str
    event_index: int
    operation: Operation
    paths: list[str] = field(default_factory=list)
    scanned_paths: list[str] = field(default_factory=list)
    result_count: int | None = None
    tokens: int | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "TraceEvent":
        operation = payload.get("operation")
        if not isinstance(operation, str) or operation not in {
            "search",
            "list",
            "read",
            "follow_link",
        }:
            raise ValueError(f"Invalid operation: {operation!r}")

        event_index = int(payload["event_index"])
        if event_index < 0:
            raise ValueError("event_index must be non-negative")

        result_count = (
            None
            if payload.get("result_count") is None
            else int(payload["result_count"])
        )
        if result_count is not None and result_count < 0:
            raise ValueError("result_count must be non-negative")

        tokens = None if payload.get("tokens") is None else int(payload["tokens"])
        if tokens is not None and tokens < 0:
            raise ValueError("tokens must be non-negative")

        return cls(
            run_id=str(payload["run_id"]),
            case_id=str(payload["case_id"]),
            event_index=event_index,
            operation=operation,  # type: ignore[arg-type]
            paths=[str(path) for path in payload.get("paths", [])],
            scanned_paths=[
                str(path) for path in payload.get("scanned_paths", [])
            ],
            result_count=result_count,
            tokens=tokens,
        )
