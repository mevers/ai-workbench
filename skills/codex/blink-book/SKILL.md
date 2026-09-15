---
name: blink-book
description: Create Blinkist-style book learning curricula from one nonfiction book or book-like resource. Use when the user provides a book title, PDF, EPUB, or asks to create a full Blink Book, a Blink-only summary, or an assessment for an existing Blink Book. Verify source access, process book content and original visuals without loading the whole book into context, produce section-based Markdown, and create evidence-based comprehension checks.
metadata:
  version: "1.4.2"
---

# Blink Book

## Purpose

Turn one nonfiction book into a mobile-friendly learning curriculum modelled on Blinkist: a source-derived set of transferable key ideas, crisp accessible prose, original visuals only, and, when requested, comprehension checks and a final review. Write in English.

## Version provenance

The `metadata.version` value in this file is the authoritative Blink skill version. Use semantic versioning and increment it whenever a released change alters the skill's behaviour, outputs, or validation. Whenever `all` or `blink-only` mode creates or regenerates learner-facing summary files, copy the current value to `blink_skill_version` in `metadata.yaml` and to the `Summary generated with Blink skill version:` line in `overview.md`. Do not add a current version to an existing book unless its learner-facing summary was created or regenerated under that version. Assessment mode preserves the recorded value.

## Modes

Use **all** by default. A request to “create a blink”, “create a Blink Book”, “summarise this book”, or similar ordinary language always means **all** unless the user explicitly asks for the assessment-free variant.

Use the assessment-free **blink-only** variant only when the user says one of these exact phrases, case-insensitively: **“summary only”**, **“no assessment”**, or **“blink-only”**. Do not infer blink-only mode from the word “blink” by itself.

- **all:** Create the complete Blink Book: source work, overview, key ideas, visuals, quizzes, and review. Complete the learner-facing phase before starting the assessment phase.
- **blink-only:** Create or regenerate only the source work, overview, key ideas, and visuals. Do not create or modify `quizzes/` or `review.md`; do not inspect or use an application context. Omit assessment links from the overview and key ideas. If assessment files already exist, leave them untouched. Run the existing validator with `--mode blink` for this internal mode.
- **assessment:** Create or regenerate only `quizzes/`, `review.md`, `_work/assessment-plan.md`, and `_work/assessment-reviews/` for an existing complete Blink Book. Require `metadata.yaml`, `overview.md`, all `key-idea-*.md` files, `visuals/`, and required source-work files to exist first. Never modify the overview, metadata, key ideas, visuals, existing source-work files, or source material. If they are incomplete, stop and tell the user what the existing Blink Book needs; do not repair it as part of assessment mode.

In **all** mode, write the overview and key-idea assessment navigation during the learner-facing phase, then create the assessment without altering those files. This preserves the same boundary as `assessment` mode.

For summary reviews, use the existing review notes to show how the most vulnerable passage supports the key idea or enables the requested judgement or action. Flag a material gap if this requires inventing reasoning, facts or instructions. Accept concise, practical wording when it works as written; extra detail is not a requirement.

## Mandatory independent summary review

For every `all` or `blink-only` Blink Book, complete the independent summary review protocol below. Use two distinct reviewer roles: a source-blind critical reader and a source-aware fidelity editor. Run up to three paired review rounds. After a failed round, make one consolidated, substantive repair of all BLOCKER findings before both reviewer roles assess the complete current bundle afresh without prior findings; do not use piecemeal micro-iterations. If a BLOCKER remains after round 3, stop with the Blink incomplete. This requirement does not apply to `assessment` mode.

Use a hard 60-minute wall-clock budget for each invocation in any mode. Record the start time, end or stop time, and review-wave counts in `_work/final-audit.md`. Check elapsed time before starting each review or repair stage. At the limit, stop with the output incomplete; do not lower a gate or continue iterating.

Use a book-centered output folder:

