#!/usr/bin/env python3
"""Add verified, remotely hosted README screenshots to no-video profiles.

Images are inspected in memory and are never downloaded into the site. The
result stores only upstream URLs and README attribution in enrichment.json.
"""

import base64
import concurrent.futures
import html
import json
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "data" / "packages-brief.json"
ENRICHMENT = ROOT / "data" / "enrichment.json"
MAX_PER_REPO = 4
UA = "omarchy-appstore-readme-media/1.0"
GITHUB_RE = re.compile(r"^https://github\.com/([^/]+)/([^/#?]+)")
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((?:<)?([^\s)>]+)(?:>)?(?:\s+['\"][^'\"]*['\"])?\)")
HTML_IMAGE_RE = re.compile(r"<img\b[^>]*?\bsrc=['\"]([^'\"]+)['\"][^>]*>", re.I)
ALT_RE = re.compile(r"\balt=['\"]([^'\"]*)['\"]", re.I)
BAD_RE = re.compile(r"(?:badge|shield|status|coverage|license|workflow|build|download|stars?|forks?)", re.I)
NON_SCREENSHOT_RE = re.compile(
    r"(?:logo|icon|avatar|favicon|wordmark|sponsor|contrib|donate|ko-?fi|banner|hero|subtitle|diagram|mascot|lockup|snowglobe|battery[_-]?support)",
    re.I,
)
GOOD_RE = re.compile(r"(?:screen(?:shot)?|preview|demo|interface|window|gallery|example|image|app)", re.I)


def token() -> str:
    return subprocess.run(["gh", "auth", "token"], check=True, capture_output=True, text=True).stdout.strip()


def api_readme(repo: str, auth: str) -> tuple[str, str, str] | None:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/readme",
        headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {auth}", "User-Agent": UA},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.load(response)
        body = base64.b64decode(data["content"]).decode("utf-8", "replace")
        return body, data["download_url"], data["html_url"]
    except (OSError, KeyError, ValueError):
        return None


def candidates(markdown: str, raw_readme: str) -> list[tuple[str, str]]:
    found = [(html.unescape(url), alt) for alt, url in MARKDOWN_IMAGE_RE.findall(markdown)]
    for tag in HTML_IMAGE_RE.findall(markdown):
        # HTML_IMAGE_RE returns only src; recover a useful empty-alt fallback.
        found.append((html.unescape(tag), ""))
    output = []
    seen = set()
    for source, alt in found:
        source = source.strip().replace("\\", "/")
        label = f"{alt} {source}"
        parsed = urllib.parse.urlparse(source)
        if source.startswith("data:") or parsed.scheme not in ("", "http", "https"):
            continue
        if BAD_RE.search(label) or NON_SCREENSHOT_RE.search(label):
            continue
        if parsed.netloc in {
            "img.shields.io", "badge.fury.io", "api.codacy.com", "codecov.io",
            "contrib.rocks", "ko-fi.com",
        }:
            continue
        url = urllib.parse.urljoin(raw_readme, source)
        url = url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/") if "/blob/" in url else url
        final = urllib.parse.urlparse(url)
        if final.path.lower().endswith(".svg") and final.netloc != "asciinema.org":
            continue
        key = urllib.parse.urlsplit(url)._replace(query="", fragment="").geturl()
        if key in seen:
            continue
        seen.add(key)
        score = 2 if GOOD_RE.search(label) else 0
        output.append((url, alt.strip() or "Project screenshot", score))
    output.sort(key=lambda item: item[2], reverse=True)
    return [(url, alt) for url, alt, _ in output[: MAX_PER_REPO * 2]]


def valid_image(item: tuple[str, str]) -> tuple[str, str] | None:
    url, alt = item
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/*"})
        with urllib.request.urlopen(req, timeout=20) as response:
            if not response.headers.get("Content-Type", "").lower().startswith("image/"):
                return None
            chunk = response.read(4096)
            if len(chunk) < 300:
                return None
        return url, alt
    except OSError:
        return None


def main() -> None:
    packages = json.loads(PACKAGES.read_text())
    enrichment = json.loads(ENRICHMENT.read_text())
    by_repo: dict[str, list[str]] = {}
    for package in packages:
        profile = enrichment.get(package["name"], {})
        profile.pop("readme_screenshots", None)
        if profile.get("youtube_id"):
            continue
        project = package.get("github") or package.get("url", "")
        match = GITHUB_RE.match(project)
        if match:
            repo = f"{match.group(1)}/{match.group(2).removesuffix('.git')}"
            by_repo.setdefault(repo, []).append(package["name"])

    auth = token()
    found_repos = found_packages = 0
    for repo, names in sorted(by_repo.items()):
        result = api_readme(repo, auth)
        if not result:
            continue
        markdown, raw_readme, readme_url = result
        possible = candidates(markdown, raw_readme)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            verified = [item for item in pool.map(valid_image, possible) if item][:MAX_PER_REPO]
        if not verified:
            continue
        records = [{"url": url, "source_url": readme_url, "alt": alt} for url, alt in verified]
        found_repos += 1
        found_packages += len(names)
        for name in names:
            enrichment.setdefault(name, {})["readme_screenshots"] = records

    ENRICHMENT.write_text(json.dumps(enrichment, indent=1, sort_keys=True) + "\n")
    print(f"README galleries: {found_repos} repositories, {found_packages} no-video package profiles")
    print("Stored remote URLs only; no image files were saved.")


if __name__ == "__main__":
    main()
