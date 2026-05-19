# Playwright Access For LinkedIn

Use Playwright for LinkedIn URL access. Treat direct HTTP requests, generic browser fetches, and static HTML assumptions as unreliable for LinkedIn because they often hit bot blocking, auth walls, incomplete markup, or dynamic content gaps.

## Setup

Use the bundled helper:

```bash
python3 skills/codex/linkedin-extract/scripts/linkedin_playwright.py --help
```

If Playwright is missing:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

The helper stores the authenticated browser profile outside the repo by default:

```text
~/.codex/browser-profiles/linkedin
```

Do not commit browser profiles, cookies, screenshots, or captured LinkedIn text unless the user explicitly asks.

## Authenticate

Open a headed Playwright-owned Chromium profile:

```bash
python3 skills/codex/linkedin-extract/scripts/linkedin_playwright.py auth
```

The user must authenticate inside the browser window. Do not ask for, paste, log, store, or automate the user's LinkedIn credentials. After authentication succeeds, the profile directory contains the session state for future Playwright runs.

If the browser cannot open from Codex because GUI access requires approval, ask for approval to run the command outside the sandbox. If the user prefers to run it directly, provide the command and wait for them to confirm the browser profile is authenticated.

## Capture A Page

Capture one or more LinkedIn profile or job URLs:

```bash
python3 skills/codex/linkedin-extract/scripts/linkedin_playwright.py snapshot "https://www.linkedin.com/jobs/view/..." "https://www.linkedin.com/in/..."
```

The helper automatically clicks visible "See more", "Show more", "Show all", and "See all" controls that behave like in-page buttons. For profile pages, it also captures read-only linked `/details/` pages so "Show all" sections such as experience, education, skills, projects, or licences can be extracted from their full pages. It must not capture edit forms or recent activity pages as profile detail sources.

The helper saves:

- visible page text as `.txt`
- a full-page screenshot as `.png`

Extract from the `.txt` and use the screenshot only for visual checks.

## Access Rules

- Use only user-requested URLs. Do not build bulk scraping, crawling, stealth, anti-detection, CAPTCHA bypass, credential replay, or rate-limit evasion.
- Respect login, permission, and visibility boundaries. If LinkedIn blocks access or asks for additional verification, stop and ask the user to complete it in the headed browser.
- Keep the browser headed for authentication and capture.
- Extract only profile/job content visible to the signed-in user. If the required page content is hidden, unavailable, truncated, or gated, stop and ask the user to fix the browser session or page state before extraction.
