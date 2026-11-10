import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("..", import.meta.url));
const dist = new URL("../dist/", import.meta.url);
const toolDir = join(root, "tools/screenshots");
const fixture = join(root, "tests/fixtures/wide-screenshot.png");
const tmp = mkdtempSync(join(tmpdir(), "oa-shot-"));

const stdout = execFileSync(
  process.execPath,
  [
    join(root, "tools/screenshots/optimize.mjs"),
    "--input", fixture,
    "--out-dir", tmp,
    "--stem", "fixture",
    "--quality", "75",
    "--widths", "1200,600",
  ],
  { encoding: "utf8", cwd: toolDir },
);
const info = JSON.parse(stdout.trim().split("\n").at(-1));
assert.equal(info.width, 1200);
assert.equal(info.height, 800);
assert.equal(info.animated, false);
assert.equal(info.files.length, 2);
assert.ok(existsSync(join(tmp, "fixture-1200.webp")));
assert.ok(existsSync(join(tmp, "fixture-1200.avif")));
assert.ok(existsSync(join(tmp, "fixture-600.webp")));
assert.ok(existsSync(join(tmp, "fixture-600.avif")));
rmSync(tmp, { recursive: true, force: true });

const flea = readFileSync(new URL("apps/flea.html", dist), "utf8");
assert.match(flea, /\/images\/screenshots\/[0-9a-f]+-1200\.webp/, "flea serves a local 1200px webp");
assert.match(flea, /<picture>/, "flea uses a picture element");
assert.match(flea, /type="image\/avif"/, "flea offers AVIF");
assert.match(flea, /srcset="/, "flea has a srcset");
assert.match(flea, /width="\d+" height="\d+"/, "flea images have dimensions");
assert.match(flea, /fetchpriority="high"/, "first flea screenshot is high priority");
assert.ok((flea.match(/loading="lazy"/g) || []).length >= 3, "later flea screenshots are lazy loaded");
assert.doesNotMatch(
  flea.split('fetchpriority="high"')[1].split("</a>")[0],
  /loading="lazy"/,
  "first flea image is not lazy",
);
assert.match(flea, /View upstream source/, "flea keeps upstream attribution");
assert.match(flea, /https:\/\/github\.com\/thisisgm\/flea/, "flea still links the source repo");

const headers = readFileSync(new URL("_headers", dist), "utf8");
assert.match(headers, /\/images\/\*\n\s+Cache-Control: public, max-age=31536000, immutable/);

const details = JSON.parse(readFileSync(new URL("package-details.json", dist), "utf8"));
assert.ok(details.flea?.gallery?.length >= 1, "package details include flea screenshots");
for (const image of details.flea.gallery) {
  assert.match(image.url, /^\/images\/screenshots\//, `${image.url} should be local`);
  assert.ok(image.local);
  assert.ok(image.width && image.height);
}

const sitemap = readFileSync(new URL("sitemap.xml", dist), "utf8");
assert.doesNotMatch(sitemap, /images\/screenshots/, "screenshots stay out of the sitemap");

const crush = readFileSync(new URL("apps/crush-bin.html", dist), "utf8");
assert.equal((crush.match(/<video /g) || []).length, 2, "crush has two looping videos");
assert.match(crush, /autoplay muted loop playsinline preload="metadata"/);
assert.match(crush, /type="video\/mp4"/);
assert.match(crush, /type="video\/webm"/);
assert.match(crush, /poster="\/images\/screenshots\/[^"]+/);
assert.match(crush, /<video width="\d+" height="\d+"/);

const mise = readFileSync(new URL("mise-bin-on-omarchy.html", dist), "utf8");
assert.match(mise, /<video /, "mise demo is a video");
assert.match(mise, /type="video\/webm"/);
assert.match(mise, /type="video\/mp4"/);
assert.doesNotMatch(mise, /raw\.githubusercontent\.com\/jdx\/mise\/main\/docs\/tapes\/demo\.gif/);

assert.doesNotMatch(flea, /<video /, "flea stills stay images");
console.log("screenshots-tests-ok");
