#!/usr/bin/env python3
"""Exercise the learner-quality validator's bounded-review invariants."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR = SCRIPT_DIR / "validate_learner_quality.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def review_text(kind: str, learner: Path) -> str:
    extra = (
        "## Plain-language and style\n\nThe central explanation is materially clear on a first read.\n"
        if kind == "source-blind"
        else "## Independent coverage baseline\n\nThe source thesis, framework, evidence provenance, and limits are covered.\n\n"
        "## Source terminology and fidelity\n\nNamed terms and central claims match the source.\n"
    )
    return f"""# {kind.title()} review

**Review wave:** 1
**Learner file SHA-256:** {sha256(learner)}

## Review conditions

The reviewer followed the required {kind} conditions.

## Reader reconstruction

The reader can reconstruct the central conclusion, mechanism, and implication.

{extra}
## Blockers

None.

## Advisories

None.

## Gate decision

Decision: PASS
"""


def create_book(root: Path) -> Path:
    book = root / "fixture-book"
    draft_dir = book / "_work" / "key-idea-drafts"
    review_dir = book / "_work" / "final-reviews"
    draft_dir.mkdir(parents=True)
    review_dir.mkdir(parents=True)

    overview = book / "overview.md"
    idea = book / "key-idea-01.md"
    overview.write_text("# Fixture\n\nThe book explains how evidence supports a sound decision.\n", encoding="utf-8")
    idea.write_text(
        "# Evidence should support the decision\n\nA conclusion should follow from the evidence cited for it.\n\n"
        "## Source basis\n\nFixture source.\n",
        encoding="utf-8",
    )
    (draft_dir / "key-idea-01-full-draft.md").write_text("Fuller fixture draft.\n", encoding="utf-8")

    for kind in ("source-blind", "source-aware"):
        (review_dir / f"overview-{kind}-review.md").write_text(
            review_text(kind, overview), encoding="utf-8"
        )
        (draft_dir / f"key-idea-01-{kind}-review.md").write_text(
            review_text(kind, idea), encoding="utf-8"
        )
    return book


def run(book: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(book)],
        check=False,
        capture_output=True,
        text=True,
    )


def require_failure(result: subprocess.CompletedProcess[str], message: str) -> None:
    if result.returncode == 0 or message not in result.stdout:
        raise AssertionError(f"Expected failure containing {message!r}:\n{result.stdout}\n{result.stderr}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="blink-learner-quality-test-") as temp:
        root = Path(temp)
        book = create_book(root / "valid")
        if (result := run(book)).returncode:
            raise AssertionError(f"Positive case failed:\n{result.stdout}\n{result.stderr}")

        case = root / "pass-with-advisory"
        shutil.copytree(book, case)
        review = case / "_work" / "final-reviews" / "overview-source-aware-review.md"
        review.write_text(
            review.read_text().replace(
                "## Advisories\n\nNone.",
                "## Advisories\n\nADVISORY: One optional sentence could be shorter.",
            ),
            encoding="utf-8",
        )
        if (result := run(case)).returncode:
            raise AssertionError(f"PASS with an advisory should remain valid:\n{result.stdout}\n{result.stderr}")

        case = root / "invalid-wave"
        shutil.copytree(book, case)
        review = case / "_work" / "final-reviews" / "overview-source-aware-review.md"
        review.write_text(review.read_text().replace("**Review wave:** 1", "**Review wave:** 4"), encoding="utf-8")
        require_failure(run(case), "Review wave must be 1, 2, or 3")

        case = root / "pass-with-blocker"
        shutil.copytree(book, case)
        review = case / "_work" / "final-reviews" / "overview-source-aware-review.md"
        review.write_text(
            review.read_text().replace(
                "## Blockers\n\nNone.",
                "## Blockers\n\nBLOCKER: An indispensable framework is missing.",
            ),
            encoding="utf-8",
        )
        require_failure(run(case), "PASS review must record `None.` under Blockers")

    print("OK: learner-quality validator tests pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
