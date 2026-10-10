-- Auction state for the sponsor slots on omarchyapps.com.
-- Slot configuration (reserves, increments, clocks) lives in data/ads.json and
-- is bundled into the Worker; this database holds only what visitors do.

CREATE TABLE slot_state (
  slot TEXT PRIMARY KEY,
  cycle INTEGER NOT NULL DEFAULT 1,
  status TEXT NOT NULL DEFAULT 'open',
  opened_at TEXT,
  closes_at TEXT,
  closed_at TEXT,
  extensions INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE bids (
  id TEXT PRIMARY KEY,
  slot TEXT NOT NULL,
  cycle INTEGER NOT NULL DEFAULT 1,
  amount INTEGER NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  verified_at TEXT,
  approved_at TEXT,
  decided_at TEXT,
  name TEXT NOT NULL,
  url TEXT NOT NULL,
  tagline TEXT NOT NULL,
  email TEXT NOT NULL,
  ip_hash TEXT,
  verify_hash TEXT,
  void_reason TEXT,
  payment_status TEXT NOT NULL DEFAULT 'unpaid',
  creative_status TEXT NOT NULL DEFAULT 'pending',
  mark TEXT,
  image TEXT
);
CREATE INDEX bids_slot_cycle_status ON bids (slot, cycle, status);
CREATE INDEX bids_email ON bids (email);
CREATE INDEX bids_verify ON bids (verify_hash);

CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  at TEXT NOT NULL,
  slot TEXT,
  bid_id TEXT,
  type TEXT NOT NULL,
  detail TEXT
);

CREATE TABLE rate_limits (
  key TEXT PRIMARY KEY,
  count INTEGER NOT NULL,
  window_start TEXT NOT NULL
);
