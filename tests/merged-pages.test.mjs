import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { readFile, readdir } from "node:fs/promises";
import { mergedTarget } from "../src/worker.js";

const merged = JSON.parse(await readFile(new URL("../data/merged-pages.json", import.meta.url), "utf8")).redirects;
const dist = new URL("../dist/", import.meta.url);

// The worker 301s the .html URL, the clean URL and a trailing slash.
assert.equal(mergedTarget("/helium-browser-bin-on-omarchy.html"), "/helium-on-omarchy.html");
assert.equal(mergedTarget("/helium-browser-bin-on-omarchy"), "/helium-on-omarchy.html");
assert.equal(mergedTarget("/apps/t3code/"), "/apps/t3code-bin.html");
assert.equal(mergedTarget("/helium-on-omarchy.html"), null);

const sitemap = await readFile(new URL("sitemap.xml", dist), "utf8");
const llms = await readFile(new URL("llms.txt", dist), "utf8");
for (const [from, to] of Object.entries(merged)) {
  assert.ok(existsSync(new URL(to.slice(1), dist)), `${from} points at missing ${to}`);
  assert.ok(!merged[to], `${to} is itself merged (no chains)`);
  assert.ok(!existsSync(new URL(from.slice(1), dist)), `${from} is still generated`);
  assert.ok(!sitemap.includes(`https://omarchyapps.com${from}<`), `${from} still in the sitemap`);
  assert.ok(!llms.includes(`https://omarchyapps.com${from})`), `${from} still in llms.txt`);
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
