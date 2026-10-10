// D1 access and the state transitions that touch several rows at once. Every
// multi-row change goes through one batch, which D1 runs as a transaction.

import adsConfig from "../../data/ads.json";
import { SLOT_IDS, slotConfig, standings, clockAfterApproval, isDue, displaced, minimumBid, termCharge, money } from "./auction.js";
import { mailConfigured, sendMail, outbidEmail, wonEmail } from "./mail.js";
import { notifyAdmin } from "./notify.js";

export const ads = adsConfig;

export function now() {
  return new Date().toISOString();
}

export function logEvent(env, at, slot, bidId, type, detail = "") {
  return env.DB.prepare("INSERT INTO events (at, slot, bid_id, type, detail) VALUES (?, ?, ?, ?, ?)").bind(at, slot, bidId, type, detail);
}

const EMPTY_STATE = (slot) => ({ slot, cycle: 1, status: "open", opened_at: null, closes_at: null, closed_at: null, extensions: 0 });

export async function loadSlot(env, id) {
  const cfg = slotConfig(ads, id);
  if (!cfg) return null;
  let state = await env.DB.prepare("SELECT * FROM slot_state WHERE slot = ?").bind(id).first();
  if (!state) {
    await env.DB.prepare("INSERT OR IGNORE INTO slot_state (slot) VALUES (?)").bind(id).run();
    state = EMPTY_STATE(id);
  }
  const bids = (await env.DB.prepare("SELECT * FROM bids WHERE slot = ? AND cycle = ? ORDER BY created_at").bind(id, state.cycle).all()).results;
  return { cfg, state, bids, st: standings(cfg, bids) };
}

export async function loadAllSlots(env) {
  const out = [];
  for (const id of SLOT_IDS) out.push(await loadSlot(env, id));
  return out;
}

// Paid, approved winners render as the slot's sponsors. The newest round wins;
// an older sponsor keeps showing until the next round's winner has paid.
export async function sponsorsFor(env, cfg) {
  const rows = (await env.DB.prepare(
    "SELECT name, url, tagline, mark, image, decided_at FROM bids WHERE slot = ? AND status = 'won' AND payment_status = 'paid' AND creative_status = 'approved' ORDER BY cycle DESC, amount DESC LIMIT ?",
  ).bind(cfg.id, cfg.units).all()).results;
  return rows.map((r) => ({ name: r.name, url: r.url, tagline: r.tagline, mark: r.mark || null, image: r.image || null, since: r.decided_at ? r.decided_at.slice(0, 10) : null }));
}

export async function rateLimited(db, key, limit, windowMs, at) {
  const row = await db.prepare("SELECT count, window_start FROM rate_limits WHERE key = ?").bind(key).first();
  if (!row || Date.parse(at) - Date.parse(row.window_start) >= windowMs) {
    await db.prepare("INSERT INTO rate_limits (key, count, window_start) VALUES (?, 1, ?) ON CONFLICT(key) DO UPDATE SET count = 1, window_start = excluded.window_start").bind(key, at).run();
    return false;
  }
  if (row.count >= limit) return true;
  await db.prepare("UPDATE rate_limits SET count = count + 1 WHERE key = ?").bind(key).run();
  return false;
}

export async function approveBid(env, bidId, at) {
  const bid = await env.DB.prepare("SELECT * FROM bids WHERE id = ?").bind(bidId).first();
  if (!bid) return { error: "No such bid", status: 404 };
  if (!["submitted", "verified"].includes(bid.status)) return { error: `This bid is already ${bid.status}`, status: 409 };
  const loaded = await loadSlot(env, bid.slot);
  const { cfg, state, bids, st: before } = loaded;
  if (bid.cycle !== state.cycle) return { error: "This bid belongs to an earlier round", status: 409 };
  if (state.status === "closed") return { error: "Bidding on this slot has closed", status: 409 };

  const superseded = bids.filter((b) => b.status === "approved" && b.id !== bid.id && b.email.toLowerCase() === bid.email.toLowerCase());
  const next = clockAfterApproval(cfg, state, at);
  const statements = [
    env.DB.prepare("UPDATE bids SET status = 'approved', approved_at = ? WHERE id = ?").bind(at, bid.id),
    ...superseded.map((b) => env.DB.prepare("UPDATE bids SET status = 'superseded', decided_at = ? WHERE id = ?").bind(at, b.id)),
    env.DB.prepare("UPDATE slot_state SET status = ?, opened_at = ?, closes_at = ?, extensions = ? WHERE slot = ?").bind(next.status, next.opened_at, next.closes_at, next.extensions || 0, cfg.id),
    logEvent(env, at, cfg.id, bid.id, "approved", money(bid.amount)),
  ];
  if (next.closes_at !== state.closes_at) statements.push(logEvent(env, at, cfg.id, bid.id, state.closes_at ? "extended" : "opened", next.closes_at));
  await env.DB.batch(statements);

  const updated = bids.map((b) => (b.id === bid.id ? { ...b, status: "approved", approved_at: at } : superseded.includes(b) ? { ...b, status: "superseded" } : b));
  const after = standings(cfg, updated);
  const out = displaced(before, after);
  if (mailConfigured(env)) {
    const minimum = minimumBid(cfg, after);
    for (const d of out) await sendMail(env, outbidEmail({ siteUrl: env.SITE_URL, cfg, bid: d, minimum, closesAt: next.closes_at }));
  }
  return { ok: true, state: next, displaced: out.map((b) => b.id), high: after.high };
}

