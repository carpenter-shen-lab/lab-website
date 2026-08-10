# Carpenter-Shen Lab Website

Academic lab website for the **Carpenter-Shen Lab** at **Purdue University**.

## Tech Stack

- **Astro** (v5) — static site generator, content-first architecture
- **Tailwind CSS** (v3) — utility-first styling
- **MDX** — Markdown with components for content pages
- Content is managed via **Astro Content Collections** with Zod schemas in `src/content.config.ts`

## Project Structure

```
src/
├── assets/images/       ← All images (imported via Astro's asset pipeline)
│   ├── team/            ← Headshot photos
│   └── icons/           ← Research area icons (CellProfiler, Cell Painting)
├── assets/styles/
│   └── global.css       ← Design system: single Purdue-branded palette, typography, utilities
├── components/
│   ├── layout/          ← Header, Footer (ThemeSwitcher deprecated)
│   └── home/            ← Hero, ResearchHighlights, LatestNews, SoftwareShowcase, TeamPreview (legacy)
├── content/             ← Markdown content (team, papers, blog, research, software, positions)
├── layouts/             ← BaseLayout, PageLayout
└── pages/               ← Route pages
```

## Key Conventions

### Images
- All images live in `src/assets/images/` and are imported in component frontmatter (`import img from '...'`), NOT referenced as string paths from `public/`.
- `public/` is only for files the browser fetches directly by URL (favicon, robots.txt, CNAME).
- This ensures correct path resolution regardless of `base` URL config.

