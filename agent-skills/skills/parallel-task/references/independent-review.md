# Independent review

Use review mode after a substantive task when the agent or user may be too
invested in the current solution to evaluate it impartially. Review the result,
not the effort spent producing it.

This is a review-only pass. Do not edit product files, implement suggestions,
or silently expand the task. The delegated agent works through one provisional
handoff file: the primary agent prepares it, the reviewer fills it, and the
primary agent and user review it together.

1. Reconstruct the original request, intended outcome, success criteria,
   decisions made, changed artifacts, and verification already performed.
2. Prepare the review packet required by the shared principles: the original
   request or specification, applicable repository guidance, relevant diff or
   output, and the tests, sources, or evidence needed to judge it.
3. Create the review handoff in the repository's designated non-canonical
   findings location. Give it status `in_progress` and include:
   - the review objective and success criteria;
   - the packet and relevant paths;
   - the review scope, non-goals, and constraints;
   - the sections the reviewer must complete.
4. Give the delegated agent the handoff path and instruct it to review the
   completed work independently against the objective, constraints, and
   evidence recorded there. It must adapt the review to the task's scope and
   risk rather than apply a fixed checklist.

5. The agent must read the handoff and packet, preserve their initial content,
   and fill the same handoff with the relevant assessment, evidence,
   uncertainties, and recommended next steps. It must not create a separate
   report, edit canonical files, or implement changes. When finished, change
   the handoff status to `provisional`.

If independent delegation is unavailable, say so explicitly and do not present
the primary agent's own review as independent. Report the handoff's location
and assessment, then wait for the user's approval before applying any change.

Finish when the completed handoff and assessment make clear what is sound, what
should change, what remains unverified, and what decision is pending.
