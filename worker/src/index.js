// Sponsor slot auction for omarchyapps.com. Public: GET /api/state, POST
// /api/bid, GET /api/bid/verify. Admin: /admin and /api/admin/*. A cron closes
// rounds whose clock has run out.

import { SLOT_IDS, publicState, validateAmount, minimumBid, money } from "./auction.js";
import { mailConfigured, sendMail, verifyEmail } from "./mail.js";
import { notifyAdmin } from "./notify.js";
import { loadSlot, sponsorsFor, rateLimited, approveBid, closeDueSlots, logEvent, now } from "./store.js";
import { handleAdminApi, adminPage } from "./admin.js";

const JSON_HEADERS = { "cache-control": "no-store", "content-type": "application/json; charset=utf-8", "x-content-type-options": "nosniff" };
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function json(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), { status, headers: { ...JSON_HEADERS, ...extra } });
}

function allowedOrigin(request, env) {
  const origin = request.headers.get("origin");
  const allowed = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  return origin && allowed.includes(origin) ? origin : null;
}

function cors(origin) {
  return origin ? { "access-control-allow-origin": origin, vary: "origin" } : {};
}

async function sha256Hex(text) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function randomToken() {
  const bytes = crypto.getRandomValues(new Uint8Array(32));
  return btoa(String.fromCharCode(...bytes)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function cleanText(value, max) {
  return typeof value === "string" ? value.replace(/\s+/g, " ").trim().slice(0, max) : "";
}

function cleanUrl(value) {
  try {
    const url = new URL(String(value || "").trim());
    return ["http:", "https:"].includes(url.protocol) && url.hostname.includes(".") ? url.href.slice(0, 200) : "";
  } catch {
    return "";
  }
}

async function stateResponse(env) {
  const at = now();
  const slots = {};
  for (const id of SLOT_IDS) {
    const { cfg, state, st } = await loadSlot(env, id);
    slots[id] = { ...publicState(cfg, state, st, at), sponsors: await sponsorsFor(env, cfg) };
  }
  return json({ generated_at: at, mode: mailConfigured(env) ? "email" : "review", slots }, 200, {
    "cache-control": "public, max-age=30",
    "access-control-allow-origin": "*",
  });
}

async function submitBid(request, env, ctx) {
  const origin = allowedOrigin(request, env);
  if (!origin) return json({ error: "Bids are accepted from omarchyapps.com only." }, 403);
  const headers = cors(origin);
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "Invalid JSON" }, 400, headers);
  }
  // Honeypot: real visitors never fill "website".
  if (body.website) return json({ ok: true, state: "review" }, 200, headers);

  const at = now();
  const loaded = await loadSlot(env, String(body.slot || ""));
  if (!loaded) return json({ error: "Unknown slot" }, 400, headers);
  const { cfg, state, st } = loaded;
  if (state.status === "closed") return json({ error: "Bidding on this slot has closed." }, 409, headers);

  const name = cleanText(body.name, 60);
  const tagline = cleanText(body.tagline, 90);
  const url = cleanUrl(body.url);
  const email = cleanText(body.email, 254).toLowerCase();
  const amount = Number(body.amount);
  if (name.length < 2) return json({ error: "Enter the product name." }, 400, headers);
  if (!url) return json({ error: "Enter a full link starting with https://." }, 400, headers);
  if (!tagline) return json({ error: "Enter a one line tagline." }, 400, headers);
  if (!EMAIL.test(email)) return json({ error: "Enter a valid email address." }, 400, headers);
  if (body.agree !== true) return json({ error: "Please agree to the bidding terms." }, 400, headers);
  const problem = validateAmount(cfg, st, amount);
  if (problem) return json({ error: problem, minimum_bid: minimumBid(cfg, st) }, 400, headers);

  const ip = request.headers.get("cf-connecting-ip") || "0.0.0.0";
  const ipHash = (await sha256Hex(`${ip}|${env.IP_SALT || ""}`)).slice(0, 32);
  if (await rateLimited(env.DB, `ip:${ipHash}`, 5, 3600e3, at) || await rateLimited(env.DB, `email:${email}`, 10, 86400e3, at)) {
    return json({ error: "Too many bids from here for now. Try again in an hour." }, 429, headers);
  }

  const id = crypto.randomUUID();
  const mail = mailConfigured(env);
  const token = mail ? randomToken() : null;
  const verifyHash = token ? await sha256Hex(token) : null;
  await env.DB.batch([
    env.DB.prepare(
      "INSERT INTO bids (id, slot, cycle, amount, status, created_at, name, url, tagline, email, ip_hash, verify_hash) VALUES (?, ?, ?, ?, 'submitted', ?, ?, ?, ?, ?, ?, ?)",
    ).bind(id, cfg.id, state.cycle, amount, at, name, url, tagline, email, ipHash, verifyHash),
    logEvent(env, at, cfg.id, id, "submitted", `${money(amount)} ${name}`),
  ]);

  const workerOrigin = new URL(request.url).origin;
  if (mail) {
    const link = `${workerOrigin}/api/bid/verify?t=${token}`;
    ctx.waitUntil(sendMail(env, verifyEmail({ siteUrl: env.SITE_URL, link, cfg, amount, name, to: email })));
  }
  const per = cfg.perMonth ? " per month" : "";
  ctx.waitUntil(notifyAdmin(env, `New bid on the ${cfg.label.toLowerCase()} slot: ${money(amount)}${per} from ${name} (${email}). ${mail ? "Awaiting their email confirmation." : `Approve it at ${workerOrigin}/admin`}`));
  console.log(JSON.stringify({ event: "bid_submitted", slot: cfg.id, amount, mode: mail ? "email" : "review" }));
  return json({ ok: true, state: mail ? "verify" : "review", bid_id: id }, 200, headers);
}

