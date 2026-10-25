#!/usr/bin/env python3
"""Check the local coaching setup without changing files or exposing coaching content."""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


def check_setup(skill_root, records_override=None):
    errors = []
    try:
        config = json.loads((skill_root / 'local-paths.json').read_text())
        configured_path = config['coaching_records_folder']
        if not isinstance(configured_path, str) or not configured_path.strip() or '\0' in configured_path:
            raise ValueError('coaching_records_folder must be a non-empty string')
        configured_root = Path(configured_path).expanduser()
        if not configured_root.is_absolute():
            raise ValueError('coaching_records_folder must be absolute')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return ['Coaching records configuration is missing or invalid (' + type(exc).__name__ + ').']

    records_root = Path(records_override).expanduser().resolve() if records_override else configured_root
    try:
        list(records_root.iterdir())
    except (OSError, ValueError):
        return ['Cannot read the coaching records folder. Confirm its location and access.']

    required = {
        skill_root: ['SKILL.md', 'agents/openai.yaml', 'references/records.md', 'references/onboarding.md'],
        records_root: [],
    }
    contents = {}
    for root, filenames in required.items():
        for filename in filenames:
            path = root / filename
            try:
                contents[path] = path.read_text(encoding='utf-8')
                if not contents[path].strip():
                    errors.append('Required file is empty: ' + filename)
            except (OSError, UnicodeError):
                errors.append('Required file is missing or unreadable: ' + filename)

    metadata = contents.get(skill_root / 'agents/openai.yaml', '')
    if not re.search(r'^\s+allow_implicit_invocation:\s*false\s*$', metadata, re.M):
        errors.append('Explicit-only invocation policy is missing.')
    if '$management-coach' not in metadata:
        errors.append('UI starter prompt needs the stable skill invocation.')

    for root in required:
        for path in root.rglob('*'):
            if '.git' in path.relative_to(root).parts or path.suffix not in {'.md', '.yaml', '.json', '.py'}:
                continue
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding='utf-8')
            except (OSError, UnicodeError):
                errors.append('Cannot inspect a text file in ' + ('skill' if root == skill_root else 'records') + '.')
                continue
            if chr(0x2014) in content:
                errors.append('Em dash found in: ' + str(path.relative_to(root)))
            if path.suffix != '.md':
                continue
            for target in re.findall(r'\[[^\]]+\]\(([^\s)]+)\)', content):
                if target.startswith(('#', 'https://', 'http://', 'mailto:')):
                    continue
                destination = unquote(target.split('#', 1)[0])
                if destination and not (path.parent / destination).exists():
                    errors.append('Broken local link in: ' + str(path.relative_to(root)))

    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records-folder', '--memory-root', dest='records_folder', type=Path,
                        help='Check a test records folder instead of the configured folder.')
    args = parser.parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    errors = check_setup(skill_root, args.records_folder)
    if errors:
        for error in errors:
            print('FAIL: ' + error)
        return 1
    print('PASS: Configuration, records access, explicit invocation, links, and writing checks.')
    print('Note: This read-only check does not verify write permission, fresh-session discovery, or coaching behaviour.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
