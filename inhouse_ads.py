"""In house ads for omarchyapps.com: twenty product ideas, one waitlist page each.

build() runs at the very end of build.py, after page dates, the sitemap and
IndexNow inputs are final, so the ad pages never enter the sitemap or the
page date ledger and the injected ad slot never moves a page's lastmod.

  dist/ad1.html ... dist/ad20.html  served at /ad1 ... /ad20 by src/worker.js
  dist/oa-ads.js                    picks the ad for each page view (fair rotation)
  every other page                  gets one empty slot under the top bar

Copy rules: plain words, no dashes, no urgency, no invented numbers.
"""
from __future__ import annotations

import html
import json
import pathlib
import re

UMAMI = '<script defer src="/stats/script.js" data-website-id="e45b1c4a-5d0b-431c-b50a-88bcc6fe91e9" data-domains="omarchyapps.com,www.omarchyapps.com"></script>'

# rank, name, ad line, headline, problem, how it works, planned price
ADS: list[dict] = [
    dict(name="Homesafe", line="Snapshots skip your home folder. Back it up.",
         headline="Back up your whole home folder with one keystroke",
         problem="Omarchy snapshots roll back the system, but nothing in the base install backs up your home folder, so a deleted file or a dead drive means lost work.",
         how=["Encrypted backups of your home folder run in the background.", "Restore a single file or everything from the Omarchy menu.", "250 GB of storage included, with your key kept on your machine."],
         price="$6 per month or $60 per year"),
    dict(name="Theme Vault", line="Twelve handcrafted themes that match every app.",
         headline="Every app on your desktop, finally in one theme",
         problem="Free themes cover the terminal and editor, but GTK4 apps, browsers and wallpapers rarely match end to end.",
         how=["Twelve themes, each covering terminal, Neovim, GTK apps, browser and wallpapers.", "Install and switch with the theme tools you already use.", "Free updates when new apps need matching."],
         price="$29 one time for all 12 themes"),
    dict(name="Query Deck", line="A fast keyboard first database client for Omarchy.",
         headline="Query your databases without leaving the keyboard",
         problem="Developers who switch from a Mac lose polished database clients like Postico, and the Linux options are either heavy Electron apps or terminal tools without a fast keyboard first GUI.",
         how=["A native, fast client for Postgres, MySQL and SQLite.", "Every action has a keybind: connect, browse tables, run and edit queries.", "Follows your Omarchy theme out of the box."],
         price="$49 one time license"),
    dict(name="Tiling Mastery", line="Master Omarchy in one weekend of video lessons.",
         headline="Own your Omarchy setup instead of copying someone else's",
         problem="Many users want to go from copying configs to understanding and owning their setup.",
         how=["Short video lessons on Hyprland, keybinds, themes and config.", "Each lesson ends with a change you make to your own machine.", "Optional live group Q and A calls."],
         price="$49 one time, or $99 with two live group Q and A calls"),
    dict(name="Config Doctor", line="Update Omarchy. Keep every custom tweak working.",
         headline="Check your custom config before every update",
         problem="Omarchy and Hyprland move fast, and personal config tweaks can fall out of step after an update.",
         how=["Scans your personal config before you update.", "Flags options that changed and suggests the new form.", "Applies fixes only when you approve them, with an easy undo."],
         price="$4 per month"),
    dict(name="Rice Market", line="Sell your Omarchy theme. Buy a finished one.",
         headline="The marketplace for Omarchy themes and configs",
         problem="Creators who build great themes and configs have no Omarchy focused place to sell them.",
         how=["Creators list themes and configs with screenshots and install steps.", "Buyers install a purchase with one command.", "Creators keep most of every sale."],
         price="Free to list, 8% per sale"),
    dict(name="WinGPU Kit", line="Windows apps with real GPU power on Omarchy.",
         headline="Run GPU heavy Windows apps beside your Omarchy desktop",
         problem="Some Windows apps need a real GPU, and setting up passthrough on Linux is a weekend project.",
         how=["Checks your hardware first and tells you what will work.", "Guided setup for a Windows VM with GPU passthrough.", "Launch Windows apps from your Omarchy launcher."],
         price="$49 one time"),
    dict(name="Desk Profiles", line="Dock your laptop. Monitors arrange themselves.",
         headline="Monitor layouts that remember every desk you use",
         problem="Docking a laptop at different desks means rearranging monitors by hand every time.",
         how=["Saves the monitor layout for each desk you use.", "Detects the desk when you plug in and applies its layout.", "Workspaces move to the right screens automatically."],
         price="$15 one time"),
    dict(name="Palette Pro", line="Raycast style power inside your Omarchy launcher.",
         headline="Pro extensions for the launcher you already use",
         problem="Mac switchers miss Raycast style extensions: AI commands, quick actions and app integrations from one launcher.",
         how=["A pack of extensions for the launcher you already use.", "AI commands, quick actions and app integrations.", "New extensions added every month."],
         price="$6 per month"),
    dict(name="Power Tune", line="Longer battery, cooler laptop, smarter GPU switching.",
         headline="More hours on battery from the same Omarchy laptop",
         problem="Hybrid GPU laptops can drain battery fast, and there is no simple app for charge limits and power profiles.",
         how=["One place for charge limits, power profiles and GPU switching.", "Presets for common laptops.", "Shows what is using your battery right now."],
         price="$19 one time"),
    dict(name="Focus Log", line="See where your hours go. Wayland native.",
         headline="Automatic time tracking built for Hyprland",
         problem="Automatic, window based time tracking has long been a pain point on Wayland desktops.",
         how=["Tracks time per app and window, built for Hyprland.", "Data stays on your machine by default.", "Weekly reports and exports for invoices."],
         price="$6 per month"),
    dict(name="Drive Bridge", line="Google Drive and OneDrive, native in your file manager.",
         headline="Your cloud drives, synced into Omarchy",
         problem="Google Drive and OneDrive users on Omarchy rely on third party sync tools to see their files in the file manager.",
         how=["Google Drive and OneDrive appear as folders in your file manager.", "Files download when you open them, so disk use stays low.", "Pick folders to keep offline."],
         price="$29 one time per cloud account"),
    dict(name="Game Key", line="One key turns Omarchy into a gaming rig.",
         headline="Gaming mode for Omarchy, tuned in one keystroke",
         problem="Turning an Omarchy machine into a tuned gaming setup takes many manual steps.",
         how=["One keybind switches into a tuned gaming mode.", "Sets performance, notifications and launchers for play.", "The same keybind switches everything back."],
         price="$9 one time"),
    dict(name="Demo Cast", line="Terminal demos that zoom and show every keystroke.",
         headline="Record terminal demos people can actually follow",
         problem="Developers recording terminal demos need keystroke overlays and zoom that follows the cursor.",
         how=["Records your screen with keystrokes shown on screen.", "Zoom follows the cursor automatically.", "Exports video sized for docs and social posts."],
         price="$39 one time"),
    dict(name="Live Walls", line="Living wallpapers that match your Omarchy theme.",
         headline="Animated wallpapers made for your theme",
         problem="Hyprland desktops stay static unless you wire up a wallpaper engine yourself.",
         how=["Animated wallpapers made to match popular themes.", "Light on battery, and they pause when a window is fullscreen.", "Switch wallpapers when you switch themes."],
         price="$9 per pack"),
    dict(name="Dot Sync", line="Same Omarchy setup on every machine you own.",
         headline="Your configs, themes and keybinds on every machine",
         problem="Running Omarchy on a desktop and a laptop means keeping configs in step by hand.",
         how=["Syncs configs, themes and keybinds between your machines.", "End to end encrypted.", "Keep some settings machine specific when you want."],
         price="$4 per month"),
    dict(name="Shell Port", line="Every server one keystroke away, synced everywhere.",
         headline="A keyboard first SSH cockpit for Omarchy",
         problem="Developers juggling many servers want saved hosts, keys and snippets synced in a fast keyboard UI.",
         how=["Saved hosts, keys and snippets in one keyboard UI.", "Connect to any server in a few keystrokes.", "Encrypted sync across your machines."],
         price="$5 per month"),
    dict(name="Laptop Fit Packs", line="Your exact laptop, tuned and tested for Omarchy.",
         headline="Tested fixes for your exact laptop model",
         problem="Some laptop models need small fixes for sound, sleep and lid behavior that are spread across many threads.",
         how=["One pack per laptop model, tested on real hardware.", "Covers sound, sleep, lid and function keys where needed.", "Installs with one command and can be removed the same way."],
         price="$15 per laptop model"),
    dict(name="Bar Widgets Pro", line="CI status, calendar and battery time in your bar.",
         headline="The widgets developers wish their top bar had",
         problem="The top bar shows system basics, but developers want CI status, next meeting and more at a glance.",
         how=["Widgets for CI status, your next meeting and battery time left.", "Styled to match your theme.", "Click a widget to open the details."],
         price="$12 one time"),
    dict(name="Snip Key", line="Type less. Expand snippets anywhere on Omarchy.",
         headline="Snippets that follow you across every app",
         problem="Typing the same commands, replies and boilerplate all day wastes keystrokes.",
         how=["Type a short trigger and it expands in any app.", "Snippets can include dates, clipboard and cursor position.", "Synced across your machines."],
         price="$3 per month"),
]
for i, ad in enumerate(ADS, 1):
    ad["rank"] = i
    ad["path"] = f"/ad{i}"

