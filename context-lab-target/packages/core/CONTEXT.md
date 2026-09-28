# Core Behaviour

This folder owns project and task rules, permission decisions, and use-case
orchestration. Its external interface should stay small and should not expose
FastAPI, SQLite, or worker mechanics.

## Destinations

- [services.py](src/context_lab_core/services.py) — current task creation use case.
- [core tests](tests/test_task_service.py) — membership, assignment, and notification coverage.
- [Product rules](../../docs/product/rules.md) — authoritative current/future product status.
- [System boundaries](../../docs/architecture/system-boundaries.md) — cross-area contracts.
