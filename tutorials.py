"""One tutorial page per Omarchy package, generated only from package facts.

Every sentence comes from the package database, the PKGBUILD or the reviewed
enrichment file; commands are the ones that work for any Omarchy package. Apps
that already have a hand-researched guide keep it and get no generated page.
"""
import datetime
import html
import re

TITLE_MAX = 60
DESC_MAX = 158


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def display_name(name: str) -> str:
    return re.sub(r"-(bin|git)$", "", name)


def _e(s: object) -> str:
    return html.escape(str(s))


def _trim(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"


def _pricing(p: dict) -> str:
    note = p.get("pricing_note")
    kind = {"free": "free to use", "free-libre": "free and open source"}.get(p.get("pricing", ""), "")
    if kind and note:
        return f"{kind[0].upper()}{kind[1:]} ({note})"
    if kind:
        return f"{kind[0].upper()}{kind[1:]}"
    if note or p.get("pricing"):
        return f"{(note or p['pricing'])[0].upper()}{(note or p['pricing'])[1:]}"
    return "Check the project site for current pricing"


def _code(cmd: str) -> str:
    return f'<pre><code class="language-bash">{_e(cmd)}</code></pre>'


def _faqs(p: dict, d: str) -> list[tuple[str, str]]:
    n, deps = p["name"], p.get("deps") or []
    faqs = [
        (f"How do I install {d} on Omarchy?",
         f"Open a terminal and run omarchy pkg add {n}. The download is {p['csize']} and it takes {p['isize']} once installed. "
         f"Omarchy pulls in any dependencies automatically."),
        (f"Is {d} free?", _pricing(p) + f". The package is licensed {p['license']}."),
        (f"How do I uninstall {d}?", f"Run omarchy pkg drop {n}. It removes the package from your system."),
        (f"What does {d} depend on?",
         (f"The package declares {len(deps)} dependenc{'y' if len(deps) == 1 else 'ies'}: {', '.join(deps[:12])}"
          f"{' and more' if len(deps) > 12 else ''}. Omarchy installs them for you."
          if deps else f"{d} declares no dependencies in the Omarchy package database.")),
    ]
    if p.get("has_gui") is True:
        faqs.append((f"Is {d} a desktop app?", f"Yes. Open the launcher with Super + Space and search for {d}."))
    elif p.get("has_gui") is False:
        faqs.append((f"Is {d} a desktop app?",
                     f"No. {d} has no window of its own; it is a command-line tool, library or system component."))
    who = (f"{p['author_name']} makes it. " if p.get("author_name") else "")
    where = f"Project site: {p['url']}. " if p.get("url") else (f"Source: {p['github']}. " if p.get("github") else "")
    faqs.append((f"Is {d} in the official Omarchy repo?",
                 f"Yes. It is published as {n} (version {p['version']}) in the official Omarchy package repository. {who}{where}"
                 f"This site is unofficial and not affiliated with Omarchy or Omacom."))
    return faqs


def _body(p: dict, d: str, faqs: list[tuple[str, str]], siblings: list[dict], profile: str, media: str) -> str:
    n = p["name"]
    built = datetime.datetime.fromtimestamp(p["built"], datetime.timezone.utc).strftime("%Y-%m-%d")
    deps = p.get("deps") or []
    what = p.get("full_desc") or p.get("desc") or ""
    if p.get("has_gui") is True:
        use = (f"<p>{_e(d)} is a desktop app. Press <kbd>Super</kbd> + <kbd>Space</kbd> to open the launcher and search for it. "
               f"If it does not show up by name, list the desktop entries the package installed:</p>"
               + _code(f"pacman -Ql {n} | grep applications"))
    elif p.get("has_gui") is False:
        use = (f"<p>{_e(d)} has no window of its own: it is a command-line tool, library or system component. "
               f"To see the commands it added to your PATH:</p>" + _code(f"pacman -Ql {n} | grep /usr/bin/"))
    else:
        use = ("<p>To see what the package installed, including any commands and desktop entries:</p>" + _code(f"pacman -Ql {n}"))
    reqs = "".join(f"<li>{_e(r)}</li>" for r in p.get("requirements", []))
    dep_list = "".join(f"<li><code>{_e(x)}</code></li>" for x in deps[:12])
    facts = [("Package", f"<code>{_e(n)}</code>"), ("Version", _e(p["version"])), ("Category", _e(p["category"])),
             ("License", _e(p["license"])), ("Download", _e(p["csize"])), ("Installed size", _e(p["isize"])),
             ("Built", built), ("Pricing", _e(_pricing(p)))]
    if p.get("author_name"):
        facts.append(("Made by", _e(p["author_name"])))
    rows = "".join(f"<tr><th scope='row'>{k}</th><td>{v}</td></tr>" for k, v in facts)
    links = [f'<a href="{_e(profile)}">{_e(d)} package page on this site</a>']
    if p.get("url"):
        links.append(f'<a href="{_e(p["url"])}" target="_blank" rel="noopener">Project site</a>')
    if p.get("github"):
        links.append(f'<a href="{_e(p["github"])}" target="_blank" rel="noopener">Source on GitHub</a>')
    sib = "".join(f'<li><a href="/{s["slug"]}.html">{_e(s["label"])}</a></li>' for s in siblings)
    faq_html = "".join(f"<details><summary>{_e(q)}</summary><p>{_e(a)}</p></details>" for q, a in faqs)
    return f"""    <nav class="guide-toc" aria-label="On this page">
      <strong>On this page</strong>
      <a href="#install">Install</a>
      <a href="#use">Open and use</a>
      <a href="#requirements">Requirements</a>
      <a href="#remove">Uninstall</a>
      <a href="#facts">Package facts</a>
      <a href="#faq">Questions</a>
    </nav>

    <section id="install">
      <h2>Install {_e(d)} on Omarchy</h2>
      <p>{_e(what)}</p>
      {media}
      <ol>
        <li>Open a terminal.</li>
        <li>Run the install command:{_code(f"omarchy pkg add {n}")}</li>
        <li>Check it landed. Pacman should list version {_e(p['version'])}:{_code(f"pacman -Qi {n}")}</li>
      </ol>
    </section>

    <section id="use">
      <h2>Open and use {_e(d)}</h2>
      {use}
    </section>

    <section id="requirements">
      <h2>{_e(d)} requirements and compatibility</h2>
      {f"<ul>{reqs}</ul>" if reqs else f"<p>No special requirements are documented for {_e(d)}.</p>"}
      {f"<h3>Dependencies Omarchy installs for you</h3><ul>{dep_list}</ul>" if deps else ""}
      <h3>Pricing and license</h3>
      <p>{_e(_pricing(p))}. License: {_e(p['license'])}.</p>
    </section>

    <section id="remove">
      <h2>Uninstall {_e(d)}</h2>
      {_code(f"omarchy pkg drop {n}")}
    </section>

    <section id="facts">
      <h2>{_e(d)} package facts</h2>
      <div class="table-scroll"><table class="compare-table"><tbody>{rows}</tbody></table></div>
      <p>{" · ".join(links)}</p>
    </section>

    <section class="guide-faq" id="faq">
      <h2>Frequently asked questions</h2>
      {faq_html}
    </section>
{f'''
    <section id="related">
      <h2>More {_e(p["category"])} apps on Omarchy</h2>
      <ul>{sib}</ul>
    </section>''' if siblings else ""}
"""


def _title(d: str) -> str:
    for pattern in ("How to Install & Use {} on Omarchy (2026)", "Install & Use {} on Omarchy (2026)", "{} on Omarchy: Install & Use"):
        if len(pattern.format(d)) <= TITLE_MAX:
            return pattern.format(d)
    return pattern.format(d)


def _media(p: dict, images: list[dict]) -> str:
    out = ""
    if images:
        img = images[0]
        src = img.get("source_url") or p.get("github") or p.get("url") or ""
        credit = (f'<p class="media-source">Image loaded from the upstream project · <a href="{_e(src)}" target="_blank" rel="noopener">source ↗</a></p>' if src else "")
        out += (f'<figure><img src="{_e(img["url"])}" alt="{_e(img.get("alt") or p["name"] + " screenshot")}" '
                f'loading="lazy" decoding="async" referrerpolicy="no-referrer" style="max-width:100%;height:auto">{credit}</figure>')
    if p.get("youtube_id"):
        out += (f'<p><a href="https://www.youtube.com/watch?v={_e(p["youtube_id"])}" target="_blank" rel="noopener">'
                f'Watch: {_e(p.get("youtube_title") or p["name"] + " demo")} ↗</a></p>')
    return out


def build(pkgs: list[dict], guided: set[str], site_url: str, images_fn=lambda p: []) -> list[dict]:
    """Return one page record per package that has no hand-written guide."""
    entries = []
    shown = [display_name(p["name"]) for p in pkgs]
    for p in pkgs:
        if p["name"] in guided:
            continue
        d = display_name(p["name"])
        if shown.count(d) > 1:  # foo and foo-bin would share a title; keep the full package name
            d = p["name"]
        s = f"{slug(p['name'])}-on-omarchy"
        title = _title(d)
        desc = _trim(f"Install {d} on Omarchy with one command: omarchy pkg add {p['name']}. "
                     f"{p['desc'].rstrip('.')}. Setup, requirements and FAQ.", DESC_MAX)
        answer = (f"To install {d} on Omarchy, open a terminal and run omarchy pkg add {p['name']}. "
                  f"It is a {p['csize']} download ({p['isize']} installed), version {p['version']}, licensed {p['license']}. "
                  f"{p['desc'].rstrip('.')}. {_pricing(p)}.")
        entries.append({
            "slug": s, "name": p["name"], "display": d, "category": p["category"], "pkg": p,
            "title": title, "description": desc, "answer": answer,
            "eyebrow": f"{p['category']} tutorial",
            "heading": f"{html.escape(d)} on <span>Omarchy</span>",
            "tagline": p.get("tagline") or p["desc"],
            "faqs": _faqs(p, d),
            "profile": f"/apps/{slug(p['name'])}.html",
            "label": d, "media": _media(p, images_fn(p)),
        })
    by_cat: dict[str, list[dict]] = {}
    for e in entries:
        by_cat.setdefault(e["category"], []).append(e)
    for e in entries:
        pool = by_cat[e["category"]]
        i = pool.index(e)
        near = [x for x in pool[i + 1:] + pool[:i]][:6]
        e["body"] = _body(e["pkg"], e["display"], e["faqs"], near, e["profile"], e["media"])
    return entries
