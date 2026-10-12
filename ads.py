"""Sponsor slots for the build: reads data/ads.json (direct placement) and
renders the homepage rotation units, the advertise page's product cards,
and per-app banners.

Model: header and footer each hold an unlimited list of sponsors and rotate
them fairly (client-side, assets/ads.js): 3 shown at a time, advancing
sequentially, every active sponsor getting equal screen time. App banners
appear on the sponsor's own app page. Only sponsors inside their contract
dates [start, end] are rendered.

Every unit is static HTML, tagged "Ad", and links carry rel="sponsored".
"""

import datetime
import html
import json
import pathlib
import urllib.parse

ROOT = pathlib.Path(__file__).parent
ADS_FILE = ROOT / "data" / "ads.json"

X_DM_RECIPIENT_ID = "1400492097082327040"


def money(cents_or_dollars) -> str:
    if isinstance(cents_or_dollars, int):
        return f"${cents_or_dollars:,}"
    return f"${cents_or_dollars:,.2f}"


def dm_url(text: str) -> str:
    return "https://x.com/messages/compose?" + urllib.parse.urlencode({"recipient_id": X_DM_RECIPIENT_ID, "text": text})


def today_iso() -> str:
    return datetime.date.today().isoformat()


def is_active(sponsor: dict, today: str | None = None) -> bool:
    """A sponsor shows only while today is within [start, end] (inclusive).
    Entries with missing or malformed dates are treated as inactive."""
    today = today or today_iso()
    start = sponsor.get("start") or ""
    end = sponsor.get("end") or ""
    if not start or not end:
        return False
    return start <= today <= end


def active_sponsors(sponsors: list[dict], quiet: bool = False) -> list[dict]:
    """Filter a sponsor list to contract-active entries, preserving order
    (order in ads.json is the rotation order). Inactive entries are skipped
    with a build note so expired contracts are visible in the log."""
    today = today_iso()
    active: list[dict] = []
    for s in sponsors:
        if not isinstance(s, dict):
            continue
        if is_active(s, today):
            active.append(s)
        elif not quiet:
            print(f"ads: sponsor '{s.get('name')}' not active "
                  f"(start={s.get('start')} end={s.get('end')}); skipped")
    return active


def active_banners(banners: dict, quiet: bool = False) -> dict:
    """Filter an app_banners.banners map to contract-active entries."""
    today = today_iso()
    out = {}
    for slug, s in (banners or {}).items():
        if not isinstance(s, dict):
            continue
        if is_active(s, today):
            out[slug] = s
        elif not quiet:
            print(f"ads: app banner '{slug}' ({s.get('name')}) not active "
                  f"(start={s.get('start')} end={s.get('end')}); skipped")
    return out


def load() -> dict:
    return json.loads(ADS_FILE.read_text(encoding="utf-8"))


def _unit(sponsor: dict, tag: str, cls: str = "", image: bool = False) -> str:
    """One sponsor unit. `image` renders the 300x180 creative (stacked
    layout); otherwise a compact unit with mark + copy + CTA."""
    cls = ("ad " + cls).strip()
    img = ""
    if image and sponsor.get("image"):
        cls += " stack"
        img = (f'<img class="shot" src="{html.escape(sponsor["image"], quote=True)}" '
               f'alt="{html.escape(sponsor["name"], quote=True)}, sponsored" '
               'width="300" height="180" loading="lazy">')
    return (
        f'<a class="{cls}" href="{html.escape(sponsor["url"], quote=True)}" '
        f'rel="sponsored" target="_blank"><span class="tag">{html.escape(tag)}</span>'
        f'<span class="mark" aria-hidden="true">{html.escape(sponsor.get("mark") or sponsor["name"][:1], quote=True)}</span>'
        f'{img}<span class="copy"><strong>{html.escape(sponsor["name"])}</strong>'
        f'<span class="sub">{html.escape(sponsor["tagline"])}</span></span>'
        '<span class="cta">Visit →</span></a>'
    )