```text
books/<book-slug>/
  metadata.yaml
  overview.md
  key-idea-01.md
  key-idea-02.md
  ...
  review.md                    # all and assessment modes only
  quizzes/                     # all and assessment modes only
    key-idea-01-comprehension.md
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
      key-idea-01-full-draft.md
      key-idea-01-source-blind-review.md
      key-idea-01-source-aware-review.md
    final-reviews/
      overview-source-blind-review.md
      overview-source-aware-review.md
    assessment-plan.md          # all and assessment modes only
    assessment-reviews/         # all and assessment modes only
      source-aware-review.md
      context-language-review.md
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
6. Create `_work/source-structure.md` before choosing key ideas. Inventory the book's core thesis, named models and pillars, named mechanisms or practices, recurring arguments, material limits or tradeoffs, important case evidence, and materially important evidence provenance such as a named research programme, report series, institution, or partnership. Give each item a source anchor and classify it as `core`, `supporting`, or `context`. Mark source terms that must appear verbatim in learner-facing files.
7. Create `_work/source-evidence.md` from bounded source reading. For every `core` or `supporting` inventory item, record its ID, the source claim or distinction, a concise source-grounded note or example, and exact source anchors. Do not draft learner-facing text from the inventory alone.
8. Synthesize the strongest teachable ideas from the source. Derive the number of key ideas from the book's arguments, named models, major practices, and important distinctions; do not start from a target count.
9. Before drafting learner-facing files, create `_work/key-idea-plan.md` from the source-structure inventory and evidence notes. Give every `core` or `supporting` item one treatment: `standalone`, `merged`, or `omitted`. For a merge, name the exact key idea and the item’s contribution. For an omission, give a reason. Do not use a broad part, chapter, or category as a treatment. Record each proposed idea’s central conclusion, evidence-note IDs, explanatory route, required source terms, and source examples to use or omit. Record the source-derived key-idea count and rationale. This is a selection and coverage map, not a paragraph checklist: do not force every mapped item into learner-facing prose.
10. Draft the Big Picture from the same source-structure and evidence work. Keep the Big-Picture Writing and Big-Picture Validation rules below unchanged. It has its own synthesis job; do not construct it by mechanically shortening the key ideas.
11. For each key idea, reread its linked source chunks and create `_work/idea-argument-packs/key-idea-NN.md`. Assemble enough source material to support a full explanation: the conclusion, the problem or tension it addresses, the causal explanation, essential conditions or limits, concrete source detail, and the transferable implication. Include a plain-language argument chain that states the source fact, the mechanism, the concept, and the transferable conclusion. Do not write learner-facing prose until this chain explains how the source detail supports the conclusion. An argument pack is not a concise evidence summary and is not learner-facing prose.
12. Design the reader’s path for each idea before drafting. First decide the transferable conclusion and central model or distinction the reader must understand. Then select only the source detail needed to explain and support that argument. Choose the sequence that best serves it, and decide where prose, a short list, a comparison, or a sequence will improve reading. Do not use a fixed section template.
13. Write a deliberately fuller first draft from the argument pack in `_work/key-idea-drafts/key-idea-NN-full-draft.md`. Then tighten it into the learner-facing section. Preserve the reasoning that makes the idea understandable: remove repetition and unnecessary detail while retaining essential definitions, connections, actors and actions. If material does not advance the section’s central lesson, reconsider its placement. Before finalising, run the plain-language and non-template prose pass below. For every sentence, ask whether a reader can identify what it refers to, what happens, and why it matters in this argument on a natural first read. Rewrite from the argument chain or remove any sentence that fails. Do not add post-hoc padding to meet a reading-time estimate. If tightening reveals a thin idea, return to the argument pack and source chunks, then rebuild the explanation. Repeat the complete prose pass after every reviewer repair; do not add a repair as another clause to an already finished sentence.
13a. Before independent review, complete every writer-side audit required below: Key-Idea Validation, Big-Picture Validation, source terminology, source purity and coverage, curriculum-wide form, visual integration, length, and deterministic prose checks. Apply all resulting learner-facing edits before the first paired review.
13b. Run the mandatory independent summary review protocol below on `overview.md` and every final learner-facing key idea. After each reviewer-repair stage, rerun deterministic validation and inspect the repaired passage, its surrounding argument, and every affected cross-file relationship. Repeat a full manual whole-file writer audit only when a repair changes the file's structure or central argument.
13c. In `all` or `blink-only` mode, finish the learner-facing summary, pass the completion release gate, and run `scripts/validate_source_work.py books/<book-slug>` before beginning any assessment work. In `blink-only` mode, stop here.
15. In `all` or `assessment` mode, complete the learner-facing phase first, then follow the assessment architecture and its routed references. Do not create, configure, edit, or offer to create an application context as part of this skill.

For PDFs, inspect extraction quality before synthesis. If text order, OCR, or visual extraction is unreliable, report the limitation and ask for a better source when the problem prevents faithful output.

## Writing Model

Match the Blinkist model:

- Surface the book's most valuable and memorable transferable insights.
- Create a clear structure that brings those ideas to light.
- Use a source-derived number of numbered key ideas, not chapter summaries. A key idea must express one coherent takeaway or insight. It may span multiple chapters, and one chapter may contribute to several key ideas. Use chapters as source anchors and evidence, never as the default unit of synthesis.
- Follow the Blinkist approach: key ideas are the big transferable takeaways, not book-specific stories, scenes, or examples. Use anecdotes only as brief support for the broader idea.
- Give every key idea a title that states a transferable lesson. Do not title a key idea after an anecdote, chapter event, place, person, object, or phrase from the book unless the book is specifically about that case.
- Keep book-specific examples short. Default to at most one brief example per key idea, and include it only when it clarifies the transferable idea.
- Include an overview landing file with title, author, total estimated reading time, key-idea table of contents, and visual inventory link. In `all` mode, also include quiz and review links. In `blink-only` mode, omit them. In `assessment` mode, do not alter the overview.
- Put the real title inside each file, not in the filename. Use stable filenames: `key-idea-01.md`, `key-idea-02.md`, etc.
- Include a backlink to `overview.md` and previous/next navigation at the bottom of each key-idea file. In `all` mode, the final key idea must use its `Next` link for [End-of-book review](review.md). In `blink-only` mode, the final key idea has no `Next` link. In `assessment` mode, do not alter any key-idea file.
- Every `review.md` must end with a working backlink to `overview.md`. This applies in both `all` and `assessment` modes.
- Add a section-level `Source basis` note at the bottom of each key idea. Prefer stable anchors such as part, chapter, section heading, named figure/table, or EPUB anchor. Use PDF page numbers only when unavoidable.

## Source Terminology Integrity

When the source names a concept, hypothesis, framework, model, stage, rule, or practice, use its exact source term at first mention and explain it immediately in plain language. Do not replace it with a new label or compressed synonym. Source terminology, including its spelling and capitalisation, overrides the Blink's house style. Ordinary paraphrase is allowed after the exact term has been established.

Use `_work/source-structure.md` as the writer's terminology aid, but do not treat it as independent evidence that terminology coverage is complete. Include named terms the summary teaches, not every term in the book. Do not promote a nearby supporting idea into the author's framework or present a Blink-created interpretation as an authorial label. Keep learner-facing prose source-pure: do not mention user feedback, prior drafts, or the drafting process.

## Plain-language and non-template prose

These rules apply to the overview and every key idea. Source fidelity governs the meaning, evidence, qualifications, and exact named terms. It does not require the source's sentence structure. Preserve the author's terminology while explaining it in simpler syntax.

- Write for a natural first reading. Prefer short, direct sentences with one main claim or causal step. Split a sentence when it stacks definitions, causes, contrasts, examples, or qualifications. A sentence fails when a reader must reread it or hold one clause in memory to understand another.
- Do not use em dashes in authored prose. Do not use the rhetorical contrast pattern `not X but Y` or variants such as `not just X but also Y`, `not merely X but Y`, `X is not Y; it is Z`, or `X does not mean Y; it means Z`. The only exception is a short verbatim source quotation that is clearly marked as a quotation. The source-aware reviewer must verify the wording and source anchor.
- Do not use generic rhetorical pivots, polished slogans, repeated imperatives, decorative three-part lists, or a repeated section formula merely to create cadence. Every sentence must carry source content, explain a relationship, or provide necessary navigation. Delete prose whose only job is to announce that an idea is important, surprising, or useful.
- After any review repair, rerun this pass across the complete modified file. Add needed explanation in the clearest place and then resynthesise the surrounding prose. Do not preserve every prior sentence and bolt the repair onto it.

## Writing Key Ideas

- Write for a smart expert entering a new domain. Be clear, precise, and accessible without simplifying the book’s argument.
- Use sentence case and British English in all learner-facing headings. Capitalise the first word of the heading and the first word after a colon, plus abbreviations and proper nouns; do not use title case.
- Build each key idea as one connected explanation. Establish the conclusion, use source detail to explain it, and show why it matters. Choose the order that best serves the argument.
- Make relationships explicit and choose an actor that identifies the kind of claim being made. Use the authors for arguments and definitions, researchers or a named study for empirical work, a survey for measurements, an analysis for statistical findings, and a figure or table for displayed evidence. State the idea directly when attribution adds no meaning. Do not default to editorial placeholders such as `the source`. Name what changed and why it mattered when describing a sequence, contrast, cause, decision, or outcome; do not make the reader infer the connection between paragraphs.
- Start with the source’s concrete claims, actions, distinctions, and examples. Generalise only after the reader can see the point. Do not replace source detail with generic workplace language or an abstract diagnosis.
- Keep related sentences together, but do not compress several relationships into one sentence. Use separate sentences for separate causal steps or qualifications, even when the source presents them together.
- Give each paragraph a clear job in the explanation and a visible connection to what comes before. Use short paragraphs and lists when they improve scanning; do not turn a sequence of related thoughts into disjoint fragments.
- Use plain, literal language. Prefer active verbs and common words when they preserve meaning. Avoid filler, buzzwords, vague abstractions, and labels that merely announce the point.
- Each key idea must use source-specific evidence that genuinely carries its explanation.
- When an idea teaches the book’s core model, define its central terms plainly and explain their relationship. Do not introduce central concepts merely as labels.
- Use headings only when they form a clear, parallel sequence in the transferable argument. Omit them when they would merely divide the text or narrate a case study.
- Use a table when it makes a transferable distinction, comparison, or relationship easier to grasp. Let source examples support the table’s argument; do not make a case study the table’s main structure.
- Strongly favour original source figures that materially improve understanding or retention, especially figures that explain a key idea or named model. Embed them where the idea is taught. Ground their explanation in the source, including relevant captions, prose, and linked notes; never guess from visual appearance. An unclear secondary detail is not a reason to omit an otherwise useful figure: explain only the supported meaning. Omit the figure only if it cannot be used without speculation.
- Begin with a full source-grounded draft, then tighten for reading ease. Do not begin with a compressed version and expand it afterward to reach a length expectation.
- Use `Remember This` as a bullet-point retention recap. Include the central conclusion and any condition or distinction needed to keep it accurate; do not introduce new material.

## Key-Idea Validation

Do not use a generic pass/fail checklist. For each final key idea, create `_work/key-idea-drafts/key-idea-NN-clarity-review.md` containing:

- the central conclusion in one plain sentence;
- the source mechanism that explains or proves it;
- the source example used, if any, and its supporting role;
- the exact sentence from the draft most likely to confuse a first-time reader, followed by its revision or deletion. Do not record `none`, `already clear`, or a general comment in place of this evidence.

Then apply the plain-language and non-template prose pass to every sentence. A final key idea fails validation when a reader cannot identify what a sentence refers to, what happens, and why it matters to the argument on a natural first read; when a sentence contains avoidable nesting or several separable relationships; when a central named term is introduced but not explained; when prohibited prose patterns remain; or when the source example rather than the transferable argument determines the structure. Return to the argument chain and revise before delivery.

The clarity review records the writer’s diagnostic work; it is not a final-QC gate and cannot substitute for the independent summary review.

## Independent summary review protocol

### Source-blind critical reader

Give this reviewer only `overview.md` and the final `key-idea-*.md` files. Do not provide the source, source work, assessment files, drafts, prior findings, expected conclusions, or writer rationale.

Its job is to test whether a first-time reader can understand the complete summary on a natural first read, without charitable interpretation, source knowledge, close analysis, or mental rewriting. Before reconstructing the argument, read each file once in order and audit it paragraph by paragraph. Report all findings in wave 1. Later text cannot repair an unclear first use, and a related word form does not count as an established definition. Only after completing this linear audit may the reviewer reconstruct the file's conclusion, mechanism, and implication.

Classify a finding as a `BLOCKER` only when ambiguity, an undefined referent, or compression materially prevents or changes understanding of a central conclusion, mechanism, qualification, or action. Classify optional wording or style improvements as `ADVISORY`; advisories do not fail the review or trigger repair. The reader must be able to state what a central term refers to, who acts, what happens, and why it matters without rereading the sentence.

For every finding, record its severity, the exact passage, the reader question it creates, and the required repair when it is a blocker. Check that unfamiliar references and embedded visuals receive enough prose context to serve the argument rather than supplying missing meaning. Put the linear audit in `## Plain-language and style`. In that section, also quote the passage that creates the greatest first-read difficulty, judge whether it is materially clear on a natural first read, and record the prohibited-pattern check. Audit repeated attribution formulas across the complete summary. Assess a pervasive use of editorial placeholders as one curriculum-wide issue that identifies the affected files instead of splitting it into sentence-level findings. Treat it as a blocker only when the pattern repeatedly obscures the actor or evidence type or makes the learner-facing prose materially abstract. A passing review may not omit this evidence or replace it with a general assurance.

