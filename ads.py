"""Sponsor slots: reads data/ads.json, overlays the live auction state from the
Cloudflare Worker (worker/), and renders the homepage units and the advertise
page's slot cards. Every unit is static HTML, tagged "Ad", and links with
rel="sponsored". The only script is ads.js, which refreshes figures and posts
bids to the Worker."""

import html
import json
import pathlib
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).parent
ADS_FILE = ROOT / "data" / "ads.json"
AUCTION_URL = "https://omarchy-auction.modecandsllc.workers.dev"
X_DM_RECIPIENT_ID = "1400492097082327040"
SLOTS = ("lifetime", "header", "rail", "footer")


def fetch_state() -> dict | None:
    """Live figures at build time, so the static pages are right even without JS."""
    try:
        with urllib.request.urlopen(AUCTION_URL + "/api/state", timeout=8) as res:
            return json.load(res)["slots"]
    except Exception as error:  # offline builds fall back to the static file
        print(f"ads: live state unavailable ({error}); rendering reserves only")
        return None


def load() -> dict:
    ads = json.loads(ADS_FILE.read_text(encoding="utf-8"))
    live = fetch_state() or {}
    for key in SLOTS:
        ads[key]["live"] = live.get(key)
        sponsors = (live.get(key) or {}).get("sponsors") or []
        if key == "footer":
            for unit in ads[key]["units"]:
                if not unit.get("sponsor") and sponsors:
                    unit["sponsor"] = sponsors.pop(0)
        elif not ads[key].get("sponsor") and sponsors:
            ads[key]["sponsor"] = sponsors[0]
    return ads


def dm_url(text: str) -> str:
    return "https://x.com/messages/compose?" + urllib.parse.urlencode({"recipient_id": X_DM_RECIPIENT_ID, "text": text})


def money(n) -> str:
    return f"${n:,.0f}"


def days_left(live: dict | None) -> str:
    if not live or live.get("status") != "live" or live.get("seconds_left") is None:
        return ""
    secs = live["seconds_left"]
    if secs >= 86400:
        return f"closes in {secs // 86400}d"
    if secs >= 3600:
        return f"closes in {secs // 3600}h"
    return "closing soon"


def _unit(sponsor: dict, tag: str, cls: str = "", image: bool = False) -> str:
    name = html.escape(sponsor["name"])
    tagline = html.escape(sponsor.get("tagline") or "")
    url = html.escape(sponsor["url"])
    mark = html.escape(sponsor.get("mark") or name[:1].upper())
    shot = ""
    if image and sponsor.get("image"):
        shot = f'<img class="shot" src="{html.escape(sponsor["image"])}" alt="" loading="lazy" width="300" height="180">'
    return (
        f'<a class="ad {cls}" href="{url}" rel="sponsored noopener" target="_blank"><span class="tag">{tag}</span>{shot}'
        f'<span class="mark" aria-hidden="true">{mark}</span><span class="copy"><strong>{name}</strong>'
        f'<span class="sub">{tagline}</span></span><span class="cta">Visit ↗</span></a>'
    )


def _lifetime_auction_card(lt: dict) -> str:
    live = lt.get("live")
    hb = (live or {}).get("high_bid")
    status = f"Current high bid {money(hb)}" if hb else f"Reserve {money(lt['reserve'])} · no bids yet"
    left = days_left(live)
    return (
        '<a class="ad lifetime stack open" href="/advertise.html#lifetime" data-slot="lifetime"><span class="tag">Lifetime sponsor</span>'
        '<span class="mark" aria-hidden="true">◆</span><span class="copy"><strong>This spot is up for auction</strong>'
        f'<span class="sub" data-ad-sub>One sponsor, forever, always right here. {status}{" · " + left if left else ""}.</span></span>'
        '<span class="cta">Place a bid →</span></a>'
    )


def _open_card(slot: dict, anchor: str, cls: str = "") -> str:
    """Placeholder for a paid slot nobody holds yet: quiet, dashed, honest."""
    per_term = slot["reserve_month"] * slot["term_days"] // 30
    live = slot.get("live")
    hb = (live or {}).get("high_bid")
    status = f"high bid {money(hb)}/mo" if hb else f"from {money(slot['reserve_month'])}/mo"
    left = days_left(live)
    tail = left if left else f"billed {money(per_term)}"
    return (
        f'<a class="ad open {cls}" href="/advertise.html#{anchor}" data-slot="{anchor}"><span class="tag">Ad · open slot</span>'
        f'<span class="mark" aria-hidden="true">+</span><span class="copy"><strong>{html.escape(slot["label"])} is open</strong>'
        f'<span class="sub" data-ad-sub>{status} · {slot["term_days"]} day term · {tail}</span></span>'
        '<span class="cta">Bid →</span></a>'
    )


