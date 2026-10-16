"""Programmatic SEO pages: categories, the full apps list, Omarchy vs <distro>
comparisons and install guides for popular apps outside the repo.

Facts come only from data/seo-facts.json, where every claim carries the
official source it was taken from (data/seo-sources.md lists them all)."""
from __future__ import annotations

import html
import json
import re

FACTS_FILE = "seo-facts.json"


def _abs_links(template: str) -> str:
    # The guide template uses page-relative links; these pages live in
    # subfolders, so root them.
    return re.sub(r'href="(?!https?:|/|#|mailto:|__)([^"]+)"', r'href="/\1"', template)


def _src(url: str) -> str:
    host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
    return f' <a class="src" href="{html.escape(url)}" target="_blank" rel="noopener">[{html.escape(host)}]</a>'


def _render(template, *, site, path, title, description, eyebrow, crumb_label, crumb_href, heading, tagline, answer, body, schema, synced, related):
    page = (_abs_links(template)
            .replace("__SITE_URL__/__SLUG__.html", site + path)
            .replace('<a href="/#guides">Guides</a>', f'<a href="{crumb_href}">{html.escape(crumb_label)}</a>')
            .replace("__TITLE__", html.escape(title))
            .replace("__DESCRIPTION__", html.escape(description))
            .replace("__EYEBROW__", html.escape(eyebrow))
            .replace("__HEADING__", heading)
            .replace("__TAGLINE__", html.escape(tagline))
            .replace("__ANSWER__", html.escape(answer))
            .replace("__BODY__", body)
            .replace("__RELATED_GUIDES__", related)
            .replace("__STRUCTURED_DATA__", json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
            .replace("__SYNCED__", synced)
            .replace("__SITE_URL__", site))
    return page


def _crumbs(site, items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": site + u} for i, (n, u) in enumerate(items, 1)]}


def _related(links):
    return "\n".join(f'<a class="related-guide" href="{h}"><strong>{html.escape(t)}</strong><span>{html.escape(d)}</span></a>' for h, t, d in links)


def build(*, root, dist, pkgs, categories, slug, display_name, guide_template, site, site_name, synced):
    """Writes the pages and returns [(path, source_paths)] for the sitemap."""
    facts = json.loads((root / "data" / FACTS_FILE).read_text(encoding="utf-8"))
    out = []
    # The fact-based pages change only when their facts do; date them by the
    # data file. Catalogue pages depend on the package data.
    fact_sources = ["data/seo-facts.json", "seo.py"]
    pkg_sources = ["data/omarchy.db", "data/categories.json", "data/enrichment.json", "seo.py"]

    def write(path, page, sources):
        target = dist / path.lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8")
        out.append((path, sources))

    def app_row(p):
        line = p.get("tagline") or p.get("desc") or ""
        return (f'<li><a href="/apps/{slug(p["name"])}.html"><strong>{html.escape(display_name(p))}</strong></a>'
                f' <code>omarchy pkg add {html.escape(p["name"])}</code><br><span>{html.escape(line)}</span></li>')

    by_cat = {c: [p for p in pkgs if p["category"] == c] for c in categories}
    cats = [c for c in categories if by_cat[c]]
    cat_links = [(f"/category/{slug(c)}.html", f"{c} apps for Omarchy", f"{len(by_cat[c])} packages from the official repo") for c in cats]

    for c in cats:
        items = by_cat[c]
        path = f"/category/{slug(c)}.html"
        title = f"{c} Apps for Omarchy: {len(items)} Packages"
        desc = (f"All {len(items)} {c.lower()} packages in the official Omarchy repository, each with its one-line install command "
                f"and a details page. Unofficial community directory.")[:160]
        body = (f'<section><h2>Every {html.escape(c.lower())} package</h2>'
                f'<p>Listed alphabetically. Categories are this site\'s own grouping; the packages and versions come from pkgs.omarchy.org.</p>'
                f'<ul class="seo-app-list">{"".join(app_row(p) for p in items)}</ul></section>')
        schema = {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "@id": site + path, "url": site + path, "name": title, "description": desc,
             "isPartOf": {"@type": "WebSite", "name": site_name, "url": site + "/"},
             "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
                 {"@type": "ListItem", "position": i, "url": f"{site}/apps/{slug(p['name'])}.html", "name": display_name(p)} for i, p in enumerate(items, 1)]}},
            _crumbs(site, [("Home", "/"), ("Apps list", "/omarchy-apps-list.html"), (c, path)])]}
        write(path, _render(guide_template, site=site, path=path, title=title, description=desc, eyebrow=c,
                            crumb_label="Apps list", crumb_href="/omarchy-apps-list.html",
                            heading=f"{html.escape(c)} apps for <span>Omarchy</span>", tagline=f"{len(items)} packages from the official Omarchy repository.",
                            answer=f"Install any of these with omarchy pkg add <name>. The list below has all {len(items)} {c.lower()} packages in the official repo as of {synced}.",
                            body=body, schema=schema, synced=synced,
                            related=_related([l for l in cat_links if l[0] != path][:6])), pkg_sources)

    path = "/omarchy-apps-list.html"
    title = f"Omarchy Apps List: All {len(pkgs)} Packages in the Official Repo"
    desc = f"The complete list of all {len(pkgs)} packages in the official Omarchy package repository, grouped by category, with install commands."[:160]
    sections = "".join(f'<section><h2 id="{slug(c)}"><a href="/category/{slug(c)}.html">{html.escape(c)}</a> ({len(by_cat[c])})</h2>'
                       f'<ul class="seo-app-list">{"".join(app_row(p) for p in by_cat[c])}</ul></section>' for c in cats)
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": site + path, "url": site + path, "name": title, "description": desc,
         "isPartOf": {"@type": "WebSite", "name": site_name, "url": site + "/"},
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(pkgs), "itemListElement": [
             {"@type": "ListItem", "position": i, "url": f"{site}/apps/{slug(p['name'])}.html", "name": display_name(p)} for i, p in enumerate(pkgs, 1)]}},
        _crumbs(site, [("Home", "/"), ("Apps list", path)])]}
    write(path, _render(guide_template, site=site, path=path, title=title, description=desc, eyebrow="Apps list",
                        crumb_label="Apps list", crumb_href=path, heading=f"Omarchy apps list: all <span>{len(pkgs)}</span> packages",
                        tagline="Every package in the official Omarchy repository, by category.",
                        answer=f"The official Omarchy package repository has {len(pkgs)} packages as of {synced}. Install any of them with omarchy pkg add <name>, or browse by category below.",
                        body=sections, schema=schema, synced=synced, related=_related(cat_links[:6])), pkg_sources)

    om = facts["omarchy"]
    vs_links = [(f"/vs/omarchy-vs-{k}.html", f"Omarchy vs {d['name']}", "Side-by-side facts from official sources") for k, d in facts["distros"].items()]
    for key, d in facts["distros"].items():
        path = f"/vs/omarchy-vs-{key}.html"
        name = d["name"]
        title = f"Omarchy vs {name}: Sourced Comparison (2026)"
        desc = f"Omarchy vs {name} compared on facts from omarchy.org and {name}'s official site: base, updates, packages and desktop. Every line is sourced."[:160]
        rows = []
        for label, okey, other in d["rows"]:
            o = om.get(okey) if okey else None
            ocell = (html.escape(o["text"]) + _src(o["src"])) if o else "<em>Not a point the Omarchy manual compares.</em>"
            rows.append(f"<tr><th scope=\"row\">{html.escape(label)}</th><td>{ocell}</td><td>{html.escape(other['text'])}{_src(other['src'])}</td></tr>")
        extra = [k for k in ("base", "release", "install", "secureboot", "firewall", "packages") if k not in {r[1] for r in d["rows"]}]
        omlist = "".join(f"<li>{html.escape(om[k]['text'])}{_src(om[k]['src'])}</li>" for k in extra)
        body = (f'<section><h2>Side by side</h2><div class="table-wrap"><table class="seo-compare"><thead><tr><th></th><th>Omarchy</th><th>{html.escape(name)}</th></tr></thead>'
                f'<tbody>{"".join(rows)}</tbody></table></div></section>'
                f'<section><h2>More about Omarchy</h2><ul>{omlist}</ul></section>'
                f'<section><h2>Sources</h2><p>Omarchy facts: <a href="https://omarchy.org/manual/">the Omarchy manual</a>. {html.escape(name)} facts: '
                f'<a href="{html.escape(d["site"])}">{html.escape(d["site"])}</a>. Checked {synced}. This site is not affiliated with either project.</p></section>')
        schema = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "@id": site + path + "#article", "headline": title, "description": desc, "url": site + path,
             "dateModified": synced, "author": {"@type": "Person", "name": "Jessyka", "url": site + "/about.html"},
             "publisher": {"@type": "Organization", "name": site_name, "url": site + "/"},
             "about": [{"@type": "SoftwareApplication", "name": "Omarchy", "applicationCategory": "OperatingSystem", "url": "https://omarchy.org/"},
                       {"@type": "SoftwareApplication", "name": name, "applicationCategory": "OperatingSystem", "url": d["site"]}]},
            _crumbs(site, [("Home", "/"), ("Guides", "/guides.html"), (f"Omarchy vs {name}", path)])]}
        write(path, _render(guide_template, site=site, path=path, title=title, description=desc, eyebrow="Comparison",
                            crumb_label="Guides", crumb_href="/guides.html", heading=f"Omarchy vs <span>{html.escape(name)}</span>",
                            tagline="Only what each project's official site says, with a source on every line.",
                            answer=f"{om['base']['text']} {name}: {d['rows'][0][2]['text']}",
                            body=body, schema=schema, synced=synced, related=_related([l for l in vs_links if l[0] != path])), fact_sources)

    in_repo = {p["name"] for p in pkgs}
    inst_links = [(f"/install/{g['slug']}-on-omarchy.html", f"Install {g['app']} on Omarchy", g["menu"]) for g in facts["install"]]
    for g in facts["install"]:
        assert g["slug"] not in in_repo, f"{g['slug']} is in the repo; it has an app page already"
        path = f"/install/{g['slug']}-on-omarchy.html"
        title = f"How to Install {g['app']} on Omarchy (2026)"
        desc = f"Install {g['app']} on Omarchy the official way: {g['menu']}. Step by step from the Omarchy manual, with the source linked."[:160]
        steps = "".join(f"<li>{html.escape(s)}</li>" for s in g["steps"])
        body = (f'<section><h2>Steps</h2><ol>{steps}</ol><p>{html.escape(g["note"])}{_src(g["src"])}</p></section>'
                f'<section><h2>Source</h2><p>From the official <a href="{html.escape(g["src"])}">Omarchy manual</a>, checked {synced}. '
                f'{html.escape(g["app"])} is not a package in the Omarchy repo, so it has no app page here; for repo apps use <a href="/omarchy-apps-list.html">the apps list</a>.</p></section>')
        schema = {"@context": "https://schema.org", "@graph": [
            {"@type": "HowTo", "@id": site + path + "#howto", "name": title, "description": desc, "url": site + path,
             "step": [{"@type": "HowToStep", "position": i, "text": s} for i, s in enumerate(g["steps"], 1)]},
            _crumbs(site, [("Home", "/"), ("Guides", "/guides.html"), (f"Install {g['app']}", path)])]}
        write(path, _render(guide_template, site=site, path=path, title=title, description=desc, eyebrow="Install guide",
                            crumb_label="Guides", crumb_href="/guides.html", heading=f"Install {html.escape(g['app'])} on <span>Omarchy</span>",
                            tagline=f"The official route: {g['menu']}.", answer=" ".join(g["steps"][:2]),
                            body=body, schema=schema, synced=synced, related=_related([l for l in inst_links if l[0] != path][:6])), fact_sources)
    return out
