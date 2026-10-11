-- Upvotes: one row per app and browser, mirroring the old Netlify Blobs keys
-- vote/<app>/<voter>. Rate limits replace Netlify's per-function limiter.
CREATE TABLE votes (
  app TEXT NOT NULL,
  voter TEXT NOT NULL,
  at TEXT NOT NULL,
  PRIMARY KEY (app, voter)
);
CREATE INDEX votes_voter ON votes (voter);

CREATE TABLE rate_limits (
  key TEXT PRIMARY KEY,
  count INTEGER NOT NULL,
  window_start TEXT NOT NULL
);
