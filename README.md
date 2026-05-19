# AI Workbench

Reusable AI skills, prompts, workflows, scripts, and templates shared across tools and projects.

## Structure

- `skills/codex/`: Codex skills, kept in their complete skill-folder format.
- `skills/shared/`: Tool-agnostic skill references or reusable capability notes.
- `prompts/`: Reusable prompts grouped by task or domain.
- `workflows/`: Multi-step procedures that may combine prompts, skills, scripts, and external tools.
- `scripts/`: Standalone helper scripts that are not bundled inside a specific skill.
- `templates/`: Reusable output templates.

## Current skills

- `skills/codex/linkedin-extract`: Extract structured YAML from LinkedIn profile and job URLs using a user-authenticated Playwright browser.

## Local setup

```bash
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
```

## Use skills from any repo

Codex auto-discovers skills from `~/.codex/skills`. Keep the canonical skill source in this repo, then symlink it into the Codex skills directory:

```bash
mkdir -p ~/.codex/skills
ln -s /path/to/ai-workbench/skills/codex/linkedin-extract ~/.codex/skills/linkedin-extract
```

After that, Codex can use `linkedin-extract` while working from any project folder, including the career knowledge base.

If a skill is not symlinked, reference it explicitly in the prompt:

```text
Use the linkedin-extract skill at /path/to/ai-workbench/skills/codex/linkedin-extract to extract this LinkedIn profile: <url>
```
