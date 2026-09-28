# Context Lab Target

This repository contains a small workspace application for organising
projects and tasks.

## Navigation map

| If you need... | See |
| --- | --- |
| Application adapters | [apps context](apps/CONTEXT.md#application-adapters) |
| Core and storage modules | [packages context](packages/CONTEXT.md#core-packages) |
| Product and domain rules | [product context](docs/product/CONTEXT.md#product-documentation) |
| Architecture and ownership | [architecture context](docs/architecture/CONTEXT.md#architecture-documentation) |
| Local verification and operations | [operations context](docs/operations/CONTEXT.md#operations-documentation) |
| Durable architecture decisions | [decisions context](docs/decisions/CONTEXT.md#architecture-decisions) |

## Task router

| Request type | First area to open | Likely dependencies |
| --- | --- | --- |
| Build application behaviour | [apps context](apps/CONTEXT.md#application-adapters) or [packages context](packages/CONTEXT.md#core-packages) | Product rules, architecture contracts, and seam tests |
| Trace a cross-area product behaviour | [product rules](docs/product/rules.md) and [system boundaries](docs/architecture/system-boundaries.md) | Relevant implementation seam and tests linked from local maps |
| Check local verification or failure semantics | [operations guide](docs/operations/local-development.md#verify-the-repository) | The linked adapter and test destinations |
| Review an ownership decision | [decisions context](docs/decisions/CONTEXT.md#architecture-decisions) | Product rules and implementation assumptions |

## Repository conventions

- Canonical documentation is in English for the first baseline.
- Product documents distinguish implemented baseline behaviour from intended
  future behaviour.
- Code and tests are the evidence for current runtime behaviour.
