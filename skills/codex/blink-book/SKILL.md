---
name: blink-book
description: Create Blinkist-style learning curricula from one nonfiction book or book-like resource, especially when the user provides a book title, PDF, EPUB, or asks for a mobile-friendly key-ideas summary with quizzes. Use when Codex must verify familiarity/access to the source, process book content and original visuals without loading the whole book into context, produce section-based Markdown under a per-book folder, extract source visuals as PNGs, and create comprehension checks.
---

# Blink Book

## Purpose

Turn one nonfiction book into a mobile-friendly learning curriculum modeled on Blinkist: a source-derived set of transferable key ideas, crisp accessible prose, original visuals only, one short comprehension check per key idea, and a final review. Write in English.

Use a book-centered output folder:

```text
books/<book-slug>/
  metadata.yaml
  overview.md
  key-idea-01.md
  key-idea-02.md
  ...
  review.md
  quizzes/
    key-idea-01-comprehension.md
    key-idea-01-going-beyond.md
  visuals/
    chapter-02-fig-01.png
  _work/
    access-assessment.md
    source-map.md
    source-index.md
    extraction-log.md
    source-structure.md
    source-evidence.md
    key-idea-plan.md
    idea-argument-packs/
    key-idea-drafts/
    final-audit.md
    chapter-notes/
```

## Source Access Rule

Require one specific book as input. If the user gives only a title, assess access top to bottom:

1. Use internal knowledge only if you know the book well and have reliable access to its content plus original visual aids.
2. Otherwise, search for a complete accessible source with text plus original visual aids.
3. Otherwise, ask the user to provide a link, PDF, EPUB, scan, or other complete copy.

Always give a short access sentence before proceeding:

```text
I am familiar with <book> at <low/medium/high> level, and I <do/do not> have verified access to its complete text and original visuals; <next step>.
```

"Access to content" means text plus original visual aids. If you know the text but not the visuals, ask for a source copy before producing the curriculum. Once the user provides a source file, treat that file as source of truth and do not rely on memory for substantive claims.

Do not invent visuals, diagrams, schematics, figures, charts, or pictures. Use only visuals copied or extracted from the source. Tables created in Markdown are allowed as textual compression, but not as new conceptual diagrams.

## Context-Safe Workflow

Never load an entire book into context. Work in bounded passes and write intermediate files in `_work/`.

1. Create `books/<book-slug>/` and subfolders.
2. Create `_work/access-assessment.md` documenting access level, source type, visual access status, extraction quality, and limitations.
3. For PDF/EPUB, run `scripts/source_map.py` to inspect structure and extract bounded text chunks.
4. Run `scripts/extract_visuals.py` to export original visuals as PNGs into `visuals/`.
5. Run `scripts/build_source_index.py books/<book-slug>` after source mapping. Use the index, table of contents, introduction, conclusion, headings, chapter openings/endings, and figure captions as the deterministic discovery baseline.
6. Create `_work/source-structure.md` before choosing key ideas. Inventory the book's core thesis, named models and pillars, named mechanisms or practices, recurring arguments, material limits or tradeoffs, and important case evidence. Give each item a source anchor and classify it as `core`, `supporting`, or `context`. Mark source terms that must appear verbatim in learner-facing files.
7. Create `_work/source-evidence.md` from bounded source reading. For every `core` or `supporting` inventory item, record its ID, the source claim or distinction, a concise source-grounded note or example, and exact source anchors. Do not draft learner-facing text from the inventory alone.
8. Synthesize the strongest teachable ideas from the source. Derive the number of key ideas from the book's arguments, named models, major practices, and important distinctions; do not start from a target count.
9. Before drafting learner-facing files, create `_work/key-idea-plan.md` from the source-structure inventory and evidence notes. Give every `core` or `supporting` item one treatment: `standalone`, `merged`, or `omitted`. For a merge, name the exact key idea and the item’s contribution. For an omission, give a reason. Do not use a broad part, chapter, or category as a treatment. Record each proposed idea’s central conclusion, evidence-note IDs, explanatory route, required source terms, and source examples to use or omit. Record the source-derived key-idea count and rationale. This is a selection and coverage map, not a paragraph checklist: do not force every mapped item into learner-facing prose.
10. Draft the Big Picture from the same source-structure and evidence work. Keep the Big-Picture Writing and Big-Picture Validation rules below unchanged. It has its own synthesis job; do not construct it by mechanically shortening the key ideas.
11. For each key idea, reread its linked source chunks and create `_work/idea-argument-packs/key-idea-NN.md`. Assemble enough source material to support a full explanation: the conclusion, the problem or tension it addresses, the causal explanation, essential conditions or limits, concrete source detail, and the transferable implication. Include a plain-language argument chain that states the source fact, the mechanism, the concept, and the transferable conclusion. Do not write learner-facing prose until this chain explains how the source detail supports the conclusion. An argument pack is not a concise evidence summary and is not learner-facing prose.
12. Design the reader’s path for each idea before drafting. First decide the transferable conclusion and central model or distinction the reader must understand. Then select only the source detail needed to explain and support that argument. Choose the sequence that best serves it, and decide where prose, a short list, a comparison, or a sequence will improve reading. Do not use a fixed section template.
13. Write a deliberately fuller first draft from the argument pack in `_work/key-idea-drafts/`. Then tighten it into the learner-facing section by removing repetition, generic extrapolation, and source detail that does not advance the explanation; restructure when it improves scanning. Before finalising, run a literal-language pass: for every sentence, ask whether a reader can identify what it refers to, what happens, and why it matters in this argument. Rewrite from the argument chain or remove any sentence that fails. Do not add post-hoc padding to meet a reading-time estimate. If tightening reveals a thin idea, return to the argument pack and source chunks, then rebuild the explanation.
14. Draft the quiz only after its learner-facing key idea is final. Run `scripts/validate_source_work.py books/<book-slug>` before drafting and again before final delivery. Run word-count and link/visual validation scripts before final delivery.

