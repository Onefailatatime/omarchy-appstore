"""Press page (/press.html), press kit (/press/), and the Q&A page (/faq.html).

Copy rules: never quote David; say the store is unofficial and was built with
David's blessing; Jessyka's title is "Creator of The Unofficial Omarchy App
Store". The app count is a dated snapshot from the live catalogue, not a live
number, so the press release reads the same everywhere it is copied.
"""
import html
import json
import pathlib
import zipfile

PRESS_DATE = "2026-10-19"
PRESS_DATE_LONG = "October 19, 2026"
COUNT_DATE_LONG = "October 18, 2026"
APP_COUNT = 194  # from https://omarchyapps.com/ ItemList numberOfItems, synced 2026-10-18
CREATOR_TITLE = "Creator of The Unofficial Omarchy App Store"
CONTACT_EMAIL = "modecandsllc@gmail.com"
CONTACT_X = "https://x.com/jessyka_boat"

HEADLINE = "Omarchy Apps launches an unofficial app store for every app in the official Omarchy package repo"
SUBHEAD = ("Built with the blessing of Omarchy's creator, David Heinemeier Hansson, the store rebuilds itself "
           "from pkgs.omarchy.org every day and gives each app its own profile.")
LEDE = (f"Omarchy Apps (omarchyapps.com), The Unofficial Omarchy App Store, is a free, searchable home for every app "
        "in the official Omarchy package repository. Built and curated by Jessyka Mathews with the blessing and "
        "approval of Omarchy's creator, David Heinemeier Hansson, it turns the official repo into app profiles that "
        "people can browse, compare and install with one command.")
BODY = [
    (f"The store is tied directly to the official Omarchy package repo. Its catalog is rebuilt from pkgs.omarchy.org "
     f"every day, so new packages and updates show up on their own. As of {COUNT_DATE_LONG}, the catalog lists "
     f"{APP_COUNT} apps."),
    ("Every app has a profile with the exact install command, omarchy pkg add followed by the package name. Profiles "
     "include demo galleries where they are available: screenshots from the app's GitHub README and YouTube demos "
     "that load only when a visitor presses play. Tutorials are added for apps, and developers can claim their "
     "profile to add their own images and videos."),
    ("There is no submission form. Developers get listed by opening a pull request to the official Omarchy package "
     "repository. Once a package is published there, the store picks it up automatically. The Develop page at "
     "omarchyapps.com/develop.html explains how."),
    ("Readers can upvote their favorite apps, and a community leaderboard shows the current top picks. The store is "
     "free to use, and anyone who wants to help keep it going can visit the Sponsor page at "
     "omarchyapps.com/sponsor.html, which includes pay-what-you-want Support the store links."),
]
QUOTE = ("I wanted a friendly front door for everything Omarchy can install. The official repo already does the hard "
         "work, so the store simply makes those apps easier to find, see and try, and gives developers a place to "
         "show off what they've built.")
BOILERPLATE = ("Omarchy Apps (omarchyapps.com) is The Unofficial Omarchy App Store: an independent, searchable "
               "directory of every app in the official Omarchy package repository, rebuilt daily from "
               "pkgs.omarchy.org. It hosts no packages itself and links every install back to the official repo. "
               "It is a community project, not affiliated with Omacom, and was built with the blessing of "
               "Omarchy's creator, David Heinemeier Hansson.")

