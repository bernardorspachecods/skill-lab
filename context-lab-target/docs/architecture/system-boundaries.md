# System Boundaries

The application is a small monorepo with a narrow core interface and concrete
adapters around it.

## Navigation map

| If you need... | See |
| --- | --- |
| Ownership of code and decisions | [Ownership](#ownership) |
| Module seams | [Seams](#seams) |
| Cross-area behaviour | [Cross-area contracts](#cross-area-contracts) |
| What confirms the intended design | [Verification source](#verification-source) |

## Current baseline status

The boundaries below describe both stable ownership and the deliberately
small implementation baseline. The API's default demo process uses the
in-memory adapter; SQLite is the durable adapter and is covered independently
by [its adapter tests](../../packages/storage/tests/test_sqlite.py).

## Ownership

- `packages/core` owns domain rules, permission decisions, and use-case
  orchestration.
- `packages/storage` owns persistence implementations.
- `apps/api` owns HTTP translation and request lifecycle concerns.
- `apps/worker` owns asynchronous notification delivery.

## Seams

The API and worker call use cases exposed by the core. The core requests state
through storage interfaces. SQLite is the durable storage adapter; the API's
default demo process uses an in-memory adapter, and focused core/API tests use
the same in-memory seam.

The core must not import FastAPI or SQLite types. Adapters translate their
external concerns at the seam and keep those details out of callers.

## Cross-area contracts

- The current task creation command enforces workspace membership before
  changing task state; see [the core use case](../../packages/core/src/context_lab_core/services.py)
  and [its tests](../../packages/core/tests/test_task_service.py).
- Creating a task with an assignee creates a notification record synchronously;
  the worker handles delivery. Completion notifications are future behaviour
  because the baseline has no completion use case.
- The HTTP adapter exposes task creation and passes `assignee_id` to core; see
  [the API adapter](../../apps/api/src/context_lab_api/app.py) and [API tests](../../apps/api/tests/test_app.py).
- The API exposes product concepts and errors, not storage implementation
  details.

## Verification source

This document describes ownership and current cross-area contracts. Product
intent that is not implemented is labelled as future above. Tests and runtime
code confirm the behaviour that actually exists; when they disagree, the
discrepancy must be resolved rather than hidden in documentation.
