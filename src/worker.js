// omarchyapps.com on Cloudflare: static assets from dist/ plus the two APIs
// that used to be Netlify Functions. Headers for static files come from
// dist/_headers; API responses set their own.

import { handleVoteRequest, D1VoteStore } from "./votes.mjs";
import { handleSubscribeRequest } from "./subscribe.mjs";

async function sha256Hex(text) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

// Sliding-window counter in D1; keys hold a salted hash, never a raw address.
export async function rateLimited(db, key, limit, windowMs, at = new Date().toISOString()) {
  const row = await db.prepare("SELECT count, window_start FROM rate_limits WHERE key = ?").bind(key).first();
  if (!row || Date.parse(at) - Date.parse(row.window_start) >= windowMs) {
    await db.prepare("INSERT INTO rate_limits (key, count, window_start) VALUES (?, 1, ?) ON CONFLICT(key) DO UPDATE SET count = 1, window_start = excluded.window_start").bind(key, at).run();
    return false;
  }
  if (row.count >= limit) return true;
  await db.prepare("UPDATE rate_limits SET count = count + 1 WHERE key = ?").bind(key).run();
  return false;
}

// First-party Umami: the tracker and its collector are served from
// omarchyapps.com/stats/* and forwarded to the self-hosted edge, whose origin
// lives only in the UMAMI_UPSTREAM Worker secret. No secret, no proxy (404).

export async function proxyStats(request, pathname, origin, fetchImpl = fetch) {
  if (!origin) return new Response("Not found", { status: 404 });
  origin = origin.replace(/\/+$/, "");
  if (pathname === "/stats/script.js" && (request.method === "GET" || request.method === "HEAD")) {
    const res = await fetchImpl(origin + "/script.js", { cf: { cacheTtl: 3600, cacheEverything: true } });
    return new Response(request.method === "HEAD" ? null : res.body, {
      status: res.status,
      headers: { "content-type": "application/javascript; charset=utf-8", "cache-control": "public, max-age=3600" },
    });
  }
  if (pathname === "/stats/api/send" && request.method === "POST") {
    const headers = new Headers({ "content-type": "application/json" });
    for (const h of ["user-agent", "accept-language", "x-umami-cache", "x-umami-website-id", "x-umami-hostname"]) if (request.headers.get(h)) headers.set(h, request.headers.get(h));
    const ip = request.headers.get("cf-connecting-ip");
    if (ip) headers.set("x-forwarded-for", ip);
    const res = await fetchImpl(origin + "/api/send", { method: "POST", headers, body: await request.text() });
    return new Response(res.body, { status: res.status, headers: { "content-type": res.headers.get("content-type") || "application/json", "cache-control": "no-store" } });
  }
  return new Response("Not found", { status: 404 });
}

const tooMany = () => new Response(JSON.stringify({ error: "Too many requests. Try again in a minute." }), {
  status: 429, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
});

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const { pathname } = url;
    try {
      // One canonical host: www redirects to the apex.
      if (url.hostname.startsWith("www.")) {
        url.hostname = url.hostname.slice(4);
        return Response.redirect(url.toString(), 301);
      }
      if (pathname.startsWith("/stats/")) return await proxyStats(request, pathname, env.UMAMI_UPSTREAM);
      if (pathname === "/api/votes" || pathname === "/api/subscribe") {
        if (request.method === "POST") {
          const ip = request.headers.get("cf-connecting-ip") || "0.0.0.0";
          const key = `${pathname}:${(await sha256Hex(`${ip}|${env.IP_SALT || ""}`)).slice(0, 32)}`;
          const limit = pathname === "/api/votes" ? 60 : 5;
          if (await rateLimited(env.DB, key, limit, 60e3)) return tooMany();
        }
        if (pathname === "/api/votes") return await handleVoteRequest(request, new D1VoteStore(env.DB));
        return await handleSubscribeRequest(request, env);
      }
      // The advertise page was renamed to sponsor.html; keep old links working.
      if (pathname === "/advertise.html" || pathname === "/advertise") {
        return Response.redirect(new URL("/sponsor.html" + url.search + url.hash, request.url).toString(), 301);
      }
      // html_handling is off so every canonical .html URL serves as-is; only the root needs a hand.
      if (pathname === "/") return env.ASSETS.fetch(new Request(new URL("/index.html", request.url), request));
      if (!pathname.includes(".") && pathname !== "/") {
        const clean = pathname.replace(/\/+$/, "");
        const probe = await env.ASSETS.fetch(new Request(new URL(clean + ".html", request.url), { method: "HEAD" }));
        if (probe.ok) {
          url.pathname = clean + ".html";
          return Response.redirect(url.toString(), 301);
        }
      }
      return env.ASSETS.fetch(request);
    } catch (error) {
      console.error(JSON.stringify({ event: "request_failed", path: pathname, error: String(error && error.stack || error) }));
      return new Response(JSON.stringify({ error: "Temporarily unavailable" }), { status: 500, headers: { "content-type": "application/json; charset=utf-8" } });
    }
  },
};
