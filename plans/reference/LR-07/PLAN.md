---
plan_id: LR-07
kind: root
parent: null
phase: root
status: complete
depends_on: []
consumers: []
execution:
  research: "standard"
  root_research: false
  research_working: true
  review: true
  user_checkpoints: plan_completion
---

# LR-07

## Objective

Supplement KNOW-02 with verified first-party guidance from AI-agent vendors,
integrated into the existing explanation of feedback-loop cases and use
patterns. Preserve the distinction between vendor-documented practices and
empirically demonstrated effects.

## Scope

This is a targeted supplement to completed plan LR-06. Reuse KNOW-02 and its
three supporting audits for the existing empirical findings, case structure,
and evidence boundaries. The gap is the missing first-party guidance from
Claude, ChatGPT/Codex, and other relevant vendor sites.

Search official product documentation, technical guides, cookbooks, examples,
and vendor-authored practice articles that directly explain how to configure
or use feedback loops in user workflows with AI agents. Prioritize patterns
that fit the existing knowledge entry: goal-based iteration, checks and
verification, user steering or approval, repair/retry limits, recurring or
scheduled work, and autonomy or handoff controls. Start with Anthropic/Claude
and OpenAI/ChatGPT/Codex, then include other vendors whose official sources
meet the same relevance standard. Bound the source set; do not claim to cover
every AI vendor or product.

Treat vendor material as first-party documentation of a capability, design,
or recommended practice. Do not use it alone to claim that a pattern improves
outcomes. Distinguish product descriptions, vendor recommendations, claims of
effectiveness, and independently tested findings; record a source's date,
product/version, source type, and limits. Use targeted follow-up research in
S2 only to resolve gaps discovered in S1 or verify claims needed for
integration.

Integrate the guidance into existing KNOW-02 text where it fits the current
topic and cases. Do not add a standalone vendor-guidance section or introduce
a new subject. Preserve the existing empirical findings and caveats. The
updated entry will cite two new supporting audits and retain one canonical
knowledge entry.

## Output

An updated KNOW-02 with first-party vendor guidance woven into its current
  sections, plus promoted source audits `KNOW-02.AUD-04` and
  `KNOW-02.AUD-05`. The
existing entry's scope and subject remain feedback loops in AI-agent user
workflows; new source material is labeled by source type and evidence role.

## Current phase

All planned work is complete and reconciled. S1's research audit and formal
review pass after the S6 outcome correction and Microsoft access note. S2's
targeted gap audit found no additional source need; the KNOW-02 integration,
audit promotion, and provenance pass independent review. The user confirmed
both plans are done and requested retention under `plans/reference/`.

## Sequence

1. **S1 — Audit first-party vendor guidance** ([LR-07.SP-01](subplans/LR-07.SP-01/PLAN.md))
   - **Action:** Research official vendor sources for guidance on feedback,
     iteration, verification, stopping, user control, and recurring work;
     distinguish documented practices from claims of effectiveness.
   - **Output:** Standard-rigor source audit and retained discovery log,
     independently reviewed before use by S2.
   - **Exit check:** Relevant official source families have been searched;
     sources are classified and claims bounded; material omissions and search
     limits are explicit; independent review is complete.

2. **S2 — Integrate the guidance into KNOW-02** ([LR-07.SP-02](subplans/LR-07.SP-02/PLAN.md))
   - **Action:** Use the reviewed S1 audit, conduct only targeted follow-up
     research where needed, and weave supported vendor guidance into the
     existing knowledge entry without a new section or topic.
   - **Output:** Updated KNOW-02 and a second reviewed source audit capturing
     any follow-up research and integration provenance; both new audits
     promoted as `KNOW-02.AUD-04` and `KNOW-02.AUD-05`.
   - **Exit check:** The update preserves the existing empirical synthesis,
     attributes vendor guidance accurately, has no unsupported effectiveness
     claims or standalone new subject, passes independent review, and has
     reconciled provenance and links.

## Completion criteria

- The work is limited to first-party vendor material that helps explain
  existing feedback-loop concepts, cases, or configuration advice in KNOW-02.
- At least Anthropic/Claude and OpenAI/ChatGPT/Codex official source routes
  are searched; other vendors are included when official material directly
  matches the scope.
- Vendor statements about capabilities, product design, and recommended use
  are clearly labeled. Marketing assertions are not treated as empirical
  effects; independently verified outcomes remain distinguishable.
- Added guidance is integrated into existing sections and current cases;
  no standalone vendor chapter or new subject is introduced.
- Every added claim is linked to a reviewed audit and source, with dates,
  product/version context, and access or evidence limits recorded.
- KNOW-02's existing empirical findings, cautions, and transfer limits remain
  intact; its `derived_from` and provenance are updated for the two new audits.
- S1 and S2 outputs pass independent review; the coordinator reconciles the
  knowledge entry, audit metadata, links, and index if needed.
- Strict plan validation passes and the reconciled update is presented at the
  plan-completion checkpoint.

## Outcome

Completed. KNOW-02 now includes reviewed vendor guidance in its existing
sections, with AUD-04 and AUD-05 promoted and linked. The prior empirical
synthesis remains intact. No additional reusable knowledge candidate was
identified beyond the canonical KNOW-02 entry and its five audits; their
material provenance is preserved in the promoted audit records. The plan is
archived for workflow history at `plans/reference/LR-07/`.
