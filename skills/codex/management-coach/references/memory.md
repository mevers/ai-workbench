# Memory protocol

## Purpose and locations

The dedicated memory repository provides continuity across Codex conversations and working repositories. Its files are human-readable and editable. Keep the smallest useful record, not a transcript or a second copy of the work second brain.

- `README.md`: navigation and current context/session links.
- `profile.md`: editable coach name, communication preferences, user background, and stable context.
- `sources.md`: canonical repository paths, relevant entrypoints, access status, and source roles.
- `context/`: dated company and role understanding with sources and unresolved questions.
- `development.md`: goals, agreed commitments, experiments, possible patterns, and review outcomes.
- `onboarding.md`: what has been learned and what remains useful to explore.
- `sessions/`: concise dated coaching notes. Create files as useful; do not scaffold empty people or case files.

The current repository is a possible source of relevant material, not the default memory destination. Company records remain in their own repositories; memory can link to them and preserve a small amount of essential context with provenance.

## Updating memory

Automatic local updates are authorised while coaching is active. Do not repeatedly ask permission to record stated goals, meaningful new context, explicit decisions, or agreed follow-ups. After the relevant exchange, save before returning the response and briefly identify the change, usually in one sentence with a link. Do not record every conversational detail.

Read each target immediately before editing. Preserve user edits and unrelated entries. Use targeted edits rather than regenerating a whole profile or journal. Use a distinct session filename such as `YYYY-MM-DD-HHMMSS-topic.md`, with a suffix if it already exists. Update the same session note during that conversation and link it from the index. Keep parallel conversations in separate session files. If overlapping edits to a shared summary are detected, reread and reconcile them; never blindly overwrite the other changes. A file-based system does not provide transactional multi-session writes.

Record the actual date of the exchange, and an event date separately if it is known. Do not infer when an undated source or screenshot was created. Group entries by source and date when this avoids repetitive metadata. Make clear whether an entry is:

- A user statement or report, including the user's own uncertainty.
- A source-document claim, with a path, section or stable ID, and inspection date.
- A coach hypothesis, with supporting observations and what would change the interpretation.
- A proposal, agreed decision, commitment, or observed outcome.

Do not upgrade a proposal into a commitment, a reported plan into a completed change, or a plausible explanation into a fact. Avoid unnecessary personal details about third parties. Do not write raw transcripts, full career documents, or extensive source excerpts by default.

Reopen modified files and verify that the intended update was saved, links resolve where accessible, and no em dashes were introduced. If saving fails, state what remains unsaved and why. Do not make a fallback copy in an unrelated repository. Follow the runtime permission workflow where necessary without treating existing user authorisation as absent.

## Corrections, ageing, and retrieval

The user's corrections and direct file edits are authoritative about their preferences and their intended records. Update current summaries promptly and mark material earlier interpretations as superseded, linking the correction. Do not repeat an old interpretation as a current truth merely because it remains in a historical note. Do not silently replace conflicting reported facts when clarification would change advice; preserve the uncertainty and ask one question.

Read current summaries before historical notes. Check the relevant live work sources before giving advice based on changing organisational facts. A newer document may cover a different scope; dates alone do not reconcile differences. Never assume a planned change happened because its target date passed.

Consolidate repetitive notes when they impair retrieval: keep the current understanding concise and link to the supporting history. Do not repeatedly reimport details the user deliberately removed. If asked to forget something, remove it from active files and relevant session notes in the authorised scope. Do not claim removal from Git history, remote copies, or platform conversation history; discuss those separately if relevant to the request.

## Source boundaries and repository operations

Keep private coaching information in this repository. Do not copy it into the reusable skill, unrelated repositories, public searches, commits to another repo, or externally shared documents. Read the work second brain as needed; COG operations are a distinct user-directed workflow. No cloud memory service, database, embeddings, background task, external message, Git commit, remote creation, or push is part of an automatic memory update.

Local Git history can be used when the user requests commits. A local repository with no remote is the initial setup; it is not a claim of encryption or access control. Runtime permissions still govern access from another workspace. Do not edit global sandbox or approval settings to make memory work.
