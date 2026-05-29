#!/usr/bin/env python3
"""Update the ATT&CK Navigator layer for ATX-1 v2.4.

- Bumps name/description to v2.4
- Adds a Navigator entry for new parent technique T6003 (showSubtechniques=true)
- Adds entries for sub-techniques T6003.001-.010

New entries intentionally omit the legacy severity-derived ``score``/``color``
and the ``Severity`` metadata field: severity was removed from the taxonomy in
v2.3 for MITRE alignment, so it is not reintroduced here. (Pre-existing entries
still carry leftover scores from before the v2.3 removal; cleaning those is a
separate task.)

Idempotent: safe to run multiple times.
"""

from __future__ import annotations

import json
from pathlib import Path

DATA_PATH = Path("docs/atx/v2/data/atx-1-techniques.json")
NAV_PATH = Path("docs/atx/v2/data/atx-1-navigator-layer.json")

NEW_PARENT = "T6003"

TACTIC_SLUGS = {
    "TA001": "violate-authority-boundaries",
    "TA002": "exceed-operational-scope",
    "TA003": "perform-irreversible-action",
    "TA004": "expose-or-exfiltrate-information",
    "TA005": "violate-state-integrity",
    "TA006": "abuse-resource-allocation",
    "TA007": "manipulate-agent-interactions",
    "TA008": "establish-or-modify-persistence",
    "TA009": "evade-detection-or-oversight",
    "TA010": "act-beyond-governance-interpretation",
}

LINKS = [
    {"label": "ATX-1 Documentation", "url": "https://aegis-docs.com/threat-matrix/techniques"},
    {"label": "STIX Bundle", "url": "https://aegis-governance.com/atx-1/stix-bundle.json"},
]


def main() -> int:
    techniques = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    nav = json.loads(NAV_PATH.read_text(encoding="utf-8"))
    by_id = {t["id"]: t for t in techniques}

    nav["name"] = "ATX-1 v2.4: AEGIS Threat Matrix"
    nav["description"] = (
        "ATX-1 v2.4 — 10 tactics, 30 techniques, 39 sub-techniques for "
        "autonomous AI agent threat modeling. v2.4 adds Termination Poisoning "
        "(T6003) under TA006 with 10 sub-techniques mapped to the strategies of "
        "Xu et al. (LoopTrap, arXiv:2605.05846)."
    )

    nav_by_id = {e["techniqueID"]: e for e in nav["techniques"]}
    parent = by_id[NEW_PARENT]
    new_entries: list[dict] = []

    def base_entry(t: dict) -> dict:
        return {
            "techniqueID": t["id"],
            "tactic": TACTIC_SLUGS[t["tactic"]],
            "comment": t["description"],
            "enabled": True,
        }

    # Parent entry
    if NEW_PARENT not in nav_by_id:
        e = base_entry(parent)
        e["metadata"] = [
            {"name": "Root Cause", "value": parent["root_cause"]},
            {"name": "Tactic", "value": parent["tactic_name"]},
            {"name": "OWASP", "value": ", ".join(parent.get("owasp_mapping") or [])},
        ]
        e["links"] = LINKS
        e["showSubtechniques"] = True
        new_entries.append(e)
        nav_by_id[NEW_PARENT] = e
    else:
        nav_by_id[NEW_PARENT]["showSubtechniques"] = True

    # Sub-technique entries
    for sub_id in parent.get("sub_techniques", []):
        if sub_id in nav_by_id:
            continue
        sub = by_id[sub_id]
        e = base_entry(sub)
        e["metadata"] = [
            {"name": "Parent Technique", "value": NEW_PARENT},
            {"name": "OWASP", "value": ", ".join(sub.get("owasp_mapping") or [])},
            {"name": "Tactic", "value": sub["tactic_name"]},
        ]
        e["links"] = LINKS
        e["showSubtechniques"] = False
        new_entries.append(e)
        nav_by_id[sub_id] = e

    nav["techniques"].extend(new_entries)
    NAV_PATH.write_text(json.dumps(nav, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Added {len(new_entries)} Navigator entries (1 parent + {len(new_entries)-1} sub-techniques)")
    print(f"Total Navigator technique entries: {len(nav['techniques'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
