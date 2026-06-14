#!/usr/bin/env python3
"""Generate the ATX-1 v2.4 threat-matrix figure (SVG + PDF) from canonical data.

Data-driven: reads docs/atx/v2/data/atx-1-techniques.json so the figure can never
drift from the spec. No severity coloring (removed in v2.3 for MITRE alignment).
The v2.4 addition (T6003 Poison Termination Judgment) is highlighted as "new".

Usage:
    python scripts/gen-threat-matrix-figure-v24.py            # writes SVG + PDF + PNG
"""
from __future__ import annotations
import json
import os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "docs/atx/v2/data/atx-1-techniques.json")
META = os.path.join(ROOT, "docs/atx/v2/atx-meta.json")
OUTDIR = os.path.join(ROOT, "docs/atx/v2/figures")
NEW_IN_V24 = {"T6003"}

# ---------------------------------------------------------------- palette
HEADER_BG = "#1e293b"; HEADER_TX = "#ffffff"; HEADER_ID = "#93c5fd"
CELL_BG = "#f8fafc"; CELL_BD = "#94a3b8"; CELL_ID = "#334155"; CELL_TX = "#0f172a"
NEW_BG = "#ecfeff"; NEW_BD = "#0891b2"; NEW_ID = "#0e7490"; NEW_TAG = "#0891b2"
BADGE_BG = "#e2e8f0"; BADGE_TX = "#475569"
TITLE_TX = "#0f172a"; SUB_TX = "#475569"; PAGE_BG = "#ffffff"

# ---------------------------------------------------------------- layout
MX, MY = 28, 24
COL_W, GAP = 158, 10
HDR_H, ROW_H = 66, 72
TITLE_H = 58
LEGEND_H = 46


def load_tactics():
    items = json.load(open(DATA, encoding="utf-8"))
    tactics = OrderedDict()
    for e in items:
        if "." in e["id"]:
            continue
        t = e["tactic"]
        tactics.setdefault(t, {"name": e.get("tactic_name", ""), "techs": []})
        nsub = sum(1 for s in items if s["id"].startswith(e["id"] + "."))
        tactics[t]["techs"].append((e["id"], e["name"], nsub))
    return tactics, items


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def wrap(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def text(x, y, s, size, color, *, weight="normal", anchor="start", mono=False, style="normal"):
    fam = ("ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, monospace" if mono
           else "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif")
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
            f'fill="{color}" font-weight="{weight}" text-anchor="{anchor}" '
            f'font-style="{style}">{esc(s)}</text>')


def rrect(x, y, w, h, r, fill, stroke, sw=1.0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def build():
    tactics, items = load_tactics()
    meta = json.load(open(META, encoding="utf-8"))
    n_cols = len(tactics)
    max_rows = max(len(v["techs"]) for v in tactics.values())
    n_tech = sum(len(v["techs"]) for v in tactics.values())
    n_sub = sum(1 for e in items if "." in e["id"])

    grid_w = n_cols * COL_W + (n_cols - 1) * GAP
    W = MX * 2 + grid_w
    grid_top = MY + TITLE_H
    H = grid_top + HDR_H + GAP + max_rows * (ROW_H + GAP) + LEGEND_H + MY

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="{PAGE_BG}"/>']

    # title block
    p.append(text(MX, MY + 22, "ATX-1 — AEGIS Threat Matrix", 22, TITLE_TX, weight="700"))
    p.append(text(MX, MY + 44,
                  f"Agentic Exploitation & Governance Intelligence Schema  ·  "
                  f"v{meta['version']}  ·  {meta['date']}",
                  11.5, SUB_TX))
    p.append(text(W - MX, MY + 44,
                  f"{n_cols} tactics  ·  {n_tech} techniques  ·  {n_sub} sub-techniques",
                  11.5, SUB_TX, anchor="end"))

    # columns
    for col, (tac, info) in enumerate(tactics.items()):
        x = MX + col * (COL_W + GAP)
        # header
        p.append(rrect(x, grid_top, COL_W, HDR_H, 7, HEADER_BG, "#334155", 0.8))
        p.append(text(x + COL_W / 2, grid_top + 16, tac, 11.5, HEADER_ID,
                      weight="700", anchor="middle", mono=True))
        nlines = wrap(info["name"], 22)[:3]
        ty = grid_top + 32 + (3 - len(nlines)) * 5
        for ln in nlines:
            p.append(text(x + COL_W / 2, ty, ln, 9.3, HEADER_TX, weight="600", anchor="middle"))
            ty += 11

        # technique cells
        for row, (tid, name, nsub) in enumerate(info["techs"]):
            y = grid_top + HDR_H + GAP + row * (ROW_H + GAP)
            new = tid in NEW_IN_V24
            bg, bd, idc = (NEW_BG, NEW_BD, NEW_ID) if new else (CELL_BG, CELL_BD, CELL_ID)
            p.append(rrect(x, y, COL_W, ROW_H, 6, bg, bd, 1.6 if new else 1.0))
            p.append(text(x + 9, y + 17, tid, 9.5, idc, weight="700", mono=True))
            if nsub:
                bw = 30
                p.append(rrect(x + COL_W - bw - 7, y + 6, bw, 14, 7, BADGE_BG, "none"))
                p.append(text(x + COL_W - bw / 2 - 7, y + 16, f"+{nsub}", 8.3, BADGE_TX,
                              weight="700", anchor="middle"))
            nlines = wrap(name, 26)[:3]
            ty = y + 32
            for ln in nlines:
                p.append(text(x + 9, ty, ln, 8.8, CELL_TX))
                ty += 10.5
            if new:
                p.append(text(x + COL_W - 7, y + ROW_H - 7, "NEW v2.4", 7.6, NEW_TAG,
                              weight="700", anchor="end", style="italic"))

    # legend / footer
    ly = H - MY - LEGEND_H + 18
    lx = MX
    p.append(rrect(lx, ly - 11, 16, 16, 4, NEW_BG, NEW_BD, 1.6))
    p.append(text(lx + 24, ly + 2, "New in v2.4 — T6003 Poison Termination Judgment "
                  "(LoopTrap, Xu et al., 2026)", 9.5, SUB_TX))
    p.append(rrect(lx + 430, ly - 11, 16, 16, 4, BADGE_BG, "none"))
    p.append(text(lx + 454, ly + 2, "+N  =  number of sub-techniques", 9.5, SUB_TX))
    p.append(text(W - MX, ly + 2,
                  "CC-BY-SA-4.0  ·  aegis-governance.com/atx-1  ·  "
                  "grounded in Agents of Chaos (Shapira et al., 2026) + RFC-0006",
                  8.6, SUB_TX, anchor="end"))

    p.append("</svg>")
    return "\n".join(p)


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    svg = build()
    svg_path = os.path.join(OUTDIR, "atx-1-threat-matrix-v2.4.svg")
    open(svg_path, "w", encoding="utf-8").write(svg)
    print("svg ->", svg_path)
    import cairosvg
    cairosvg.svg2pdf(bytestring=svg.encode("utf-8"),
                     write_to=os.path.join(OUTDIR, "atx-1-threat-matrix-v2.4.pdf"))
    cairosvg.svg2png(bytestring=svg.encode("utf-8"),
                     write_to=os.path.join(OUTDIR, "atx-1-threat-matrix-v2.4.png"),
                     output_width=1800, background_color="#ffffff")
    print("pdf + png written to", OUTDIR)


if __name__ == "__main__":
    main()
