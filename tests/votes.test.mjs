import assert from "node:assert/strict";
import { handleVoteRequest } from "../netlify/functions/votes.mjs";

class MemoryStore {
  constructor() { this.values = new Map(); }
  async getMetadata(key) { return this.values.has(key) ? { etag: "test" } : null; }
  async set(key, value) { this.values.set(key, value); }
  async list({ prefix }) {
    return { blobs: Array.from(this.values.keys()).filter((key) => key.startsWith(prefix)).map((key) => ({ key })) };
  }
}

const store = new MemoryStore();
const voter = "12345678-1234-1234-1234-123456789abc";
const url = "https://omarchyapps.com/api/votes";

const first = await handleVoteRequest(new Request(url, {
  method: "POST",
  headers: { "content-type": "application/json", "origin": "https://omarchyapps.com" },
  body: JSON.stringify({ app: "flea" }),
}), store, () => voter);
assert.equal(first.status, 200);
assert.equal((await first.json()).count, 1);
assert.match(first.headers.get("set-cookie"), /Secure; HttpOnly; SameSite=Lax/);

const duplicate = await handleVoteRequest(new Request(url, {
  method: "POST",
  headers: { "content-type": "application/json", "cookie": `__Host-omarchy_voter=${voter}` },
  body: JSON.stringify({ app: "flea" }),
}), store);
assert.equal((await duplicate.json()).count, 1);

const listing = await handleVoteRequest(new Request(url, {
  headers: { "cookie": `__Host-omarchy_voter=${voter}` },
}), store);
assert.deepEqual(await listing.json(), { counts: { flea: 1 }, voted: ["flea"] });

const unknown = await handleVoteRequest(new Request(url, {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ app: "not-a-real-package" }),
}), store);
assert.equal(unknown.status, 400);

const crossSite = await handleVoteRequest(new Request(url, {
  method: "POST",
  headers: { "content-type": "application/json", "origin": "https://example.com" },
  body: JSON.stringify({ app: "flea" }),
}), store);
assert.equal(crossSite.status, 403);

console.log("vote-function-tests-ok");
