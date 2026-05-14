import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ============================================================
# Figure 1: ATX-1 Threat Matrix
# ============================================================

tactics = [
    ("TA001\nAuthority\nBoundary\nViolation", [
        ("T1001", "Non-Owner\nInstruction\nCompliance", "high"),
        ("T1002", "Implicit\nAuthority\nAcceptance", "high"),
        ("T1003", "Mass Distrib.\nSpoofed\nAuthority", "critical"),
    ]),
    ("TA002\nDestructive\nAction", [
        ("T2001", "Irreversible\nCollateral\nAction", "critical"),
        ("T2002", "Cascading\nMulti-System\nDamage", "critical"),
        ("T2003", "Unvalidated\nBulk\nOperation", "high"),
    ]),
    ("TA003\nScope\nViolation", [
        ("T3001", "Autonomous\nScope\nExpansion", "high"),
    ]),
    ("TA004\nInformation\nBreach", [
        ("T4001", "Context Window\nData\nExfiltration", "critical"),
        ("T4002", "Cross-Session\nInfo Leakage", "high"),
    ]),
    ("TA005\nDeceptive\nOutput", [
        ("T5001", "False Task\nCompletion\nReport", "high"),
        ("T5002", "Hallucinated\nAction\nAttribution", "medium"),
    ]),
    ("TA006\nResource\nAbuse", [
        ("T6001", "Recursive\nSelf-Invocation\nLoop", "high"),
        ("T6002", "Unbounded\nExternal API\nConsumption", "medium"),
    ]),
    ("TA007\nMulti-Agent\nExploitation", [
        ("T7001", "Agent\nIdentity\nSpoofing", "critical"),
        ("T7002", "Delegation\nChain\nInjection", "high"),
    ]),
    ("TA008\nPersistence\nViolation", [
        ("T8001", "Memory\nPoisoning via\nInjected Context", "high"),
        ("T8002", "Governance\nState\nCorruption", "critical"),
    ]),
    ("TA009\nMonitoring\nEvasion", [
        ("T9001", "Silent\nProvider-Level\nTask Failure", "medium"),
    ]),
]

severity_colors = {
    "critical": {"bg": "#fee2e2", "border": "#dc2626", "text": "#991b1b"},
    "high":     {"bg": "#fef3c7", "border": "#d97706", "text": "#92400e"},
    "medium":   {"bg": "#dbeafe", "border": "#2563eb", "text": "#1e40af"},
    "low":      {"bg": "#dcfce7", "border": "#16a34a", "text": "#166534"},
}

col_w = 1.55
row_h = 0.82
hdr_h = 1.05
gap = 0.1
n_cols = len(tactics)
max_rows = max(len(t[1]) for t in tactics)

fw = n_cols * (col_w + gap) + 0.3
fh = hdr_h + max_rows * (row_h + gap) + 0.9

fig, ax = plt.subplots(figsize=(fw, fh))
ax.set_xlim(0, fw)
ax.set_ylim(0, fh)
ax.axis('off')
ax.set_aspect('equal')

ax.text(fw/2, fh - 0.1, 'ATX-1: AEGIS Threat Matrix', ha='center', va='top', fontsize=11, fontweight='bold')

y_hdr = fh - 0.35 - hdr_h

for col, (tac_label, techs) in enumerate(tactics):
    x = 0.15 + col * (col_w + gap)
    r = mpatches.FancyBboxPatch((x, y_hdr), col_w, hdr_h, boxstyle="round,pad=0.05",
                                 facecolor="#1e293b", edgecolor="#334155", linewidth=0.8)
    ax.add_patch(r)
    ax.text(x + col_w/2, y_hdr + hdr_h/2, tac_label, ha='center', va='center',
            fontsize=5.2, color='white', fontweight='bold', linespacing=1.1)

    for row, (tid, tname, sev) in enumerate(techs):
        y = y_hdr - (row + 1) * (row_h + gap)
        c = severity_colors[sev]
        r = mpatches.FancyBboxPatch((x, y), col_w, row_h, boxstyle="round,pad=0.04",
                                     facecolor=c["bg"], edgecolor=c["border"], linewidth=0.8)
        ax.add_patch(r)
        ax.text(x + col_w/2, y + row_h - 0.11, tid, ha='center', va='top',
                fontsize=4.8, color=c["text"], fontweight='bold', fontfamily='monospace')
        ax.text(x + col_w/2, y + row_h/2 - 0.06, tname, ha='center', va='center',
                fontsize=4.8, color='#1e293b', linespacing=1.05)
        ax.text(x + col_w/2, y + 0.07, sev.upper(), ha='center', va='bottom',
                fontsize=3.8, color=c["text"], fontweight='bold', fontstyle='italic')

