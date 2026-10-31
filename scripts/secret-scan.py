#!/usr/bin/env python3
"""Secret scanner for the shared workspace.

Usage:
  git diff --cached -U0 | secret-scan.py --diff     # scan added lines of a diff
  git log -p --all      | secret-scan.py --diff     # scan a whole history
  secret-scan.py --files PATH...                    # scan files or folders

Prints "path:line: <kind>" for every hit (never the value) and exits 1 if
anything was found, 0 if clean.
"""
import os
import re
import sys

B = r'(?<![A-Za-z0-9_])'  # left boundary, so "risk-first" never matches "sk-"
PATTERNS = [
    ('openai/anthropic key', B + r'sk-(?:ant-|proj-|live-)?[A-Za-z0-9_\-]{20,}'),
    ('github token', B + r'(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}'),
    ('github pat', B + r'github_pat_[A-Za-z0-9_]{30,}'),
    ('aws key', B + r'AKIA[0-9A-Z]{16}'),
    ('google key', B + r'AIza[0-9A-Za-z_\-]{35}'),
    ('slack token', B + r'xox[abposr]-[A-Za-z0-9\-]{10,}'),
    ('bearer token', r'Bearer\s+[A-Za-z0-9._~+/\-]{20,}'),
    ('jwt', B + r'eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}'),
    ('private key', r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
    ('tavily key', B + r'tvly-[A-Za-z0-9]{20,}'),
    ('huggingface token', B + r'hf_[A-Za-z0-9]{30,}'),
    ('replicate token', B + r'r8_[A-Za-z0-9]{30,}'),
    ('fal key', B + r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}:[0-9a-f]{32}'),
    ('telegram bot token', B + r'[0-9]{8,10}:AA[A-Za-z0-9_\-]{33}'),
    ('assignment', r'(?i)(?:api[_-]?key|apikey|secret|token|passw(?:or)?d|client[_-]?secret)["\']?\s*[:=]\s*["\']?([A-Za-z0-9_\-\./+=]{16,})'),
]
COMPILED = [(k, re.compile(p)) for k, p in PATTERNS]
PLACEHOLDER = re.compile(
    r'(?i)(x{4,}|your|example|placeholder|dummy|sample|fake|test|redacted|changeme|'
    r'<[^>]*>|\.\.\.|\$\{|\$[A-Z_]|process\.env|os\.environ|getenv|env\[|0000000|1234567|abcdef)')
SKIP_DIRS = {'.git', 'node_modules', '.venv', '__pycache__'}
BINARY_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov', '.mp3', '.wav',
              '.pdf', '.zip', '.gz', '.ico', '.woff', '.woff2', '.ttf', '.otf', '.psd'}


def hits(line):
    for kind, rx in COMPILED:
        for m in rx.finditer(line):
            value = m.group(1) if m.groups() else m.group(0)
            if PLACEHOLDER.search(value) or PLACEHOLDER.search(line[max(0, m.start() - 20):m.end() + 20]):
                continue
            if kind == 'assignment' and not re.search(r'[0-9]', value):
                continue  # words like token=requestHeaderName are not secrets
            yield kind
            break


def scan_diff(stream):
    found, path, lineno = [], '?', 0
    for raw in stream:
        line = raw.rstrip('\n')
        if line.startswith('+++ '):
            path = line[6:] if line.startswith('+++ b/') else line[4:]
            continue
        if line.startswith('@@'):
            m = re.search(r'\+(\d+)', line)
            lineno = int(m.group(1)) - 1 if m else 0
            continue
        if line.startswith('+') and not line.startswith('+++'):
            lineno += 1
            for kind in hits(line[1:]):
                found.append(f'{path}:{lineno}: {kind}')
        elif not line.startswith('-'):
            lineno += 1
    return found


def scan_file(p):
    found = []
    name = os.path.basename(p)
    if name == '.env' or (name.startswith('.env.') and name != '.env.example'):
        return [f'{p}:0: .env file']
    if os.path.splitext(p)[1].lower() in BINARY_EXT:
        return []
    try:
        with open(p, encoding='utf-8', errors='strict') as fh:
            for i, line in enumerate(fh, 1):
                for kind in hits(line):
                    found.append(f'{p}:{i}: {kind}')
    except (UnicodeDecodeError, OSError):
        pass
    return found


def scan_paths(paths):
    found = []
    for root in paths:
        if os.path.isfile(root):
            found += scan_file(root)
            continue
        for d, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
            for f in files:
                found += scan_file(os.path.join(d, f))
    return found


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '--diff':
        result = scan_diff(sys.stdin)
    elif len(sys.argv) >= 3 and sys.argv[1] == '--files':
        result = scan_paths(sys.argv[2:])
    else:
        sys.exit(__doc__)
    for r in result:
        print(r)
    sys.exit(1 if result else 0)
