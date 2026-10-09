"""Sponsor slots: reads data/ads.json and renders the homepage units and the
advertise page's slot cards. Every unit is static HTML, tagged "Ad", and
links with rel="sponsored". No scripts, no tracking."""

import html
import json
import pathlib
import urllib.parse

ROOT = pathlib.Path(__file__).parent
ADS_FILE = ROOT / "data" / "ads.json"
X_DM_RECIPIENT_ID = "1400492097082327040"


def load() -> dict:
    return json.loads(ADS_FILE.read_text(encoding="utf-8"))


def bid_url(slot_label: str, amount_hint: str) -> str:
    text = (
        f"Hi! I'd like to bid on the {slot_label} slot on omarchyapps.com.\n\n"
        f"My bid: $ ({amount_hint})\n"
        "Product name: \n"
        "Link: \n"
        "One-line tagline: \n"
        "Billing email: "
    )
    return "https://x.com/messages/compose?" + urllib.parse.urlencode({"recipient_id": X_DM_RECIPIENT_ID, "text": text})


def money(n) -> str:
    return f"${n:,.0f}"


def _unit(sponsor: dict, tag: str, cls: str = "", image: bool = False) -> str:
    name = html.escape(sponsor["name"])
    tagline = html.escape(sponsor.get("tagline", ""))
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


def _lifetime_auction_card(ads: dict) -> str:
    lt = ads["lifetime"]
    bid = lt.get("high_bid")
    status = f"Current high bid {money(bid)}" if bid else f"Reserve {money(lt['reserve'])} · no bids yet"
    closes = f" · closes {html.escape(lt['closes'])}" if lt.get("closes") else ""
    return (
        '<a class="ad lifetime stack open" href="/advertise.html#lifetime"><span class="tag">Lifetime sponsor</span>'
        '<span class="mark" aria-hidden="true">◆</span><span class="copy"><strong>This spot is up for auction</strong>'
        f'<span class="sub">One sponsor, forever, always right here. {status}{closes}.</span></span>'
        '<span class="cta">Place a bid →</span></a>'
    )


def _open_card(slot: dict, anchor: str, cls: str = "") -> str:
    """Placeholder for a paid slot nobody holds yet: quiet, dashed, honest."""
    per_term = slot["reserve_month"] * slot["term_days"] // 30
    hb = slot.get("high_bid")
    status = f"high bid {money(hb)}" if hb else f"from {money(slot['reserve_month'])}/mo"
    return (
        f'<a class="ad open {cls}" href="/advertise.html#{anchor}"><span class="tag">Ad · open slot</span>'
        f'<span class="mark" aria-hidden="true">+</span><span class="copy"><strong>{html.escape(slot["label"])} is open</strong>'
        f'<span class="sub">{status} · {slot["term_days"]} day term · billed {money(per_term)}</span></span>'
        '<span class="cta">Bid →</span></a>'
    )


def render_homepage(ads: dict) -> dict[str, str]:
    """Return the three homepage placeholders. Open slots show a bid card."""
    h = ads["header"]
    header_unit = _unit(h["sponsor"], "Ad", "text") if h.get("sponsor") else _open_card(h, "header", "text")
    header = f'<div class="ad-header">{header_unit}</div>'

    lt = ads["lifetime"]
    rail_units = [_unit(lt["sponsor"], "Lifetime sponsor", "lifetime stack", image=True) if lt.get("sponsor") else _lifetime_auction_card(ads)]
    r = ads["rail"]
    rail_units.append(_unit(r["sponsor"], "Ad", "stack", image=True) if r.get("sponsor") else _open_card(r, "rail", "stack"))
    rail = ('<aside class="ad-rail" aria-label="Sponsors">' + "".join(rail_units)
            + '<p class="rail-note">Sponsors keep the store free · <a href="/advertise.html">advertise</a></p></aside>')

    f = ads["footer"]
    footer_units = [_unit(u["sponsor"], "Ad") if u.get("sponsor") else _open_card(f, "footer") for u in f["units"]]
    footer = ('<div class="ad-footer"><h2 class="sec-label">Sponsors <small>' + f'{sum(1 for u in f["units"] if not u.get("sponsor"))} of {len(f["units"])} footer units open'
              + '</small></h2><div class="ad-footer-row">' + "".join(footer_units) + "</div></div>")
    return {"__AD_HEADER__": header, "__AD_RAIL__": rail, "__AD_FOOTER__": footer}


def render_slot_cards(ads: dict) -> str:
    """Slot cards for the advertise page, with live reserve and high-bid figures."""
    lt = ads["lifetime"]
    cards = []

    def card(anchor, label, position, price_line, status_line, bid_label, hint, featured=False):
        cards.append(
            f'<article class="slot{" featured" if featured else ""}" id="{anchor}">'
            f'<h3>{html.escape(label)}</h3><p class="pos">{html.escape(position)}</p>'
            f'<p class="price">{price_line}</p><p class="status">{status_line}</p>'
            f'<a class="button{"" if featured else " ghost"}" href="{html.escape(bid_url(label, hint))}" target="_blank" rel="noopener">{bid_label} ↗</a></article>'
        )

    bid = lt.get("high_bid")
    lt_status = f"Current high bid <b>{money(bid)}</b>" if bid else "No bids yet"
    if lt.get("closes"):
        lt_status += f" · bidding closes <b>{html.escape(lt['closes'])}</b>"
    elif lt.get("opened"):
        lt_status += f" · opened {html.escape(lt['opened'])}"
    else:
        lt_status += f" · the {lt['auction_days']} day clock starts at the first qualifying bid"
    card("lifetime", lt["label"], lt["position"],
         f"Reserve <b>{money(lt['reserve'])}</b> · one payment · never expires",
         lt_status, "Bid on the lifetime slot", f"reserve {money(lt['reserve'])}", featured=True)

    for key in ("header", "rail"):
        s = ads[key]
        per_term = s["reserve_month"] * s["term_days"] // 30
        hb = s.get("high_bid")
        status = f"Current high bid <b>{money(hb)}</b> per {s['term_days']} days" if hb else "Open · no bids yet"
        if s.get("sponsor"):
            status = f"Held by <b>{html.escape(s['sponsor']['name'])}</b> · next term opens for bids 14 days before it ends"
        card(key, s["label"], s["position"],
             f"Reserve <b>{money(s['reserve_month'])}</b> / month · billed as <b>{money(per_term)}</b> per {s['term_days']} day term",
             status, f"Bid on the {s['label'].lower()}", f"reserve {money(per_term)} per {s['term_days']} days")

    f = ads["footer"]
    per_term = f["reserve_month"] * f["term_days"] // 30
    taken = sum(1 for u in f["units"] if u.get("sponsor"))
    open_units = len(f["units"]) - taken
    status = f"<b>{open_units}</b> of {len(f['units'])} units open" if open_units else "All units held · next term opens for bids 14 days before it ends"
    card("footer", f["label"], f["position"],
         f"Reserve <b>{money(f['reserve_month'])}</b> / month · billed as <b>{money(per_term)}</b> per {f['term_days']} day term",
         status, "Bid on a footer unit", f"reserve {money(per_term)} per {f['term_days']} days")
    return "\n".join(cards)
