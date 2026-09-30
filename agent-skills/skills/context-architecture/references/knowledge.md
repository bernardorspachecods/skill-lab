# Repository knowledge structure

This reference defines the repository-level organization for reusable,
repository-specific knowledge. It describes the knowledge area and its
relationship to repository context, plans, and source artifacts. It does not
specify when an agent should consult or promote knowledge.

## Purpose and ownership

Repository knowledge is a maintained collection of information that can serve
multiple tasks in one repository. Keep it distinct from:

- skills, which define reusable agent behavior;
- `CONTEXT.md`, which routes agents to relevant areas and documents;
- plans and their task-specific working or audit artifacts;
- implementation documentation whose canonical owner is the code or project;
- temporary notes and unverified research material.

The knowledge area owns the reusable synthesis and its limitations. Source
artifacts remain the evidence for claims and must stay resolvable through the
knowledge entry's provenance.

## Organization and discovery

A repository that maintains repository-level knowledge uses a dedicated
`knowledge/` area. Its root context map links to the knowledge entrypoint,
usually `knowledge/INDEX.md`, and states that the destination contains
repository-level reusable knowledge. Keep this as a routing pointer; do not
load the whole knowledge area as default context.

Knowledge created for one plan may remain in that plan root's `knowledge/`
area, shared by the root plan and all its subplans. Do not create separate
knowledge areas in subplan directories. Repository-level and plan-local
knowledge have separate identity scopes and must not be mixed merely because
their subjects overlap.

Use the plan-management skill's shared `artifact_ids.py` allocator to reserve
IDs. Run it with `KNOW` for repository-level knowledge or add `--root LR-01`
for plan-local knowledge:

```bash
python3 <plan-management-skill>/scripts/artifact_ids.py <repository> KNOW
python3 <plan-management-skill>/scripts/artifact_ids.py <repository> KNOW --root LR-01
python3 <plan-management-skill>/scripts/artifact_ids.py <repository> AUD --root KNOW-01
python3 <plan-management-skill>/scripts/artifact_ids.py <repository> WORK --root KNOW-01
```

Use stable IDs for relationships; the plan validator builds an in-memory
index to check IDs and anchors against current locations. Do not maintain a
second registry of paths in the index.

Keep repository knowledge artifacts in shared type folders: `knowledge/audit/`
for supporting evidence audits and `knowledge/working/` for retained working
files. Name each artifact under its knowledge entry, using `<KNOW-ID>.AUD-##`
for audits and `<KNOW-ID>.WORK-##` for working files. For example:

```text
knowledge/
├── KNOW-01.md
├── audit/
│   ├── KNOW-01.AUD-01.md
│   └── KNOW-01.AUD-02.md
└── working/
    └── KNOW-01.WORK-01.md
```

The `AUD` and `WORK` ordinals are allocated separately for each knowledge ID.
The knowledge entry's `derived_from` lists the supporting artifact IDs. Each
artifact declares `belongs_to` as its owning knowledge ID. Promoted research
artifacts also record their original research ID, role, and requester as
`source_artifact_id`, `source_artifact_role`, and `source_requested_by`.

## Identities and entries

Each knowledge entry is an entity with its own `KNOW` ID. Plan-local knowledge
includes its root plan ID, such as `LR-01.KNOW-04`. Repository-level knowledge
uses the repository-wide sequence without a plan prefix, such as `KNOW-12`.
The allocator assigns and reserves IDs; agents do not choose numbers. Ordinals
use at least two digits, and removed IDs are never reused.

Give each entry one clear, reusable purpose. Before creating an entry, check
whether an existing entry serves that same purpose. Update the existing entry
when its purpose remains the same; create another entry when it serves a
distinct purpose that should be consulted separately.

An entry contains its assigned ID, title, intended utility, knowledge content,
applicable scope, limitations, and concrete provenance. Use the repository's
established file and metadata conventions; do not copy `PLAN` frontmatter to a
knowledge entry. Knowledge metadata includes `derived_from` references to the
specific source artifacts that support its content.

When an entry is enriched, update its provenance to cover the retained content.
When plan-local knowledge becomes repository-level knowledge, use the
repository-level identity and move each supporting research audit into
`knowledge/audit/` as part of promotion. Move a retained research working file
into `knowledge/working/` when it supports the promoted entry. Reassign each
moved audit or working file a knowledge-owned ID such as `KNOW-01.AUD-01` or
`KNOW-01.WORK-01`, rename its file to match, and set `belongs_to` to the owning
knowledge ID. Preserve the former research ID, artifact role, and requester in
`source_artifact_id`, `source_artifact_role`, and `source_requested_by`. Update
the knowledge entry's `derived_from` and all links or references to the new IDs.
Keep one canonical copy. Do this before the plan can be deleted, so the
promoted entry and its evidence remain self-contained in `knowledge/`.

## Index

If the repository maintains `knowledge/INDEX.md`, keep it as a short discovery
catalog with one row per repository-level entry:

| ID | Title | Utility |
|---|---|---|
| KNOW-12 | Authentication patterns | Define authentication and authorization |

The ID links to the entry through the repository's relative Markdown link
conventions. The index is a discovery aid, not an access boundary: agents may
also consult relevant entries through a direct ID reference or repository
search, even when an entry is not listed in the index. The index contains no
path, status, relationship, version, consultation, or review-state columns.
Keep content, provenance, and limitations in the entry itself.