def _open_card(label: str, anchor: str, price_month: int, term_days: int) -> str:
    """Placeholder card shown while a slot has no active sponsors."""
    per_term = price_month * term_days // 30
    return (
        f'<a class="ad open" href="/advertise.html#{anchor}">'
        '<span class="tag">Ad · open slot</span>'
        '<span class="mark" aria-hidden="true">+</span>'
        f'<span class="copy"><strong>{html.escape(label)}: your app here</strong>'
        f'<span class="sub">{money(price_month)}/mo · {term_days} day term · billed {money(per_term)}</span></span>'
        '<span class="cta">Sponsor →</span></a>'
    )


def _rotation(units: list[str], visible: int, slot_id: str) -> str:
    """Wrap sponsor units in a fair sequential rotation container.
    assets/ads.js shows `visible` at a time and advances one position on a
    fixed timer, so every active sponsor gets equal screen time."""
    return (
        f'<div class="ad-rotate" data-rotate="{visible}" data-slot-id="{html.escape(slot_id, quote=True)}">'
        + "".join(units) + "</div>"
    )


def active_lifetime(sponsors: list[dict], quiet: bool = False) -> list[dict]:
    """Lifetime sponsors: active while today >= start. A missing end date
    means forever (inquiry-only slot, handled manually)."""
    today = today_iso()
    active: list[dict] = []
    for s in sponsors or []:
        if not isinstance(s, dict):
            continue
        start = s.get("start") or ""
        end = s.get("end") or ""
        if start and start <= today and (not end or today <= end):
            active.append(s)
        elif not quiet:
            print(f"ads: lifetime sponsor '{s.get('name')}' not active "
                  f"(start={start} end={end or 'forever'}); skipped")
    return active


def render_lifetime(ads: dict) -> str:
    """Pinned lifetime unit(s) for the top of the homepage, or '' if none.
    Never rotates, the premium forever placement."""
    sponsors = active_lifetime((ads.get("lifetime") or {}).get("sponsors"))
    if not sponsors:
        return ""
    units = [_unit(s, "Ad", "text", image=True) for s in sponsors]
    return '<div class="ad-lifetime">' + "".join(units) + "</div>"


def render_homepage(ads: dict) -> dict[str, str]:
    h = ads["header"]
    hsponsors = active_sponsors(h.get("sponsors") or [])
    if hsponsors:
        hunits = [_unit(s, "Ad", "text") for s in hsponsors]
        header = f'<div class="ad-header">{_rotation(hunits, h.get("visible_units", 3), "header")}</div>'
    else:
        header = (f'<div class="ad-header">'
                  f'{_open_card(h["label"], "header", h["price_month"], h["term_days"])}'
                  "</div>")

    f = ads["footer"]
    fsponsors = active_sponsors(f.get("sponsors") or [])
    if fsponsors:
        funits = [_unit(s, "Ad") for s in fsponsors]
        footer = ('<div class="ad-footer"><h2 class="sec-label">Sponsors</h2>'
                  f'{_rotation(funits, f.get("visible_units", 3), "footer")}</div>')
    else:
        footer = ('<div class="ad-footer"><h2 class="sec-label">Sponsors</h2>'
                  f'{_open_card(f["label"], "footer", f["price_month"], f["term_days"])}'
                  "</div>")
    return {"__AD_HEADER__": header, "__AD_FOOTER__": footer,
            "__AD_LIFETIME__": render_lifetime(ads)}


def render_app_banner(banners: dict, app_slug: str) -> str:
    """Banner for an app's profile page, or '' if none. Takes the
    already date-filtered banners map (see active_banners); call it once
    per build, not once per app page."""
    sponsor = (banners or {}).get(app_slug)
    if not sponsor:
        return ""
    return (f'<div class="ad-app-banner">'
            f'{_unit(sponsor, "Sponsor", "text", image=True)}'
            "</div>")


