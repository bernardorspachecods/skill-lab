# API Adapter

This folder owns the FastAPI adapter: routing, request validation, response
mapping, and HTTP error translation. Business rules belong in
`packages/core`; persistence details belong in `packages/storage`.

## Destinations

- [app.py](src/context_lab_api/app.py) — task creation route and request/response mapping.
- [API tests](tests/test_app.py) — authentication, membership, and assignee coverage.
- [Product rules](../../docs/product/rules.md) — ownership and assignment rules.
- [System boundaries](../../docs/architecture/system-boundaries.md) — cross-area contract.
