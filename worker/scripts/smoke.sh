#!/usr/bin/env bash
# End-to-end check of the auction API. Needs BASE (worker origin), TOKEN
# (admin token) and ORIGIN (an allowed site origin). Leaves the slots it
# touched reset, so it is safe against production when nothing has been sold.
#   BASE=http://localhost:8787 TOKEN=dev-admin-token ORIGIN=http://localhost:8000 worker/scripts/smoke.sh
set -euo pipefail
: "${BASE:?}" "${TOKEN:?}" "${ORIGIN:?}"
j() { python3 -I -c 'import json,sys; d=json.load(sys.stdin); print(eval(sys.argv[1]))' "$1"; }
post() { curl -s -X POST "$BASE$1" -H "content-type: application/json" -H "origin: $ORIGIN" -d "$2"; }
admin() { curl -s -X POST "$BASE$1" -H "content-type: application/json" -H "authorization: Bearer $TOKEN" -d "${2:-{\}}"; }
fail() { echo "FAIL: $*" >&2; exit 1; }

echo "1. state is public and all four slots are open"
S=$(curl -s "$BASE/api/state"); [ "$(echo "$S" | j 'len(d["slots"])')" = 4 ] || fail "slots"
echo "$S" | j 'd["slots"]["footer"]["minimum_bid"]' | grep -q '^25$' || fail "footer minimum"

echo "2. cross-site and bad bids are refused"
curl -s -o /dev/null -w '%{http_code}\n' -X POST "$BASE/api/bid" -H "content-type: application/json" -H "origin: https://evil.example" -d '{}' | grep -q 403 || fail "origin"
post /api/bid '{"slot":"footer","amount":10,"name":"Low","url":"https://example.com","tagline":"t","email":"low@example.com","agree":true}' | grep -q 'minimum bid is \$25 per month' || fail "minimum"
post /api/bid '{"slot":"footer","amount":30,"name":"Bad","url":"ftp://x","tagline":"t","email":"bad@example.com","agree":true}' | grep -q 'starting with https' || fail "url"
post /api/bid '{"slot":"footer","amount":30,"name":"Bot","url":"https://example.com","tagline":"t","email":"bot@example.com","agree":true,"website":"spam"}' | grep -q '"ok":true' || fail "honeypot"

echo "3. three bids land, one above, one below"
A=$(post /api/bid '{"slot":"footer","amount":30,"name":"Alpha","url":"https://alpha.example.com","tagline":"First in","email":"alpha@example.com","agree":true}' | j 'd["bid_id"]')
B=$(post /api/bid '{"slot":"footer","amount":40,"name":"Beta","url":"https://beta.example.com","tagline":"Second","email":"beta@example.com","agree":true}' | j 'd["bid_id"]')
C=$(post /api/bid '{"slot":"footer","amount":26,"name":"Gamma","url":"https://gamma.example.com","tagline":"Third","email":"gamma@example.com","agree":true}' | j 'd["bid_id"]')
curl -s "$BASE/api/state" | j 'd["slots"]["footer"]["bid_count"]' | grep -q '^0$' || fail "unapproved bids must not count"

echo "4. admin needs the token"
curl -s -o /dev/null -w '%{http_code}\n' "$BASE/api/admin/overview" | grep -q 401 || fail "auth"
curl -s "$BASE/api/admin/overview" -H "authorization: Bearer $TOKEN" | j 'len([b for s in d["slots"] if s["id"]=="footer" for b in s["bids"]])' | grep -q '^3$' || fail "overview bids"

