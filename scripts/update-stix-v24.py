#!/usr/bin/env python3
"""Add STIX 2.1 objects for ATX-1 v2.4: technique T6003 + sub-techniques.

T6003 (Poison Termination Judgment) is a NEW PARENT technique under tactic
TA006, so unlike the v2.2 update (sub-techniques only) this also creates the
parent attack-pattern, its tactic ``uses`` relationship, its course-of-action
mitigation, and the ``mitigates`` relationship — mirroring how the original
parent techniques are represented in the bundle.

Idempotent: re-running after T6003 is present is a no-op.
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

DATA_PATH = Path("docs/atx/v2/data/atx-1-techniques.json")
STIX_PATH = Path("docs/atx/v2/stix/atx-1-bundle.json")

NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
TIMESTAMP = "2026-05-29T00:00:00.000Z"
NEW_PARENT = "T6003"
MITIGATION_EXTERNAL_ID = "M030"
COA_NAME = "AGP Progress-Signal Verification and Provenance-Aware Context Processing"

OWASP_DESC = {
    "LLM01": "Prompt Injection",
    "LLM06": "Excessive Agency",
    "LLM10": "Unbounded Consumption",
}

# Provenance reference for the LoopTrap source paper.
LOOPTRAP_REF = {
    "source_name": "looptrap",
    "external_id": "arXiv:2605.05846",
    "description": "H. Xu et al., LoopTrap: Termination Poisoning Attacks on LLM Agents",
    "url": "https://arxiv.org/abs/2605.05846",
}


def deterministic_id(prefix: str, key: str) -> str:
    return f"{prefix}--{uuid.uuid5(NAMESPACE, key)}"


def owasp_refs(technique: dict) -> list[dict]:
    refs = []
    for owasp in technique.get("owasp_mapping") or []:
        ref = {"source_name": "owasp-llm-top-10", "external_id": owasp}
        if owasp in OWASP_DESC:
            ref["description"] = OWASP_DESC[owasp]
        refs.append(ref)
    return refs


def main() -> int:
    techniques = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    bundle = json.loads(STIX_PATH.read_text(encoding="utf-8"))
    objs = bundle["objects"]

    by_id = {t["id"]: t for t in techniques}
    identity_id = None
    existing_aps: dict[str, dict] = {}
    tactic_by_extid: dict[str, dict] = {}
    for o in objs:
        if o.get("type") == "identity":
            identity_id = o["id"]
        elif o.get("type") == "attack-pattern":
            for r in o.get("external_references", []):
                if r.get("source_name") == "atx-1":
                    existing_aps[r["external_id"]] = o
        elif o.get("type") == "x-mitre-tactic":
            for r in o.get("external_references", []):
                if r.get("source_name") == "atx-1":
                    tactic_by_extid[r["external_id"]] = o

    if identity_id is None:
        print("ERROR: no identity object in bundle", file=sys.stderr)
        return 1
    if NEW_PARENT in existing_aps:
        print(f"{NEW_PARENT} already present in STIX bundle — nothing to do.")
        return 0

    parent = by_id[NEW_PARENT]
    tactic = tactic_by_extid[parent["tactic"]]
    phase_name = tactic["x_mitre_shortname"]
    new_objects: list[dict] = []

    # --- Parent attack-pattern ---
    parent_ap_id = deterministic_id("attack-pattern", f"atx1:{NEW_PARENT}")
    parent_ap = {
        "type": "attack-pattern",
        "spec_version": "2.1",
        "id": parent_ap_id,
        "created": TIMESTAMP,
        "modified": TIMESTAMP,
        "created_by_ref": identity_id,
        "name": parent["name"],
        "description": parent["description"],
        "kill_chain_phases": [{"kill_chain_name": "atx-1", "phase_name": phase_name}],
        "external_references": [
            {"source_name": "atx-1", "external_id": NEW_PARENT},
            LOOPTRAP_REF,
            *owasp_refs(parent),
        ],
    }
    new_objects.append(parent_ap)

    # --- tactic uses technique ---
    new_objects.append({
        "type": "relationship",
        "spec_version": "2.1",
        "id": deterministic_id("relationship", f"atx1:uses:{NEW_PARENT}"),
        "created": TIMESTAMP,
        "modified": TIMESTAMP,
        "created_by_ref": identity_id,
        "relationship_type": "uses",
        "source_ref": tactic["id"],
        "target_ref": parent_ap_id,
    })

    # --- course-of-action (mitigation) + mitigates relationship ---
    mit = parent["aegis_mitigation"]
    coa_id = deterministic_id("course-of-action", f"atx1:{MITIGATION_EXTERNAL_ID}")
    coa = {
        "type": "course-of-action",
        "spec_version": "2.1",
        "id": coa_id,
        "created": TIMESTAMP,
        "modified": TIMESTAMP,
        "created_by_ref": identity_id,
        "name": COA_NAME,
        "description": f"{mit['mechanism']} Constitutional Article: {mit['constitutional_article']}.",
        "external_references": [
            {"source_name": "atx-1", "external_id": MITIGATION_EXTERNAL_ID},
            {"source_name": "aegis-constitution", "description": f"Article: {mit['constitutional_article']}"},
            {"source_name": "aegis-governance", "description": mit["agp_mechanism"]},
        ],
    }
    new_objects.append(coa)
    new_objects.append({
        "type": "relationship",
        "spec_version": "2.1",
        "id": deterministic_id("relationship", f"atx1:mitigates:{NEW_PARENT}"),
        "created": TIMESTAMP,
        "modified": TIMESTAMP,
        "created_by_ref": identity_id,
        "relationship_type": "mitigates",
        "source_ref": coa_id,
        "target_ref": parent_ap_id,
    })

    # --- sub-technique attack-patterns + subtechnique-of relationships ---
    for sub_id in parent.get("sub_techniques", []):
        sub = by_id[sub_id]
        sub_ap_id = deterministic_id("attack-pattern", f"atx1:{sub_id}")
        new_objects.append({
            "type": "attack-pattern",
            "spec_version": "2.1",
            "id": sub_ap_id,
            "created": TIMESTAMP,
            "modified": TIMESTAMP,
            "created_by_ref": identity_id,
            "name": sub["name"],
            "description": sub["description"],
            "kill_chain_phases": [{"kill_chain_name": "atx-1", "phase_name": phase_name}],
            "external_references": [
                {"source_name": "atx-1", "external_id": sub_id},
                *owasp_refs(sub),
            ],
            "x_mitre_is_subtechnique": True,
            "x_aegis_parent_technique": NEW_PARENT,
        })
        new_objects.append({
            "type": "relationship",
            "spec_version": "2.1",
            "id": deterministic_id("relationship", f"atx1:subtech-of:{sub_id}"),
            "created": TIMESTAMP,
            "modified": TIMESTAMP,
            "created_by_ref": identity_id,
            "relationship_type": "subtechnique-of",
            "source_ref": sub_ap_id,
            "target_ref": parent_ap_id,
        })

    objs.extend(new_objects)
    STIX_PATH.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    from collections import Counter
    print(f"Added {len(new_objects)} objects:", dict(Counter(o['type'] for o in new_objects)))
    print(f"Total STIX objects: {len(objs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
