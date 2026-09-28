from efficiency_validator.network import parse_network_trace, summarize_network


def test_network_trace_keeps_metadata_without_payload() -> None:
    parsed = parse_network_trace(
        [
            '{"type":"network.trace.started",'
            '"schema_version":"network-trace-1",'
            '"run_id":"run-net-1","case_id":"case-net-1",'
            '"trace_id":"trace-net-1","source":"structured-runtime",'
            '"authority":"structured-runtime-observation",'
            '"status":"available"}',
            '{"type":"network.access",'
            '"schema_version":"network-trace-1",'
            '"run_id":"run-net-1","case_id":"case-net-1",'
            '"trace_id":"trace-net-1","event_index":0,'
            '"timestamp":"2026-09-25T10:00:00Z",'
            '"source":"structured-runtime",'
            '"authority":"structured-runtime-observation",'
            '"destination":"api.example.test:443","process":"Codex",'
            '"pid":456,"duration_ms":120,"bytes_sent":180,'
            '"bytes_received":640,"result":"success"}',
        ],
        expected_run_id="run-net-1",
        expected_case_id="case-net-1",
    )

    assert parsed.status == "available"
    assert parsed.events[0].destination == "api.example.test:443"
    assert parsed.events[0].bytes_received == 640
    assert "payload" not in parsed.events[0].to_dict()
    assert summarize_network(parsed)["total_bytes"] == 820


def test_network_trace_mismatch_is_partial() -> None:
    parsed = parse_network_trace(
        [
            '{"type":"network.trace.started",'
            '"schema_version":"network-trace-1",'
            '"run_id":"run-net-1","case_id":"case-net-1",'
            '"trace_id":"trace-net-1","source":"structured-runtime",'
            '"authority":"structured-runtime-observation",'
            '"status":"available"}',
        ],
        expected_run_id="different-run",
        expected_case_id="case-net-1",
    )

    assert parsed.status == "partial"
    assert parsed.issues
