---
title: |
  Response to Reviewers (Revision 2)\
  Manuscript ID DATA-00033-2026.R1\
  *Descriptor: AEGIS Threat Matrix for Agentic AI Systems (ATX-1)*
author: |
  Kenneth Tannenbaum\
  AEGIS Initiative, AEGIS Operations LLC\
  `ktannenbaum@aegis-initiative.com` --- ORCID 0009-0007-4215-1789
date: 2026-09-06
papersize: letter
fontsize: 11pt
geometry: margin=1in
linestretch: 1.15
linkcolor: blue
urlcolor: blue
citecolor: blue
numbersections: false
toc: false
header-includes:
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{microtype}
  - \usepackage{fancyhdr}
  - \usepackage{etoolbox}
  - \pagestyle{fancy}
  - \fancyhf{}
  - \fancyhead[L]{\small DATA-00033-2026.R1}
  - \fancyhead[R]{\small Response to Reviewers (Rev. 2)}
  - \fancyfoot[C]{\thepage}
  - \renewcommand{\headrulewidth}{0.4pt}
  - \let\oldtexttt\texttt
  - \renewcommand{\texttt}[1]{{\small\oldtexttt{#1}}}
  - \AtBeginEnvironment{longtable}{\footnotesize}
  - \AtBeginEnvironment{tabular}{\footnotesize}
---

# Editorial Note {-}

We thank the Editor-in-Chief, the Associate Editor, and both Reviewers for the second round of careful review. Reviewer 1 recommended acceptance with no further revisions; Reviewer 2 identified five writing/formatting issues; the Associate Editor asked that the bibliography be independently verified for authenticity, completeness, and citation consistency before final acceptance. This revision addresses all of it.

The bibliography verification (Associate Editor comment) was performed by checking every arXiv-sourced reference against its live arXiv record and every CVE/incident reference against its primary source. Four genuine citation errors were found and corrected; several other entries that appeared uncertain on first pass (conference-venue attributions, a CVE that did not immediately resolve through one lookup path) were independently re-verified and confirmed correct rather than removed on suspicion alone — the corrections below are the full set of errors found, not a partial pass.

The revised manuscript is submitted with tracked changes marked via the LaTeX `changes` package (blue underline for additions, red strikethrough for deletions), consistent with Revision 1. The remainder of this document responds point-by-point to each comment.

---

# Associate Editor Comments {-}

## AE-2. "Before final acceptance, please carefully verify and correct the references flagged by the editorial system, ensuring that all sources are authentic, complete, and consistently cited." {-}

**Response.** All 35 bibliography entries were individually re-verified against primary sources (arXiv abstract pages for preprints; CVE/incident databases and primary disclosure blogs for security references). Four errors were found and corrected; one numerical claim in the body text was corrected as a byproduct of the same verification pass.

**Action.**

- **[ref1] Wrong author, wrong year.** The AI Agent Index citation listed "R. Chan et al." — this does not match the paper's actual author list. Verified against arXiv:2602.17753: the correct first author is Leon Staufer (9 co-authors total), and the paper's title has a subtitle omitted from the original entry. Corrected to "L. Staufer et al., 'The 2025 AI Agent Index: Documenting Technical and Safety Features of Deployed Agentic AI Systems,' arXiv:2602.17753, 2026." The year is also corrected from 2025 to 2026, matching the arXiv posting date (Feb. 2026).
- **[ref18] Wrong month.** The Anthropic *Agentic Misalignment* citation listed "Jun. 2025." Verified against arXiv:2510.05179: the paper was posted Oct. 5, 2025. Corrected to "Oct. 2025."
- **[ref19] Wrong author initials.** The *Why Do Multi-Agent LLM Systems Fail?* citation listed "Y. Pan, Y. Yang" for the second and third authors. Verified against arXiv:2503.13657: the correct authors are Melissa Z. Pan and Shuyi Yang. Corrected to "M. Z. Pan, S. Yang."
- **[ref23] Wrong author initial.** The OpenAgentSafety citation listed "M. Vijayvargiya." Verified against arXiv:2507.06134: the correct first author is Sanidhya Vijayvargiya. Corrected to "S. Vijayvargiya."
- **[Body text, Production-incident corroboration] Understated CVSS score.** The Microsoft Semantic Kernel RCE disclosure (CVE-2026-26030, CVE-2026-25592) was described as "CVSS up to 9.8." Verified against the primary disclosure: CVE-2026-25592 carries CVSS 10.0. Corrected to "CVSS up to 10.0."

**Verified and confirmed correct (no change).** Several entries were independently re-checked and found accurate despite initial uncertainty during verification, and are reported here for transparency: the four conference-venue attributions that could not be confirmed via each paper's arXiv "Comments" metadata field (NeurIPS 2025 for ref19, NeurIPS 2024 for ref21, COLM 2025 for ref24, ICML 2025 for ref32) were all independently confirmed correct via each venue's own proceedings/poster listing; CVE-2025-64671 (ref33, Reprompt) does not resolve through the NVD/CVE.org web UI used in one verification pass (a JavaScript-rendering limitation of that lookup path, not evidence of an invalid CVE) but is confirmed valid via OSV.dev and the disclosure timeline (Microsoft patched it 2026-01-13, consistent with the "Jan. 2026" citation date); CVE-2025-32711 (EchoLeak, ref28) and CVE-2026-26030/CVE-2026-25592 (ref34) are all confirmed genuine and correctly attributed.

---

# Reviewer 1 {-}

**Recommendation:** Accept, no revisions.

**Response.** We thank Reviewer 1 for the review across both rounds and for confirming the revised manuscript is acceptable. No action required.

---

# Reviewer 2 {-}

## R2-1. "In Section RECORDS AND STORAGE, 'File Inventory' and 'Storage Locations' appear as bold text, what are these means? Please ensure the document structure is clear." {-}

**Response.** Confirmed — this was a genuine structural defect, not a formatting choice. The "File Inventory" subsection heading in RECORDS AND STORAGE was a vestigial artifact from an earlier draft: the actual File Inventory table (Table 2) was relocated to the Machine-Readable Encoding subsection during Revision 1, but the orphaned heading was left behind in RECORDS AND STORAGE with no content beneath it — immediately followed by the "Storage Locations" heading, producing exactly the confusing back-to-back bold-heading appearance Reviewer 2 flagged.

**Action.** The orphaned "File Inventory" heading is removed from RECORDS AND STORAGE. The section now opens directly with "Storage Locations," which has actual body content. (Because this is a whole-heading deletion rather than a text edit, it is not marked via the `changes` package — LaTeX `\subsection*{}` commands cannot be wrapped in tracked-changes markup without breaking compilation — but it is disclosed here per standard practice for whole-element deletions in this revision cycle.)

## R2-2. "The caption for Figure 1 repeats the exact text of the paragraph directly above it. This is redundant. The caption should be a concise summary, not a duplicate of the body text." {-}

**Response.** Confirmed. The caption's second and third sentences closely paraphrased the BACKGROUND section's second paragraph and the paragraph immediately preceding the figure in reading order.

**Action.** Figure 1's caption is rewritten as a single concise sentence summarizing what the figure shows, without restating the surrounding prose: "Threat framework coverage gap: ATT&CK addresses human adversaries, ATLAS addresses adversaries targeting AI/ML systems, and ATX-1 addresses the agent-resident failure surface neither covers—the conditions under which an agent's own action path produces destructive outcomes. The three taxonomies are complementary, not mutually exclusive."

## R2-3. "Many sentences use long em-dash parentheticals... overuse makes the text feel cluttered. Consider breaking some into separate sentences." {-}

**Response.** Agreed for the clearest cases, including the exact example cited.

**Action.** Three of the most cluttered instances are rewritten as separate sentences:

- The Arora et al. sentence quoted in the review ("...including plan construction strategies, inter-agent context sharing, and fallback behaviors...") is split into two sentences.
- The opening BACKGROUND sentence defining autonomous AI agents is split into a definition sentence and a growth-trend sentence.
- The IDEsaster sentence in Production-incident corroboration is split at its em-dash into two sentences.

We did not attempt to eliminate every em-dash parenthetical in the manuscript — many are short, standard appositives that read naturally — to avoid introducing new errors under deadline in a 10-page document during a targeted revision pass.

## R2-4. "There is a visible formatting gap on Page 2." {-}

**Response.** We were unable to reproduce a literal blank-space gap in our own compiled PDF at the exact page Reviewer 2's copy showed it (pagination can shift slightly across LaTeX distributions/versions). However, the orphaned "File Inventory" heading identified in R2-1 is the strongest candidate: two bare bold subsection headings stacked with no content between them is exactly the kind of artifact that reads as a structural "gap" in a two-column IEEE layout, and its removal (R2-1) also tightens that page. Separately, we noticed Figures 1 and 2 (both full-width `figure*` floats) were landing stacked back-to-back at the top of the same page with no connecting text — visually dense in the same way. A `\FloatBarrier` was added between them so they no longer compete for the same page; Figure 2 now floats naturally to its own page. If a distinct gap remains in the copyedited/typeset version, we would welcome a page reference to address it directly.

**Action.** See R2-1. Figures 1 and 2 no longer share a page.

## R2-5. "Some sections read as a list of evidence points rather than a coherent narrative. The content would benefit from reorganization into a logical flow." {-}

**Response.** Agreed, most acutely in the *External Validation and Corroborating Evidence* subsection, where four bold-lead-in paragraphs (Controlled multi-agent evaluation, Corroborating-studies coverage, Production-incident corroboration, Cumulative empirical base) sat side by side with no connective framing — and the subsection's own introductory sentence promised "three lines of evidence" while delivering four, compounding the listy feel.

**Action.**

- The introductory sentence is rewritten to correctly frame all four subsections as "four converging lines of evidence, presented in order of increasing independence from the original dataset."
- A one-sentence transition is added at the start of each of the three subsequent paragraphs, explicitly linking it to what came before: "Beyond this controlled replication, independent research groups have separately converged on the same failure patterns" (into Corroborating-studies coverage); "These controlled and corroborating studies are further reinforced by incidents observed in production deployments, outside any research setting" (into Production-incident corroboration); "Taken together, these three lines of evidence substantially expand the taxonomy's empirical grounding beyond the original case studies" (into Cumulative empirical base).

The dense factual content of each paragraph is otherwise unchanged — the fix is connective framing, not a rewrite of the evidence itself.

## Additional typesetting corrections (not tied to a specific comment) {-}

While finalizing the tracked-changes PDF, three line-wrap defects were found and fixed — none change any wording, only how existing text wraps within the two-column layout:

- The `ACTION_PROPOSE {verb: drop_table, target: production_db}` code example (AEGIS mitigation, Worked Example section) was overrunning the column edge. Split across multiple `\texttt{}` spans so it wraps normally.
- References [17] and [34] each end in a long unbroken URL that was overrunning the column edge (and, in [34]'s case, the page margin). Both are now set with `\url{}` so they wrap at slashes/hyphens instead of running off the page.

**Note on the tracked-changes rendering.** During this pass we also confirmed that nesting a `\replaced{}{}` inside an already-`\added{}` paragraph — as opposed to placing them as siblings — can cause the LaTeX `changes` package's underline markup to fail catastrophically on long paragraphs (severe column overflow, not a cosmetic wrap issue). This was corrected internally; it has no effect on the manuscript's wording, only on how the tracked-changes markup renders.

---

# Summary of Changes {-}

| Reviewer/AE concern | Manuscript change |
|------------------|-------------------|
| AE-2: reference authenticity/completeness/consistency | 4 bibliography corrections (ref1 author+year, ref18 month, ref19 initials, ref23 initial) + 1 body-text CVSS correction; full 35-entry verification documented above |
| R2-1, R2-4: orphaned heading / structural gap | "File Inventory" heading removed from RECORDS AND STORAGE; Figures 1 and 2 separated onto different pages |
| R2-2: Figure 1 caption duplication | Caption rewritten as a single concise, non-duplicative sentence |
| R2-3: em-dash overuse | 3 representative sentences (including the reviewer's cited example) split into separate sentences |
| R2-5: listy evidence sections | Intro sentence corrected (3→4 lines of evidence); transition sentences added between all four *External Validation* subsections |
| (not comment-specific) | 3 line-wrap fixes: `ACTION_PROPOSE` code example, refs [17] and [34] URLs |

No changes were made to the dataset, the taxonomy content, the STIX bundle, or any numerical claim other than the CVSS correction above. No wording changed as part of the typesetting corrections.

We thank the reviewers and editors again for the thoroughness of this review. We look forward to your decision.

---

**License.** This document is released under the Creative Commons Attribution 4.0 International License (CC BY 4.0).
