import assert from "node:assert/strict";
import worker from "../src/worker.js";

const env = { ASSETS: { fetch: async () => new Response("asset", { status: 200 }) } };
const go = (u) => worker.fetch(new Request(u, { redirect: "manual" }), env, {});

let r = await go("http://omarchyapps.com/apps/flea.html?x=1");
assert.equal(r.status, 301);
assert.equal(r.headers.get("location"), "https://omarchyapps.com/apps/flea.html?x=1");
r = await go("http://www.omarchyapps.com/sitemap.xml");
assert.equal(r.headers.get("location"), "https://omarchyapps.com/sitemap.xml", "http www goes to https apex in one hop");
r = await go("https://www.omarchyapps.com/");
assert.equal(r.headers.get("location"), "https://omarchyapps.com/");
r = await go("https://omarchyapps.com/index.html");
assert.equal(r.status, 301);
assert.equal(r.headers.get("location"), "https://omarchyapps.com/");
r = await go("https://omarchyapps.com/");
assert.equal(r.status, 200, "the homepage itself is served");
r = await go("http://localhost:8787/apps/flea.html");
assert.equal(r.status, 200, "local dev stays on http");
console.log("canonical-origin-tests-ok");
