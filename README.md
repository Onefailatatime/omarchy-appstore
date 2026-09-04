# Unofficial Omarchy App Store

A community package browser for [Omarchy](https://omarchy.org): every package
in the official repo (`pkgs.omarchy.org`), searchable, with the one install
command Omarchy users actually type — `omarchy pkg add <name>`.

It serves no packages itself. It reads the official pacman database, hides the
`-debug` companions, and renders one static page. There is no framework or
tracker, and fonts are self-hosted. A small set of curated profiles can show a
verified screenshot from the app's own site; YouTube demos use privacy-enhanced
embeds and are not requested until the visitor explicitly presses play. Styled
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
  terms.html   terms, ownership, licence, trademark, and warranty notices
  style.css   Tokyo Night tokens + components (fonts self-hosted from assets/)
assets/fonts/ JetBrains Mono 400/700, latin, woff2
data/         cached omarchy.db (auto-refreshed on each online build)
dist/         what ships: index.html + fonts/, nothing else
```

## Curated profiles

`data/enrichment.json` adds a researched tagline, longer description, pricing,
requirements, and optional media to package detail pages. Missing media is an
expected state: the profile falls back cleanly to text rather than guessing at
a screenshot or video.

Before replacing the shipped enrichment file, verify every remote media claim:

```bash
python3 tools/validate_enrichment.py candidates.json > data/enrichment.json
```

The validator makes a real request for each screenshot and YouTube ID and drops
claims that cannot be verified. Review its stderr report, then rebuild normally.

## Deploy

Static folder: publish `dist/`. House rule: Netlify CLI only.
