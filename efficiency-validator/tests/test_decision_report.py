from efficiency_validator.decision_report import (
    build_decision_report,
    render_markdown,
)


def _run(run_id: str, variation: str, total_tokens: int) -> dict[str, object]:
    return {
        "label": variation,
        "report_path": f"runs/{run_id}/report.json",
        "report": {
            "manifest": {
                "run_id": run_id,
                "case_id": "case-1",
                "variation": variation,
                "prompt": f"Prompt for {variation}",
                "model": "codex-default",
                "complete": True,
            },
            "observability": {
                "raw_event_count": 42,
                "tokens": {
                    "status": "available",
                    "totals": {
                        "input_tokens": total_tokens - 100,
                        "cached_input_tokens": 50,
                        "output_tokens": 100,
                        "reasoning_output_tokens": 25,
                        "total_tokens": total_tokens,
                    },
                },
                "filesystem": {
                    "status": "available",
                    "authority": "os-kernel-observation",
                    "events": [
                        {"operation": "open", "path": "/target/docs/rules.md"},
                        {"operation": "open", "path": "/target/docs/rules.md"},
                    ],
                    "issues": [],
                },
            },
            "command_trace": {
                "command_count": 8,
                "failed_command_count": 0,
                "agent_message_count": 2,
            },
        },
        "quality": {
            "quality": {
                "status": "pass",
                "missing_required_claim_ids": [],
                "disallowed_claims": [],
            }
        },
    }


def test_decision_report_surfaces_decision_fields_without_raw_event_dump() -> None:
    comparison = {
        "schema_version": "comparison-report-1",
        "comparison": {
            "verdict": "inconclusive",
            "evidence_status": "exploratory",
            "primary_metric": "tokens",
            "reasons": ["high_run_to_run_variance"],
            "deltas": {
                "tokens": {"absolute": -10, "relative": -0.01},
                "commands": {"absolute": -1, "relative": -0.1},
            },
            "prompt_diff": {
                "same_exact_prompt": False,
                "unified_diff": "--- baseline\n+++ candidate",
            },
        },
    }
    aggregate = {
        "schema_version": "aggregate-report-1",
        "verdict": "inconclusive",
        "evidence_status": "exploratory",
        "pair_count": 3,
        "verdict_counts": {"better": 2, "same": 1},
        "reason_codes": ["high_run_to_run_variance"],
    }

    summary = build_decision_report(
        [_run("run-base", "baseline", 1000), _run("run-candidate", "candidate", 990)],
        comparison=comparison,
        aggregate=aggregate,
    )
    markdown = render_markdown(summary)

    assert summary["decision"]["verdict"] == "inconclusive"
    assert summary["decision"]["evidence_status"] == "exploratory"
    assert "Prompt for baseline" in markdown
    assert "high_run_to_run_variance" in markdown
    assert "raw_events" not in markdown
    assert "175" not in markdown
    assert "filesystem" in markdown.lower()


def test_decision_report_exposes_exact_read_ledger_without_raw_content() -> None:
    run = _run("run-exact", "exact", 1000)
    run["report"]["observability"]["exact_read"] = {
        "status": "available",
        "valid": True,
        "file_count": 1,
        "read_count": 1,
        "total_bytes": 12,
        "total_lines": 2,
        "processes": [{"pid": 42, "process": "sed"}],
        "files": [
            {
                "path": "/target/docs/rules.md",
                "file_size": 100,
                "line_count": 10,
                "content_sha256": "file-hash",
            }
        ],
        "events": [
            {
                "event_index": 0,
                "pid": 42,
                "process": "sed",
                "path": "/target/docs/rules.md",
                "operation": "read",
                "offset": 20,
                "bytes": 12,
                "line_start": 3,
                "line_end": 4,
                "content_sha256": "content-hash",
                "file_sha256": "file-hash",
                "content_base64": "c2VjcmV0",
            }
        ],
        "invalid_reasons": [],
    }

    summary = build_decision_report([run])
    markdown = render_markdown(summary)

    assert "Exact file-read audit" in markdown
    assert "/target/docs/rules.md" in markdown
    assert "3-4" in markdown
    assert "file-hash" in markdown
    assert "c2VjcmV0" not in markdown
