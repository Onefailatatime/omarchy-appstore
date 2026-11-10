"""Programmatic SEO pages: categories, the full apps list, Omarchy vs <distro>
comparisons and install guides for popular apps outside the repo.

Facts come only from data/seo-facts.json, where every claim carries the
official source it was taken from (data/seo-sources.md lists them all)."""
from __future__ import annotations

import html
import json
import re

FACTS_FILE = "seo-facts.json"
TITLE_MAX = 65
DESC_MAX = 160


def clamp_title(text: str, limit: int = TITLE_MAX) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"


def clamp_description(text: str, limit: int = DESC_MAX) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"


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
            .replace("__CRUMB__", f'<a href="{crumb_href}">{html.escape(crumb_label)}</a>')
            .replace("__FACTS__", "Independent editorial guide")
            .replace("__TITLE__", html.escape(clamp_title(title)))
            .replace("__DESCRIPTION__", html.escape(clamp_description(description)))
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


def _related(links, limit=4):
    links = links[:limit]
    return "\n".join(f'<a class="related-guide" href="{h}"><strong>{html.escape(t)}</strong><span>{html.escape(d)}</span></a>' for h, t, d in links)



def _plain(text: str) -> str:
    """Official repo wording, with typographic dashes folded so new page copy stays dash-free."""
    text = (text or "").replace("—", ", ").replace("–", ", ")
    text = re.sub(r"\s+-\s+", ", ", text)
    return re.sub(r"\s+", " ", text).strip()


def _join_examples(names: list[str]) -> str:
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + f" and {names[-1]}"


