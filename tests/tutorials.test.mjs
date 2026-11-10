import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";

const dist = new URL("../dist/", import.meta.url);
const merged = JSON.parse(await readFile(new URL("../data/merged-pages.json", import.meta.url), "utf8")).redirects;
const sitemap = await readFile(new URL("sitemap.xml", dist), "utf8");
const apps = (await readdir(new URL("apps/", dist))).filter((f) => f.endsWith(".html"));
assert.ok(apps.length > 100, "profiles were built");

// Every profile either links to a live tutorial (or the kept page that tutorial now 301s into),
// or is itself the page those how-tos now 301 into.
for (const file of apps) {
  const page = await readFile(new URL(`apps/${file}`, dist), "utf8");
  const mergedIntoThis = Object.entries(merged).some(([, to]) => to === `/apps/${file}`);
  if (mergedIntoThis) continue;
  const link = page.match(/<a class="button" href="(\/(?:apps\/)?[a-z0-9-]+\.html)">Tutorial:/);
  assert.ok(link, `${file} links to its tutorial`);
  const tutorial = await readFile(new URL(link[1].slice(1), dist), "utf8");
  const canonical = tutorial.match(/<link rel="canonical" href="([^"]+)">/)[1];
  if (link[1].startsWith("/apps/")) {
    // Variant listings (for example t3code-nightly) share the kept package page.
    assert.equal(canonical, `https://omarchyapps.com${link[1]}`, `${link[1]} is self canonical`);
    assert.equal((tutorial.match(/<h1/g) || []).length, 1, `${link[1]} has one h1`);
    continue;
  }
  // A tutorial is either in the sitemap, or it points its canonical at this profile and stays out of it.
  if (canonical === `https://omarchyapps.com/apps/${file}`) {
    assert.doesNotMatch(sitemap, new RegExp(`omarchyapps\\.com${link[1].replace(".", "\\.")}<`), `${link[1]} left out of sitemap`);
  } else if (/<meta name="robots" content="noindex,follow">/.test(tutorial)) {
    // Thin app (data/thin-apps.json): the tutorial is noindexed with its app page and stays out of the sitemap.
    assert.doesNotMatch(sitemap, new RegExp(`omarchyapps\\.com${link[1].replace(".", "\\.")}<`), `${link[1]} noindex, left out of sitemap`);
  } else {
    assert.equal(canonical, `https://omarchyapps.com${link[1]}`, `${link[1]} is self canonical`);
    assert.match(sitemap, new RegExp(`omarchyapps\\.com${link[1].replace(".", "\\.")}`), `${link[1]} in sitemap`);
  }
  assert.equal((tutorial.match(/<h1/g) || []).length, 1, `${link[1]} has one h1`);
  // A variant whose own tutorial was merged (data/merged-pages.json) shares its sibling's page, which links the main profile.
  const mergedAway = Object.values(merged).includes(link[1]) && merged[`/${file.replace(/\.html$/, "")}-on-omarchy.html`];
  const wonMerge = merged[`/apps/${file}`] === link[1];
  if (!mergedAway && !wonMerge) assert.match(tutorial, new RegExp(`href="/apps/${file.replace(".", "\\.")}"`), `${link[1]} links back to its profile`);
}

// Tutorials that won the one-page-per-app merge are self canonical and in the sitemap unless noindex.
for (const [from, to] of Object.entries(merged)) {
  if (!from.startsWith("/apps/") || !to.endsWith("-on-omarchy.html")) continue;
  const tutorial = await readFile(new URL(to.slice(1), dist), "utf8");
  const canonical = tutorial.match(/<link rel="canonical" href="([^"]+)">/)[1];
  if (/<meta name="robots" content="noindex,follow">/.test(tutorial)) {
    assert.doesNotMatch(sitemap, new RegExp(`omarchyapps\\.com${to.replace(".", "\\.")}<`), `${to} noindex, left out of sitemap`);
  } else {
    assert.equal(canonical, `https://omarchyapps.com${to}`, `${to} is self canonical`);
    assert.match(sitemap, new RegExp(`omarchyapps\\.com${to.replace(".", "\\.")}<`), `${to} in sitemap`);
  }
}
console.log("tutorials-tests-ok");
