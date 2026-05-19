---
name: linkedin-extract
description: Extract structured data or raw content from LinkedIn profiles and LinkedIn job posts. Use when the user explicitly asks to extract, get, fetch, capture, parse, structure, or normalise content from one or more LinkedIn profile or job URLs. Use Playwright with a user-authenticated browser profile for all LinkedIn access.
---

# LinkedIn Extract

## Core Workflow

1. Accept only one or more LinkedIn URLs as source input. If the user provides pasted content, screenshots, PDFs, exports, or non-LinkedIn URLs, ask for the relevant LinkedIn URL instead.
2. Capture each URL with Playwright using the user's authenticated browser profile. If authentication is not set up, follow [references/playwright-access.md](references/playwright-access.md).
3. If LinkedIn blocks access or asks for additional verification, stop and ask the user to complete access in the Playwright browser. Do not bypass access controls.
4. Extract only visible page content into structured YAML. Do not infer values that are not present on the captured page.
5. Record source URLs and any schema fields not present in the captured content.

For schemas and field definitions, read [references/extraction-schemas.md](references/extraction-schemas.md).
For LinkedIn URL setup and capture, read [references/playwright-access.md](references/playwright-access.md).

## Source Handling

- Treat LinkedIn pages as unstable sources. Prefer Playwright-rendered visible text and semantic page labels over brittle DOM selectors.
- Capture only content visible to the signed-in user in the Playwright browser.
- When duplicate sections appear, prefer the most complete visible version and mention duplicates in notes.
- For profile experience, preserve each role as a structured object. Include role descriptions, visible skill tags, nested company-group roles, dates, durations, locations, and employment type when present. Do not collapse experience into a title-only list.
- Keep original wording for names, titles, companies, locations, dates, compensation, and qualifications unless normalising into a separate field.
- Use British English in all generated documents, field names, notes, and extracted content.
- Do not review, score, compare, rank, critique, or suggest improvements. If the user asks for those tasks, first complete extraction, then treat review or advice as a separate downstream process.

## Privacy And Compliance

- Extract only from LinkedIn URLs the user provides and content visible through the user's authenticated Playwright browser.
- Do not infer or classify sensitive attributes such as age, race, religion, health, political views, union membership, sexual orientation, or disability.
- Do not create tooling for bulk scraping, stealth automation, credential use, CAPTCHA bypass, or evasion of LinkedIn restrictions.
- Use Playwright only with an authenticated profile owned by the user. Do not ask for credentials, automate login forms, or export cookies into the repo.
- If contact details are present, include them only when the user asked for contact extraction.

## Output Patterns

Return structured YAML.

For extraction tasks, provide:

- `source_type`
- `source_url`
- `extracted_content` or `extracted_fields`
- `not_present`
- `notes`
