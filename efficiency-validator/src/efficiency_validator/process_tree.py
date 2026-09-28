"""Small process-tree adapter used to scope host-level evidence."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Iterable, Literal


ProcessTreeStatus = Literal["available", "unavailable", "partial"]


@dataclass(frozen=True)
class ProcessTreeSnapshot:
    root_pid: int
    pids: tuple[int, ...]
    status: ProcessTreeStatus
    process_names: tuple[str, ...] = ()
    error: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "root_pid": self.root_pid,
            "pids": list(self.pids),
            "status": self.status,
            "process_names": list(self.process_names),
            "error": self.error,
        }


def parse_process_table(lines: Iterable[str]) -> dict[int, int]:
    """Parse the portable ``ps`` PID/PPID columns conservatively."""

    table: dict[int, int] = {}
    for line in lines:
        fields = line.split()
        if len(fields) < 2:
            continue
        try:
            pid, parent_pid = (int(value) for value in fields[:2])
        except ValueError:
            continue
        if pid > 0 and parent_pid >= 0:
            table[pid] = parent_pid
    return table


def parse_process_names(lines: Iterable[str]) -> dict[int, str]:
    names: dict[int, str] = {}
    for line in lines:
        fields = line.split()
        if len(fields) < 3:
            continue
        try:
            pid = int(fields[0])
        except ValueError:
            continue
        if pid > 0:
            names[pid] = fields[2]
    return names


def descendant_pids(table: dict[int, int], root_pid: int) -> set[int]:
    """Return the root and every known descendant, excluding host siblings."""

    result = {root_pid}
    changed = True
    while changed:
        changed = False
        for pid, parent_pid in table.items():
            if parent_pid in result and pid not in result:
                result.add(pid)
                changed = True
    return result


def snapshot_process_tree(root_pid: int) -> ProcessTreeSnapshot:
    """Read one host process snapshot for a measured process root."""

    try:
        result = subprocess.run(
            ["/bin/ps", "-axo", "pid=,ppid=,comm="],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        return ProcessTreeSnapshot(
            root_pid=root_pid,
            pids=(root_pid,),
            status="unavailable",
            error=str(exc),
        )
    table = parse_process_table(result.stdout.splitlines())
    pids = descendant_pids(table, root_pid)
    names = parse_process_names(result.stdout.splitlines())
    return ProcessTreeSnapshot(
        root_pid=root_pid,
        pids=tuple(sorted(pids)),
        status="available" if root_pid in table else "partial",
        process_names=tuple(sorted({names[pid] for pid in pids if pid in names})),
    )