### Color Scheme
- Single light theme: warm cream hero/nav + white content cards, with a single dark footer.
- No theme switcher (dropped per Anne's feedback, issue #2).
- All colors use CSS custom properties in `src/assets/styles/global.css`.
- **Light surfaces** (hero, nav, content): warm cream page (#FAF7EF), white cards (#FFFFFF), dark text (#1A1A1A). Accents are Boilermaker Gold (#CFB991), Aged Gold (#8E6F3E, AA-safe for text/links), and Rush Gold (#DAAA00).
- **Footer**: the only dark surface, near-black (#1A1A1A) with Boilermaker Gold accents.
- **Legacy `--accent-teal`** now aliases Rush Gold (#DAAA00); teal is not in the Purdue palette (see [`.agents/skills/purdue-brand/reference/color.md`](.agents/skills/purdue-brand/reference/color.md)). Avoid using it for text on white (low contrast).
- Purdue brand reference: https://marcom.purdue.edu/our-brand/visual-identity/
- **Authoritative brand rules for this repo** live in [`.agents/skills/purdue-brand/`](.agents/skills/purdue-brand/) (palette, typography, logo, voice, checklist).
- **Signature accents (intentional extensions beyond the Purdue palette).** Runxi likes these and they are deliberately kept, scoped to the hero "Cell to Cure" wordmark only: **GFP green `#7CFF33`** (the "Cure" word), exposed as the `--cure-green` token in `global.css`. Not a convention violation — use the token, do not hardcode the hex, and do not spread it to other surfaces.

### Typography (Plus Jakarta Sans everywhere, plus one signature serif)
- **The body of the site uses one font: Plus Jakarta Sans** (free, Google Fonts). Per Runxi's preference, the old serif (Source Serif 4) and the Barlow family were dropped — do not reintroduce them. (Hanken Grotesk was trialed as a replacement and reverted — some of its letterforms, e.g. the double-f in "suffering", read oddly; don't re-swap to Hanken.)
- **One intentional exception (loved, kept):** the hero "Cell to Cure" wordmark uses **Fraunces** (warm high-contrast serif, Google Fonts), exposed as the `--font-cure` token in `global.css`. This is a deliberate, scoped extension — Fraunces is for the wordmark only and must not spread to headings or body copy.
- Purdue's real brand fonts (Acumin Pro, United Sans) are **paid Adobe Fonts** and cannot be self-hosted on the public GitHub Pages site, so Plus Jakarta Sans stands in as a free Acumin/Proxima-style geometric sans. To use real Acumin, an Adobe Fonts web-project kit ID would be required.
- All five font CSS variables (`--font-display`, `--font-heading`, `--font-body`, `--font-label`, `--font-condensed` in `global.css`) point to Plus Jakarta Sans. Kept as separate tokens for flexibility, but currently identical.
- **Two sources of truth for fonts** — `global.css` (CSS variables) AND `tailwind.config.mjs` (`fontFamily`, used by `font-*` utility classes like the footer's `font-body`). Change BOTH when swapping fonts, and **restart the dev server** (Tailwind config is not hot-reloaded).
- The wordmark **CARPENTER-SHEN LAB** uses Plus Jakarta at natural width (no condensed squeeze — `scaleX` distorts the letterforms).
- Section header pattern: a larger eyebrow (`.section-label`, ~1.2rem) over a smaller `h2` heading (capped ~2.5rem) so the pair reads balanced.
- Body paragraphs are globally `text-align: justify`; section subtitles under headers should be `text-center` to override it.

### Hosting
- Hosted on GitHub Pages at the **custom domain `https://carpentershenlab.org`** (`site: 'https://carpentershenlab.org'`, `base: '/'` in `astro.config.mjs`). The domain is bound via `public/CNAME`; the Pages host stays `carpenter-shen-lab.github.io` and 301-redirects to the custom domain. HTTPS is enforced and the domain is org-verified (anti-takeover).
- **Cloudflare DNS** (registrar + zone): apex and `www` are `CNAME` records to `carpenter-shen-lab.github.io`, **DNS-only (grey cloud)**. Do not proxy (orange) unless SSL/TLS is set to Full (strict), or GitHub cert provisioning / redirects break.
- **`base: '/'` gotcha:** use `withBase()` from `src/lib/paths.ts` for internal links/assets, never `` `${import.meta.env.BASE_URL}/path` `` (which double-slashes to `//path` at root base).
- **SEO / AI discovery** (all sourced from `src/lib/site.ts`): `@astrojs/sitemap` emits `/sitemap-index.xml` (submitted to Google Search Console + Bing); `public/robots.txt` (welcomes AI crawlers) + `public/llms.txt`; `BaseLayout` renders canonical + Open Graph + Twitter tags + a JSON-LD `ResearchOrganization` entity (`sameAs` disambiguates from the Broad-based Carpenter-Singh Lab); social card at `public/og-image.png`.
- **Deploys are triggered manually** via `workflow_dispatch` (`gh workflow run "Deploy to GitHub Pages" --ref main`) — the `push` trigger in `.github/workflows/deploy.yml` has not been firing on this repo, so a merge to `main` does not auto-deploy.
- The old personal repo (`runxi-shen/carpenter-shen-lab-website`) is archived; development continues in the org repo.

## Content

### People
- **Anne E. Carpenter** — Principal Investigator, Professor
- **Runxi Shen** — Co-Principal Investigator, Research Assistant Professor
- **Shantanu Singh** — Senior Consultant (not shown on homepage yet, maybe shown as a team member later), still need to consult Shantanu/Anne for their preferences

### Writing Style
- No em dashes in body text. Use commas or restructure sentences instead.
- Body paragraphs are justified (both-side aligned).
- Section headers use the `.section-label` class (uppercase Plus Jakarta, gold, flanked by decorative lines).

## Design workflow

Two skills cover frontend design on this repo. Use them together:

- **[purdue-brand](.agents/skills/purdue-brand/SKILL.md)** — encodes Purdue Marcom rules (palette, type, logo, voice, 77° diagonals). Loads first so brand constraints are in scope.
- **[impeccable](.agents/skills/impeccable/SKILL.md)** — design quality, composition, motion, audit. Reads `docs/PRODUCT.md` + `docs/DESIGN.md` (the loader auto-falls-back to `docs/`), which are already seeded with the Purdue rules.

Typical sequence for a visual change:

```
/purdue-brand audit            # baseline compliance check
/impeccable shape <surface>     # plan the design within brand constraints
/impeccable craft <surface>     # implement
/purdue-brand audit            # confirm no regressions
```

When brand and impeccable conflict (e.g. impeccable's "use OKLCH, never `#000`" vs Purdue's required exact hex values), **brand wins** for identity (colors, fonts, logo), impeccable wins for everything else (hierarchy, motion, spacing, contrast strategy).

## Development

```bash
npm run dev      # Local dev server at localhost:4321/lab-website
npm run build    # Static build to dist/
npm run preview  # Preview production build
```

## Reference
- The `_archive/` folder (gitignored) contains content snapshots from the original Carpenter-Singh Lab website at the Broad Institute for migration reference.
- Reference site: https://carpenter-singh-lab.broadinstitute.org/