async function verifyBid(request, env) {
  const token = new URL(request.url).searchParams.get("t") || "";
  const back = (result, slot = "") => Response.redirect(`${env.SITE_URL}/advertise.html?bid=${result}${slot ? `#${slot}` : ""}`, 302);
  if (!/^[A-Za-z0-9_-]{20,64}$/.test(token)) return back("invalid");
  const bid = await env.DB.prepare("SELECT * FROM bids WHERE verify_hash = ?").bind(await sha256Hex(token)).first();
  if (!bid) return back("invalid");
  if (bid.status !== "submitted") return back("already", bid.slot);
  const at = now();
  await env.DB.batch([
    env.DB.prepare("UPDATE bids SET status = 'verified', verified_at = ? WHERE id = ?").bind(at, bid.id),
    logEvent(env, at, bid.slot, bid.id, "verified", ""),
  ]);
  if (env.AUTO_APPROVE === "1") {
    const result = await approveBid(env, bid.id, at);
    if (!result.ok) console.error(JSON.stringify({ event: "auto_approve_failed", bid: bid.id, error: result.error }));
  }
  return back("verified", bid.slot);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    try {
      if (request.method === "OPTIONS" && path.startsWith("/api/")) {
        const origin = allowedOrigin(request, env);
        return new Response(null, {
          status: 204,
          headers: { ...cors(origin), "access-control-allow-methods": "GET, POST, OPTIONS", "access-control-allow-headers": "content-type", "access-control-max-age": "86400" },
        });
      }
      if (path === "/api/state" && request.method === "GET") return await stateResponse(env);
      if (path === "/api/bid" && request.method === "POST") return await submitBid(request, env, ctx);
      if (path === "/api/bid/verify" && request.method === "GET") return await verifyBid(request, env);
      if (path.startsWith("/api/admin/")) return await handleAdminApi(request, env, path);
      if (path === "/admin") return adminPage();
      if (path === "/healthz") return new Response("ok", { headers: { "cache-control": "no-store" } });
      if (path === "/") return Response.redirect(`${env.SITE_URL}/advertise.html`, 302);
      return json({ error: "Not found" }, 404);
    } catch (error) {
      console.error(JSON.stringify({ event: "request_failed", path, error: String(error && error.stack || error) }));
      return json({ error: "The auction is temporarily unavailable." }, 500);
    }
  },

  async scheduled(controller, env, ctx) {
    const closed = await closeDueSlots(env, now());
    console.log(JSON.stringify({ event: "cron", closed }));
  },
};
