"""Channel palette + rendering for VarChamp Cell Painting images.

The palette is the reference one used in broadinstitute/2025_varchamp_snakemake
(img_utils.py: channel_dict, channel_to_cmap, channel_to_rgb) for Batch 13.

VarChamp is a 4-fluorescent-channel assay (not the standard 5-channel Cell
Painting) because the experiment images GFP-tagged protein *variants*:
    ch1 DAPI  -> DNA / nucleus        (blue)
    ch2 GFP   -> tagged protein       (green)
    ch3 AGP   -> actin/Golgi/membrane (yellow)
    ch4 Mito  -> mitochondria         (red)
    ch5-7     -> brightfield          (not rendered)
"""
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, to_rgb

# Channel index inside the PerkinElmer filename: ...-ch{N}sk1fk1fl1.tiff
CHANNEL_NUM = {
    "DAPI": "1", "GFP": "2", "AGP": "3", "Mito": "4",
    "Brightfield1": "5", "Brightfield2": "6", "Brightfield": "7",
}

# All four fluorescent channels (shown as individual panels; brightfield excluded)
FLUOR_CHANNELS = ["DAPI", "GFP", "AGP", "Mito"]

# Channels blended into the morphology composite. GFP (the tagged protein) is
# deliberately excluded and shown on its own, so the composite is a clean
# cell-context backdrop (nuclei/cytoskeleton/mitochondria).
COMPOSITE_CHANNELS = ["DAPI", "AGP", "Mito"]

# Reference per-channel colors (exact hex from img_utils.channel_to_cmap)
CHANNEL_HEX = {
    "DAPI": "#0000FF",  # blue
    "GFP":  "#65fe08",  # green
    "AGP":  "#FFFF00",  # yellow
    "Mito": "#FF0000",  # red
}

# Human-readable labels for panel titles
CHANNEL_LABEL = {
    "DAPI": "DNA · DAPI",
    "GFP":  "Protein · GFP",
    "AGP":  "AGP",
    "Mito": "Mito",
}

CHANNEL_RGB = {k: np.array(to_rgb(v), dtype=np.float32) for k, v in CHANNEL_HEX.items()}


def channel_cmap(channel: str) -> LinearSegmentedColormap:
    """Black -> channel-color colormap for single-channel display."""
    color = CHANNEL_HEX.get(channel, "#FFFFFF")
    return LinearSegmentedColormap.from_list(f"{channel}_cmap", ["#000000", color])


def normalize(img: np.ndarray, low: float = 1.0, high: float = 99.0) -> np.ndarray:
    """Percentile contrast stretch to [0, 1] (display only, matches reference)."""
    img = img.astype(np.float32)
    lo, hi = np.percentile(img, low), np.percentile(img, high)
    if hi <= lo:
        hi = lo + 1.0
    return np.clip((img - lo) / (hi - lo), 0.0, 1.0)


def composite(
    channel_imgs: dict[str, np.ndarray],
    low: float = 1.0,
    high: float = 99.0,
    gains: dict[str, float] | None = None,
    use: list[str] | None = None,
) -> np.ndarray:
    """Additive RGB composite -> HxWx3 in [0,1].

    By default only the morphology channels (COMPOSITE_CHANNELS: DNA/AGP/Mito) are
    blended; GFP is excluded even if present in `channel_imgs`. Pass `use` to
    override the channel set.
    """
    gains = gains or {}
    use = use or COMPOSITE_CHANNELS
    first = next(iter(channel_imgs.values()))
    rgb = np.zeros((*first.shape, 3), dtype=np.float32)
    for ch in use:
        img = channel_imgs.get(ch)
        if img is None or ch not in CHANNEL_RGB:
            continue
        n = normalize(img, low, high) * float(gains.get(ch, 1.0))
        rgb += n[..., None] * CHANNEL_RGB[ch][None, None, :]
    return np.clip(rgb, 0.0, 1.0)
