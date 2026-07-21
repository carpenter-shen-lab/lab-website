// Single source of truth for site-level identity, canonical URLs, and SEO
// defaults. BaseLayout (meta/OG/canonical), the JSON-LD entity, the sitemap
// (via `site` in astro.config), and shared components all draw from here so
// values stay in sync.
import { withBase } from './paths';

export const SITE = {
  name: 'Carpenter-Shen Lab',
  url: 'https://carpentershenlab.org', // canonical origin, no trailing slash

  defaultTitle: 'Carpenter-Shen Lab | Purdue University',
  // Original site description, only re-led with the lab name + Purdue so the
  // indexed snippet contains the query verbatim (see SEO plan, step 2).
  defaultDescription:
    'The Carpenter-Shen Lab at Purdue University develops and applies ' +
    'computational methods to make discoveries in cell images, accelerating ' +
    'drug discovery.',

  // Absolute-from-site paths (resolved against Astro.site in BaseLayout).
  // TODO: add a real 1200x630 social card at public/og-image.png, then point
  // defaultImage at '/og-image.png'. Until then the favicon keeps OG tags valid.
  defaultImage: '/favicon.svg',
  logoPath: '/favicon.svg', // used by JSON-LD `logo`

  twitterHandle: '@DrAnneCarpenter',

  // Paste the Google Search Console meta-tag token here to emit the
  // <meta name="google-site-verification"> tag (fast GSC verification path).
  googleSiteVerification: '',

  // Lab-level external profiles for JSON-LD `sameAs`. This array is what
  // disambiguates "Carpenter-Shen" from "Carpenter-Singh" for the Knowledge
  // Graph and AI retrieval — keep it accurate and growing.
  sameAs: [
    'https://github.com/carpenter-shen-lab',
    // TODO: add the org LinkedIn company page + any lab X/Bluesky handle.
  ],

  // Per-PI profile URLs for JSON-LD Person.sameAs (mirrors the team .md links).
  // (No Purdue departmental faculty pages exist yet; add them here when live.)
  people: {
    anneCarpenter: [
      'https://www.linkedin.com/in/annecarpenter1/',
      'https://github.com/AnneCarpenter',
      'https://x.com/DrAnneCarpenter',
      'https://orcid.org/0000-0003-1555-8261',
      'https://scholar.google.com/citations?user=pj6Bz0gAAAAJ&hl=en',
    ],
    runxiShen: [
      'https://www.linkedin.com/in/runxi-shen/',
      'https://github.com/runxi-shen',
      'https://x.com/wshenrx',
      'https://runxi-shen.github.io/cv/',
      'https://orcid.org/0000-0002-8883-5496',
      'https://scholar.google.com/citations?user=L9f8qagAAAAJ&hl=en',
    ],
  },
} as const;

// schema.org ResearchOrganization node for the homepage. Names Purdue as the
// parent org and both PIs as members, each with their external profiles, so
// search + AI tools resolve the lab as a distinct entity under purdue.edu.
export function organizationSchema() {
  return {
    '@type': 'ResearchOrganization',
    '@id': `${SITE.url}/#organization`,
    name: SITE.name,
    url: SITE.url,
    description: SITE.defaultDescription,
    logo: `${SITE.url}${withBase(SITE.logoPath)}`,
    parentOrganization: {
      '@type': 'CollegeOrUniversity',
      name: 'Purdue University',
      url: 'https://www.purdue.edu/',
    },
    member: [
      {
        '@type': 'Person',
        name: 'Anne E. Carpenter',
        jobTitle: 'Professor, Biological Sciences and Computer Science',
        sameAs: SITE.people.anneCarpenter,
      },
      {
        '@type': 'Person',
        name: 'Runxi Shen',
        jobTitle: 'Research Assistant Professor, Biological Sciences',
        sameAs: SITE.people.runxiShen,
      },
    ],
    sameAs: SITE.sameAs,
  };
}

// Shared site-level constants. Import from here so URLs and other values
// stay in sync across components (e.g. the header CTA and people-page CTA
// both reference the same joinUrl without duplication).
export const joinUrl =
  'https://docs.google.com/document/d/1R5kSSUX4A3x0CZYsTUdUtxPJYHRwZ04SIl5G06_MrlQ/preview?tab=t.0';
