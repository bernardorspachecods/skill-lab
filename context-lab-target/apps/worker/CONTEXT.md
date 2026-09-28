# Worker Adapter

This folder owns the independently testable notification delivery cycle.
Business decisions belong in `packages/core`; storage details belong in
`packages/storage`. The baseline exposes `NotificationWorker.run_once`; it has
no standalone process entry point or built-in backoff/dead-letter policy.

## Destinations

- [worker.py](src/context_lab_worker/worker.py) — delivery and success/failure boundary.
- [worker tests](tests/test_worker.py) — successful delivery and pending-on-failure semantics.
- [Product rules](../../docs/product/rules.md) — current assignment notification rule.
- [System boundaries](../../docs/architecture/system-boundaries.md) — asynchronous delivery ownership.
