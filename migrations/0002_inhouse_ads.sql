-- In house ads (/ad1 to /ad20): daily counters per ad and page type, plus the
-- waitlist. Days are Pacific time (America/Los_Angeles) to match the recap.
CREATE TABLE ad_daily (
  day TEXT NOT NULL,
  ad INTEGER NOT NULL,
  page_type TEXT NOT NULL,
  impressions INTEGER NOT NULL DEFAULT 0,
  clicks INTEGER NOT NULL DEFAULT 0,
  views INTEGER NOT NULL DEFAULT 0,
  signups INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, ad, page_type)
);

CREATE TABLE waitlist (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  at TEXT NOT NULL,
  ad INTEGER NOT NULL,
  product TEXT NOT NULL,
  email TEXT NOT NULL,
  use_case TEXT NOT NULL DEFAULT '',
  who TEXT NOT NULL DEFAULT '',
  source TEXT NOT NULL DEFAULT '',
  UNIQUE (ad, email)
);
CREATE INDEX waitlist_at ON waitlist (at);
