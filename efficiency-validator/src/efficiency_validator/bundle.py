"""Validation and discovery for reusable captured-run bundles."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .filesystem import parse_filesystem_trace
from .exact_read import parse_exact_read_trace
from .manifest import RunManifest
from .network import parse_network_trace


@dataclass(frozen=True)
class BundleValidation:
    """The downstream-safe result of validating one run bundle."""

    valid: bool
    filesystem_status: str
    issues: tuple[str, ...]
    network_status: str = "unavailable"
    exact_read_status: str = "unavailable"


@dataclass(frozen=True)
class RunBundle:
    """Locate and validate the stable files emitted for one captured run."""

    root: Path

    @classmethod
    def from_root(cls, root: Path) -> "RunBundle":
        return cls(root.resolve())

    @property
    def events_path(self) -> Path:
        return self.root / "events.jsonl"

    @property
    def manifest_path(self) -> Path:
        return self.root / "manifest.json"

    @property
    def report_path(self) -> Path:
        return self.root / "report.json"

    @property
    def filesystem_path(self) -> Path:
        return self.root / "filesystem.jsonl"

    @property
    def network_path(self) -> Path:
        return self.root / "network.jsonl"

    @property
    def exact_read_path(self) -> Path:
        return self.root / "exact-read.jsonl"

    def validate(self) -> BundleValidation:
        issues: list[str] = []
        for path in (self.events_path, self.manifest_path, self.report_path):
            if not path.is_file():
                issues.append(f"missing artifact: {path.name}")

        manifest: RunManifest | None = None
        if self.manifest_path.is_file():
            try:
                manifest = RunManifest.from_dict(
                    json.loads(self.manifest_path.read_text(encoding="utf-8"))
                )
            except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
                issues.append(f"invalid manifest: {exc}")

        report: dict[str, object] | None = None
        if self.report_path.is_file():
            try:
                raw_report = json.loads(
                    self.report_path.read_text(encoding="utf-8")
                )
                if not isinstance(raw_report, dict):
                    raise ValueError("report must be a JSON object")
                report = raw_report
            except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
                issues.append(f"invalid report: {exc}")

        if manifest is not None and report is not None:
            report_manifest = report.get("manifest")
            if isinstance(report_manifest, dict):
                for field in ("run_id", "case_id"):
                    if report_manifest.get(field) != getattr(manifest, field):
                        issues.append(f"report {field} does not match manifest")
            else:
                issues.append("report is missing manifest identity")

        filesystem_status = _report_filesystem_status(report)
        if self.filesystem_path.is_file():
            expected_run_id = manifest.run_id if manifest is not None else None
            expected_case_id = manifest.case_id if manifest is not None else None
            try:
                parsed = parse_filesystem_trace(
                    self.filesystem_path.read_text(
                        encoding="utf-8", errors="replace"
                    ).splitlines(),
                    expected_run_id=expected_run_id,
                    expected_case_id=expected_case_id,
                )
            except OSError as exc:
                issues.append(f"filesystem sidecar unreadable: {exc}")
            else:
                filesystem_status = parsed.status
                issues.extend(
                    f"filesystem: {issue.kind}: {issue.detail}"
                    for issue in parsed.issues
                )
        elif filesystem_status == "available":
            issues.append("report claims filesystem available but sidecar is missing")

        network_status = _report_network_status(report)
        if self.network_path.is_file():
            expected_run_id = manifest.run_id if manifest is not None else None
            expected_case_id = manifest.case_id if manifest is not None else None
            try:
                parsed_network = parse_network_trace(
                    self.network_path.read_text(
                        encoding="utf-8", errors="replace"
                    ).splitlines(),
                    expected_run_id=expected_run_id,
                    expected_case_id=expected_case_id,
                )
            except OSError as exc:
                issues.append(f"network sidecar unreadable: {exc}")
            else:
                network_status = parsed_network.status
                issues.extend(
                    f"network: {issue.kind}: {issue.detail}"
                    for issue in parsed_network.issues
                )
        elif network_status == "available":
            issues.append("report claims network available but sidecar is missing")

        exact_read_status = _report_exact_read_status(report)
        if manifest is not None and manifest.exact_read_required:
            if not self.exact_read_path.is_file():
                exact_read_status = "unavailable"
                issues.append("exact-read mode requires exact-read.jsonl")
            else:
                try:
                    parsed_exact = parse_exact_read_trace(
                        self.exact_read_path.read_text(
                            encoding="utf-8", errors="replace"
                        ).splitlines(),
                        expected_run_id=manifest.run_id,
                        expected_case_id=manifest.case_id,
                    )
                except OSError as exc:
                    exact_read_status = "unavailable"
                    issues.append(f"exact-read sidecar unreadable: {exc}")
                else:
                    exact_read_status = parsed_exact.status
                    if not parsed_exact.valid:
                        issues.extend(
                            f"exact-read: {reason}"
                            for reason in parsed_exact.invalid_reasons
                        )
                    if not self._exact_process_tree_is_covered(
                        parsed_exact.processes, issues
                    ):
                        exact_read_status = "partial"
        elif self.exact_read_path.is_file():
            try:
                parsed_exact = parse_exact_read_trace(
                    self.exact_read_path.read_text(
                        encoding="utf-8", errors="replace"
                    ).splitlines(),
                    expected_run_id=(manifest.run_id if manifest else None),
                    expected_case_id=(manifest.case_id if manifest else None),
                )
                exact_read_status = parsed_exact.status
            except OSError as exc:
                issues.append(f"exact-read sidecar unreadable: {exc}")

        return BundleValidation(
            valid=not issues,
            filesystem_status=filesystem_status,
            issues=tuple(issues),
            network_status=network_status,
            exact_read_status=exact_read_status,
        )

    def _exact_process_tree_is_covered(
        self,
        processes: tuple[object, ...],
        issues: list[str],
    ) -> bool:
        tree_path = self.root / "process-tree.json"
        if not tree_path.is_file():
            issues.append("exact-read mode requires process-tree.json")
            return False
        try:
            payload = json.loads(tree_path.read_text(encoding="utf-8"))
            if payload.get("status") != "available":
                issues.append("exact-read process tree is not available")
                return False
            expected = {
                int(pid) for pid in payload.get("pids", []) if isinstance(pid, int)
            }
            if not expected:
                issues.append("exact-read process tree contains no measured pids")
                return False
            observed = {
                int(getattr(process, "pid")) for process in processes
            }
        except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
            issues.append(f"exact-read process tree is invalid: {exc}")
            return False
        missing = sorted(expected - observed)
        if missing:
            issues.append(
                "exact-read process coverage missing pids: "
                + ", ".join(str(pid) for pid in missing)
            )
            return False
        return True


def _report_filesystem_status(report: dict[str, object] | None) -> str:
    if report is None:
        return "unavailable"
    observability = report.get("observability")
    if not isinstance(observability, dict):
        return "unavailable"
    filesystem = observability.get("filesystem")
    if not isinstance(filesystem, dict):
        return "unavailable"
    status = filesystem.get("status")
    return status if isinstance(status, str) and status else "unavailable"


def _report_network_status(report: dict[str, object] | None) -> str:
    if report is None:
        return "unavailable"
    observability = report.get("observability")
    if not isinstance(observability, dict):
        return "unavailable"
    network = observability.get("network")
    if not isinstance(network, dict):
        return "unavailable"
    status = network.get("status")
    return status if isinstance(status, str) and status else "unavailable"


def _report_exact_read_status(report: dict[str, object] | None) -> str:
    if report is None:
        return "unavailable"
    observability = report.get("observability")
    if not isinstance(observability, dict):
        return "unavailable"
    exact_read = observability.get("exact_read")
    if not isinstance(exact_read, dict):
        return "unavailable"
    status = exact_read.get("status")
    return status if isinstance(status, str) and status else "unavailable"