def render_homepage(ads: dict) -> dict[str, str]:
    """Return the three homepage placeholders. Open slots show a bid card."""
    h = ads["header"]
    header_unit = _unit(h["sponsor"], "Ad", "text") if h.get("sponsor") else _open_card(h, "header", "text")
    header = f'<div class="ad-header">{header_unit}</div>'

    lt = ads["lifetime"]
    rail_units = [_unit(lt["sponsor"], "Lifetime sponsor", "lifetime stack", image=True) if lt.get("sponsor") else _lifetime_auction_card(lt)]
    r = ads["rail"]
    rail_units.append(_unit(r["sponsor"], "Ad", "stack", image=True) if r.get("sponsor") else _open_card(r, "rail", "stack"))
    rail = ('<aside class="ad-rail" aria-label="Sponsors">' + "".join(rail_units)
            + '<p class="rail-note">Sponsors keep the store free · <a href="/advertise.html">advertise</a></p></aside>')

    f = ads["footer"]
    footer_units = [_unit(u["sponsor"], "Ad") if u.get("sponsor") else _open_card(f, "footer") for u in f["units"]]
    footer = ('<div class="ad-footer"><h2 class="sec-label">Sponsors <small>' + f'{sum(1 for u in f["units"] if not u.get("sponsor"))} of {len(f["units"])} footer units open'
              + '</small></h2><div class="ad-footer-row">' + "".join(footer_units) + "</div></div>")
    return {"__AD_HEADER__": header, "__AD_RAIL__": rail, "__AD_FOOTER__": footer}


def _status_line(slot: dict, per_month: bool) -> str:
    live = slot.get("live") or {}
    unit = " per month" if per_month else ""
    hb = live.get("high_bid")
    parts = [f"Current high bid <b>{money(hb)}</b>{unit}" if hb else "No bids yet"]
    if live.get("status") == "live" and live.get("closes_at"):
        parts.append(f"bidding closes <b>{html.escape(live['closes_at'][:10])}</b>" + (" (extended)" if live.get("extensions") else ""))
    elif live.get("status") == "closed":
        parts = ["This round has closed"]
    else:
        parts.append(f"the {slot['auction_days']} day clock starts at the first approved bid")
    return " · ".join(parts)


def _bid_form(key: str, slot: dict, per_month: bool, label: str, featured: bool) -> str:
    live = slot.get("live") or {}
    minimum = live.get("minimum_bid") or (slot["reserve_month"] if per_month else slot["reserve"])
    unit = "$ per month" if per_month else "$ one payment"
    summary = f'<summary class="button{"" if featured else " ghost"}">{html.escape(label)}</summary>'
    return (
        f'<details class="bid-wrap">{summary}'
        f'<form class="bid" data-bid data-slot="{key}" data-per-month="{1 if per_month else 0}" action="{AUCTION_URL}/api/bid" method="post">'
        f'<label>Your bid <small>{unit}</small><input name="amount" type="number" inputmode="numeric" min="{minimum}" step="1" placeholder="{minimum}" required data-bid-amount></label>'
        '<label>Product name<input name="name" maxlength="60" required autocomplete="organization"></label>'
        '<label>Link<input name="url" type="url" maxlength="200" placeholder="https://" required autocomplete="url"></label>'
        '<label>One line tagline<input name="tagline" maxlength="90" required placeholder="Under 90 characters"></label>'
        '<label>Your email<input name="email" type="email" maxlength="254" required autocomplete="email"></label>'
        '<input class="trap" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">'
        '<label class="agree"><input type="checkbox" name="agree" required> A winning bid is a commitment to pay. I have read the <a href="#terms">bidding terms</a>.</label>'
        '<button class="button" type="submit">Place bid</button>'
        '<p class="bid-status" data-bid-status aria-live="polite"></p>'
        '</form></details>'
    )


def render_slot_cards(ads: dict) -> str:
    """Slot cards for the advertise page with live figures and a bid form each."""
    lt = ads["lifetime"]
    cards = []

    def card(key, label, position, price_line, status_line, bid_label, per_month, featured=False):
        cards.append(
            f'<article class="slot{" featured" if featured else ""}" id="{key}" data-slot="{key}">'
            f'<h3>{html.escape(label)}</h3><p class="pos">{html.escape(position)}</p>'
            f'<p class="price">{price_line}</p><p class="status" data-slot-status>{status_line}</p>'
            + _bid_form(key, ads[key], per_month, bid_label, featured) + "</article>"
        )

    card("lifetime", lt["label"], lt["position"],
         f"Reserve <b>{money(lt['reserve'])}</b> · one payment · never expires",
         _status_line(lt, False), "Bid on the lifetime slot", False, featured=True)

    for key in ("header", "rail"):
        s = ads[key]
        per_term = s["reserve_month"] * s["term_days"] // 30
        status = _status_line(s, True)
        if s.get("sponsor"):
            status = f"Held by <b>{html.escape(s['sponsor']['name'])}</b> · the next term opens for bids before this one ends"
        card(key, s["label"], s["position"],
             f"Reserve <b>{money(s['reserve_month'])}</b> / month · billed as <b>{money(per_term)}</b> per {s['term_days']} day term",
             status, f"Bid on the {s['label'].lower()}", True)

    f = ads["footer"]
    per_term = f["reserve_month"] * f["term_days"] // 30
    open_units = sum(1 for u in f["units"] if not u.get("sponsor"))
    status = _status_line(f, True)
    if not open_units:
        status = "All units held · the next term opens for bids before this one ends"
    card("footer", f["label"], f["position"],
         f"Reserve <b>{money(f['reserve_month'])}</b> / month · billed as <b>{money(per_term)}</b> per {f['term_days']} day term · <b>{open_units}</b> of {len(f['units'])} units open",
         status, "Bid on a footer unit", True)
    return "\n".join(cards)
