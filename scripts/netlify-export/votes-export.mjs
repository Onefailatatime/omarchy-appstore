import { getStore } from "@netlify/blobs";
// One-off: dumps every upvote key for the Cloudflare migration. Deploy it to
// the Netlify site once (see export.sh), read /api/votes-export?key=..., then
// it is gone with the next deploy.
export default async function exportVotes(request) {
  if (new URL(request.url).searchParams.get("key") !== "__EXPORT_KEY__") return new Response("no", { status: 404 });
  const store = getStore({ name: "omarchy-app-votes", consistency: "strong" });
  const { blobs } = await store.list({ prefix: "vote/" });
  const rows = [];
  for (const b of blobs) rows.push({ key: b.key, value: await store.get(b.key) });
  return new Response(JSON.stringify({ count: rows.length, rows }), { headers: { "content-type": "application/json", "cache-control": "no-store" } });
}
export const config = { path: "/api/votes-export" };
