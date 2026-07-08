"""Explore RHO panel candidates across Batch 13 vs Batch 14 and all timepoints,
to find a cohesive, consistent triptych. Rows = the three panels; columns =
plate/timepoint. Field f05.

    pixi run python scripts/explore_rho.py [SITE]
"""
import sys
import os

sys.path.insert(0, os.getcwd())
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from varchamp_qc import cpg
from varchamp_qc.channels import composite, normalize, channel_cmap

SITE = int(sys.argv[1]) if len(sys.argv) > 1 else 5

cols = [f"2025_01_27_B13A7A8P2_T{t}" for t in (1, 2, 3, 4)] + \
       [f"2025_01_28_B14A7A8P2_T{t}" for t in (1, 2, 3, 4)]

rows = [
    ("RHO GFP (I17)", "I17", "gfp"),
    ("RHO comp (I17)", "I17", "comp"),
    ("Cys110Tyr GFP (C19)", "C19", "gfp"),
]


def gfp(ch):
    return channel_cmap("GFP")(normalize(ch["GFP"], 1.0, 99.0))[..., :3]


fig, axes = plt.subplots(3, 8, figsize=(8 * 2.6, 3 * 2.75))
for ri, (label, well, view) in enumerate(rows):
    for ci, plate in enumerate(cols):
        ax = axes[ri, ci]
        try:
            ch = cpg.fetch_channels(plate, well, SITE)
            ax.imshow(gfp(ch) if view == "gfp" else composite(ch, 1.0, 99.0))
        except Exception:
            ax.text(0.5, 0.5, "n/a", ha="center", va="center")
        b = "B13" if "B13" in plate else "B14"
        tp = plate.split("_")[-1]
        if ri == 0:
            ax.set_title(f"{b} {tp}", fontsize=10)
        if ci == 0:
            ax.set_ylabel(label, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])

fig.suptitle(f"RHO triptych candidates — Batch 13 vs 14 x timepoints (field f{SITE:02d})", fontsize=13)
fig.tight_layout()
out = f"selected/hero/_explore_rho_f{SITE:02d}.png"
fig.savefig(out, dpi=100, bbox_inches="tight")
print("wrote", out)
