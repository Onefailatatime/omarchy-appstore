#!/usr/bin/env python3
"""Build the Unofficial Omarchy App Store — a static package browser for the official repo.

Reads the pacman database from pkgs.omarchy.org (falling back to the cached
copy in data/), joins it with the omarchy-pkgs git history for first-added
dates and PKGBUILD locations, joins it with the curated data/categories.json,
and writes one self-contained page plus fonts to dist/. No framework, no
tracker, no third-party requests — the store serves no packages itself, it
only prints the official install command.
"""

import datetime
import html
import io
import json
import pathlib
import re
import subprocess
import tarfile
import urllib.parse
import urllib.request
from compression import zstd  # stdlib since Python 3.14

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
DB_URL = "https://pkgs.omarchy.org/stable/x86_64/omarchy.db"
DB_CACHE = ROOT / "data" / "omarchy.db"
PKGS_REMOTE = "https://github.com/omacom/omarchy-pkgs"
PKGS_REPO = ROOT / "data" / "omarchy-pkgs"
CATEGORIES_FILE = ROOT / "data" / "categories.json"
ENRICHMENT_FILE = ROOT / "data" / "enrichment.json"
FALLBACK_CATEGORY = "Utilities"
NEW_ARRIVALS = 4
CONTACT_URL = "https://x.com/jessyka_boat"
X_DM_RECIPIENT_ID = "1400492097082327040"
SITE_URL = "https://omarchyapps.com"
SITE_NAME = "Unofficial Omarchy App Store"
FAQ = [
    ("What is the Unofficial Omarchy App Store?", "It is an independent, searchable directory of packages published by the official Omarchy package repository. It is not affiliated with or endorsed by Omarchy or Omacom."),
    ("How do I install an app on Omarchy?", "Open a package, review its requirements, then copy the displayed omarchy pkg add command into a terminal. Packages are downloaded from the official Omarchy repository, not from this site."),
    ("Does this site host or sell apps?", "No. The site hosts no packages and sells no software. It organizes public package information and links visitors to upstream projects and official PKGBUILDs."),
    ("How can a developer update or claim an app listing?", "Open the package and choose Claim this app. The X direct-message form asks for the developer's role, project URL, corrections, screenshots, and an optional demo video."),
    ("How can I prepare an app for Omarchy?", "Use the Develop for Omarchy checklist for packaging, permissions, checksums, desktop integration, clean-build testing, and pull-request preparation. Official repository guidance always takes precedence."),
]

# Fixed order controls both the catalogue's section order and the category
# filter row. Deliberately not alphabetical: biggest/most-relevant first.
CATEGORY_ORDER = [
    "AI & Agents", "Developer Tools", "Terminal & Shell", "Themes & Desktop",
    "System & Drivers", "Gaming & Emulation", "Media & Creative",
    "Productivity & Notes", "Security & Privacy", "Browsers & Web",
    "Communication", "Utilities",
]
# One hue per category, from Tokyo Night's documented palette (omarchy.org's
# own root.css only wires up the subset it uses on the marketing page — the
# rest of the theme's colors are still Tokyo Night, not invented). Blue,
# green, terminal-white, and turquoise are reserved elsewhere (body text,
# data/versions, headings, hover) so no category may use them. Big categories
# get the most mutually distinct hues since they appear most often; small
# ones can sit closer together. Every place a hue appears, the category name
# is always printed alongside it — color is a support signal, never the only one.
CATEGORY_COLOR = {
    "System & Drivers": "41A6B5",     # deep teal — 34 pkgs, the largest hued bucket
    "Utilities": "565F89",            # comment grey — 31 pkgs, deliberately unfiled-looking
    "Gaming & Emulation": "F7768E",   # red
    "Themes & Desktop": "9D7CD8",     # purple
    "AI & Agents": "7DCFFF",          # cyan
    "Developer Tools": "E0AF68",      # yellow
    "Media & Creative": "73DACA",     # teal-green
    "Terminal & Shell": "0DB9D7",     # cyan-blue
    "Security & Privacy": "DB4B4B",   # deep red
    "Productivity & Notes": "BB9AF7", # magenta
    "Browsers & Web": "737AA2",       # muted slate — 2 pkgs
    "Communication": "A9B1D6",        # near-white muted — 1 pkg
}


