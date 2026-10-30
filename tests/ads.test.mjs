import assert from "node:assert/strict";
import { DatabaseSync } from "node:sqlite";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { handleAdEvent, handleWaitlist, handleStats, pacificDay } from "../src/ads.mjs";

// A tiny D1 stand in on node:sqlite with the real migration.
function fakeD1() {
  const db = new DatabaseSync(":memory:");
  db.exec(readFileSync(new URL("../migrations/0002_inhouse_ads.sql", import.meta.url), "utf8"));
  return {
    raw: db,
    prepare(sql) {
      let args = [];
      const st = {
        bind(...a) { args = a; return st; },
        async run() { const r = db.prepare(sql).run(...args); return { meta: { changes: Number(r.changes) } }; },
        async first() { return db.prepare(sql).get(...args) ?? null; },
        async all() { return { results: db.prepare(sql).all(...args) }; },
      };
      return st;
    },
  };
}

const ORIGIN = "https://omarchyapps.com";
const post = (path, body, headers = {}) => new Request(ORIGIN + path, { method: "POST", headers: { "content-type": "application/json", origin: ORIGIN, ...headers }, body: JSON.stringify(body) });
const sent = [];
const env = { DB: fakeD1(), ADS_STATS_TOKEN: "test-token", ALERT_TO: "owner@example.com", ALERT_FROM: "alerts@example.com", EMAIL: { async send(m) { sent.push(m); return { messageId: "x" }; } } };
const now = new Date("2026-10-29T18:00:00Z");

// Events: impressions and clicks per page type, views on the mini page.
assert.equal((await handleAdEvent(post("/api/ads/event", { ad: 3, type: "impression", page: "app" }), env, now)).status, 204);
assert.equal((await handleAdEvent(post("/api/ads/event", { ad: 3, type: "impression", page: "home" }), env, now)).status, 204);
assert.equal((await handleAdEvent(post("/api/ads/event", { ad: 3, type: "click", page: "home" }), env, now)).status, 204);
assert.equal((await handleAdEvent(post("/api/ads/event", { ad: 3, type: "view", page: "home" }), env, now)).status, 204);
assert.equal((await handleAdEvent(post("/api/ads/event", { ad: 21, type: "click" }), env, now)).status, 400, "only ads 1 to 20");
assert.equal((await handleAdEvent(post("/api/ads/event", { ad: 3, type: "signup" }), env, now)).status, 400, "signups only come from the waitlist");
assert.equal((await handleAdEvent(post("/api/ads/event", { ad: 3, type: "click" }, { origin: "https://evil.test" }), env, now)).status, 403);
// Header and footer slots on every page type keep their own page type.
for (const pt of ["guide_header", "tutorial_footer", "category_header", "other_footer", "app_footer"]) {
  assert.equal((await handleAdEvent(post("/api/ads/event", { ad: 4, type: "impression", page: pt }), env, now)).status, 204);
}
assert.deepEqual(env.DB.raw.prepare("SELECT page_type FROM ad_daily WHERE ad = 4 ORDER BY page_type").all().map((r) => r.page_type),
  ["app_footer", "category_header", "guide_header", "other_footer", "tutorial_footer"]);
const views = env.DB.raw.prepare("SELECT page_type, views FROM ad_daily WHERE views > 0").all();
assert.deepEqual(views.map((r) => ({ ...r })), [{ page_type: "mini", views: 1 }]);
assert.equal(pacificDay(now), "2026-10-29");

