---
name: blink-book
description: Create a readable, source-faithful Blink Book from one nonfiction PDF or EPUB. Use for full Blinks, summaries, or assessments of existing Blinks.
metadata:
  version: "2.0.0"
---

# Blink Book

- Teach the book's essential argument through a compelling, readable synthesis.
- Preserve core concepts, complete frameworks and the author's terminology.
- Prefer understanding over brevity.

## Choose the mode

- **all** (default): Generate and review both the synthesis and its assessments.
- **blink-only**: Generate and review the synthesis, including source work, overview, key ideas and original visuals. Exclude assessment generation and assessment reviews.
- **assessment**: Generate and review assessments only. Require existing approved synthesis files and their source work. Do not edit the synthesis files and their source work.

## Plan timing

- Record the creation start and deadline before work.
- Reserve time for the generation, reviews and repairs required by the selected mode.
- Read [Timing and release checks](references/output-templates.md#release-checks).
- Treat 45 minutes at 135 words per minute as an editorial reading target. Keep longer explanations when they improve understanding.

## Establish the source

- Require the complete PDF or EPUB source.
- Verify access to its text and original figures. Reuse verified extraction from that file.
- Read bounded passages. Never load the whole book at once.
- For synthesis generation, follow [Summary workflow](references/summary-workflow.md) for source preparation and retained records.

## Design with knowledge, write from source

- Before synthesis design, state whether internal knowledge of this book is available.
- If prior knowledge is available:
  - Use available knowledge to propose the central arguments, core concepts, frameworks and key-idea structure.
  - Based on available knowledge, state which ideas deserve most emphasis and why.
  - Save this in `_work/prior-knowledge-proposal.md`, labelled “Unverified prior-knowledge proposal”.
  - Verify the proposal against the source. Record corrections without overwriting the original proposal.
  - Create `_work/key-idea-plan.md` from the verified findings.
- If prior knowledge is unavailable or too uncertain:
  - Alert the user.
  - Identify the central arguments, core concepts, frameworks and structure directly from the source.
  - Create `_work/key-idea-plan.md` from those findings.
- Group related concepts around one central point per key idea. Split groups that require separate explanations.
- Set the number of key ideas from these groups. Do not use a fixed quota.
- Order key ideas so readers learn the concepts needed to understand each subsequent idea.
- Write every explanation and paraphrase from source passages. Never write book content from memory.

## Develop the synthesis

- State each key idea's central point in its title.
- Build a compelling narrative within each key idea and across key ideas.
- Explain causes and consequences using examples from the book. Do not invent scenarios, details or dialogue.
- For important claims, explain whose findings or experience support them and when they apply.
- Explain every essential framework's parts and relationships. Naming its parts is insufficient.
- Make the overview explain the central argument and connect the core concepts.
- Never invent examples or supporting concepts that are not grounded in the source material.
- Retain a fuller draft. Improve organisation without removing necessary reasoning.

## Language and presentation

- Use plain British English. Complete the plain-language and non-template prose pass.
- Preserve the author's terminology. Introduce important terms in bold and explain them plainly.
- Bold the core concepts in the overview.
- Use original source images only. Explain relevant labels, symbols and relationships nearby.
- Follow [Output templates](references/output-templates.md) for files and formatting.

## Create assessments

- Follow [Assessment workflow](references/assessment-workflow.md) when assessments are in scope.
- Reuse the user's application context unchanged. Use generic recap when requested.
- Ask only for missing or materially ambiguous context. Never create or edit it.
- Use recognisable situations, clear actions and credible answer choices. Use recap when useful application does not fit.

## Produce and review

- For synthesis, use parallel authors for independent key-idea groups. Keep one editor responsible for whole-book coherence.
- In all mode, draft assessments alongside stable key ideas. Check final alignment with the approved synthesis.
- Use independent source and learner reviewers. Nobody approves their own writing.
- For synthesis, review the design before drafting. For each selected mode, review the complete content and verify repairs.
- For synthesis, follow [Summary review](references/summary-review.md). For assessments, follow [Assessment review](references/assessment-review.md).
- Judge what the text explains. Do not supply missing meaning from familiarity.
- Withhold whole-Blink approval if an essential concept or framework is missing.
- Repair affected explanations or assessment items as complete units. Never micro-adjust.

## Deliver

- Meet the user's deadline for the selected mode, including reviews and validation.
- Deliver the complete, approved output for the selected mode. Report any unresolved failure honestly.
- Run the [release checks](references/output-templates.md#release-checks). Automated checks do not establish content quality.
- Record this version in new summaries. Record timing, limitations and review outcomes in `_work/final-audit.md`.
