import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import sys

    # notebook is launched from the worktree root (via `pixi run edit`)
    sys.path.insert(0, os.getcwd())

    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from PIL import Image

    from varchamp_qc import cpg, channels
    from varchamp_qc.channels import FLUOR_CHANNELS, CHANNEL_LABEL, channel_cmap, normalize, composite

    return (
        CHANNEL_LABEL,
        FLUOR_CHANNELS,
        Image,
        channel_cmap,
        composite,
        cpg,
        mo,
        normalize,
        np,
        os,
        plt,
    )


@app.cell
def _(mo):
    mo.md("""
    # VarChamp Batch 13 — high-quality image picker

    Ranked candidate wells (all four fluorescent channels strong, none flagged
    background) are pulled from the reference QC parquet. Pick a well, scan its
    9 fields, tune contrast, then **Save** the full-resolution PNGs to `selected/`.

    Channels → colors: **DAPI** blue · **GFP** green · **AGP** yellow · **Mito** red.
    """)
    return


@app.cell
def _(mo):
    # Pin specific gene_alleles to the top of the candidate list (e.g. F9 ref +
    # a variant). These show even if they fall below the top-N signal cutoff.
    allele_pin = mo.ui.text(
        value="F9, F9_Cys28Arg",
        label="Pin alleles (comma-separated gene_allele)",
        full_width=True,
    )
    allele_pin
    return (allele_pin,)


@app.cell
def _(allele_pin, cpg, mo):
    _pins = [a.strip() for a in allele_pin.value.split(",") if a.strip()]
    ranked = cpg.rank_wells(top=80, include_alleles=_pins or None)
    mo.md(
        f"**{ranked.height} candidate wells** — {len(_pins)} pinned "
        f"({', '.join(_pins) or 'none'}), rest ranked by weakest-channel signal-to-noise."
    )
    return (ranked,)


@app.cell
def _(cpg, mo, ranked):
    # dropdown: label -> row index
    _opts = {}
    for _i, _r in enumerate(ranked.iter_rows(named=True)):
        _opts[f"{_i:02d} · {cpg.well_label(_r)}"] = _i
    well_pick = mo.ui.dropdown(options=_opts, value=list(_opts)[0], label="Candidate well")
    well_pick
    return (well_pick,)


@app.cell
def _(mo):
    # contrast + per-channel gain controls. Composite = DNA+AGP+Mito (no GFP),
    # so only those three have gains; GFP is shown on its own single-channel panel.
    lo = mo.ui.slider(0.0, 10.0, value=1.0, step=0.5, label="vmin percentile")
    hi = mo.ui.slider(90.0, 100.0, value=99.0, step=0.1, label="vmax percentile")
    g_dapi = mo.ui.slider(0.0, 2.0, value=1.0, step=0.05, label="DAPI gain")
    g_agp = mo.ui.slider(0.0, 2.0, value=1.0, step=0.05, label="AGP gain")
    g_mito = mo.ui.slider(0.0, 2.0, value=1.0, step=0.05, label="Mito gain")
    mo.vstack([mo.hstack([lo, hi]), mo.hstack([g_dapi, g_agp, g_mito])])
    return g_agp, g_dapi, g_mito, hi, lo


@app.cell
def _(g_agp, g_dapi, g_mito):
    gains = {"DAPI": g_dapi.value, "AGP": g_agp.value, "Mito": g_mito.value}
    return (gains,)


@app.cell
def _(ranked, well_pick):
    sel = ranked.row(well_pick.value, named=True)
    plate, well = sel["plate"], sel["well"]
    return plate, sel, well


