# Output Templates

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
key_idea_count: 8
estimated_reading_minutes: 42
generated_date: "YYYY-MM-DD"
language: "English"
```

## overview.md

```markdown
# <Book Title>

By <Author>

Estimated reading time: <N> minutes

## Big Picture

<Brief orientation in 2-4 short paragraphs. Explain what the book is trying to change in the reader's thinking.>

## Key Ideas

1. [<Key idea title>](key-idea-01.md)
2. [<Key idea title>](key-idea-02.md)

## Visuals

Original source visuals are stored in [visuals/](visuals/). Only include visuals that appear in the source.

## Quiz Index

- [Key Idea 1 comprehension](quizzes/key-idea-01-comprehension.md)
- [Key Idea 2 comprehension](quizzes/key-idea-02-comprehension.md)

## Review

- [End-of-book review](review.md)
```

## key-idea-NN.md

```markdown
# Key Idea N of M

## <Crisp sentence-style key idea title>

<Short opener. For Key Idea 1, this can be a "What's in it for me?" style orientation. For later ideas, explain why this matters in 2-3 sentences.>

<Mobile-friendly summary. Use short paragraphs, bullets, and tables when they compress distinctions or tradeoffs. Avoid wall-of-text blocks.>

![<Source caption or concise description>](visuals/<filename>.png)

<Continue explanation only if the visual is directly relevant. Do not include visuals decoratively.>

## Mechanism

<Optional. Use only when it clarifies cause/effect, constraints, tradeoffs, or a repeatable pattern.>

## Remember This

- <One compressed takeaway.>
- <Another compressed takeaway.>

## Check Understanding

[Take the comprehension check](quizzes/key-idea-NN-comprehension.md)

## Source Basis

Grounded in <part/chapter/section/figure/table/source anchor>. Page numbers only if unavoidable.

---

Previous: [Key Idea N-1](key-idea-NN.md) | Next: [Key Idea N+1](key-idea-NN.md)
```

For the first key idea, omit `Previous`. For the last key idea, omit `Next`.

## comprehension quiz

```markdown
# Key Idea N Comprehension Check

## Question

<One multiple-choice question that checks comprehension of the key idea.>

A. <Option>
B. <Option>
C. <Option>
D. <Option>

<details>
<summary>Answer</summary>

Correct: <Letter>

<Brief explanation tied to the source idea.>

</details>

[Back to Key Idea N](../key-idea-NN.md)
```

## going-beyond quiz

```markdown
# Key Idea N Going Beyond

## Question

<One optional application or transfer question. Use only when useful.>

A. <Option>
B. <Option>
C. <Option>
D. <Option>

<details>
<summary>Answer</summary>

Best answer: <Letter>

<Brief explanation. Mark this as application beyond the source, not direct source recall.>

</details>

[Back to Key Idea N](../key-idea-NN.md)
```

## review.md

```markdown
# End-of-Book Review

Estimated time: <N> minutes

## Question 1

<Repeat comprehension question from Key Idea 1.>

A. <Option>
B. <Option>
C. <Option>
D. <Option>

<details>
<summary>Answer</summary>

Correct: <Letter>

<Brief explanation.>

</details>

...
```