SNIPPETS = [
    ("one-line", "One-line description",
     "Omarchy Apps is The Unofficial Omarchy App Store: every app in the official Omarchy repo, searchable, with one-command installs."),
    ("fifty", "50-word description",
     "Omarchy Apps is The Unofficial Omarchy App Store, built with the blessing of Omarchy's creator, David "
     "Heinemeier Hansson. It lists every app in the official Omarchy package repo, rebuilds daily from "
     "pkgs.omarchy.org, and gives each app a profile with its install command, plus screenshots, demo videos and "
     "tutorials where available."),
    ("hundred", "100-word description",
     "Omarchy Apps (omarchyapps.com) is The Unofficial Omarchy App Store, built and curated by Jessyka Mathews with "
     "the blessing and approval of Omarchy's creator, David Heinemeier Hansson. It is tied directly to the official "
     "Omarchy package repo and rebuilds its catalog every day from pkgs.omarchy.org, so it stays current on its own. "
     "Every app gets a profile with the exact install command, and many include screenshots from the app's README, "
     "click-to-play YouTube demos and tutorials. Developers can claim their profile to add their own images and "
     "videos. Getting listed is just a pull request to the official Omarchy repo."),
    ("tweet", "Tweet-length blurb",
     "Omarchy Apps is an unofficial app store for Omarchy, built with David's blessing. Every app in the official "
     "repo, rebuilt daily from pkgs.omarchy.org, with app profiles, demos and one-command installs. omarchyapps.com"),
    ("bio", "Creator bio",
     "Jessyka Mathews is the Creator of The Unofficial Omarchy App Store. Hazardous waste executive by day and indie "
     "hacker by night, she loves turning messy problems into useful little tools, learning in public, and making the "
     "internet a little more delightful along the way. She is @jessyka_boat on X."),
]
FACTS = [
    ("Name", "Omarchy Apps, The Unofficial Omarchy App Store"),
    ("Website", "https://omarchyapps.com"),
    ("Creator", f"Jessyka Mathews, {CREATOR_TITLE}"),
    ("Status", "Unofficial and independent, built with the blessing of Omarchy's creator, David Heinemeier Hansson"),
    ("Catalog source", "The official Omarchy package repo, rebuilt daily from pkgs.omarchy.org"),
    ("Apps listed", f"{APP_COUNT} (as of {COUNT_DATE_LONG})"),
    ("Install", "omarchy pkg add <name>, straight from the official repo"),
    ("Getting listed", "A pull request to the official Omarchy package repo; no submission form"),
    ("App profiles", "Screenshot galleries from README files, click-to-play YouTube demos, tutorials, claimable by developers"),
    ("Price", "Free to use; supported through the Sponsor page"),
    ("Media contact", f"{CONTACT_EMAIL} · @jessyka_boat on X"),
]
KIT_FILES = [
    ("logos/omarchy-apps-logo-dark.svg", "Logo, dark (SVG)"), ("logos/omarchy-apps-logo-dark.png", "Logo, dark (PNG)"),
    ("logos/omarchy-apps-logo-light.svg", "Logo, light (SVG)"), ("logos/omarchy-apps-logo-light.png", "Logo, light (PNG)"),
    ("logos/omarchy-apps-icon-dark.svg", "Icon, dark (SVG)"), ("logos/omarchy-apps-icon-dark.png", "Icon, dark (PNG)"),
    ("logos/omarchy-apps-icon-light.svg", "Icon, light (SVG)"), ("logos/omarchy-apps-icon-light.png", "Icon, light (PNG)"),
]
SHOTS = [
    ("desktop-home.png", "Desktop: the Omarchy Apps homepage with search and the community favorites"),
    ("desktop-app-profile.png", "Desktop: an app profile with install command and screenshot gallery"),
    ("desktop-leaderboard.png", "Desktop: the community leaderboard of top Omarchy apps"),
    ("desktop-develop.png", "Desktop: the Develop for Omarchy page explaining how apps get listed"),
    ("mobile-home.png", "Mobile: the Omarchy Apps homepage at phone size"),
    ("mobile-app-profile.png", "Mobile: an app profile at phone size"),
]

FAQ_PAGE = [
    ("What is Omarchy Apps?",
     "Omarchy Apps (omarchyapps.com) is The Unofficial Omarchy App Store. It is a free, searchable directory of every "
     "app in the official Omarchy package repository, with a profile and a one-line install command for each app."),
    ("Is Omarchy Apps official?",
     "No. It is an unofficial, independent community project and is not affiliated with Omacom. It was built with the "
     "blessing and approval of Omarchy's creator, David Heinemeier Hansson."),
    ("Where does the app catalog come from?",
     "Straight from the official Omarchy package repo. The store reads the package database published at "
     "pkgs.omarchy.org and hosts no packages of its own."),
    ("How often does it update?",
     "Every day. The catalog is rebuilt automatically from pkgs.omarchy.org on a schedule, currently twice a day, so "
     "new packages and version changes appear without anyone submitting them."),
    ("How many apps are listed?",
     f"{APP_COUNT} apps as of {COUNT_DATE_LONG}. The number follows the official repo, so it changes as packages are added."),
    ("How do I install an app?",
     "Open the app's profile and copy its command, for example omarchy pkg add followed by the package name, into a "
     "terminal on Omarchy. The package downloads from the official Omarchy repository, not from this site."),
    ("Is it free?",
     "Yes. Browsing and installing are free. The store does not sell software, and there is no account to create."),
    ("How do apps get listed?",
     "By opening a pull request to the official Omarchy package repo. There is no submission form. Once the package is "
     "published to pkgs.omarchy.org, the next build picks it up. The Develop page at omarchyapps.com/develop.html explains how."),
    ("What is on an app profile?",
     "The install command, version, size and license, plus a demo gallery where one exists: screenshots from the app's "
     "GitHub README and YouTube demos that load only when you press play. Tutorials are added for apps too."),
    ("How can developers claim their app profile?",
     "Open the app's profile and choose Claim this app. It opens a short message to @jessyka_boat on X where you can "
     "share your role, corrections, and your own screenshots and demo videos."),
    ("How can I support the store?",
     "Visit the Sponsor page at omarchyapps.com/sponsor.html. It has pay-what-you-want Support the store links and "
     "sponsor spots. Upvoting and sharing your favorite apps helps too."),
    ("Who built Omarchy Apps?",
     f"Jessyka Mathews, {CREATOR_TITLE}, built it solo. Press can find the release, logos, screenshots and contact "
     "details at omarchyapps.com/press.html."),
]


