"""Offline reporting over retained operational bundles; no model calls."""
from __future__ import annotations

from dataclasses import asdict
import json
import math
import os
from pathlib import Path
from datetime import datetime, timezone

from .codex_events import parse_codex_stream
from .operational import VERSION, digest, inventory, write_json


def load_bundle(bundle: Path) -> dict:
    manifest = json.loads((bundle / "manifest.json").read_text())
    if manifest.get("schema") != VERSION:
        raise ValueError("Unsupported bundle schema; use the matching collector/report version")
    if manifest.get("termination") in {"preparing", "running"}:
        raise ValueError("Run is unfinished; finalize or recover it before reporting")
    for name, expected in manifest.get("evidence_hashes", {}).items():
        path = bundle / name
        if not path.resolve().is_relative_to(bundle.resolve()) or not path.is_file() or digest(path.read_bytes()) != expected:
            raise ValueError(f"Evidence integrity failure: {name}")
    for directory, key in (("inputs/target", "input_inventory"), ("outputs/target", "output_inventory")):
        if key in manifest and inventory(bundle / directory) != manifest[key]:
            raise ValueError(f"Evidence integrity failure: {directory}")
    return manifest


def annotate(bundle: Path, *, kind: str, text: str, start: float | None = None,
             end: float | None = None) -> dict:
    manifest = load_bundle(bundle)
    if kind not in {"correction", "hint", "approval", "note"} or not text.strip():
        raise ValueError("Annotation requires a supported kind and nonempty text")
    duration = manifest.get("execution", {}).get("duration_seconds", 0)
    if (start is None) != (end is None) or (start is not None and
        (not all(math.isfinite(v) for v in (start, end)) or not 0 <= start <= end <= duration)):
        raise ValueError("Wait interval must lie within task duration")
    value = {"schema": "intervention-1", "source": "operator-annotation",
             "kind": kind, "text": text, "start_seconds": start, "end_seconds": end,
             "recorded_at": datetime.now(timezone.utc).isoformat()}
    with (bundle / "annotations.jsonl").open("a") as stream:
        stream.write(json.dumps(value) + "\n")
    return value


def _wait_seconds(notes: list[dict]) -> float | None:
    spans = sorted((n["start_seconds"], n["end_seconds"]) for n in notes if n.get("start_seconds") is not None)
    if not spans:
        return None
    total, end = 0.0, 0.0
    for start, stop in spans:
        total += max(0, stop - max(start, end))
        end = max(end, stop)
    return total


def report(bundle: Path) -> dict:
    """Verify evidence then derive a factual report. Missing data stays null."""
    manifest = load_bundle(bundle)
    raw_path = bundle / "events.jsonl"
    lines = raw_path.read_text(errors="replace").splitlines() if raw_path.exists() else []
    parsed = parse_codex_stream(lines)
    arrivals_path = bundle / "events.arrivals.jsonl"
    arrivals = {r["line"]: r["elapsed_seconds"] for r in
                (json.loads(line) for line in arrivals_path.read_text().splitlines())} if arrivals_path.exists() else {}
    timeline, commands, tools, starts, messages, usages = [], [], [], {}, [], []
    for raw in parsed.raw_events:
        event = raw.payload
        elapsed = arrivals.get(raw.event_index)
        timeline.append({"line": raw.event_index, "observed_seconds": elapsed, "event": event})
        if event.get("type") == "turn.started":
            starts.clear()
        item = event.get("item")
        if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            usages.append(event["usage"])
        if not isinstance(item, dict):
            continue
        identifier = item.get("id")
        if event.get("type") == "item.started":
            starts[identifier] = elapsed
        if event.get("type") != "item.completed":
            continue
        if item.get("type") == "agent_message":
            messages.append(item.get("text"))
        if item.get("type") in {"command_execution", "mcp_tool_call", "web_search", "file_change", "tool_call"}:
            start = starts.get(identifier)
            observation = {"line": raw.event_index, "item": item, "start_seconds": start,
                           "end_seconds": elapsed,
                           "observed_duration_seconds": elapsed - start if elapsed is not None and start is not None else None,
                           "execution_duration_seconds": None}
            tools.append(observation)
            if item["type"] == "command_execution":
                commands.append(observation)
    fields = ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens")
    usage = {key: sum(u[key] for u in usages) if usages and all(type(u.get(key)) is int and u[key] >= 0 for u in usages) else None for key in fields}
    usage["total_tokens"] = usage["input_tokens"] + usage["output_tokens"] if usage["input_tokens"] is not None and usage["output_tokens"] is not None else None
    usage["coverage"] = "complete_turns" if parsed.turns and all(t.status == "completed" for t in parsed.turns) and not parsed.issues else "partial_or_unavailable"
    usage["source"] = "events.jsonl:turn.completed.usage"
    notes_path = bundle / "annotations.jsonl"
    notes = [json.loads(line) for line in notes_path.read_text().splitlines()] if notes_path.exists() else []
    checks_path = bundle / "checks.json"
    checks = json.loads(checks_path.read_text()) if checks_path.exists() else []
    changes_path = bundle / "changes.json"
    changes = json.loads(changes_path.read_text()) if changes_path.exists() else None
    outputs = [c["item"].get("aggregated_output") for c in commands]
    text_outputs = [o for o in outputs if isinstance(o, str)]
    repeats = len([o for o in text_outputs if o]) - len(set(o for o in text_outputs if o))
    issues = [asdict(issue) for issue in parsed.issues]
    completed_checks = checks and len(checks) == len(manifest.get("checks_requested", []))
    quality = "pass" if completed_checks and all(c["exit_code"] == 0 and c["termination"] == "exited" for c in checks) else "fail" if checks else "unassessed"
    return {
        "schema": "operational-report-1", "generator": VERSION,
        "generator_sha256": digest(Path(__file__).read_bytes()),
        "manifest": manifest, "execution_status": manifest["termination"],
        "collection_status": "partial" if issues or manifest["termination"] != "completed" else "available",
        "usage": usage, "timeline": timeline, "tools": tools, "commands": commands,
        "final_response": messages[-1] if messages and manifest["termination"] == "completed" else None,
        "last_agent_message": messages[-1] if messages else None,
        "metrics": {"observed_commands": len(commands),
                    "failed_commands": sum(c["item"].get("exit_code") not in (None, 0) or c["item"].get("status") == "failed" for c in commands),
                    "observed_tool_items": len(tools), "identical_nonempty_command_outputs": repeats,
                    "returned_command_output_bytes": sum(len(o.encode()) for o in text_outputs) if len(text_outputs) == len(outputs) else None},
        "timing": {"task_seconds": manifest.get("execution", {}).get("duration_seconds"),
                   "setup_seconds": manifest.get("setup_seconds"), "total_seconds": manifest.get("total_seconds"),
                   "recorded_user_wait_seconds": _wait_seconds(notes),
                   "tool_duration_source": "host receipt timestamps; includes event delivery latency"},
        "interventions": {"coverage": "operator-annotations-only; native interactive input unavailable in exec mode",
                          "observed_count": len(notes), "total_count": None, "records": notes},
        "changes": changes, "checks": checks,
        "quality": {"status": quality, "scope": "explicit evaluator commands only; not general answer quality"},
        "issues": issues,
        "limitations": ["Only CLI-emitted events are observed; filesystem reads and actual model context are not certified.",
                        "Command output bytes are exposed UTF-8 text, not filesystem bytes or tokens; upstream truncation can be unknown.",
                        "Global instructions, skills, environment, system policy and provider caches are not fully isolated.",
                        "No automatic relevance classification or complete search/read count; inspect command inputs and outputs.",
                        "Requested model is recorded; provider-resolved model may be unavailable.",
                        "Event timestamps measure host receipt, not exact tool execution; parallel durations must not be summed as wall time."]}


