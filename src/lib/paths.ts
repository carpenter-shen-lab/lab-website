// Join an internal path onto the configured base URL, correct for any base
// ('/', '/lab-website', or a trailing-slash variant). Use this for every
// internal href/src instead of `${import.meta.env.BASE_URL}/path`, which
// produces a broken protocol-relative `//path` when the base is '/'.
const BASE = import.meta.env.BASE_URL;

export function withBase(path = '/'): string {
  const base = BASE.replace(/\/+$/, ''); // '' (root) or '/lab-website'
  const rel = path.replace(/^\/+/, ''); // drop leading slash(es)
  return rel ? `${base}/${rel}` : `${base}/`;
}
