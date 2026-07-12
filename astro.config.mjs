import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  // ─── Hosting Configuration ───────────────────────────────────────────
  // GitHub Pages at https://carpenter-shen-lab.github.io/lab-website/
  // `base` MUST be the exact GitHub repo name (lab-website)
  // or every asset in production will 404 while local dev still works.
  site: 'https://carpenter-shen-lab.github.io',
  base: '/lab-website',
  // ─────────────────────────────────────────────────────────────────────

  output: 'static',
  integrations: [
    tailwind(),
    mdx(),
  ],
});