PAGE_TYPES = ("home", "app", "category", "tutorial", "guide", "other")
DASHES = re.compile("[\u2010-\u2015\u2212]|(?<=\\w)-(?=\\w)| - ")


def copy_problems() -> list[str]:
    """Copy rule check: no dashes in any visible ad or page text."""
    bad = []
    for ad in ADS:
        for key in ("name", "line", "headline", "problem", "price"):
            if DASHES.search(ad[key]):
                bad.append(f"ad{ad['rank']} {key}: {ad[key]}")
        for h in ad["how"]:
            if DASHES.search(h):
                bad.append(f"ad{ad['rank']} how: {h}")
    return bad


def page_type(rel: str, tutorials: set[str], guides: set[str]) -> str:
    if rel == "index.html":
        return "home"
    if rel.startswith("apps/"):
        return "app"
    if rel.startswith("category/"):
        return "category"
    if rel in tutorials or rel == "tutorials.html":
        return "tutorial"
    if rel in guides or rel == "guides.html":
        return "guide"
    if rel.endswith("-on-omarchy.html"):  # older tutorial pages that stay in dist/
        return "tutorial"
    return "other"


MINI_CSS = """
@font-face{font-family:"JetBrains Mono";src:url(/fonts/jetbrains-mono-latin-700.woff2) format("woff2");font-weight:700;font-display:swap}
@font-face{font-family:"Geist";src:url(/fonts/geist-latin-wght-normal.woff2) format("woff2");font-weight:100 900;font-display:swap}
*{box-sizing:border-box}
html{background:#1a1b26;color:#c0caf5;-webkit-text-size-adjust:100%}
body{margin:0;font:16px/1.55 "Geist",system-ui,sans-serif}
main{max-width:40rem;margin:0 auto;padding:2.25rem 1.15rem 2.5rem}
.kicker{display:inline-block;margin:0 0 1rem;padding:.2em .6em;border:1px solid rgba(122,162,247,.55);border-radius:.4em;color:#7dcfff;font:700 .78rem/1.4 "JetBrains Mono",monospace;letter-spacing:.02em}
h1{margin:0 0 .75rem;font:700 clamp(1.6rem,6.2vw,2.3rem)/1.18 "JetBrains Mono",monospace;color:#c0caf5}
.lead{margin:0 0 1.75rem;color:rgba(192,202,245,.82);font-size:1.05rem}
h2{margin:1.9rem 0 .55rem;font:700 .82rem/1.3 "JetBrains Mono",monospace;text-transform:uppercase;letter-spacing:.08em;color:#7aa2f7}
p{margin:0 0 .8rem}
ul{margin:0;padding-left:1.15rem}
li{margin:0 0 .45rem}
.price{display:flex;flex-wrap:wrap;align-items:baseline;gap:.5rem;padding:.85rem 1rem;border:1px solid rgba(65,72,104,.8);border-radius:.4em;background:#24283b}
.price b{font:700 1.15rem/1.3 "JetBrains Mono",monospace;color:#9ece6a}
.price span{color:rgba(192,202,245,.7);font-size:.92rem}
form{margin-top:.4rem;padding:1.1rem 1rem 1.2rem;border:1px solid rgba(122,162,247,.45);border-radius:.4em;background:#24283b}
label,legend{display:block;margin:0 0 .35rem;font-weight:600;font-size:.95rem}
input[type=email],textarea{width:100%;padding:.7rem .75rem;border:1px solid rgba(65,72,104,.95);border-radius:.4em;background:#1a1b26;color:#c0caf5;font:inherit;font-size:16px}
input[type=email]:focus,textarea:focus{outline:2px solid #7aa2f7;outline-offset:1px}
textarea{min-height:5.5rem;resize:vertical}
.field{margin:0 0 1rem}
fieldset{margin:0 0 1.1rem;padding:0;border:0}
.choice{display:flex;gap:.6rem;flex-wrap:wrap}
.choice label{display:flex;align-items:center;gap:.45rem;margin:0;padding:.55rem .8rem;border:1px solid rgba(65,72,104,.95);border-radius:.4em;font-weight:400;cursor:pointer}
.choice input{accent-color:#7aa2f7;width:1.05rem;height:1.05rem}
button{width:100%;padding:.85rem 1rem;border:0;border-radius:.4em;background:#7aa2f7;color:#1a1b26;font:700 1rem/1.2 "JetBrains Mono",monospace;cursor:pointer}
button:hover{background:#7dcfff}
button[disabled]{opacity:.6;cursor:wait}
.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.msg{margin:.85rem 0 0;font-size:.95rem}
.msg.ok{color:#9ece6a}.msg.err{color:#ff9e64}
.note{margin-top:1.75rem;padding:.8rem 1rem;border-left:3px solid #ff9e64;background:rgba(255,158,100,.07);font-size:.93rem}
footer{max-width:40rem;margin:0 auto;padding:0 1.15rem 2.5rem;color:rgba(192,202,245,.55);font-size:.82rem}
@media (min-width:48rem){main{padding-top:4rem}}
""".strip()

