"""Check setup failures and confirm that the checker does not change files."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from check_setup import check_setup


def test_setup():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        skill, records = root / 'skill', root / 'records'
        for folder in (skill / 'references', skill / 'agents', records):
            folder.mkdir(parents=True)
        for name in ('SKILL.md', 'references/records.md', 'references/onboarding.md'):
            (skill / name).write_text('# Instructions\n')
        (skill / 'agents/openai.yaml').write_text(
            'interface:\n  default_prompt: Use $management-coach\n'
            'policy:\n  allow_implicit_invocation: false\n'
        )
        config = skill / 'local-paths.json'
        assert check_setup(skill), 'Missing configuration must fail.'
        for value in (None, '', 'relative', '/bad\0path'):
            config.write_text(json.dumps({'coaching_records_folder': value}))
            assert check_setup(skill), 'Invalid paths must fail.'
        config.write_text(json.dumps({'coaching_records_folder': str(records)}))
        assert not check_setup(skill), 'An empty records folder must be valid.'
        records.rmdir()
        assert check_setup(skill), 'A missing records folder must fail.'
        assert not records.exists(), 'The checker must not create the folder.'
        records.mkdir()
        with patch.object(Path, 'iterdir', side_effect=PermissionError):
            assert check_setup(skill), 'An inaccessible folder must fail.'
        profile = records / 'profile.md'
        profile.write_bytes(b'\xff')
        assert check_setup(skill), 'An unreadable record must fail.'
        profile.write_text('[Source](missing.md)\n')
        assert check_setup(skill), 'A broken link must fail.'
        profile.write_text('# Background\n')
        before = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
        assert not check_setup(skill), 'A partial profile must be valid.'
        after = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
        assert before == after, 'The checker must not change files.'
        (skill / 'references/records.md').unlink()
        assert check_setup(skill), 'Missing skill instructions must fail.'


if __name__ == '__main__':
    test_setup()
    print('PASS: Configuration, folder access, optional records, links, and no file changes.')