### Source-aware fidelity editor

Give this reviewer the final learner-facing bundle, the source map and index, and direct access to the source so it can search and read bounded passages. Do not provide the writer's source structure, evidence notes, key-idea plan, terminology baseline, drafts, prior findings, expected conclusions, or rationale.

Before opening the learner-facing bundle, independently derive a source-coverage baseline containing the indispensable thesis, named frameworks or models, evidence base and provenance, and material limits. An item is indispensable when omitting it would materially misrepresent what the book argues or why its evidence carries weight. Record this in `## Independent coverage baseline`. Then compare the summary's selection with the baseline. A missing or distorted indispensable item is a `BLOCKER`.

Independently identify the named concepts that the Blink teaches. Verify that their exact source terms appear at first mention and are explained plainly. An invented substitute label is a `BLOCKER` even when its intended meaning is inferable.

It must also verify the summary's claims, mechanisms, conditions, trade-offs, examples, and visual explanations against the source. Simpler syntax is expected and must not be treated as loss of fidelity when the meaning remains intact. If a prohibited prose pattern appears inside a direct quotation, verify that the wording is verbatim and that the recorded source anchor supports it. For every finding, record its severity, the exact learner-facing passage, the source anchor, the issue, and the required repair when it is a blocker. Its standard is faithful explanation, not copied wording or unnecessary source detail.