// Waitlist: validation, honeypot, first signup alerts once, repeat updates answers.
let r = await handleWaitlist(post("/api/waitlist", { ad: 3, email: "nope", who: "myself" }), env, null, now);
assert.equal(r.status, 400);
r = await handleWaitlist(post("/api/waitlist", { ad: 3, email: "a@b.co" }), env, null, now);
assert.equal(r.status, 400, "myself or company is required");
r = await handleWaitlist(post("/api/waitlist", { ad: 3, email: "bot@b.co", who: "myself", website: "x" }), env, null, now);
assert.equal((await r.json()).status, "joined");
assert.equal(env.DB.raw.prepare("SELECT COUNT(*) n FROM waitlist").get().n, 0, "honeypot stores nothing");
r = await handleWaitlist(post("/api/waitlist", { ad: 3, email: " Dev@Example.com ", who: "company", use_case: "Postgres at work", source: "app" }), env, null, now);
assert.equal((await r.json()).status, "joined");
assert.equal(sent.length, 1);
assert.match(sent[0].subject, /ad 3 Query Deck/);
assert.match(sent[0].text, /Email: dev@example.com/);
assert.match(sent[0].text, /For: My company/);
assert.match(sent[0].text, /Postgres at work/);
assert.equal(sent[0].replyTo, "dev@example.com");
r = await handleWaitlist(post("/api/waitlist", { ad: 3, email: "dev@example.com", who: "myself", use_case: "side project" }), env, null, now);
assert.equal((await r.json()).status, "existing");
assert.equal(sent.length, 1, "no second alert for a repeat");
assert.equal(env.DB.raw.prepare("SELECT who FROM waitlist WHERE email = 'dev@example.com'").get().who, "myself");
// Plain form post (no JS) gets a page, not JSON, with no links.
r = await handleWaitlist(new Request(ORIGIN + "/api/waitlist", { method: "POST", headers: { origin: ORIGIN, "content-type": "application/x-www-form-urlencoded" }, body: "ad=5&email=form%40example.com&who=myself&use_case=dotfiles" }), env, null, now);
const page = await r.text();
assert.match(page, /on the list/);
assert.doesNotMatch(page, /<a\s/);
assert.equal(sent.length, 2);

// Stats need the token and report CTR and signups per ad.
assert.equal((await handleStats(new Request(ORIGIN + "/api/ads/stats"), env, now)).status, 401);
assert.equal((await handleStats(new Request(ORIGIN + "/api/ads/stats", { headers: { authorization: "Bearer wrong" } }), env, now)).status, 401);
r = await handleStats(new Request(ORIGIN + "/api/ads/stats?signups=1", { headers: { authorization: "Bearer test-token" } }), env, now);
const stats = await r.json();
const q = stats.ads.find((a) => a.ad === 3);
assert.equal(stats.ads.length, 20);
assert.deepEqual([q.impressions, q.clicks, q.ctr, q.views, q.signups], [2, 1, 50, 1, 1]);
assert.deepEqual(q.impressions_by_page_type, { app: 1, home: 1 });
assert.equal(stats.top_ideas[0].ad, 3);
assert.equal(stats.signups.length, 2);
assert.equal((await handleStats(new Request(ORIGIN + "/api/ads/stats"), { ...env, ADS_STATS_TOKEN: "" }, now)).status, 401, "no token configured means closed");

