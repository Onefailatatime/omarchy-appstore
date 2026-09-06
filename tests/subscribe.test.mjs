import assert from "node:assert/strict";
import { handleSubscribeRequest } from "../netlify/functions/subscribe.mjs";
import checklist from "../netlify/functions/checklist.mjs";

const url = "https://omarchyapps.com/api/subscribe";
const env = { RESEND_API_KEY: "re_test", RESEND_AUDIENCE_ID: "aud_1", NEWSLETTER_FROM: "Omarchy App Store <hello@omarchyapps.com>" };

function fakeResend(existing) {
  const calls = [];
  const fetchImpl = async (target, init) => {
    calls.push({ url: target, method: init.method, body: init.body ? JSON.parse(init.body) : undefined, auth: init.headers.authorization });
    if (init.method === "GET") {
      return existing
        ? Response.json({ id: "c1", email: "dev@example.com", unsubscribed: false })
        : Response.json({ name: "not_found", message: "Contact not found" }, { status: 404 });
    }
    return Response.json({ id: "ok" });
  };
  return { calls, fetchImpl };
}

function post(body, headers = {}) {
  return new Request(url, {
    method: "POST",
    headers: { "content-type": "application/json", origin: "https://omarchyapps.com", ...headers },
    body: JSON.stringify(body),
  });
}

// New subscriber: contact created, checklist emailed as an attachment.
let { calls, fetchImpl } = fakeResend(false);
let res = await handleSubscribeRequest(post({ email: " Dev@Example.com " }), env, fetchImpl);
assert.equal(res.status, 200);
assert.deepEqual(await res.json(), { status: "subscribed" });
assert.deepEqual(calls.map((c) => c.method + " " + c.url), [
  "GET https://api.resend.com/audiences/aud_1/contacts/dev%40example.com",
  "POST https://api.resend.com/audiences/aud_1/contacts",
  "POST https://api.resend.com/emails",
]);
assert.equal(calls[0].auth, "Bearer re_test");
assert.deepEqual(calls[1].body, { email: "dev@example.com", unsubscribed: false });
const mail = calls[2].body;
assert.equal(mail.from, env.NEWSLETTER_FROM);
assert.deepEqual(mail.to, ["dev@example.com"]);
assert.equal(mail.attachments[0].filename, "develop-for-omarchy.md");
assert.equal(Buffer.from(mail.attachments[0].content, "base64").toString("utf8"), checklist);
assert.match(mail.text, /develop\.html/);

// Already subscribed: no duplicate contact, no second email.
({ calls, fetchImpl } = fakeResend(true));
res = await handleSubscribeRequest(post({ email: "dev@example.com" }), env, fetchImpl);
assert.deepEqual(await res.json(), { status: "existing" });
assert.equal(calls.length, 1);

// Honeypot filled: pretend success, call nothing.
({ calls, fetchImpl } = fakeResend(false));
res = await handleSubscribeRequest(post({ email: "bot@example.com", website: "http://spam" }), env, fetchImpl);
assert.equal(res.status, 200);
assert.equal(calls.length, 0);

// Bad input and bad origin.
res = await handleSubscribeRequest(post({ email: "not-an-email" }), env, fetchImpl);
assert.equal(res.status, 400);
res = await handleSubscribeRequest(post({ email: "dev@example.com" }, { origin: "https://evil.example" }), env, fetchImpl);
assert.equal(res.status, 403);
res = await handleSubscribeRequest(new Request(url, { method: "GET" }), env, fetchImpl);
assert.equal(res.status, 405);

// Unconfigured deployment fails clearly instead of calling Resend.
res = await handleSubscribeRequest(post({ email: "dev@example.com" }), {}, fetchImpl);
assert.equal(res.status, 500);
assert.equal(calls.length, 0);

// Resend rejecting the contact surfaces as a retryable error.
res = await handleSubscribeRequest(post({ email: "dev@example.com" }), env, async (target, init) =>
  init.method === "GET" ? Response.json({}, { status: 404 }) : Response.json({ name: "validation_error" }, { status: 422 }));
assert.equal(res.status, 502);

console.log("subscribe: ok");
