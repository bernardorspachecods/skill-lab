"""Deterministic quality gating for one captured run."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal


QualityStatus = Literal["pass", "fail", "indeterminate"]
ReviewStatus = Literal["pass", "fail", "unknown"]


@dataclass(frozen=True)
class QualityResult:
    """Quality evidence consumed by the paired-run comparison."""

    status: QualityStatus
    quality_gate_passed: bool
    required_claim_ids: tuple[str, ...]
    identified_required_claim_ids: tuple[str, ...]
    missing_required_claim_ids: tuple[str, ...]
    unknown_required_claim_ids: tuple[str, ...]
    disallowed_claims: tuple[str, ...]
    answer_complete: bool | None
    authority_status: ReviewStatus | None
    support_status: ReviewStatus | None
    stream_complete: bool
    parser_issue_count: int
    reason_codes: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def evaluate_quality(
    report: dict[str, object],
    oracle: dict[str, object],
    review: dict[str, object] | None,
) -> QualityResult:
    """Apply the quality policy to a report and normalized host review.

    The review is deliberately a separate input from the measured agent's
    answer. It is the evaluator's normalized adjudication of claims, authority,
    support, and completeness; this function only applies deterministic gate
    rules and never treats a cheaper run as higher quality.
    """

    required = _required_claim_ids(oracle)
    stream_complete, parser_issue_count = _stream_state(report)
    base = {
        "required_claim_ids": required,
        "stream_complete": stream_complete,
        "parser_issue_count": parser_issue_count,
    }
    if review is None:
        return QualityResult(
            **base,
            status="indeterminate",
            quality_gate_passed=False,
            identified_required_claim_ids=(),
            missing_required_claim_ids=required,
            unknown_required_claim_ids=(),
            disallowed_claims=(),
            answer_complete=None,
            authority_status=None,
            support_status=None,
            reason_codes=("quality_review_missing",),
        )

    identified = _string_tuple(review.get("required_claim_ids"))
    identified_known = tuple(claim for claim in required if claim in identified)
    unknown = tuple(claim for claim in identified if claim not in required)
    missing = tuple(claim for claim in required if claim not in identified_known)
    disallowed = _string_tuple(review.get("disallowed_claims"))
    answer_complete = _optional_bool(review.get("answer_complete"))
    authority_status = _review_status(review.get("authority_status"))
    support_status = _review_status(review.get("support_status"))

    hard_failures: list[str] = []
    indeterminate: list[str] = []
    if missing:
        hard_failures.append("missing_required_claims")
    if disallowed:
        hard_failures.append("disallowed_claims")
    if unknown:
        indeterminate.append("unknown_required_claim_ids")
    if answer_complete is None:
        indeterminate.append("answer_completeness_unknown")
    elif not answer_complete:
        hard_failures.append("answer_incomplete")
    if authority_status == "fail":
        hard_failures.append("authority_failed")
    elif authority_status in {None, "unknown"}:
        indeterminate.append("authority_unknown")
    if support_status == "fail":
        hard_failures.append("support_failed")
    elif support_status in {None, "unknown"}:
        indeterminate.append("support_unknown")

    final_answer = _final_answer(report)
    if not final_answer:
        hard_failures.append("answer_missing")
    if not stream_complete:
        indeterminate.append("run_incomplete")
    if parser_issue_count:
        indeterminate.append("parser_issues")

    reasons = tuple(dict.fromkeys((*hard_failures, *indeterminate)))
    status: QualityStatus
    if hard_failures:
        status = "fail"
    elif indeterminate:
        status = "indeterminate"
    else:
        status = "pass"
    return QualityResult(
        **base,
        status=status,
        quality_gate_passed=status == "pass",
        identified_required_claim_ids=identified_known,
        missing_required_claim_ids=missing,
        unknown_required_claim_ids=unknown,
        disallowed_claims=disallowed,
        answer_complete=answer_complete,
        authority_status=authority_status,
        support_status=support_status,
        reason_codes=reasons,
    )


def _required_claim_ids(oracle: dict[str, object]) -> tuple[str, ...]:
    claims = oracle.get("required_claims", [])
    if not isinstance(claims, list):
        return ()
    values = []
    for claim in claims:
        if isinstance(claim, str):
            values.append(claim)
        elif isinstance(claim, dict) and isinstance(claim.get("id"), str):
            values.append(claim["id"])
    return tuple(dict.fromkeys(values))


def _stream_state(report: dict[str, object]) -> tuple[bool, int]:
    parser = report.get("parser")
    parser_complete = isinstance(parser, dict) and parser.get("complete") is True
    report_complete = report.get("status") == "complete"
    issues = parser.get("issues", []) if isinstance(parser, dict) else []
    issue_count = len(issues) if isinstance(issues, list) else 1
    return report_complete and parser_complete, issue_count


def _final_answer(report: dict[str, object]) -> str | None:
    command_trace = report.get("command_trace")
    if not isinstance(command_trace, dict):
        return None
    answer = command_trace.get("final_agent_message")
    return answer.strip() if isinstance(answer, str) and answer.strip() else None


def _string_tuple(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(dict.fromkeys(item for item in value if isinstance(item, str)))


def _optional_bool(value: object) -> bool | None:
    return value if isinstance(value, bool) else None


def _review_status(value: object) -> ReviewStatus | None:
    if value in {"pass", "fail", "unknown"}:
        return value  # type: ignore[return-value]
    return None
