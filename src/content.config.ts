import { defineCollection, z } from 'astro:content';
import { SOCIAL_KEYS } from './lib/social';

const team = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    role: z.enum([
      'principal-investigator',
      'co-pi',
      'senior-consultant',
      'senior-group-leader',
      'postdoc',
      'phd-student',
      'research-scientist',
      'visiting-scientist',
      'admin',
      'alumni',
    ]),
    title: z.string(),
    photo: z.string().optional(),
    email: z.string().email().optional(),
    // Social / profile links rendered by SocialLinks.astro. The supported
    // keys come from src/lib/social.ts so the schema, type, and renderer
    // stay in sync.
    links: z
      .object(Object.fromEntries(SOCIAL_KEYS.map((k) => [k, z.string().url().optional()])))
      .optional(),
    bio: z.string(),
    order: z.number().default(99),
    active: z.boolean().default(true),
    // When true, the member is kept in the collection but not rendered on the
    // People page (e.g. pending sign-off to be listed publicly).
    hidden: z.boolean().default(false),
    startDate: z.string().optional(),
    endDate: z.string().optional(),
    affiliation: z.string().optional(),
  }),
});

const papers = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    authors: z.array(z.string()),
    journal: z.string(),
    year: z.number(),
    volume: z.string().optional(),
    pages: z.string().optional(),
    doi: z.string().optional(),
    pmid: z.string().optional(),
    pdf: z.string().url().optional(),
    github: z.string().url().optional(),
    type: z.enum(['research', 'review', 'conference', 'preprint', 'book-chapter']).default('research'),
    highlight: z.boolean().default(false),
    labAuthors: z.array(z.string()).default([]),
  }),
});

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.date(),
    author: z.string(),
    excerpt: z.string(),
    category: z.enum(['how-to', 'announcement', 'general', 'release', 'career']).default('general'),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    draft: z.boolean().default(false),
    // Optional source links for this specific post (e.g. the LinkedIn announcements behind it)
    linkedin: z.array(z.object({ name: z.string(), url: z.string().url() })).optional(),
  }),
});

const research = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    icon: z.string().optional(),
    order: z.number().default(99),
  }),
});

export const collections = { team, papers, blog, research };
