# The Postiz playbook: how Nevo David built and grew an open-source scheduler with a paid cloud (2023 to 2026), plus comparable OSS-plus-cloud indie stories

Research date: 2026-10-11. All revenue figures below are founder-self-reported unless stated otherwise; none has been independently audited. "SR" = self-reported by the founder.

## Key question 1: Postiz star count over time (launch, 1k, 10k, current) and the events that drove each jump

### Takeaway
The repo was created 2023-07-08 as "Gitroom" (an open-source launch/growth tool for OSS maintainers), was repositioned as "Postiz" around 2024-09-01, reached ~14k stars by 2024-12-02 (SR), ~25k by early 2026, 33.9k on 2026-07-29 and 37,048 on 2026-10-11. The biggest single spike was the 2024-11-20 Product Hunt launch (898 votes, #1 of the day) plus the same-day Show HN (42 points), which put the repo at #1 on GitHub Trending on 2024-11-23.

### Cited Findings
- Repo `gitroomhq/postiz-app` was created 2023-07-08T17:24:22Z (GitHub API, queried 2026-10-11 via `gh api repos/gitroomhq/postiz-app`); star-history.com also shows "Created: July 8, 2023" — [Star History](https://www.star-history.com/gitroomhq/postiz-app)
- Gitroom, the predecessor, was "an open source platform created by Nevo David, the former head of growth at Novu" to help OSS maintainers schedule posts/articles, swap posts with influencers, and generate star-stat media; profiled 2024-05-01 — [Open Pioneers newsletter](https://oss.beehiiv.com/p/gitroom)
- Nevo David's own account: Postiz was "created" on September 1, 2024 and "has grown to almost 14k stars" by the article date of 2024-12-02 (SR). He frames it as applying his Novu playbook: "I could replicate the same thing if I built my own open-source" — [dev.to, 2024-12-02](https://dev.to/nevodavid/i-built-an-open-source-social-media-scheduling-and-it-blew-up-415e)
- Hacker News launch sequence (hn.algolia.com API): "Show HN: I built a social media scheduling tool and open-sourced it" 2024-08-24 (2 points); Show HN 2024-08-30 (19 points, 7 comments); Show HN 2024-09-01 (2 points); Show HN 2024-09-06 (7 points); Show HN 2024-11-20 (42 points, 4 comments, the best result); further Show HNs 2024-12-09, 2024-12-12, 2024-12-18; "Postiz Introduces MCPs" 2025-04-15; "Show HN: Schedule posts to social media with AI Agent CLI" 2026-02-14 — [HN Algolia search](https://hn.algolia.com/api/v1/search?query=postiz&tags=story)
- Product Hunt launch 2024-11-20: 898 votes, ranked #1 of that day's 30 listed products (next was SocLeads at 696) — [aitoolly PH daily 2024-11-20](https://aitoolly.com/nl/producthunt-daily/2024-11-20); Postiz's own launch announcement — [postiz.com/news](https://postiz.com/news/postiz-is-on-product-hunt). Nevo claims "1st product of the day/week/month" and "more than 2,000 voters" (SR; the aggregator shows 898, so the 2,000 figure likely counts later votes or is inflated) — [dev.to](https://dev.to/nevodavid/i-built-an-open-source-social-media-scheduling-and-it-blew-up-415e)
- GitHub Trending Global Rank #1 reached 2024-11-23, three days after the PH/HN launch — [Star History](https://www.star-history.com/gitroomhq/postiz-app)
- ~25k stars paired with ">$17,000 MRR" in an early-2026 news item — [Munich Startup insights](https://insights.munich-startup.de/news/feed/open-source-saas-founder-grows-postiz-to-17k-month-with-25k-github-stars)
- 33.9k stars, Global Rank #925 on 2026-07-29 — [Star History (search snapshot)](https://www.star-history.com/gitroomhq/postiz-app)
- 37,048 stars, 7,181 forks on 2026-10-11 (GitHub API); star-history shows +359 stars in the week to 2026-10-11, Global Rank #864, 75 contributors — [Star History](https://www.star-history.com/gitroomhq/postiz-app); [GitHub repo](https://github.com/gitroomhq/postiz-app)
- Nevo's prior track record used as credibility: Novu reached 20,000 stars in a year while he was Head of Growth (GitHub20k launched on Product Hunt 2023-07-14) — [GitHub20k PH listing](https://webmail.hunted.space/product/github20k/launches/github20k); later cited as 31k stars in two years — [dev.to](https://dev.to/nevodavid/i-built-an-open-source-social-media-scheduling-and-it-blew-up-415e)

### Inferences
- Roughly 0 to 14k stars in three months (Sept to Dec 2024) was driven by a drumbeat of repeated Show HN posts (eight in four months), the PH day win, and the resulting Trending #1. After that the curve flattened: ~14k (Dec 2024) to ~25k (early 2026) to 37k (Oct 2026), i.e. ~1k/month, with a renewed uptick in 2026 when the agent/MCP/CLI pivot and the OpenClaw viral moment brought new traffic.
- Repo age matters: because the Gitroom repo was reused, the "created 3 years ago" date on trackers understates how fast Postiz itself grew.

### Gaps
- No source gives the exact dates Postiz crossed 1k, 10k, 20k or 30k stars; star-history.com renders this only as an unlabeled chart. The Munich Startup "25k" item is undated beyond "early 2026".
- The self-reported "2,000 voters" PH figure could not be reconciled with the 898-vote aggregator snapshot.

## Key question 2: Postiz cloud pricing and exactly which features are cloud-only versus self-hosted

### Takeaway
Postiz does not gate features: self-hosted installs run as the top tier with no limits. Cloud (four tiers, $29 to $99/month, 7-day trial, no free plan) sells convenience: pre-approved social-platform developer apps, metered AI image/video credits, hosting, updates and priority support. The founder now explicitly calls self-hosting "a secondary option".

### Cited Findings
- Pricing tiers (monthly / yearly-equivalent): Standard $29 / $23: 5 channels, unlimited posts, no team members, no AI images, 3 AI videos/mo, 60 AI clipping minutes. Team $39 / $31: 10 channels, unlimited team members, 100 AI images, 10 AI videos, 120 min. Pro $49 / $39: 30 channels, 300 images, 30 videos, 300 min. Ultimate $99 / $79: 100 channels, 500 images, 60 videos, 600 min. All tiers include AI Copilot, Smart Agent, picture editor, API, webhooks, MCP server, CLI, comments, repeated posts, cross-posting, plugs, analytics, RSS auto-post, signatures. "Postiz has a 7-day free trial on every plan." — [postiz.com/pricing](https://postiz.com/pricing)
- Pricing page states "Self-hosting is a secondary option; the hosted platform is where the agent features ship first" and offers obtaining your own social-media app approvals as an optional paid service — [postiz.com/pricing](https://postiz.com/pricing)
- README: "We do not 'gate' features or limit the license"; self-hosted is "Free forever (AGPL-3.0); you pay only for your own infra"; differences are AI (cloud quotas vs your own provider keys), social platform app approval, and support (priority vs community) — [GitHub README](https://github.com/gitroomhq/postiz-app)
- Cloud docs: "The difference is not the feature set." Cloud-only: plans/billing/invoices/affiliate programme, pre-registered provider developer apps, metered AI credits, 7-day trial, email+Discord support reaching the team, managed data and continuous updates, documented refund path. Self-hosted-only: "Every install behaves as the top tier, with no limits", effectively unlimited channels. "No free plan": without a subscription the cloud UI is replaced by the plan picker — [docs.postiz.com/cloud/overview](https://docs.postiz.com/cloud/overview)
- Third-party pricing pages broadly agree on the $29/$39/$49/$99 ladder — [Blotato](https://www.blotato.com/blog/postiz-pricing); [Mallary](https://mallary.ai/alternatives/postiz-pricing); one lists Standard as "400 posts per month", contradicting the official "unlimited" — [apis.io](https://apis.io/plans/postiz/postiz-plans-pricing/); another claims a free plan, contradicting the official docs — [thatmarketingbuddy](https://thatmarketingbuddy.com/pricing/postiz)
- In Dec 2024 the pitch was "Everything is 100% free (apache-2)! There is no weird license for enterprises or withholding SSO for enterprises." — [dev.to](https://dev.to/nevodavid/i-built-an-open-source-social-media-scheduling-and-it-blew-up-415e)

### Inferences
- The moat is not code, it is the painful part: platform API approvals (X, Meta, TikTok, LinkedIn developer apps) and AI credits. Self-hosters must register their own apps with each network, which is where most of the support tickets come from (see Q7).
- "Agent features ship first on hosted" (2026) marks a drift from the 2024 "everything is free" framing toward a soft open-core by release timing rather than by license.

### Gaps
- No official statement of how long the lag is between cloud and open-source releases of new agent features.

## Key question 3: Published revenue, user counts, or self-host install counts

### Takeaway
Postiz revenue (all SR) went from ~$350/mo in Sept 2024 to $6.5k (Jul 2025), $12.6k (Aug 2025), $14.2k (Nov 2025), a plateau around $17k (late 2025 to Feb 2026), then an agent-driven surge: ~$45k (Mar 2026), $118k (Jun 2026), $143k (Jul 2026), ~$170k (Aug 2026), $186,713 MRR / "$2.2M ARR" (Sept 2026, Stripe-profile screenshot). About 5,000+ active subscribers was cited mid-2026. No self-host install count has been published.

### Cited Findings
- Mixergy interview (published 2026-03-11): started "around September at about $350/month", plateaued at ~$17k then ~$20k, reached ~$45k/month after OpenClaw emerged, expecting ~$50k the following week; quote: "My revenue just exploded once I started sending to agents" (SR) — [Mixergy](https://mixergy.com/interviews/revenue-jumped-when-he-sold-to-ai-agents/)
- HN post by nevodavid10, 2025-11-28: "My SaaS jumped from $6,523 to $12,648 monthly, here is how" (SR) — [HN Algolia](https://hn.algolia.com/api/v1/search?query=postiz&tags=story)
- Indie Hackers post, Nov 2025: "My open-source company now makes $14.2k monthly as a single developer" (SR) — [Indie Hackers profile](https://www.indiehackers.com/nevos); a third-party profile dates the milestones as $6,523 (Jul 2025), $12,648 (Aug 2025), $14,200 (Nov 2025) — [onepage-research](https://onepage-research.sliplane.app/products/postiz)
- ">$17,000 MRR with 25k GitHub stars" (early 2026) — [Munich Startup](https://insights.munich-startup.de/news/feed/open-source-saas-founder-grows-postiz-to-17k-month-with-25k-github-stars)
- "My First Dollar" podcast (June 2026): grew Postiz "from $21K to $118K a month in three months, as the only person in the company" (SR) — [Apple Podcasts](https://podcasts.apple.com/us/podcast/id1896879547)
- Stork.ai (2026-07-30): $17k to $143k MRR in four months; churn fell from ~28% to 13.7%; a user's viral X post about Postiz + OpenClaw got 7.2M views and drove ~700 new trials/day; Nevo's own X article got ~500k views from a 200-follower account; he paid influencers $60 to $350 per repost; hired first developer and dedicated support — [Stork.ai](https://www.stork.ai/blog/17k-to-143k-mrr-the-agentic-pivot)
- Indie Hackers (IH+ paywalled) headline: "Growing an open-source product to $1.3M ARR in two years", snippet cites $113k MRR (SR) — [Indie Hackers](https://www.indiehackers.com/post/tech/growing-an-open-source-product-to-1-3m-arr-in-two-years-hbMiXIoZsueV9D3L58DP)
- Aggregator timeline (cites TrustMRR/PulseMRR): ~$170k-$173k MRR early Aug 2026, ~13.5% MoM growth, ~5,000+ active subscribers, $760k-$850k all-time revenue; also claims ~$14k/mo "late 2024", which conflicts with Nevo's own 2025 figures and should be treated as an error — [bestmillionstartups](https://www.bestmillionstartups.com/best/postiz-mrr-growth-story-what-founders-can-learn-2026)
- Postiz blog 2026-09-08: Stripe public profile shows $186,713 MRR, headline "$2.2M ARR"; revenue was flat "about two years" then climbed from early 2026; Nevo: "might be a little lucky there" (SR) — [postiz.com blog](https://postiz.com/blog/saas-marketing-strategy-chatgpt-astra-2-2m-arr)
- User count: only "thousands of creators and businesses" — [postiz.com blog](https://postiz.com/blog/saas-marketing-strategy-chatgpt-astra-2-2m-arr)

### Inferences
- For roughly 18 months (Sept 2024 to Feb 2026) ~25k stars translated to under $20k MRR, i.e. under $1 of MRR per star. The 10x in 2026 came from a buyer change (agents/automation users who churn less), not from more stars.
- Sources disagree on exact monthly figures but agree on shape: slow grind, plateau, step-change in Mar to Jul 2026.

### Gaps
- No self-host install count, Docker pull count, or cloud conversion rate from self-hosters has been published.
- The IH+ article and the Stork original are paywalled or secondary; the "$1.3M ARR" and "$113k MRR" snapshot date is unknown (probably ~May 2026).

## Key question 4: Nevo David's own explanations of what worked

### Takeaway
Nevo's stated playbook: (1) be the first fully open-source entrant in an old, crowded category; (2) post relentlessly where developers are (HN, Reddit, dev.to, PH, X) and ride hype topics early (MCP, agents, CLI); (3) treat GitHub as a growth channel; (4) in 2026, sell to AI agents via MCP/CLI/skills and use X long-form Articles plus paid reposts and UGC video for distribution.

### Cited Findings
- "Scheduling tools have existed for almost 20 years, but no open-source solution exists"; users asked "Please make another one open-sourced, and it exploded"; "The community grows so fast that I can handle it"; Discord bot that formats posts and nags him on unanswered messages (2024-12-02) — [dev.to](https://dev.to/nevodavid/i-built-an-open-source-social-media-scheduling-and-it-blew-up-415e)
- Gitroom era tactics (2024-05): scheduling articles to Reddit/DEV/Hashnode, exchanging or buying posts with influencers, "used by" sections swapped with other OSS founders — [Open Pioneers](https://oss.beehiiv.com/p/gitroom)
- GitHub20k newsletter (PH 2023-07-14): growth tactics "measured weekly, without relying on SEO or paid ads"; credits Novu's contributor community with indirectly bringing enterprise deals — [GitHub20k](https://webmail.hunted.space/product/github20k/launches/github20k)
- Mixergy (2026-03-11): open source as differentiator ("posts about open source got strong engagement"); hype-driven posts starting with MCP: "this is like a very easy way to attract people in"; built MCP integration early; had Claude convert the public API into a CLI and published a skill on ClawHub; "the CLI people that are going to build startups with a CLI are going to win big"; automated posting lowers churn — [Mixergy](https://mixergy.com/interviews/revenue-jumped-when-he-sold-to-ai-agents/)
- 2026-09 X article (100k+ views in a day, SR): principle "a person needs to see you many times before buying"; weekly X cadence (Monday value video, reply to everything, quote-post relaunches, convert to Article; an 84k-view video became a 204k-view article); daily UGC on Instagram/Facebook at 200 to 500 views each until one hits 200k+ (outliers 286k, 997k, 1.2M), creators paid $20 to $45/video; TikTok "person, conflict, reveal" slideshows (234k views); "Sell an outcome, not an alternative"; automate publishing but keep a human on engagement to avoid bans — [postiz.com blog](https://postiz.com/blog/saas-marketing-strategy-chatgpt-astra-2-2m-arr)
- Stork's distillation of Nevo's advice: build a public API, ship an MD file documenting it for agents, list in agent marketplaces (ChatGPT, Claude), build "before the trend happens", infrastructure must "just don't break" — [Stork.ai](https://www.stork.ai/blog/17k-to-143k-mrr-the-agentic-pivot)
- Ancillary repos used as launch surfaces: postiz-n8n (Show HN 2025-08-04), postiz-agent CLI (Show HN 2026-02-14) — [HN Algolia](https://hn.algolia.com/api/v1/search?query=postiz&tags=story)

### Inferences
- The "open-source marketing repo" tactic (GitHub20k, Gitroom) predates Postiz and is the same muscle: Nevo markets by publishing tools and newsletters about marketing.
- His 2026 growth is paid-amplified (influencer reposts, UGC creators), not purely organic, which is rarely emphasized in the "solo founder" framing.

### Gaps
- Could not access the IH+ article or Nevo's X threads directly (X not fetchable); his newsletter subscriber count and Discord size are not published anywhere found.

## Key question 5: License and how the project handles contributors versus the paid cloud

### Takeaway
Postiz shipped under Apache-2.0 (Gitroom era through Dec 2024) and switched to AGPL-3.0 on 2025-01-06. There is no CLA, no enterprise edition, and no gated code; the cloud is the same codebase run by Postiz with their platform credentials. Contributor volume is modest (75 contributors on 37k stars) and the maintainer has said low-quality PRs and docs gaps are a burden.

### Cited Findings
- LICENSE file history: commit ed684fa "Update LICENSE to AGPL3" on 2025-01-06T07:08:54Z; previous LICENSE commit 2024-03-11 (GitHub API `repos/gitroomhq/postiz-app/commits?path=LICENSE`, queried 2026-10-11). Current license AGPL-3.0 — [GitHub repo](https://github.com/gitroomhq/postiz-app)
- Dec 2024 statement: "Everything is 100% free (apache-2)!" — [dev.to](https://dev.to/nevodavid/i-built-an-open-source-social-media-scheduling-and-it-blew-up-415e). The aggregator claim that Postiz "open-sourced in September 2024 under AGPL-3.0" is therefore wrong on the license at that date — [bestmillionstartups](https://www.bestmillionstartups.com/best/postiz-mrr-growth-story-what-founders-can-learn-2026)
- 75 contributors, 3,319 commits, 135 open issues, 96 open PRs (2026-10-11) — [Star History](https://www.star-history.com/gitroomhq/postiz-app); [GitHub](https://github.com/gitroomhq/postiz-app)
- Maintainer on Lemmy (v1.35.1 post): "I agree documentation is lacking", "I haven't found enough motivation to update the missing thing", "It's also challenging to add providers" because of social-network approval processes, "I have seen some posts on the channels that it's hard to self-host postiz" — [Lemmy via scribe](https://scribe.disroot.org/post/1945251)
- A search-result summary of another maintainer update reports ~5-10 support tickets/day mostly from Portainer, Coolify and Unraid users, and difficulty maintaining the OSS side due to low-quality PRs and slow review (original post not retrieved; treat as unverified) — [search summary of Lemmy posts](https://scribe.disroot.org/post/1484614)
- README: "We do not 'gate' features or limit the license"; Cloud = "Hosted by Postiz; data stored in our infrastructure" — [GitHub README](https://github.com/gitroomhq/postiz-app)

### Inferences
- The Apache to AGPL move (one month after the PH/HN spike and 1.5 months before monetization began to show) is the standard anti-rehosting defence: it stops competitors from offering a closed hosted Postiz, while leaving self-hosters untouched.
- With no CLA, Postiz cannot relicense contributor code again without consent, which effectively locks it into AGPL or more permissive.

### Gaps
- No public CLA/DCO policy or contributor agreement found; no statement from Nevo explaining the AGPL switch.

## Key question 6: Common pattern across Postiz, Dub, Formbricks, Documenso, Cap, Papermark

### Takeaway
All six follow the same arc: viral launch post (X or HN) around an "open-source alternative to [incumbent]", AGPL or similar license plus an un-gated or lightly gated self-host, a hosted cloud that sells convenience and compliance, and revenue that lags stars by 12 to 24 months. Time to ~10k stars ranged from ~3 months (Postiz) to ~2 years (Formbricks, Papermark). Early MRR for the bootstrapped ones was $20k to $75k by month 18 to 24.

### Cited Findings
Repo facts (GitHub API, 2026-10-11): dubinc/dub created 2022-08-27, 24,877 stars; formbricks/formbricks created 2022-06-06, 13,081 stars; documenso/documenso created 2023-03-12, 15,395 stars, AGPL-3.0; CapSoftware/Cap created 2023-11-17, 23,221 stars; papermark/papermark created 2023-05-29, 9,244 stars; gitroomhq/postiz-app created 2023-07-08, 37,048 stars, AGPL-3.0.

Dub (Steven Tey):
- Started as an open-source URL shortener while Tey worked at Vercel; he left Vercel late 2023 and founded the company; $2M total raised from OSS Capital, Guillermo Rauch, Balaji Srinivasan, Framer founders, Soleio, Peer Richelsen; customers Twilio (hosted SaaS), Malaysian government (self-hosts the OSS), Huberman Lab; free plan exists; "Conversions" launched Jan 2025 — [TechCrunch 2025-01-16](https://techcrunch.com/2025/01/16/dub-co-is-an-open-source-url-shortener-and-link-attribution-engine-packed-into-one)
- "Almost 18K stars" on 2024-10-03; a top HN post drove early momentum; analytics "unlocked much higher ACVs" — [Open Source Startup Podcast ep.152](https://ossstartuppodcast.substack.com/p/episode-152-taking-on-bitly-with)
- No disclosed revenue; a $4.1M ARR estimate is modelled, not reported — [StartupHub](https://www.startuphub.ai/startups/dub)

Formbricks (Johannes Dancker, Matti):
- Started as Snoopforms, repositioned as "open source alternative to Qualtrics"; launch-week of one feature per day (Mar 2024); seeded community via oss.gg gamified contributions — [Open Pioneers 2024-03-20](https://oss.beehiiv.com/p/formbricks)
- "From zero to 4k GitHub in one year building a Typeform killer" — [Indie Hackers](https://www.indiehackers.com/post/from-zero-to-4k-github-in-one-year-building-a-typeform-killer-72ec1525ba); GitHub Accelerator 2023 cohort ($20k grant) — [Indie Hackers](https://www.indiehackers.com/post/our-open-source-project-got-funded-by-github-20k-eff00bcd98); [Formbricks blog](https://formbricks.com/blog/inaugural-batch-github-accelerator)
- Pre-seed 2023-11-01 from OSS Capital, Flex Capital, Peer Richelsen, angels (amount undisclosed) — [CB Insights](https://www.cbinsights.com/company/formbricks/financials); about page claims 11k+ stars and backing from Tom Preston-Werner — [formbricks.com/about](https://formbricks.com/about)
- Revenue from SaaS plus "paid variations" (enterprise edition) — [isitreallyfoss](https://isitreallyfoss.com/projects/formbricks). No MRR disclosed.

Documenso (Timur Ercan, Lucas Smith):
- $1.25M pre-seed announced 2023-08-17 (total $1.54M), OSS Capital joined; "Open Startup" policy of publishing financial KPIs — [Documenso blog](https://documenso.com/blog/pre-seed)
- First angel was Cal.com co-founder Peer; model is self-host, Documenso-hosted, or hybrid; advice: "launch early", wishes he had leaned harder into a grassroots movement; framing: signing should be open infrastructure like Let's Encrypt — [Open Pioneers 2024-07-24](https://oss.beehiiv.com/p/documenso)
- Bootstrapped/no public revenue figure per Latka — [GetLatka](https://getlatka.com/companies/documenso.com)

Cap (Richie McIlroy, Liverpool):
- "Open source alternative to Loom", Tauri/Rust desktop app, AGPLv3 + MIT, self-hostable; free tier capped at 5-minute recordings for personal use; Cap Pro $8.16/mo yearly vs Loom Business $18; enterprise lever is SOC 2 / ISO 27001 / HIPAA compliance; ~21k stars — [flaviocopes.com](https://flaviocopes.com/cap-business-model/); 19,228 stars on 2026-05-27 with slowing growth — [oosmetrics](https://oosmetrics.com/repo/CapSoftware/Cap)
- No revenue disclosed in any source found.

Papermark (Marc Seitz, Iuliia Shnai):
- "Started as a tweet" announcing an open-source DocSend alternative (~40k views in hours); weekend MVP, launch tweet ~100k views; ~$20k MRR year 1, ~$75k MRR (~$900k annualized) mid-year 2; 7,000 stars, 60 contributors, ~30,000 users (mostly free), ~1,000 paying; self-host free, hosted paid, advanced features need an enterprise license that can attach to self-host; costs ~80% people, ~15% marketing; "They just come to us because we do the best service in hosting the solution"; "You need to reach at least feature parity with the existing tools" (all SR, article 2025-08-16) — [Starter Story](https://www.starterstory.com/stories/how-we-built-it-900k-open-source-saas)
- Earlier: $45k MRR "in a little over a year" after 11 failed products; both full-time from Jan 2024 — [Indie Hackers](https://www.indiehackers.com/post/after-11-failed-products-this-founder-hit-45k-mrr-in-a-little-over-a-year-xyRkxAsD8Rys7URjYd5d)

Postiz: see Q1 to Q5 (0 to ~14k stars in ~3 months; ~$17k MRR at month 17; $186k MRR at month 24, SR).

### Inferences
- Common launch sequence: (1) tweet or Show HN of "open-source alternative to X" to a dev audience; (2) repeated re-launches (Postiz did eight Show HNs; Formbricks did launch weeks); (3) Product Hunt once the repo already has momentum; (4) hosted cloud from day one or within months.
- Gating choice splits two ways: "no gating, sell ops/credentials/compliance" (Postiz, Cap, Dub's free plan) vs "enterprise edition license" (Formbricks, Papermark). Both keep the self-host free for individuals.
- Time to 10k stars: Postiz ~3 months (Sept to Dec 2024, SR); Dub ~2 years (Aug 2022 to ~2024); Cap ~1.5 years; Documenso ~2 years; Formbricks ~2.5 years; Papermark has not reached 10k after 3.5 years yet has the clearest bootstrapped revenue. Stars and MRR are weakly coupled.
- Common 2024-2026 investors/angels recur: OSS Capital (Dub, Formbricks, Documenso) and Peer Richelsen of Cal.com (Dub, Formbricks, Documenso), i.e. a distinct COSS indie ecosystem.
- Early MRR (bootstrapped): Papermark $20k at ~12 months and $75k at ~18 months; Postiz ~$14k at ~14 months and ~$17k at ~17 months. VC-backed Dub/Formbricks/Documenso do not disclose.

### Gaps
- No MRR or conversion figures for Dub, Formbricks, Documenso, or Cap. Documenso promised open metrics but current numbers were not surfaced.
- Rybbit, OpenStatus, Twenty were not researched for lack of tool budget.

## Key question 7: Criticisms: stars vs revenue, self-hoster support burden, cloud conversion rates

### Takeaway
Critics and the founders themselves agree that stars do not pay: Postiz sat at ~25k stars and <$20k MRR for over a year; a Cloudron maintainer concluded in Feb 2026 that "upstream is not really intending this to be a production ready selfhosted app" after Postiz added a Temporal server dependency; the founder admits weak docs and heavy provider-approval friction. No OSS-plus-cloud founder in this set has published a self-host to cloud conversion rate.

### Cited Findings
- Cloudron staff (2026-02-09): new Postiz versions require temporal-server, which would need its own backup/restore addon; "cannot be updated"; "pretty clear that upstream is not really intending this to be a production ready selfhosted app"; considering dropping the package. User nichu42 "suspects the project is about making money" and had hoped for an affordable option for nonprofits; by 2026-06-17 staff suggested forking as a community package — [Cloudron forum](https://forum.cloudron.io/topic/15047/plan-to-drop-postiz-package-from-cloudron)
- Maintainer admits "documentation is lacking", lost motivation to fix docs, providers hard to add due to network approvals, has seen posts "that it's hard to self-host postiz"; a commenter: "It took me an embarrassingly long time to figure out what this actually is" — [Lemmy via scribe](https://scribe.disroot.org/post/1945251)
- Unverified summary of a maintainer update: ~5-10 tickets/day mostly from Portainer/Coolify/Unraid users; low-quality PRs and slow review — [search summary](https://scribe.disroot.org/post/1484614)
- Pricing page now says "Self-hosting is a secondary option" — [postiz.com/pricing](https://postiz.com/pricing)
- Review aggregation: complaints about Docker-only deployment friction, missing bulk duplication, Instagram connection limits, higher-tier pricing — [postplanify](https://postplanify.com/postiz-reviews); a reviewer frames cloud and self-host as "effectively different purchases" and recommends self-hosting only when someone owns upgrades/backups/credentials — [gptprompts.ai](https://gptprompts.ai/postiz-review)
- Postiz's own account of two flat years then a 2026 spike, with Nevo's caveat "might be a little lucky there" — [postiz.com blog](https://postiz.com/blog/saas-marketing-strategy-chatgpt-astra-2-2m-arr)
- Stork attributes the 2026 jump largely to one user's 7.2M-view viral post and to paid influencer reposts ($60 to $350 each), i.e. a partly bought, partly lucky surge rather than a repeatable organic loop — [Stork.ai](https://www.stork.ai/blog/17k-to-143k-mrr-the-agentic-pivot)
- General critique: "weak direct correlation between star count and revenue"; 50k-star projects can struggle while 5k-star repos make millions; who stars matters more than how many — [Monetizely](https://www.getmonetizely.com/articles/what-role-should-github-stars-play-in-your-open-source-pricing-strategy-7cd11); cannibalization by self-hosters is often overstated because self-hosters "were never going to be paying customers" — [Monetizely](https://www.getmonetizely.com/articles/is-your-open-source-community-cannibalizing-your-saas-revenue-a-strategic-analysis)
- Claimed conversion benchmarks (2-5% dev tools, 5-10% infra, 15-20% enterprise) are attributed to Bessemer without a verifiable primary link — [Monetizely](https://www.getmonetizely.com/articles/whats-the-relationship-between-open-source-adoption-and-saas-revenue); a sales-pitch example of "5,000 stars, 3,000 Discord members, $0 MRR" — [Clarm](https://www.clarm.com/blog/articles/convert-github-stars-to-revenue)
- A different OSS social-tool founder, one month after open-sourcing (1.7k stars), made the hosted version free because self-hosters "are forcing the product to mature faster" while hosted removes the Docker blocker for agencies — [Indie Hackers](https://www.indiehackers.com/post/1-month-after-open-sourcing-my-social-media-tool-1-7k-stars-and-why-the-hosted-version-is-now-0-for-everyone-d8a4867720)
- Papermark's counter-view: self-hosters do convert "because we do the best service in hosting the solution" (SR, no rate given) — [Starter Story](https://www.starterstory.com/stories/how-we-built-it-900k-open-source-saas)

### Inferences
- The repeatable lesson for a 2025-2026 OSS-plus-cloud launch: stars buy distribution and credibility, not revenue; revenue came when the product found a buyer with a recurring automated workflow (agents for Postiz, compliance buyers for Cap, enterprise attribution for Dub). Expect 12 to 24 months at <$20k MRR even with a top-1% star curve.
- The self-host offer tends to degrade over time (Temporal dependency, "secondary option" language, cloud-first features) as the cloud matures; this is the most common complaint and a reputational cost to budget for.
- The 2026 Postiz surge is hard to replicate: it combined a new distribution surface (X Articles, agent marketplaces), a hype wave (OpenClaw), paid amplification, and a founder with an existing growth-marketing playbook.

### Gaps
- No founder in this set has published a self-host to cloud conversion rate or a support-cost figure; the "5-10 tickets/day" number is second-hand.
- Reddit r/selfhosted critique threads were not directly retrievable; HN comment threads on the Show HNs were not read (low comment counts: 4 to 7).
