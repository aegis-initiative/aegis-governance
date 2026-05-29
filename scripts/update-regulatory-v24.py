#!/usr/bin/env python3
"""Add regulatory cross-reference entries for ATX-1 v2.4 (T6003 + sub-techniques).

The regulatory crossref includes sub-techniques, so this adds 11 entries
(1 parent + 10 sub-techniques), mirroring the structure of existing entries.

Idempotent.
"""

from __future__ import annotations

import json
from pathlib import Path

PATH = Path("docs/atx/v2/data/atx-1-regulatory-crossref.json")

NIST = {
    "functions": ["Manage", "Measure"],
    "description": (
        "MANAGE 2.2 (Mechanisms for managing AI risks), MEASURE 2.5 (Computational "
        "resource and execution-loop monitoring)"
    ),
}
EU = {
    "articles": ["Article 9", "Article 15"],
    "description": (
        "Art. 9 Risk management — termination-signal integrity as a risk control; "
        "Art. 15 Robustness — resilience against adversarial inputs that induce "
        "unbounded execution"
    ),
}
OWASP = ["LLM01", "LLM10"]

PARENT = {
    "id": "T6003",
    "name": "Poison Termination Judgment",
    "tactic": "TA006",
    "nist_ai_rmf": NIST,
    "eu_ai_act": EU,
    "owasp_llm_top_10": OWASP,
    "atm_1_scenario": (
        "Injected content in untrusted retrieved context distorts the agent's "
        "termination judgment, causing it to treat an already-complete task as "
        "incomplete and continue executing without bound"
    ),
}

SUBS = [
    ("T6003.001", "Shift the Completion Target",
     "Injected content repeatedly redefines the scope of 'complete,' so each satisfied criterion reveals new required coverage and the agent never terminates"),
    ("T6003.002", "Inject Open-Ended Subgoals",
     "Injected content supplies an unbounded sequence of intermediate milestones, each framed as a prerequisite to completion"),
    ("T6003.003", "Assert Asymptotic Incompletion",
     "Injected content insists the task is perpetually almost complete, so the agent keeps iterating toward a state it never reaches"),
    ("T6003.004", "Fabricate Authority Directives",
     "Injected content impersonates system or operator directives forbidding termination, exploiting the agent's deference to apparent authority"),
    ("T6003.005", "Invoke Sunk-Cost Framing",
     "Injected content frames stopping as wasting the effort already expended, pressuring the agent to continue"),
    ("T6003.006", "Appeal to Expert Norms",
     "Injected content claims expert agents would continue or verify further, inducing conformity-driven continuation"),
    ("T6003.007", "Force Recursive Verification",
     "Injected content makes each verification step require its own verification, creating an unbounded regress of self-checking"),
    ("T6003.008", "Impose Circular Prerequisites",
     "Injected content introduces circular prerequisites among steps, with no satisfiable terminal state"),
    ("T6003.009", "Reward Continued Execution",
     "Injected content praises each additional step, reinforcing continuation and discouraging the stopping decision"),
    ("T6003.010", "Introduce Fabricated Scoring",
     "Injected content introduces a fabricated score or progress bar the agent seeks to maximize, deferring termination indefinitely"),
]


def main() -> int:
    r = json.loads(PATH.read_text(encoding="utf-8"))
    ids = [e["id"] for e in r["techniques"]]
    if "T6003" in ids:
        print("T6003 already in regulatory crossref — nothing to do.")
        return 0

    entries = [PARENT]
    for sid, name, scenario in SUBS:
        entries.append({
            "id": sid,
            "name": name,
            "tactic": "TA006",
            "parent_technique": "T6003",
            "nist_ai_rmf": NIST,
            "eu_ai_act": EU,
            "owasp_llm_top_10": OWASP,
            "atm_1_scenario": scenario,
        })

    idx = ids.index("T6002") + 1 if "T6002" in ids else len(r["techniques"])
    r["techniques"][idx:idx] = entries

    r["version"] = "2.4.0"
    r["date"] = "2026-05-29"
    r["description"] = (
        "ATX-1 v2.4 regulatory cross-reference matrix mapping techniques and "
        "sub-techniques to NIST AI RMF, EU AI Act, OWASP LLM Top 10, and ATM-1 "
        "threat scenarios. v2.4 adds Termination Poisoning (T6003) under TA006 with "
        "10 sub-techniques; all 69 entries (30 parent techniques + 39 sub-techniques) "
        "are preserved."
    )

    PATH.write_text(json.dumps(r, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Inserted {len(entries)} regulatory entries at index {idx}. Total: {len(r['techniques'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
