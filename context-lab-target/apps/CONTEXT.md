# Application Adapters

This area owns adapters that expose the core use cases to external execution
environments. It must not own domain rules or storage details.

## Destinations

- [api/CONTEXT.md](api/CONTEXT.md) — HTTP adapter and request/response mapping.
- [worker/CONTEXT.md](worker/CONTEXT.md) — background execution adapter.

See the [system boundaries](../docs/architecture/system-boundaries.md) for the
current application seams.
