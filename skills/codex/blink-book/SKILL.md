---
name: blink-book
description: Create Blinkist-style book learning curricula from one nonfiction book or book-like resource. Use when the user provides a book title, PDF, EPUB, or asks to create a full Blink Book, a Blink-only summary, or an assessment for an existing Blink Book. Verify source access, process book content and original visuals without loading the whole book into context, produce section-based Markdown, and create evidence-based comprehension checks.
---

# Blink Book

## Purpose

Turn one nonfiction book into a mobile-friendly learning curriculum modelled on Blinkist: a source-derived set of transferable key ideas, crisp accessible prose, original visuals only, and, when requested, comprehension checks and a final review. Write in English.

## Modes

Use **all** by default. A request to “create a blink”, “create a Blink Book”, “summarise this book”, or similar ordinary language always means **all** unless the user explicitly asks for the assessment-free variant.

Use the assessment-free **blink-only** variant only when the user says one of these exact phrases, case-insensitively: **“summary only”**, **“no assessment”**, or **“blink-only”**. Do not infer blink-only mode from the word “blink” by itself.

- **all:** Create the complete Blink Book: source work, overview, key ideas, visuals, quizzes, and review. Complete the learner-facing phase before starting the assessment phase.
- **blink-only:** Create or regenerate only the source work, overview, key ideas, and visuals. Do not create or modify `quizzes/` or `review.md`; do not inspect or use an application context. Omit assessment links from the overview and key ideas. If assessment files already exist, leave them untouched. Run the existing validator with `--mode blink` for this internal mode.
- **assessment:** Create or regenerate only `quizzes/`, `review.md`, `_work/assessment-plan.md`, and `_work/assessment-reviews/` for an existing complete Blink Book. Require `metadata.yaml`, `overview.md`, all `key-idea-*.md` files, `visuals/`, and required source-work files to exist first. Never modify the overview, metadata, key ideas, visuals, existing source-work files, or source material. If they are incomplete, stop and tell the user what the existing Blink Book needs; do not repair it as part of assessment mode.

In **all** mode, write the overview and key-idea assessment navigation during the learner-facing phase, then create the assessment without altering those files. This preserves the same boundary as `assessment` mode.

## Mandatory independent final review

For every `all` or `blink-only` Blink Book, the main agent must obtain two independent sub-agent reviews before delivery: a source-blind critical reader and a source-aware fidelity editor. This is a completion gate, not a polishing step.

