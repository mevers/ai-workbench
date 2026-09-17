# Assessment review and release

Use a source reviewer and a learner reviewer, different from each other and from the assessed material's author. They may be the same people as the summary reviewers. Give them the user's standards and confirmed context. Keep writer rationale, prior review findings and the other reviewer's judgement out of the initial review.

## Complete-content round

The source reviewer checks targets, answers, feedback and practice against the approved key ideas, plan and relevant source passages. Investigate ambiguity directly in the book. Verify that printed facts support the requested judgement, the strongest alternative is wrong for a meaningful reason, and practice uses the book's mechanism. A preliminary inquiry must not be presented as an established diagnosis.

The learner reviewer first receives copies with entire answer blocks removed using `validate_assessment.py --blind-file`. For each question, save the selected answer or ambiguity and any cue; for practice, check the printed people, work, problem, action and useful result. Correct selection alone is insufficient. An answer must not stand out through polish, length, caution or an obviously unreasonable set of alternatives. A practice must be usable without inventing its central task. Save the first pass before opening full files, then check feedback without erasing initial findings.

Keep records concise: brief per-item evidence and exact defects are enough. Review completed groups in parallel with writing elsewhere, then check the complete bundle's scope and variety. If a key idea changes, check its assessment alignment.

## Consolidate and verify

Missing facts, wrong or ambiguous answers, implausible scenarios, answer cues, material reading difficulty and unusable practice are blockers. Optional polish is advisory. Replace weak items as whole questions or exercises; do not add defensive clauses. Prefer a source-grounded recap when the context does not support useful application.

Keep the same reviewer pair through completion. After one consolidated repair, verify changed quizzes, relevant plan sections and affected dependencies. Preserve unchanged approvals and first-pass evidence. A changed question receives a new answer-blind attempt before feedback is checked. Broad changes justify broader checking; local changes do not restart the complete assessment review.

Reviewers maintain their own `_work/assessment-reviews/source-aware-review.md` and `context-language-review.md` using the output schema. Include every file's decision, a positive review-wave number and the current aggregate bundle digest. Record which files were verified again and which earlier approvals were retained. Update the source record's plan digest after checking changed plan entries. Context changes affect both reviewers. Do not refresh a digest without the corresponding verification.

PASS requires no unresolved blockers, current hashes and both semantic approvals. Run `validate_output.py` for the requested mode. These checks establish reviewed completion, not mastery or guaranteed future learning.

When changing assessment validation, run `test_validate_assessment.py`. Validate workflow changes on actual generated assessments and preserve user-rejected results as evidence rather than treating previous model agreement as proof.
