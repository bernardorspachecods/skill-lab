# Architecture Documentation

This folder records the intended system structure, ownership seams, and
cross-area contracts. Code and tests remain the final evidence of current
runtime behaviour.

## Destinations

- [system-boundaries.md](system-boundaries.md) — module seams and cross-area
  contracts.
- [core tests](../../packages/core/tests/test_task_service.py) — domain/use-case evidence.
- [API tests](../../apps/api/tests/test_app.py) — HTTP boundary evidence.
- [worker tests](../../apps/worker/tests/test_worker.py) — delivery evidence.
- [SQLite tests](../../packages/storage/tests/test_sqlite.py) — persistence evidence.
