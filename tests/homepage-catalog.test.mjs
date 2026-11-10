import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { existsSync } from "node:fs";

const dist = new URL("../dist/", import.meta.url);
const homepage = await readFile(new URL("index.html", dist), "utf8");
const catalog = JSON.parse(await readFile(new URL("home-catalog.json", dist), "utf8"));
const details = JSON.parse(await readFile(new URL("package-details.json", dist), "utf8"));

assert.ok(existsSync(new URL("home.js", dist)), "home.js is copied into dist");
assert.match(homepage, /<script src="\/home.js" defer><\/script>/);
assert.doesNotMatch(homepage, /<script>\s*\(function \(\)/, "catalogue script is no longer inlined");
assert.match(homepage, /rel="preload"[^>]+fonts\/jetbrains-mono-latin-400\.woff2/);
assert.match(homepage, /rel="preload"[^>]+fonts\/geist-latin-wght-normal\.woff2/);
assert.match(homepage, /<script src="\/oa-ads.js" defer><\/script>/);
assert.equal([...homepage.matchAll(/src="\/oa-ads.js"/g)].length, 1, "oa-ads.js appears once");

// Preview HTML only, the rest lives in the cached JSON.
const preview = [...homepage.matchAll(/<section class="group[^"]*" data-cat="([^"]+)" data-preview="(\d+)"/g)];
assert.ok(preview.length > 0, "category groups are present");
let htmlCards = 0;
for (const [block, cat, previewN] of preview) {
  const start = homepage.indexOf(block);
  const slice = homepage.slice(start, homepage.indexOf("</section>", start));
  const count = (slice.match(/<article class="card/g) || []).length;
  htmlCards += count;
  assert.ok(count <= Number(previewN), `${cat} ships ${count} cards, preview is ${previewN}`);
}
const rest = Object.values(catalog.groups || {}).reduce((n, list) => n + list.length, 0);
assert.ok(rest > 0, "home-catalog.json holds the remaining cards");
assert.ok(htmlCards + rest >= 100, "preview plus JSON covers the catalogue");

// Structured data lists new arrivals, not every package.
const ld = homepage.match(/<script type="application\/ld\+json">([^<]+)<\/script>/);
assert.ok(ld, "homepage has JSON-LD");
const graph = JSON.parse(ld[1]);
const list = (graph["@graph"] || []).find((n) => n.mainEntity && n.mainEntity["@type"] === "ItemList");
assert.ok(list, "CollectionPage ItemList is present");
assert.ok(list.mainEntity.numberOfItems >= htmlCards + rest);
assert.ok(list.mainEntity.itemListElement.length < 20, "ItemList is not a full dump of the catalogue");

assert.ok(typeof details === "object");

assert.match(homepage, /rel="preload"[^>]+fonts\/jetbrains-mono-latin-400\.woff2/);
assert.doesNotMatch(homepage, /jetbrains-mono-latin-700/, "Bold is not preloaded or linked");
const cssName = homepage.match(/href="\/(style\.[0-9a-f]{10}\.css)"/)[1];
const css = await readFile(new URL(cssName, dist), "utf8");
assert.match(css, /jetbrains-mono-latin-400\.woff2/);
assert.doesNotMatch(css, /jetbrains-mono-latin-700/, "Bold @font-face is gone");
assert.ok(existsSync(new URL("fonts/jetbrains-mono-latin-400.woff2", dist)));
assert.ok(existsSync(new URL("fonts/geist-latin-wght-normal.woff2", dist)));
assert.ok(!existsSync(new URL("fonts/jetbrains-mono-latin-700.woff2", dist)), "Bold file is not in dist");
console.log(`homepage-catalog-ok (preview ${htmlCards} cards, ${rest} deferred)`);
