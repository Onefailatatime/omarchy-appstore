import assert from "node:assert/strict";
import { existsSync, readdirSync } from "node:fs";
import { readFile } from "node:fs/promises";

const dist = new URL("../dist/", import.meta.url);
const read = (p) => readFile(new URL(p, dist), "utf8");
const sitemap = await read("sitemap.xml");
const headers = await read("_headers");
const today = new Date().toISOString().slice(0, 10);
const thinApps = new Set(JSON.parse(await readFile(new URL("../data/thin-apps.json", import.meta.url), "utf8")).apps);

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
  // /ad1 to /ad20 are standalone noindex waitlist pages (tests/ads.test.mjs).
  if (/^ad\d+\.html$/.test(page)) continue;
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

const appExtras = JSON.parse(await readFile(new URL("../data/app-extras.json", import.meta.url), "utf8"));
const apps = pages.filter((p) => p.startsWith("apps/"));
for (const p of apps) {
  const html = await read(p);
  const name = p.slice(5, -5);
  // data/app-extras.json gives a few hand written app pages their own title and an FAQ.
  if (appExtras[name]) {
    assert.ok(html.includes(`<title>${appExtras[name].title}</title>`), p);
    assert.match(html, /"@type":"FAQPage"/, `${p} FAQ schema`);
  } else assert.match(html, /<title>Install [^<]+ on Omarchy( \| [^<]+)?<\/title>/, p);
  const ld = JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
  const app = ld["@graph"].find((n) => n["@type"] === "SoftwareApplication");
  for (const k of ["name", "applicationCategory", "operatingSystem", "softwareVersion", "url", "fileSize", "dateModified"]) assert.ok(app[k], `${p} ${k}`);
  assert.equal(app.aggregateRating, undefined, "no invented ratings");
  const inSitemap = new RegExp(`/apps/${name.replace(/[.+]/g, "\\$&")}\\.html<`);
  // data/thin-apps.json: thin app pages are noindex, follow and stay out of the sitemap.
  if (thinApps.has(name)) {
    assert.match(html, /<meta name="robots" content="noindex,follow">/, `${p} noindex`);
    assert.doesNotMatch(sitemap, inSitemap, `${p} not in sitemap`);
  } else {
    assert.match(html, /<meta name="robots" content="index,follow/, `${p} indexable`);
    assert.match(sitemap, inSitemap);
  }
}
for (const keep of ["flea", "strata", "slap-notes-bin", "omarchy-task-manager"]) assert.ok(!thinApps.has(keep), `${keep} stays indexed`);

const mergedRedirects = JSON.parse(await readFile(new URL("../data/merged-pages.json", import.meta.url), "utf8")).redirects;
const liveOf = (path) => {
  let cur = path;
  const seen = new Set();
  while (mergedRedirects[cur] && !seen.has(cur)) { seen.add(cur); cur = mergedRedirects[cur]; }
  return cur;
};
for (const name of thinApps) {
  const appPath = `/apps/${name}.html`;
  const live = liveOf(appPath);
  if (live !== appPath) {
    const file = live.slice(1);
    assert.ok(existsSync(new URL(file, dist)), `${name} live page ${live} missing`);
    const html = await read(file);
    assert.match(html, /<meta name="robots" content="noindex,follow">/, `${live} noindex`);
    assert.doesNotMatch(sitemap, new RegExp(live.replace(/[.+]/g, "\\$&") + "<"), `${live} not in sitemap`);
  }
}

// No build time freshness: no footer sync stamp and no review stamp on generated pages.
for (const p of pages) {
  const html = await read(p);
  assert.doesNotMatch(html, /<span>Synced \d{4}/, `${p} footer stamp`);
  if (p.startsWith("category/") || p.startsWith("vs/") || p.startsWith("install/")) assert.doesNotMatch(html, /Reviewed \d{4}/, `${p} review stamp`);
}

const cats = pages.filter((p) => p.startsWith("category/"));
assert.equal(cats.length, 12, "12 category pages");
for (const p of cats) {
  const html = await read(p);
  assert.ok(html.includes("<p>") || html.includes("<p "), `${p} has an intro`);
}
assert.ok(!existsSync(new URL("omarchy-apps-list.html", dist)), "apps list is merged into /");
const compared = await read("vs/omarchy-compared.html");
assert.ok((compared.match(/class="src"/g) || []).length >= 4, "comparison hub cites sources");
assert.doesNotMatch(compared, /<!-- (TABLE|FAQ) -->/, "comparison hub filled its slots");
const cachy = await read("vs/omarchy-vs-cachyos.html");
assert.match(cachy, /<title>Omarchy vs CachyOS \(2026\): Which Arch Distro Fits You\?<\/title>/);
assert.match(cachy, /"@type":"FAQPage"/, "cachyos comparison has FAQ schema");
assert.doesNotMatch(cachy, /<!-- (TABLE|FAQ) -->/, "cachyos comparison filled its slots");
const installs = pages.filter((p) => p.startsWith("install/"));
assert.ok(installs.length >= 8);
assert.ok(installs.includes("install/gaming-on-omarchy.html"), "gaming install hub exists");
assert.ok(!existsSync(new URL("install/lutris-on-omarchy.html", dist)));
assert.ok(!existsSync(new URL("install/heroic-epic-games-on-omarchy.html", dist)));
for (const p of installs) assert.match(await read(p), /omarchy\.org\/manual\//, `${p} cites the manual`);
for (const p of [...cats, ...installs, "vs/omarchy-compared.html", "vs/omarchy-vs-cachyos.html"]) {
  assert.match(sitemap, new RegExp(p.replace(/\./g, "\\.")));
}

assert.match(await read("catalog.html"), /<meta name="robots" content="noindex,follow">/, "catalog is noindex");
assert.doesNotMatch(sitemap, /catalog\.html</, "catalog is out of the sitemap");

// Sitemap URLs are indexable.
for (const [, path] of locs) {
  const file = path || "index.html";
  const html = await read(file);
  assert.doesNotMatch(html, /<meta name="robots" content="noindex/, `sitemap ${file} is noindex`);
}

// Internal links on new pages resolve.
for (const p of [...cats, ...installs, "vs/omarchy-compared.html", "vs/omarchy-vs-cachyos.html"]) {
  for (const [, href] of (await read(p)).matchAll(/href="(\/[^"?#]*)/g)) {
    assert.ok(existsSync(new URL((href === "/" ? "index.html" : href.slice(1)), dist)), `${p} links to missing ${href}`);
  }
}
console.log(`seo-pages-tests-ok (${pages.length} html pages, ${locs.length} sitemap urls)`);
