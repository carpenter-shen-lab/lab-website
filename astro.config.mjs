import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // ─── Hosting Configuration ───────────────────────────────────────────
  // Custom domain carpentershenlab.org, served at the ROOT ('/').
  // The GitHub Pages host stays carpenter-shen-lab.github.io; the custom
  // domain is bound via public/CNAME. `site` MUST be the public origin so
  // canonical URLs, Open Graph tags, and the sitemap are absolute and correct.
  // (Under a custom domain GitHub serves the repo at '/', not '/lab-website'.)
  site: 'https://carpentershenlab.org',
  base: '/',
  // ─────────────────────────────────────────────────────────────────────

  output: 'static',
  integrations: [
    tailwind(),
    mdx(),
    // Emits /sitemap-index.xml (+ /sitemap-0.xml) from `site`. Referenced by
    // public/robots.txt and submitted to Google Search Console / Bing.
    sitemap(),
  ],
});
