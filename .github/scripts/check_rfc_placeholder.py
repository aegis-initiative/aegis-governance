import glob
import re
import sys

# Placeholder RFCs only need minimal required fields and a placeholder note
REQUIRED_HEADERS = [
    r'\*\*RFC:?\*\*',
    r'\*\*Status:?\*\*',
    r'\*\*Version:?\*\*',
    r'\*\*Created:?\*\*',
    r'\*\*Updated:?\*\*',
    r'\*\*Author:?\*\*',
]
REQUIRED_SECTIONS = [
    r'## Summary',
    r'## Status Note',
]
PLACEHOLDER_STATUS = re.compile(r'\*\*Status:?\*\*\s*Placeholder', re.IGNORECASE)
PLACEHOLDER_NOTE = re.compile(r'This is a placeholder RFC', re.IGNORECASE)

failures = 0
for path in glob.glob('rfc/RFC-*.md'):
    if 'TEMPLATE' in path:
        continue
    with open(path, encoding='utf-8') as f:
        content = f.read()
        # Only check RFCs with Status: Placeholder
        if not PLACEHOLDER_STATUS.search(content):
            continue
        for header in REQUIRED_HEADERS:
            if not re.search(header, content):
                print(f'Missing metadata: {header} in {path}')
                failures += 1
        for section in REQUIRED_SECTIONS:
            if not re.search(section, content):
                print(f'Missing section: {section} in {path}')
                failures += 1
        if not PLACEHOLDER_NOTE.search(content):
            print(f'Missing placeholder note in {path}')
            failures += 1
if failures:
    print(f"\n{failures} Placeholder RFC(s) missing required fields or sections.")
    sys.exit(1)
else:
    print("All Placeholder RFCs conform to the minimal template.")
