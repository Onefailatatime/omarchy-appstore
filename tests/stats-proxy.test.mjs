import assert from "node:assert/strict";
import { proxyStats } from "../src/worker.js";

const calls = [];
const fake = async (url, init = {}) => { calls.push({ url, init }); return new Response(url.endsWith("script.js") ? "/*umami*/" : '{"ok":1}', { status: 200, headers: { "content-type": "application/json" } }); };

let r = await proxyStats(new Request("https://omarchyapps.com/stats/script.js"), "/stats/script.js", "https://edge.test/", fake);
assert.equal(r.status, 200);
assert.equal(await r.text(), "/*umami*/");
assert.equal(calls.at(-1).url, "https://edge.test/script.js");

r = await proxyStats(new Request("https://omarchyapps.com/stats/api/send", { method: "POST", body: '{"type":"event"}', headers: { "user-agent": "UA", "x-umami-cache": "tok", "cf-connecting-ip": "203.0.113.9", cookie: "secret=1" } }), "/stats/api/send", "https://edge.test/", fake);
assert.equal(r.status, 200);
const sent = calls.at(-1);
assert.equal(sent.url, "https://edge.test/api/send");
assert.equal(sent.init.body, '{"type":"event"}');
assert.equal(sent.init.headers.get("x-forwarded-for"), "203.0.113.9");
assert.equal(sent.init.headers.get("user-agent"), "UA");
assert.equal(sent.init.headers.get("x-umami-cache"), "tok", "session cache token is forwarded");
assert.equal(sent.init.headers.get("cookie"), null, "cookies are never forwarded");

for (const [path, method] of [["/stats/", "GET"], ["/stats/api/websites", "GET"], ["/stats/api/send", "GET"], ["/stats/script.js", "POST"]]) {
  const n = calls.length;
  r = await proxyStats(new Request("https://omarchyapps.com" + path, { method, body: method === "POST" ? "{}" : undefined }), path, "https://edge.test/", fake);
  assert.equal(r.status, 404, path + " " + method);
  assert.equal(calls.length, n, "nothing else is forwarded");
}
const before = calls.length;
for (const origin of [undefined, ""]) {
  r = await proxyStats(new Request("https://omarchyapps.com/stats/script.js"), "/stats/script.js", origin, fake);
  assert.equal(r.status, 404, "no secret means no proxy");
}
assert.equal(calls.length, before);
console.log("stats-proxy-tests-ok");