def render_slot_cards(ads: dict) -> str:
    """Product cards for the advertise page: fixed prices, contact CTA,
    no bidding."""
    cards: list[str] = []

    def product_card(key: str, label: str, position: str, price_line: str, blurb: str, cta_label: str, checkout_url: str = "") -> None:
        dm = html.escape(dm_url(f"Hi! I want to sponsor omarchyapps.com ({label})."), quote=True)
        if checkout_url:
            actions = (f'<p class="slot-actions"><a class="button" href="{html.escape(checkout_url, quote=True)}" rel="noopener">{html.escape(cta_label)} \u2197</a>'
                       f'<a class="button ghost" href="{dm}" target="_blank" rel="noopener">Ask first \u2197</a></p>')
        else:
            actions = f'<a class="button" href="{dm}" target="_blank" rel="noopener">{html.escape(cta_label)} \u2197</a>'
        cards.append(
            f'<article class="slot" id="{html.escape(key, quote=True)}">'
            f'<h3>{html.escape(label)}</h3><p class="pos">{html.escape(position)}</p>'
            f'<p class="price">{price_line}</p><p class="status">{blurb}</p>{actions}</article>'
        )

    def term_price(slot: dict) -> str:
        per_term = slot["price_month"] * slot["term_days"] // 30
        return (f'<b>{money(slot["price_month"])}</b> / month'
                f' · billed as <b>{money(per_term)}</b> every {slot["term_days"]} days, cancel any time')

    h = ads["header"]
    n_h = len(active_sponsors(h.get("sponsors") or [], quiet=True))
    product_card(
        "header", "Header rotation", h["position"], term_price(h),
        f"Three units under the hero, rotating fairly through every active sponsor. Equal screen time, no bidding for position. "
        f"<b>{n_h}</b> sponsor{'s' if n_h != 1 else ''} active now; unlimited spots.",
        "Sponsor the header", h.get("checkout_url", ""),
    )

    f = ads["footer"]
    n_f = len(active_sponsors(f.get("sponsors") or [], quiet=True))
    product_card(
        "footer", "Footer rotation", f["position"], term_price(f),
        f"Sponsor units above the site footer, rotating fairly through every active sponsor. "
        f"<b>{n_f}</b> sponsor{'s' if n_f != 1 else ''} active now; unlimited spots.",
        "Sponsor the footer", f.get("checkout_url", ""),
    )

    ab = ads["app_banners"]
    n_ab = len(active_banners((ab.get("banners") or {}), quiet=True))
    product_card(
        "app-banner", "App profile banner", ab["position"], term_price(ab),
        f"Your banner on your app's own page, the highest intent spot on the site, seen by everyone who looks up that app. "
        f"<b>{n_ab}</b> app{'s' if n_ab != 1 else ''} sponsored now.",
        "Sponsor an app page", ab.get("checkout_url", ""),
    )

    lt = ads.get("lifetime") or {}
    n_lt = len(active_lifetime(lt.get("sponsors"), quiet=True))
    cards.append(
        f'<article class="slot" id="lifetime">'
        f'<h3>{html.escape(lt.get("label", "Lifetime pin"))}</h3>'
        f'<p class="pos">{html.escape(lt.get("position", ""))}</p>'
        f'<p class="price"><b>Make an offer</b> · one payment · yours forever</p>'
        f'<p class="status">No listed price and no checkout. Message with the amount you have in mind and we talk it through; '
        f'one sponsor holds this spot permanently. '
        f"<b>{n_lt}</b> active now.</p>"
        f'<a class="button" href="{html.escape(dm_url("Hi! I would like to make an offer for the lifetime sponsor pin on omarchyapps.com. My offer: $"), quote=True)}" '
        'target="_blank" rel="noopener">Make an offer \u2197</a>'
        "</article>"
    )
    return "\n".join(cards)