@app.cell
def _(composite, cpg, gains, hi, lo, plate, plt, well):
    # --- 9-field overview: composite thumbnail per site, to pick the best field ---
    fig_ov, axes_ov = plt.subplots(3, 3, figsize=(9, 9))
    for _s in range(1, 10):
        _ax = axes_ov.flat[_s - 1]
        try:
            _ch = cpg.fetch_channels(plate, well, _s)
            _ax.imshow(composite(_ch, lo.value, hi.value, gains))
        except Exception as _e:  # missing field
            _ax.text(0.5, 0.5, f"f{_s:02d}\n(n/a)", ha="center", va="center")
        _ax.set_title(f"f{_s:02d}", fontsize=9)
        _ax.axis("off")
    fig_ov.suptitle(f"{plate}  ·  well {well}  ·  composite by field", fontsize=11)
    fig_ov.tight_layout()
    fig_ov
    return


@app.cell
def _(mo):
    site = mo.ui.slider(1, 9, value=5, step=1, label="Field / site for detail + save")
    site
    return (site,)


@app.cell
def _(
    CHANNEL_LABEL,
    FLUOR_CHANNELS,
    channel_cmap,
    composite,
    cpg,
    gains,
    hi,
    lo,
    normalize,
    plate,
    plt,
    sel,
    site,
    well,
):
    # --- detail view for the chosen field: 4 single channels + composite ---
    chimgs = cpg.fetch_channels(plate, well, site.value)
    fig, axes = plt.subplots(1, 5, figsize=(20, 4.2))
    for _ax, _ch in zip(axes[:4], FLUOR_CHANNELS):
        _ax.imshow(normalize(chimgs[_ch], lo.value, hi.value), cmap=channel_cmap(_ch))
        _ax.set_title(CHANNEL_LABEL[_ch], fontsize=11)
        _ax.axis("off")
    axes[4].imshow(composite(chimgs, lo.value, hi.value, gains))
    axes[4].set_title("Composite · DNA+AGP+Mito", fontsize=11)
    axes[4].axis("off")
    _gene = sel.get("gene_allele") or sel.get("symbol") or "?"
    fig.suptitle(f"{plate} · {well} · f{site.value:02d} · {_gene}", fontsize=12)
    fig.tight_layout()
    fig
    return (chimgs,)


@app.cell
def _(mo, plate, sel, site, well):
    _gene = (sel.get("gene_allele") or sel.get("symbol") or "cell").replace(" ", "").replace("/", "-")
    default_name = f"varchamp_b13_{plate.split('_')[3]}_{well}_f{site.value:02d}_{_gene}"
    name_in = mo.ui.text(value=default_name, label="Save name", full_width=True)
    save_btn = mo.ui.run_button(label="💾 Save full-res PNGs to selected/")
    mo.vstack([name_in, save_btn])
    return name_in, save_btn


@app.cell
def _(
    FLUOR_CHANNELS,
    Image,
    channel_cmap,
    chimgs,
    composite,
    gains,
    hi,
    lo,
    mo,
    name_in,
    normalize,
    np,
    os,
    save_btn,
):
    mo.stop(not save_btn.value, mo.md("_Adjust the view, then press Save._"))

    outdir = os.path.join("selected", name_in.value)
    os.makedirs(outdir, exist_ok=True)

    def _save_rgb(arr01, path):
        Image.fromarray((np.clip(arr01, 0, 1) * 255).astype(np.uint8)).save(path)

    # composite (full 1080x1080)
    comp = composite(chimgs, lo.value, hi.value, gains)
    _save_rgb(comp, os.path.join(outdir, "composite.png"))

    # each channel, colored with its LUT
    saved = ["composite.png"]
    for _ch in FLUOR_CHANNELS:
        _n = normalize(chimgs[_ch], lo.value, hi.value)
        _rgba = channel_cmap(_ch)(_n)  # HxWx4 in [0,1]
        _save_rgb(_rgba[..., :3], os.path.join(outdir, f"{_ch}.png"))
        saved.append(f"{_ch}.png")

    mo.md(f"**Saved {len(saved)} PNGs** to `{outdir}/`:\n\n" + "\n".join(f"- {s}" for s in saved))
    return


if __name__ == "__main__":
    app.run()