// Built site: twenty noindex pages with no way back, house ads only in empty sponsor slots, sitemap clean.
const dist = new URL("../dist/", import.meta.url).pathname;
const sitemap = readFileSync(join(dist, "sitemap.xml"), "utf8");
assert.doesNotMatch(sitemap, /\/ad\d+/);
for (let n = 1; n <= 20; n++) {
  const html = readFileSync(join(dist, `ad${n}.html`), "utf8");
  assert.match(html, /<meta name="robots" content="noindex, nofollow">/, `ad${n} noindex`);
  assert.doesNotMatch(html, /<a[\s>]|<nav|href="(?!\/fonts\/|data:)|https?:\/\/(www\.)?omarchyapps\.com/, `ad${n} has no links`);
  assert.match(html, /Apply to join the waitlist/);
  assert.match(html, /Not affiliated with Omarchy, Omacom or 37signals/);
  assert.match(html, /name="who" value="myself"/);
  assert.doesNotMatch(html.replace(/<style>[\s\S]*?<\/style>|<script[\s\S]*?<\/script>|<[^>]+>/g, " "), /[\u2010-\u2015]|\w-\w| - /, `ad${n} copy has no dashes`);
}
const walk = (d) => readdirSync(d).flatMap((f) => statSync(join(d, f)).isDirectory() ? walk(join(d, f)) : [join(d, f)]);
const pages = walk(dist).filter((f) => f.endsWith(".html") && !/\/ad\d+\.html$/.test(f) && !f.includes("/_preview/"));
// House ads fill the homepage sponsor slots and the app banner, and every
// other page gets a header slot under its title block (never right under the
// top bar) and a footer slot just above the site footer.
const slotsIn = (html) => [...html.matchAll(/data-oa-slot="([a-z]+)" data-oa-pos="([a-z]+)"/g)].map((m) => m[1] + "_" + m[2]);
const TYPES = ["guide", "tutorial", "category", "other"];
let withSlots = 0;
for (const f of pages) {
  const html = readFileSync(f, "utf8");
  const rel = f.slice(dist.length);
  const slots = slotsIn(html);
  assert.equal((html.match(/data-oa-slot=/g) || []).length, slots.length, `well formed slots in ${rel}`);
  assert.doesNotMatch(html, /<header class="topbar">(?:(?!<\/header>)[\s\S])*<\/header>\s*<div class="(oa-house|ad-header)/, `no bar under the top bar in ${rel}`);
  assert.doesNotMatch(html, /data-oa-count="[^3]"/, `three ads per slot in ${rel}`);
  if (slots.length) withSlots++;
  if (rel === "index.html") {
    assert.deepEqual(slots, ["home_header", "home_footer"]);
    assert.match(html, /<div class="ad-header"><div class="oa-house" data-oa-slot="home" data-oa-pos="header" data-oa-class="ad text" data-oa-count="3"><\/div><script src="\/oa-ads.js"><\/script><\/div>/);
    assert.doesNotMatch(html, /href="\/sponsor\.html#(header|footer)"/, "open cards replaced");
    assert.match(html, /<div class="ad-footer"><div class="oa-house" data-oa-slot="home" data-oa-pos="footer" data-oa-class="ad" data-oa-count="3"><\/div><script src="\/oa-ads.js"><\/script><\/div>/, "no Sponsors heading over a house ad, three house ads");
  } else if (rel.startsWith("apps/")) {
    assert.deepEqual(slots, ["app_banner", "app_footer"], rel);
    assert.match(html, /<\/header>\n<div class="ad-app-banner"><div class="oa-house"/);
    assert.match(html, /<\/main>\n+<div class="ad-footer" data-oa-page><div class="oa-house"[^>]*><\/div><script src="\/oa-ads.js"><\/script><\/div>\n<footer class="site">/);
  } else {
    assert.equal(slots.length, 2, `header and footer slot in ${rel}`);
    const [h, ft] = slots;
    assert.ok(TYPES.some((t) => h === t + "_header" && ft === t + "_footer"), `${rel}: ${slots}`);
    assert.match(html, /<\/header>\n<div class="ad-header" data-oa-page><div class="oa-house"[^>]*><\/div><script src="\/oa-ads.js"><\/script><\/div>\n\n*<main class="wrap/, `header slot under the title block in ${rel}`);
    assert.match(html, /<\/main>\n+<div class="ad-footer" data-oa-page><div class="oa-house"[^>]*><\/div><script src="\/oa-ads.js"><\/script><\/div>\n<footer class="site">/, `footer slot above the site footer in ${rel}`);
    assert.doesNotMatch(html, /Sponsors<\/h2><div class="oa-house"/);
  }
}
assert.equal(withSlots, pages.length, "every site page has ad slots");
const js = readFileSync(join(dist, "oa-ads.js"), "utf8");
assert.match(js, /a\.target="_blank";a\.rel="noopener"/);
assert.doesNotMatch(js, /FROM US/i);
assert.match(js, /used\[ad\.r\]/, "no ad repeats on a page");
console.log("ads-tests-ok");
