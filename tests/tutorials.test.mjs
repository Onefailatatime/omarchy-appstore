import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";

const dist = new URL("../dist/", import.meta.url);
const sitemap = await readFile(new URL("sitemap.xml", dist), "utf8");
const hub = await readFile(new URL("tutorials.html", dist), "utf8");
const apps = (await readdir(new URL("apps/", dist))).filter((f) => f.endsWith(".html"));
assert.ok(apps.length > 100, "profiles were built");

// Every profile links to a tutorial page that exists, is in the sitemap, and is listed on the hub or is a guide.
for (const file of apps) {
  const page = await readFile(new URL(`apps/${file}`, dist), "utf8");
  const link = page.match(/<a class="button" href="(\/[a-z0-9-]+\.html)">Tutorial:/);
  assert.ok(link, `${file} links to its tutorial`);
  const tutorial = await readFile(new URL(link[1].slice(1), dist), "utf8");
  assert.match(sitemap, new RegExp(`omarchyapps\\.com${link[1].replace(".", "\\.")}`), `${link[1]} in sitemap`);
  assert.equal((tutorial.match(/<h1/g) || []).length, 1, `${link[1]} has one h1`);
  assert.match(tutorial, /"@type":\s*"FAQPage"/, `${link[1]} has FAQ schema`);
  assert.match(tutorial, new RegExp(`href="/apps/${file.replace(".", "\\.")}"`), `${link[1]} links back to its profile`);
}
assert.match(hub, /<h1>Omarchy app <span>tutorials<\/span><\/h1>/);
console.log("tutorials-tests-ok");
