"""Public catalog feed for other Omarchy store clients.

Everything about the feed lives in this one file:
  - dist/catalog/v1.json   the versioned feed (VERSION below)
  - dist/catalog.json      alias: byte-for-byte copy of the current version
  - dist/catalog.html      the public page that explains the feed and its terms
CORS and cache headers come from resources/netlify-headers (copied to dist/_headers).

To make a breaking change, bump VERSION (old files are not deleted, so v1 keeps
serving until you remove it by hand), update FIELDS and app_entry(), and rebuild.
Only fields the site already has real data for go in; empty values are dropped.
"""
import datetime
import html
import json

VERSION = "1"
STATUS = "preview"
ATTRIBUTION = "Catalog by omarchyapps.com"
PAGE_SLUG = "catalog"

# (field, description) — documents the feed on the public page. Keep in sync with app_entry().
FIELDS = [
    ("id", "Stable id, the same slug used in the app's omarchyapps.com URL."),
    ("name", "The app name as the store shows it (the package name)."),
    ("package", "Package name in the official Omarchy package repository."),
    ("install_command", "The install command exactly as the store shows it."),
    ("category", "The store's category for the app."),
    ("description", "One-line description from the package."),
    ("homepage", "The project's own site, when the package lists one."),
    ("repository", "The project's source repository, when it is known and differs from the homepage."),
    ("tutorial_url", "The store's tutorial or guide for the app, when one exists."),
    ("url", "The app's canonical page on omarchyapps.com. Link each app here."),
]


def app_entry(p: dict, site: str, slug, tutorial_path) -> dict:
    """One app. slug() and tutorial_path() come from build.py so URLs match the site exactly."""
    app_id = slug(p["name"])
    entry = {
        "id": app_id,
        "name": p["name"],
        "package": p["name"],
        "install_command": "omarchy pkg add " + p["name"],
        "category": p.get("category") or "",
        "description": (p.get("desc") or "").strip(),
        "homepage": p.get("url") or "",
        "repository": p.get("github") or "",
        "tutorial_url": site + tutorial_path(p["name"]) if tutorial_path(p["name"]) else "",
        "url": f"{site}/apps/{app_id}.html",
    }
    return {k: v for k, v in entry.items() if v}


def feed(pkgs: list[dict], site: str, slug, tutorial_path) -> dict:
    apps = [app_entry(p, site, slug, tutorial_path) for p in pkgs]
    return {
        "schema_version": VERSION,
        "status": STATUS,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "source": ATTRIBUTION,
        "attribution": ATTRIBUTION,
        "site": site + "/",
        "terms_url": f"{site}/{PAGE_SLUG}.html#terms",
        "docs_url": f"{site}/{PAGE_SLUG}.html",
        "app_count": len(apps),
        "apps": apps,
    }