For PDFs, inspect extraction quality before synthesis. If text order, OCR, or visual extraction is unreliable, report the limitation and ask for a better source when the problem prevents faithful output.

## Writing Model

Match the Blinkist model:

- Surface the book's most valuable and memorable transferable insights.
- Create a clear structure that brings those ideas to light.
- Use a source-derived number of numbered key ideas, not chapter summaries. A key idea must express one coherent takeaway or insight. It may span multiple chapters, and one chapter may contribute to several key ideas. Use chapters as source anchors and evidence, never as the default unit of synthesis.
- Follow the Blinkist approach: key ideas are the big transferable takeaways, not book-specific stories, scenes, or examples. Use anecdotes only as brief support for the broader idea.
- Give every key idea a title that states a transferable lesson. Do not title a key idea after an anecdote, chapter event, place, person, object, or phrase from the book unless the book is specifically about that case.
- Keep book-specific examples short. Default to at most one brief example per key idea, and include it only when it clarifies the transferable idea.
- Include an overview landing file with title, author, total estimated reading time, key-idea table of contents, visual inventory link, quiz index, and review link.
- Put the real title inside each file, not in the filename. Use stable filenames: `key-idea-01.md`, `key-idea-02.md`, etc.
- Include a backlink to `overview.md` and previous/next navigation at the bottom of each key-idea file.
- Add a section-level `Source basis` note at the bottom of each key idea. Prefer stable anchors such as part, chapter, section heading, named figure/table, or EPUB anchor. Use PDF page numbers only when unavoidable.

## Source Terminology Integrity

Preserve the author's named model terms. Plain paraphrase is useful for explaining a term, but it must not replace the term when the term is part of the book's core structure.

- Use the source-structure inventory as the terminology baseline. Include the book's named models, pillars, stages, frameworks, rules, and terms the author explicitly defines.
- Treat terms from the title, subtitle, table of contents, introduction, conclusion, glossary, index, diagrams, and summary chapters as candidates for preservation.
- Distinguish between the author's named structure and nearby supporting ideas. For example, if a book says the model has three named parts, those exact terms must appear; nearby ideas can be explained in their own place but must not be promoted into the author's model.
- In the overview, name the book's central model terms verbatim before paraphrasing them in plain language.
- In key ideas, use the source term when the section teaches that concept, then define it in-line with plain wording.
- Do not swap a source term for a broader synonym when that would hide the author's structure. For example, do not replace a named pillar with a paraphrase like `skill` unless the source term also appears nearby.
- Do not invent a neat triad, framework, or label from adjacent concepts. If the source does not name it that way, present it as an interpretation, not as the author's model.
- Keep learner-facing prose source-pure. Do not mention user feedback, prior drafts, or the drafting process.

