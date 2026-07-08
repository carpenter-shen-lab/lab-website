"""Access to the public Cell Painting Gallery (cpg0020-varchamp, Batch 13).

Everything is read on the fly:
  - QC + allele metadata parquet come straight from the reference GitHub repo.
  - Raw TIFFs are streamed anonymously (UNSIGNED) from the public S3 bucket and
    cached under ./cache so interactive scrubbing does not re-download.
"""
import io
import functools
import urllib.request
from pathlib import Path

import boto3
import numpy as np
import polars as pl
import tifffile
from botocore import UNSIGNED
from botocore.config import Config

from .channels import CHANNEL_NUM, FLUOR_CHANNELS

BUCKET = "cellpainting-gallery"
BATCH = "2025_01_27_Batch_13"
IMG_BASE = f"cpg0020-varchamp/broad/images/{BATCH}/images/"

_REF_RAW = "https://raw.githubusercontent.com/broadinstitute/2025_varchamp_snakemake/main"
QC_PARQUET_URL = f"{_REF_RAW}/3.downstream_analyses/inputs/1.plate_well_qc_metrics/all_img_wells_qc.parquet"
ALLELE_META_URL = f"{_REF_RAW}/3.downstream_analyses/inputs/1.plate_well_qc_metrics/allele_meta_df.parquet"

# well letter (A..P) -> 2-digit microscope row
LETTER_ROW = {c: f"{i + 1:02d}" for i, c in enumerate("ABCDEFGHIJKLMNOP")}

CACHE = Path(__file__).resolve().parent.parent / "cache"


# --------------------------------------------------------------------------- S3
@functools.lru_cache(maxsize=1)
def _s3():
    return boto3.client("s3", config=Config(signature_version=UNSIGNED))


import re


def _batch_folder(plate_short: str) -> str:
    """Derive the S3 batch folder from a plate id.

    '2025_01_27_B13A7A8P2_T1' -> '2025_01_27_Batch_13'
    '2025_01_28_B14A7A8P2_T1' -> '2025_01_28_Batch_14'
    """
    m = re.match(r"(\d{4}_\d{2}_\d{2})_B(\d+)", plate_short)
    if not m:
        raise ValueError(f"cannot parse batch from plate {plate_short!r}")
    return f"{m.group(1)}_Batch_{m.group(2)}"


@functools.lru_cache(maxsize=16)
def _plate_folders(batch_folder: str) -> dict[str, tuple[str, str]]:
    """Map short plate id (QC `plate`) -> (image base prefix, full measurement folder)."""
    base = f"cpg0020-varchamp/broad/images/{batch_folder}/images/"
    r = _s3().list_objects_v2(Bucket=BUCKET, Prefix=base, Delimiter="/")
    folders = [p["Prefix"].split("/")[-2] for p in r.get("CommonPrefixes", [])]
    return {f.split("__")[0]: (base, f) for f in folders}


def plate_folders(batch_folder: str = BATCH) -> dict[str, tuple[str, str]]:
    return _plate_folders(batch_folder)


def image_key(plate_short: str, well: str, site, channel: str) -> str:
    base, full = _plate_folders(_batch_folder(plate_short))[plate_short]
    row, col = LETTER_ROW[well[0]], well[1:3]
    fn = f"r{row}c{col}f{int(site):02d}p01-ch{CHANNEL_NUM[channel]}sk1fk1fl1.tiff"
    return f"{base}{full}/Images/{fn}"


def fetch_tiff(plate_short: str, well: str, site, channel: str, use_cache: bool = True) -> np.ndarray:
    key = image_key(plate_short, well, site, channel)
    cache_path = CACHE / key.replace("/", "__")
    if use_cache and cache_path.exists():
        return tifffile.imread(cache_path)
    raw = _s3().get_object(Bucket=BUCKET, Key=key)["Body"].read()
    if use_cache:
        CACHE.mkdir(exist_ok=True)
        cache_path.write_bytes(raw)
    return tifffile.imread(io.BytesIO(raw))


def fetch_channels(plate_short: str, well: str, site, channels=None, use_cache: bool = True) -> dict[str, np.ndarray]:
    channels = channels or FLUOR_CHANNELS
    return {ch: fetch_tiff(plate_short, well, site, ch, use_cache) for ch in channels}