### Completion release gate

1. **Initial paired wave:** Spawn two separate agents, one for each role. Both must be different from the writer and from each other. Neither may see the other review. They review the complete learner-facing bundle concurrently, report all findings without editing it, and label each finding `BLOCKER` or `ADVISORY`.
2. **Severity:** A `BLOCKER` is a material factual or unsupported claim, omitted or distorted indispensable content, provenance, or limit, central ambiguity, source-grounding failure, or another defect that can change the learner's understanding or action. An `ADVISORY` is non-material polish. Only blockers fail a review or authorise repair.
3. **Hash-bound file decisions:** Every per-file PASS applies only to the exact learner-file hash recorded in that review. A learner-facing edit invalidates both reviews for the changed file. PASS records for unchanged files remain valid while their hashes remain unchanged.
4. **Up to three fresh rounds:** After any failed round, the writer makes one consolidated, substantive repair of all blockers from the source before both reviewers assess the complete current learner-facing bundle afresh without prior findings; do not repair advisories or use piecemeal micro-iterations.
5. **Stop after round 3:** If either reviewer reports a blocker in round 3, keep the Blink incomplete and report the blocker.
7. **Budget stop:** Before each review or repair stage, check the 60-minute invocation budget. At the limit, keep the Blink incomplete and report where the process stopped.
8. **Release:** Release only when every learner-facing file has both reviewer PASS records for its current hash and neither record contains a blocker. Do not make later learner-facing changes without invalidating and renewing both records for every affected file.

