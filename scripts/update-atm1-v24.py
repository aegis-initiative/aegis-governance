#!/usr/bin/env python3
"""Add the ATM-1 mapping entry for ATX-1 v2.4 technique T6003.

ATM-1 mapping covers parent techniques only (sub-techniques are not mapped).
T6003 is mapped to real ATM-1 catalog IDs:
  - AV-7.1  Coordinated Low-Risk Abuse  (same vector as sibling T6001)
  - PC-4    Input Validation & Sanitization  (covers the injected-context vector)
  - DC-2    Behavioral Anomaly Detection  (detects the unbounded loop)

Coverage is "partial": detection of unbounded execution is present, but the
independent progress-signal verification proposed by LoopTrap is not yet an
ATM-1 preventive control.

Idempotent.
"""

from __future__ import annotations

import json
from pathlib import Path

MAP_PATH = Path("docs/atx/v2/data/atx-1-atm1-mapping.json")

ENTRY = {
    "atx_id": "T6003",
    "atx_name": "Poison Termination Judgment",
    "tactic": "TA006",
    "atm_vectors": ["AV-7.1"],
    "atm_controls": ["PC-4", "DC-2"],
    "atm_detections": ["request_rate_anomaly", "resource_usage_spike"],
    "coverage": "partial",
    "notes": (
        "Unbounded execution is detectable via behavioral anomaly signals; PC-4 "
        "covers sanitization of the untrusted-context injection vector. Independent "
        "progress-signal verification (the LoopTrap defense) is not yet an ATM-1 "
        "preventive control."
    ),
}


def main() -> int:
    m = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    ids = [e["atx_id"] for e in m["mappings"]]
    if ENTRY["atx_id"] in ids:
        print("T6003 already mapped — nothing to do.")
        return 0

    # Insert after T6002 to keep id ordering.
    idx = ids.index("T6002") + 1 if "T6002" in ids else len(m["mappings"])
    m["mappings"].insert(idx, ENTRY)

    m["coverage"]["atx_version"] = "2.4"
    m["description"] = (
        "Mapping of ATX-1 techniques to ATM-1 attack vectors, controls, and "
        "detection signals. Aligned with ATX-1 v2.4."
    )
    m["generated"] = "2026-05-29"

    MAP_PATH.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Inserted T6003 ATM-1 mapping at index {idx}. Total mappings: {len(m['mappings'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