# ---------------------------------------------------------------------- metadata
@functools.lru_cache(maxsize=1)
def _read_remote_parquet(url: str) -> pl.DataFrame:
    return pl.read_parquet(io.BytesIO(urllib.request.urlopen(url).read()))


def load_qc() -> pl.DataFrame:
    return _read_remote_parquet(QC_PARQUET_URL)


def load_allele_meta() -> pl.DataFrame:
    return _read_remote_parquet(ALLELE_META_URL)


def _plate_map_name(plate_short: str) -> str:
    """'2025_01_27_B13A7A8P1_T2' -> 'B13A7A8P1_R1' (allele-meta plate_map_name)."""
    token = plate_short.split("_")[3]  # B13A7A8P1
    return f"{token}_R1"


def _well_s2n(batch: str = BATCH) -> pl.DataFrame:
    """Per plate+well signal-to-noise aggregate across the 4 fluorescent channels,
    tagged with the allele-meta plate_map_name for joining to gene/variant labels."""
    qc = load_qc().filter(
        (pl.col("Metadata_Batch") == batch) & (pl.col("channel").is_in(FLUOR_CHANNELS))
    )
    return (
        qc.group_by(["plate", "well"])
        .agg(
            pl.len().alias("n_ch"),
            pl.col("is_bg").sum().alias("n_bg"),
            pl.col("s2n_ratio").min().round(3).alias("min_s2n"),
            pl.col("s2n_ratio").mean().round(3).alias("avg_s2n"),
        )
        .with_columns(
            pl.col("plate")
            .map_elements(_plate_map_name, return_dtype=pl.Utf8)
            .alias("plate_map_name")
        )
    )


def _allele_labels(batch: str = BATCH) -> pl.DataFrame:
    return load_allele_meta().filter(pl.col("Metadata_Batch") == batch).select(
        pl.col("plate_map_name"),
        pl.col("imaging_well").alias("well"),
        "symbol", "gene_allele", "aa_change", "node_type",
    )


def find_wells(alleles=None, symbols=None, batch: str = BATCH) -> pl.DataFrame:
    """Look up specific wells by exact gene_allele and/or gene symbol.

    Returns one row per (plate, well) across ALL plates/timepoints that carry the
    allele, with per-well s2n — so you can pick the best-looking timepoint. Join is
    on plate_map + well (a well letter alone is a different allele on another plate).
    """
    meta = _allele_labels(batch)
    if alleles:
        meta = meta.filter(pl.col("gene_allele").is_in(list(alleles)))
    if symbols:
        meta = meta.filter(pl.col("symbol").is_in(list(symbols)))
    out = _well_s2n(batch).join(meta, on=["plate_map_name", "well"], how="inner")
    return out.sort(["gene_allele", "plate"])


def rank_wells(batch: str = BATCH, top: int = 80, include_alleles=None) -> pl.DataFrame:
    """Best wells: all 4 fluorescent channels present, none flagged background,
    ranked by the weakest channel's signal-to-noise (so every channel is strong).

    Adds gene/variant labels from the allele metadata. `include_alleles` pins
    specific gene_alleles (e.g. ["F9", "F9_Cys28Arg"]) to the top of the list even
    when they fall below the top-N signal cutoff.
    """
    agg = (
        _well_s2n(batch)
        .filter((pl.col("n_ch") == 4) & (pl.col("n_bg") == 0))
        .sort("min_s2n", descending=True)
        .head(top)
        .join(_allele_labels(batch), on=["plate_map_name", "well"], how="left")
    )

    if include_alleles:
        pinned = find_wells(alleles=include_alleles, batch=batch)
        agg = pl.concat([pinned, agg], how="diagonal_relaxed").unique(
            subset=["plate", "well"], keep="first", maintain_order=True
        )
    return agg


def well_label(row: dict) -> str:
    """Compact human label for a ranked-well row."""
    gene = row.get("gene_allele") or row.get("symbol") or "?"
    return f"{row['plate']}  {row['well']}  [{gene}]  s2n≥{row['min_s2n']}"