MINI_JS = """
(function(){var AD=__AD__;function send(t,extra){var b=JSON.stringify(Object.assign({ad:AD,type:t,page:"mini"},extra||{}));try{if(navigator.sendBeacon&&navigator.sendBeacon("/api/ads/event",new Blob([b],{type:"application/json"})))return}catch(e){}fetch("/api/ads/event",{method:"POST",headers:{"content-type":"application/json"},body:b,keepalive:true}).catch(function(){})}
send("view");
var f=document.getElementById("wl"),m=document.getElementById("wl-msg"),src=(new URLSearchParams(location.search).get("from")||"").slice(0,20);f.source.value=src;
f.addEventListener("submit",function(e){e.preventDefault();var btn=f.querySelector("button");var who=f.querySelector("input[name=who]:checked");m.className="msg";m.textContent="";
if(!f.email.value||!f.email.checkValidity()){m.className="msg err";m.textContent="Please enter a valid email address.";return}
if(!who){m.className="msg err";m.textContent="Please choose myself or my company.";return}
btn.disabled=true;fetch("/api/waitlist",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({ad:AD,email:f.email.value,use_case:f.use_case.value,who:who.value,source:src,website:f.website.value})}).then(function(r){return r.json().then(function(d){return{ok:r.ok,d:d}})}).then(function(x){if(x.ok){f.reset();f.querySelectorAll("input,textarea,button").forEach(function(el){el.disabled=true});m.className="msg ok";m.textContent=x.d.status==="existing"?"You are already on the list. Your answers were updated. Thank you.":"Thank you. You are on the list, and we will email you when early access opens.";if(window.umami)umami.track("waitlist_signup",{ad:AD})}else{btn.disabled=false;m.className="msg err";m.textContent=(x.d&&x.d.error)||"Something went wrong. Please try again."}}).catch(function(){btn.disabled=false;m.className="msg err";m.textContent="Network error. Please try again."})})})();
""".strip()


