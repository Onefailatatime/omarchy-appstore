"""Download upstream app screenshots and resize them for our own origin.

Converted files live in dist/images/screenshots/ and are reused across the
twice-daily refresh when the upstream bytes have not changed. A failed
download keeps the original upstream URL.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST_IMAGES = "images/screenshots"
MANIFEST_FILE = ROOT / "data" / "screenshot-manifest.json"
TOOL_DIR = ROOT / "tools" / "screenshots"
OPTIMIZE = TOOL_DIR / "optimize.mjs"
NODE = os.environ.get("NODE", "node")
QUALITY = 75
WIDTHS = (1200, 600)
MAX_BYTES = 40 * 1024 * 1024
TIMEOUT = 25
USER_AGENT = "omarchyapps-screenshot-optimizer/1.0 (https://omarchyapps.com/about.html)"

# url -> localized fields (url, srcset, sources, width, height, local)
_localized: dict[str, dict] = {}


def _opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(urllib.request.HTTPSHandler())


def _request(url: str, method: str = "GET", headers: dict | None = None) -> urllib.request.Request:
    hdrs = {"User-Agent": USER_AGENT, "Accept": "image/*,*/*;q=0.8"}
    if headers:
        hdrs.update(headers)
    return urllib.request.Request(url, method=method, headers=hdrs)


def _load_manifest() -> dict:
    if MANIFEST_FILE.exists():
        return json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    return {"version": 1, "quality": QUALITY, "widths": list(WIDTHS), "images": {}}


def _save_manifest(manifest: dict) -> None:
    MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _ensure_sharp() -> None:
    probe = subprocess.run(
        [NODE, "-e", "import('sharp').then(() => process.exit(0)).catch(() => process.exit(1))"],
        cwd=TOOL_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if probe.returncode == 0:
        return
    lock = TOOL_DIR / "package-lock.json"
    cmd = [NODE.replace("node", "npm") if NODE.endswith("node") else "npm", "ci" if lock.exists() else "install"]
    # Prefer the npm next to node.
    npm = str(Path(NODE).with_name("npm")) if Path(NODE).name == "node" else "npm"
    cmd = [npm, "ci" if lock.exists() else "install"]
    subprocess.run(cmd, cwd=TOOL_DIR, check=True)


def _head_etag(url: str) -> str | None:
    try:
        with _opener().open(_request(url, method="HEAD"), timeout=TIMEOUT) as resp:
            return resp.headers.get("ETag") or resp.headers.get("etag")
    except Exception:
        return None


def _download(url: str) -> tuple[bytes, str, str | None]:
    with _opener().open(_request(url), timeout=TIMEOUT) as resp:
        ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        etag = resp.headers.get("ETag") or resp.headers.get("etag")
        chunks = []
        total = 0
        while True:
            chunk = resp.read(64 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_BYTES:
                raise ValueError(f"image larger than {MAX_BYTES} bytes")
            chunks.append(chunk)
        return b"".join(chunks), ctype, etag


def _is_raster(content_type: str, url: str, data: bytes) -> bool:
    if content_type in {"image/svg+xml", "text/html", "application/json", "text/plain"}:
        return False
    if url.lower().split("?", 1)[0].endswith(".svg"):
        return False
    if data.startswith(b"<") or data.lstrip().startswith(b"<?xml") or data.lstrip().startswith(b"<svg"):
        return False
    return True


def _files_exist(dist: Path, entry: dict) -> bool:
    for variant in entry.get("files") or []:
        for key in ("webp", "avif"):
            rel = variant.get(key)
            if rel and not (dist / rel).is_file():
                return False
        if not variant.get("webp"):
            return False
    return bool(entry.get("files"))


def _fields_from_entry(entry: dict) -> dict:
    files = sorted(entry["files"], key=lambda f: f["width"])
    largest = files[-1]
    sources = []
    avif_bits = [f"{'/' + f['avif']} {f['width']}w" for f in files if f.get("avif")]
    webp_bits = [f"{'/' + f['webp']} {f['width']}w" for f in files if f.get("webp")]
    if avif_bits:
        sources.append({"type": "image/avif", "srcset": ", ".join(avif_bits)})
    if webp_bits:
        sources.append({"type": "image/webp", "srcset": ", ".join(webp_bits)})
    return {
        "url": "/" + largest["webp"],
        "srcset": ", ".join(webp_bits),
        "sizes": "(max-width: 700px) 100vw, 1200px",
        "sources": sources,
        "width": entry["width"],
        "height": entry["height"],
        "local": True,
        "animated": bool(entry.get("animated")),
    }


def _relative_files(dist: Path, result: dict) -> list[dict]:
    written = []
    for variant in result["files"]:
        rec = {"width": variant["width"], "webp": None, "avif": None}
        for fmt in ("webp", "avif"):
            src = variant.get(fmt)
            if not src:
                continue
            path = Path(src)
            rec[fmt] = f"{DIST_IMAGES}/{path.name}"
            # Confirm the optimizer wrote into dist/images/screenshots.
            if not (dist / rec[fmt]).is_file():
                raise FileNotFoundError(rec[fmt])
        written.append(rec)
    return written


def _optimize(input_path: Path, stem: str, dest_dir: Path) -> dict:
    _ensure_sharp()
    dest_dir.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [
            NODE,
            str(OPTIMIZE),
            "--input", str(input_path),
            "--out-dir", str(dest_dir),
            "--stem", stem,
            "--quality", str(QUALITY),
            "--widths", ",".join(str(w) for w in WIDTHS),
        ],
        cwd=TOOL_DIR,
        check=True,
        capture_output=True,
        text=True,
    )
    line = proc.stdout.strip().splitlines()[-1]
    result = json.loads(line)
    sidecar = dest_dir / f"{stem}.json"
    sidecar.unlink(missing_ok=True)
    return result


def localize_url(url: str, dist: Path, manifest: dict) -> dict | None:
    """Return localized fields, or None to keep the upstream URL."""
    images = manifest.setdefault("images", {})
    existing = images.get(url)
    etag = _head_etag(url)
    if existing and existing.get("etag") and etag and existing["etag"] == etag and _files_exist(dist, existing):
        return _fields_from_entry(existing)
    if existing and not etag and _files_exist(dist, existing):
        # Upstream did not answer HEAD; keep the converted files we already have
        # unless a later GET shows a new hash.
        try:
            data, ctype, new_etag = _download(url)
        except Exception:
            return _fields_from_entry(existing)
        digest = hashlib.sha256(data).hexdigest()
        if digest == existing.get("sha256"):
            if new_etag and new_etag != existing.get("etag"):
                existing["etag"] = new_etag
            return _fields_from_entry(existing)
        return _convert(url, dist, manifest, data, ctype, new_etag, digest)
    try:
        data, ctype, new_etag = _download(url)
    except Exception:
        if existing and _files_exist(dist, existing):
            return _fields_from_entry(existing)
        return None
    digest = hashlib.sha256(data).hexdigest()
    if existing and digest == existing.get("sha256") and _files_exist(dist, existing):
        existing["etag"] = new_etag or existing.get("etag")
        return _fields_from_entry(existing)
    return _convert(url, dist, manifest, data, ctype, new_etag, digest)


def _convert(url: str, dist: Path, manifest: dict, data: bytes, ctype: str, etag: str | None, digest: str) -> dict | None:
    if not data or not _is_raster(ctype, url, data):
        return None
    stem = digest[:16]
    with tempfile.TemporaryDirectory(prefix="oa-shot-src-") as tmp:
        suffix = ".bin"
        if "jpeg" in ctype or "jpg" in ctype:
            suffix = ".jpg"
        elif "png" in ctype:
            suffix = ".png"
        elif "webp" in ctype:
            suffix = ".webp"
        elif "gif" in ctype:
            suffix = ".gif"
        elif "avif" in ctype:
            suffix = ".avif"
        src = Path(tmp) / f"src{suffix}"
        src.write_bytes(data)
        try:
            result = _optimize(src, stem, dist / DIST_IMAGES)
        except Exception:
            return None
    files = _relative_files(dist, result)
    entry = {
        "etag": etag,
        "sha256": digest,
        "content_type": ctype,
        "width": result["width"],
        "height": result["height"],
        "animated": result.get("animated", False),
        "files": files,
    }
    manifest.setdefault("images", {})[url] = entry
    return _fields_from_entry(entry)


def prepare(dist: Path, urls: list[str]) -> dict:
    """Convert every unique screenshot URL. Returns a short summary."""
    manifest = _load_manifest()
    seen = []
    used = set()
    converted = reused = failed = skipped = 0
    for url in urls:
        if not url or url in used:
            continue
        used.add(url)
        before = json.dumps(manifest.get("images", {}).get(url, {}), sort_keys=True)
        fields = localize_url(url, dist, manifest)
        if fields:
            _localized[url] = fields
            after = json.dumps(manifest.get("images", {}).get(url, {}), sort_keys=True)
            if before and before == after:
                reused += 1
            else:
                converted += 1
            seen.append(url)
        else:
            # Leave _localized unset so apply() keeps the upstream URL.
            skipped += 1 if url else 0
            failed += 1
    # Drop converted files no longer referenced.
    keep = set()
    for url in seen:
        for variant in manifest.get("images", {}).get(url, {}).get("files") or []:
            for key in ("webp", "avif"):
                if variant.get(key):
                    keep.add(variant[key])
    shot_dir = dist / DIST_IMAGES
    if shot_dir.is_dir():
        for path in shot_dir.iterdir():
            rel = f"{DIST_IMAGES}/{path.name}"
            if path.is_file() and rel not in keep:
                path.unlink()
    # Drop manifest entries we no longer use so the next refresh stays small.
    manifest["images"] = {url: manifest["images"][url] for url in seen if url in manifest.get("images", {})}
    manifest["quality"] = QUALITY
    manifest["widths"] = list(WIDTHS)
    _save_manifest(manifest)
    return {"converted": converted, "reused": reused, "failed": failed, "total": len(used)}


def apply(image: dict) -> dict:
    """Merge localized fields onto one profile image dict, keeping attribution."""
    url = image.get("url") or ""
    extra = _localized.get(url)
    if not extra:
        return image
    out = dict(image)
    out["upstream_url"] = url
    out.update(extra)
    return out


def img_tag(image: dict, *, first: bool = False, alt: str = "") -> str:
    """HTML for one screenshot, with srcset, dimensions, and load hints."""
    from html import escape
    alt = escape(alt or image.get("alt") or "App screenshot")
    src = escape(image["url"])
    width = image.get("width")
    height = image.get("height")
    dims = f' width="{int(width)}" height="{int(height)}"' if width and height else ""
    srcset = f' srcset="{escape(image["srcset"])}"' if image.get("srcset") else ""
    sizes = f' sizes="{escape(image["sizes"])}"' if image.get("sizes") and image.get("srcset") else ""
    if first:
        loading = ' fetchpriority="high" decoding="async"'
    else:
        loading = ' loading="lazy" decoding="async"'
    referrer = "" if image.get("local") else ' referrerpolicy="no-referrer"'
    img = f'<img src="{src}"{srcset}{sizes}{dims} alt="{alt}"{loading}{referrer}>'
    sources = image.get("sources") or []
    if sources:
        parts = []
        for source in sources:
            sizes_attr = f' sizes="{escape(image["sizes"])}"' if image.get("sizes") else ""
            parts.append(
                f'<source type="{escape(source["type"])}" srcset="{escape(source["srcset"])}"{sizes_attr}>'
            )
        img = "<picture>" + "".join(parts) + img + "</picture>"
    return img
