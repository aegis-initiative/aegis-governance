# LoopTrap — Termination Poisoning inclusion in ATX-1

**Date:** 2026-05-17 (response 2026-05-22)\
**From:** Kenneth Tannenbaum, AEGIS Initiative\
**To:** Zhibo Wang (corresponding author), Huiyu Xu (first author) — Zhejiang University *(addresses masked)*\
**Status:** Replies sent (2026-05-29 endorsement ack, 2026-06-14 DOI delivery); collaboration open\
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
- **Deposited:** ATX-1 v2.4 published to IEEE DataPort, DOI [10.21227/edxj-ka42](https://doi.org/10.21227/edxj-ka42) (2026-06-14).
- **Correspondence:** AEGIS reply sent 2026-05-29 (thank-you + endorsement acknowledgment; flagged alignment with the authors' benchmark and shadow-progress-model defense). DOI-delivery follow-up sent 2026-06-14 with the v2.4 DataPort DOI and live taxonomy link. Full text: `housekeeping/looptrap-reply-draft-2026-05-29.md` (SENT) and `housekeeping/looptrap-followup-doi-2026-06-14.md` (SENT).
- **Decided:** the four behavioral vulnerability dimensions (phase compliance, authority compliance, recursive susceptibility, verification tendency) are deferred to the authors' forthcoming termination-layer robustness benchmark — defender-side measurement constructs, not techniques. Intent to cite that benchmark as corroborating evidence once public stands.

---

**Part of**: AEGIS Documentation\
**Maintained by**: AEGIS Initiative