def mini_page(ad: dict) -> str:
    e = html.escape
    how = "".join(f"<li>{e(h)}</li>" for h in ad["how"])
    js = MINI_JS.replace("__AD__", str(ad["rank"]))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(ad['name'])}: {e(ad['headline'])}</title>
<meta name="description" content="{e(ad['line'])}">
<meta name="robots" content="noindex, nofollow">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="theme-color" content="#1a1b26">
<link rel="icon" href="data:,">
<link rel="preload" href="/fonts/jetbrains-mono-latin-700.woff2" as="font" type="font/woff2" crossorigin>
<style>{MINI_CSS}</style>
{UMAMI}
</head>
<body>
<main>
  <p class="kicker">{e(ad['name'])} · coming soon</p>
  <h1>{e(ad['headline'])}</h1>
  <p class="lead">{e(ad['line'])}</p>
  <h2>The problem</h2>
  <p>{e(ad['problem'])}</p>
  <h2>How {e(ad['name'])} will solve it</h2>
  <ul>{how}</ul>
  <h2>Planned price</h2>
  <div class="price"><b>{e(ad['price'])}</b><span>Shown now so you know before you apply.</span></div>
  <h2>Apply to join the waitlist</h2>
  <form id="wl" method="post" action="/api/waitlist" novalidate>
    <input type="hidden" name="ad" value="{ad['rank']}">
    <input type="hidden" name="source" value="">
    <div class="hp" aria-hidden="true"><label for="website">Leave this empty</label><input id="website" name="website" tabindex="-1" autocomplete="off"></div>
    <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" inputmode="email" required maxlength="254" placeholder="you@example.com"></div>
    <div class="field"><label for="use_case">What would you use it for?</label><textarea id="use_case" name="use_case" maxlength="1000" placeholder="A sentence or two is plenty"></textarea></div>
    <fieldset><legend>Is this for you or your company?</legend><div class="choice"><label><input type="radio" name="who" value="myself" required> Myself</label><label><input type="radio" name="who" value="company"> My company</label></div></fieldset>
    <button type="submit">Apply to join the waitlist</button>
    <p class="msg" id="wl-msg" role="status" aria-live="polite"></p>
  </form>
  <p class="note"><b>Coming soon.</b> {e(ad['name'])} is not built yet. We are gathering interest first, and we will email you when early access opens. Your email is used only for this and is never sold or shared.</p>
