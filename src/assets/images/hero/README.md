# Homepage Hero Artwork

These assets are intentionally tracked through Astro's image pipeline. Keep production and reference artwork in this directory rather than moving it to `public/`.

## Production

- `hero-cell-network-circle-champagne-motion-v3-4k-crisp.png` is the high-resolution production master for the slowly rotating cellular network. Its exact cream background and sharpened champagne line mask preserve definition under the hero's 1.9x zoom. Astro emits responsive WebP variants from this source.
- Reduced-motion mode uses this same production master with its rotation disabled, keeping the composition static and equally sharp without loading a separate fallback.

The champagne treatment is the current visual direction because it preserves the network detail without competing with the hero copy or Purdue identity.

## Reference Only

- `hero-cell-network-circle-champagne-motion-v3-4k.png` preserves the softer high-resolution reconstruction before deterministic contrast and edge refinement.
- `hero-cell-network-circle-charcoal-motion.png` preserves the square charcoal alternative.

The charcoal treatment has stronger contrast and may be useful in a future composition, but it is not approved for the current homepage. Do not import the charcoal asset into production without an explicit design request.

Reference-only files are deliberate design-history artifacts, not dead production dependencies. Do not delete, optimize in place, recolor, or overwrite them during routine cleanup.

## Versioning

Create a new versioned sibling when revising artwork. Preserve the prior approved source so visual changes remain reviewable and reversible. Update this file and the relevant Astro import when a new version becomes the production choice.