## Writing Key Ideas

- Write for a smart expert entering a new domain. Be clear, precise, and accessible without simplifying the book’s argument.
- Build each key idea as one connected explanation. Establish the conclusion, use source detail to explain it, and show why it matters. Choose the order that best serves the argument.
- Make relationships explicit. Name who did what, what changed, and why it mattered when the source describes a sequence, contrast, cause, decision, or outcome. Do not make the reader infer the connection between paragraphs.
- Start with the source’s concrete claims, actions, distinctions, and examples. Generalise only after the reader can see the point. Do not replace source detail with generic workplace language or an abstract diagnosis.
- Write sentences for clarity of relationship, not for artificial brevity. Keep a claim, reason, contrast, or example together when that makes the thought easier to follow. Split a sentence only when doing so makes its meaning clearer.
- Give each paragraph a clear job in the explanation and a visible connection to what comes before. Use short paragraphs and lists when they improve scanning; do not turn a sequence of related thoughts into disjoint fragments.
- Use plain, literal language. Prefer active verbs and common words when they preserve meaning. Avoid filler, buzzwords, vague abstractions, and labels that merely announce the point.
- Preserve named source terms and define critical domain terms briefly at first use. Each key idea must use source-specific evidence that genuinely carries its explanation.
- When an idea teaches the book’s core model, define its central terms plainly and explain their relationship. Do not introduce central concepts merely as labels.
- Use headings only when they form a clear, parallel sequence in the transferable argument. Omit them when they would merely divide the text or narrate a case study.
- Use a table when it makes a transferable distinction, comparison, or relationship easier to grasp. Let source examples support the table’s argument; do not make a case study the table’s main structure.
- Begin with a full source-grounded draft, then tighten for reading ease. Do not begin with a compressed version and expand it afterward to reach a length expectation.
- Do not use em dashes in learner-facing files unless reproducing a source quotation verbatim.
- Use `Remember This` as a bullet-point retention recap. Include the central conclusion and any condition or distinction needed to keep it accurate; do not introduce new material.

## Key-Idea Validation

Do not use a generic pass/fail checklist. For each final key idea, create `_work/key-idea-drafts/key-idea-NN-clarity-review.md` containing:

- the central conclusion in one plain sentence;
- the source mechanism that explains or proves it;
- the source example used, if any, and its supporting role;
- the sentence most likely to confuse a first-time reader, followed by its revision or deletion.

Then apply the literal-language pass to every sentence. A final key idea fails validation when a reader cannot identify what a sentence refers to, what happens, and why it matters to the argument; when a central named term is introduced but not explained; or when the source example rather than the transferable argument determines the structure. Return to the argument chain and revise before delivery.

## Big-Picture Writing

For the Big Picture in `overview.md`:

1. **Focus on the book’s transferable ideas.** Tell the reader what the book teaches. Use specific settings and scenarios to establish the stakes or clarify the argument.
2. **Preserve and plainly explain the book’s central models, pillars, and frameworks when they are present.** Key concepts are more important than specific story details.
3. **Use the right level of abstraction.** Make models, pillars, and frameworks concrete. Do not invent vague labels.
4. **Use case studies and examples as evidence, not the main story.**

## Big-Picture Validation

Before delivery, assess `overview.md` against all five checks:

1. **Premise:** Does it identify the real problem, question, or subject of the book, rather than a downstream symptom?
2. **Argument:** Does it state the book’s main transferable idea and any central named model, pillar, or framework?
3. **Selection:** Do settings, examples, and outcomes clarify the argument rather than become the story?
4. **Fidelity:** Are the central claims supported by relevant source passages, without invented labels, causal claims, or evaluations?
5. **Clarity:** Can a smart reader understand the overview in one read, including why the book matters?

## Length And Quizzes

Keep learner-facing summary reading time under 45 minutes. Estimate summary text only, excluding quizzes and review, at 135 words per minute. Record the calculated estimate, rounded to the nearest whole minute, in `metadata.yaml` and `overview.md`; do not add a separate estimate for the full learning experience.