</main>
<footer>An independent project. Not affiliated with Omarchy, Omacom or 37signals.</footer>
<script>{js}</script>
</body>
</html>
"""


def ads_js() -> str:
    data = [{"r": a["rank"], "n": a["name"], "l": a["line"]} for a in ADS]
    return ("/* In house ads for omarchyapps.com, built by inhouse_ads.py.\n"
            " * They fill the site's own sponsor slots only while no paid sponsor holds them:\n"
            " * the homepage header and footer rotations and the app profile banner.\n"
            " * Fair rotation: each browser starts at a random ad and then steps to the\n"
            " * next one for every slot it fills, so all twenty get equal exposure.\n"
            " * Impressions count once per slot when the ad is half visible; clicks\n"
            " * open /adN in a new tab. */\n"
            + ADS_RUNTIME.replace("__ADS__", json.dumps(data, separators=(",", ":"), ensure_ascii=False)))


# Each copy of the script fills the slots placed above it, so a slot is drawn
# as soon as it is parsed. The unit reuses the sponsor unit markup and classes
# (.ad, .ad.text, .mark, .copy, .sub, .cta) so it has the slot's size and look.
ADS_RUNTIME = r"""(function(){"use strict";
var ADS=__ADS__,N=ADS.length,KEY="oa_ad_next";
var slots=document.querySelectorAll("[data-oa-slot]:not([data-oa-done])");
function next(){var i;try{var s=localStorage.getItem(KEY);i=s===null?Math.floor(Math.random()*N):(parseInt(s,10)%N+N)%N;localStorage.setItem(KEY,String((i+1)%N))}catch(e){i=Math.floor(Math.random()*N)}return ADS[i]}
function send(ad,t,page){var b=JSON.stringify({ad:ad.r,type:t,page:page});try{if(navigator.sendBeacon&&navigator.sendBeacon("/api/ads/event",new Blob([b],{type:"application/json"})))return}catch(e){}try{fetch("/api/ads/event",{method:"POST",headers:{"content-type":"application/json"},body:b,keepalive:true})}catch(e){}}
function fill(slot){
slot.setAttribute("data-oa-done","1");
var type=slot.getAttribute("data-oa-slot")||"other",pos=slot.getAttribute("data-oa-pos")||"",page=pos?type+"_"+pos:type,ad=next();
var a=document.createElement("a");a.className=slot.getAttribute("data-oa-class")||"ad";
a.href="/ad"+ad.r+"?from="+encodeURIComponent(type)+(pos?"&slot="+encodeURIComponent(pos):"");a.target="_blank";a.rel="noopener";
a.setAttribute("data-oa-ad",String(ad.r));
a.innerHTML='<span class="mark" aria-hidden="true"></span><span class="copy"><strong></strong><span class="sub"></span></span><span class="cta">Join the waitlist ↗</span>';
a.querySelector(".mark").textContent=ad.n.charAt(0);a.querySelector("strong").textContent=ad.n;a.querySelector(".sub").textContent=ad.l;
a.setAttribute("aria-label",ad.n+": "+ad.l+" Opens the waitlist in a new tab.");
a.addEventListener("click",function(){send(ad,"click",page);if(window.umami)try{umami.track("house_ad_click",{ad:ad.r,page:type,slot:pos})}catch(e){}});
slot.appendChild(a);
var seen=false;function imp(){if(seen)return;seen=true;send(ad,"impression",page)}
if("IntersectionObserver" in window){var io=new IntersectionObserver(function(es){for(var k=0;k<es.length;k++){if(es[k].isIntersecting){imp();io.disconnect()}}},{threshold:.5});io.observe(a)}else imp()}
for(var j=0;j<slots.length;j++)fill(slots[j]);
})();"""


def slot_html(kind: str, pos: str, unit_class: str) -> str:
    return (f'<div class="oa-house" data-oa-slot="{kind}" data-oa-pos="{pos}" data-oa-class="{unit_class}"></div>'
            '<script src="/oa-ads.js"></script>')


# The site's designated sponsor slots (sponsors.py) and how an empty one looks
# in the built page. A slot held by a paid sponsor never matches, so it is left alone.
OPEN_CARD = r'<a class="ad open" href="/sponsor\.html#{anchor}">.*?</a>'
HOME_SLOTS = [
    ("header", re.compile(r'(<div class="ad-header">)' + OPEN_CARD.format(anchor="header") + r'(</div>)', re.S), "ad text"),
    ("footer", re.compile(r'(<div class="ad-footer"><h2 class="sec-label">Sponsors</h2>)' + OPEN_CARD.format(anchor="footer") + r'(</div>)', re.S), "ad"),
]
APP_HEADER_RE = re.compile(r'(<header class="app-header">.*?</header>\n)', re.S)

# Markup from earlier builds that must come out before pages are hashed:
# the old bar under the top bar (v1), plus anything this module adds now.
SLOT_STRIP = [
    re.compile(r'\n<div class="oa-house" data-oa-slot="[a-z]+" hidden></div><script src="/oa-ads.js"></script>'),
    re.compile(r'<div class="ad-app-banner"><div class="oa-house"[^>]*></div><script src="/oa-ads.js"></script></div>\n'),
]


def clean(dist: pathlib.Path) -> None:
    """Undo the last build's ads before pages are hashed for their dates.

    build.py does not rewrite every file in dist/ (old tutorial pages stay put),
    so strip ad markup from those too; otherwise their hash, and date, would move.
    The homepage is always rebuilt, so its open cards come back on their own."""
    for a in ADS:
        (dist / f"ad{a['rank']}.html").unlink(missing_ok=True)
    for page in dist.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        if "data-oa-slot" in text:
            for rx in SLOT_STRIP:
                text = rx.sub("", text)
            page.write_text(text, encoding="utf-8")


def build(dist: pathlib.Path, tutorials: set[str], guides: set[str]) -> dict:
    """Write the twenty ad pages and the runtime, then fill the empty sponsor
    slots: homepage header and footer, and the banner spot on each app page
    without a paid banner. Returns how many slots were filled per slot name."""
    bad = copy_problems()
    if bad:
        raise SystemExit("inhouse ads copy has dashes:\n" + "\n".join(bad))
    for a in ADS:
        (dist / f"ad{a['rank']}.html").write_text(mini_page(a), encoding="utf-8")
    (dist / "oa-ads.js").write_text(ads_js(), encoding="utf-8")
    counts = {"home_header": 0, "home_footer": 0, "app_banner": 0, "sponsor_held": 0}

    home = dist / "index.html"
    text = home.read_text(encoding="utf-8")
    for pos, rx, cls in HOME_SLOTS:
        text, n = rx.subn(lambda m, pos=pos, cls=cls: m.group(1) + slot_html("home", pos, cls) + m.group(2), text, count=1)
        counts[f"home_{pos}"] += n
        counts["sponsor_held"] += 1 - n
    home.write_text(text, encoding="utf-8")

    for page in sorted((dist / "apps").glob("*.html")):
        text = page.read_text(encoding="utf-8")
        if 'class="ad-app-banner"' in text:
            counts["sponsor_held"] += 1
            continue
        new, n = APP_HEADER_RE.subn(
            lambda m: m.group(1) + '<div class="ad-app-banner">' + slot_html("app", "banner", "ad text") + "</div>\n",
            text, count=1)
        if n:
            page.write_text(new, encoding="utf-8")
            counts["app_banner"] += 1
    return counts