def _e(s: str) -> str:
    return html.escape(s, quote=True)


def word_count(text: str) -> int:
    return len(text.split())


def press_release_text() -> str:
    parts = [HEADLINE, "", SUBHEAD, "", f"{PRESS_DATE_LONG}. {LEDE}", ""]
    for p in BODY:
        parts += [p, ""]
    parts += [f"\"{QUOTE}\" said Jessyka Mathews, {CREATOR_TITLE}.", "", "About Omarchy Apps", BOILERPLATE, "",
              "Media contact", f"Jessyka Mathews, {CREATOR_TITLE}", CONTACT_EMAIL, "@jessyka_boat on X",
              "https://omarchyapps.com/press.html", ""]
    return "\n".join(parts)


def snippets_text() -> str:
    out = [f"Omarchy Apps press copy ({PRESS_DATE_LONG})", ""]
    for _, label, text in SNIPPETS:
        out += [label, text, ""]
    out.append("Key facts")
    out += [f"- {k}: {v}" for k, v in FACTS]
    return "\n".join(out) + "\n"


def _kit_zip(src: pathlib.Path, dest: pathlib.Path, og: list[pathlib.Path]) -> None:
    """Deterministic zip (fixed timestamps) so rebuilds don't churn the file."""
    entries = []
    for rel, _ in KIT_FILES:
        entries.append((f"omarchy-apps-press-kit/{rel}", (src / rel).read_bytes()))
    for name, _ in SHOTS:
        entries.append((f"omarchy-apps-press-kit/screenshots/{name}", (src / "screenshots" / name).read_bytes()))
    for f in og:
        entries.append((f"omarchy-apps-press-kit/og/{f.name}", f.read_bytes()))
    entries.append(("omarchy-apps-press-kit/press-release.txt", press_release_text().encode()))
    entries.append(("omarchy-apps-press-kit/copy-and-facts.txt", snippets_text().encode()))
    tmp = dest.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 19, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
    if dest.exists() and dest.read_bytes() == tmp.read_bytes():
        tmp.unlink()
    else:
        tmp.replace(dest)