- The writer cannot perform either review. The two reviewers must be separate agents from the writer and from each other.
- The reviewers must not see each other’s findings, the writer’s rationale, prior reviews, drafts, or the final audit.
- Neither reviewer may edit learner-facing prose during its first review. The writer makes repairs, then sends each repaired file back to the reviewer whose concern it addresses. Do not treat an editor’s own revision as evidence that the file has passed.
- Do not create, describe, or deliver a Blink Book as complete while either review is pending or has an unresolved concern. If the required separate sub-agents cannot be spawned, stop and report that the Blink Book cannot be completed under this skill.
- This requirement does not apply to `assessment` mode because that mode must not alter learner-facing overview or key ideas.

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
6. Create `_work/source-structure.md` before choosing key ideas. Inventory the book's core thesis, named models and pillars, named mechanisms or practices, recurring arguments, material limits or tradeoffs, and important case evidence. Give each item a source anchor and classify it as `core`, `supporting`, or `context`. Mark source terms that must appear verbatim in learner-facing files.
7. Create `_work/source-evidence.md` from bounded source reading. For every `core` or `supporting` inventory item, record its ID, the source claim or distinction, a concise source-grounded note or example, and exact source anchors. Do not draft learner-facing text from the inventory alone.
8. Synthesize the strongest teachable ideas from the source. Derive the number of key ideas from the book's arguments, named models, major practices, and important distinctions; do not start from a target count.
9. Before drafting learner-facing files, create `_work/key-idea-plan.md` from the source-structure inventory and evidence notes. Give every `core` or `supporting` item one treatment: `standalone`, `merged`, or `omitted`. For a merge, name the exact key idea and the item’s contribution. For an omission, give a reason. Do not use a broad part, chapter, or category as a treatment. Record each proposed idea’s central conclusion, evidence-note IDs, explanatory route, required source terms, and source examples to use or omit. Record the source-derived key-idea count and rationale. This is a selection and coverage map, not a paragraph checklist: do not force every mapped item into learner-facing prose.
10. Draft the Big Picture from the same source-structure and evidence work. Keep the Big-Picture Writing and Big-Picture Validation rules below unchanged. It has its own synthesis job; do not construct it by mechanically shortening the key ideas.
11. For each key idea, reread its linked source chunks and create `_work/idea-argument-packs/key-idea-NN.md`. Assemble enough source material to support a full explanation: the conclusion, the problem or tension it addresses, the causal explanation, essential conditions or limits, concrete source detail, and the transferable implication. Include a plain-language argument chain that states the source fact, the mechanism, the concept, and the transferable conclusion. Do not write learner-facing prose until this chain explains how the source detail supports the conclusion. An argument pack is not a concise evidence summary and is not learner-facing prose.
12. Design the reader’s path for each idea before drafting. First decide the transferable conclusion and central model or distinction the reader must understand. Then select only the source detail needed to explain and support that argument. Choose the sequence that best serves it, and decide where prose, a short list, a comparison, or a sequence will improve reading. Do not use a fixed section template.
13. Write a deliberately fuller first draft from the argument pack in `_work/key-idea-drafts/key-idea-NN-full-draft.md`. Then tighten it into the learner-facing section by removing repetition, generic extrapolation, and source detail that does not advance the explanation; restructure when it improves scanning. Before finalising, run a literal-language pass: for every sentence, ask whether a reader can identify what it refers to, what happens, and why it matters in this argument. Rewrite from the argument chain or remove any sentence that fails. Do not add post-hoc padding to meet a reading-time estimate. If tightening reveals a thin idea, return to the argument pack and source chunks, then rebuild the explanation.
13a. Run the mandatory independent final review described below on `overview.md` and every final learner-facing key idea. A learner-facing file fails until both reviewers pass it.
13b. In `all` or `blink-only` mode, finish the learner-facing summary, pass both independent reviews, and run `scripts/validate_source_work.py books/<book-slug>` before beginning any assessment work. In `blink-only` mode, stop here.
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
- Use sentence case and British English in all learner-facing headings. Capitalise the first word of the heading and the first word after a colon, plus abbreviations and proper nouns; do not use title case.
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
- When a source figure is selected, embed the original figure at the exact point where the learner-facing argument discusses it; do not leave it as an unintegrated asset or a text-only reference. Its surrounding explanation must come solely from the figure’s caption and its accompanying source prose. Quote briefly or make a faithful, bounded paraphrase, and record the exact source anchor. Never create an explanation from visual inspection, including by inferring what a line, area, arrow, colour, position, or shape means. Do not add a causal, mathematical, or case interpretation unless the source text explicitly provides it. If the source supplies only a caption, use a neutral source-grounded introduction or omit the figure rather than inventing its significance. A caption or nearby source-basis note is not enough, and a visual must not supply a necessary causal link, definition, case context, or conclusion absent from the prose.
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

For every embedded visual, add a `Visual integration` entry to the clarity review. Record the visual filename, the exact surrounding prose that introduces it, the caption and accompanying source-prose anchor, the source-stated feature or relationship being discussed, and the precise contribution it makes to the section’s conclusion. The key idea fails validation if any embedded visual is merely decorative, has no explicit prose-to-visual link, includes unexplained case context, carries an essential part of the argument that is absent from the prose, or includes an interpretation not supported by the figure’s caption or accompanying source prose.

The clarity review records the writer’s diagnostic work; it is not a final-QC gate and cannot substitute for either independent reviewer. Preserve source-defined technical terms that carry the author’s model, and define them in-line. Do not solve a clarity failure by deleting a necessary source term. Instead, explain it plainly at first use and make its relationship to the argument explicit. Remove or rewrite only labels introduced by the blink when they act as unexplained shorthand, invent a framework, or conceal a missing causal explanation.

## Independent final review protocol

### Source-blind critical reader

Spawn this reviewer with no conversation fork. Give it only `overview.md` and the final `key-idea-*.md` files. Do not provide the source, source chunks, source-work files, assessment files, drafts, prior reviews, expected conclusions, or final audit.

Its job is to test whether the prose communicates its meaning without charitable interpretation, source knowledge, or mental rewriting by the reader. It must identify any passage that is vague, needlessly convoluted, jargon-heavy, or abstract in a way that hides meaning. Abstract language is allowed when it is necessary to explain the book’s argument and its meaning is clear in context. It fails when it substitutes for a concrete explanation or leaves the reader unable to say what happens, who acts, or why it matters.

For every actual concern, record the exact passage, the reader question it creates, what information or relationship is missing or obscured, and the required repair: delete, use plainer wording, define a term, name an actor, or state a causal link. The reviewer must not mark a passage clear merely because its likely meaning can be reconstructed from context, prior knowledge, or charitable interpretation.

