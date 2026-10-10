import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { slotConfig } from "../worker/src/auction.js";
import { verifyEmail, outbidEmail, wonEmail, sendMail, mailConfigured } from "../worker/src/mail.js";
import { notifyAdmin } from "../worker/src/notify.js";

const ads = JSON.parse(readFileSync(new URL("../data/ads.json", import.meta.url), "utf8"));
const lifetime = slotConfig(ads, "lifetime");
const footer = slotConfig(ads, "footer");
const bid = { email: "b@example.com", amount: 40, name: "Beta", url: "https://beta.example.com" };
const messages = [
  verifyEmail({ siteUrl: "https://omarchyapps.com", link: "https://x/verify?t=1", cfg: lifetime, amount: 1000, name: "Alpha", to: "a@example.com" }),
  outbidEmail({ siteUrl: "https://omarchyapps.com", cfg: footer, bid, minimum: 45, closesAt: "2026-11-09T12:00:00.000Z" }),
  wonEmail({ siteUrl: "https://omarchyapps.com", cfg: footer, bid, charge: 120 }),
];
for (const m of messages) {
  assert.ok(m.subject && m.text && m.to.length === 1);
  // House rule: nothing a reader sees carries AI dashes.
  assert.doesNotMatch(m.subject + m.text, /[–—]|--/);
}
assert.match(messages[1].text, /\$45 per month/);
assert.match(messages[2].text, /\$120/);

// Unconfigured providers skip quietly; configured ones post the right shape.
assert.equal(mailConfigured({}), false);
assert.deepEqual(await sendMail({}, messages[0]), { ok: false, skipped: true });
let seen;
const fakeFetch = async (url, init) => { seen = { url, body: JSON.parse(init.body), auth: init.headers.authorization }; return { ok: true, status: 200 }; };
await sendMail({ RESEND_API_KEY: "re_test", MAIL_FROM: "Omarchy Apps <hello@omarchyapps.com>" }, messages[0], fakeFetch);
assert.equal(seen.url, "https://api.resend.com/emails");
assert.equal(seen.auth, "Bearer re_test");
assert.equal(seen.body.from, "Omarchy Apps <hello@omarchyapps.com>");
assert.deepEqual(seen.body.to, ["a@example.com"]);
assert.deepEqual(await notifyAdmin({}, "x"), { ok: false, skipped: true });
await notifyAdmin({ TELEGRAM_BOT_TOKEN: "t", TELEGRAM_CHAT_ID: "7" }, "hello", fakeFetch);
assert.equal(seen.url, "https://api.telegram.org/bott/sendMessage");
assert.equal(seen.body.chat_id, "7");
console.log("auction-mail-tests-ok");
