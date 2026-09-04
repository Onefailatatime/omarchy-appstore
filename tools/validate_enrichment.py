#!/usr/bin/env python3
"""Ground-truth check every screenshot_url and youtube_id a research pass
proposed, before it ever reaches data/enrichment.json.

An agent's own confidence is not evidence: a screenshot_url might be a normal
webpage, not an image, and a youtube_id might be well-formed and still not
exist, or exist but be unrelated to what the title claims. This script makes
one real HTTP request per claim and drops anything that doesn't check out —
a missing image or video is a fine, honest outcome; a broken or wrong one
embedded on the page is not.

Usage: python3 tools/validate_enrichment.py candidates.json > data/enrichment.json
  candidates.json: {name: {..., screenshot_url, youtube_id, youtube_title}}
"""

import json
import re
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) omarchy-appstore-validator/1.0"}
YT_ID_RE = re.compile(r"^[\w-]{11}$")


def check_image(url: str) -> bool:
    if not url or not url.startswith(("http://", "https://")):
        return False
    try:
        req = urllib.request.Request(url, headers=UA, method="GET")
        with urllib.request.urlopen(req, timeout=15) as resp:
            ctype = resp.headers.get("Content-Type", "")
            if not ctype.startswith("image/"):
                return False
            # Read a little to confirm the body is actually present (some
            # servers 200 an empty/placeholder response for missing assets).
            chunk = resp.read(2048)
            return len(chunk) > 200
    except OSError:
        return False


def check_youtube(video_id: str) -> bool:
    if not YT_ID_RE.match(video_id or ""):
        return False
    oembed = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    try:
        req = urllib.request.Request(oembed, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status == 200
    except OSError:
        return False


def main() -> None:
    candidates = json.loads(open(sys.argv[1]).read()) if len(sys.argv) > 1 else json.loads(sys.stdin.read())
    out = {}
    dropped_shots, dropped_videos = [], []
    for name, prof in candidates.items():
        prof = dict(prof)
        shot = prof.get("screenshot_url", "")
        if shot and not check_image(shot):
            dropped_shots.append((name, shot))
            prof["screenshot_url"] = ""
        yt = prof.get("youtube_id", "")
        if yt and not check_youtube(yt):
            dropped_videos.append((name, yt))
            prof["youtube_id"] = ""
            prof["youtube_title"] = ""
        out[name] = prof
    print(json.dumps(out, indent=1, sort_keys=True))
    if dropped_shots:
        print(f"dropped {len(dropped_shots)} unverifiable screenshots:", file=sys.stderr)
        for n, u in dropped_shots:
            print(f"  {n}: {u}", file=sys.stderr)
    if dropped_videos:
        print(f"dropped {len(dropped_videos)} unverifiable youtube IDs:", file=sys.stderr)
        for n, v in dropped_videos:
            print(f"  {n}: {v}", file=sys.stderr)


if __name__ == "__main__":
    main()
