#!/usr/bin/env python3
"""Draft the release digest as a Resend broadcast.

Reads the same package data the site is built from, finds everything added
since the last issue, and creates the broadcast in Resend as a draft. Nothing
is ever sent from here: open the draft in Resend, write the news section, and
press send yourself.

    RESEND_API_KEY=re_... RESEND_SEGMENT_ID=seg_... \\
    NEWSLETTER_FROM="Omarchy App Store <hello@omarchyapps.com>" \\
    python3 tools/draft_newsletter.py [--dry-run]
"""

import datetime
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))  # the package data comes from build.py, one level up

from build import SITE_URL, load_packages, slug, sync_pkgbuilds  # noqa: E402

BROADCASTS_URL = "https://api.resend.com/broadcasts"
STATE_FILE = ROOT / "data" / "newsletter.json"
FIRST_ISSUE_DAYS = 7
# Resend swaps this for the recipient's own one-click unsubscribe link.
UNSUBSCRIBE = "{{{RESEND_UNSUBSCRIBE_URL}}}"


def last_issue() -> datetime.datetime:
    """When the previous issue was drafted; a week back on the first run."""
    now = datetime.datetime.now(datetime.timezone.utc)
    if not STATE_FILE.exists():
        return now - datetime.timedelta(days=FIRST_ISSUE_DAYS)
    stamp = json.loads(STATE_FILE.read_text())["last_issue"]
    return datetime.datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def issue_body(new: list[dict], since: datetime.datetime) -> str:
    lines = [
        f"{len(new)} new {'app' if len(new) == 1 else 'apps'} landed in the official"
        f" Omarchy repo since {since.date().isoformat()}.",
        "",
    ]
    for p in new:
        lines += [
            p["name"],
            (p["tagline"] or p["desc"] or "").strip(),
            f"  omarchy pkg add {p['name']}",
            f"  {SITE_URL}/apps/{slug(p['name'])}.html",
            "",
        ]
    lines += [
        "---",
        "",
        "[News and gossip go here. Write this section in Resend before sending.]",
        "",
        "---",
        "",
        f"Browse every package: {SITE_URL}",
        f"Unsubscribe: {UNSUBSCRIBE}",
    ]
    return "\n".join(lines)


def create_draft(key: str, payload: dict) -> dict:
    request = urllib.request.Request(
        BROADCASTS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"authorization": f"Bearer {key}", "content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        sys.exit(f"resend rejected the broadcast ({error.code}): {error.read().decode('utf-8', 'replace')}")


def main() -> None:
    dry_run = "--dry-run" in sys.argv[1:]
    since = last_issue()

    sync_pkgbuilds()
    new = sorted(
        (p for p in load_packages() if p["added"] and
         datetime.datetime.fromtimestamp(p["added"], datetime.timezone.utc) > since),
        key=lambda p: (-p["added"], p["name"]),
    )
    if not new:
        print(f"nothing new since {since.date().isoformat()} — no draft created")
        return

    subject = f"{len(new)} new {'app' if len(new) == 1 else 'apps'} in the Omarchy repo"
    body = issue_body(new, since)
    if dry_run:
        print(f"subject: {subject}\n\n{body}")
        return

    key = os.environ.get("RESEND_API_KEY")
    segment = os.environ.get("RESEND_SEGMENT_ID")
    sender = os.environ.get("NEWSLETTER_FROM")
    if not key or not segment or not sender:
        sys.exit("set RESEND_API_KEY, RESEND_SEGMENT_ID, and NEWSLETTER_FROM (see README)")

    # No "send": the broadcast stays a draft until a human sends it in Resend.
    draft = create_draft(key, {
        "segment_id": segment,
        "from": sender,
        "reply_to": os.environ.get("NEWSLETTER_REPLY_TO", sender),
        "subject": subject,
        "name": f"Release digest {datetime.date.today().isoformat()}",
        "text": body,
    })

    drafted = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    STATE_FILE.write_text(json.dumps({"last_issue": drafted.isoformat().replace("+00:00", "Z")}, indent=2) + "\n")
    print(f"drafted {draft.get('id', '?')} · {len(new)} apps · {', '.join(p['name'] for p in new)}")
    print("open resend.com/broadcasts to write the news section and send")


if __name__ == "__main__":
    main()
