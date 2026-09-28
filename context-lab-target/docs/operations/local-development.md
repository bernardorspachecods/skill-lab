# Local Development

The application must be testable locally without external services. The API's
default demo process uses in-memory stores; the SQLite adapter is available for
durable storage tests. The worker is an independently testable library cycle,
not a standalone production process in this baseline.

## Navigation map

| If you need... | See |
| --- | --- |
| Verify application contracts | [Verify the repository](#verify-the-repository) |
| Run the API demo | [Run the API locally](#run-the-api-locally) |
| Inspect worker delivery semantics | [Inspect a worker cycle](#inspect-a-worker-cycle) |

## Verify the repository

Run the test suite with:

```sh
UV_CACHE_DIR=/tmp/context-lab-uv-cache uv run --extra test pytest
```

The test suite covers the core use case, the in-memory and SQLite storage
adapters, the HTTP adapter, and worker success and failure semantics:

- [core tests](../../packages/core/tests/test_task_service.py)
- [SQLite tests](../../packages/storage/tests/test_sqlite.py)
- [API tests](../../apps/api/tests/test_app.py)
- [worker tests](../../apps/worker/tests/test_worker.py)

## Run the API locally

```sh
PYTHONPATH=packages/core/src:packages/storage/src:apps/api/src \
  UV_CACHE_DIR=/tmp/context-lab-uv-cache \
  uv run uvicorn context_lab_api.app:app
```

The default process uses an in-memory demo workspace. SQLite-backed API
configuration is not part of this baseline; the storage adapter itself is
covered independently by tests.

## Inspect a worker cycle

The baseline has no worker process entry point. Instantiate
`NotificationWorker.run_once` with a `NotificationStore` and a delivery
adapter; [the worker tests](../../apps/worker/tests/test_worker.py) are the
executable reference for success and failure behaviour.
