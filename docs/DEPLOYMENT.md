# Deployment

## Hosting

- **Public site:** `https://carpentershenlab.org/`
- **GitHub Pages host:** `https://carpenter-shen-lab.github.io/` 301-redirects to the custom domain
- **Astro configuration:** `site: 'https://carpentershenlab.org'`, `base: '/'` in `astro.config.mjs`
- **Custom-domain binding:** `public/CNAME`
- **DNS:** Cloudflare. Apex and `www` are `CNAME` records to `carpenter-shen-lab.github.io`, DNS-only (grey cloud). Do not proxy unless SSL/TLS is set to Full (strict), or GitHub certificate provisioning and redirects break.

## Releasing

Deploys are triggered manually, because the `push` trigger in
`.github/workflows/deploy.yml` has not been firing reliably on this repository:

```bash
gh workflow run "Deploy to GitHub Pages" --ref main
```

## Visibility notes

- The repository (`carpenter-shen-lab/lab-website`) is public.
- The deployed site on GitHub Pages is always publicly accessible, even from a
  private repository. There is no built-in way to restrict access to
  collaborators only.
- For collaborator-only access during development, alternatives include
  Cloudflare Pages + Access, Netlify with password protection, or Vercel with
  password protection.