def fetch_db() -> bytes:
    # pkgs.omarchy.org 403s the default Python-urllib agent; identify like a client.
    req = urllib.request.Request(DB_URL, headers={"User-Agent": "omarchy-appstore-build/1.0"})
    try:
        raw = urllib.request.urlopen(req, timeout=30).read()
        DB_CACHE.write_bytes(raw)
        print(f"db: fetched fresh ({len(raw):,} bytes)")
    except OSError as e:
        raw = DB_CACHE.read_bytes()
        print(f"db: offline ({e}); using cached copy")
    return raw


def sync_pkgbuilds() -> None:
    """Blob-less clone of omarchy-pkgs: ~3 MB, and its history is the only
    source of 'when was this package added' — the pacman db only knows last build."""
    try:
        if (PKGS_REPO / ".git").exists():
            subprocess.run(["git", "-C", str(PKGS_REPO), "pull", "--ff-only", "--quiet"], check=True, timeout=120)
        else:
            subprocess.run(["git", "clone", "--quiet", "--filter=blob:none", PKGS_REMOTE, str(PKGS_REPO)], check=True, timeout=300)
        print("omarchy-pkgs: synced")
    except (subprocess.SubprocessError, OSError) as e:
        print(f"omarchy-pkgs: offline ({e}); using checkout as-is")


OMARCHY_PKGS_URLS = {"https://github.com/omacom-io/omarchy-pkgs", "https://github.com/omacom/omarchy-pkgs"}


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _related(pkgname: str, pkgbase: str, repo: str) -> bool:
    """A source array can carry a build-time toolchain download (a JDK, a
    vendored plugin) alongside the real project tarball — a bare 'found a
    github link' match can't tell those apart. Require the repo name to
    actually resemble the package before trusting it; a missed link is far
    cheaper than presenting a stranger's project as this one's."""
    r = _norm(repo)
    if not r:
        return False
    for cand in (pkgname, pkgbase):
        n = _norm(cand)
        n_stripped = re.sub(r"(bin|git|cli|dev)$", "", n)
        if n in r or r in n or (n_stripped and n_stripped in r):
            return True
    return False


def extract_github_repo(pkgbuild_text: str, pkg_url: str, pkgname: str = "", pkgbase: str = "") -> str | None:
    """Best-effort: find the package's own upstream GitHub repo (distinct from
    the omarchy-pkgs build recipe) by scanning PKGBUILD source=()/source_*=()
    arrays, substituting the PKGBUILD's own scalar variables (pkgname, pkgver,
    _appname, ...) where referenced. Returns None rather than guess wrong —
    a wrong link is worse than no link.

    Only worth attempting when the package's real homepage is NOT already a
    GitHub link: a source array often vendors a second, unrelated dependency
    from its own GitHub repo (e.g. omarchy-fish bundles fzf.fish, omarchy-zsh
    bundles omadots) — grabbing "the first github.com URL in source=" would
    silently present that unrelated project as if it were this one."""
    if pkg_url.startswith("https://github.com/"):
        return None
    scalars = {}
    for m in re.finditer(r"^(_?[a-zA-Z][\w]*)=(['\"]?)([^\n'\"]*)\2\s*$", pkgbuild_text, re.M):
        name, _, val = m.groups()
        if "(" not in val:
            scalars.setdefault(name, val)
    pm = re.search(r"^pkgname=([^\s(][^\n]*)", pkgbuild_text, re.M)
    if pm:
        scalars.setdefault("pkgname", pm.group(1).strip("'\""))

    def resolve(s: str) -> str:
        for _ in range(4):
            new = re.sub(r"\$\{?(\w+)\}?", lambda m: scalars.get(m.group(1), m.group(0)), s)
            if new == s:
                break
            s = new
        return s

    candidates = []
    for m in re.finditer(r"^source(?:_\w+)?=\(([^)]*)\)", pkgbuild_text, re.M | re.S):
        candidates.append(m.group(1))
    candidates.append(pkg_url or "")

    for block in candidates:
        for raw in re.findall(r"https://github\.com/[^\s'\")]+", block):
            resolved = resolve(raw)
            if "$" in resolved:
                continue
            m = re.match(r"https://github\.com/([\w.-]+)/([\w.-]+)", resolved)
            if not m:
                continue
            owner, repo = m.groups()
            repo = re.sub(r"\.git$", "", repo)
            url = f"https://github.com/{owner}/{repo}"
            if url in OMARCHY_PKGS_URLS:
                continue
            if not _related(pkgname, pkgbase, repo):
                continue
            return url
    return None


