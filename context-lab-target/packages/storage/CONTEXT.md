# Storage Adapters

This folder owns concrete persistence implementations. SQLite is the durable
adapter; the in-memory adapter supports focused tests and the API demo.
Storage adapters satisfy interfaces defined at the core seam.

## Destinations

- [memory.py](src/context_lab_storage/memory.py) — in-memory adapter used by focused tests and the API demo.
- [sqlite.py](src/context_lab_storage/sqlite.py) — durable SQLite adapter.
- [SQLite tests](tests/test_sqlite.py) — persistence round-trip coverage.
- [System boundaries](../../docs/architecture/system-boundaries.md) — adapter ownership and runtime status.
