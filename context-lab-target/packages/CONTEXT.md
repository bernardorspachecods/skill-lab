# Core Packages

This area owns reusable application behaviour and persistence adapters. The
core should remain independent of FastAPI and SQLite-specific details.

## Destinations

- [core/CONTEXT.md](core/CONTEXT.md) — domain rules and use-case orchestration.
- [storage/CONTEXT.md](storage/CONTEXT.md) — SQLite and in-memory adapters.

See the [system boundaries](../docs/architecture/system-boundaries.md) for the
current interfaces and ownership seams.
