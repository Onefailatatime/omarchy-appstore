// In house ads: event counters, the waitlist and the stats read endpoint.
// Storage is D1 (tables in migrations/0002_inhouse_ads.sql). Alerts go out
// through the Cloudflare Email Sending binding (env.EMAIL) when configured.
import ADS from "./ad-catalog.mjs";

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
// Plain page types plus the sponsor slots the house ads fill (page_slot).
const PAGE_TYPES = new Set(["home", "app", "category", "tutorial", "guide", "other", "mini", "home_header", "home_footer", "app_banner"]);
const EVENTS = { impression: "impressions", click: "clicks", view: "views" };
const headers = { "cache-control": "no-store", "content-type": "application/json; charset=utf-8", "x-content-type-options": "nosniff" };
const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers });

export function pacificDay(at = new Date()) {
  return new Intl.DateTimeFormat("en-CA", { timeZone: "America/Los_Angeles", year: "numeric", month: "2-digit", day: "2-digit" }).format(at);
}

const adNumber = (v) => { const n = Number(v); return Number.isInteger(n) && ADS[n] ? n : 0; };

function sameSite(request) {
  const url = new URL(request.url);
  const origin = request.headers.get("origin");
  if (origin) return origin === url.origin;
  const ref = request.headers.get("referer");
  return !ref || ref.startsWith(url.origin + "/");
}

async function bump(db, day, ad, pageType, column) {
  await db.prepare(`INSERT INTO ad_daily (day, ad, page_type, ${column}) VALUES (?, ?, ?, 1)
    ON CONFLICT(day, ad, page_type) DO UPDATE SET ${column} = ${column} + 1`).bind(day, ad, pageType).run();
}

async function readBody(request) {
  const type = request.headers.get("content-type") || "";
  if (type.includes("application/x-www-form-urlencoded") || type.includes("multipart/form-data")) {
    return { form: true, data: Object.fromEntries(await request.formData()) };
  }
  const text = await request.text();
  try { return { form: false, data: JSON.parse(text || "{}") }; } catch { return { form: false, data: null }; }
}

export async function handleAdEvent(request, env, now = new Date()) {
  if (request.method !== "POST") return json({ error: "Method not allowed" }, 405);
  if (!sameSite(request)) return json({ error: "Cross site events are not accepted" }, 403);
  const { data } = await readBody(request);
  const ad = adNumber(data && data.ad);
  const column = data && EVENTS[data.type];
  let page = data && typeof data.page === "string" ? data.page : "other";
  if (!PAGE_TYPES.has(page)) page = "other";
  if (data && data.type === "view") page = "mini";
  if (!ad || !column) return json({ error: "Unknown ad or event" }, 400);
  await bump(env.DB, pacificDay(now), ad, page, column);
  return new Response(null, { status: 204, headers: { "cache-control": "no-store" } });
}

