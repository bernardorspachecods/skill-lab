# Maintenance

This directory keeps quality criteria for the field manual itself.

## Validation

Run:

```bash
python3 scripts/validate_repo.py
```

The validator checks:

- required encyclopedia, pattern, example, and source files exist;
- Markdown links resolve;
- knowledge topics contain required behavior sections;
- source trails reference known source IDs;
- source notes referenced by `sources/SOURCE_INDEX.md` exist;
- stale product-shell directories are absent;
- product-package language and placeholders do not re-enter the docs.

## Editorial Quality Bar

A topic is useful only if it teaches behavior:

- what the LLM should do;
- what the LLM should not do;
- common pitfalls or failure modes;
- when to ask the human;
- how to verify or ground the work;
- source trail.

Do not add new topics without source support unless the file clearly marks the area as an open question.
