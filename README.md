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

## Local copy

```bash
git clone https://github.com/Onefailatatime/omarchy-appstore
cd omarchy-appstore
python3 build.py
python3 -m http.server -d dist 8000
```

The last command serves the built site at http://localhost:8000 until Ctrl-C.

The first build also clones `omacom/omarchy-pkgs` into `data/omarchy-pkgs`
(gitignored) for the first-added dates, so it needs git and network access.

The static server serves the pages. Upvotes and the newsletter form call the
Netlify Functions, which it does not run; `npx netlify dev` serves those.

The tests need Node 22.12+ and the one dependency:

```bash
npm ci
for t in tests/*.test.mjs; do node --test "$t"; done
```

## Build

`python3 build.py` fetches `https://pkgs.omarchy.org/stable/x86_64/omarchy.db`
(falls back to the cached copy in `data/` when offline), parses every `desc`, and writes
`dist/index.html` plus `dist/fonts/`. Needs Python 3.14+ for the stdlib
`compression.zstd` module — Omarchy ships it.

Re-run it whenever you deploy; the repo changes daily and the page bakes in
the sync date. Without a system Python 3.14, `uv run --python 3.14 --no-project
python build.py` works.

## How apps get in

The store has no submission form. Every listing comes from the official
`omacom/omarchy-pkgs` repository: a contributor opens a PKGBUILD pull request
there, the Omarchy maintainers merge and publish it to `pkgs.omarchy.org`, and
the next scheduled build here picks it up. Point people at `/develop.html`,
which covers the checklist, package size expectations, and the pull request.

## Automated builds

`.github/workflows/deploy.yml` rebuilds the site at 06:00 and 18:00 UTC, and
can be run on demand from the Actions tab. It runs `build.py` and the tests,
then commits the refreshed `dist/`, `data/omarchy.db`, and vote allow-list.
Netlify is connected to this repository and publishes every push to `main`,
so that commit is the deploy. GitHub only runs schedules from the default
branch. No secrets are needed.

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
security headers while allowing upstream HTTPS screenshots and click-to-play
YouTube embeds.

## Search and answer engines

The build generates one canonical page per package under `dist/apps/`, plus
`robots.txt`, `sitemap.xml`, `llms.txt`, page-specific metadata, JSON-LD, and
social preview assets for `https://omarchyapps.com`. Keep `SITE_URL` in
`build.py` aligned with the primary production domain.

## Community app requests

The homepage keeps requests to one compact call-to-action bar. Visitors send a
prefilled app-suggestion DM to `@jessyka_boat` on X; there is no public form,
account system, or request database on the site.

## Persistent package upvotes

Every package card and profile has a first-party upvote control backed by the
Netlify Function at `/api/votes` and the site-wide `omarchy-app-votes` Blob
store. Vote records survive deploys. A secure HTTP-only random browser cookie
prevents ordinary duplicate votes without storing an IP address or asking for
an account. The function uses one immutable Blob key per app/browser pair,
strong consistency, package allow-listing, same-origin POST checks, and Netlify
rate limiting. `data/indie.json` controls the curated Indie app stickers.

Each vote button doubles as a meter: `votes.js` fills it in proportion to the
most-voted app, so a full bar is the current leader and the hover title reads
"N of top M".

## Newsletter

Both the homepage and `/develop.html` carry a signup form posting to the
Netlify Function at `/api/subscribe`. It adds the address to the Resend
contacts (and a segment when one is configured) and emails the Develop for Omarchy checklist as a Markdown attachment; the
checklist is no longer published as a public file. `build.py` bakes
`resources/develop-for-omarchy.md` into `netlify/functions/checklist.mjs` on
every build. The function checks for an existing contact first, ignores
honeypot submissions, requires a same-origin POST, and is rate limited to five
requests per minute per IP.

Setup, once, in Resend (`resend.com`):

1. Add and verify the sending domain (`omarchyapps.com`); Resend lists the
   DNS records (DKIM, SPF, and a return-path MX) to add at the DNS host.
2. Optionally create a segment (Resend's replacement for audiences) to keep
   store subscribers apart from other contacts, and copy its ID.
3. Create an API key with full access.

Then set these environment variables on the Netlify site:

| Variable | Value |
| --- | --- |
| `RESEND_API_KEY` | the API key |
| `RESEND_SEGMENT_ID` | optional; the segment ID |
| `NEWSLETTER_FROM` | e.g. `Omarchy App Store <hello@omarchyapps.com>` |
| `NEWSLETTER_REPLY_TO` | optional; a mailbox you read, defaults to the from address |

Netlify applies environment variables at deploy time, so trigger a redeploy
after adding them — until it finishes the deployed function still runs with the
old values. Where the plan exposes variable scopes, include Functions: a
build-only variable never reaches `/api/subscribe`.

Until they are set the form reports that signup is not configured yet.

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

Static folder: publish `dist/`. Netlify publishes `main` on push; the Netlify
CLI remains the house rule for any manual deploy.
