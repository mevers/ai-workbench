---
name: comment-python-code
description: Add concise comments to explicit Python files or snippets without using docstrings. Use when Codex is asked to add comments, documentation, explanations, or annotations to Python files, Python snippets, functions, classes, methods, scripts, modules, or code blocks.
---

# Comment Python code

## Scope rule

Always target explicit Python files or pasted Python snippets.

Treat named files, pasted snippets, explicit globs, and explicit directories as valid targets.

If the user asks to add comments or documentation without naming a file, file set, pasted snippet, explicit glob, or explicit directory, ask which file or files to comment before making changes.

For pasted snippets, return the edited snippet unless the user identifies a file to update.

Do not search the repository and choose targets unless the user explicitly asks you to find candidate files.

## Code preservation

Do not change executable code. Do not reformat, rename, reorder imports, adjust logic, change type hints, or run formatters.

Edit only `#` comments unless the user explicitly asks for code changes.

Do not add, remove, or convert docstrings unless the user explicitly asks.

## Commenting rules

Add only `#` comments. Do not add docstrings.

Keep comments minimal:

- Prefer one-line comments.
- Use two lines only when one line would be unclear.
- Comment critical logic steps, non-obvious business rules, important transformations, and decisions that affect behaviour.
- Do not restate syntax, variable names, or obvious control flow.
- Do not add broad defensive commentary about hypothetical cases unless the code already handles them.

Place a one-line comment immediately above every `def` and `async def`. For methods, explain the method's role in the surrounding class or workflow.

For decorated functions, place the function comment immediately above the first decorator.

## Editing workflow

Read the surrounding code before commenting so the comment describes the code's actual purpose.

Keep existing useful comments. Remove or tighten comments only when they are misleading, redundant, or conflict with these rules.

After editing a file, scan the diff and verify:

- Every `def` and `async def` has a one-line `#` comment immediately above it.
- No docstrings were added.
- Comments explain why or what the critical step achieves, not how Python syntax works.
- No comment is longer than two lines.
- No executable code changed.

After commenting, briefly mention any functions that were hard to comment because they are extremely small or only wrap a single expression. Do not refactor or suggest replacements unless the user asks.
