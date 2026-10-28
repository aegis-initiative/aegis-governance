"""Generate fig4-trust-interactions.pdf: GFN-1's two structurally independent
trust mechanisms, matching the house palette used in fig1/fig2/fig3."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# House palette (consistent with fig3)
BLUE = "#1f4e79"
LIGHT_BLUE = "#d6e4f0"
GRAY = "#595959"
RED = "#a6192e"
GREEN = "#2e7d32"

fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.4)
ax.axis("off")

def box(x, y, w, h, text, fc=LIGHT_BLUE, ec=BLUE, fontsize=8.5, weight="normal", textcolor="black"):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                        linewidth=1.3, edgecolor=ec, facecolor=fc)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fontsize, weight=weight, color=textcolor, wrap=True)
    return b

def arrow(x1, y1, x2, y2, color=GRAY, style="-|>"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                         mutation_scale=12, linewidth=1.2, color=color)
    ax.add_patch(a)

# Title halves
ax.text(2.5, 6.1, "Federation Publisher Trust", ha="center", fontsize=10.5, weight="bold", color=BLUE)
ax.text(7.5, 6.1, "Agent Runtime Trust", ha="center", fontsize=10.5, weight="bold", color=BLUE)

# --- Left half: Federation publisher trust ---
box(0.3, 5.0, 4.4, 0.7, "Five weighted factors:\nB, H, Q, A, F  (GFN-1 §3.7)", fontsize=8)
arrow(2.5, 5.0, 2.5, 4.55)
box(0.3, 3.85, 4.4, 0.65, "T = 0.30B + 0.25H + 0.20Q + 0.15A + 0.10F", fontsize=8.5, weight="bold")
arrow(2.5, 3.85, 2.5, 3.4)
box(0.3, 2.75, 4.4, 0.6, "Exponential decay (λ=0.01,\nhalf-life ≈69 days)", fontsize=8)
arrow(2.5, 2.75, 2.5, 2.3)
box(0.3, 1.65, 4.4, 0.6, "Weights signal trust from\nremote federation nodes", fontsize=8)

# --- Right half: Agent runtime trust ---
box(5.3, 4.65, 4.4, 1.0,
    "Threat Detection Layer\n(Engine layer — binary,\nfires immediately on\nactive threat signals)",
    fc="#f6dede", ec=RED, fontsize=8)
box(5.3, 3.15, 4.4, 1.0,
    "Reputation Layer\n(Schema layer — graduated,\nlongitudinal, informs\nautonomy expansion)",
    fc="#e2efe2", ec=GREEN, fontsize=8)

# Non-override constraint, drawn as a blocked arrow from Reputation to Threat Detection
arrow(7.5, 4.15, 7.5, 4.6, color=GREEN, style="-")
ax.plot([7.15, 7.85], [4.4, 4.4], color=RED, linewidth=2.2, solid_capstyle="round")
ax.text(7.5, 2.85, "non-override constraint:\nno Reputation score softens\na Threat Detection block",
        ha="center", va="top", fontsize=7.6, style="italic", color=GRAY)

# Dividing line + "never shared" label
ax.plot([5.0, 5.0], [1.3, 6.0], color=GRAY, linewidth=1.0, linestyle=(0, (4, 3)))
ax.text(5.0, 1.0, "structurally independent — never share a score,\na decay function, or a combined threshold",
        ha="center", fontsize=7.8, color=GRAY, style="italic")

plt.tight_layout()
plt.savefig("fig4-trust-interactions.pdf", bbox_inches="tight")
print("wrote fig4-trust-interactions.pdf")
