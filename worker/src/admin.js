// Admin API and the one page page that drives it. Bearer token only; the token
// lives in the ADMIN_TOKEN secret and in Jessyka's Keychain.

import { SLOT_IDS, publicState, minimumBid, termCharge } from "./auction.js";
import { mailConfigured } from "./mail.js";
import { loadSlot, sponsorsFor, approveBid, voidBid, closeSlot, reopenSlot, resetSlot, logEvent, now } from "./store.js";

const JSON_HEADERS = { "cache-control": "no-store", "content-type": "application/json; charset=utf-8", "x-content-type-options": "nosniff" };

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: JSON_HEADERS });
}

export async function authorized(request, env) {
  const header = request.headers.get("authorization") || "";
  const token = header.startsWith("Bearer ") ? header.slice(7).trim() : "";
  if (!env.ADMIN_TOKEN || !token) return false;
  const a = new TextEncoder().encode(token);
  const b = new TextEncoder().encode(env.ADMIN_TOKEN);
  if (a.byteLength !== b.byteLength) return false;
  return crypto.subtle.timingSafeEqual(a, b);
}

async function overview(env) {
  const at = now();
  const slots = [];
  for (const id of SLOT_IDS) {
    const { cfg, state, bids, st } = await loadSlot(env, id);
    const history = (await env.DB.prepare("SELECT * FROM bids WHERE slot = ? AND cycle < ? AND status = 'won' ORDER BY cycle DESC").bind(id, state.cycle).all()).results;
    slots.push({
      ...publicState(cfg, state, st, at),
      winners: st.winners.map((b) => b.id),
      bids: bids.map((b) => ({ ...b, charge: termCharge(cfg, b.amount) })),
      history,
      sponsors: await sponsorsFor(env, cfg),
    });
  }
  const events = (await env.DB.prepare("SELECT * FROM events ORDER BY id DESC LIMIT 60").all()).results;
  return { generated_at: at, mode: mailConfigured(env) ? "email" : "review", telegram: Boolean(env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID), slots, events };
}

async function updateBid(env, id, fields, type, detail) {
  const bid = await env.DB.prepare("SELECT * FROM bids WHERE id = ?").bind(id).first();
  if (!bid) return { error: "No such bid", status: 404 };
  const keys = Object.keys(fields);
  const at = now();
  await env.DB.batch([
    env.DB.prepare(`UPDATE bids SET ${keys.map((k) => `${k} = ?`).join(", ")} WHERE id = ?`).bind(...keys.map((k) => fields[k]), id),
    logEvent(env, at, bid.slot, id, type, detail),
  ]);
  return { ok: true };
}

