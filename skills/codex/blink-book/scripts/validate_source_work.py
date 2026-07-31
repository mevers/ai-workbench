#!/usr/bin/env python3
"""Validate the source inventory, evidence notes, and key-idea plan for a Blink Book."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TABLE_ROW_RE = re.compile(r"^\|\s*(S\d+)\s*\|.*?\|\s*(core|supporting|context)\s*\|", re.IGNORECASE)
EVIDENCE_RE = re.compile(r"^##\s+(S\d+)\s*:", re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book_dir", type=Path, help="Blink Book output folder")
    args = parser.parse_args()
    work_dir = args.book_dir.expanduser().resolve() / "_work"
    required = ["source-index.md", "source-structure.md", "source-evidence.md", "key-idea-plan.md"]
    errors = [f"Missing _work/{name}" for name in required if not (work_dir / name).exists()]
    if errors:
        print("Source-work validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    structure = (work_dir / "source-structure.md").read_text(encoding="utf-8")
    evidence = (work_dir / "source-evidence.md").read_text(encoding="utf-8")
    plan = (work_dir / "key-idea-plan.md").read_text(encoding="utf-8")
    material_ids = {
        match.group(1): match.group(2).lower()
        for line in structure.splitlines()
        if (match := TABLE_ROW_RE.match(line))
        and match.group(2).lower() in {"core", "supporting"}
    }
    if not material_ids:
        errors.append("No core or supporting source items found in source-structure.md")

    evidence_ids = set(EVIDENCE_RE.findall(evidence))
    for item_id in sorted(material_ids, key=lambda value: int(value[1:])):
        if item_id not in evidence_ids:
            errors.append(f"{item_id}: missing evidence note in source-evidence.md")
        if not re.search(rf"\b{re.escape(item_id)}\b", plan):
            errors.append(f"{item_id}: missing treatment in key-idea-plan.md")

    if errors:
        print("Source-work validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print(
        "OK: source index, structure, evidence notes, and key-idea plan cover "
        f"{len(material_ids)} core/supporting source items."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