def page(data: dict, site: str) -> tuple[dict, str]:
    """Guide-style page (rendered with parts/guide.html by build.py)."""
    e = html.escape
    feed_url = f"{site}/catalog/v{VERSION}.json"
    alias_url = f"{site}/catalog.json"
    example = dict(data, apps=data["apps"][:1])
    example_json = json.dumps(example, indent=2, ensure_ascii=False)
    rows = "".join(f"<li><code>{e(k)}</code>: {e(v)}</li>" for k, v in FIELDS)
    guide = {
        "slug": PAGE_SLUG,
        "title": "Omarchy App Catalog Feed (JSON) | Unofficial Omarchy App Store",
        "description": f"A free JSON feed of every app in the Unofficial Omarchy App Store, {data['app_count']} apps, for anyone building an Omarchy store client. Early preview.",
        "eyebrow": "Catalog feed",
        "heading": "The Omarchy app <span>catalog feed</span>",
        "tagline": "One free JSON file with every app this store lists, for anyone building an Omarchy app store client.",
        "answer": (f"Fetch {feed_url}. It lists all {data['app_count']} apps with install commands, categories, links and "
                   f"the omarchyapps.com page for each. It is free to use: show \"{ATTRIBUTION}\" and link each app "
                   "to its omarchyapps.com page. This is an early preview, so fields and terms may change."),
        "faqs": [
            ("Is the catalog feed free?", f"Yes. Anyone can use it, as long as the client shows \"{ATTRIBUTION}\" and links each app to its omarchyapps.com page."),
            ("How often does the feed update?", "It is rebuilt every time the store refreshes from the official Omarchy package repository, which happens twice a day."),
            ("Will the format change?", f"It might. The feed is an early preview. Breaking changes will ship under a new version number (v{int(VERSION) + 1}.json), and the version you use keeps its shape."),
            ("Is this an official Omarchy feed?", "No. The Unofficial Omarchy App Store is an independent community project, not affiliated with or endorsed by Omacom or David Heinemeier Hansson. Package facts come from pkgs.omarchy.org."),
        ],
    }
    faq_items = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in guide["faqs"])
    body = f"""    <nav class="guide-toc" aria-label="On this page">
      <strong>On this page</strong>
      <a href="#url">Feed URL</a><a href="#fields">Fields</a><a href="#example">Example</a><a href="#terms">Terms</a><a href="#faq">Questions</a>
    </nav>
    <section id="preview">
      <h2>An early preview</h2>
<p>This feed is new. Its fields and terms may change while people start building on it. When a change would break existing clients, it ships as a new version number, so code written for <code>v{VERSION}</code> keeps working. Right now the feed reports <code>"status": "{e(STATUS)}"</code>.</p>
    </section>
    <section id="url">
      <h2>Feed URL</h2>
<p>The versioned feed, best for clients:</p>
<pre style="white-space:pre-wrap;overflow-wrap:anywhere"><code>{e(feed_url)}</code></pre>
<p>A short alias that always points at the current version:</p>
<pre style="white-space:pre-wrap;overflow-wrap:anywhere"><code>{e(alias_url)}</code></pre>
<p>Both are plain JSON, can be read from any website or app (cross-origin requests are allowed), and are rebuilt each time the store syncs with the official Omarchy package repository, twice a day. Today the feed lists {data['app_count']} apps, the same apps you can browse on the <a href="/">home page</a>.</p>
<pre style="white-space:pre-wrap;overflow-wrap:anywhere"><code class="language-bash">curl -s {e(feed_url)}</code></pre>
    </section>
    <section id="fields">
      <h2>Fields</h2>
<p>The top of the file has <code>schema_version</code>, <code>status</code>, <code>generated_at</code> (ISO 8601 with offset), <code>source</code> and <code>attribution</code> (both "{e(ATTRIBUTION)}"), <code>terms_url</code>, <code>app_count</code>, and the <code>apps</code> array. Each app has these fields. A field is left out when the store has no real value for it, so check before you use it.</p>
<ul>{rows}</ul>
    </section>
    <section id="example">
      <h2>Example</h2>
<p>The start of the current feed, cut down to one app:</p>
<pre style="white-space:pre-wrap;overflow-wrap:anywhere"><code class="language-json">{e(example_json)}</code></pre>
    </section>
    <section id="terms">
      <h2>Terms</h2>
<ul>
<li>The feed is free for anyone to use, in open source and commercial clients alike.</li>
<li>Show "{e(ATTRIBUTION)}" somewhere people can see it in your client.</li>
<li>Link each app to its omarchyapps.com page (the <code>url</code> field).</li>
<li>Votes, ratings and reviews belong on omarchyapps.com: send people to the app's page to leave them.</li>
<li>The store is unofficial and the feed comes with no guarantee. Package facts come from pkgs.omarchy.org (the official <a href="https://github.com/omacom/omarchy-pkgs" target="_blank" rel="noopener">omarchy-pkgs</a> repository), and official upstream sources take precedence. The site's general <a href="/terms.html">Terms of Use</a> also apply.</li>
</ul>
<p>Building a client on the feed? Say hello to Jessyka, Creator of The Unofficial Omarchy App Store, on <a href="https://x.com/jessyka_boat" target="_blank" rel="noopener">X</a>.</p>
    </section>
    <section class="guide-faq" id="faq">
      <h2>Questions</h2>
{faq_items}
    </section>
"""
    return guide, body


def build(dist, pkgs: list[dict], site: str, slug, tutorial_path, render_page) -> list[tuple[str, list[str]]]:
    """Write the feed, its alias and the page. Returns sitemap entries (path, source files)."""
    data = feed(pkgs, site, slug, tutorial_path)
    text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    (dist / "catalog").mkdir(exist_ok=True)
    (dist / "catalog" / f"v{VERSION}.json").write_text(text, encoding="utf-8")
    (dist / "catalog.json").write_text(text, encoding="utf-8")
    guide, body = page(data, site)
    (dist / f"{PAGE_SLUG}.html").write_text(render_page(guide, body), encoding="utf-8")
    print(f"dist/catalog/v{VERSION}.json {len(text):,} bytes · {data['app_count']} apps (alias dist/catalog.json)")
    return [(f"/{PAGE_SLUG}.html", ["catalog.py"])]