export async function voidBid(env, bidId, reason, at) {
  const bid = await env.DB.prepare("SELECT * FROM bids WHERE id = ?").bind(bidId).first();
  if (!bid) return { error: "No such bid", status: 404 };
  if (!["submitted", "verified", "approved"].includes(bid.status)) return { error: `This bid is already ${bid.status}`, status: 409 };
  await env.DB.batch([
    env.DB.prepare("UPDATE bids SET status = 'voided', void_reason = ?, decided_at = ? WHERE id = ?").bind(reason || "", at, bid.id),
    logEvent(env, at, bid.slot, bid.id, "voided", reason || ""),
  ]);
  return { ok: true };
}

export async function closeSlot(env, slotId, at, force = false) {
  const loaded = await loadSlot(env, slotId);
  if (!loaded) return { error: "Unknown slot", status: 404 };
  const { cfg, state, bids, st } = loaded;
  if (state.status === "closed") return { error: "Already closed", status: 409 };
  if (!force && !isDue(state, at)) return { error: "Not due yet", status: 409 };
  const winners = new Set(st.winners.map((b) => b.id));
  const statements = [];
  for (const b of bids) {
    if (b.status === "approved") statements.push(env.DB.prepare("UPDATE bids SET status = ?, decided_at = ? WHERE id = ?").bind(winners.has(b.id) ? "won" : "lost", at, b.id));
    else if (["submitted", "verified"].includes(b.status)) statements.push(env.DB.prepare("UPDATE bids SET status = 'expired', decided_at = ? WHERE id = ?").bind(at, b.id));
  }
  statements.push(env.DB.prepare("UPDATE slot_state SET status = 'closed', closed_at = ? WHERE slot = ?").bind(at, cfg.id));
  statements.push(logEvent(env, at, cfg.id, null, force ? "closed_by_admin" : "closed", `${st.winners.length} winner(s)`));
  await env.DB.batch(statements);
  if (mailConfigured(env)) {
    for (const w of st.winners) await sendMail(env, wonEmail({ siteUrl: env.SITE_URL, cfg, bid: w, charge: termCharge(cfg, w.amount) }));
  }
  const summary = st.winners.map((w) => `${money(w.amount)} ${w.name} <${w.email}>`).join("; ") || "no winner";
  await notifyAdmin(env, `${cfg.label} auction closed: ${summary}`);
  return { ok: true, winners: st.winners.map((w) => ({ id: w.id, amount: w.amount, name: w.name, email: w.email, charge: termCharge(cfg, w.amount) })) };
}

export async function reopenSlot(env, slotId, at) {
  const loaded = await loadSlot(env, slotId);
  if (!loaded) return { error: "Unknown slot", status: 404 };
  if (loaded.state.status !== "closed") return { error: "Close the round before reopening it", status: 409 };
  await env.DB.batch([
    env.DB.prepare("UPDATE slot_state SET cycle = cycle + 1, status = 'open', opened_at = NULL, closes_at = NULL, closed_at = NULL, extensions = 0 WHERE slot = ?").bind(slotId),
    logEvent(env, at, slotId, null, "reopened", `round ${loaded.state.cycle + 1}`),
  ]);
  return { ok: true, cycle: loaded.state.cycle + 1 };
}

// Wipes the current round. Refused once anyone in it has paid, so it can only
// ever clear test bids and mistakes, never a sale.
export async function resetSlot(env, slotId, at) {
  const loaded = await loadSlot(env, slotId);
  if (!loaded) return { error: "Unknown slot", status: 404 };
  if (loaded.bids.some((b) => b.payment_status === "paid")) return { error: "This round has a paid winner and cannot be reset", status: 409 };
  await env.DB.batch([
    env.DB.prepare("DELETE FROM bids WHERE slot = ? AND cycle = ?").bind(slotId, loaded.state.cycle),
    env.DB.prepare("UPDATE slot_state SET status = 'open', opened_at = NULL, closes_at = NULL, closed_at = NULL, extensions = 0 WHERE slot = ?").bind(slotId),
    logEvent(env, at, slotId, null, "reset", `round ${loaded.state.cycle} cleared (${loaded.bids.length} bids)`),
  ]);
  return { ok: true };
}

export async function closeDueSlots(env, at) {
  const closed = [];
  for (const id of SLOT_IDS) {
    const loaded = await loadSlot(env, id);
    if (isDue(loaded.state, at)) {
      const result = await closeSlot(env, id, at);
      if (result.ok) closed.push(id);
    }
  }
  return closed;
}
