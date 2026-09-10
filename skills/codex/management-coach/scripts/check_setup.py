#!/usr/bin/env python3
"""Check the local coaching setup without changing files or exposing memory content."""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


def check_setup(skill_root, memory_override=None):
    errors = []
    try:
        config = json.loads((skill_root / 'local-paths.json').read_text())
        configured_path = config['memory_root']
        if not isinstance(configured_path, str) or not configured_path.strip():
            raise ValueError('memory_root must be a non-empty string')
        configured_root = Path(configured_path).expanduser()
        if not configured_root.is_absolute():
            raise ValueError('memory_root must be absolute')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return ['Local memory configuration is missing or invalid (' + type(exc).__name__ + ').']

    memory_root = Path(memory_override).expanduser().resolve() if memory_override else configured_root
    required = {
        skill_root: ['SKILL.md', 'agents/openai.yaml', 'references/memory.md', 'references/onboarding.md'],
        memory_root: ['README.md', 'profile.md', 'sources.md', 'development.md', 'onboarding.md'],
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

    profile = contents.get(memory_root / 'profile.md', '')
    frontmatter = re.match(r'\A---\n(.*?)\n---(?:\n|$)', profile, flags=re.S)
    name = re.search(r'^coach_name:\s*([^\n]+)$', frontmatter.group(1), re.M) if frontmatter else None
    if not name or not name.group(1).strip().strip('\'"').strip():
        errors.append('Profile needs a non-empty coach_name in its frontmatter.')

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
                errors.append('Cannot inspect a text file in ' + ('skill' if root == skill_root else 'memory') + '.')
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
    parser.add_argument('--memory-root', type=Path, help='Check an isolated memory fixture instead of the configured repository.')
    args = parser.parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    errors = check_setup(skill_root, args.memory_root)
    if errors:
        for error in errors:
            print('FAIL: ' + error)
        return 1
    print('PASS: Local configuration, required readable memory, explicit invocation, links, and writing checks.')
    print('Note: This read-only check does not verify write permission, fresh-session discovery, or coaching behaviour.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
