#!/usr/bin/env python3
"""Migrate docs/atx/ATX-1_TECHNIQUE_TAXONOMY.md from the stale v1.0 structure to v2.4.

The human-readable taxonomy doc still carried the pre-v2.0 tactic/technique
numbering and names (e.g. TA006 "Governance State Corruption", T2001
"Irreversible Collateral Action") despite a v2.3 header. This regenerates the
data-driven sections (§4 Tactic Taxonomy, §5 Technique Catalog, §6 Mitigation
Mapping, §7 OWASP Cross-Reference) from the canonical v2 data and updates counts,
ID references, the evidence hierarchy, and references in the narrative sections.

Source of truth: docs/atx/v2/data/atx-1-techniques.json + STIX tactic descriptions.
Narrative sections (§1-3 prose, §8-10) are preserved with targeted edits.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

DOC = Path("docs/atx/ATX-1_TECHNIQUE_TAXONOMY.md")
TECH = Path("docs/atx/v2/data/atx-1-techniques.json")
STIX = Path("docs/atx/v2/stix/atx-1-bundle.json")

OWASP_NAME = {
    "LLM01": "Prompt Injection",
    "LLM02": "Sensitive Information Disclosure",
    "LLM06": "Excessive Agency",
    "LLM07": "System Prompt Leakage",
    "LLM10": "Unbounded Consumption",
}

KEY_QUESTION = {
    "TA001": "Did the agent verify that the instruction source holds authority for the requested action scope?",
    "TA002": "Is the action within the scope and proportionality of the delegated objective?",
    "TA003": "Could this action cause irreversible or cascading changes to system state?",
    "TA004": "Is the recipient authorized to receive this information, and was disclosure explicitly sanctioned?",
    "TA005": "Does the reported state match the actual, verified system state?",
    "TA006": "Are resource consumption and execution bounded and proportionate to the task?",
    "TA007": "Has the agent verified the identity, provenance, and authorization of peer agents and inherited configurations?",
    "TA008": "Could this action create state or instructions that persist beyond the current authorized session?",
    "TA009": "Are all of the agent's actions observable and faithfully recorded by the governance layer?",
    "TA010": "Does the governance layer have a complete model of what the execution environment will actually do with this action?",
}

TACTIC_ORDER = [f"TA{n:03d}" for n in range(1, 11)]


def load():
    techniques = json.loads(TECH.read_text(encoding="utf-8"))
    bundle = json.loads(STIX.read_text(encoding="utf-8"))
    tactic_desc = {}
    tactic_name = {}
    for o in bundle["objects"]:
        if o.get("type") == "x-mitre-tactic":
            for r in o.get("external_references", []):
                if r.get("source_name") == "atx-1":
                    tactic_desc[r["external_id"]] = o["description"]
                    tactic_name[r["external_id"]] = o["name"]
    return techniques, tactic_desc, tactic_name


def provenance(t: dict) -> str:
    if t.get("agents_of_chaos_case"):
        return "Agents of Chaos Case Study " + ", ".join(f"#{n}" for n in t["agents_of_chaos_case"])
    if t["id"].startswith("T6003"):
        return "LoopTrap (Xu et al., arXiv:2605.05846)"
    if t["tactic"] == "TA010":
        return "RFC-0006 adversarial testing"
    return "AEGIS RFC-0006 / aegis-core red-team validation"


def owasp_str(t: dict) -> str:
    ids = t.get("owasp_mapping") or []
    if not ids:
        return "—"
    return ", ".join(f"{i} ({OWASP_NAME.get(i, i)})" for i in ids)


def mitigation_str(t: dict) -> str:
    m = t["aegis_mitigation"]
    parts = [m["mechanism"].strip()]
    tail = f"Constitutional Article: {m['constitutional_article']}."
    if m.get("agp_mechanism"):
        tail += f" AGP Mechanism(s): {m['agp_mechanism']}."
    return f"{parts[0]} {tail}"


def md_escape(s: str) -> str:
    return s.replace("|", "\\|")


def gen_section4(techniques, tactic_desc, tactic_name) -> str:
    parents_by_tactic: dict[str, list] = {}
    for t in techniques:
        if "." not in t["id"]:
            parents_by_tactic.setdefault(t["tactic"], []).append(t)
    out = ["## 4. Tactic Taxonomy", ""]
    out.append(
        "ATX-1 defines 10 tactics. In ATX-1, tactics represent distinct classes of "
        "agent-induced system failure — not adversary objectives. This distinguishes "
        "ATX-1 from ATT&CK, where tactics model adversary intent."
    )
    out.append("")
    out.append("---")
    out.append("")
    for ta in TACTIC_ORDER:
        out.append(f"### {ta}: {tactic_name[ta]}")
        out.append("")
        out.append(f"**Description:** {tactic_desc[ta]}")
        out.append("")
        out.append(f"**Key Question:** {KEY_QUESTION[ta]}")
        out.append("")
        members = parents_by_tactic.get(ta, [])
        listed = ", ".join(f"{t['id']} ({t['name']})" for t in members)
        out.append(f"**Techniques:** {listed}")
        out.append("")
        out.append("---")
        out.append("")
    return "\n".join(out)


def gen_section5(techniques, tactic_name) -> str:
    parents_by_tactic: dict[str, list] = {}
    subs_by_parent: dict[str, list] = {}
    for t in techniques:
        if "." in t["id"]:
            subs_by_parent.setdefault(t["parent_technique"], []).append(t)
        else:
            parents_by_tactic.setdefault(t["tactic"], []).append(t)

    out = ["## 5. Technique Catalog", ""]
    for ta in TACTIC_ORDER:
        out.append(f"### {ta}: {tactic_name[ta]}")
        out.append("")
        for t in parents_by_tactic.get(ta, []):
            out.append(f"#### {t['id']}: {t['name']}")
            out.append("")
            out.append("| Field | Value |")
            out.append("|-------|-------|")
            out.append(f"| **ID** | {t['id']} |")
            out.append(f"| **Name** | {md_escape(t['name'])} |")
            out.append(f"| **Tactic** | {ta} — {tactic_name[ta]} |")
            out.append(f"| **Description** | {md_escape(t['description'])} |")
            out.append(f"| **Root Cause** | {md_escape(t['root_cause'])} |")
            out.append(f"| **Provenance** | {md_escape(provenance(t))} |")
            out.append(f"| **AEGIS Mitigation** | {md_escape(mitigation_str(t))} |")
            out.append(f"| **OWASP LLM Mapping** | {md_escape(owasp_str(t))} |")
            subs = subs_by_parent.get(t["id"], [])
            if subs:
                sub_list = "; ".join(f"{s['id']} ({s['name']})" for s in subs)
                out.append(f"| **Sub-Techniques** | {md_escape(sub_list)} |")
            out.append("")
        out.append("---")
        out.append("")

    # Sub-technique detail listing
    out.append("### 5.11 Sub-Techniques")
    out.append("")
    out.append(
        "Sub-technique IDs use the format `T####.###`. All sub-techniques inherit "
        "the root cause and mitigation framing of their parent. Full definitions are "
        "in [`v2/data/atx-1-techniques.json`](v2/data/atx-1-techniques.json) and the "
        "[STIX 2.1 bundle](v2/stix/atx-1-bundle.json)."
    )
    out.append("")
    for parent_id in sorted(subs_by_parent, key=lambda x: (len(x), x)):
        parent = next(t for t in techniques if t["id"] == parent_id)
        out.append(f"#### {parent_id} sub-techniques ({parent['name']})")
        out.append("")
        for s in subs_by_parent[parent_id]:
            first = s["description"].split(". ")[0].rstrip(".")
            out.append(f"- **{s['id']}** — {s['name']}: {md_escape(first)}.")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def gen_section6(techniques, tactic_name) -> str:
    out = ["## 6. AEGIS Mitigation Mapping", ""]
    out.append("| Technique | Constitutional Article | AGP Mechanism | Mitigation Description |")
    out.append("|-----------|----------------------|---------------|----------------------|")
    for t in techniques:
        if "." in t["id"]:
            continue
        m = t["aegis_mitigation"]
        out.append(
            f"| {t['id']} | {md_escape(m['constitutional_article'])} | "
            f"{md_escape(m.get('agp_mechanism','—') or '—')} | {md_escape(m['mechanism'])} |"
        )
    return "\n".join(out)


def gen_section7(techniques, tactic_name) -> str:
    by_owasp: dict[str, list] = {}
    for t in techniques:
        if "." in t["id"]:
            continue
        for o in t.get("owasp_mapping") or []:
            by_owasp.setdefault(o, []).append(t)
    out = ["## 7. OWASP Top 10 LLM Cross-Reference", ""]
    out.append(
        "The OWASP Top 10 for Large Language Model Applications identifies security "
        "risks in LLM deployments. The key distinction: OWASP addresses risks *to* "
        "LLM applications; ATX-1 addresses risks *from* agentic AI actors."
    )
    out.append("")
    for o in sorted(by_owasp):
        out.append(f"### {o}: {OWASP_NAME.get(o, o)}")
        out.append("")
        out.append("| ATX-1 Technique | Tactic | Provenance |")
        out.append("|----------------|--------|------------|")
        for t in by_owasp[o]:
            out.append(f"| {t['id']} — {md_escape(t['name'])} | {t['tactic']} | {md_escape(provenance(t))} |")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    techniques, tactic_desc, tactic_name = load()
    doc = DOC.read_text(encoding="utf-8")

    # --- Splice §4-§7 ---
    new_body = (
        gen_section4(techniques, tactic_desc, tactic_name)
        + "\n" + gen_section5(techniques, tactic_name)
        + "\n" + gen_section6(techniques, tactic_name)
        + "\n\n---\n\n" + gen_section7(techniques, tactic_name)
        + "\n---\n\n"
    )
    start = doc.index("## 4. Tactic Taxonomy")
    end = doc.index("## 8. Methodology Precedent")
    doc = doc[:start] + new_body + doc[end:]

    # --- Header ---
    doc = doc.replace("**Version:** 2.3.0\\", "**Version:** 2.4.0\\")
    doc = doc.replace("**Date:** 2026-04-24\\", "**Date:** 2026-05-29\\")
    new_status = (
        "**Status:** Active — v2.4 adds Termination Poisoning (T6003) under TA006 with "
        "10 sub-techniques mapped to the strategies of Xu et al. (LoopTrap, "
        "arXiv:2605.05846). Severity remains removed (v2.3) for MITRE alignment.\\"
    )
    doc = re.sub(
        r"\*\*Status:\*\* Active —.*?\(preserved unchanged in v2\.3\)\.\\",
        lambda m: new_status,
        doc, flags=re.DOTALL,
    )

    # --- §1 / §8 / §9 counts and ID references ---
    doc = doc.replace(
        "The taxonomy defines **10 tactics** and **29 techniques**,",
        "The taxonomy defines **10 tactics** and **30 techniques** (plus 39 sub-techniques),",
    )
    doc = doc.replace(
        "| ATX-1 | Agents of Chaos (2026), RFC-0006 adversarial testing (2026) | 2026 | 10 tactics, 29 techniques |",
        "| ATX-1 | Agents of Chaos (2026), RFC-0006 adversarial testing (2026), LoopTrap (Xu et al., 2026) | 2026 | 10 tactics, 30 techniques |",
    )
    # Evidence hierarchy: add LoopTrap Tier-1 row after the RFC-0006 row.
    rfc_row = (
        "| **RFC-0006 Adversarial Testing** (AEGIS Initiative, 2026-03-26) | 4 techniques in "
        "governance interpretation gap | T10001-T10004 (TA010) | 5 rounds of white-box "
        "adversarial testing against AEGIS Claude Code governance plugin |"
    )
    looptrap_row = (
        "\n| **LoopTrap** (Xu et al., arXiv:2605.05846, 2026) | Termination Poisoning attack on "
        "the agentic control loop | T6003 + 10 sub-techniques (TA006) | 3.57x average step "
        "amplification (peak 25x) across 8 LLM agents over 60 GAIA tasks; inclusion endorsed by "
        "the authors (2026-05-22) |"
    )
    doc = doc.replace(rfc_row, rfc_row + looptrap_row)
    doc = doc.replace(
        "ATX-1 technique IDs (T1001-T10004) are designed",
        "ATX-1 technique IDs (T1001-T10004, including T6003) are designed",
    )

    # --- §10 References: insert LoopTrap as #6, renumber the tail 6->7, 7->8, 8->9, 9->10 ---
    doc = doc.replace(
        '9. **Saltzer, J. H. and Schroeder, M. D.**', '10. **Saltzer, J. H. and Schroeder, M. D.**')
    doc = doc.replace('8. **Anderson, J. P.**', '9. **Anderson, J. P.**')
    doc = doc.replace('7. **Mirsky, Y., et al.**', '8. **Mirsky, Y., et al.**')
    doc = doc.replace(
        '6. **OWASP.** "OWASP Top 10 for Large Language Model Applications." Version 2.0, 2025.',
        '6. **Xu, H., et al.** "LoopTrap: Termination Poisoning Attacks on LLM Agents." '
        "*arXiv:2605.05846*, May 2026.\n\n"
        '7. **OWASP.** "OWASP Top 10 for Large Language Model Applications." Version 2.0, 2025.',
    )

    DOC.write_text(doc, encoding="utf-8")
    n_parents = sum(1 for t in techniques if "." not in t["id"])
    n_subs = len(techniques) - n_parents
    print(f"Migrated taxonomy doc to v2.4: {n_parents} parent techniques, {n_subs} sub-techniques.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