# Legend
ly = 0.12
lx = 0.4
for i, (sev, c) in enumerate(severity_colors.items()):
    xx = lx + i * 2.1
    r = mpatches.FancyBboxPatch((xx, ly), 0.22, 0.18, boxstyle="round,pad=0.02",
                                 facecolor=c["bg"], edgecolor=c["border"], linewidth=0.5)
    ax.add_patch(r)
    ax.text(xx + 0.32, ly + 0.09, sev.capitalize(), va='center', fontsize=5.5, color=c["text"])

plt.tight_layout(pad=0.1)
plt.savefig('D:/Users/Finnoybu/Documents/IEEE/Data Descripters/atx1-submission/fig-matrix.pdf',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('D:/Users/Finnoybu/Documents/IEEE/Data Descripters/atx1-submission/fig-matrix.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print('Fig 1: ATX-1 Matrix saved')
plt.close()

# ============================================================
# Figure 2: Framework Gap Diagram
# ============================================================

fig, ax = plt.subplots(figsize=(7, 3.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4.2)
ax.axis('off')

ax.text(5, 4.1, 'Threat Framework Coverage Gap', ha='center', va='top',
        fontsize=12, fontweight='bold')

frameworks = [
    {"x": 0.3, "label": "MITRE ATT&CK", "color": "#dbeafe", "border": "#2563eb",
     "threat": "Human\nAdversary", "target": "Computer\nSystems", "arrow": "attacks",
     "scope": "Tactics & techniques for\nhuman threat actors against\nIT infrastructure"},
    {"x": 3.5, "label": "MITRE ATLAS", "color": "#fef3c7", "border": "#d97706",
     "threat": "Adversary", "target": "AI/ML\nSystems", "arrow": "attacks",
     "scope": "Tactics & techniques for\nadversaries targeting\nAI/ML models"},
    {"x": 6.7, "label": "ATX-1 (AEGIS)", "color": "#fee2e2", "border": "#dc2626",
     "threat": "AI Agent", "target": "Operational\nInfrastructure", "arrow": "acts on",
     "scope": "Tactics & techniques for\nungoverned AI agents acting\nas the threat source"},
]

for fw in frameworks:
    x, w = fw["x"], 2.8
    # Header
    r = mpatches.FancyBboxPatch((x, 3.0), w, 0.55, boxstyle="round,pad=0.08",
                                 facecolor=fw["color"], edgecolor=fw["border"], linewidth=1.2)
    ax.add_patch(r)
    ax.text(x+w/2, 3.27, fw["label"], ha='center', va='center', fontsize=9, fontweight='bold', color='#1e293b')

    # Threat box
    r = mpatches.FancyBboxPatch((x+0.05, 2.0), 1.1, 0.6, boxstyle="round,pad=0.06",
                                 facecolor='white', edgecolor='#64748b', linewidth=0.8)
    ax.add_patch(r)
    ax.text(x+0.6, 2.3, fw["threat"], ha='center', va='center', fontsize=6.5, fontweight='bold')

    # Arrow
    ax.annotate('', xy=(x+1.8, 2.3), xytext=(x+1.2, 2.3),
                arrowprops=dict(arrowstyle='->', color='#475569', lw=1.2))
    ax.text(x+1.5, 2.5, fw["arrow"], ha='center', va='bottom', fontsize=5, color='#64748b', fontstyle='italic')

    # Target box
    r = mpatches.FancyBboxPatch((x+1.65, 2.0), 1.1, 0.6, boxstyle="round,pad=0.06",
                                 facecolor='white', edgecolor='#64748b', linewidth=0.8)
    ax.add_patch(r)
    ax.text(x+2.2, 2.3, fw["target"], ha='center', va='center', fontsize=6.5, fontweight='bold')

    # Scope
    ax.text(x+w/2, 1.3, fw["scope"], ha='center', va='center', fontsize=6, color='#475569',
            linespacing=1.3, bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8fafc',
                                        edgecolor='#e2e8f0', linewidth=0.5))

# Gap callout
ax.text(5, 0.35, 'ATX-1 fills the gap: AI agents that are themselves the threat source',
        ha='center', va='center', fontsize=8, fontweight='bold', color='#dc2626',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#fef2f2', edgecolor='#fecaca', linewidth=1))

plt.tight_layout(pad=0.2)
plt.savefig('D:/Users/Finnoybu/Documents/IEEE/Data Descripters/atx1-submission/fig-gap.pdf',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('D:/Users/Finnoybu/Documents/IEEE/Data Descripters/atx1-submission/fig-gap.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print('Fig 2: Framework Gap Diagram saved')
plt.close()

print('\nAll figures saved.')
