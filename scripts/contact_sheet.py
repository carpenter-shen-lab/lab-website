"""Headless first look: render composite thumbnails of the top-ranked, distinct
Batch-13 wells into a single contact-sheet PNG. Also doubles as a smoke test of
the whole data path (QC parquet -> S3 TIFF stream -> composite render).

    pixi run python scripts/contact_sheet.py [N] [SITE]
"""
import sys
import os

sys.path.insert(0, os.getcwd())

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from varchamp_qc import cpg
from varchamp_qc.channels import composite

N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
SITE = int(sys.argv[2]) if len(sys.argv) > 2 else 5

ranked = cpg.rank_wells(top=200)

# dedup to distinct biological wells (collapse T1..T4 timepoints)
seen, rows = set(), []
for r in ranked.iter_rows(named=True):
    key = (r["plate_map_name"], r["well"])
    if key in seen:
        continue
    seen.add(key)
    rows.append(r)
    if len(rows) >= N:
        break

cols = 4
nrows = (len(rows) + cols - 1) // cols
fig, axes = plt.subplots(nrows, cols, figsize=(cols * 3.4, nrows * 3.6))
for ax, r in zip(axes.flat, rows):
    ch = cpg.fetch_channels(r["plate"], r["well"], SITE)
    ax.imshow(composite(ch, 1.0, 99.0))
    gene = r.get("gene_allele") or r.get("symbol") or "?"
    ax.set_title(f"{r['plate'].split('_')[3]} {r['well']} f{SITE:02d}\n{gene}  s2n≥{r['min_s2n']}", fontsize=8)
    ax.axis("off")
for ax in axes.flat[len(rows):]:
    ax.axis("off")

fig.suptitle(f"VarChamp Batch 13 — top {len(rows)} distinct wells (composite, field f{SITE:02d})", fontsize=12)
fig.tight_layout()
out = os.path.join("selected", f"_contact_sheet_f{SITE:02d}.png")
os.makedirs("selected", exist_ok=True)
fig.savefig(out, dpi=110, bbox_inches="tight")
print("wrote", out, "with", len(rows), "wells")
