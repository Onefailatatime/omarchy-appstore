"""Download upstream app screenshots and resize them for our own origin.

Converted files live in dist/images/screenshots/ and are reused across the
twice-daily refresh when the upstream bytes have not changed. Animated GIF
or WebP files over about 300 KB become a muted looping video (MP4 and WebM)
with a still poster. A failed download or transcode keeps the current image
or the original upstream URL.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
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
VIDEO_MIN_BYTES = 300 * 1024
FFMPEG = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = os.environ.get("FFPROBE") or shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"

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


def _ffmpeg_version() -> str:
    try:
        out = subprocess.check_output([FFMPEG, "-version"], text=True, timeout=10)
        return out.splitlines()[0].replace("ffmpeg version ", "").split()[0]
    except Exception:
        return ""


def _probe_video(path: Path) -> dict:
    out = subprocess.check_output(
        [
            FFPROBE, "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height,nb_frames",
            "-of", "json", str(path),
        ],
        text=True, timeout=60,
    )
    streams = json.loads(out).get("streams") or [{}]
    stream = streams[0]
    frames = stream.get("nb_frames")
    try:
        frames = int(frames) if frames and frames != "N/A" else 0
    except (TypeError, ValueError):
        frames = 0
    return {
        "width": int(stream.get("width") or 0),
        "height": int(stream.get("height") or 0),
        "frames": frames,
    }


def _is_animated_bytes(data: bytes, ctype: str, path: Path | None = None) -> bool:
    if data.startswith(b"GIF8"):
        if path:
            try:
                return _probe_video(path).get("frames", 0) != 1
            except Exception:
                return len(data) > VIDEO_MIN_BYTES
        return True
    if b"ANIM" in data[:256] or (ctype or "").lower() in {"image/gif", "video/webp"}:
        return True
    if path and (ctype or "").lower() in {"image/webp", "image/gif"}:
        try:
            return _probe_video(path).get("frames", 0) > 1
        except Exception:
            return False
    return False


def _largest_local_still(dist: Path, entry: dict) -> Path | None:
    files = entry.get("files") or []
    paths = []
    for variant in files:
        rel = variant.get("webp") or variant.get("avif")
        if rel and (dist / rel).is_file():
            paths.append((variant.get("width") or 0, dist / rel))
    if not paths:
        return None
    paths.sort()
    return paths[-1][1]


def _video_complete(dist: Path, entry: dict) -> bool:
    video = entry.get("video") or {}
    if not video.get("poster"):
        return False
    if not video.get("mp4") and not video.get("webm"):
        return False
    for key in ("mp4", "webm", "poster"):
        rel = video.get(key)
        if rel and not (dist / rel).is_file():
            return False
    return True


def _wants_video(entry: dict | None, data: bytes | None = None, ctype: str = "", path: Path | None = None) -> bool:
    size = len(data) if data is not None else 0
    if data is not None:
        if size < VIDEO_MIN_BYTES:
            return False
        return _is_animated_bytes(data, ctype, path)
    if not entry:
        return False
    if entry.get("video") and not entry.get("video").get("mp4"):
        return True
    if not entry.get("animated"):
        return False
    # Fall back to the size of the current served still or animation.
    total = 0
    for variant in entry.get("files") or []:
        for key in ("webp", "avif"):
            rel = variant.get(key)
            # Size is checked later against dist; treat animated entries as candidates.
            if rel:
                total = 1
    return bool(entry.get("animated") and total)


def _transcode_video(src: Path, dist: Path, stem: str) -> dict | None:
    """Write MP4, WebM and a still poster. Returns relative paths or None."""
    if not Path(FFMPEG).is_file() and not shutil.which("ffmpeg"):
        return None
    dest = dist / DIST_IMAGES
    dest.mkdir(parents=True, exist_ok=True)
    vf = "scale='min(1200,iw)':-2:flags=lanczos"
    mp4 = dest / f"{stem}-1200.mp4"
    webm = dest / f"{stem}-1200.webm"
    try:
        subprocess.run(
            [
                FFMPEG, "-y", "-i", str(src), "-an", "-vf", vf,
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", "-crf", "28", "-preset", "medium",
                str(mp4),
            ],
            check=True, timeout=180, capture_output=True,
        )
        subprocess.run(
            [
                FFMPEG, "-y", "-i", str(src), "-an", "-vf", vf,
                "-c:v", "libvpx-vp9", "-pix_fmt", "yuv420p",
                "-crf", "32", "-b:v", "0", "-row-mt", "1", "-deadline", "good",
                str(webm),
            ],
            check=True, timeout=240, capture_output=True,
        )
    except Exception:
        mp4.unlink(missing_ok=True)
        webm.unlink(missing_ok=True)
        return None
    if not mp4.is_file() or not webm.is_file():
        return None
    try:
        with tempfile.TemporaryDirectory(prefix="oa-poster-") as tmp:
            poster_png = Path(tmp) / "poster.png"
            subprocess.run(
                [
                    FFMPEG, "-y", "-i", str(src), "-frames:v", "1", "-vf", vf,
                    str(poster_png),
                ],
                check=True, timeout=60, capture_output=True,
            )
            result = _optimize(poster_png, f"{stem}-poster", dest)
        files = _relative_files(dist, result)
        largest = sorted(files, key=lambda f: f["width"])[-1]
        poster = largest.get("webp") or largest.get("avif")
        if not poster:
            raise RuntimeError("poster missing")
        info = _probe_video(mp4)
        return {
            "mp4": f"{DIST_IMAGES}/{mp4.name}",
            "webm": f"{DIST_IMAGES}/{webm.name}",
            "poster": poster,
            "poster_avif": largest.get("avif"),
            "poster_files": files,
            "width": info.get("width") or result.get("width"),
            "height": info.get("height") or result.get("height"),
            "ffmpeg": _ffmpeg_version(),
        }
    except Exception:
        mp4.unlink(missing_ok=True)
        webm.unlink(missing_ok=True)
        return None


def _attach_video(entry: dict, dist: Path, source: Path) -> bool:
    video = _transcode_video(source, dist, entry.get("sha256", "clip")[:16])
    if not video:
        return False
    entry["video"] = {k: v for k, v in video.items() if k != "poster_files"}
    if video.get("width"):
        entry["width"] = video["width"]
    if video.get("height"):
        entry["height"] = video["height"]
    entry["animated"] = True
    # Prefer the still poster in "files" so the huge animated stills can be pruned.
    if video.get("poster_files"):
        entry["files"] = video["poster_files"]
    return True


def _files_exist(dist: Path, entry: dict) -> bool:
    if _video_complete(dist, entry):
        return True
    for variant in entry.get("files") or []:
        for key in ("webp", "avif"):
            rel = variant.get(key)
            if rel and not (dist / rel).is_file():
                return False
        if not variant.get("webp"):
            return False
    return bool(entry.get("files"))


def _fields_from_entry(entry: dict) -> dict:
    files = sorted(entry.get("files") or [], key=lambda f: f["width"])
    sources = []
    url = ""
    srcset = ""
    if files:
        largest = files[-1]
        avif_bits = [f"{'/' + f['avif']} {f['width']}w" for f in files if f.get("avif")]
        webp_bits = [f"{'/' + f['webp']} {f['width']}w" for f in files if f.get("webp")]
        if avif_bits:
            sources.append({"type": "image/avif", "srcset": ", ".join(avif_bits)})
        if webp_bits:
            sources.append({"type": "image/webp", "srcset": ", ".join(webp_bits)})
        url = "/" + (largest.get("webp") or largest.get("avif") or "")
        srcset = ", ".join(webp_bits)
    video = entry.get("video") or {}
    if video.get("poster") and not url:
        url = "/" + video["poster"]
    fields = {
        "url": url,
        "srcset": srcset,
        "sizes": "(max-width: 700px) 100vw, 1200px" if srcset else "",
        "sources": sources,
        "width": (video.get("width") if video else None) or entry.get("width"),
        "height": (video.get("height") if video else None) or entry.get("height"),
        "local": True,
        "animated": bool(entry.get("animated") or video),
    }
    if video.get("mp4") or video.get("webm"):
        if video.get("mp4"):
            fields["mp4"] = "/" + video["mp4"]
        if video.get("webm"):
            fields["webm"] = "/" + video["webm"]
        if video.get("poster"):
            fields["poster"] = "/" + video["poster"]
        if video.get("poster_avif"):
            fields["poster_avif"] = "/" + video["poster_avif"]
    return fields


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


def _ensure_video(entry: dict, dist: Path, data: bytes | None = None, ctype: str = "", src: Path | None = None) -> None:
    if _video_complete(dist, entry):
        return
    if data is not None and src is not None:
        if _wants_video(entry, data=data, ctype=ctype, path=src):
            _attach_video(entry, dist, src)
        return
    if not _wants_video(entry) and not entry.get("animated"):
        return
    # Re-download, or transcode a local animated still if the host is unreachable.
    local = _largest_local_still(dist, entry)
    if local and local.stat().st_size >= VIDEO_MIN_BYTES and entry.get("animated"):
        # Only use the local file when we cannot or do not need a fresh original.
        if _attach_video(entry, dist, local):
            return
    # Caller may pass no data; give up quietly and keep the current image.


def localize_url(url: str, dist: Path, manifest: dict) -> dict | None:
    """Return localized fields, or None to keep the upstream URL."""
    images = manifest.setdefault("images", {})
    existing = images.get(url)

    def reused(entry: dict, data: bytes | None = None, ctype: str = "", src: Path | None = None) -> dict:
        if data is not None and src is not None:
            _ensure_video(entry, dist, data=data, ctype=ctype, src=src)
        elif not _video_complete(dist, entry) and entry.get("animated"):
            # Need the original bytes to transcode. Download, then attach.
            try:
                fresh, fresh_ctype, _etag = _download(url)
                with tempfile.TemporaryDirectory(prefix="oa-shot-src-") as tmp:
                    path = Path(tmp) / "src.bin"
                    path.write_bytes(fresh)
                    _ensure_video(entry, dist, data=fresh, ctype=fresh_ctype, src=path)
            except Exception:
                _ensure_video(entry, dist)
        return _fields_from_entry(entry)

    etag = _head_etag(url)
    if existing and existing.get("etag") and etag and existing["etag"] == etag and _files_exist(dist, existing):
        return reused(existing)
    if existing and not etag and _files_exist(dist, existing):
        try:
            data, ctype, new_etag = _download(url)
        except Exception:
            return reused(existing)
        digest = hashlib.sha256(data).hexdigest()
        if digest == existing.get("sha256"):
            if new_etag and new_etag != existing.get("etag"):
                existing["etag"] = new_etag
            with tempfile.TemporaryDirectory(prefix="oa-shot-src-") as tmp:
                src = Path(tmp) / "src.bin"
                src.write_bytes(data)
                return reused(existing, data=data, ctype=ctype, src=src)
        return _convert(url, dist, manifest, data, ctype, new_etag, digest)
    try:
        data, ctype, new_etag = _download(url)
    except Exception:
        if existing and _files_exist(dist, existing):
            return reused(existing)
        return None
    digest = hashlib.sha256(data).hexdigest()
    if existing and digest == existing.get("sha256") and _files_exist(dist, existing):
        existing["etag"] = new_etag or existing.get("etag")
        with tempfile.TemporaryDirectory(prefix="oa-shot-src-") as tmp:
            src = Path(tmp) / "src.bin"
            src.write_bytes(data)
            return reused(existing, data=data, ctype=ctype, src=src)
    return _convert(url, dist, manifest, data, ctype, new_etag, digest)


def _suffix_for(ctype: str) -> str:
    if "jpeg" in ctype or "jpg" in ctype:
        return ".jpg"
    if "png" in ctype:
        return ".png"
    if "webp" in ctype:
        return ".webp"
    if "gif" in ctype:
        return ".gif"
    if "avif" in ctype:
        return ".avif"
    return ".bin"


def _convert(url: str, dist: Path, manifest: dict, data: bytes, ctype: str, etag: str | None, digest: str) -> dict | None:
    if not data or not _is_raster(ctype, url, data):
        return None
    stem = digest[:16]
    with tempfile.TemporaryDirectory(prefix="oa-shot-src-") as tmp:
        src = Path(tmp) / f"src{_suffix_for(ctype)}"
        src.write_bytes(data)
        result = None
        try:
            result = _optimize(src, stem, dist / DIST_IMAGES)
        except Exception:
            result = None
        files = _relative_files(dist, result) if result else []
        entry = {
            "etag": etag,
            "sha256": digest,
            "content_type": ctype,
            "width": (result or {}).get("width") or 0,
            "height": (result or {}).get("height") or 0,
            "animated": bool((result or {}).get("animated")) or _is_animated_bytes(data, ctype, src),
            "files": files,
        }
        _ensure_video(entry, dist, data=data, ctype=ctype, src=src)
        if not entry.get("files") and not entry.get("video"):
            return None
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
        entry = manifest.get("images", {}).get(url, {})
        for variant in entry.get("files") or []:
            for key in ("webp", "avif"):
                if variant.get(key):
                    keep.add(variant[key])
        for key in ("mp4", "webm", "poster", "poster_avif"):
            rel = (entry.get("video") or {}).get(key)
            if rel:
                keep.add(rel)
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


def gallery_tile(image: dict, *, first: bool = False, alt: str = "") -> str:
    """One gallery item: a video, or a link to the still screenshot."""
    from html import escape
    tag = img_tag(image, first=first, alt=alt)
    if image.get("mp4") or image.get("webm"):
        return f'<div class="shot-wrap">{tag}</div>'
    href = escape(image["url"])
    label = escape(alt or image.get("alt") or "App screenshot")
    return (
        f'<a class="shot-wrap" href="{href}" target="_blank" rel="noopener" '
        f'aria-label="Open full-size {label}">{tag}</a>'
    )


def img_tag(image: dict, *, first: bool = False, alt: str = "") -> str:
    """HTML for one screenshot, with srcset, dimensions, and load hints."""
    from html import escape
    alt = escape(alt or image.get("alt") or "App screenshot")
    if image.get("mp4") or image.get("webm"):
        width = image.get("width")
        height = image.get("height")
        dims = f' width="{int(width)}" height="{int(height)}"' if width and height else ""
        poster = f' poster="{escape(image["poster"])}"' if image.get("poster") else ""
        sources = []
        if image.get("mp4"):
            sources.append(f'<source src="{escape(image["mp4"])}" type="video/mp4">')
        if image.get("webm"):
            sources.append(f'<source src="{escape(image["webm"])}" type="video/webm">')
        return (
            f'<video{dims} autoplay muted loop playsinline preload="metadata"'
            f'{poster} aria-label="{alt}">{"".join(sources)}</video>'
        )
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
