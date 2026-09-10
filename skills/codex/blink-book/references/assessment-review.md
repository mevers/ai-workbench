# Assessment review and release

Use this reference only for assessment work. Assessment quality requires two independent semantic reviewers. Structural validation cannot replace either review.

## Reviewer 1: Source-aware assessment review

Use a reviewer with no conversation fork. Give it:

- the final key ideas;
- relevant source-evidence notes and bounded source excerpts;
- `_work/assessment-plan.md`;
- the final quizzes and `review.md`; and
- the confirmed application context when the assessment is contextual.

Do not provide writer rationale, drafts, repair history, the other review, expected decisions, or prior failures.

For every question and practice, verify:

- the source anchor supports the tested mechanism;
- the route is justified;
- Quick recall tests an important idea rather than trivial wording;
- Apply makes the source mechanism decisive to one immediate judgement;
- Try this practises the mechanism through a credible present action;
- contextual facts do not exceed the quoted context evidence;
- the answer mode and precommitted answer set are defensible;
- distractors represent meaningful errors and do not create multiple unintended answers;
- explanations correctly connect every answer to the book concept; and
- review questions are new and source-grounded.

Record the result in `_work/assessment-reviews/source-aware-review.md` using the compact template. Identify the most vulnerable item in each assessment file and classify every finding by severity.

## Reviewer 2: Context, language, and practice review

Use a different reviewer with no conversation fork and no source material, source notes, assessment plan, answer key, writer rationale, prior review, repair history, expected decisions, or prior failures. Give it only:

- the confirmed application context, if contextual; and
- the final learner-facing assessment files with `Correct answer(s)` lines removed but explanations retained.

For every item, test the exact learner-facing words:

- Can a capable first-time learner identify every actor, object, action, referent, decision, and result without mentally supplying missing facts?
- Is every important phrase ordinary language or explicitly established in the page or application context?
- Does any generic container phrase stand in for a concrete comment, question, feedback, report, decision, or action that could be named directly? Apply this test to explanations as well as stems and options.
- Does the situation follow from the application context without an invented meeting, artefact, workflow, audience, motive, reaction, or event sequence?
- Would people plausibly behave or speak this way? Fail convenient dialogue that states a feeling, interpretation, or book construct a person would more likely leave implicit.
- Do all options answer the same question in parallel form without signalling the answer through length, nuance, qualification, courtesy, or completeness?
- Does the explanation clarify the options without supplying missing question facts?
- Is Try this a useful action now in a familiar, context-supported moment?

For every file, quote the most vulnerable phrase and state what its exact words establish. If the reviewer must produce a charitable paraphrase that adds a fact or motivation, record a blocker. Record the result in `_work/assessment-reviews/context-language-review.md` and classify every finding by severity.

## Finding severity

A `BLOCKER` is a defect that makes an item invalid or materially misleading: unsupported source or context, an incorrect or non-unique answer, invented situational facts, missing facts needed to answer, an unusable practice, material ambiguity, or an explanation that cannot justify the keyed answer. An `ADVISORY` is a non-material wording or polish suggestion that does not change validity, understanding, or learner action.

Only blockers fail a review or authorise repair. Use `Decision: PASS` when `## Blockers` contains exactly `None.` or `None`; advisories may remain with PASS.

## Independence and invalidation

The writer and the two reviewers must be different, and the reviewers must be different from each other. Reviewers may not edit files during their first pass.

After a repair:

- any learner-facing assessment change invalidates both reviews;
- a plan-only change invalidates the source-aware review;
- an application-context change invalidates both reviews and every contextual plan entry.

Rerun affected reviews on the complete current artefacts within the bounded process below. A PASS attached to an earlier digest is stale.

## Bounded review and repair

1. Run up to three fresh concurrent paired review rounds on the complete current assessment bundle without prior findings.
2. After a failed round, the writer makes one consolidated, substantive repair of all blockers before the next round; do not repair advisories or use piecemeal micro-iterations.
3. If either reviewer reports a blocker in round 3, stop with the assessment incomplete.
4. Obey the skill's 60-minute total invocation budget. At the limit, stop incomplete rather than weakening a gate or continuing review.

## Deterministic validation

Run `scripts/validate_output.py` in the selected assessment mode after both semantic reviews. The validator checks only reliable mechanical invariants: required files, routes and component shapes, exact context excerpts, question and answer syntax, plan/answer agreement, reviewer independence, approved links, and fresh bundle digests.

Before finalising review records, run `scripts/validate_assessment.py books/<book-slug> --print-bundle-digest` and record that digest in both reviews. Record the ordinary SHA-256 digest of `_work/assessment-plan.md` in the source-aware review.

It does not judge behavioural credibility, source fidelity, plain language, usefulness, distractor quality, or whether an answer is truly correct. It must not contain phrase blacklists or semantic-writing gates. Warnings about option length or answer-position concentration are prompts for human/model review, not proof of failure.

When changing this subsystem, run `scripts/test_validate_assessment.py` and conduct independent forward tests using realistic complete outputs. Test outcomes and meaningful invariants, not exact generated wording.

## Release

Do not describe an assessment as reviewed or complete until both semantic reviews contain no blockers and deterministic validation passes on the same learner-facing assessment bundle within the three-round cap. State assessment evidence modestly: retrieval, constrained judgement, and guided practice do not establish mastery or durable transfer.