def build(*, root: pathlib.Path, dist: pathlib.Path, site: str, site_name: str, synced: str, css: str) -> list[str]:
    src = root / "assets" / "press"
    press_css = (root / "parts" / "press.css").read_text(encoding="utf-8").strip()
    out = dist / "press"
    for sub in ("logos", "screenshots"):
        (out / sub).mkdir(parents=True, exist_ok=True)
    for rel, _ in KIT_FILES:
        (out / rel).write_bytes((src / rel).read_bytes())
    for name, _ in SHOTS:
        (out / "screenshots" / name).write_bytes((src / "screenshots" / name).read_bytes())
    og = [root / "assets" / "images" / "og-press.png", root / "assets" / "images" / "og-faq.png", root / "assets" / "images" / "social-card.png"]
    _kit_zip(src, out / "press-kit.zip", og)
    zip_mb = round((out / "press-kit.zip").stat().st_size / 1024 / 1024, 1)

    org = {"@type": "Organization", "@id": site + "/#organization", "name": "Omarchy Apps",
           "alternateName": site_name, "url": site + "/", "logo": site + "/press/logos/omarchy-apps-icon-dark.png",
           "sameAs": [CONTACT_X], "email": CONTACT_EMAIL}
    person = {"@type": "Person", "@id": site + "/#jessyka", "name": "Jessyka Mathews", "jobTitle": CREATOR_TITLE,
              "url": site + "/about.html", "sameAs": [CONTACT_X]}

    # ---- press.html
    body_html = "\n".join(f"    <p>{_e(p)}</p>" for p in BODY)
    snippet_html = "\n".join(
        f'    <div class="press-snippet"><div class="press-snippet-head"><h3 id="copy-{k}">{_e(label)}</h3>'
        f'<button class="button ghost press-copy" type="button" data-copy="snip-{k}" aria-describedby="copy-{k}">Copy</button></div>'
        f'<p id="snip-{k}">{_e(text)}</p></div>'
        for k, label, text in SNIPPETS)
    facts_html = "\n".join(f"      <div><dt>{_e(k)}</dt><dd>{_e(v)}</dd></div>" for k, v in FACTS)
    facts_plain = "\n".join(f"{k}: {v}" for k, v in FACTS)
    files_html = "\n".join(f'      <li><a href="/press/{rel}" download>{_e(label)}</a></li>' for rel, label in KIT_FILES)
    shots_html = "\n".join(
        f'      <figure><a href="/press/screenshots/{n}" download><img src="/press/screenshots/{n}" alt="{_e(a)}" '
        f'loading="lazy" decoding="async" width="{720 if n.startswith("desktop") else 195}" height="{450 if n.startswith("desktop") else 422}"></a>'
        f'<figcaption>{_e(a)}</figcaption></figure>'
        for n, a in SHOTS)
    press_schema = {"@context": "https://schema.org", "@graph": [
        org, person,
        {"@type": "NewsArticle", "@id": site + "/press.html#release", "headline": HEADLINE, "description": SUBHEAD,
         "datePublished": PRESS_DATE, "dateModified": PRESS_DATE, "articleSection": "Press release",
         "url": site + "/press.html", "mainEntityOfPage": site + "/press.html", "image": [site + "/images/og-press.png"],
         "author": {"@id": site + "/#jessyka"}, "publisher": {"@id": site + "/#organization"},
         "about": {"@type": "WebSite", "name": site_name, "url": site + "/"}},
        {"@type": "WebPage", "@id": site + "/press.html", "url": site + "/press.html",
         "name": "Press and press kit: Omarchy Apps", "isPartOf": {"@type": "WebSite", "name": site_name, "url": site + "/"},
         "primaryImageOfPage": site + "/images/og-press.png", "dateModified": synced},
    ]}
    press = ((root / "parts" / "press.html").read_text(encoding="utf-8")
             .replace("__HEADLINE__", _e(HEADLINE)).replace("__SUBHEAD__", _e(SUBHEAD))
             .replace("__PRESS_DATE__", PRESS_DATE).replace("__PRESS_DATE_LONG__", PRESS_DATE_LONG)
             .replace("__LEDE__", _e(LEDE)).replace("__BODY__", body_html).replace("__QUOTE__", _e(QUOTE))
             .replace("__CREATOR_TITLE__", _e(CREATOR_TITLE)).replace("__BOILERPLATE__", _e(BOILERPLATE))
             .replace("__CONTACT_EMAIL__", _e(CONTACT_EMAIL)).replace("__SNIPPETS__", snippet_html)
             .replace("__FACTS__", facts_html).replace("__FACTS_PLAIN__", _e(facts_plain))
             .replace("__KIT_FILES__", files_html).replace("__SHOTS__", shots_html).replace("__ZIP_MB__", str(zip_mb))
             .replace("__STRUCTURED_DATA__", json.dumps(press_schema, ensure_ascii=False).replace("</", "<\\/"))
             .replace("__SYNCED__", synced).replace("__SITE_URL__", site).replace("__STYLE__", css).replace("__PRESS_CSS__", press_css))
    (dist / "press.html").write_text(press, encoding="utf-8")

    # ---- faq.html
    faq_html = "\n".join(
        f'    <details{" open" if i < 2 else ""}><summary><h2>{_e(q)}</h2></summary><p>{_e(a)}</p></details>'
        for i, (q, a) in enumerate(FAQ_PAGE))
    faq_schema = {"@context": "https://schema.org", "@graph": [
        org,
        {"@type": "FAQPage", "@id": site + "/faq.html#faq", "url": site + "/faq.html",
         "name": "Omarchy Apps Q&A", "dateModified": synced,
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_PAGE]},
    ]}
    faq = ((root / "parts" / "faq.html").read_text(encoding="utf-8")
           .replace("__FAQ_ITEMS__", faq_html)
           .replace("__STRUCTURED_DATA__", json.dumps(faq_schema, ensure_ascii=False).replace("</", "<\\/"))
           .replace("__SYNCED__", synced).replace("__SITE_URL__", site).replace("__STYLE__", css).replace("__PRESS_CSS__", press_css))
    (dist / "faq.html").write_text(faq, encoding="utf-8")
    return ["press", "faq"]