Never ask the user to choose a duration. Estimate the appropriate length from the source-derived number of core ideas. Use roughly five minutes per key idea as an editorial calibration: draft each idea fully first, then tighten it toward a readable form with enough explanation and useful detail. Three to eight minutes per idea is normal, depending on the material. This is a guide, not a target or a reason to change the source-derived idea count. Investigate a material departure from it rather than treating shortness as success. If a final idea is thin, return to its argument pack and source passages; do not pad the existing draft. Allocate space according to the source: a key idea may need an explanation of the claim, why it works, its limits or tradeoffs, and a source-supported example or practice. Do not reduce an idea to a headline, one named term, and an application merely to be concise.

If a new version is materially shorter than an existing trusted version, explain the reduction in `_work/final-audit.md` and treat it as a likely regression unless source coverage has demonstrably improved.

Create at most one comprehension question per key idea. Put it in a separate quiz file with the answer hidden in a collapsible `<details>` block. Render every multiple-choice option as a lettered choice (`A.` through `D.`), with a blank line between choices. Bold the letter label only, not the option text. Bold the correct answer letter in the answer block. Do not use bullet points for quiz options. Create optional going-beyond quiz files only when useful, and keep them separate from comprehension checks.

Create `review.md` by default. Repeat all comprehension questions directly in sequence with collapsed answers.

## Files To Read When Needed

- Read `references/output-templates.md` before writing final learner-facing files.
- Use `scripts/requirements.txt` for helper-script dependencies.
- Use `scripts/source_map.py` for EPUB/PDF source maps and bounded text extraction.
- Use `scripts/build_source_index.py` to generate the deterministic source-discovery index after source mapping.
- Use `scripts/validate_source_work.py` to verify that every core or supporting source item has both evidence and a key-idea-plan treatment.
- Use `scripts/extract_visuals.py` for original visual extraction and PNG conversion.
- Use `scripts/count_reading_time.py` before final delivery.
- Use `scripts/validate_output.py` before final delivery.

## Final QA

Before responding to the user:

1. Verify `metadata.yaml`, `overview.md`, `review.md`, `quizzes/`, `visuals/`, and `_work/` exist as applicable. Verify `_work/source-index.md`, `_work/source-structure.md`, `_work/source-evidence.md`, `_work/key-idea-plan.md`, and the per-idea argument packs before synthesis.
2. Run `scripts/count_reading_time.py books/<book-slug> --limit-minutes 45 --wpm 135`. Fail if the learner-facing summary exceeds 45 minutes. Do not treat a shorter result as a success without checking the source-coverage map.
3. Run `scripts/validate_output.py books/<book-slug>` and fix missing links, missing quiz files, missing previous/next navigation, and missing visual files.
4. Run `scripts/validate_source_work.py books/<book-slug>` and fix missing evidence notes or plan treatments.
5. Run Key-Idea Validation and retain the per-idea clarity review in `_work/key-idea-drafts/`. Record completion in `_work/final-audit.md`. Confirm that each learner-facing key idea was tightened from its long draft rather than expanded after a short first pass.
6. Run Big-Picture Validation and record the result in `_work/final-audit.md`.
7. Add a source-terminology audit to `_work/final-audit.md`: list every required term from `_work/source-structure.md`, where it appears in learner-facing files, and whether it is defined in-line. Fix missing or mislabeled source terms before delivery.
8. Run a source-purity audit over learner-facing files.
9. Run a source-coverage audit against `_work/source-structure.md` and `_work/source-evidence.md`, not only `_work/key-idea-plan.md`. For every `core` or `supporting` item, confirm an evidence note exists and record the exact learner-facing location for `standalone` and `merged` treatments. Reconsider every omission after drafting. Confirm that the key-idea count is source-derived, the learner-facing structure is not a chapter-by-chapter summary, each key idea has one coherent takeaway, and cross-chapter evidence is merged where it serves that takeaway. Do not turn this audit into a reason to add isolated source details after the argument has been drafted.
10. Run a curriculum-wide form audit. Review all key ideas side by side and ask whether each uses the form that best serves its own argument, or whether a repeated structure has appeared because it was convenient in an earlier idea. Revise forms that reflect a template rather than an independent editorial choice. Do not vary form merely for variation’s sake.
11. If a user says the summary is untrusted or broadly flawed, regenerate learner-facing files from source notes and source chunks. Do not patch the existing summary as the primary repair.
12. State any source or extraction limitations plainly.
