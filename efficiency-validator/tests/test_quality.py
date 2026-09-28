from efficiency_validator.quality import evaluate_quality


ORACLE = {
    "required_claims": [
        {"id": "rule", "description": "The rule is identified."},
        {"id": "storage", "description": "The adapter is distinguished."},
    ],
    "disallowed_claims": ["the API uses SQLite by default"],
    "authoritative_paths": ["docs/product/rules.md"],
}


def _report() -> dict[str, object]:
    return {
        "status": "complete",
        "parser": {"complete": True, "issues": []},
        "command_trace": {"final_agent_message": "complete answer"},
    }


def test_quality_passes_only_when_all_quality_inputs_pass() -> None:
    result = evaluate_quality(
        _report(),
        ORACLE,
        {
            "required_claim_ids": ["rule", "storage"],
            "disallowed_claims": [],
            "answer_complete": True,
            "authority_status": "pass",
            "support_status": "pass",
        },
    )

    assert result.status == "pass"
    assert result.quality_gate_passed is True
    assert result.missing_required_claim_ids == ()
    assert result.reason_codes == ()


def test_quality_fails_for_missing_required_claim() -> None:
    result = evaluate_quality(
        _report(),
        ORACLE,
        {
            "required_claim_ids": ["rule"],
            "disallowed_claims": [],
            "answer_complete": True,
            "authority_status": "pass",
            "support_status": "pass",
        },
    )

    assert result.status == "fail"
    assert result.quality_gate_passed is False
    assert result.missing_required_claim_ids == ("storage",)
    assert "missing_required_claims" in result.reason_codes


def test_quality_fails_for_disallowed_claim_even_when_cheaper() -> None:
    result = evaluate_quality(
        _report(),
        ORACLE,
        {
            "required_claim_ids": ["rule", "storage"],
            "disallowed_claims": ["the API uses SQLite by default"],
            "answer_complete": True,
            "authority_status": "pass",
            "support_status": "pass",
        },
    )

    assert result.status == "fail"
    assert "disallowed_claims" in result.reason_codes


def test_quality_is_indeterminate_without_normalized_review() -> None:
    result = evaluate_quality(_report(), ORACLE, None)

    assert result.status == "indeterminate"
    assert result.quality_gate_passed is False
    assert result.reason_codes == ("quality_review_missing",)


def test_quality_is_indeterminate_when_evidence_is_incomplete() -> None:
    report = _report()
    report["status"] = "incomplete"
    report["parser"] = {"complete": False, "issues": [{"kind": "truncated"}]}
    result = evaluate_quality(
        report,
        ORACLE,
        {
            "required_claim_ids": ["rule", "storage"],
            "disallowed_claims": [],
            "answer_complete": True,
            "authority_status": "pass",
            "support_status": "pass",
        },
    )

    assert result.status == "indeterminate"
    assert "run_incomplete" in result.reason_codes


def test_quality_fails_when_authority_or_support_is_rejected() -> None:
    review = {
        "required_claim_ids": ["rule", "storage"],
        "disallowed_claims": [],
        "answer_complete": True,
        "authority_status": "fail",
        "support_status": "fail",
    }

    result = evaluate_quality(_report(), ORACLE, review)

    assert result.status == "fail"
    assert result.reason_codes == ("authority_failed", "support_failed")