export async function handleAdminApi(request, env, path) {
  if (!(await authorized(request, env))) return json({ error: "Unauthorized" }, 401);
  const at = now();
  if (request.method === "GET" && path === "/api/admin/overview") return json(await overview(env));
  if (request.method !== "POST") return json({ error: "Method not allowed" }, 405);

  let body = {};
  try { body = await request.json(); } catch { body = {}; }
  const text = (v, max) => (typeof v === "string" ? v.trim().slice(0, max) : "");

  let m = path.match(/^\/api\/admin\/bids\/([0-9a-f-]{36})\/([a-z-]+)$/);
  if (m) {
    const [, id, action] = m;
    let result;
    if (action === "approve") result = await approveBid(env, id, at);
    else if (action === "void") result = await voidBid(env, id, text(body.reason, 200), at);
    else if (action === "paid") result = await updateBid(env, id, { payment_status: "paid" }, "paid", "");
    else if (action === "unpaid") result = await updateBid(env, id, { payment_status: "unpaid" }, "unpaid", "");
    else if (action === "creative-approve") {
      const image = text(body.image, 300);
      result = await updateBid(env, id, { creative_status: "approved", mark: text(body.mark, 2) || null, image: /^https:\/\//.test(image) ? image : null }, "creative_approved", "");
    } else if (action === "creative-hide") result = await updateBid(env, id, { creative_status: "hidden" }, "creative_hidden", "");
    else return json({ error: "Unknown action" }, 404);
    return json(result, result.status || 200);
  }

  m = path.match(/^\/api\/admin\/slots\/(lifetime|header|rail|footer)\/(close|reopen|reset)$/);
  if (m) {
    const [, slot, action] = m;
    const result = action === "close" ? await closeSlot(env, slot, at, true) : action === "reopen" ? await reopenSlot(env, slot, at) : await resetSlot(env, slot, at);
    return json(result, result.status || 200);
  }
  return json({ error: "Not found" }, 404);
}

export function adminPage() {
  return new Response(ADMIN_HTML, {
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex",
      "content-security-policy": "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; form-action 'none'",
    },
  });
}

const ADMIN_HTML = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>Omarchy Apps sponsor auction</title>
<style>
:root{color-scheme:dark}body{margin:0;padding:1rem;background:#1a1b26;color:#c0caf5;font:15px/1.5 ui-monospace,Menlo,monospace}
h1{font-size:1.15rem;margin:0 0 .25rem}h2{font-size:1rem;margin:0}small,.muted{color:#7aa2f7}
.top{display:flex;flex-wrap:wrap;gap:.75rem;align-items:center;justify-content:space-between;margin-bottom:1rem}
.slot{margin:0 0 1rem;padding:1rem;border:1px solid #3b4261;border-radius:.5rem;background:#24283b}
.head{display:flex;flex-wrap:wrap;gap:.5rem 1rem;align-items:baseline;justify-content:space-between}
.pill{display:inline-block;padding:0 .5em;border-radius:1em;font-size:.8em;border:1px solid #3b4261}
.live{color:#9ece6a;border-color:#9ece6a}.closed{color:#f7768e;border-color:#f7768e}.open{color:#7aa2f7}
table{width:100%;border-collapse:collapse;margin-top:.75rem;font-size:.9em}th,td{padding:.35rem .4rem;text-align:left;vertical-align:top;border-top:1px solid #3b4261}th{color:#7aa2f7;font-weight:400}
button{font:inherit;font-size:.85em;padding:.2em .6em;margin:0 .25em .25em 0;border:1px solid #7aa2f7;border-radius:.3em;background:transparent;color:#c0caf5;cursor:pointer}
button:hover{background:#7aa2f7;color:#1a1b26}button.danger{border-color:#f7768e}button.danger:hover{background:#f7768e}
.won{color:#9ece6a}.voided,.lost,.expired,.superseded{color:#565f89}.approved{color:#c0caf5}.submitted,.verified{color:#e0af68}
a{color:#7dcfff}#msg{min-height:1.4em;color:#e0af68}.events{font-size:.85em;color:#565f89}details{margin-top:.5rem}
@media(max-width:700px){table,thead,tbody,tr,td,th{display:block}thead{display:none}td{border:0;padding:.1rem 0}tr{border-top:1px solid #3b4261;padding:.4rem 0}td:before{content:attr(data-l) ": ";color:#7aa2f7}}
</style></head><body>
<div class="top"><div><h1>Sponsor auction</h1><small id="mode"></small></div><div><button id="refresh">Refresh</button> <button id="logout">Forget token</button></div></div>
<p id="msg"></p>
<div id="slots"></div>
<details><summary>Recent events</summary><div class="events" id="events"></div></details>
<script>
(function(){
"use strict";
var KEY="omarchy_auction_admin";
function token(){var t=sessionStorage.getItem(KEY);if(!t){t=prompt("Admin token");if(t)sessionStorage.setItem(KEY,t.trim());}return t;}
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
function money(n){return "$"+Number(n).toLocaleString("en-US");}
function left(sec){if(sec==null)return "";var d=Math.floor(sec/86400),h=Math.floor(sec%86400/3600),m=Math.floor(sec%3600/60);return d?d+"d "+h+"h":h?h+"h "+m+"m":m+"m";}
function api(path,opts){opts=opts||{};opts.headers=Object.assign({authorization:"Bearer "+token()},opts.headers||{});return fetch(path,opts).then(function(r){return r.json().then(function(d){if(r.status===401){sessionStorage.removeItem(KEY);}if(!r.ok)throw new Error(d.error||("HTTP "+r.status));return d;});});}
function act(path,body){document.getElementById("msg").textContent="Working…";return api(path,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(body||{})}).then(function(d){document.getElementById("msg").textContent=d.winners?("Closed. Winners: "+d.winners.map(function(w){return money(w.amount)+" "+w.name+" <"+w.email+"> charge "+money(w.charge);}).join("; ")||"Closed with no winner"):"Done.";load();}).catch(function(e){document.getElementById("msg").textContent=e.message;});}
function bidRow(slot,b){
  var isW=slot.winners.indexOf(b.id)>=0;
  var acts="";
  if(b.status==="submitted"||b.status==="verified")acts+='<button data-a="approve" data-id="'+b.id+'">Approve</button>';
  if(["submitted","verified","approved"].indexOf(b.status)>=0)acts+='<button class="danger" data-a="void" data-id="'+b.id+'">Void</button>';
  if(b.status==="won"){acts+=b.payment_status==="paid"?'<button data-a="unpaid" data-id="'+b.id+'">Mark unpaid</button>':'<button data-a="paid" data-id="'+b.id+'">Mark paid</button>';
    acts+=b.creative_status==="approved"?'<button data-a="creative-hide" data-id="'+b.id+'">Hide ad</button>':'<button data-a="creative-approve" data-id="'+b.id+'">Approve ad</button>';}
  return '<tr><td data-l="Amount"><b>'+money(b.amount)+(slot.per_month?"/mo":"")+'</b>'+(isW?' <span class="pill live">winning</span>':'')+'</td>'
   +'<td data-l="Product"><a href="'+esc(b.url)+'" target="_blank" rel="noopener">'+esc(b.name)+'</a><br><small>'+esc(b.tagline)+'</small></td>'
   +'<td data-l="Email"><a href="mailto:'+esc(b.email)+'">'+esc(b.email)+'</a></td>'
   +'<td data-l="Status"><span class="'+esc(b.status)+'">'+esc(b.status)+'</span>'+(b.status==="won"?'<br><small>'+esc(b.payment_status)+' · ad '+esc(b.creative_status)+' · charge '+money(b.charge)+'</small>':'')+(b.void_reason?'<br><small>'+esc(b.void_reason)+'</small>':'')+'</td>'
   +'<td data-l="When"><small>'+esc((b.created_at||"").slice(0,16).replace("T"," "))+'</small></td><td data-l="Actions">'+acts+'</td></tr>';
}
function render(d){
  document.getElementById("mode").textContent=(d.mode==="email"?"Email verification on":"Review mode: approve each bid by hand")+(d.telegram?" · Telegram alerts on":" · no Telegram alerts")+" · "+d.generated_at.slice(0,16).replace("T"," ")+" UTC";
  document.getElementById("slots").innerHTML=d.slots.map(function(s){
    var clock=s.status==="live"?"closes "+s.closes_at.slice(0,16).replace("T"," ")+" UTC ("+left(s.seconds_left)+" left"+(s.extensions?", extended "+s.extensions+"x":"")+")":s.status==="closed"?"closed "+(s.closed_at||"").slice(0,16).replace("T"," "):"clock starts at the first approved bid";
    var sl='<button data-s="close" data-slot="'+s.id+'" class="danger">Close now</button>';
    if(s.status==="closed")sl+='<button data-s="reopen" data-slot="'+s.id+'">Reopen (new round)</button>';
    sl+='<button data-s="reset" data-slot="'+s.id+'" class="danger">Reset round</button>';
    var sp=s.sponsors.length?'<p><small>Live sponsor'+(s.sponsors.length>1?"s":"")+': '+s.sponsors.map(function(x){return esc(x.name);}).join(", ")+'</small></p>':'';
    var rows=s.bids.length?'<table><thead><tr><th>Amount</th><th>Product</th><th>Email</th><th>Status</th><th>When</th><th></th></tr></thead><tbody>'+s.bids.slice().sort(function(a,b){return b.amount-a.amount;}).map(function(b){return bidRow(s,b);}).join("")+'</tbody></table>':'<p class="muted">No bids this round.</p>';
    var hist=s.history.length?'<details><summary>Earlier winners</summary>'+s.history.map(function(b){return '<div>Round '+b.cycle+': '+money(b.amount)+' '+esc(b.name)+' ('+esc(b.email)+') '+esc(b.payment_status)+'</div>';}).join("")+'</details>':'';
    return '<section class="slot"><div class="head"><h2>'+esc(s.label)+' <span class="pill '+esc(s.status)+'">'+esc(s.status)+'</span> <small>round '+s.cycle+'</small></h2><div>'+sl+'</div></div>'
     +'<p><small>'+clock+' · reserve '+money(s.reserve)+(s.per_month?"/mo":"")+' · high '+(s.high_bid==null?"none":money(s.high_bid))+' · minimum '+(s.minimum_bid==null?"n/a":money(s.minimum_bid))+' · '+s.units+' unit'+(s.units>1?"s":"")+'</small></p>'+sp+rows+hist+'</section>';
  }).join("");
  document.getElementById("events").innerHTML=d.events.map(function(e){return '<div>'+esc(e.at.slice(0,16).replace("T"," "))+' '+esc(e.slot||"")+' '+esc(e.type)+' '+esc(e.detail||"")+'</div>';}).join("");
}
function load(){if(!token())return;api("/api/admin/overview").then(render).catch(function(e){document.getElementById("msg").textContent=e.message;});}
document.addEventListener("click",function(ev){
  var b=ev.target.closest("button");if(!b)return;
  if(b.id==="refresh")return load();
  if(b.id==="logout"){sessionStorage.removeItem(KEY);location.reload();return;}
  if(b.dataset.a){var body={};
    if(b.dataset.a==="void"){var r=prompt("Reason (shown to nobody, kept in the log)");if(r===null)return;body.reason=r;}
    if(b.dataset.a==="creative-approve"){body.mark=prompt("Mark (one or two characters shown beside the name, blank for the first letter)")||"";body.image=prompt("Image URL for sidebar units (300x180 https, blank for none)")||"";}
    return act("/api/admin/bids/"+b.dataset.id+"/"+b.dataset.a,body);}
  if(b.dataset.s){if(!confirm(b.dataset.s+" "+b.dataset.slot+"?"))return;return act("/api/admin/slots/"+b.dataset.slot+"/"+b.dataset.s);}
});
load();
})();
</script></body></html>`;
