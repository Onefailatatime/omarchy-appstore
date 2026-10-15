#!/usr/bin/env node
// Tell IndexNow (Bing, Yandex, Seznam, Naver...) which URLs changed.
// Dry run by default: prints what it would send. Add --submit to send.
//   node scripts/indexnow-submit.mjs                 # all sitemap URLs, dry run
//   node scripts/indexnow-submit.mjs --since 2026-10-15 --submit
// The key file must already be live at https://omarchyapps.com/<key>.txt.
import { readFileSync, readdirSync } from "node:fs";

const args = process.argv.slice(2);
const submit = args.includes("--submit");
const since = args.includes("--since") ? args[args.indexOf("--since") + 1] : null;
const keyFile = readdirSync(new URL("../assets/indexnow/", import.meta.url)).find((f) => /^[0-9a-f]{32}\.txt$/.test(f));
if (!keyFile) throw new Error("no IndexNow key in assets/indexnow/");
const key = keyFile.slice(0, -4);
const host = "omarchyapps.com";
const sitemap = readFileSync(new URL("../dist/sitemap.xml", import.meta.url), "utf8");
const urls = [...sitemap.matchAll(/<loc>([^<]+)<\/loc><lastmod>([^<]+)<\/lastmod>/g)]
  .filter(([, , d]) => !since || d >= since).map(([, u]) => u);
const body = { host, key, keyLocation: `https://${host}/${key}.txt`, urlList: urls.slice(0, 10000) };
console.log(`${urls.length} URL(s)${since ? ` changed since ${since}` : ""}; key location ${body.keyLocation}`);
if (!submit) { console.log("Dry run. Re-run with --submit to send."); process.exit(0); }
const check = await fetch(body.keyLocation);
if (!check.ok || (await check.text()).trim() !== key) throw new Error("key file is not live yet; deploy first");
const res = await fetch("https://api.indexnow.org/indexnow", { method: "POST", headers: { "content-type": "application/json; charset=utf-8" }, body: JSON.stringify(body) });
console.log(`IndexNow answered ${res.status} ${res.statusText}`);
if (res.status >= 400) process.exit(1);
