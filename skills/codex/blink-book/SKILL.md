---
name: blink-book
description: Write and review clear, engaging summaries of nonfiction PDF or EPUB books, with optional assessments.
metadata:
  version: "2.0.0"
---

# Blink book

- Write for a general reader. Use simple, conversational British English.
- Tell a clear, engaging story of the book's argument. Make each key idea easy and enjoyable to follow.
- Keep the author's essential arguments, named core concepts, complete frameworks and terminology.
- Use prior knowledge to guide the structure. Use the source book to write the content.

## Choose the mode

- `all` (default): Create and review the synthesis and assessments.
- `blink-only`: Create and review the synthesis. Exclude assessments.
- `assessment`: Create and review assessments for an approved synthesis. Require its source records and leave both unchanged. Skip source preparation and synthesis creation. Run assessment reviews and final checks.
## Set time limits

- Use the user's deadline, or 30 minutes if none is given. Record the start and deadline in `_work/final-audit.md`.
- Leave time for writing, reviews, repairs and final checks.
- Keep the overview and key ideas within 45 minutes at 135 words per minute. Count assessments separately.
## Assign the work

- **Editor:** prepares the source, plans, writes, revises and delivers the work.
- **Source reviewer:** checks completeness and accuracy against the book.
- **Reader reviewer:** checks clarity, reading enjoyment and assessment usability.
- Neither reviewer reviews their own writing.
- Keep the same Source reviewer and Reader reviewer through repairs.
- Instructions without an explicit owner are for the Editor.
- Run independent work in parallel when useful.

## Check the source

- Require the complete PDF or EPUB. Check access to its text and original figures.
- Save searchable text with page or section references. Reuse verified extraction when available.
- Read relevant passages as needed. Do not load the whole book at once.

## Plan the synthesis

- State whether you have prior knowledge of the book.
- If available, use it to propose the main arguments, core concepts, frameworks and order of key ideas.
- Save `_work/prior-knowledge-proposal.md`. Label it “Unverified prior-knowledge proposal” and preserve it unchanged.
- Always identify all named central arguments, frameworks and core concepts from the source.
- Check the contents, glossary, introduction, conclusion and relevant passages.
- Verify the prior knowledge proposal against those findings. Without prior knowledge, build the plan directly from the source.
- Save `_work/key-idea-plan.md`. Record what the source confirmed, corrected or added.
- Distinguish the main ideas from supporting practices and examples. Explain these choices and give source references.
- Show how the core concepts support the book's main argument.
- List every essential framework's parts. Show where each part and core concept will be explained.
- Give each key idea a reader question and the argument that answers it.
- Order the key ideas so each prepares the reader for the next. Let the explanation determine their number.
- Assign words to the overview and each key idea within the reading limit.
- Choose examples and details that help explain the main ideas. Omit details that add little.

## Write the first drafts

- Save drafts in `_work/drafts/`. Start with the overview and first key idea.
- Reread the relevant source passages before writing each draft.
- Explain what happens, why it happens and why it matters. Use the book's examples and evidence.
- Build one argument through each key idea. Make each paragraph develop the previous one.
- Explain connections clearly. Do not make the reader guess what a sentence refers to.
- Introduce essential source terms in bold and explain them plainly.
- Explain every framework's parts and how they work together.
- Say whose findings or experience support important claims. Keep qualifications that affect their meaning.
- Never invent examples, dialogue, motives, outcomes or claims in the synthesis.
- Use the overview to explain the central argument and connect the core concepts. Bold those concepts.
- Include original source figures only when they help explain an idea. Inspect and explain relevant labels, symbols and relationships nearby.

## Review the design and opening

- The Source reviewer checks the book's essential concepts before reading the plan. The Source reviewer compares that coverage with the plan and opening drafts.
- Give the Reader reviewer only the draft overview, first key idea and included figures. Withhold the plan, source notes and writer explanations.
- The Reader reviewer records confusion on first reading, before trying to infer the intended meaning.
- The Reader reviewer rejects dense explanations, unexplained connections and lists of terms that interrupt the argument.
- The Reader reviewer compares clarity and pace with user-approved writing when available. The Editor must not copy its content or structure.
- Save the Source reviewer's and Reader reviewer's findings in `_work/final-audit.md`. Fix coverage and reading problems before drafting the remaining ideas.

## Complete the synthesis

- The Editor drafts the remaining key ideas using the writing rules above.
- The Editor keeps these drafts in `_work/drafts/`.
- The Editor edits the overview and key ideas into one connected explanation.
- The Editor removes repetition and unnecessary details to meet the reading limit.
- The Editor preserves necessary reasoning and complete frameworks.

