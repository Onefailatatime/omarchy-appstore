import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  slotConfig, standings, minimumBid, validateAmount, clockAfterApproval, isDue, displaced, termCharge, publicState,
} from "../worker/src/auction.js";

const ads = JSON.parse(readFileSync(new URL("../data/ads.json", import.meta.url), "utf8"));
const bid = (id, amount, email, approved_at = "2026-10-10T00:00:00.000Z", status = "approved") => ({ id, amount, email, approved_at, status });

// Lifetime: one unit, reserve starts the ladder.
const lifetime = slotConfig(ads, "lifetime");
assert.equal(lifetime.units, 1);
assert.equal(lifetime.perMonth, false);
let st = standings(lifetime, []);
assert.equal(st.full, false);
assert.equal(minimumBid(lifetime, st), lifetime.reserve);
assert.equal(validateAmount(lifetime, st, lifetime.reserve - 1), `The minimum bid is $${lifetime.reserve.toLocaleString("en-US")}.`);
assert.equal(validateAmount(lifetime, st, lifetime.reserve), null);
assert.match(validateAmount(lifetime, st, lifetime.maxBid + 1), /need a quick word/);
assert.equal(validateAmount(lifetime, st, 1000.5), "Enter a whole dollar amount.");

st = standings(lifetime, [bid("a", 1000, "a@x.com"), bid("b", 1200, "b@x.com", "2026-10-11T00:00:00.000Z")]);
assert.deepEqual(st.winners.map((b) => b.id), ["b"]);
assert.equal(st.toBeat, 1200);
assert.equal(minimumBid(lifetime, st), 1200 + lifetime.increment);

// Ties go to the earlier approval; one bid per email counts.
st = standings(lifetime, [bid("late", 1500, "a@x.com", "2026-10-12T00:00:00.000Z"), bid("early", 1500, "b@x.com", "2026-10-11T00:00:00.000Z"), bid("dupe", 1400, "A@X.com")]);
assert.deepEqual(st.ranked.map((b) => b.id), ["early", "late"]);

// Footer: three units, the third-highest sets the bar.
const footer = slotConfig(ads, "footer");
assert.equal(footer.units, 3);
assert.equal(footer.perMonth, true);
st = standings(footer, [bid("1", 25, "1@x.com"), bid("2", 30, "2@x.com")]);
assert.equal(st.full, false);
assert.equal(minimumBid(footer, st), footer.reserve);
st = standings(footer, [bid("1", 25, "1@x.com"), bid("2", 30, "2@x.com"), bid("3", 40, "3@x.com"), bid("4", 26, "4@x.com")]);
assert.deepEqual(st.winners.map((b) => b.id), ["3", "2", "4"]);
assert.equal(st.toBeat, 26);
assert.equal(minimumBid(footer, st), 26 + footer.increment);
assert.equal(validateAmount(footer, st, 26), "The minimum bid is $31 per month.");
assert.equal(termCharge(footer, 25), 75);
assert.equal(termCharge(lifetime, 1000), 1000);

// Clock: first approval opens it, a late approval extends it, an early one does not.
let state = { slot: "lifetime", cycle: 1, status: "open", opened_at: null, closes_at: null, closed_at: null, extensions: 0 };
state = clockAfterApproval(lifetime, state, "2026-10-10T00:00:00.000Z");
assert.equal(state.status, "live");
assert.equal(state.closes_at, "2026-11-09T00:00:00.000Z");
const untouched = clockAfterApproval(lifetime, state, "2026-10-20T00:00:00.000Z");
assert.equal(untouched.closes_at, state.closes_at);
assert.equal(untouched.extensions, 0);
const extended = clockAfterApproval(lifetime, state, "2026-11-08T12:00:00.000Z");
assert.equal(extended.closes_at, "2026-11-09T12:00:00.000Z");
assert.equal(extended.extensions, 1);
assert.equal(isDue(extended, "2026-11-09T11:59:00.000Z"), false);
assert.equal(isDue(extended, "2026-11-09T12:00:00.000Z"), true);
assert.equal(isDue({ ...extended, status: "closed" }, "2026-12-01T00:00:00.000Z"), false);

// Displacement: whoever drops out of the winning set gets the outbid notice.
const before = standings(footer, [bid("1", 25, "1@x.com"), bid("2", 30, "2@x.com"), bid("3", 40, "3@x.com")]);
const after = standings(footer, [bid("1", 25, "1@x.com"), bid("2", 30, "2@x.com"), bid("3", 40, "3@x.com"), bid("4", 50, "4@x.com")]);
assert.deepEqual(displaced(before, after).map((b) => b.id), ["1"]);

// Public shape never leaks bidder details.
const pub = publicState(footer, { ...state, cycle: 1 }, after, "2026-10-20T00:00:00.000Z");
assert.equal(pub.high_bid, 50);
assert.equal(pub.low_winning_bid, 30);
assert.equal(pub.minimum_bid, 35);
assert.equal(pub.bid_count, 4);
assert.ok(pub.seconds_left > 0);
assert.equal(JSON.stringify(pub).includes("@x.com"), false);

console.log("auction-rules-tests-ok");
