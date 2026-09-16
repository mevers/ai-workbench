# Assessment review and release

## Independent reviews

Use two reviewers different from the writer and each other, with no conversation fork. They review concurrently and do not edit learner files. Give both the user’s requirements and supplied examples of useful or unhelpful language. Withhold writer rationale, earlier model reviews, repair history, expected verdicts on the current draft and the other review. Independence must not withhold the user’s standards.

### Source reviewer

Supply the key ideas, bounded source excerpts, plan, context and final assessment. Check each target and answer against its source. Check that the situation actually supports the requested judgement, the strongest distractor is wrong for the stated reason, and practice exercises the relevant mechanism. Distinguish a first diagnostic question from evidence that a diagnosis is established. Direct recall is valid when it retrieves a central idea.

### Learner reviewer

First supply the user’s brief, context and learner files with **entire answer blocks removed**, including explanations. Do not supply source notes, plans or keys. Use `scripts/validate_assessment.py --blind-file <quiz>` to produce each blinded copy.

Before seeing feedback, record for each question: the intended task, the selected answer or ambiguity, and what drove that choice. Check whether the stem gives away the reasoning or one option stands out through scope, wording or polish. Correct selection alone is not a pass. For Apply, identify details that can be removed without changing the judgement. For practice, identify the people, work and problem from the printed exercise. Fail if you must invent details to make the situation specific or relatable. Then check whether the actions clearly apply the book’s insight. Judge whether the intended reader could use the exact wording in an ordinary conversation. Shortness, grammatical clarity and a single question do not establish usefulness. Related questions may form one practical task; reject disconnected exercises or a generic prompt that leaves the reader to invent the useful conversation.

Save this first pass in the review record. Only then provide the complete learner files for a feedback check. Preserve the first-pass findings and add any issues in the explanations. Do not silently reinterpret a confusing item after seeing its answer.

## Decisions and repair

A `BLOCKER` includes incorrect or ambiguous answers, unsupported reasoning, implausible situations, missing facts, material first-read difficulty, answer cues, a stem that gives away its answer, or a practice with no usable task, unnatural dialogue or disconnected exercises. These fail even when the keyed answer is factually defensible. Quote the passage and explain the defect without mentally rewriting it.

An `ADVISORY` is optional polish that does not affect understanding, usability or the value of the question. The writer may address advisories in the same consolidated repair as blockers; they do not require their own review loop. Replace or drop weak items instead of adding clauses to defend them.

Run at most three paired rounds, using fresh reviewers after repairs. Review the complete current assessment scope each time. Stop incomplete if blockers remain in round three or the skill's 60-minute invocation budget expires. If separate reviewers are unavailable, report the missing review and leave the output incomplete.

Each reviewer authors the record in the output template. Use PASS only with `None.` under Blockers. Any learner edit invalidates both reviews; plan edits invalidate source review; context edits invalidate both. Keep the source reviewer bound to the plan digest and both reviewers bound to the assessment bundle digest. A pilot records only its tested scope.

## Validation and release

After semantic PASS, run `scripts/validate_output.py` in the selected mode. Before finalising review records, use `scripts/validate_assessment.py <book> --print-bundle-digest` and record the plan's SHA-256 in the source review. The validator checks schemas, keys, context provenance, links, declared reviewer separation and digest freshness. It cannot establish practical realism, source fidelity, review independence in fact or assessment quality. Length warnings prompt inspection; they are not quality scores.

For format 2, the learner record must preserve `## First pass` and `## Feedback check`, and confirm that answers and explanations were withheld until the first pass was saved. Older assessment records retain their original structural contract; passing their validation does not certify them under this workflow.

When changing this subsystem, run `scripts/test_validate_assessment.py`. Also test behaviour independently on known failures and fresh generated items. Give test authors the skill and minimum source/context inputs, not the desired wording or prior diagnosis. For a redesign, include held-out books with different mechanisms and assessment modes. Known examples calibrate the standard; recognising them is not independent proof. Judge whether fresh tasks are clear, credible and meaningful; do not turn wording preferences into exact-match tests.

Release only with both semantic PASS records and structural validation for the final files. Report a scoped pilot as a pilot, never as a repaired full assessment. A user rejection remains a failed result even when model reviewers pass; preserve that evidence and reassess the design.
