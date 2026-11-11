"""Check Markdown footnote integrity across the repository.

Fails when:
  1. A document uses an inline footnote marker ([^N]) that has no matching
     definition ([^N]: ...) in the same file. Without the definition the
     marker renders as literal text and the citation is lost.
  2. The "Entries" count in the REFERENCES.md footer does not match the
     number of numbered entries, or entry numbers are duplicated.

Footnote definitions that are never referenced are reported as warnings.

Markers inside fenced code blocks and inline code spans are ignored, so
documentation that describes the convention (e.g. `[^N]`) does not trip
the check.
"""
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

FENCE = re.compile(r'^\s{0,3}(```|~~~)')
INLINE_CODE = re.compile(r'(`+)(.+?)\1')
DEFINITION = re.compile(r'^\s{0,3}\[\^([^\]\s]+)\]:')
MARKER = re.compile(r'\[\^([^\]\s]+)\]')
REFERENCE_ENTRY = re.compile(r'^\[(\d+)\]\s')
ENTRIES_FOOTER = re.compile(r'^\*\*Entries\*\*:\s*(\d+)')


def tracked_markdown_files():
    out = subprocess.run(
        ['git', 'ls-files', '-z', '*.md'],
        cwd=REPO_ROOT, capture_output=True, check=True,
    ).stdout.decode('utf-8')
    return [p for p in out.split('\0') if p]


def scan(path):
    """Return (markers, definitions) as {label: first line number}."""
    markers, definitions = {}, {}
    in_fence = False
    text = (REPO_ROOT / path).read_text(encoding='utf-8', errors='replace')
    for lineno, line in enumerate(text.splitlines(), start=1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = INLINE_CODE.sub('', line)
        definition = DEFINITION.match(line)
        if definition:
            definitions.setdefault(definition.group(1), lineno)
            line = line[definition.end():]
        for marker in MARKER.finditer(line):
            markers.setdefault(marker.group(1), lineno)
    return markers, definitions


def check_footnotes():
    errors, warnings = [], []
    for path in tracked_markdown_files():
        markers, definitions = scan(path)
        for label, lineno in markers.items():
            if label not in definitions:
                errors.append(
                    f'{path}:{lineno}: footnote marker [^{label}] has no definition'
                )
        for label, lineno in definitions.items():
            if label not in markers:
                warnings.append(
                    f'{path}:{lineno}: footnote definition [^{label}] is never referenced'
                )
    return errors, warnings


def check_references_footer():
    path = REPO_ROOT / 'REFERENCES.md'
    if not path.exists():
        return []
    numbers, declared = [], None
    for line in path.read_text(encoding='utf-8').splitlines():
        entry = REFERENCE_ENTRY.match(line)
        if entry:
            numbers.append(int(entry.group(1)))
        footer = ENTRIES_FOOTER.match(line)
        if footer:
            declared = int(footer.group(1))
    errors = []
    duplicates = sorted({n for n in numbers if numbers.count(n) > 1})
    if duplicates:
        errors.append(f'REFERENCES.md: duplicate entry numbers {duplicates}')
    if declared is None:
        errors.append('REFERENCES.md: footer has no "**Entries**: N" line')
    elif declared != len(numbers):
        errors.append(
            f'REFERENCES.md: footer says Entries: {declared} '
            f'but the file has {len(numbers)} numbered entries'
        )
    return errors


def main():
    errors, warnings = check_footnotes()
    errors += check_references_footer()
    for warning in warnings:
        print(f'WARNING: {warning}')
    for error in errors:
        print(f'ERROR: {error}')
    if errors:
        print(f'\nFootnote check failed with {len(errors)} error(s).')
        sys.exit(1)
    print('Footnote check passed.')


if __name__ == '__main__':
    main()
