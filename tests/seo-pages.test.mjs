import assert from "node:assert/strict";
import { existsSync, readdirSync } from "node:fs";
import { readFile } from "node:fs/promises";

const dist = new URL("../dist/", import.meta.url);
const read = (p) => readFile(new URL(p, dist), "utf8");
const sitemap = await read("sitemap.xml");
const headers = await read("_headers");
const today = new Date().toISOString().slice(0, 10);

assert.doesNotMatch(headers, /[.]ts[.]net/);
assert.match(headers, /\/style\.\*\.css\n\s+Cache-Control: public, max-age=31536000, immutable/);
const css = readdirSync(dist).filter((f) => /^style\.[0-9a-f]{10}\.css$/.test(f));
assert.equal(css.length, 1, "exactly one hashed stylesheet");

const pages = [];
const walk = (dir, rel = "") => { for (const e of readdirSync(new URL(dir, dist), { withFileTypes: true })) {
  if (e.isDirectory()) walk(dir + e.name + "/", rel + e.name + "/"); else if (e.name.endsWith(".html")) pages.push(rel + e.name);
} };
walk("");
const locs = [...sitemap.matchAll(/<loc>https:\/\/omarchyapps\.com\/([^<]*)<\/loc><lastmod>(\d{4}-\d\d-\d\d)<\/lastmod>/g)];
assert.ok(locs.length > 0);
for (const [, path, date] of locs) {
  assert.ok(date <= today, `${path} lastmod in the future`);
  assert.ok(existsSync(new URL(path || "index.html", dist)), `sitemap lists missing ${path}`);
}
assert.equal(new Set(locs.map((m) => m[1])).size, locs.length, "no duplicate sitemap URLs");

for (const page of pages) {
  // disktree-bin-on-omarchy.html is a stale file committed by a refresh run
  // from an uncommitted draft; build.py does not generate it.
  if (["404.html", "disktree-bin-on-omarchy.html"].includes(page)) continue;
  const html = await read(page);
  assert.doesNotMatch(html, /[.]ts[.]net[:/]/, `${page} references the private host`);
  if (!/<title>/.test(html)) continue;
  assert.doesNotMatch(html, /<style>\s*:root/, `${page} still inlines the shared CSS`);
  assert.match(html, new RegExp(`<link rel="stylesheet" href="/${css[0].replace(".", "\\.")}">`), `${page} misses the stylesheet`);
  assert.match(html, /<script defer src="\/stats\/script\.js" data-website-id="e45b1c4a-5d0b-431c-b50a-88bcc6fe91e9"/, `${page} misses first-party Umami`);
  assert.doesNotMatch(html, /__[A-Z][A-Z_]+__/, `${page} has an unfilled placeholder`);
  for (const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    const data = JSON.parse(m[1]);
    assert.equal(data["@context"], "https://schema.org", page);
  }
}

const apps = pages.filter((p) => p.startsWith("apps/"));
for (const p of apps) {
  const html = await read(p);
  const name = p.slice(5, -5);
  assert.match(html, /<title>Install [^<]+ on Omarchy( \| [^<]+)?<\/title>/, p);
  const ld = JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
  const app = ld["@graph"].find((n) => n["@type"] === "SoftwareApplication");
  for (const k of ["name", "applicationCategory", "operatingSystem", "softwareVersion", "url", "fileSize", "dateModified"]) assert.ok(app[k], `${p} ${k}`);
  assert.equal(app.aggregateRating, undefined, "no invented ratings");
  assert.match(sitemap, new RegExp(`/apps/${name.replace(/[.+]/g, "\\$&")}\\.html`));
}

const cats = pages.filter((p) => p.startsWith("category/"));
assert.equal(cats.length, 12, "12 category pages");
const list = await read("omarchy-apps-list.html");
assert.equal((list.match(/<li><a href="\/apps\//g) || []).length, apps.length, "apps list links every app once");
for (const k of ["ubuntu", "cachyos", "arch", "fedora", "mint", "popos", "bazzite"]) {
  const html = await read(`vs/omarchy-vs-${k}.html`);
  assert.ok((html.match(/class="src"/g) || []).length >= 4, `${k} comparison cites sources`);
}
const installs = pages.filter((p) => p.startsWith("install/"));
assert.ok(installs.length >= 8);
for (const p of installs) assert.match(await read(p), /omarchy\.org\/manual\//, `${p} cites the manual`);
for (const p of [...cats, ...installs, "omarchy-apps-list.html"]) assert.match(sitemap, new RegExp(p.replace(/\./g, "\\.")));

// Internal links on new pages resolve.
for (const p of [...cats, ...installs, "omarchy-apps-list.html", "vs/omarchy-vs-ubuntu.html"]) {
  for (const [, href] of (await read(p)).matchAll(/href="(\/[^"?#]*)/g)) {
    assert.ok(existsSync(new URL((href === "/" ? "index.html" : href.slice(1)), dist)), `${p} links to missing ${href}`);
  }
}
console.log(`seo-pages-tests-ok (${pages.length} html pages, ${locs.length} sitemap urls)`);