Reviewers must not edit learner-facing prose. The final release reviewers must author the existing per-file review records themselves. Each record must include `**Review wave:** 1`, `2`, or `3`, the reviewed learner file's SHA-256 hash, `## Review conditions`, `## Reader reconstruction`, `## Blockers`, `## Advisories`, and `## Gate decision`; source-blind records must also include `## Plain-language and style`, and source-aware records must also include `## Independent coverage baseline` and `## Source terminology and fidelity`. Use `Decision: FAIL` when `## Blockers` contains any finding. Use `Decision: PASS` only when `## Blockers` contains exactly `None.` or `None`; advisories may remain. Record diagnostic findings, repairs, reviewer identities, wave counts, and review decisions in `_work/final-audit.md`.

For each key idea, retain `_work/key-idea-drafts/key-idea-NN-source-blind-review.md` and `_work/key-idea-drafts/key-idea-NN-source-aware-review.md`. Retain `overview-source-blind-review.md` and `overview-source-aware-review.md` in `_work/final-reviews/`. `scripts/validate_learner_quality.py` enforces the deterministic prose prohibitions and checks that final review records exist and contain `PASS`; it cannot establish semantic quality or replace either reviewer. If the required separate agents cannot be spawned, stop and report that the Blink cannot be completed under this skill.