echo "5. approving starts the clock, the board fills, a fourth bid displaces the lowest"
admin "/api/admin/bids/$A/approve" | grep -q '"ok":true' || fail "approve A"
S=$(curl -s "$BASE/api/state"); [ "$(echo "$S" | j 'd["slots"]["footer"]["status"]')" = live ] || fail "clock"
admin "/api/admin/bids/$B/approve" >/dev/null; admin "/api/admin/bids/$C/approve" >/dev/null
S=$(curl -s "$BASE/api/state"); [ "$(echo "$S" | j 'd["slots"]["footer"]["minimum_bid"]')" = 31 ] || fail "minimum after fill: $S"
D=$(post /api/bid '{"slot":"footer","amount":50,"name":"Delta","url":"https://delta.example.com","tagline":"Fourth","email":"delta@example.com","agree":true}' | j 'd["bid_id"]')
admin "/api/admin/bids/$D/approve" | j 'd["displaced"]' | grep -q "$C" || fail "displace gamma"
S=$(curl -s "$BASE/api/state"); [ "$(echo "$S" | j 'd["slots"]["footer"]["high_bid"]')" = 50 ] || fail "high"
[ "$(echo "$S" | j 'd["slots"]["footer"]["low_winning_bid"]')" = 30 ] || fail "low winning"

echo "6. a second bid from the same email replaces the first"
A2=$(post /api/bid '{"slot":"footer","amount":60,"name":"Alpha","url":"https://alpha.example.com","tagline":"Raised","email":"alpha@example.com","agree":true}' | j 'd["bid_id"]')
admin "/api/admin/bids/$A2/approve" >/dev/null
curl -s "$BASE/api/admin/overview" -H "authorization: Bearer $TOKEN" | j '[b["status"] for s in d["slots"] if s["id"]=="footer" for b in s["bids"] if b["id"]=="'"$A"'"][0]' | grep -q superseded || fail "supersede"

echo "7. void a bid, the cron leaves a live round alone, closing picks three winners"
admin "/api/admin/bids/$B/void" '{"reason":"test"}' | grep -q '"ok":true' || fail "void"
curl -s "$BASE/cdn-cgi/local/scheduled" >/dev/null 2>&1 || true
[ "$(curl -s "$BASE/api/state" | j 'd["slots"]["footer"]["status"]')" = live ] || fail "cron closed early"
W=$(admin /api/admin/slots/footer/close); echo "$W" | j 'len(d["winners"])' | grep -q '^3$' || fail "winners: $W"
echo "$W" | j '[w["name"] for w in d["winners"]]' | grep -q "Alpha.*Delta.*Gamma\|Alpha.*Gamma.*Delta" || fail "winner set: $W"
[ "$(curl -s "$BASE/api/state" | j 'd["slots"]["footer"]["minimum_bid"]')" = None ] || fail "closed minimum"
post /api/bid '{"slot":"footer","amount":99,"name":"Late","url":"https://late.example.com","tagline":"t","email":"late@example.com","agree":true}' | grep -q 'has closed' || fail "closed slot rejects"

echo "8. paid plus approved ad becomes a sponsor; reopen starts round 2; reset refuses a paid round"
admin "/api/admin/bids/$A2/paid" >/dev/null; admin "/api/admin/bids/$A2/creative-approve" '{"mark":"A","image":"https://alpha.example.com/ad.png"}' >/dev/null
curl -s "$BASE/api/state" | j 'd["slots"]["footer"]["sponsors"][0]["name"]' | grep -q Alpha || fail "sponsor"
admin /api/admin/slots/footer/reset | grep -q 'paid winner' || fail "reset guard"
admin /api/admin/slots/footer/reopen | j 'd["cycle"]' | grep -q '^2$' || fail "reopen"
curl -s "$BASE/api/state" | j 'd["slots"]["footer"]["sponsors"][0]["name"]' | grep -q Alpha || fail "sponsor persists into round 2"

echo "9. clean up: unpay and reset round 2 and round 1"
admin "/api/admin/bids/$A2/unpaid" >/dev/null
admin /api/admin/slots/footer/reset | grep -q '"ok":true' || fail "reset r2"
echo "smoke-ok (footer left on round 2, empty; round 1 history kept with no paid rows)"
