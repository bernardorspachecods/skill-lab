from efficiency_validator.path_categories import classify_path


def test_path_categories_prefer_specific_roots_and_keep_unknown_explicit() -> None:
    roots = {
        "target": ("/work/target",),
        "skill": ("/Users/test/agent-skills",),
        "evaluator": ("/work/context-lab-evaluator",),
        "external-context": ("/work/shared-context",),
        "other-repository": ("/work/other-repo",),
        "cache-dependency": ("/Users/test/.cache",),
    }

    assert classify_path("/work/target/docs/rules.md", roots) == "target"
    assert classify_path("/Users/test/agent-skills/chat-start/SKILL.md", roots) == "skill"
    assert classify_path("/work/context-lab-evaluator/oracle.json", roots) == "evaluator"
    assert classify_path("/work/shared-context/CONTEXT.md", roots) == "external-context"
    assert classify_path("/work/other-repo/app.py", roots) == "other-repository"
    assert classify_path("/Users/test/.cache/pkg/index", roots) == "cache-dependency"
    assert classify_path("/Users/test/agent-skills/check-docs/SKILL.md", {}) == "skill"
    assert classify_path("/Users/test/.codex/sessions/run.jsonl", {}) == "external-context"
    assert classify_path("/secret/unknown.txt", roots) == "sensitive-unknown"
