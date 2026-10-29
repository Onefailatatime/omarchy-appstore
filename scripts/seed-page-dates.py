#!/usr/bin/env python3
"""One-time seed for data/page-dates.json.

For every page in dist/, walk its git history and find the most recent commit
where the page changed in something other than a date string or the hashed
stylesheet name. That commit date is the page's real last change. build.py
adopts these dates on its next run and records each page's content hash.
"""
import json, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATES = re.compile(rb"\d{4}-\d{2}-\d{2}")
CSS = re.compile(rb"/style\.[0-9a-f]{10}\.css")


def norm(b: bytes) -> bytes:
    return CSS.sub(b"/style.css", DATES.sub(b"D", b))


def git(*a: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, check=True).stdout


def main() -> None:
    out = {}
    files = sorted(p.relative_to(ROOT / "dist").as_posix() for p in (ROOT / "dist").rglob("*.html"))
    cat = subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def show(rev: str, path: str):
        cat.stdin.write(f"{rev}:{path}\n".encode()); cat.stdin.flush()
        head = cat.stdout.readline().split()
        if len(head) < 3 or head[1] != b"blob":
            return None
        data = cat.stdout.read(int(head[2])); cat.stdout.readline()
        return data

    for rel in files:
        path = f"dist/{rel}"
        log = [l.split() for l in git("log", "--format=%H %cs", "--", path).splitlines()]
        if not log:
            continue
        date = log[-1][1]  # first commit that added the page
        for (h, d), (ph, _) in zip(log, log[1:]):
            cur, prev = show(h, path), show(ph, path)
            if cur is None or prev is None or norm(cur) != norm(prev):
                date = d
                break
        out[rel] = {"date": date}
    cat.stdin.close(); cat.wait()
    (ROOT / "data" / "page-dates.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"seeded {len(out)} pages")


if __name__ == "__main__":
    main()
