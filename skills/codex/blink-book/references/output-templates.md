# Output templates

Use these structures for final learner-facing files. Keep placeholders out of final output.

## metadata.yaml

```yaml
title: "<Book title>"
author: "<Author>"
book_slug: "<book-slug>"
source_type: "pdf|epub|web|internal|user-provided"
extraction_quality: "high|medium|low|not-applicable"
visual_access_status: "complete|partial|none|not-applicable"
limitations:
  - "<Any source, extraction, OCR, or visual limitation. Use [] if none.>"
key_idea_count: <source-derived count>
estimated_reading_minutes: 42
generated_date: "YYYY-MM-DD"
language: "English"
```

## overview.md in all mode

```markdown
# <Book title>

By <Author>

Estimated reading time: <N> minutes

## Big picture

<Brief orientation in 2-4 short paragraphs. Explain what the book is trying to change in the reader's thinking.>

## Key ideas

1. [<Key idea title>](key-idea-01.md)
2. [<Key idea title>](key-idea-02.md)

## Visuals

Original source visuals are stored in [visuals/](visuals/). Only include visuals that appear in the source.

## Quiz index

- [Key Idea 1 comprehension](quizzes/key-idea-01-comprehension.md)
- [Key Idea 2 comprehension](quizzes/key-idea-02-comprehension.md)

## Review

- [End-of-book review](review.md)
```

## overview.md in blink-only mode

Use the same heading, byline, reading-time, Big picture, Key ideas, and Visuals sections as the all-mode overview. Omit `## Quiz index` and `## Review`. Do not create assessment files or links.

## key-idea-NN.md in all mode

```markdown
# Key idea N of M

## <Crisp sentence-style key idea title>

<Short opener. For Key Idea 1, this can be a "What's in it for me?" style orientation. For later ideas, explain why this matters in 2-3 sentences.>

<Mobile-friendly summary. Use short paragraphs, bullets, and tables when they compress distinctions or tradeoffs. Avoid wall-of-text blocks.>

![<Source caption or concise description>](visuals/<filename>.png)

<Continue explanation only if the visual is directly relevant. Do not include visuals decoratively.>

## Remember this

<!-- Use bullet points. Vary their number and length according to the key idea; include only what the reader should retain after the details fade. -->

- <A concise retention takeaway.>

## Check understanding

[Take the comprehension check](quizzes/key-idea-NN-comprehension.md)

## Source basis

Grounded in <part/chapter/section/figure/table/source anchor>. Page numbers only if unavoidable.

---

[Back to overview](overview.md) | Previous: [Key idea N-1](key-idea-NN.md) | Next: [Key idea N+1](key-idea-NN.md)
```

For the first key idea, omit `Previous`. For the final key idea, use `Next: [End-of-book review](review.md)` in place of the next key-idea link. Keep the `overview.md` backlink in every key-idea file.

## key-idea-NN.md in blink-only mode

Use the all-mode key-idea template but omit `## Check understanding` and its link. For the final key idea, omit `Next` rather than linking to a review. Do not change key-idea files in assessment mode.

## `_work/key-idea-drafts/key-idea-NN-first-reader-review.md`

This is a working-quality artefact, not learner-facing text. An independent reviewer receives only the final `key-idea-NN.md` file. They must not see the book, source extracts, outline, argument pack, or fuller draft.

```markdown
# Source-blind first-reader review: Key idea N

## Review conditions

**Reviewer:** <human name or separate agent/model>

**Writer and reviewer are different:** yes

The reviewer was source-blind and reviewed the final learner-facing key-idea file only.

## Reader reconstruction

**Central conclusion:** <What the reader understood the takeaway to be.>

**Key mechanism:** <How the reader understood the claim to work.>

**Action or implication:** <What the reader understood they should do or notice.>

**Unresolved confusion:** <none, or the precise unresolved question.>

## Unfamiliar names and case examples

### <Name of case, person, place, event, or organisation>

**What is it:** <Identity and setting needed to understand the reference.>

**What happens:** <Relevant decision, event, and outcome.>

**Why it matters here:** <How it supports this key idea.>

**Final-prose evidence:** <Exact final prose that supplies the needed context.>

**Verdict:** PASS

## Terms and labels

**Source-defined terms retained:** <Named book terms, their plain in-line explanation, and why they are needed.>

**Non-source labels removed or rewritten:** <What was changed, or none.>

## Gate decision

Decision: PASS
```

