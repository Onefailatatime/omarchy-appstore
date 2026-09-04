# Unofficial Omarchy App Store

A community package browser for [Omarchy](https://omarchy.org): every package
in the official repo (`pkgs.omarchy.org`), searchable, with the one install
command Omarchy users actually type — `omarchy pkg add <name>`.

It serves no packages itself. It reads the official pacman database, hides the
`-debug` companions, and renders one static page. There is no framework or
tracker, and fonts are self-hosted. Profiles without a demo video can show a
verified gallery linked directly from the upstream repository README; images
remain on their original hosts and open full-size when clicked. YouTube demos
use privacy-enhanced embeds and are not requested until the visitor explicitly presses play. Styled
with the Tokyo Night tokens lifted from omarchy.org's own `root.css` so it reads
as family.

Not affiliated with Omacom or DHH — say so on the page, always.

## Build

```bash
python3 build.py
```

Fetches `https://pkgs.omarchy.org/stable/x86_64/omarchy.db` (falls back to the
cached copy in `data/` when offline), parses every `desc`, and writes
`dist/index.html` plus `dist/fonts/`. Needs Python 3.14+ for the stdlib
`compression.zstd` module — Omarchy ships it.

Re-run it whenever you deploy; the repo changes daily and the page bakes in
the sync date.

## Layout

```
parts/
  body.html   the page — hero, search, grid, detail dialog, footer, inline JS
  develop.html public packaging checklist and contributor tips
  about.html   short project description and builder bio
  terms.html   terms, ownership, licence, trademark, and warranty notices
  style.css   Tokyo Night tokens + components (fonts self-hosted from assets/)
resources/    portable Markdown resources, including the LLM-ready checklist
assets/fonts/ JetBrains Mono 400/700, latin, woff2
assets/images/ self-hosted site imagery
data/         cached omarchy.db (auto-refreshed on each online build)
dist/         generated site, package pages, sitemap, crawler files, and assets
```

The icon set includes SVG, ICO, 32px PNG, and 180px Apple-touch variants. The
The generated Netlify `_headers` file adds a restrictive content policy and standard browser
security headers while allowing the public GitHub request feed, upstream HTTPS
screenshots, and click-to-play YouTube embeds.

## Search and answer engines

The build generates one canonical page per package under `dist/apps/`, plus
`robots.txt`, `sitemap.xml`, `llms.txt`, page-specific metadata, JSON-LD, and
social preview assets for `https://omarchyapps.com`. Keep `SITE_URL` in
`build.py` aligned with the primary production domain.

## Community app requests

The homepage shows only the three most-upvoted open GitHub issues labeled
`app-request`. Visitors vote with a 👍 reaction on GitHub or send a prefilled
app-suggestion DM to `@jessyka_boat` on X. After reviewing a DM, the site owner
can create a public issue with the `app-request` label to add it to voting.
This keeps the homepage compact, avoids an unmoderated public submission form,
and adds no custom account system or database. Close a request when it no
longer belongs in the active wishlist; it then disappears from the homepage.

## Persistent package upvotes

Every package card and profile has a first-party upvote control backed by the
Netlify Function at `/api/votes` and the site-wide `omarchy-app-votes` Blob
store. Vote records survive deploys. A secure HTTP-only random browser cookie
prevents ordinary duplicate votes without storing an IP address or asking for
an account. The function uses one immutable Blob key per app/browser pair,
strong consistency, package allow-listing, same-origin POST checks, and Netlify
rate limiting. `data/indie.json` controls the curated Indie app stickers.

## Curated profiles

`data/enrichment.json` adds a researched tagline, longer description, pricing,
requirements, and optional media to package detail pages. Missing media is an
expected state: the profile falls back cleanly to text rather than guessing at
a screenshot or video.

`data/authors.json` supplies public creator attribution for every card. It uses
published full names where available and links to the creator's X profile,
personal site, official organization site, or public upstream profile. Keep
attribution conservative: never infer a private identity or publish maintainer
email addresses from package recipes.

Before replacing the shipped enrichment file, verify every remote media claim:

```bash
python3 tools/validate_enrichment.py candidates.json > data/enrichment.json
```

The validator makes a real request for each screenshot and YouTube ID and drops
claims that cannot be verified. Review its stderr report, then rebuild normally.

To refresh README galleries for profiles without a video, run:

```bash
python3 tools/discover_readme_screenshots.py
```

The discovery tool reads repository README files through GitHub, rejects common
badges and logos, verifies image responses in memory, and stores remote URLs and
source attribution only. It never saves the upstream image files.

## Deploy

Static folder: publish `dist/`. House rule: Netlify CLI only.
