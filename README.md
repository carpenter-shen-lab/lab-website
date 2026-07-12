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
npm run dev        # Local dev server at localhost:4321/lab-website
npm run build      # Production build to dist/
npm run preview    # Preview production build
```

## Deployment

Currently deployed via GitHub Pages. The site builds and deploys automatically on push to `main` via GitHub Actions.

- **GitHub Pages:** `https://carpenter-shen-lab.github.io/lab-website/`
- **Custom domain:** When ready, update `site` and `base` in `astro.config.mjs` and add a `CNAME` file in `public/`

### Visibility Notes

- The **repository** (`carpenter-shen-lab/lab-website`) is public.
- The **deployed site** on GitHub Pages is always publicly accessible, even from a private repo. There is no built-in way to restrict access to collaborators only.
- For collaborator-only access during development, alternatives include Cloudflare Pages + Access, Netlify with password protection, or Vercel with password protection.
