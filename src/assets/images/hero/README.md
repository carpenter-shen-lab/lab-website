# Homepage Hero Artwork

These assets are intentionally tracked through Astro's image pipeline. Keep production and reference artwork in this directory rather than moving it to `public/`.

## Production

- `hero-cell-network-circle-champagne-motion-v4-4k-handdrawn.png` is the current high-resolution production master for the slowly rotating cellular network. It is the v3 etched network warped through a gentle, smoothed displacement field so the connecting lines gain a subtle hand-drawn wobble while the radial cell bodies stay crisp. Generated at the full 4096 master resolution; Astro emits responsive WebP variants from this source.
- Reduced-motion mode uses this same production master with its rotation disabled, keeping the composition static and equally sharp without loading a separate fallback.

The champagne treatment remains the visual direction: it preserves network detail without competing with the hero copy or Purdue identity.

## Reference Only

- `hero-cell-network-circle-champagne-motion-v3-4k-crisp.png` is the prior approved production master (crisp, un-warped). Retained so the v4 change stays reviewable and reversible.
- `hero-cell-network-circle-champagne-motion-v3-4k.png` preserves the softer high-resolution reconstruction before deterministic contrast and edge refinement.
- `hero-cell-network-champagne-v4-handdrawn-ref-{subtle,medium,loose}.png` are stronger hand-drawn warp settings kept for reference. They were **not** chosen: at amplitudes large enough to clearly read as hand-drawn, the ~1-2px linework fragments into a distressed, grainy texture and the radial cell bodies dissolve. That is a technical limit of warping thin raster lines, not an approved look; only the gentle setting adds character without shredding detail. (These are 2048px previews, not 4k.)
- `hero-cell-network-circle-charcoal-motion.png` preserves the square charcoal alternative. The charcoal treatment has stronger contrast and may be useful in a future composition, but it is not approved for the current homepage. Do not import the charcoal asset into production without an explicit design request.

Reference-only files are deliberate design-history artifacts, not dead production dependencies. Do not delete, optimize in place, recolor, or overwrite them during routine cleanup.

## Versioning

Create a new versioned sibling when revising artwork. Preserve the prior approved source so visual changes remain reviewable and reversible. Update this file and the relevant Astro import when a new version becomes the production choice.