def pkgbuild_index() -> dict:
    """Map every pkgname and pkgbase in omarchy-pkgs to (directory, first-added
    timestamp, github repo url or None). Split packages (yaru-*,
    libretro-vice-*) live under one directory, so the directory — not
    pacman's %BASE% — is what a PKGBUILD link needs."""
    index = {}
    root = PKGS_REPO / "pkgbuilds"
    if not root.exists():
        return index
    for d in sorted(root.iterdir()):
        pkgbuild = d / "PKGBUILD"
        if not pkgbuild.exists():
            continue
        text = pkgbuild.read_text(encoding="utf-8", errors="replace")
        names = {d.name}
        for m in re.finditer(r"^pkg(?:name|base)=\(([^)]*)\)", text, re.M):
            names.update(n.strip("'\" ") for n in m.group(1).split())
        for m in re.finditer(r"^pkg(?:name|base)=([^\s(]+)", text, re.M):
            names.add(m.group(1).strip("'\""))
        um = re.search(r"^url=(['\"]?)([^\n'\"]*)\1", text, re.M)
        pkg_url = um.group(2) if um else ""
        bm = re.search(r"^pkgbase=([^\s(]+)", text, re.M)
        pkgbase = bm.group(1).strip("'\"") if bm else d.name
        github = extract_github_repo(text, pkg_url, pkgname=d.name, pkgbase=pkgbase)
        log = subprocess.run(
            ["git", "-C", str(PKGS_REPO), "log", "--diff-filter=A", "--format=%at", "--reverse", "--", f"pkgbuilds/{d.name}"],
            capture_output=True, text=True,
        ).stdout.split()
        added = int(log[0]) if log else 0
        for n in names:
            if n and not n.startswith("$"):
                index[n] = (d.name, added, github)
    return index


def parse_desc(text: str) -> dict:
    fields = {}
    for m in re.finditer(r"%(\w+)%\n((?:[^\n]+\n?)*)", text):
        fields[m.group(1)] = m.group(2).strip().split("\n")
    return fields


def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1000 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}".replace(".0 ", " ")
        n /= 1000
    return f"{n} GB"


