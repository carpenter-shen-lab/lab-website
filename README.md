# Carpenter-Shen Lab

Source code and content for the Carpenter-Shen Lab website at Purdue University.

> **Note:** This website is under active development. Content and design may change frequently.

## Tech Stack

- [Astro](https://astro.build/) — static site generator
- [Tailwind CSS](https://tailwindcss.com/) — utility-first styling
- [MDX](https://mdxjs.com/) — Markdown with components

## Development

```bash
npm install        # Install dependencies
npm run dev        # Local dev server at localhost:4321/
npm run build      # Production build to dist/
npm run preview    # Preview production build
```

## Deployment

Deployed via GitHub Pages at the custom domain. Deployments are currently triggered manually with the `Deploy to GitHub Pages` workflow because the repository's push trigger has not been firing reliably.

- **Public site:** `https://carpentershenlab.org/`
- **GitHub Pages host:** `https://carpenter-shen-lab.github.io/` redirects to the custom domain
- **Astro configuration:** `site: 'https://carpentershenlab.org'` and `base: '/'`
- **Custom-domain binding:** `public/CNAME`

### Visibility Notes

- The **repository** (`carpenter-shen-lab/lab-website`) is public.
- The **deployed site** on GitHub Pages is always publicly accessible, even from a private repo. There is no built-in way to restrict access to collaborators only.
- For collaborator-only access during development, alternatives include Cloudflare Pages + Access, Netlify with password protection, or Vercel with password protection.