## Big-Picture Writing

For the Big Picture in `overview.md`:

1. **Focus on the book’s transferable ideas.** Tell the reader what the book teaches. Use specific settings and scenarios to establish the stakes or clarify the argument.
2. **Preserve and plainly explain the book’s central models, pillars, and frameworks when they are present.** Key concepts are more important than specific story details.
3. **Use the right level of abstraction.** Make models, pillars, and frameworks concrete. Do not invent vague labels.
4. **Use case studies and examples as evidence, not the main story.**

## Big-Picture Validation

This is the writer’s source-guided diagnostic, not a final-QC gate. It cannot substitute for the source-blind critical reader or source-aware fidelity editor.

Before delivery, assess `overview.md` against all five checks:

1. **Premise:** Does it identify the real problem, question, or subject of the book, rather than a downstream symptom?
2. **Argument:** Does it state the book’s main transferable idea and any central named model, pillar, or framework?
3. **Selection:** Do settings, examples, and outcomes clarify the argument rather than become the story?
4. **Fidelity:** Are the central claims supported by relevant source passages, without invented labels, causal claims, or evaluations?
5. **Clarity:** Can a smart reader understand the overview in one read, including why the book matters?

## Length and assessments

Keep learner-facing summary reading time under 45 minutes. Estimate summary text only, excluding quizzes and review, at 135 words per minute. Record the calculated estimate, rounded to the nearest whole minute, in `metadata.yaml` and `overview.md`; do not add a separate estimate for the full learning experience.

Never ask the user to choose a duration. Estimate the appropriate length from the source-derived number of core ideas. Use roughly five minutes per key idea as an editorial calibration: draft each idea fully first, then tighten it toward a readable form with enough explanation and useful detail. Three to eight minutes per idea is normal, depending on the material. This is a guide, not a target or a reason to change the source-derived idea count. Investigate a material departure from it rather than treating shortness as success. If a final idea is thin, return to its argument pack and source passages; do not pad the existing draft. Allocate space according to the source: a key idea may need an explanation of the claim, why it works, its limits or tradeoffs, and a source-supported example or practice. Do not reduce an idea to a headline, one named term, and an application merely to be concise.

If a new version is materially shorter than an existing trusted version, explain the reduction in `_work/final-audit.md` and treat it as a likely regression unless source coverage has demonstrably improved.

### Assessment architecture

Assessment work begins after the summary is complete. Preserve source processing, key ideas, visuals and summary review. The book determines correct reasoning; the confirmed application context determines the domain and role. The user’s requirements apply to writing and review. Assessment form and review follow these references, including when an older context file contains writing advice:

- `references/assessment-workflow.md`: plan, draft, question design and practice.
- `references/assessment-review.md`: independent review, repair and release.
- The assessment section of `references/output-templates.md`: file schemas.

Read all three before assessment work. Follow this sequence:

1. Read the confirmed context, or use generic recap when requested. Do not create or edit a context as part of assessment generation.
2. Choose `FULL` or `RECAP_ONLY` per idea and plan the learning target. Use a plausible fictional situation consistent with the context only when it makes the book's distinction useful. Print the facts needed to answer; do not present invented events as facts about the user.
3. Draft questions, options and practice together, then freeze the answer key and plan for review.
4. Run two independent reviewers concurrently: source fidelity and learner usability. The learner reviewer records a first pass before seeing answers or explanations.
5. Consolidate repairs, replacing weak items where necessary. Repeat with fresh reviewers for at most three rounds, within the invocation budget.
6. Release only after both reviews and structural validation pass on the same files. Stop incomplete at either limit.

Assessment edits invalidate both reviews. Plan edits invalidate source review; context edits invalidate both reviews and contextual plans.

## Files To Read When Needed

