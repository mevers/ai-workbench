# Summary review

Use two independent roles, neither reviewing their own writing. Their work should improve the explanation, not generate a parallel book of review notes.

## Round 1: design

The source reviewer independently derives the indispensable argument and models from the source index and bounded passages before seeing the synthesis plan. Compare the plan against that baseline, including essential pairs, causal relationships, evidence and limits. The learner editor checks whether the planned sequence teaches a small number of central ideas with a clear progression. Resolve missing concepts and overloaded groupings before drafting the whole book.

## Round 2: complete content

The source reviewer verifies the final overview and every key idea against direct source evidence. Check the whole conceptual hierarchy as well as individual claims. Verify each example against its source passage. Invented scenarios, details or dialogue are blockers, even when labelled illustrative. A term appearing in the text is insufficient: verify the complete model and the relationships that make it meaningful.

The source-blind reader receives final learner files and embedded images without source notes, plans or intended interpretations. Review the overview first, before reading the key ideas. Record unclear references and unexplained connections before proceeding. Read the key ideas in order, inspect the images, and judge whether a newcomer can follow and retain the explanation. Record first-read problems before reconstructing the argument. Familiarity must not fill a gap. Judge pacing and conceptual density as well as sentence clarity; a fluent collection of definitions can still fail.

If the learner editor saw the design, use a different reader for this source-blind round. The complete-content reviewer pair stays through repairs. Authors may deliver groups for review as they finish; include a final whole-book coherence check.

## Repair and approval

A blocker is a material gap in coverage, meaning, fidelity, explanation or usability. A missing central model or relationship invalidates the bundle's coverage approval, even if other passages are correct. Optional polish is advisory and does not trigger a repair round.

Report all findings together. Rebuild affected explanations in one substantive repair, then have the same reviewers verify changed files and affected relationships. Retain approvals for unchanged files. A wider conceptual change requires a wider coverage check. Continue resolving actual defects; do not restart full reviews or replace reviewers merely because a repair was needed.

Reviewers write their own concise records: `key-idea-drafts/key-idea-NN-source-blind-review.md` and `...-source-aware-review.md`; overview records go in `final-reviews/`. Include reviewer identity, a positive `**Review wave:**`, current learner SHA-256, and these headings: `Review conditions`, `Reader reconstruction`, `Blockers`, `Advisories`, `Gate decision`. The blind record adds `Plain-language and style` with first-read evidence and the hardest passage. The aware record adds `Independent coverage baseline` and `Source terminology and fidelity` with exact anchors. Short substantive entries are sufficient.

Use `Decision: PASS` only with `None.` under Blockers. Changed files require renewed hashes and both approvals. Record design, complete-content and repair rounds in the final audit. Run `validate_learner_quality.py`; it checks records and hashes, not semantic quality.
