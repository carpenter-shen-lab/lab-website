# VarChamp Batch-13 image QC & picker

Throwaway tooling (separate git worktree, branch `tooling/varchamp-image-qc`) to
grep **high-quality Cell Painting images** from the public Cell Painting Gallery
(`cpg0020-varchamp`, Batch 13) and pick a few for the lab website's front page.

Only the **final chosen images** get copied back into the website repo
(`src/assets/images/`). Nothing else here is meant to be merged.

## What it does

1. Reads the pre-computed image QC parquet from the reference repo
   [`broadinstitute/2025_varchamp_snakemake`](https://github.com/broadinstitute/2025_varchamp_snakemake)
   (no recompute) — per well × channel signal-to-noise + a background flag.
2. Ranks Batch-13 wells where all four fluorescent channels are strong
   (`is_bg == False`, high `s2n_ratio`), labeled with their gene/variant.
3. Streams the raw TIFFs anonymously from S3 (`botocore UNSIGNED`), caches them
   under `cache/`.
4. Renders single channels (correct LUTs) + an additive RGB composite, with
   interactive contrast/gain controls, in a marimo notebook.

Channel → color (reference palette, from `img_utils.py`):

| channel | compartment              | color  |
|---------|--------------------------|--------|
| DAPI    | DNA / nucleus            | blue   |
| GFP     | tagged protein variant   | green  |
| AGP     | actin / Golgi / membrane | yellow |
| Mito    | mitochondria             | red    |

## Environment

Nix provides the `pixi` binary; pixi manages the Python scientific stack
(conda-forge). direnv auto-loads the shell.

```bash
direnv allow            # once — loads the flake dev shell (provides pixi)
pixi install            # once — solves + downloads the Python env
```

If you don't use direnv, prefix pixi with nix: `nix run nixpkgs#pixi -- <cmd>`.

## Use

```bash
pixi run sheet          # headless: contact sheet of top wells -> selected/_contact_sheet_f05.png
pixi run edit           # interactive marimo picker (browser)
```

In the picker: choose a candidate well, scan its 9 fields, tune contrast/gains,
set a field, then **Save** — full-res PNGs (composite + each channel) land in
`selected/<name>/`.

## Then, back in the website repo

Copy the chosen composite (or channels) into
`../carpenter-shen-lab-website/src/assets/images/` and reference it from the
front page.