def load_packages() -> list[dict]:
    raw = zstd.decompress(fetch_db())
    index = pkgbuild_index()
    categories = json.loads(CATEGORIES_FILE.read_text()) if CATEGORIES_FILE.exists() else {}
    enrichment = json.loads(ENRICHMENT_FILE.read_text()) if ENRICHMENT_FILE.exists() else {}
    pkgs = []
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        for member in tar.getmembers():
            if not member.name.endswith("/desc"):
                continue
            f = parse_desc(tar.extractfile(member).read().decode("utf-8"))
            name = f["NAME"][0]
            if name.endswith("-debug"):
                continue
            base = f.get("BASE", [name])[0]
            directory, added, github = index.get(name) or index.get(base) or (name, 0, None)
            url = f.get("URL", [""])[0]
            if url in OMARCHY_PKGS_URLS:
                # Some PKGBUILDs default url= to the packaging repo itself when
                # the underlying project genuinely has no homepage of its own —
                # that's not "their site", so don't present it as one.
                url = ""
            if github == url:
                github = None  # nothing to add — the project's site already is its GitHub repo
            prof = enrichment.get(name, {})
            pkgs.append({
                "name": name,
                "dir": directory,
                "version": f["VERSION"][0],
                "desc": f.get("DESC", [""])[0],
                "url": url,
                "github": github or "",
                "license": ", ".join(f.get("LICENSE", ["unknown"])),
                "csize": human_size(int(f["CSIZE"][0])),
                "isize": human_size(int(f["ISIZE"][0])),
                "built": int(f["BUILDDATE"][0]),
                "added": added,
                "deps": [re.split(r"[<>=]", d)[0] for d in f.get("DEPENDS", [])],
                "category": categories.get(name, FALLBACK_CATEGORY),
                "tagline": prof.get("tagline", ""),
                "full_desc": prof.get("description", ""),
                "pricing": prof.get("pricing", ""),
                "pricing_note": prof.get("pricing_note", ""),
                "requirements": prof.get("requirements", []),
                "screenshot_url": prof.get("screenshot_url", ""),
                "youtube_id": prof.get("youtube_id", ""),
                "youtube_title": prof.get("youtube_title", ""),
            })
    pkgs.sort(key=lambda p: p["name"])
    return pkgs


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def json_script(value: object) -> str:
    """Serialize JSON-LD without allowing a value to close its script tag."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def description_for(p: dict, limit: int = 158) -> str:
    text = re.sub(r"\s+", " ", p.get("full_desc") or p.get("desc") or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit - 1].rsplit(" ", 1)[0] + "…"


def claim_url(name: str) -> str:
    message = (
        f"Hi! I'd like to claim the {name} listing on the Unofficial Omarchy App Store.\n\n"
        "I can provide:\n- a correction or edit\n- screenshots of the app\n- a demo video\n\n"
        "Project URL: \nMy role with the app: "
    )
    return "https://x.com/messages/compose?" + urllib.parse.urlencode({
        "recipient_id": X_DM_RECIPIENT_ID,
        "text": message,
    })


def card(p: dict, featured: bool = False) -> str:
    e = {k: html.escape(str(v)) for k, v in p.items() if isinstance(v, str)}
    built = datetime.date.fromtimestamp(p["built"]).isoformat()
    added_date = datetime.date.fromtimestamp(p["added"]) if p["added"] else None
    added = added_date.isoformat() if added_date else ""
    deps = html.escape(json.dumps(p["deps"]))
    reqs = html.escape(json.dumps(p["requirements"]))
    cat_slug = slug(p["category"])
    cls = f"card cat-{cat_slug} featured" if featured else f"card cat-{cat_slug}"
    footer = (
        f'<span class="added">added {added_date.strftime("%b")} {added_date.day}</span><span class="size">{e["csize"]}</span>'
        if featured else
        f'<span class="cat-dot" aria-hidden="true"></span><span class="size">{e["csize"]}</span>'
    )
    detail_url = f"apps/{slug(p['name'])}.html"
    return f"""<article class="{cls}" data-detail-url="{detail_url}"
  data-name="{e['name']}" data-dir="{e['dir']}" data-version="{e['version']}" data-desc="{e['desc']}"
  data-url="{e['url']}" data-github="{e['github']}" data-license="{e['license']}" data-csize="{e['csize']}" data-isize="{e['isize']}"
  data-built="{built}" data-built-ts="{p['built']}" data-added="{added}" data-added-ts="{p['added']}"
  data-deps="{deps}" data-category="{e['category']}" data-cat="{cat_slug}"
  data-tagline="{e['tagline']}" data-full-desc="{e['full_desc']}" data-pricing="{e['pricing']}"
  data-pricing-note="{e['pricing_note']}" data-reqs="{reqs}" data-shot="{e['screenshot_url']}"
  data-yt="{e['youtube_id']}" data-yt-title="{e['youtube_title']}">
  <header><h3><a href="{detail_url}">{e['name']}</a></h3><span class="ver">{e['version']}</span></header>
  <p>{e['desc'] or '<em>No description provided.</em>'}</p>
  <footer>{footer}</footer>
