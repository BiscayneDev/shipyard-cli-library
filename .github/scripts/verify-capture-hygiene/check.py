#!/usr/bin/env python3
"""Keep known research captures fictional. Never print matched values."""
import pathlib
import re
import subprocess
import sys

JWT = re.compile(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+')
SENSITIVE_FIELD = re.compile(r'"(?:securityToken|meetingPassword|access_token|refresh_token)"\s*:\s*"([^"\n]+)"', re.I)
SAFE = ('FICTIONAL_', 'REDACTED', '<REDACTED', '<TOKEN', 'YOUR_', 'EXAMPLE_')


def issues(text):
    if JWT.search(text):
        yield 'JWT-shaped meeting/access credential'
    for match in SENSITIVE_FIELD.finditer(text):
        if not match[1].upper().startswith(SAFE):
            yield 'non-fictional sensitive response field'


def main():
    root = pathlib.Path(__file__).resolve().parents[3]
    paths = subprocess.check_output(['git', 'ls-files', '-z', 'library'], cwd=root).decode().split('\0')
    failed = False
    for name in paths:
        if not name or not ('.manuscripts/' in name or '/docs/research/' in name):
            continue
        path = root / name
        if not path.is_file():
            continue
        # Only scan archival text formats, not executable/binary build outputs.
        if path.suffix not in ('.md', '.json', '.log', '.har', '.yaml', '.txt'):
            continue
        text = path.read_text(errors='replace')
        # Bundled public OpenAPI schemas contain field-name and token-format examples,
        # not captured responses. This gate targets live proof/discovery artifacts.
        if 'openapi' in path.name.lower():
            continue
        for reason in sorted(set(issues(text))):
            print(f'{name}: {reason}')
            failed = True
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
