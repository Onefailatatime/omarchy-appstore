#!/bin/zsh
# Exports the upvotes still held in Netlify Blobs, then imports them into D1.
# Run once from the repo root while omarchyapps.com is still on Netlify:
#   scripts/netlify-export/export.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
SITE=d487ea21-2ea9-4b8e-a0aa-a20430f99ca0
KEY=$(openssl rand -hex 16)
W=$(mktemp -d)
git worktree add -q "$W" origin/main
sed "s/__EXPORT_KEY__/$KEY/" scripts/netlify-export/votes-export.mjs > "$W/netlify/functions/votes-export.mjs"
(cd "$W" && npm ci --no-audit --no-fund >/dev/null && netlify deploy --prod --site $SITE --dir dist --functions netlify/functions --message "upvote export for the Cloudflare move")
sleep 20
curl -sf --retry 5 --retry-delay 10 "https://omarchyapps.com/api/votes-export?key=$KEY" > data/votes-export-$(date +%F).json
git worktree remove --force "$W"
python3 - <<'PY' > /tmp/votes-import.sql
import json, glob
rows = json.load(open(sorted(glob.glob("data/votes-export-*.json"))[-1]))["rows"]
print("DELETE FROM votes WHERE voter LIKE 'netlify-count-%';")
for r in rows:
    _, app, voter = r["key"].split("/")
    print(f"INSERT OR IGNORE INTO votes (app, voter, at) VALUES ('{app}', '{voter}', '{r['value']}');")
print(f"-- {len(rows)} votes")
PY
npx wrangler d1 execute omarchyapps --remote --file /tmp/votes-import.sql
echo "imported; now check https://omarchyapps.modecandsllc.workers.dev/api/votes"