def build(*, root, dist, pkgs, categories, slug, display_name, guide_template, site, site_name, synced, merged=None, live_path=None):
    """Writes the pages and returns [(path, source_paths)] for the sitemap."""
    facts = json.loads((root / "data" / FACTS_FILE).read_text(encoding="utf-8"))
    merged = merged or {}
    out = []
    fact_sources = ["data/seo-facts.json", "seo.py"]
    pkg_sources = ["data/omarchy.db", "data/categories.json", "data/enrichment.json", "seo.py"]

    def live(path: str) -> str:
        if live_path:
            return live_path(path)
        return merged.get(path, path)

    def write(path, page, sources):
        if path in merged:
            return
        target = dist / path.lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8")
        out.append((path, sources))

    def app_href(p):
        return live(f"/apps/{slug(p['name'])}.html")

    def app_row(p):
        line = _plain(p.get("tagline") or p.get("desc") or "")
        href = app_href(p)
        return (f'<li><a href="{html.escape(href)}"><strong>{html.escape(display_name(p))}</strong></a>'
                f' <code>omarchy pkg add {html.escape(p["name"])}</code><br><span>{html.escape(line)}</span></li>')

    by_cat = {c: [p for p in pkgs if p["category"] == c] for c in categories}
    cats = [c for c in categories if by_cat[c]]
    cat_links = [(f"/category/{slug(c)}.html", f"{c} apps for Omarchy", f"{len(by_cat[c])} packages from the official repo") for c in cats]

    for c in cats:
        items = by_cat[c]
        path = f"/category/{slug(c)}.html"
        title = clamp_title(f"{c} apps for Omarchy ({len(items)} packages)")
        examples = []
        for p in items:
            line = _plain(p.get("tagline") or p.get("desc") or "").rstrip(".")
            label = display_name(p)
            examples.append(f"{label} ({line})" if line else label)
            if len(examples) == 3:
                break
        sample = _join_examples(examples)
        intro = (
            f"The {c} group has {len(items)} packages in the official Omarchy repository."
            + (f" Examples include {sample}." if sample else "")
            + " Install any of them with omarchy pkg add followed by the package name."
        )
        desc = clamp_description(
            f"{intro} Categories are this site's own grouping; packages and versions come from pkgs.omarchy.org."
        )
        body = (f'<section><h2>What you will find here</h2><p>{html.escape(intro)} '
                f"Categories are this site's own grouping; the packages and versions come from pkgs.omarchy.org.</p></section>"
                f'<section><h2>Every {html.escape(c.lower())} package</h2>'
                f'<p>Listed alphabetically, each with its one line install command and a details page.</p>'
                f'<ul class="seo-app-list">{"".join(app_row(p) for p in items)}</ul></section>')
        schema = {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "@id": site + path, "url": site + path, "name": title, "description": desc,
             "isPartOf": {"@type": "WebSite", "name": site_name, "url": site + "/"},
             "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
                 {"@type": "ListItem", "position": i, "url": site + app_href(p), "name": display_name(p)} for i, p in enumerate(items, 1)]}},
            _crumbs(site, [("Home", "/"), (c, path)])]}
        write(path, _render(guide_template, site=site, path=path, title=title, description=desc, eyebrow=c,
                            crumb_label="Apps", crumb_href="/",
                            heading=f"{html.escape(c)} apps for <span>Omarchy</span>", tagline=f"{len(items)} packages from the official Omarchy repository.",
                            answer=f"Install any of these with omarchy pkg add <name>. The list below has all {len(items)} {c.lower()} packages in the official repo as of {synced}.",
                            body=body, schema=schema, synced=synced,
                            related=_related([l for l in cat_links if l[0] != path])), pkg_sources)

    # The apps list page is merged to the homepage; only write it if it is still live.
    path = "/omarchy-apps-list.html"
    title = clamp_title(f"Omarchy apps list: all {len(pkgs)} official packages")
    desc = clamp_description(f"The complete list of all {len(pkgs)} packages in the official Omarchy package repository, grouped by category, with install commands.")
    sections = "".join(f'<section><h2 id="{slug(c)}"><a href="/category/{slug(c)}.html">{html.escape(c)}</a> ({len(by_cat[c])})</h2>'
                       f'<ul class="seo-app-list">{"".join(app_row(p) for p in by_cat[c])}</ul></section>' for c in cats)
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": site + path, "url": site + path, "name": title, "description": desc,
         "isPartOf": {"@type": "WebSite", "name": site_name, "url": site + "/"},
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(pkgs), "itemListElement": [
             {"@type": "ListItem", "position": i, "url": site + app_href(p), "name": display_name(p)} for i, p in enumerate(pkgs, 1)]}},
        _crumbs(site, [("Home", "/"), ("Apps list", path)])]}
    write(path, _render(guide_template, site=site, path=path, title=title, description=desc, eyebrow="Apps list",
                        crumb_label="Apps list", crumb_href=path, heading=f"Omarchy apps list: all <span>{len(pkgs)}</span> packages",
                        tagline="Every package in the official Omarchy repository, by category.",
                        answer=f"The official Omarchy package repository has {len(pkgs)} packages as of {synced}. Install any of them with omarchy pkg add <name>, or browse by category below.",
                        body=sections, schema=schema, synced=synced, related=_related(cat_links)), pkg_sources)

    om = facts["omarchy"]
    hub_path = "/vs/omarchy-compared.html"
    vs_links = [(f"/vs/omarchy-vs-cachyos.html", "Omarchy vs CachyOS", "Sourced comparison")]
    vs_links.append((hub_path, "Omarchy compared with other Linux systems", "Sourced facts from official sites"))

    def vs_table(key, d):
        name = d["name"]
        rows = []
        for label, okey, other in d["rows"]:
            o = om.get(okey) if okey else None
            ocell = (html.escape(o["text"]) + _src(o["src"])) if o else "Not a point the Omarchy manual compares."
            rows.append(f"<tr><th scope=\"row\">{html.escape(label)}</th><td>{ocell}</td><td>{html.escape(other['text'])}{_src(other['src'])}</td></tr>")
        table = (f'<div class="table-wrap"><table class="seo-compare"><thead><tr><th></th><th>Omarchy</th><th>{html.escape(name)}</th></tr></thead>'
                 f'<tbody>{"".join(rows)}</tbody></table></div>')
        sources = (f'<p>Omarchy facts: <a href="https://omarchy.org/manual/">the Omarchy manual</a>. {html.escape(name)} facts: '
                   f'<a href="{html.escape(d["site"])}">{html.escape(d["site"])}</a>.</p>')
        return name, table, sources

    for key, d in facts["distros"].items():
        path = f"/vs/omarchy-vs-{key}.html"
        if path in merged and not d.get("editorial"):
            continue
        name, table, sources = vs_table(key, d)
        title = clamp_title(f"Omarchy vs {name}: sourced comparison (2026)")
        desc = clamp_description(f"Omarchy vs {name} compared on facts from omarchy.org and {name}'s official site: base, updates, packages and desktop. Every line is sourced.")
        extra = [k for k in ("base", "release", "install", "secureboot", "firewall", "packages") if k not in {r[1] for r in d["rows"]}]
        omlist = "".join(f"<li>{html.escape(om[k]['text'])}{_src(om[k]['src'])}</li>" for k in extra)
        body = (f'<section><h2>Side by side</h2>{table}</section>'
                f'<section><h2>More about Omarchy</h2><ul>{omlist}</ul></section>'
                f'<section><h2>Sources</h2>{sources}<p>This site is not affiliated with either project.</p></section>')
        ed = d.get("editorial")
        sources_list = fact_sources
        faq_graph = []
        if ed:
            title, desc = clamp_title(ed["title"]), clamp_description(ed["description"])
            part = (root / ed["body_file"]).read_text(encoding="utf-8")
            sources_list = fact_sources + [ed["body_file"]]
            def faq_item(q, a):
                links = ed.get("faq_links", {}).get(q, [])
                more = (" " + ", ".join(f'<a href="{h}">{html.escape(t)}</a>' for h, t in links) + ".") if links else ""
                return f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}{more}</p></details>"
            faq = ('<section class="guide-faq" id="faq"><h2>Frequently asked questions</h2>'
                   + "".join(faq_item(q, a) for q, a in ed["faqs"]) + "</section>")
            body = part.replace("<!-- TABLE -->", body.split("<section><h2>Sources</h2>")[0]).replace(
                "<!-- FAQ -->", faq + "<section><h2>Sources</h2>" + body.split("<section><h2>Sources</h2>")[1])
            faq_graph = [{"@type": "FAQPage", "@id": site + path + "#faq", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in ed["faqs"]]}]
        schema = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "@id": site + path + "#article", "headline": title, "description": desc, "url": site + path,
             "dateModified": synced, "author": {"@type": "Person", "name": "Jessyka", "url": site + "/about.html"},
             "publisher": {"@type": "Organization", "name": site_name, "url": site + "/"},
             "about": [{"@type": "SoftwareApplication", "name": "Omarchy", "applicationCategory": "OperatingSystem", "url": "https://omarchy.org/"},
                       {"@type": "SoftwareApplication", "name": name, "applicationCategory": "OperatingSystem", "url": d["site"]}]},
            _crumbs(site, [("Home", "/"), ("Guides", "/guides.html"), (f"Omarchy vs {name}", path)])] + faq_graph}
        write(path, _render(guide_template, site=site, path=path, title=title, description=desc, eyebrow="Comparison",
                            crumb_label="Guides", crumb_href="/guides.html", heading=f"Omarchy vs <span>{html.escape(name)}</span>",
                            tagline=ed["tagline"] if ed else "Only what each project's official site says, with a source on every line.",
                            answer=ed["answer"] if ed else f"{om['base']['text']} {name}: {d['rows'][0][2]['text']}",
                            body=body, schema=schema, synced=synced, related=_related([l for l in vs_links if l[0] != path])), sources_list)

    # One sourced hub for the thinner comparisons, built only from seo-facts.json.
    hub_body_parts = [
        "<section><h2>How this page is built</h2><p>Every line below is taken from the Omarchy manual or from that project's official site. "
        "This site is not affiliated with those projects. A longer, hand written comparison for CachyOS lives on its own page.</p></section>"
    ]
    hub_sources = ['<p>Omarchy facts: <a href="https://omarchy.org/manual/">the Omarchy manual</a>.']
    for key, d in facts["distros"].items():
        if d.get("editorial"):
            continue
        name, table, sources = vs_table(key, d)
        hub_body_parts.append(f'<section id="{html.escape(key)}"><h2>Omarchy and {html.escape(name)}</h2>{table}{sources}</section>')
        hub_sources.append(f' <a href="{html.escape(d["site"])}">{html.escape(d["site"])}</a>')
    hub_sources.append("</p>")
    hub_body = "".join(hub_body_parts) + "<section><h2>Sources</h2>" + "".join(hub_sources) + "</section>"
    hub_title = clamp_title("Omarchy compared with other Linux systems (2026)")
    hub_desc = clamp_description(
        "Sourced side by side facts for Omarchy versus Ubuntu, Arch Linux, Fedora, Linux Mint, Pop!_OS and Bazzite, taken from official sites."
    )
    hub_answer = (
        f"{om['base']['text']} The tables below compare that with what each project's official site says. "
        "For CachyOS, see the longer comparison linked at the end of this page."
    )
    hub_schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": site + hub_path + "#article", "headline": hub_title, "description": hub_desc,
         "url": site + hub_path, "dateModified": synced,
         "author": {"@type": "Person", "name": "Jessyka", "url": site + "/about.html"},
         "publisher": {"@type": "Organization", "name": site_name, "url": site + "/"}},
        _crumbs(site, [("Home", "/"), ("Guides", "/guides.html"), ("Omarchy compared", hub_path)])]}
    write(hub_path, _render(guide_template, site=site, path=hub_path, title=hub_title, description=hub_desc,
                            eyebrow="Comparison", crumb_label="Guides", crumb_href="/guides.html",
                            heading="Omarchy compared with <span>other Linux systems</span>",
                            tagline="Only what each official site says, with a source on every line.",
                            answer=hub_answer, body=hub_body, schema=hub_schema, synced=synced,
                            related=_related(vs_links)), fact_sources)

    in_repo = {p["name"] for p in pkgs}
    gaming_slugs = {"lutris", "heroic-epic-games"}
    inst_links = []
    for g in facts["install"]:
        path = f"/install/{g['slug']}-on-omarchy.html"
        inst_links.append((live(path) if g["slug"] in gaming_slugs else path, f"Install {g['app']} on Omarchy", g["menu"]))
    inst_links.insert(0, ("/install/gaming-on-omarchy.html", "Install Windows game stores on Omarchy", "Lutris and Heroic from the Omarchy menu"))
    # de-dupe hrefs after live()
    seen_href = set()
    inst_links_unique = []
    for item in inst_links:
        if item[0] in seen_href:
            continue
        seen_href.add(item[0])
        inst_links_unique.append(item)
    inst_links = inst_links_unique

    for g in facts["install"]:
        assert g["slug"] not in in_repo, f"{g['slug']} is in the repo; it has an app page already"
        path = f"/install/{g['slug']}-on-omarchy.html"
        if path in merged:
            continue
        title = clamp_title(f"How to install {g['app']} on Omarchy (2026)")
        desc = clamp_description(f"Install {g['app']} on Omarchy the official way: {g['menu']}. Step by step from the Omarchy manual, with the source linked.")
        steps = "".join(f"<li>{html.escape(s)}</li>" for s in g["steps"])
        body = (
            f'<section><h2>Official steps</h2><p>{html.escape(g["note"])}{_src(g["src"])}</p>'
            f'<ol>{steps}</ol></section>'
            f'<section><h2>Source</h2><p>From the official <a href="{html.escape(g["src"])}">Omarchy manual</a>. '
            f'{html.escape(g["app"])} is not a package in the official Omarchy repository, so it has no app page here. '
            f'For repository apps, start at the <a href="/">home page</a>.</p></section>'
        )
        schema = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "@id": site + path + "#article", "headline": title, "description": desc, "url": site + path,
             "dateModified": synced, "author": {"@type": "Person", "name": "Jessyka", "url": site + "/about.html"},
             "publisher": {"@type": "Organization", "name": site_name, "url": site + "/"}},
            _crumbs(site, [("Home", "/"), ("Guides", "/guides.html"), (f"Install {g['app']}", path)])]}
        write(path, _render(guide_template, site=site, path=path, title=title, description=desc, eyebrow="Install guide",
                            crumb_label="Guides", crumb_href="/guides.html", heading=f"Install {html.escape(g['app'])} on <span>Omarchy</span>",
                            tagline=f"The official route: {g['menu']}.", answer=" ".join(g["steps"][:2]),
                            body=body, schema=schema, synced=synced, related=_related([l for l in inst_links if l[0] != path])), fact_sources)

    # Hub for the two weakest menu guides (Lutris and Heroic), using only official gaming facts.
    gaming = [g for g in facts["install"] if g["slug"] in gaming_slugs]
    if gaming:
        gpath = "/install/gaming-on-omarchy.html"
        sections = []
        for g in gaming:
            steps = "".join(f"<li>{html.escape(s)}</li>" for s in g["steps"])
            sections.append(
                f'<section id="{html.escape(g["slug"])}"><h2>Install {html.escape(g["app"])}</h2>'
                f'<p>Official menu path: {html.escape(g["menu"])}. {html.escape(g["note"])}{_src(g["src"])}</p>'
                f'<ol>{steps}</ol></section>'
            )
        src = gaming[0]["src"]
        sections.append(
            f'<section><h2>Source</h2><p>From the official <a href="{html.escape(src)}">Omarchy manual gaming page</a>. '
            f'Steam and Battle.net have their own install pages, linked below. These tools are not packages in the official '
            f'Omarchy repository, so they have no app page here.</p></section>'
        )
        gtitle = clamp_title("Install Lutris and Heroic on Omarchy (2026)")
        gdesc = clamp_description(
            "Install Lutris and Heroic (Epic Games) from the Omarchy menu, with official steps and notes from the Omarchy manual."
        )
        ganswer = " ".join(
            f"{g['app']}: open the Omarchy menu with Super + Space, then choose {g['menu']}." for g in gaming
        )
        gschema = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "@id": site + gpath + "#article", "headline": gtitle, "description": gdesc, "url": site + gpath,
             "dateModified": synced, "author": {"@type": "Person", "name": "Jessyka", "url": site + "/about.html"},
             "publisher": {"@type": "Organization", "name": site_name, "url": site + "/"}},
            _crumbs(site, [("Home", "/"), ("Guides", "/guides.html"), ("Install Lutris and Heroic", gpath)])]}
        write(gpath, _render(guide_template, site=site, path=gpath, title=gtitle, description=gdesc, eyebrow="Install guide",
                             crumb_label="Guides", crumb_href="/guides.html",
                             heading="Install Lutris and Heroic on <span>Omarchy</span>",
                             tagline="Official menu paths from the Omarchy manual.",
                             answer=ganswer, body="".join(sections), schema=gschema, synced=synced,
                             related=_related([l for l in inst_links if l[0] != gpath])), fact_sources)
    return out
