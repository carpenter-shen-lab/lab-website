import { getCollection, type CollectionEntry } from 'astro:content';
import type { SocialLinkSet } from './social';

// Resolve team photos through Astro's asset pipeline. The .md files store a
// bare filename (e.g. "alan_munoz_resized.jpg"); this glob maps each filename
// to its processed, fingerprinted URL so paths stay correct under `base`.
const photoModules = import.meta.glob<{ default: { src: string } }>(
  '../assets/images/team/*.{jpg,jpeg,png,webp}',
  { eager: true }
);

const photosByFile: Record<string, string> = {};
for (const path in photoModules) {
  const file = path.split('/').pop()!;
  photosByFile[file] = photoModules[path].default.src;
}

export function teamPhoto(filename?: string): string | undefined {
  if (!filename) return undefined;
  const src = photosByFile[filename];
  if (!src) {
    // Fail loudly at build time, the way the old static imports did, instead
    // of rendering a broken <img> for a mistyped or missing filename.
    throw new Error(
      `Team photo "${filename}" not found in src/assets/images/team/. ` +
        `Fix the photo filename in the member's .md frontmatter or add the image.`
    );
  }
  return src;
}

// Display labels for the role badge, keyed by the schema's role enum.
export const roleLabels: Record<CollectionEntry<'team'>['data']['role'], string> = {
  'principal-investigator': 'Principal Investigator',
  'co-pi': 'Co-Principal Investigator',
  'senior-consultant': 'Senior Consultant',
  'senior-group-leader': 'Senior Group Leader',
  'postdoc': 'Postdoctoral Fellow',
  'phd-student': 'PhD Student',
  'research-scientist': 'Research Scientist',
  'visiting-scientist': 'Visiting Scientist',
  'admin': 'Administrator',
  'alumni': 'Alumni',
};

// Roles shown as large "lead" cards at the top. Everyone else visible is
// rendered in the smaller card grid below, so no role is ever silently
// dropped (e.g. un-hiding a senior-consultant, or adding an alumni member).
const LEAD_ROLES: readonly string[] = ['principal-investigator', 'co-pi'];

export interface TeamCardMember {
  name: string;
  roleLabel: string;
  title: string;
  photoSrc?: string;
  bio: string;
  links?: SocialLinkSet;
}

function toCardMember(entry: CollectionEntry<'team'>): TeamCardMember {
  const { name, role, title, photo, bio, links, affiliation } = entry.data;
  // Append the affiliation to the role badge (e.g. "Visiting Scientist, ONO Pharma").
  const roleLabel = affiliation ? `${roleLabels[role]}, ${affiliation}` : roleLabels[role];
  return { name, roleLabel, title, photoSrc: teamPhoto(photo), bio, links };
}

// Visible team members, split into the page's two card tiers and sorted by
// `order`. Members are excluded when `hidden` (e.g. pending sign-off) or when
// `active` is explicitly false (e.g. they have left the lab).
export async function getTeamGrouped(): Promise<{ leads: TeamCardMember[]; members: TeamCardMember[] }> {
  const visible = (
    await getCollection('team', ({ data }) => !data.hidden && data.active !== false)
  ).sort((a, b) => a.data.order - b.data.order);

  const leads: TeamCardMember[] = [];
  const members: TeamCardMember[] = [];
  for (const entry of visible) {
    (LEAD_ROLES.includes(entry.data.role) ? leads : members).push(toCardMember(entry));
  }

  return { leads, members };
}