def render_report(value: dict, evidence_prefix: str = "..") -> str:
    m = value["manifest"]
    lines = [f"# Run {m['run_id']}", "", f"Variant: {m['variant']}",
             f"Execution: {value['execution_status']} | Evidence: {value['collection_status']}",
             f"Quality checks: {value['quality']['status']} (explicit evaluator checks only)", "",
             "## Costs", "", "| Metric | Value |", "| --- | --- |"]
    for key, val in {**value["metrics"], **{k: v for k, v in value["usage"].items() if k.endswith("tokens")},
                     **{k: v for k, v in value["timing"].items() if k.endswith("seconds")}}.items():
        lines.append(f"| {key} | {val if val is not None else 'unavailable'} |")
    lines.extend(["", "## Configuration", "", "```json", json.dumps({key: m.get(key) for key in
                  ("model_requested", "model_resolved", "reasoning", "sandbox", "versions", "input_sha256", "overlay_paths", "cache_state", "budget_support")}, indent=2), "```",
                  "", "## Activity", ""])
    for tool in value["tools"]:
        lines.extend([f"### Event line {tool['line']} — {tool['item'].get('type')}", "",
                      "````json", json.dumps(tool, indent=2, ensure_ascii=False), "````", ""])
    lines.extend(["## Final response", "", value["final_response"] or "unavailable", "",
                  "## Work products and interventions", "", "```json",
                  json.dumps({"changes": value["changes"], "checks": value["checks"], "interventions": value["interventions"]}, indent=2), "```",
                  "", "## Evidence", "", "Links to the retained bundle:", "",
                  *[f"- [{name}](<{evidence_prefix}/{name}>)" for name in
                    ("manifest.json", "events.jsonl", "events.arrivals.jsonl", "events.stderr", "inputs/", "outputs/", "changes.json", "changes.patch", "checks.json")],
                  "", "## Limitations", ""])
    lines.extend("- " + item for item in value["limitations"])
    if value["issues"]:
        lines.extend(["", "Parser issues:", "```json", json.dumps(value["issues"], indent=2), "```"])
    return "\n".join(lines) + "\n"


def save_report(bundle: Path, output: Path | None = None) -> dict:
    result = report(bundle)
    destination = output or bundle / "derived"
    destination = destination.resolve()
    protected = bundle.resolve()
    if destination == protected or any(destination.is_relative_to(protected / d) for d in ("inputs", "outputs")):
        raise ValueError("Report output must not overwrite retained evidence")
    destination.mkdir(parents=True, exist_ok=True)
    write_json(destination / "report.json", result)
    (destination / "report.md").write_text(render_report(result, Path(os.path.relpath(bundle.resolve(), destination)).as_posix()))
    return result
