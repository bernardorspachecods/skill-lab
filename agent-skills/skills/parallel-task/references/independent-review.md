# Independent review

Use review mode after a substantive task when the agent or user may be too
invested in the current solution to evaluate it impartially. Review the result,
not the effort spent producing it.

This is a review-only pass. Do not edit product files, implement suggestions,
or silently expand the task. The primary agent prepares a temporary execution
plan, one reserved findings file for the reviewer, and `review.md`. The
reviewer fills only its findings file; the primary agent owns the plan and
review file.

1. Reconstruct the original request, intended outcome, success criteria,
   decisions made, changed artifacts, and verification already performed.
2. Prepare the review packet required by the shared principles: the original
   request or specification, applicable repository guidance, relevant diff or
   output, and the tests, sources, or evidence needed to judge it.
3. Create the temporary execution plan and review packet in the repository's
   designated non-canonical findings location. Give the plan status
   `in_progress` and include:
   - the review objective and success criteria;
   - the packet and relevant paths;
   - the review scope, non-goals, and constraints;
   - the reviewer's reserved findings path;
   - the sections the reviewer must complete.
4. Give the delegated agent the execution-plan path and its reserved findings
   path. Instruct it to review the
   completed work independently against the objective, constraints, and
   evidence recorded there. It must adapt the review to the task's scope and
   risk rather than apply a fixed checklist.

5. The reviewer must read the execution plan and packet, then fill only its
   reserved findings file with the relevant assessment, evidence,
   uncertainties, and recommended next steps. It must not edit the execution
   plan or review file, create another report, edit canonical files, or
   implement changes. When finished, leave the plan for the coordinator to
   change to `awaiting_review`.

If independent delegation is unavailable, say so explicitly and do not present
the primary agent's own review as independent. Report the packet's location and
assessment, then wait for the user's approval before applying any change.

Finish when the findings and `review.md` make clear what is sound, what should
change, what remains unverified, what decision is pending, and whether cleanup
is ready. The primary agent and user must complete the joint review before
adopting any conclusion or deleting the temporary packet.
