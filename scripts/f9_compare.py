"""F9 reference vs a chosen F9 variant across all four timepoints, showing the
two views we care about: GFP alone (the tagged protein) and the DNA+AGP+Mito
morphology composite.

Layout (4 rows x 4 timepoints):
    row 0: F9 ref        GFP
    row 1: F9 ref        composite (DNA+AGP+Mito)
    row 2: VARIANT       GFP
    row 3: VARIANT       composite (DNA+AGP+Mito)

    pixi run python scripts/f9_compare.py [VARIANT] [SITE]
"""
import sys
import os

sys.path.insert(0, os.getcwd())
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from varchamp_qc import cpg
from varchamp_qc.channels import composite, normalize, channel_cmap

VARIANT = sys.argv[1] if len(sys.argv) > 1 else "F9_Cys28Arg"
SITE = int(sys.argv[2]) if len(sys.argv) > 2 else 5

rows = cpg.find_wells(alleles=["F9", VARIANT])
print(rows.select("plate", "well", "gene_allele", "node_type", "n_bg", "min_s2n", "avg_s2n"))

plates = sorted(rows["plate"].unique().to_list())  # ..._T1.._T4
by_allele = {"F9": {}, VARIANT: {}}
for r in rows.iter_rows(named=True):
    by_allele.setdefault(r["gene_allele"], {})[r["plate"]] = r["well"]

row_specs = [
    ("F9", "GFP"), ("F9", "COMP"),
    (VARIANT, "GFP"), (VARIANT, "COMP"),
]
gfp_cmap = channel_cmap("GFP")

fig, axes = plt.subplots(4, len(plates), figsize=(len(plates) * 3.4, 4 * 3.6))
for ri, (allele, view) in enumerate(row_specs):
    for ci, plate in enumerate(plates):
        ax = axes[ri, ci]
        well = by_allele.get(allele, {}).get(plate)
        if well is None:
            ax.text(0.5, 0.5, "n/a", ha="center", va="center"); ax.axis("off"); continue
        ch = cpg.fetch_channels(plate, well, SITE)
        if view == "GFP":
            ax.imshow(gfp_cmap(normalize(ch["GFP"], 1.0, 99.0)))
            tag = "GFP"
        else:
            ax.imshow(composite(ch, 1.0, 99.0))
            tag = "DNA+AGP+Mito"
        tp = plate.split("_")[-1]
        ax.set_title(f"{allele} · {well} · {tp}\n{tag}", fontsize=8)
        ax.axis("off")

fig.suptitle(f"F9 (ref) vs {VARIANT} — GFP alone vs morphology composite · field f{SITE:02d}", fontsize=12)
fig.tight_layout()
out = os.path.join("selected", f"_f9_compare_{VARIANT}_f{SITE:02d}.png")
os.makedirs("selected", exist_ok=True)
fig.savefig(out, dpi=120, bbox_inches="tight")
print("wrote", out)