const thanksPage = (msg) => new Response(`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>Waitlist</title><style>body{margin:0;background:#1a1b26;color:#c0caf5;font:16px/1.55 system-ui,sans-serif}main{max-width:36rem;margin:0 auto;padding:3rem 1.2rem}</style></head><body><main><p>${msg}</p><p>You can close this tab.</p></main></body></html>`,
  { status: 200, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex, nofollow" } });

function alertText(row) {
  return [
    `New waitlist signup for ad ${row.ad}: ${row.product}`,
    "",
    `Ad number: ${row.ad} (https://omarchyapps.com/ad${row.ad})`,
    `Product: ${row.product}`,
    `Email: ${row.email}`,
    `For: ${row.who === "company" ? "My company" : row.who === "myself" ? "Myself" : "(not given)"}`,
    `What they would use it for: ${row.use_case || "(left blank)"}`,
    `Came from: ${row.source || "(direct)"}`,
    `Time: ${new Date(row.at).toLocaleString("en-US", { timeZone: "America/Los_Angeles" })} PT`,
    "",
    "Reply to this email to answer them directly.",
  ].join("\n");
}

export async function sendAlert(env, row) {
  if (!env.EMAIL || !env.ALERT_TO || !env.ALERT_FROM) return "skipped";
  await env.EMAIL.send({
    from: { email: env.ALERT_FROM, name: "omarchyapps waitlist" },
    to: env.ALERT_TO,
    replyTo: row.email,
    subject: `Waitlist: ad ${row.ad} ${row.product} (${row.email})`,
    text: alertText(row),
  });
  return "sent";
}

export async function handleWaitlist(request, env, ctx, now = new Date()) {
  if (request.method !== "POST") return json({ error: "Method not allowed" }, 405);
  if (!sameSite(request)) return json({ error: "Cross site signup is not allowed" }, 403);
  const { form, data } = await readBody(request);
  if (!data) return json({ error: "Invalid request" }, 400);
  const fail = (error, status = 400) => form ? thanksPage(error + " Please go back and try again.") : json({ error }, status);
  if (data.website) return form ? thanksPage("Thank you.") : json({ status: "joined" });
  const ad = adNumber(data.ad);
  if (!ad) return fail("Unknown product.");
  const email = typeof data.email === "string" ? data.email.trim().toLowerCase() : "";
  if (!EMAIL.test(email) || email.length > 254) return fail("Please enter a valid email address.");
  const who = data.who === "company" ? "company" : data.who === "myself" ? "myself" : "";
  if (!who) return fail("Please choose myself or my company.");
  const row = {
    at: now.toISOString(), ad, product: ADS[ad], email, who,
    use_case: String(data.use_case || "").trim().slice(0, 1000),
    source: String(data.source || "").replace(/[^a-z]/g, "").slice(0, 20),
  };
  const res = await env.DB.prepare(`INSERT INTO waitlist (at, ad, product, email, use_case, who, source) VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(ad, email) DO NOTHING`).bind(row.at, row.ad, row.product, row.email, row.use_case, row.who, row.source).run();
  const isNew = (res.meta && res.meta.changes) > 0;
  if (!isNew) {
    await env.DB.prepare("UPDATE waitlist SET use_case = ?, who = ? WHERE ad = ? AND email = ?").bind(row.use_case, row.who, ad, email).run();
    return form ? thanksPage("You are already on the list. Thank you.") : json({ status: "existing" });
  }
  await bump(env.DB, pacificDay(now), ad, "mini", "signups");
  const alert = sendAlert(env, row).catch((e) => console.error(JSON.stringify({ event: "waitlist_alert_failed", ad, error: String(e && e.message || e) })));
  if (ctx && ctx.waitUntil) ctx.waitUntil(alert); else await alert;
  return form ? thanksPage("Thank you. You are on the list, and we will email you when early access opens.") : json({ status: "joined" });
}

async function authorized(request, env) {
  const token = env.ADS_STATS_TOKEN;
  if (!token) return false;
  const given = (request.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  const enc = new TextEncoder();
  const [a, b] = await Promise.all([crypto.subtle.digest("SHA-256", enc.encode(given)), crypto.subtle.digest("SHA-256", enc.encode(token))]);
  const x = new Uint8Array(a), y = new Uint8Array(b);
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x[i] ^ y[i];
  return diff === 0;
}

// GET /api/ads/stats?from=YYYY-MM-DD&to=YYYY-MM-DD (Pacific days, both inclusive; default today)
//   or ?days=N (last N Pacific days including today) or ?all=1
export async function handleStats(request, env, now = new Date()) {
  if (request.method !== "GET") return json({ error: "Method not allowed" }, 405);
  if (!(await authorized(request, env))) return json({ error: "Unauthorized" }, 401);
  const q = new URL(request.url).searchParams;
  const day = /^\d{4}-\d\d-\d\d$/;
  let from = pacificDay(now), to = from;
  if (q.get("all")) from = "0000-00-00";
  else if (q.get("days")) {
    const n = Math.max(1, Math.min(366, parseInt(q.get("days"), 10) || 1));
    from = pacificDay(new Date(now.getTime() - (n - 1) * 86400e3));
  }
  if (day.test(q.get("from") || "")) from = q.get("from");
  if (day.test(q.get("to") || "")) to = q.get("to");
  const rows = (await env.DB.prepare(`SELECT ad, page_type, SUM(impressions) i, SUM(clicks) c, SUM(views) v, SUM(signups) s
    FROM ad_daily WHERE day BETWEEN ? AND ? GROUP BY ad, page_type`).bind(from, to).all()).results || [];
  const per = {};
  for (const [n, name] of Object.entries(ADS)) per[n] = { ad: Number(n), name, url: `https://omarchyapps.com/ad${n}`, impressions: 0, clicks: 0, ctr: 0, views: 0, signups: 0, signup_rate: 0, impressions_by_page_type: {} };
  for (const r of rows) {
    const p = per[r.ad];
    if (!p) continue;
    p.impressions += r.i; p.clicks += r.c; p.views += r.v; p.signups += r.s;
    if (r.i) p.impressions_by_page_type[r.page_type] = (p.impressions_by_page_type[r.page_type] || 0) + r.i;
  }
  const ads = Object.values(per).map((p) => ({ ...p, ctr: p.impressions ? +(p.clicks / p.impressions * 100).toFixed(2) : 0, signup_rate: p.views ? +(p.signups / p.views * 100).toFixed(2) : 0 }));
  const totals = ads.reduce((t, p) => ({ impressions: t.impressions + p.impressions, clicks: t.clicks + p.clicks, views: t.views + p.views, signups: t.signups + p.signups }), { impressions: 0, clicks: 0, views: 0, signups: 0 });
  totals.ctr = totals.impressions ? +(totals.clicks / totals.impressions * 100).toFixed(2) : 0;
  const top = [...ads].sort((a, b) => b.signups - a.signups || b.clicks - a.clicks || b.ctr - a.ctr || a.ad - b.ad).slice(0, 5).map(({ ad, name, signups, clicks, ctr, views }) => ({ ad, name, signups, clicks, ctr, views }));
  let signups = [];
  if (q.get("signups") === "1") {
    signups = (await env.DB.prepare(`SELECT at, ad, product, email, who, use_case, source FROM waitlist WHERE substr(at, 1, 10) >= ? ORDER BY at DESC LIMIT 500`).bind(from === "0000-00-00" ? from : from).all()).results || [];
  }
  return json({ timezone: "America/Los_Angeles", from: from === "0000-00-00" ? "all" : from, to, totals, top_ideas: top, ads, ...(q.get("signups") === "1" ? { signups } : {}) });
}
