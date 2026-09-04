import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { readFile } from "node:fs/promises";

const guides = [
  "omarchy-vs-macos-windows-ubuntu",
  "free-notion-alternative-linux-slap-notes",
  "free-video-editor-linux-omarchy",
  "best-apps-for-omarchy",
  "how-to-install-apps-on-omarchy",
];

const sitemap = await readFile(new URL("../dist/sitemap.xml", import.meta.url), "utf8");
const homepage = await readFile(new URL("../dist/index.html", import.meta.url), "utf8");

for (const slug of guides) {
  const page = await readFile(new URL(`../dist/${slug}.html`, import.meta.url), "utf8");
  assert.match(page, /<title>[^<]{25,70}<\/title>/);
  assert.match(page, /<meta name="description" content="[^\"]{80,170}">/);
  assert.match(page, new RegExp(`<link rel="canonical" href="https://omarchyapps\\.com/${slug}\\.html">`));
  assert.match(page, /<h1>.+<\/h1>/);
  assert.match(page, /Short answer/);
  assert.match(page, /"@type":"Article"/);
  assert.match(page, /"@type":"BreadcrumbList"/);
  assert.match(page, /"@type":"FAQPage"/);
  assert.doesNotMatch(page, /__[A-Z][A-Z_]+__/);
  const schema = page.match(/<script type="application\/ld\+json">([^<]+)<\/script>/)?.[1];
  assert.doesNotThrow(() => JSON.parse(schema), `${slug} has invalid JSON-LD`);
  assert.match(sitemap, new RegExp(`https://omarchyapps\\.com/${slug}\\.html`));
  assert.match(homepage, new RegExp(`href="/${slug}\\.html"`));

  const ids = [...page.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]);
  assert.equal(new Set(ids).size, ids.length, `${slug} has duplicate IDs`);

  const internalLinks = [...page.matchAll(/href="(\/[^"?#]*)(?:[?#][^"]*)?"/g)].map((match) => match[1]);
  for (const href of internalLinks) {
    const path = href === "/" ? "index.html" : href.slice(1);
    assert.ok(existsSync(new URL(`../dist/${path}`, import.meta.url)), `${slug} links to missing ${href}`);
  }
}

const notes = await readFile(new URL("../dist/free-notion-alternative-linux-slap-notes.html", import.meta.url), "utf8");
assert.match(notes, /href="https:\/\/slapnotes\.com\/"/);
assert.match(notes, /href="\/apps\/slap-notes-bin\.html"/);

const video = await readFile(new URL("../dist/free-video-editor-linux-omarchy.html", import.meta.url), "utf8");
assert.match(video, /href="\/apps\/omacut\.html"/);
assert.match(video, /not a full replacement|No—and that is its advantage/);

console.log("seo-guide-tests-ok");