## Review the completed synthesis

- The Source reviewer and Reader reviewer begin after the Editor completes the synthesis.
- The Source reviewer checks that the synthesis explains the book’s central concepts.
- The Source reviewer checks each explanation and figure against the book.
- The Source reviewer checks terms, examples, claims and qualifications.
- The Editor gives the Reader reviewer only the completed synthesis and included figures.
- The Reader reviewer reads the overview and key ideas in order.
- The Reader reviewer records unclear passages and breaks in the argument.
- The Reader reviewer checks that the prose is clear and enjoyable on first reading.
- The Reader reviewer rejects passages that require reconstructing the intended meaning.
- The Source reviewer and Reader reviewer record their findings in `_work/final-audit.md`.

## Repair and approve the synthesis

- The Editor rewrites failed explanations as whole units.
- The Source reviewer and Reader reviewer recheck repairs and affected connections.
- The Source reviewer and Reader reviewer retain approvals for unchanged work.
- The Editor repeats the repair step if a review identifies remaining failures.
- The Editor verifies the reading time before release.
- The Editor releases the synthesis only when the Source reviewer and Reader reviewer approve and the reading limit is met.

## Create assessments

- Follow the [assessment template](references/assessment-template.md) for every comprehension check and end-of-book review.
- Use the user's application context unchanged. Ask if it is missing; use generic recap only when requested.
- In `all` mode, start assessments alongside stable key ideas when useful. Check them against the final synthesis.
- Save `_work/assessment-plan.md`. Record what each item tests, source references, context assumptions and reasons for the answers.
- Give each key idea a book-only Quick recall question and an Apply question.
- Use Deeper comprehension instead of Apply when practical application does not fit.
- Add Try this for contextual application. Use When, Do and Why now to state the situation, task and useful result.
- Label invented assessment scenarios as hypothetical. Keep them consistent with the context and include all facts needed to answer.
- Do not assume private motives. Ask for a clear action or judgement.
- Use four plausible options and one best answer by default. Make wrong answers reflect likely misunderstandings.
- Hide answers in `<details>` blocks. Briefly explain the correct answer and why the strongest alternative is wrong.
- Do not add missing scenario facts in the feedback.
- Finish with new review questions covering the main ideas.
- Compare each key idea's concepts with those in all other available Blinks.
- Include Related ideas and further reading in every comprehension check.
- Select relevant links allowed by the context. Explain each connection. Check the linked text and path.

## Review the assessments

- The Reader reviewer checks that the assessments follow the required template.
- The Source reviewer checks every question, answer, explanation and exercise against the synthesis, source passages and application context.
- Give the Reader reviewer questions with the answer blocks removed. Withhold the assessment plan and writer explanations.
- The Reader reviewer saves choices, confusion and clues that give away answers before seeing the feedback.
- The Reader reviewer checks that each question supports one best answer. The Reader reviewer checks that Try this gives usable instructions.
- The Editor then shows the feedback. The Reader reviewer checks its explanation.
- Save the Source reviewer's and Reader reviewer's findings in `_work/final-audit.md`. Rewrite failed questions or exercises as whole units.
- The Source reviewer and Reader reviewer recheck repairs. The Reader reviewer tests changed questions again before seeing the answers.
- Approve only when the answers are supported, choices are credible and instructions are usable.

## Save and check the output

- Store each Blink in `books/<book-slug>/`.
- Keep `overview.md`, `key-idea-NN.md` and `metadata.yaml` in the book folder.
- Keep only the raw source PDF or EPUB in `source/`.
- Store original source visuals in `visuals/`.
- Store the visual inventory in `visuals/inventory.md`.
- Store extraction, plans, drafts and review records in `_work/`.
- Format key ideas using [the key-idea template](references/key-idea-template.md).
- Put assessments in `quizzes/key-idea-NN-comprehension.md` and `review.md`. Link key ideas to their quizzes in `all` mode.
- Link new overviews to all included reader sections and any visual inventory.
- Record title, author, source type, idea count, reading minutes, date, language and skill version in metadata.
- Show reading time and skill version in the overview.
- Check folder placement, required files, links, image paths, answer keys and reading time.
- Record reviewer identities, review rounds, repairs, final decisions and approved-file hashes in `_work/final-audit.md`.
- Record elapsed time and limitations there too. Report unresolved failures honestly; do not claim approval for incomplete work.
