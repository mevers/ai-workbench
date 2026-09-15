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
blink_skill_version: "<current SKILL.md metadata.version>"
```

## overview.md in all mode

```markdown
# <Book title>

By <Author>

Estimated reading time: <N> minutes

Summary generated with Blink skill version: <same value as metadata.yaml>

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

## Assessment template index

Read `references/assessment-workflow.md` and `references/assessment-review.md` before using these schemas.

- Contextual `FULL`: Quick recall, Apply, Try this, and related ideas.
- Contextual `RECAP_ONLY`: Quick recall, Deeper comprehension, and related ideas.
- Generic: Quick recall and Deeper comprehension only.
- Internal records: one assessment plan and two independent review records.

## Knowledge-question syntax

Use this syntax for Quick recall, Apply, Deeper comprehension, and review questions:

```md
<Question that makes sense without reading the options>

<Select one answer. OR Select all that apply.>

**A.** <Option>

**B.** <Option>

**C.** <Option>

**D.** <Option>

<details>
<summary>Answer</summary>

Correct answer: **<letter>**

<Plain explanation of the relevant book concept and why the options differ. For multi-select, use `Correct answers: **<letters>**` and explain A-D separately.>

</details>
```

## Contextual assessment: FULL

```md
# Key idea N: Recall and apply

[← Back to key idea](../key-idea-NN.md)

Commit to each answer before expanding its answer block.

## Quick recall

<Book-only question using the knowledge-question syntax>

## Apply

<Context-grounded question using the knowledge-question syntax>

## Try this in your <domain> environment

**When:** <Recognisable trigger consistent with the application context>

**Do:** <One practical task; related questions or steps may serve it>

**Why now:** <Useful result in the current situation>

## Related ideas and further reading

### In other Blinks

- *<Source book title>*: [<Related key idea title>](<direct link>). <Specific connection>

### Research and practice

- [<Source title>](<approved direct URL>): <specific connection>
```

## Contextual assessment: RECAP_ONLY

Use the same question syntax as `FULL`.

```md
# Key idea N: Recall and deepen

[← Back to key idea](../key-idea-NN.md)

Commit to each answer before expanding its answer block.

## Quick recall

<Book-only retrieval question and collapsed answer>

## Deeper comprehension

<Different source-grounded question and collapsed answer>

## Related ideas and further reading

<Context-approved links only; do not imply contextual practice occurred.>
```

## End-of-book review

```md
# End-of-book review

Review the book's ideas in new questions.

Commit to each answer before expanding its answer block.

## Question 1

<New contextual or source-grounded recap question using the knowledge-question syntax>

<Repeat for the required number of questions.>

## Related ideas and further reading

<Context-approved links and clear connections; omit in generic mode.>

[← Back to overview](overview.md)
```

## Generic assessment and review

Use the `RECAP_ONLY` learner-facing structure without related-ideas sections or domain language. Every quiz contains Quick recall and Deeper comprehension. The mixed review contains new source-grounded recap questions and ends with `[← Back to overview](overview.md)`.

## Assessment plan

Use format 2 for new assessments. Retain older plans when their assessments are outside the task scope.

```md
# Assessment plan

**Assessment format:** 2
**Assessment mode:** <CONTEXTUAL | GENERIC>
**Context path:** <confirmed path or None.>
**Context SHA-256:** <digest or None.>

## Key idea 1

**Route:** <FULL | RECAP_ONLY>
**Route reason:** <why this idea supports useful application, or why recap is better>

### Quick recall

**Learning target:** <one distinction or mechanism>
**Source anchor:** <chapter and section>
**Context basis:** None.
**Scenario facts:** None.
**Answer mode:** <ONE_BEST | SELECT_ALL>
**Correct answers:** <letter or comma-separated letters, after drafting>
**Reasoning:** <correct reasoning and the tempting misconception; brief A-D rationales for select-all>

### Apply

<For FULL, repeat the question fields. Context basis names the relevant context section and constraint. Scenario facts lists the added hypothetical facts, or None. when no additions are needed.>

### Try this

**Learning target:** <mechanism practised>
**Source anchor:** <chapter and section>
**Context basis:** <context section and relevant ordinary situation>
**Scenario facts:** <added hypothetical facts or None.>
**Action and use:** <one practical task and the decision or next step it enables>

<For RECAP_ONLY, replace Apply and Try this with Deeper comprehension using the question fields and None. for both context fields.>

## Review question 1

<Repeat the question fields; use None. for both context fields when book-only.>

Plan status: FROZEN
```

## Review records

Use `_work/assessment-reviews/source-aware-review.md` and `context-language-review.md`. Each reviewer writes their own record. Include every assessed quiz and review.md under File decisions; a scoped pilot includes only its tested files.

```md
# <Source-aware assessment review | Context, language, and practice review>

**Reviewer ID:** <actual reviewer identity>
**Writer and reviewer are different:** yes
**Review wave:** <1 | 2 | 3>
**Assessment bundle SHA-256:** <digest>
```

The source review also records `**Plan SHA-256:** <digest>`.

The learner review also records:

```md
**Context SHA-256:** <digest or None.>
**Answers and explanations withheld until first pass saved:** yes

## First pass

<Save before viewing complete learner files. For each question record the task, chosen answer or ambiguity, and evidence of content reasoning or answer cues. Assess each practice's situation and usefulness.>

## Feedback check

<After the first pass is saved, inspect explanations for accuracy of comparison, missing facts and unnecessary commentary.>
```

Both records finish with:

```md
## File decisions

### quizzes/key-idea-NN-comprehension.md

<Quote any defect and explain its effect. Give the verdict and evidence for source/answer validity or learner usability, according to the reviewer role.>

## Blockers

<Findings, or exactly None.>

## Advisories

<Optional polish, or None.>

## Gate decision

Decision: <PASS | FAIL>
```
