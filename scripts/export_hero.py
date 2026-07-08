"""Export the hero triptych as clean, pixel-pure 1080x1080 full-color PNGs.

Selected set (Option A) — all from Batch 13, plate P2, timepoint T2, field f05,
for a cohesive same-session look:
    left   = RHO GFP           (I17)
    middle = RHO composite      (I17, DNA+AGP+Mito)
    right  = RHO_Cys110Tyr GFP  (C19)

The previous set (mixed T1/T2) is written to selected/hero/backup/ as a fallback.

    pixi run python scripts/export_hero.py
"""
import sys
import os

sys.path.insert(0, os.getcwd())
import numpy as np
from PIL import Image

from varchamp_qc import cpg
from varchamp_qc.channels import composite, normalize, channel_cmap

OUT = "selected/hero"
BACKUP = "selected/hero/backup"
os.makedirs(OUT, exist_ok=True)
os.makedirs(BACKUP, exist_ok=True)


def save_rgb(arr01, path):
    Image.fromarray((np.clip(arr01, 0, 1) * 255).astype(np.uint8)).save(path)
    print("wrote", path)


def gfp(ch):
    return channel_cmap("GFP")(normalize(ch["GFP"], 1.0, 99.0))[..., :3]


SITE = 5

# --- Selected (Option A): all B13 T2 ---
rho = cpg.fetch_channels("2025_01_27_B13A7A8P2_T2", "I17", SITE)
cys = cpg.fetch_channels("2025_01_27_B13A7A8P2_T2", "C19", SITE)
save_rgb(gfp(rho), f"{OUT}/01_RHO_GFP.png")
save_rgb(composite(rho, 1.0, 99.0), f"{OUT}/02_RHO_composite.png")
save_rgb(gfp(cys), f"{OUT}/03_RHO_Cys110Tyr_GFP.png")

# --- Backup: previous mixed-timepoint set (T1 ref + T2 variant) ---
rho_b = cpg.fetch_channels("2025_01_27_B13A7A8P2_T1", "I17", SITE)
cys_b = cpg.fetch_channels("2025_01_27_B13A7A8P2_T2", "C19", SITE)
save_rgb(gfp(rho_b), f"{BACKUP}/01_RHO_GFP.png")
save_rgb(composite(rho_b, 1.0, 99.0), f"{BACKUP}/02_RHO_composite.png")
save_rgb(gfp(cys_b), f"{BACKUP}/03_RHO_Cys110Tyr_GFP.png")

print("\nhero triptych (Option A) ready in", OUT, "| backup in", BACKUP)
