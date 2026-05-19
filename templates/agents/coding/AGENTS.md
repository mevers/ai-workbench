# Global guidance

## How you should behave

1. Don't assume. Don't hide confusion. Surface tradeoffs.
2. Minimum code that solves the problem. Nothing speculative.
3. Touch only what you must. Clean up only your own mess unless explicitly instructed.
4. Define success criteria. Loop until verified.

## Defensive code policy

Avoid defensive code generation by default. Do not add defensive code for impossible states unless the user asks for it or the repository proves the state can occur. In this project, "safe" code is code that matches the known business rules, not code that guards every hypothetical failure mode.

- Do not add `None` checks, fallback field names, broad `try`/`except`, missing-file checks, retries, compatibility wrappers, or permissive parsing unless they are requested or supported by evidence.
- If a schema or invariant is stated as guaranteed, write code that relies on it.
- If you think an invariant might be false, verify it against the code or data before proposing guards.
- If verification is not possible, you must ask rather than coding around imagined uncertainty.
- Prefer failing clearly over silently skipping, defaulting, or inventing data when a guaranteed invariant is violated.

### Example of good generated code

```python
def load_suburbs(csv_path: Path, state: str) -> list[str]:
    suburbs = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            division = row.get("division")
            row_state = row.get("state")
            postcode = row.get("postcode")
            suburbs.append(f"{division.strip()}, {row_state}, {postcode.strip()}")
    return sorted(set(suburbs))
```

- Minimal code
- Trusts the schema described in the task
- Does not add missing-data handling unless it is requested or evidenced

### Example of bad generated code

```python
def load_suburbs(csv_path: Path, state: str) -> list[str]:
    suburbs = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            division = row.get("division") or row.get("Division") or row.get("name")
            row_state = row.get("state") or row.get("state_abbreviation") or row.get("State")
            if not division:
                continue
            if row_state and row_state.strip().upper() != state:
                continue
            suburbs.append(f"{division.strip()}, {row_state}")
    return sorted(set(suburbs))
```

- Guesses alternative field names without evidence
- Assumes missing data needs handling without being asked

## Implementation discipline

- Do not add fallbacks, validation, retries, or configurability unless requested or supported by evidence in the codebase.
- Do not make code more defensive just because an input is technically nullable in Python. First establish whether it is nullable in the business model.
- Prefer the existing local pattern over introducing a new abstraction.
- Change the smallest surface area that fully solves the request.

## Command line conventions

- Use `python3`, never `python`.
- Prefer `rg` and `rg --files` for searching.
- Check a Python file with `python3 -m ruff check path/to/file.py` and `npx pyright path/to/file.py`.

## The language you should use

- British English everywhere.
- In document titles and headings, use sentence case. That is, capitalise only the first word in the title, the first word in a subheading after a colon, and any proper nouns or other terms that are always capitalised a certain way.
