# LoopTrap — Termination Poisoning inclusion in ATX-1

**Date:** 2026-05-17 (response 2026-05-22)\
**From:** Kenneth Tannenbaum, AEGIS Initiative\
**To:** Zhibo Wang (corresponding author), Huiyu Xu (first author) — Zhejiang University *(addresses masked)*\
**Status:** Active — ongoing exchange\
**Response:** Received — 2026-05-22\
**Discussion:** —

---

## Context

Outreach to the authors of "LoopTrap: Termination Poisoning Attacks on LLM Agents" (H. Xu et al., arXiv:2605.05846, May 2026), proposing inclusion of Termination Poisoning as an ATX-1 technique under tactic TA006 (Abuse Resource Allocation), with sub-techniques mapped to the paper's 10 strategies, and asking whether the authors had objections or attribution preferences.

The taxonomic case made in the outreach:

- **Surface:** the agent's progress-evaluation / termination step in the agentic control loop — not the model's forward pass. Distinct from model-level resource-exhaustion ("sponge") attacks, which are ATLAS-adjacent.
- **Vector:** injected instructions in untrusted retrieved context (web, documents, API responses, federated/shared skills) — the same vector family as indirect prompt injection, but with a distinct goal: corrupt termination rather than action selection.
- **Defenses proposed by the authors** (independent progress-signal verification, provenance-aware context processing) map onto AEGIS's out-of-band enforcement architecture and independently validate the column-three thesis.

## Outcome

Huiyu Xu replied on 2026-05-22 on behalf of the LoopTrap team:

- **No objections** to inclusion. The authors welcome it.
- **Mapping ratified:** Termination Poisoning as a technique under the resource/control-flow tactic, with sub-techniques corresponding to the 10 strategies, is "faithful to the structure of the paper and taxonomically sound."
- **Naming conventions** as described were endorsed.
- The authors flagged two active research axes they consider directly relevant to the ATX-1 entries: (1) a multi-dimensional **termination-layer robustness benchmark** (behavioral persistence, recovery latency, cross-agent transferability), and (2) **defense architectures** — lightweight runtime monitors maintaining an independent "shadow" progress model immune to context injection, plus trust-stratified context-processing pipelines — offered as actionable countermeasure mappings for ATX-1.

## Downstream

- ATX-1 v2.4 adds technique **T6003 (Poison Termination Judgment)** under TA006 with sub-techniques T6003.001–T6003.010. See `changelog/2026-05-29-atx1-v2.4.md`.
- Reference added to `REFERENCES.md` ([38]).
- Open follow-up: whether to pair the four behavioral vulnerability dimensions (phase compliance, authority compliance, recursive susceptibility, verification tendency) with the technique as a defender's-side characterization, and whether to track the authors' forthcoming benchmark as corroborating evidence.

---

**Part of**: AEGIS Documentation\
**Maintained by**: AEGIS Initiative
