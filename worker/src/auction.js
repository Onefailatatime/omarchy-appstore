// Pure auction rules: no I/O, so tests/auction.test.mjs runs them under plain
// node. Slot configuration comes from data/ads.json; bids and slot state come
// from D1. Amounts are whole US dollars. Term slots bid per month.

export const SLOT_IDS = ["lifetime", "header", "rail", "footer"];

export function slotConfig(ads, id) {
  const s = ads[id];
  if (!s || !SLOT_IDS.includes(id)) return null;
  const perMonth = id !== "lifetime";
  return {
    id,
    label: s.label,
    position: s.position,
    units: Array.isArray(s.units) ? s.units.length : 1,
    reserve: perMonth ? s.reserve_month : s.reserve,
    perMonth,
    termDays: perMonth ? s.term_days : null,
    increment: s.increment,
    maxBid: s.max_bid,
    auctionDays: s.auction_days,
    extendHours: s.extend_hours,
  };
}

function compare(a, b) {
  if (b.amount !== a.amount) return b.amount - a.amount;
  if (a.approved_at !== b.approved_at) return a.approved_at < b.approved_at ? -1 : 1;
  return a.id < b.id ? -1 : 1;
}

// Winners are the top `units` approved bids, one per email, highest amount
// first and earliest approval breaking ties.
export function standings(cfg, bids) {
  const seen = new Set();
  const ranked = [];
  for (const bid of bids.filter((b) => b.status === "approved").sort(compare)) {
    const key = bid.email.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    ranked.push(bid);
  }
  const winners = ranked.slice(0, cfg.units);
  const full = winners.length >= cfg.units;
  return {
    ranked,
    winners,
    full,
    high: winners.length ? winners[0].amount : null,
    toBeat: full ? winners[winners.length - 1].amount : null,
  };
}

export function minimumBid(cfg, st) {
  return st.full ? Math.max(cfg.reserve, st.toBeat + cfg.increment) : cfg.reserve;
}

export function money(n) {
  return "$" + Number(n).toLocaleString("en-US");
}

export function validateAmount(cfg, st, amount) {
  if (!Number.isInteger(amount) || amount <= 0) return "Enter a whole dollar amount.";
  const min = minimumBid(cfg, st);
  if (amount < min) return `The minimum bid is ${money(min)}${cfg.perMonth ? " per month" : ""}.`;
  if (amount > cfg.maxBid) return `Bids above ${money(cfg.maxBid)} need a quick word first. Message @jessyka_boat on X.`;
  return null;
}

function iso(ms) {
  return new Date(ms).toISOString();
}

// The first approved bid starts the clock. A bid approved inside the final
// extend window pushes the close out by that window, so sniping never pays.
export function clockAfterApproval(cfg, state, nowIso) {
  const now = Date.parse(nowIso);
  if (!state.closes_at) {
    return { ...state, status: "live", opened_at: nowIso, closes_at: iso(now + cfg.auctionDays * 86400e3) };
  }
  const extendMs = cfg.extendHours * 3600e3;
  if (Date.parse(state.closes_at) - now < extendMs) {
    return { ...state, status: "live", closes_at: iso(now + extendMs), extensions: (state.extensions || 0) + 1 };
  }
  return { ...state, status: "live" };
}

export function isDue(state, nowIso) {
  return state.status === "live" && !!state.closes_at && Date.parse(state.closes_at) <= Date.parse(nowIso);
}

export function displaced(before, after) {
  const still = new Set(after.winners.map((b) => b.id));
  return before.winners.filter((b) => !still.has(b.id));
}

export function termCharge(cfg, amount) {
  return cfg.perMonth ? Math.round((amount * cfg.termDays) / 30) : amount;
}

export function publicState(cfg, state, st, nowIso) {
  const secondsLeft = state.closes_at ? Math.max(0, Math.round((Date.parse(state.closes_at) - Date.parse(nowIso)) / 1000)) : null;
  return {
    id: cfg.id,
    label: cfg.label,
    units: cfg.units,
    per_month: cfg.perMonth,
    term_days: cfg.termDays,
    reserve: cfg.reserve,
    increment: cfg.increment,
    auction_days: cfg.auctionDays,
    extend_hours: cfg.extendHours,
    status: state.status,
    cycle: state.cycle,
    opened_at: state.opened_at,
    closes_at: state.closes_at,
    closed_at: state.closed_at,
    extensions: state.extensions || 0,
    seconds_left: state.status === "live" ? secondsLeft : null,
    bid_count: st.ranked.length,
    high_bid: st.high,
    low_winning_bid: st.full ? st.toBeat : null,
    minimum_bid: state.status === "closed" ? null : minimumBid(cfg, st),
  };
}
