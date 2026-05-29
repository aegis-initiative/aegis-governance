#!/usr/bin/env python3
"""Sync the governance-site taxonomy page to the canonical v2.4 taxonomy doc.

site/src/content/docs/threat-model/taxonomy.md is a published copy of the
ATX-1 technique taxonomy and was still on the v2.2 / pre-v2.0-structure content
(TA006 "Governance State Corruption", 29 techniques, no T6003). This replaces
its body with the migrated canonical doc (docs/atx/ATX-1_TECHNIQUE_TAXONOMY.md,
now v2.4), preserving the page's Astro frontmatter and refreshing its
description. Both files use identical internal/relative links.
"""

from __future__ import annotations

from pathlib import Path

CANON = Path("docs/atx/ATX-1_TECHNIQUE_TAXONOMY.md")
SITE = Path("site/src/content/docs/threat-model/taxonomy.md")
H1 = "# ATX-1: AEGIS Threat Matrix — Technique Taxonomy"


def main() -> int:
    canon = CANON.read_text(encoding="utf-8")
    body = canon[canon.index(H1):]

    site = SITE.read_text(encoding="utf-8")
    # Frontmatter = first block delimited by the opening and the next "---".
    assert site.startswith("---\n"), "taxonomy.md missing leading frontmatter"
    close = site.index("\n---\n", 4) + len("\n---\n")
    frontmatter = site[:close]
    frontmatter = frontmatter.replace(
        '"ATX-1 technique taxonomy — 10 tactics, 29 techniques for agentic AI threats"',
        '"ATX-1 technique taxonomy — 10 tactics, 30 techniques (39 sub-techniques) for agentic AI threats"',
    )

    SITE.write_text(frontmatter + "\n" + body, encoding="utf-8")
    print("Synced taxonomy.md body to canonical v2.4 doc.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