- Read `references/output-templates.md` before writing final learner-facing files.
- Before writing assessments, read `references/assessment-workflow.md`, `references/assessment-review.md`, and the assessment section of `references/output-templates.md` completely.
- Use `scripts/requirements.txt` for helper-script dependencies.
- Use `scripts/source_map.py` for EPUB/PDF source maps and bounded text extraction.
- Use `scripts/build_source_index.py` to generate the deterministic source-discovery index after source mapping.
- Use `scripts/validate_source_work.py` to verify that every core or supporting source item has both evidence and a key-idea-plan treatment.
- Use `scripts/validate_learner_quality.py` as a structural check for retained fuller drafts and final review records. It cannot approve learner-facing clarity or replace the independent summary review.
- When changing the summary-review subsystem, run `scripts/test_validate_learner_quality.py`.
- Use `scripts/extract_visuals.py` for original visual extraction and PNG conversion.
- Use `scripts/count_reading_time.py` before final delivery.
- Use `scripts/validate_output.py` before final delivery.

## Final QA

Before responding to the user:

1. In `all` or `blink` mode, verify `metadata.yaml`, `overview.md`, `visuals/`, and `_work/` exist. Verify `_work/source-index.md`, `_work/source-structure.md`, `_work/source-evidence.md`, `_work/key-idea-plan.md`, and the per-idea argument packs before synthesis.
2. In `all` or `blink` mode, run `scripts/count_reading_time.py books/<book-slug> --limit-minutes 45 --wpm 135`. Fail if the learner-facing summary exceeds 45 minutes. Do not treat a shorter result as a success without checking the source-coverage map.
3. Run `scripts/validate_output.py books/<book-slug> --mode blink` for `blink-only` mode; `--mode all --assessment-mode contextual --context-file <confirmed-context-path>` or `--mode all --assessment-mode generic` for `all` mode; or the equivalent `--mode assessment` command for assessment mode. For assessments, complete the bounded three-round gate in the assessment references. Fix only files permitted by the selected mode.
4. In `all` or `blink` mode, run `scripts/validate_source_work.py books/<book-slug>` and fix missing evidence notes or plan treatments.
5. In `all` or `blink` mode, run Key-Idea Validation and retain each per-idea clarity review and fuller draft. Complete the bounded completion release gate in the Independent summary review protocol. Run `scripts/validate_learner_quality.py books/<book-slug>` as a structural, hash-freshness, and prohibited-pattern check; it must pass, but it cannot overrule either reviewer. Record findings, blocker-repair stages, reviewer identities, wave counts, and decisions in `_work/final-audit.md`. Confirm that both reviewers passed every learner-facing file at its current hash, that no PASS record contains a blocker, and that each learner-facing key idea was tightened from its retained long draft rather than expanded after a short first pass.
6. In `all` or `blink` mode, run Big-Picture Validation and record the result in `_work/final-audit.md` as a writer diagnostic; it cannot substitute for the independent summary review.
7. In `all` or `blink` mode, add a source-terminology audit to `_work/final-audit.md`: list every required term from `_work/source-structure.md`, where it appears in learner-facing files, and whether it is defined in-line. Fix missing or mislabeled source terms before delivery.
8. In `all` or `blink` mode, run a source-purity audit over learner-facing files and a source-coverage audit against `_work/source-structure.md` and `_work/source-evidence.md`. For every `core` or `supporting` item, confirm an evidence note exists and record the exact learner-facing location for `standalone` and `merged` treatments. Reconsider every omission after drafting. Confirm that the key-idea count is source-derived, the learner-facing structure is not a chapter-by-chapter summary, each key idea has one coherent takeaway, and cross-chapter evidence is merged where it serves that takeaway.
9. In `all` or `blink` mode, run a curriculum-wide form audit. Review all key ideas side by side and ask whether each uses the form that best serves its own argument, or whether a repeated structure has appeared because it was convenient in an earlier idea. Revise forms that reflect a template rather than an independent editorial choice. Do not vary form merely for variation’s sake.
10. In `all` or `blink` mode, check that the Blink includes the source figures that materially improve learning and that their explanations do not speculate beyond the source.
11. If a user says the summary is untrusted or broadly flawed, regenerate learner-facing files from source notes and source chunks. Do not patch the existing summary as the primary repair.
12. State any source or extraction limitations plainly.
