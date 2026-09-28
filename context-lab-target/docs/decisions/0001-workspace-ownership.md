# Workspace owns projects and memberships

Status: accepted

The workspace is the ownership boundary for projects and memberships, while a
project owns its tasks. This gives permission checks one stable scope and makes
cross-area navigation explicit; a project cannot be shared directly between
workspaces in the canonical baseline.

## Consequences

- Every project and task access path needs a workspace membership check.
- Evaluation cases can test both local project work and cross-boundary
  permission reasoning.
- Future sharing across workspaces would be a deliberate domain change rather
  than an incidental storage feature.
