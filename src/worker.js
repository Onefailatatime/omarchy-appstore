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
