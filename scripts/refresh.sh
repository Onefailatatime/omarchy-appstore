#!/bin/zsh
# Twice-daily refresh: rebuild the store from pkgs.omarchy.org, run the tests,
# deploy to Cloudflare, and commit the refreshed catalogue so the repo matches
# what is live. Installed as the launchd job com.omarchyapps.refresh.
set -euo pipefail
export PATH="/Users/funnelfix/.nvm/versions/node/v22.22.0/bin:/opt/homebrew/bin:/usr/bin:/bin"
cd /Users/funnelfix/omarchy-appstore
echo "== $(date -u +%FT%TZ) refresh start"
git pull -q --ff-only origin main
python3 build.py
npm test
npx wrangler deploy
git add dist data/omarchy.db data/page-dates.json src/app-names.mjs src/checklist.mjs
git diff --cached --quiet || git commit -qm "Refresh package catalogue from pkgs.omarchy.org"
git push -q origin main
echo "== $(date -u +%FT%TZ) refresh done"
