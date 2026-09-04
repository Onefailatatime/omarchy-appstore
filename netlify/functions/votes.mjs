import { randomUUID } from "node:crypto";
import { getStore } from "@netlify/blobs";
import appNames from "./app-names.mjs";

const COOKIE = "__Host-omarchy_voter";
const STORE_NAME = "omarchy-app-votes";
const allowedApps = new Set(appNames);
const jsonHeaders = {
  "cache-control": "no-store",
  "content-type": "application/json; charset=utf-8",
  "referrer-policy": "same-origin",
  "x-content-type-options": "nosniff",
};

function response(data, status = 200, cookie = "") {
  const headers = new Headers(jsonHeaders);
  if (cookie) headers.set("set-cookie", cookie);
  return new Response(JSON.stringify(data), { status, headers });
}

function cookieValue(header, name) {
  for (const pair of (header || "").split(";")) {
    const [key, ...value] = pair.trim().split("=");
    if (key === name) return decodeURIComponent(value.join("="));
  }
  return "";
}

async function countVotes(store, voter = "") {
  const { blobs } = await store.list({ prefix: "vote/" });
  const counts = {};
  const voted = [];
  for (const blob of blobs) {
    const parts = blob.key.split("/");
    if (parts.length !== 3 || !allowedApps.has(parts[1])) continue;
    counts[parts[1]] = (counts[parts[1]] || 0) + 1;
    if (voter && parts[2] === voter) voted.push(parts[1]);
  }
  return { counts, voted };
}

export async function handleVoteRequest(request, store, makeID = randomUUID) {
  if (request.method === "GET") {
    const voter = cookieValue(request.headers.get("cookie"), COOKIE);
    return response(await countVotes(store, voter));
  }

  if (request.method !== "POST") {
    return response({ error: "Method not allowed" }, 405);
  }

  const origin = request.headers.get("origin");
  if (origin && origin !== new URL(request.url).origin) {
    return response({ error: "Cross-site voting is not allowed" }, 403);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return response({ error: "Invalid JSON" }, 400);
  }
  const app = typeof body.app === "string" ? body.app : "";
  if (!allowedApps.has(app)) {
    return response({ error: "Unknown app" }, 400);
  }

  let voter = cookieValue(request.headers.get("cookie"), COOKIE);
  let setCookie = "";
  if (!/^[0-9a-f-]{36}$/.test(voter)) {
    voter = makeID();
    setCookie = `${COOKIE}=${encodeURIComponent(voter)}; Path=/; Max-Age=31536000; Secure; HttpOnly; SameSite=Lax`;
  }

  const key = `vote/${app}/${voter}`;
  const existing = await store.getMetadata(key, { consistency: "strong" });
  if (!existing) await store.set(key, new Date().toISOString());
  const { blobs } = await store.list({ prefix: `vote/${app}/` });
  return response({ app, count: blobs.length, voted: true }, 200, setCookie);
}

export default async function votes(request) {
  try {
    const store = getStore({ name: STORE_NAME, consistency: "strong" });
    return await handleVoteRequest(request, store);
  } catch (error) {
    console.error("vote function failed", error);
    return response({ error: "Votes are temporarily unavailable" }, 500);
  }
}

export const config = {
  path: "/api/votes",
  rateLimit: {
    windowLimit: 60,
    windowSize: 60,
    aggregateBy: ["ip", "domain"],
  },
};
