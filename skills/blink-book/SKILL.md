---
name: blink-book
description: Create Blinkist-style learning curricula from one nonfiction book or book-like resource, especially when the user provides a book title, PDF, EPUB, or asks for a mobile-friendly key-ideas summary with quizzes. Use when Codex must verify familiarity/access to the source, process book content and original visuals without loading the whole book into context, produce section-based Markdown under a per-book folder, extract source visuals as PNGs, create comprehension checks, and keep the learner-facing reading time under 1 hour.
---

# Blink Book

## Purpose

Turn one nonfiction book into a mobile-friendly learning curriculum modeled on Blinkist: usually 7-8 transferable key ideas, crisp accessible prose, original visuals only, one short comprehension check per key idea, and a final review. Write in English.

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
    extraction-log.md
    source-terms.md
    key-idea-plan.md
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
5. Read the source map, table of contents, intro/conclusion, headings, chapter openings/endings, and figure captions.
6. Create `_work/source-terms.md` before synthesis. Record the author's named models, pillars, frameworks, recurring key terms, acronyms, and any terms the book explicitly defines. Include the source anchor for each and mark which terms must appear verbatim in the overview or key ideas.
7. Process the book in passes. Write concise notes in `_work/chapter-notes/`; do not keep the whole source in chat context.
8. Synthesize the strongest teachable ideas, prioritizing Blinkist-style key ideas over chapter-by-chapter structure.
9. Before drafting learner-facing files, create `_work/key-idea-plan.md`. For each proposed key idea, include: transferable takeaway, why it matters, source basis, named source terms to preserve verbatim, critical terms to define in-line, and book-specific example to use or omit.
10. Reread only the source chunks needed for each key idea before writing the final section and quiz.
11. Run word-count and link/visual validation scripts before final delivery.

For PDFs, inspect extraction quality before synthesis. If text order, OCR, or visual extraction is unreliable, report the limitation and ask for a better source when the problem prevents faithful output.

## Writing Model

Match the Blinkist model:

- Surface the book's most valuable and memorable transferable insights.
- Create a clear structure that brings those ideas to light.
- Use numbered key ideas, not chapter summaries.
- Follow the Blinkist approach: key ideas are the big transferable takeaways, not book-specific stories, scenes, or examples. Use anecdotes only as brief support for the broader idea.
- Give every key idea a title that states a transferable lesson. Do not title a key idea after an anecdote, chapter event, place, person, object, or phrase from the book unless the book is specifically about that case.
- Keep book-specific examples short. Default to at most one brief example per key idea, and include it only when it clarifies the transferable idea.
- Include an overview landing file with title, author, total estimated reading time, key-idea table of contents, visual inventory link, quiz index, and review link.
- Put the real title inside each file, not in the filename. Use stable filenames: `key-idea-01.md`, `key-idea-02.md`, etc.
- Include previous/next navigation at the bottom of each key-idea file.
- Add a section-level `Source basis` note at the bottom of each key idea. Prefer stable anchors such as part, chapter, section heading, named figure/table, or EPUB anchor. Use PDF page numbers only when unavoidable.

## Source Terminology Integrity

Preserve the author's named model terms. Plain paraphrase is useful for explaining a term, but it must not replace the term when the term is part of the book's core structure.

- Before writing learner-facing files, identify the book's named models, pillars, stages, frameworks, rules, and terms the author explicitly defines.
- Treat terms from the title, subtitle, table of contents, introduction, conclusion, glossary, index, diagrams, and summary chapters as candidates for preservation.
- Distinguish between the author's named structure and nearby supporting ideas. For example, if a book says the model has three named parts, those exact terms must appear; nearby ideas can be explained in their own place but must not be promoted into the author's model.
- In the overview, name the book's central model terms verbatim before paraphrasing them in plain language.
- In key ideas, use the source term when the section teaches that concept, then define it in-line with plain wording.
- Do not swap a source term for a broader synonym when that would hide the author's structure. For example, do not replace a named pillar with a paraphrase like `skill` unless the source term also appears nearby.
- Do not invent a neat triad, framework, or label from adjacent concepts. If the source does not name it that way, present it as an interpretation, not as the author's model.
- Keep the learner-facing summary source-pure. Do not mention the user's comments, questions, corrections, disputes, prior drafts, audits, or why a term is included or excluded. Use feedback only to improve the process and the `_work/` files. The final learner-facing prose must read as if written directly from the book.
- If a user correction reveals a missing source term, add the term where the book teaches it and define it plainly. Do not add defensive sentences such as `X matters, but Y is the real model` unless the book itself makes that contrast.

Style for this user:

- Write for a smart expert entering a new domain.
- Be crisp, precise, and accessible without dumbing down.
- Use plain, literal wording. Avoid vague metaphors, business buzzwords, and consultant shorthand. Plain does not mean childish; it means the reader should not need to translate the sentence.
- Run these sentence-level tests on learner-facing prose:
  - Actor test: can the reader tell who does what?
  - Decision test: if the sentence is about power or authority, does it say what people are allowed to decide?
  - Concrete meaning test: can an abstract noun be replaced by a concrete action without losing meaning?
  - One-read test: can a smart reader understand the sentence after one read?
  - One-idea test: does the sentence carry one main idea? Split it if it carries a rule, reason, and example at once.
- Prefer active voice and present tense unless another form is clearer.
- Prefer common words over formal words: `use`, not `utilize`; `help`, not `facilitate`; `about`, not `regarding`; `start`, not `commence`.
- Watch for noun-heavy phrasing, especially words ending in `-ion`, `-ment`, `-ity`, and `-ance`. These are allowed, but often hide the action. Rewrite when a verb is clearer.
- Avoid meta labels such as `the transferable lesson is this`. State the lesson directly.
- Avoid motivational filler, corporate fluff, and chatty over-explanation.
- Use short paragraphs, bullets, and tables to reduce prose load.
- Define any critical proper noun, acronym, role, setting-specific term, or domain term briefly at first use in the relevant sentence. Do not create a separate glossary or abstract terms section.
- Make cause/effect, constraints, tradeoffs, and failure modes visible in plain language.
- Add an optional `Mechanism` block only when it clarifies the idea; if used, define what the mechanism does in ordinary words.
- During drafting, mark vague, generic, jargony, or compressed sentences as `TOO GENERIC` in notes and rewrite them before final output.
- Before final output, review learner-facing prose for jargon, buzzwords, and compressed phrasing. Judge the sentence, not isolated words. Rewrite only when the sentence is unclear, too abstract, or makes the reader translate the idea.

## Length And Quizzes

Keep learner-facing summary reading time under 60 minutes. Estimate at 225 words/minute. Do not enforce Blinkist's strict 15-minute total timebox; use the length needed for clear transferable learning while staying under one hour. Shorter is better when it does not oversimplify.

Each key idea should usually take about 5-8 minutes to read, but can be shorter when the idea is simple. Use longer sections only when needed to preserve an important mechanism, distinction, or source-supported nuance.

Create at most one comprehension question per key idea. Put it in a separate quiz file with the answer hidden in a collapsible `<details>` block. Create optional going-beyond quiz files only when useful, and keep them separate from comprehension checks.

Create `review.md` by default. Repeat all comprehension questions directly in sequence with collapsed answers.

## Files To Read When Needed

- Read `references/output-templates.md` before writing final learner-facing files.
- Use `scripts/requirements.txt` for helper-script dependencies.
- Use `scripts/source_map.py` for EPUB/PDF source maps and bounded text extraction.
- Use `scripts/extract_visuals.py` for original visual extraction and PNG conversion.
- Use `scripts/count_reading_time.py` before final delivery.
- Use `scripts/validate_output.py` before final delivery.

## Final QA

Before responding to the user:

1. Verify `metadata.yaml`, `overview.md`, `review.md`, `quizzes/`, `visuals/`, and `_work/` exist as applicable.
2. Run `scripts/count_reading_time.py books/<book-slug>` and compress if over 60 minutes.
3. Run `scripts/validate_output.py books/<book-slug>` and fix missing links, missing quiz files, missing previous/next navigation, and missing visual files.
4. Create `_work/final-audit.md` with one row per key idea covering: undefined critical terms, vague wording, jargon, overcompressed sentences, story dominance, transferability, and source support.
5. Add a source-terminology audit to `_work/final-audit.md`: list every required term from `_work/source-terms.md`, where it appears in learner-facing files, and whether it is defined in-line. Fix missing or mislabeled source terms before delivery.
6. Run a source-purity audit over learner-facing files. Remove any wording that responds to the user's feedback, explains a prior mistake, mentions an audit, or contrasts a user-suggested term with the source model instead of summarizing the book.
7. Run a clarity audit sentence by sentence. Use the actor, decision, concrete meaning, one-read, and one-idea tests. Do not remove words just because they appear on a review list; remove or rewrite only when the sentence is unclear, too abstract, or too compressed.
8. Run a transferability audit: every key idea must answer what the learner can use outside the book's specific setting. Source-specific examples must support the idea, not become the main point or title, unless the book is itself about that specific case.
9. If a user says the summary is untrusted or broadly flawed, regenerate learner-facing files from source notes and source chunks. Do not patch the existing summary as the primary repair.
10. State any source or extraction limitations plainly.