The reviewer must reconstruct the central conclusion, mechanism, and implication of every reviewed file. Before passing a file, it must identify the passage most likely to confuse a first-time reader and explain why that passage passes or specify the repair. For unfamiliar named references, it must state what the reference is, what happens or decision is relevant, and why it belongs in the argument. A reference fails if the needed context exists only in a visual, source note, linked quiz, or reviewer knowledge.

For every embedded visual, the reviewer must state whether the surrounding prose identifies what the visual depicts, the relevant feature or relationship, and why it advances the current argument. It must fail the file when the reader has to infer the visual’s purpose, reconstruct a link from source knowledge, or use the visual to supply missing case context or causal explanation. It must not endorse an explanation merely because it sounds plausible from the image: the source-aware editor is responsible for source support.

### Source-aware fidelity editor

Spawn a different reviewer with no conversation fork. Give it the final learner-facing overview and key ideas, the relevant source chunks, the source-structure inventory, source-evidence notes, and the terminology baseline. Do not provide drafts, prior reviews, the writer’s rationale, or final audit.

Its job is to test whether the Blink faithfully and clearly represents the book. It must flag invented terms or distinctions presented as authorial, missing or misused named source terms, paraphrases that change a claim, mechanism, condition, or trade-off, unsupported generalisations, and examples that do not support the learner-facing conclusion. It must also flag prose that is technically faithful but so compressed or indirect that it obscures the author’s argument.

For every embedded visual, it must verify that the asset is an original, complete, legible source visual with its required source label/title where the source provides one; that it has no unrelated clipped body text or omitted visual content; and that every statement in its learner-facing explanation is directly supported by the figure caption or the accompanying source prose. It must record the exact supporting source anchor and flag any inferred reading of a line, area, arrow, colour, position, or shape. It must also verify that the source-supported explanation identifies the visual’s role in the argument, and flag a visual that is source-faithful but not argument-integrated.

The fidelity editor must not require copied source wording or unnecessary detail. Its standard is faithful explanation, not textual similarity. For each concern, record the exact learner-facing passage, the source anchor, the fidelity or clarity issue, and the required repair.

### Records and gate decision

For each key idea, retain `_work/key-idea-drafts/key-idea-NN-source-blind-review.md` and `_work/key-idea-drafts/key-idea-NN-source-aware-review.md`. Retain `overview-source-blind-review.md` and `overview-source-aware-review.md` in `_work/final-reviews/`.

Each review record must include `## Review conditions`, `## Reader reconstruction`, `## Concerns and required repairs`, `## Most vulnerable passage`, and `## Gate decision`. The source-aware record must also include `## Source terminology and fidelity`.

Use `Decision: FAIL` when a concern remains. Use `Decision: PASS` only when the reviewer can reconstruct the conclusion, mechanism, and implication without supplying unstated meaning, and no identified concern remains unresolved. Automated checks, source coverage, reading time, and assessment validation do not constitute evidence that learner-facing prose is clear.

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

Everything under this heading governs assessment only. It must not change source processing, idea selection, overview or key-idea prose, visuals, reading-time calculation, or learner-facing summary review.

For the assessment phase of `all` mode and for `assessment` mode, read these files completely and use each for its stated job:

1. `references/assessment-workflow.md` for application-context handling, routes, the single assessment plan, question design, Try-this practice, options, explanations, and mixed review.
2. `references/assessment-review.md` for the two independent semantic reviews, repair invalidation, deterministic validation, and release.
3. The assessment section of `references/output-templates.md` for exact learner-facing and internal artifact schemas.

Do not use the surrounding Blink-content instructions to invent, complete, or judge an applied assessment situation. The confirmed `application-context.md` is the sole authority for workplace situations, actor behaviour, work objects, interaction patterns, and domain language. The book is the sole authority for the tested concept and correct answer.

The assessment workflow has this fixed order:

1. confirm the assessment mode and application context;
2. choose `FULL` or `RECAP_ONLY` for each key idea and freeze one compact `_work/assessment-plan.md`;
3. draft the learner-facing assessments from that plan;
4. obtain an independent source-aware assessment PASS;
5. obtain an independent context, language, and practice PASS; and
6. run deterministic structural validation on the same final assessment bundle.

Fail closed. An unsupported or doubtful workplace situation routes the key idea to `RECAP_ONLY`; it is not repaired with an application assumption. If even source-grounded recap is not possible, stop and report a prerequisite failure in the existing Blink or source work.

No reviewer or validator may substitute for another stage. Any learner-facing assessment change invalidates both reviews. A plan-only change invalidates the source-aware review, and an application-context change invalidates both reviews and every contextual plan entry.

