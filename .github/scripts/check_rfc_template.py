import glob
import re
import sys

# Required metadata fields and section headers (adjust as your template evolves)
REQUIRED_HEADERS = [
    r'\*\*RFC:\*\*',
    r'\*\*Status:\*\*',
    r'\*\*Version:\*\*',
    r'\*\*Created:\*\*',
    r'\*\*Updated:\*\*',
    r'\*\*Author:\*\*',
]
REQUIRED_SECTIONS = [
    r'## Summary',
    r'## Motivation',
    r'## Guide-Level Explanation',
    r'## Reference-Level Explanation',
    r'## Drawbacks',
    r'## Alternatives Considered',
    r'## Compatibility',
    r'## Implementation Notes',
    r'## Open Questions',
    r'## Success Criteria',
    r'## References',
]

failures = 0
for path in glob.glob('rfc/RFC-*.md'):
    if 'TEMPLATE' in path:
        continue
    with open(path, encoding='utf-8') as f:
        content = f.read()
        for header in REQUIRED_HEADERS:
            if not re.search(header, content):
                print(f'Missing metadata: {header} in {path}')
                failures += 1
        for section in REQUIRED_SECTIONS:
            if not re.search(section, content):
                print(f'Missing section: {section} in {path}')
                failures += 1
if failures:
    print(f"\n{failures} RFC(s) missing required template fields or sections.")
    sys.exit(1)
else:
    print("All RFCs conform to the template.")
