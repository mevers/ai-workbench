#!/usr/bin/env python3
"""Capture LinkedIn pages with a user-authenticated Playwright browser."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


PROFILE_DIR = Path("~/.codex/browser-profiles/linkedin").expanduser()
OUTPUT_DIR = Path("linkedin-snapshots")
EXPAND_LABELS = ("see more", "show more", "show all", "see all", "… more", "... more")
DETAIL_SECTIONS = {
    "certifications",
    "courses",
    "education",
    "experience",
    "honors",
    "languages",
    "projects",
    "publications",
    "recommendations",
    "skills",
    "volunteering-experiences",
}


def slug(url: str) -> str:
    parsed = urlparse(url)
    value = f"{parsed.netloc}{parsed.path}" if parsed.netloc else url
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "linkedin-page"


def browser(playwright):
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    return playwright.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        headless=False,
        viewport={"width": 1440, "height": 1200},
    )


def auth(_: argparse.Namespace) -> None:
    print(f"Using Playwright profile: {PROFILE_DIR}")
    print("Log in to LinkedIn in the browser window. Do not share your password with Codex.")
    with sync_playwright() as playwright:
        context = browser(playwright)
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
        input("Press Enter here after LinkedIn has loaded successfully...")
        context.close()
    print("Authentication browser profile saved.")


def expand_page(page) -> None:
    page.evaluate("window.scrollTo(0, 0)")
    for _ in range(80):
        clicked = page.evaluate(
            """
            (labels) => {
              const visible = (el) => {
                const rect = el.getBoundingClientRect();
                const style = getComputedStyle(el);
                return rect.width && rect.height && style.display !== 'none' && style.visibility !== 'hidden';
              };
              for (const el of document.querySelectorAll('button, [role="button"]')) {
                const text = [el.innerText, el.ariaLabel, el.title].filter(Boolean).join(' ').toLowerCase();
                if (visible(el) && labels.some((label) => text.includes(label)) && !text.includes('show less')) {
                  el.click();
                  return true;
                }
              }
              return false;
            }
            """,
            list(EXPAND_LABELS),
        )
        if clicked:
            page.wait_for_timeout(500)
            continue

        at_bottom = page.evaluate("window.scrollY + window.innerHeight >= document.body.scrollHeight - 8")
        if at_bottom:
            break
        page.evaluate("window.scrollBy(0, window.innerHeight * 0.85)")
        page.wait_for_timeout(300)


def detail_links(page) -> list[str]:
    return page.evaluate(
        """
        (sections) => [...new Set([...document.querySelectorAll('a[href]')].flatMap((a) => {
          const url = new URL(a.getAttribute('href'), location.href);
          const match = url.pathname.match(/^\\/in\\/[^/]+\\/details\\/([^/]+)\\/?$/);
          return match && sections.includes(match[1]) ? [url.href] : [];
        }))]
        """,
        list(DETAIL_SECTIONS),
    )


def save(page, url: str, output_dir: Path) -> None:
    name = slug(url)
    text_path = output_dir / f"{name}.txt"
    image_path = output_dir / f"{name}.png"
    text_path.write_text(page.locator("body").inner_text(timeout=60_000), encoding="utf-8")
    page.screenshot(path=str(image_path), full_page=True)
    print(f"Saved text: {text_path}")
    print(f"Saved screenshot: {image_path}")


def snapshot(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        context = browser(playwright)
        page = context.pages[0] if context.pages else context.new_page()
        queue = list(args.urls)
        seed_urls = set(queue)
        seen = set()

        while queue:
            url = queue.pop(0)
            if url in seen:
                continue
            seen.add(url)

            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            expand_page(page)

            if url in seed_urls:
                queue.extend(link for link in detail_links(page) if link not in seen and link not in queue)

            save(page, url, output_dir)

        context.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("auth").set_defaults(func=auth)

    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.add_argument("urls", nargs="+")
    snapshot_parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    snapshot_parser.set_defaults(func=snapshot)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