## Files To Read When Needed

- Read `references/output-templates.md` before writing final learner-facing files.
- Before writing assessments, read `references/assessment-workflow.md`, `references/assessment-review.md`, and the assessment section of `references/output-templates.md` completely.
- Use `scripts/requirements.txt` for helper-script dependencies.
- Use `scripts/source_map.py` for EPUB/PDF source maps and bounded text extraction.
- Use `scripts/build_source_index.py` to generate the deterministic source-discovery index after source mapping.
- Use `scripts/validate_source_work.py` to verify that every core or supporting source item has both evidence and a key-idea-plan treatment.
- Use `scripts/validate_learner_quality.py` as a structural check for retained fuller drafts and review records. It cannot approve learner-facing clarity or replace the two independent final reviews.
- Use `scripts/extract_visuals.py` for original visual extraction and PNG conversion.
- Use `scripts/count_reading_time.py` before final delivery.
- Use `scripts/validate_output.py` before final delivery.

## Final QA

Before responding to the user:

1. In `all` or `blink` mode, verify `metadata.yaml`, `overview.md`, `visuals/`, and `_work/` exist. Verify `_work/source-index.md`, `_work/source-structure.md`, `_work/source-evidence.md`, `_work/key-idea-plan.md`, and the per-idea argument packs before synthesis.
2. In `all` or `blink` mode, run `scripts/count_reading_time.py books/<book-slug> --limit-minutes 45 --wpm 135`. Fail if the learner-facing summary exceeds 45 minutes. Do not treat a shorter result as a success without checking the source-coverage map.
3. Run `scripts/validate_output.py books/<book-slug> --mode blink` for `blink-only` mode; `--mode all --assessment-mode contextual --context-file <confirmed-context-path>` or `--mode all --assessment-mode generic` for `all` mode; or the equivalent `--mode assessment` command for assessment mode. For assessments, complete the routed workflow and all applicable gates in the assessment references, repair failures, invalidate affected receipts, and re-review the final artifacts. Fix only files permitted by the selected mode.
4. In `all` or `blink` mode, run `scripts/validate_source_work.py books/<book-slug>` and fix missing evidence notes or plan treatments.
5. In `all` or `blink` mode, run Key-Idea Validation and retain each per-idea clarity review and fuller draft. Run the two independent final reviews for the overview and every key idea, including fresh re-review after repairs. Run `scripts/validate_learner_quality.py books/<book-slug>` as a structural check only; it must pass, but it cannot overrule either reviewer. Record reviewer identities or agents, source-blind and source-aware conditions, concerns, repairs, and final decisions in `_work/final-audit.md`. Confirm that each learner-facing key idea was tightened from its retained long draft rather than expanded after a short first pass.
6. In `all` or `blink` mode, run Big-Picture Validation and record the result in `_work/final-audit.md` as a writer diagnostic; it cannot substitute for either independent final review.
7. In `all` or `blink` mode, add a source-terminology audit to `_work/final-audit.md`: list every required term from `_work/source-structure.md`, where it appears in learner-facing files, and whether it is defined in-line. Fix missing or mislabeled source terms before delivery.
8. In `all` or `blink` mode, run a source-purity audit over learner-facing files and a source-coverage audit against `_work/source-structure.md` and `_work/source-evidence.md`. For every `core` or `supporting` item, confirm an evidence note exists and record the exact learner-facing location for `standalone` and `merged` treatments. Reconsider every omission after drafting. Confirm that the key-idea count is source-derived, the learner-facing structure is not a chapter-by-chapter summary, each key idea has one coherent takeaway, and cross-chapter evidence is merged where it serves that takeaway.
9. In `all` or `blink` mode, run a curriculum-wide form audit. Review all key ideas side by side and ask whether each uses the form that best serves its own argument, or whether a repeated structure has appeared because it was convenient in an earlier idea. Revise forms that reflect a template rather than an independent editorial choice. Do not vary form merely for variation’s sake.
10. In `all` or `blink` mode, run a visual-integration-and-fidelity audit over every learner-facing embedded visual. Record the file, exact prose-to-visual link, caption and accompanying source-prose anchor, source-supported argument role, and both reviewers’ decisions in `_work/final-audit.md`. Repair any visual that is decorative, incomplete, poorly clipped, lacks its source label/title, depends on unstated visual interpretation, or includes an explanation inferred from the image rather than grounded in source material.
11. If a user says the summary is untrusted or broadly flawed, regenerate learner-facing files from source notes and source chunks. Do not patch the existing summary as the primary repair.
12. State any source or extraction limitations plainly.