</article>"""


def group_section(category: str, pkgs: list[dict]) -> str:
    cat_slug = slug(category)
    cards = "\n".join(card(p) for p in pkgs)
    return f"""<section class="group cat-{cat_slug}" data-cat="{cat_slug}">
  <h2><span class="dot" aria-hidden="true"></span>{html.escape(category)} <b>{len(pkgs)}</b></h2>
  <div class="grid">
{cards}
  </div>
</section>"""


def render_app_page(template: str, css: str, p: dict, synced: str) -> str:
    canonical = f"{SITE_URL}/apps/{slug(p['name'])}.html"
    desc = description_for(p)
    project_url = p.get("url") or p.get("github") or f"https://github.com/omacom/omarchy-pkgs/tree/master/pkgbuilds/{urllib.parse.quote(p['dir'])}"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareApplication",
                "@id": canonical + "#app",
                "name": p["name"],
                "description": p.get("full_desc") or p.get("desc") or "Omarchy package",
                "applicationCategory": p["category"],
                "operatingSystem": "Omarchy Linux",
                "softwareVersion": p["version"],
                "license": p["license"],
                "url": canonical,
                "sameAs": project_url,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": SITE_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": p["name"], "item": canonical},
                ],
            },
        ],
    }
    if p.get("screenshot_url"):
        schema["@graph"][0]["screenshot"] = p["screenshot_url"]
    if p.get("pricing") in ("free", "free-libre"):
        schema["@graph"][0]["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    reqs = "".join(f"<li>{html.escape(str(r))}</li>" for r in p.get("requirements", []))
    links = []
    if p.get("url"):
        links.append(f'<a class="button ghost" href="{html.escape(p["url"])}" target="_blank" rel="noopener">Project site ↗</a>')
    if p.get("github"):
        links.append(f'<a class="button ghost" href="{html.escape(p["github"])}" target="_blank" rel="noopener">GitHub ↗</a>')
    links.append(f'<a class="button ghost" href="https://github.com/omacom/omarchy-pkgs/tree/master/pkgbuilds/{urllib.parse.quote(p["dir"])}" target="_blank" rel="noopener">PKGBUILD ↗</a>')
    shot = (f'<figure class="shot-wrap"><img src="{html.escape(p["screenshot_url"])}" alt="{html.escape(p["name"])} app screenshot" width="1200" height="675"></figure>' if p.get("screenshot_url") else "")
    video = (f'<p><a class="button ghost" href="https://www.youtube.com/watch?v={html.escape(p["youtube_id"])}" target="_blank" rel="noopener">Watch: {html.escape(p["youtube_title"] or p["name"] + " demo")} ↗</a></p>' if p.get("youtube_id") else "")
    pricing = p.get("pricing_note") or p.get("pricing") or "Check the project site for current pricing."
    replacements = {
        "__STYLE__": css,
        "__SITE_URL__": SITE_URL,
        "__CANONICAL__": canonical,
        "__NAME__": html.escape(p["name"]),
        "__VERSION__": html.escape(p["version"]),
        "__CATEGORY__": html.escape(p["category"]),
        "__DESCRIPTION__": html.escape(desc),
        "__FULL_DESCRIPTION__": html.escape(p.get("full_desc") or p.get("desc") or "No description provided."),
        "__INSTALL_COMMAND__": html.escape("omarchy pkg add " + p["name"]),
        "__LICENSE__": html.escape(p["license"]),
        "__DOWNLOAD_SIZE__": html.escape(p["csize"]),
        "__INSTALLED_SIZE__": html.escape(p["isize"]),
        "__PRICING__": html.escape(pricing),
        "__REQUIREMENTS__": reqs or "<li>No special requirements documented.</li>",
        "__SCREENSHOT__": shot,
        "__VIDEO__": video,
        "__LINKS__": "".join(links),
        "__CLAIM_URL__": html.escape(claim_url(p["name"])),
        "__STRUCTURED_DATA__": json_script(schema),
        "__SYNCED__": synced,
    }
    page = template
    for key, value in replacements.items():
        page = page.replace(key, value)
    return page


def main() -> None:
    sync_pkgbuilds()
    pkgs = load_packages()
    synced = datetime.date.today().isoformat()

    newest = sorted((p for p in pkgs if p["added"]), key=lambda p: (-p["added"], p["name"]))[:NEW_ARRIVALS]
    newest_names = {p["name"] for p in newest}

    # Arrivals get their own featured card up top; skip them in the catalogue
    # below so nobody sees the same package twice on one page.
    by_cat: dict[str, list[dict]] = {c: [] for c in CATEGORY_ORDER}
    for p in pkgs:
        if p["name"] in newest_names:
            continue
        by_cat.setdefault(p["category"], []).append(p)
    groups = "\n".join(group_section(c, by_cat[c]) for c in CATEGORY_ORDER if by_cat.get(c))

    chips = "\n".join(
        f'<button class="chip cat-{slug(c)}" type="button" data-cat="{slug(c)}" aria-pressed="false">'
        f'<span class="dot" aria-hidden="true"></span>{html.escape(c)} <b>{len(by_cat.get(c, []))}</b></button>'
        for c in CATEGORY_ORDER if by_cat.get(c)
    )
    legend = " · ".join(
        f'<span class="cat-{slug(c)}"><span class="dot" aria-hidden="true"></span>{html.escape(c)}</span>'
        for c in CATEGORY_ORDER if by_cat.get(c)
    )
    cat_vars = "\n".join(f".cat-{slug(c)} {{ --cat: #{h}; }}" for c, h in CATEGORY_COLOR.items())

    body = (ROOT / "parts" / "body.html").read_text(encoding="utf-8")
    css = (ROOT / "parts" / "style.css").read_text(encoding="utf-8")
    faq_html = "\n".join(
        f"    <details><summary>{html.escape(question)}</summary><p>{html.escape(answer)}</p></details>"
        for question, answer in FAQ
    )
    homepage_schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": SITE_NAME, "alternateName": "Omarchy Apps", "description": "Searchable community directory of packages in the official Omarchy repository."},
            {"@type": "CollectionPage", "@id": SITE_URL + "/#webpage", "url": SITE_URL + "/", "name": SITE_NAME, "isPartOf": {"@id": SITE_URL + "/#website"}, "mainEntity": {"@type": "ItemList", "numberOfItems": len(pkgs), "itemListElement": [
                {"@type": "ListItem", "position": i, "url": f"{SITE_URL}/apps/{slug(p['name'])}.html", "name": p["name"]}
                for i, p in enumerate(pkgs, 1)
            ]}},
            {"@type": "FAQPage", "@id": SITE_URL + "/#faq", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in FAQ
            ]},
        ],
    }
    page = (body
            .replace("__NEW__", "\n".join(card(p, featured=True) for p in newest))
            .replace("__GROUPS__", groups)
            .replace("__CHIPS__", chips)
            .replace("__LEGEND__", legend)
            .replace("__COUNT__", str(len(pkgs)))
            .replace("__CATCOUNT__", str(len(CATEGORY_ORDER)))
            .replace("__NEWCOUNT__", str(len(newest)))
            .replace("__SYNCED__", synced)
            .replace("__SITE_URL__", SITE_URL)
            .replace("__FAQ__", faq_html)
            .replace("__STRUCTURED_DATA__", json_script(homepage_schema))
            .replace("__CONTACT__", html.escape(CONTACT_URL))
            .replace("__X_DM_RECIPIENT__", X_DM_RECIPIENT_ID)
            .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
    DIST.mkdir(exist_ok=True)
    (DIST / "index.html").write_text(page, encoding="utf-8")
    develop = ((ROOT / "parts" / "develop.html").read_text(encoding="utf-8")
               .replace("__SYNCED__", synced)
               .replace("__SITE_URL__", SITE_URL)
               .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
    (DIST / "develop.html").write_text(develop, encoding="utf-8")
    terms = ((ROOT / "parts" / "terms.html").read_text(encoding="utf-8")
             .replace("__SYNCED__", synced)
             .replace("__SITE_URL__", SITE_URL)
             .replace("__CONTACT__", html.escape(CONTACT_URL))
             .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
    (DIST / "terms.html").write_text(terms, encoding="utf-8")
    fonts = DIST / "fonts"
    fonts.mkdir(exist_ok=True)
    for f in (ROOT / "assets" / "fonts").glob("*.woff2"):
        (fonts / f.name).write_bytes(f.read_bytes())
    images = DIST / "images"
    images.mkdir(exist_ok=True)
    for f in (ROOT / "assets" / "images").glob("*"):
        if f.is_file():
            (images / f.name).write_bytes(f.read_bytes())
    about = ((ROOT / "parts" / "about.html").read_text(encoding="utf-8")
             .replace("__SYNCED__", synced)
             .replace("__CONTACT__", html.escape(CONTACT_URL))
             .replace("__SITE_URL__", SITE_URL)
             .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
    (DIST / "about.html").write_text(about, encoding="utf-8")
    apps_dir = DIST / "apps"
    apps_dir.mkdir(exist_ok=True)
    for old in apps_dir.glob("*.html"):
        old.unlink()
    app_template = (ROOT / "parts" / "app.html").read_text(encoding="utf-8")
    resolved_css = css.replace("__CATVARS__", cat_vars).replace("url(fonts/", "url(../fonts/")
    for p in pkgs:
        (apps_dir / f"{slug(p['name'])}.html").write_text(
            render_app_page(app_template, resolved_css, p, synced), encoding="utf-8"
        )

    sitemap_urls = [SITE_URL + "/", SITE_URL + "/develop.html", SITE_URL + "/about.html", SITE_URL + "/terms.html"]
    sitemap_urls.extend(f"{SITE_URL}/apps/{slug(p['name'])}.html" for p in pkgs)
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap.extend(f"  <url><loc>{url}</loc><lastmod>{synced}</lastmod></url>" for url in sitemap_urls)
    sitemap.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8"
    )
    (DIST / "llms.txt").write_text(
        f"# {SITE_NAME}\n\n"
        "> An independent directory of packages published by the official Omarchy package repository.\n\n"
        f"Canonical site: {SITE_URL}/\n\n"
        "This site is unofficial and is not affiliated with or endorsed by Omarchy, Omacom, or DHH. "
        "It does not host packages. Package facts are refreshed from pkgs.omarchy.org, and official upstream sources take precedence.\n\n"
        "## Main pages\n"
        f"- [Browse packages]({SITE_URL}/)\n"
        f"- [Develop for Omarchy]({SITE_URL}/develop.html)\n"
        f"- [About]({SITE_URL}/about.html)\n"
        f"- [Terms of Use]({SITE_URL}/terms.html)\n\n"
        "Contact: https://x.com/jessyka_boat\n", encoding="utf-8"
    )

    unresolved = [p["name"] for p in pkgs if not p["added"]]
    uncategorized = [p["name"] for p in pkgs if p["category"] == FALLBACK_CATEGORY and p["name"] not in json.loads(CATEGORIES_FILE.read_text() or "{}")]
    print(f"dist/index.html  {len(page):,} bytes · {len(pkgs)} packages · synced {synced}")
    print(f"dist/develop.html {len(develop):,} bytes · public packaging checklist")
    print(f"dist/terms.html   {len(terms):,} bytes · terms of use")
    print(f"dist/about.html   {len(about):,} bytes · project and builder bio")
    print(f"dist/apps/        {len(pkgs)} crawlable package pages")
    print(f"dist/sitemap.xml  {len(sitemap_urls)} canonical URLs")
    print("new arrivals:    " + ", ".join(f"{p['name']} ({datetime.date.fromtimestamp(p['added'])})" for p in newest))
    if unresolved:
        print(f"no git history for {len(unresolved)}: {', '.join(unresolved)}")
    if not CATEGORIES_FILE.exists():
        print("categories:      data/categories.json missing — everything filed under Utilities")
    elif uncategorized:
        print(f"uncategorized (fell back to Utilities): {', '.join(uncategorized)}")


if __name__ == "__main__":
    main()
