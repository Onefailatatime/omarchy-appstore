import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { readFile, readdir } from "node:fs/promises";
import { mergedTarget, goneTarget } from "../src/worker.js";

const merged = JSON.parse(await readFile(new URL("../data/merged-pages.json", import.meta.url), "utf8")).redirects;
const dist = new URL("../dist/", import.meta.url);

// The worker 301s the .html URL, the clean URL and a trailing slash.
assert.equal(mergedTarget("/helium-browser-bin-on-omarchy.html"), "/helium-on-omarchy.html");
assert.equal(mergedTarget("/helium-browser-bin-on-omarchy"), "/helium-on-omarchy.html");
assert.equal(mergedTarget("/apps/t3code/"), "/apps/t3code-bin.html");
assert.equal(mergedTarget("/helium-on-omarchy.html"), null);
assert.equal(mergedTarget("/apps/elephant.html"), "/walker-on-omarchy.html");
assert.equal(mergedTarget("/apps/elephant-all"), "/walker-on-omarchy.html");
assert.equal(mergedTarget("/apps/omarchy-walker.html"), "/walker-on-omarchy.html");
assert.equal(mergedTarget("/apps/t3code-patched-bin.html"), "/apps/t3code-bin.html");
assert.equal(mergedTarget("/t3code-nightly-bin-on-omarchy.html"), "/apps/t3code-nightly-bin.html");
assert.equal(mergedTarget("/apps/linux-ptl-headers.html"), null);
assert.equal(mergedTarget("/store.html"), "/");
assert.equal(mergedTarget("/omarchy-store.html"), "/");
assert.equal(mergedTarget("/omarchy-apps-list.html"), "/");
assert.equal(mergedTarget("/tutorials.html"), "/guides.html");
assert.equal(mergedTarget("/advertise.html"), "/sponsor.html");
assert.equal(mergedTarget("/linux-firmware-cirrus-on-omarchy.html"), "/linux-firmware-cirrus-dx13260-on-omarchy.html");
assert.equal(mergedTarget("/apps/linux-firmware-cirrus.html"), "/linux-firmware-cirrus-dx13260-on-omarchy.html");
assert.equal(mergedTarget("/vs/omarchy-vs-ubuntu.html"), "/vs/omarchy-compared.html");
assert.equal(mergedTarget("/install/lutris-on-omarchy.html"), "/install/gaming-on-omarchy.html");
assert.equal(mergedTarget("/install/heroic-epic-games-on-omarchy.html"), "/install/gaming-on-omarchy.html");
assert.equal(goneTarget("/apps/opencode.html"), true);
assert.equal(goneTarget("/opencode-on-omarchy"), true);
assert.equal(goneTarget("/linux-ptl-headers.html"), true);
assert.equal(goneTarget("/apps/linux-ptl-headers.html"), true);
assert.equal(goneTarget("/helium-on-omarchy.html"), false);


const sitemap = await readFile(new URL("sitemap.xml", dist), "utf8");
const llms = await readFile(new URL("llms.txt", dist), "utf8");
for (const [from, to] of Object.entries(merged)) {
  assert.ok(existsSync(new URL(to.slice(1), dist)), `${from} points at missing ${to}`);
  assert.ok(!merged[to], `${to} is itself merged (no chains)`);
  assert.ok(!existsSync(new URL(from.slice(1), dist)), `${from} is still generated`);
  assert.ok(!sitemap.includes(`https://omarchyapps.com${from}<`), `${from} still in the sitemap`);
  assert.ok(!llms.includes(`https://omarchyapps.com${from})`), `${from} still in llms.txt`);
}

const gone = new Set(JSON.parse(await readFile(new URL("../data/gone-pages.json", import.meta.url), "utf8")).pages);
for (const path of gone) {
  assert.ok(!existsSync(new URL(path.slice(1), dist)), `${path} is still generated`);
  assert.ok(!merged[path], `${path} is also a merge source (would 301 to a 410)`);
  assert.ok(!Object.values(merged).includes(path), `${path} is a merge target (would 301 to a 410)`);
  assert.ok(!sitemap.includes(`https://omarchyapps.com${path}<`), `${path} still in the sitemap`);
}

// No built page links to a merged URL.
const files = (await readdir(dist, { recursive: true })).filter((f) => f.endsWith(".html"));
const sources = new Set(Object.keys(merged));
for (const f of files) {
  const html = await readFile(new URL(f, dist), "utf8");
  for (const [, href] of html.matchAll(/href="(?:https:\/\/omarchyapps\.com)?(\/[^"?#]*)/g)) {
    assert.ok(!sources.has(href), `${f} links to merged ${href}`);
  }
}
console.log(`merged-pages-tests-ok (${sources.size} merged URLs)`);