Do not use `PASS` when the reviewer had to rely on prior knowledge, a visual, or source material to fill a gap. A source-defined technical term may remain when it carries the book’s model and is explained in-line. The gate targets unexplained references and blink-invented shorthand, not useful domain vocabulary.

## Contextual assessment

For every multiple-choice item, choose one option family and write four parallel options before marking the correct answer. Keep their grammar and informational load comparable; do not make the correct option the only complete plan or qualified statement. Ensure exactly one option satisfies the tested principle; distractors must not paraphrase the correct answer.

```markdown
# Key idea N: Recall and apply

Commit to each answer before expanding its answer block.

## Quick recall

<One four-option multiple-choice item that checks the central distinction, mechanism, or principle.>

**A.** <Option>

**B.** <Option>

**C.** <Option>

**D.** <Option>

<details>
<summary>Answer</summary>

Correct: **<Letter>**

<Brief explanation tied to the source idea.>

</details>

## Apply

<A novel four-option scenario in the configured application context. Test a decision, diagnosis, or tradeoff, not a restated definition. Make every option a comparable manager move, diagnosis, prioritisation choice, or interpretation.>

**A.** <Option>

**B.** <Option>

**C.** <Option>

**D.** <Option>

<details>
<summary>Answer</summary>

Best answer: **<Letter>**

<A short coaching explanation: the decisive contextual clue, why the answer fits, and the most instructive tempting alternative(s).>

</details>

## Try this in your <domain> environment

<Give all compatible actions the learner should take. Do not present alternatives from which they must choose.>

**Outcome:** <The management result these actions intend to create.>

**Start:** <The next appropriate work touchpoint.>

- <Concrete, compatible action.>
- <Concrete, compatible action.>
- <Concrete, compatible action when useful.>

**Review:** <Where and when to inspect what happened.>

## References and evidence basis

- **Quick recall:** <Book chapter, section, figure, table, or page range.>
- **Apply:** <Book chapter, section, figure, table, or page range>; <Registered context-source ID, relevant section>. <Verification note.>
- **Try this:** <Book chapter, section, figure, table, or page range>; <Registered context-source ID, relevant section>. <Verification note.>

[Back to Key Idea N](../key-idea-NN.md)
```

## Contextual review

```markdown
# End-of-book review

Estimated time: <N> minutes

## Question 1

<A new four-option, applied case that draws on two or three key ideas. Do not repeat a section question.>

**A.** <Option>

**B.** <Option>

**C.** <Option>

**D.** <Option>

<details>
<summary>Answer</summary>

Correct: **<Letter>**

<Natural coaching explanation that identifies the relevant book ideas and the contextual clue.>

</details>

...

## References and evidence basis

- **Question 1:** <Book chapters, sections, figures, tables, or page ranges>; <Registered context-source ID, relevant section>. <Verification note.>
```

## Generic assessment

For every multiple-choice item, choose one option family and write four parallel options before marking the correct answer. Keep their grammar and informational load comparable; do not make the correct option the only complete or qualified statement. Ensure exactly one option satisfies the tested principle; distractors must not paraphrase the correct answer.

```markdown
# Key idea N: Recall and deepen

Commit to each answer before expanding its answer block.

## Quick recall

<One four-option multiple-choice question that checks the central distinction, mechanism, or principle from the book.>

**A.** <Option>

**B.** <Option>

**C.** <Option>

**D.** <Option>

<details>
<summary>Answer</summary>

Correct: **<Letter>**

<Brief explanation tied to the book source.>

</details>

## Deeper comprehension

<A second, distinct four-option book-recap question. Test a mechanism, distinction, implication, or trade-off from the book without introducing an application context.>

**A.** <Option>

**B.** <Option>

**C.** <Option>

**D.** <Option>

<details>
<summary>Answer</summary>

Correct: **<Letter>**

<Brief explanation tied to the book source.>

</details>

[Back to key idea N](../key-idea-NN.md)
```

## Generic review

```markdown
# End-of-book review

Estimated time: <N> minutes

## Question 1

<A new, mixed four-option book-recap question. Do not repeat a section question or introduce an application context. Use five questions for books with five to seven ideas, six for books with eight or more, and one per idea for shorter books.>

**A.** <Option>

**B.** <Option>

**C.** <Option>

**D.** <Option>

<details>
<summary>Answer</summary>

Correct: **<Letter>**

<Brief explanation tied to the relevant book ideas.>

</details>
```
