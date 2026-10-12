# Indiehacker tool stack and incumbent pricing (2025-2026)

All vendor prices below were read from the vendor's own pricing page on **2026-10-11** unless marked "third-party". Third-party figures are flagged and dated. Indie Hackers post pages returned HTTP 403 to the fetcher, so IH material comes from search-engine snippets of those posts and is marked "snippet".

## KQ1. Which tools appear most often in 2025-2026 "my stack" / "what I pay for" posts?

### Takeaway
Across the 2025-2026 stack posts and cost breakdowns found, the same ~10 names recur almost every time: Vercel (hosting), Supabase (DB + auth), Stripe (payments), Resend (transactional email), PostHog or Plausible (analytics), Sentry (errors), Cursor / Claude (AI coding), beehiiv or Kit (newsletter), Crisp or Intercom (support), Notion (docs). Categories that rarely appear as paid line items in these posts: changelog/feedback tools, status pages, link shorteners, testimonial tools, screen recorders, scheduling, forms.

### Cited Findings
- Prompts to Product "$1K MRR real numbers" (reviewed May 2026) itemises: Vercel Pro $25, Supabase Pro $25, Stripe fees $44, Resend Pro $20, Namecheap domain $1.25, Sentry $8, PostHog Free $0, ShipFast boilerplate amortised $25; total $148.25/mo — [Prompts to Product](https://www.promptstoproduct.com/saas-cost-at-1k-mrr)
- socialanimal.dev "SaaS MVP cost 2026" (Apr 2026, updated Aug 2026) stack is Clerk, Supabase, Stripe, PostHog, Vercel, Resend, Sentry, Cloudflare domain; at launch (~$2K MRR) total $171/mo (Supabase Pro $25, Stripe $60, Vercel Pro 2 seats $40, Resend Pro $20, Sentry Team $26) — [socialanimal.dev](https://socialanimal.dev/blog/saas-mvp-cost-2026/)
- Krispy "Indie Hacker Stack 2026" (May 2026): Cloudflare Workers, Supabase/Neon, Supabase Auth/Clerk, Resend, PostHog, Sentry/GlitchTip, Stripe/Lemon Squeezy, Krispy/Chatwoot support, Uptime Robot; total $0 on free tiers or ~$20-50/mo paid entry — [Krispy blog](https://blog.krispyai.com/indie-hacker-stack-2026)
- Superframeworks "Solopreneur AI stack 2026" (Mar 2026): Cursor Pro $20, Claude Pro $20, Supabase $0-25, Vercel $0-20, Resend $0-20, Stripe 2.9%+30c, ChatGPT/Claude $20, beehiiv $0-42, Canva Pro $13, Buffer free, Crisp $0-25, Make.com $0-16, PostHog free, Sentry free; total claimed $73-205/mo — [Superframeworks](https://superframeworks.com/articles/solopreneur-ai-stack-2026)
- tools8020 "8-tool 80/20 stack for solo founders" (May 2026): Notion Plus $10, Cursor Pro $20, Figma, Framer Mini $5, beehiiv Scale $42, Attio CRM, Cal.com, Plausible $9; article claims ~$116/mo paid though listed items sum to $86 — [tools8020](https://tools8020.com/blog/stack-for-solo-founders/)
- saasranger "Indie hacker tool stack" (Mar 2026): Lovable/Cursor $20, Supabase free then $25, Vercel free, Lemon Squeezy 5%+50c, Plausible $9, Resend free then $20, support (Plain/Intercom, Senja, Notion docs) ~ $20 combined; headline "under $20/mo before revenue" — [saasranger](https://saasranger.com/blog/indie-hacker-tool-stack-what-successful-solo-founders-actually-use/)
- IH post "The real monthly cost of running 14 SaaS products solo" (snippet, 2025-26): domains $15-25, hosting ~$0 (Supabase free tier for auth + DB), dev tools $30-50 (Lovable primary, Claude, occasionally Cursor), misc $10-20 — [Indie Hackers](https://www.indiehackers.com/post/the-real-monthly-cost-of-running-14-saas-products-solo-4611174aad)
- IH "$7k/mo side-project portfolio" (snippet): NextJS + Supabase + Claude Code; no dollar breakdown — [Indie Hackers](https://www.indiehackers.com/post/tech/this-full-time-data-scientist-built-a-7k-mo-portfolio-of-side-projects-quOo7AXtrGlePopsGslc)
- IH "From zero to $10k/mo app portfolio" (snippet): commenter notes AI tools cut monthly costs from $1k to $200 — [Indie Hackers](https://www.indiehackers.com/post/tech/from-zero-to-10k-mo-app-portfolio-in-a-year-71h2PPGYn1VnPOkj9qi6)
- IH "I killed my $50/mo Reddit marketing stack" (snippet): founder paid ~$50/mo across Reddit marketing tools before replacing with a free local app — [Indie Hackers](https://www.indiehackers.com/post/i-killed-my-50-mo-reddit-marketing-stack-and-built-a-free-local-tool-e77a94445a)
- dev.to "How I run my SaaS for $45/month, just Rails" (Jun 2025, Andres Urdaneta): Hetzner dedicated $13.49 + 2x shared $4.99, DigitalOcean Spaces $5.33, Zoho Mail $1, Postmark $15; total ~$45 — [dev.to](https://dev.to/untaught/how-i-run-my-saas-for-45month-without-supabase-vercel-or-firebase-just-rails-22pc)
- dev.to "Solo dev SaaS stack powering $10k/mo micro SaaS" (Aug 2025) names Firebase, Supabase, Stripe, Clerk, Resend, SendGrid, CleanShot, Tella, Vercel, Cloudflare Pages, OpenAI; no prices — [dev.to](https://dev.to/dev_tips/the-solo-dev-saas-stack-powering-10kmonth-micro-saas-tools-in-2025-pl7)
- Older but itemised: Waitlist founder stack (Dec 2022) totalled $281.32/mo, dominated by Ahrefs $99, Intercom $89, Vercel $40, Linear $10, Google Workspace $6, 1Password $2.99; most else $0 via credits — [dev.to](https://dev.to/getwaitlist/my-frugal-indie-dev-startup-stack-40b7)
- Older IH threads (snippets, pre-2025): "My monthly costs are $223" (Mailchimp $65, Transistor, Gumroad); "Which SaaS do you pay for" (one founder: template + domain + ~$20 AWS, first startup under $30/mo; another: ~$500/mo incl. Ahrefs, SurferSEO, Canva, Zoom, Google Workspace); "What tools do you use" lists Plausible $6/mo — [IH $223](https://www.indiehackers.com/post/my-monthly-costs-are-223-what-are-yours-bcea20aebd); [IH which SaaS](https://www.indiehackers.com/post/which-saas-do-you-pay-for-as-an-indie-hacker-131cca2b19); [IH tools](https://www.indiehackers.com/post/what-tools-do-you-use-to-run-your-service-product-ill-start-8c4f8e7398)
- Marc Lou (ShipFast) late-2024 newsletter: pays beehiiv $99/mo for ShipFast updates, Mailgun for transactional, moved new products to Resend — [ShipFast newsletter via search](https://shipfast.beehiiv.com/p/2-new-perks-just-dropped)
- Vercel overage complaints are a recurring IH theme: "must purchase the subscription for commercial usage ($20/month)"; one user got hit with ~$400 serverless charges after a traffic attack — [IH Vercel expensive](https://www.indiehackers.com/post/vercel-is-ridiculously-expensive-4d7bce8ca8); [MDX.one huge Vercel costs](https://www.indiehackers.com/product/mdx-one/huge-vercel-costs-and-rebrand-to-feather--Myc071NF66jYxLB2yED)

### Inferences
- Frequency ranking (by appearance in the ~10 2025-26 stack posts above): Vercel, Supabase, Stripe, Resend, PostHog, Cursor/Claude appear in nearly all; Plausible, Sentry, beehiiv, Crisp, Notion in about half; Clerk, Lemon Squeezy, Cal.com, Figma, Canva in a few. Changelog, feedback boards, status pages, link shorteners, testimonials, screen recorders essentially never show up as paid lines in the solo-founder cost posts, even though vendors in those categories charge $20-90/mo.
- The 2025-26 shift vs. 2022-era posts: AI coding subscriptions ($20-40/mo for Cursor + Claude/ChatGPT) are now the largest fixed line for pre-revenue founders, replacing SEO tools (Ahrefs) and support seats (Intercom) that dominated older lists.

### Gaps
- Could not fetch Reddit (r/SaaS, r/indiehackers, r/microsaas) threads directly; search engine returned no Reddit results for four query variants. No Reddit-sourced numbers are included.
- Could not find a 2025-26 Hacker News "Ask HN: what do you pay for" thread; only 2012 and 2015 HN threads surfaced.
- Indie Hackers pages 403'd; comment-level detail is unavailable.
- No X/Twitter "my stack" posts could be retrieved (no read tool for X available in this session).

## KQ2. Current pricing (2025-2026) for named incumbents

### Takeaway
Entry paid tiers cluster at $9-29/mo across categories; the tier a solo founder realistically lands on (needs custom domain, removes branding, or exceeds a free cap) is usually $20-60/mo per tool. Several formerly free/cheap tools have moved to higher entry points (Loops $49, Canny $79, Dub $90, beehiiv $49 annual, Screen Studio subscription-only).

### Cited Findings

**Analytics**
- Plausible (third-party, Seline, updated Aug 2026; plausible.io unreachable from fetcher): Starter ~$9/mo (10k pageviews, 1 site), Growth ~$14/mo (3 sites, 3 team members), Business ~$19/mo (10 sites, funnels, Stats API); no permanent free plan, 30-day trial; annual = 2 months free — [Seline](https://seline.com/blog/plausible-analytics-pricing); corroborated by [Motion Analytics](https://analytics.motion.dev/vs-plausible). Conflicting: Temperstack lists Growth $19 / Business $39 — [Temperstack](https://www.temperstack.com/plans/plausible/)
- Fathom (vendor, 2026-10-11): $15/mo up to 100k pageviews, $25 (200k), $45 (500k), $60 (1M), $100 (2M), $140 (5M), $200 (10M); yearly = 2 months free — [Fathom](https://usefathom.com/pricing)
- PostHog (third-party Usercall, verified May 2026; posthog.com unreachable from fetcher): free 1M events, 5K session recordings, 1M flag requests, 1,500 survey responses, 100K exceptions, 50GB logs per month; then $0.00005/event, $0.005/recording, $0.0001/flag request, decreasing with volume; no platform fee on pay-as-you-go — [Usercall](https://usercall.co/post/posthog-pricing)

**Transactional and newsletter email**
- Resend (vendor): Free $0 (3,000 emails/mo, 100/day); Pro $20 (50k) / $35 (100k); Scale from $90 (100k) to $1,150 (2.5M). Marketing (Broadcasts) free to 1,000 contacts, then Pro from $40 (5k contacts) to $650 (150k) — [Resend](https://resend.com/pricing)
- Loops (vendor page shows only free tier: 1,000 contacts, 4,000 sends/30 days; paid tiers behind JS slider) — [Loops](https://loops.so/pricing). Third-party (smtpedia, Sep 2026, reading the slider): $49 up to ~5k contacts, $99 (10k), $199 (25k), $249 (50k), $399 (100k); unlimited sends; monthly billing only — [smtpedia](https://smtpedia.com/platforms/loops-so/review/)
- Kit (ConvertKit) (vendor): Free $0 up to 10,000 subscribers; Creator $33/mo billed yearly ($390/yr) at 1,000 subs; Pro $66/mo (first-year promo $50/mo, $593 first year) at 1,000 subs; paid prices scale with list size — [Kit](https://kit.com/pricing)
- beehiiv (vendor): Free up to 2,500 subs; Lite $49/mo billed yearly (to 100k subs); Pro $95/mo billed yearly (to 250k); monthly prices not shown, yearly saves up to 20% — [beehiiv](https://www.beehiiv.com/pricing). tools8020 cites beehiiv "Scale $42/mo" (older plan name) — [tools8020](https://tools8020.com/blog/stack-for-solo-founders/)
- Buttondown (vendor): $0 for first 100 subscribers; feature add-ons $9/mo (tagging, paid subs, analytics, RSS), $29/mo (custom domain archives, multiple newsletters, automations), $79/mo (whitelabel, teams); subscriber-scaled base price not shown on page — [Buttondown](https://buttondown.com/pricing)

**Feedback / changelog**
- Canny (vendor): Free $0 (25 tracked users, 5 managers); Pro from $79/mo billed yearly (100+ tracked users, 10 managers); Business custom — [Canny](https://canny.io/pricing)
- Featurebase (vendor): Free (1 seat, no AI, unlimited conversations); Growth $29/seat/mo billed yearly + $0.49/AI resolution; Professional $59/seat; Enterprise $99/seat — [Featurebase](https://www.featurebase.app/pricing)
- Headway (vendor): Free (unlimited changelogs, widget, public page); Pro $29/mo (whitelabel, custom domain, integrations, private changelogs, scheduled publishing) — [Headway](https://headwayapp.co/)
- Beamer (vendor): Free (1,000 MAU, 1 teammate); Starter $59/mo ($49 yearly, 5k MAU); Pro $119 ($99 yearly, 10k MAU); Scale $299 ($249 yearly, 50k MAU); extra 5k MAU $50/mo — [Beamer](https://www.getbeamer.com/pricing)

**Support / chat**
- Crisp (vendor): Free (2 agents, 100 profiles); Mini $45/mo per workspace (4 agents, 5k profiles, $5 AI credits); Essentials $95 (10 agents, 50k profiles, 2 sub-inboxes); Plus $295 (20+ agents, 200k profiles); extra agent $10/mo; VAT not included — [Crisp](https://crisp.chat/en/pricing/)
- Intercom (vendor): Essential $29/seat/mo; Advanced $85/seat; Expert $132/seat; Fin AI $0.99 per resolution — [Intercom](https://www.intercom.com/pricing)

**Forms**
- Tally (vendor): Free (unlimited forms and submissions, 10MB uploads); Pro $24/mo (yearly = 2 months off); Business $74/mo — [Tally](https://tally.so/pricing)
- Typeform: vendor page fetch failed twice (no output). Gap.

**Testimonials**
- Senja (vendor): Free (15 testimonials); Starter $29/mo (unlimited testimonials, 3 forms, 1 project, 2 seats); Pro $59/mo (unlimited forms, 5 projects, 5 seats; +$10/project, +$5/seat); yearly = 2 months free — [Senja](https://senja.io/pricing)
- Testimonial.to (vendor): Free (10 text + 2 video); Starter $25/mo ($300/yr annual; unlimited text, 2 video, 1 space); Ultimate $50/space/mo ($600/yr); Ultimate+ $95/space/mo ($1,140/yr) — [Testimonial.to](https://testimonial.to/pricing)

**Links / shorteners**
- Dub (vendor): Business $90/mo (10k new links/mo, 250k tracked events); Advanced $300/mo (50k links, 1M events); Enterprise custom. No free or sub-$90 tier shown on page — [Dub](https://dub.co/pricing)
- Bitly (vendor): Free (5 links/mo); Core $10/mo annual only ($120/yr, 100 links); Growth $29/mo ($348/yr, 500 links); Premium $199/mo ($2,388/yr, 3,000 links) — [Bitly](https://bitly.com/pages/pricing)

**Uptime / status**
- Better Stack (vendor): 10 monitors and 1 status page included at $0; +50 monitors $25/mo ($21 yearly); additional status page $15/mo; custom CSS/JS $15/mo; password-protected page $50/mo; white-label, IP allowlist, SSO, custom sender domain each $250/mo per page; 1,000 subscribers included, +1,000 for $40/mo — [Better Stack](https://betterstack.com/pricing)
- Instatus (vendor): Starter free (15 monitors, 2-min checks, email alerts, public page, 200 subscribers); Pro from $20/mo (50 monitors, 30-sec, SMS, custom domain, 5,000 subscribers); Business price not listed (1,000 monitors, SAML); Enterprise custom — [Instatus](https://instatus.com/pricing)

**Scheduling**
- Cal.com (vendor): Free forever for 1 user (unlimited event types, calendars); Teams $12/user/mo billed yearly; Organizations $28/user/mo yearly; Enterprise custom — [Cal.com](https://cal.com/pricing)

**Social scheduling**
- Typefully: vendor pricing page returned nav only (no prices in HTML). Third-party Toolradar (verified Sep 2026): Starter $8/mo, Creator $19/mo ($12.50 annual), Team $39 or $49 (ambiguous); says Typefully "does not publish a public price list" — [Toolradar](https://toolradar.com/tools/typefully/pricing). Another listing (Jun 2026) shows Free / Pro $10 / Business $20 — [aiproductivity.ai](https://aiproductivity.ai/pricing/typefully/). Treat as unresolved.
- Hypefury (vendor): Flexible $6/mo (1 channel, +$6 per extra platform, 2 Tweetshots/day); Full $19/mo (all channels incl. Bluesky, Threads, LinkedIn, Instagram, TikTok; 5 Tweetshots/day; carousels, analytics) — [Hypefury](https://hypefury.com/pricing)

**Screen recording / video**
- Screen Studio (vendor): subscription only; Yearly $9/mo ("save 69%"), Monthly $29/mo; one-time licenses "no longer available for new purchases" — [Screen Studio](https://screen.studio/)
- Loom (vendor): Starter $0 (25 videos, 5-min cap, 720p); Business $18/user/mo (unlimited, 4K); Business + AI $24/user/mo; annual saves up to 17% — [Loom](https://www.loom.com/pricing)

**Payments**
- Stripe (vendor): 2.9% + 30c domestic cards; +1.5% international, +1% currency conversion, +0.5% manual entry; Billing pay-as-you-go 0.7% of volume (monthly plan from $620/mo on 1-yr contract); Tax Basic 0.5%/txn no-code or $0.50/txn API; Tax Complete from $90/mo — [Stripe](https://stripe.com/pricing)
- Lemon Squeezy (vendor): 5% + 50c per transaction, no monthly fee; email marketing free to 500 subscribers; extra fees possible outside US — [Lemon Squeezy](https://www.lemonsqueezy.com/pricing)
- Paddle (vendor): 5% + 50c per checkout transaction, no monthly fee; bespoke rates for high volume or sub-$10 products — [Paddle](https://www.paddle.com/pricing)

**Hosting**
- Vercel (vendor): Hobby $0 (1 seat, 1M CDN requests, 100GB transfer, 4h Fluid CPU, 1M function invocations; non-commercial, no overage purchases); Pro $20/seat/mo with $20 included usage credit, 10M CDN requests, 1TB transfer, overage pay-as-you-go; Enterprise custom — [Vercel](https://vercel.com/pricing)
- Netlify (vendor): Free $0 (300 credits); Personal $9/mo (1,000 credits, individual); Pro $20/mo flat for unlimited members (3,000 credits, ~$0.00667/credit); Enterprise custom — [Netlify](https://www.netlify.com/pricing/)
- Supabase (third-party, Makerkit 2026): Free (500MB DB, 50k MAU, 5GB egress, pauses after 1 week idle); Pro $25/mo incl. $10 compute credit, 8GB DB, 250GB egress — [Makerkit](https://makerkit.dev/blog/saas/supabase-pricing)

**Auth**
- Clerk (vendor): bills on Monthly Retained Users; Hobby free to 50k MRU; Pro $25/mo ($20 annual) with 50k MRU free then $0.02/MRU to 100k, $0.018 to 1M; Business $300/mo ($250 annual) — [Clerk](https://clerk.com/pricing)
- Auth0 (vendor): Free to 25,000 MAU; Essentials from $35/mo (B2C, 500 MAU) or $150/mo (B2B); Professional from $240/mo (B2C) or $800 (B2B); yearly = 11x monthly — [Auth0](https://auth0.com/pricing)

**Docs / PM**
- Notion (vendor): Free $0; Plus $10/member/mo; Business $20/member/mo; Enterprise custom — [Notion](https://www.notion.com/pricing)
- Linear (vendor): Free $0; Basic $10/user/mo billed yearly; Business $16/user/mo yearly; Enterprise custom, annual only — [Linear](https://linear.app/pricing)

**Other recurring lines in posts**
- Cursor Pro $20/mo; Claude Pro / ChatGPT Plus $20/mo — [Superframeworks](https://superframeworks.com/articles/solopreneur-ai-stack-2026)
- Sentry Team $26/mo; Uptime Robot $7/mo; Cloudflare Workers paid $5/mo; Railway Hobby $5/mo; Hetzner CAX11 EUR3.79/mo — [Krispy blog](https://blog.krispyai.com/indie-hacker-stack-2026); [socialanimal.dev](https://socialanimal.dev/blog/saas-mvp-cost-2026/)

### Inferences
- "Entry tier" vs. "tier you end up on": the free tiers of Resend, PostHog, Supabase, Clerk, Cal.com, Tally, Instatus, Better Stack and Headway are genuinely usable for a $0-5k MRR product. The categories where a solo founder is forced onto a paid tier quickly are: hosting (Vercel Pro $20 because Hobby bans commercial use), newsletter (beehiiv $49, Loops $49, Kit $33 once over free cap or needing automations), support chat (Crisp Mini $45, Intercom $29/seat), feedback boards (Canny $79, Featurebase $29/seat), link management (Dub $90), testimonial walls (Senja $29).
- The combined cost of buying one incumbent per "secondary" category (changelog $29 + feedback $29-79 + testimonials $29 + status page $20 + link shortener $29-90 + screen recorder $9-29 + social scheduler $19) is roughly $165-300/mo, which is more than the entire core infra stack ($45-170/mo) in the cost posts. This matches why those categories are absent from "what I pay for" lists: founders skip them, use free tiers, or self-build.

### Gaps
- plausible.io and posthog.com DNS lookups failed from this environment; figures are from third-party trackers dated Aug/May 2026 and should be re-verified.
- Typeform pricing page fetch failed twice; no figure recorded.
- Typefully publishes no HTML price list; third-party figures conflict ($8/19/39-49 vs $10/20).
- Loops and Buttondown hide subscriber-scaled prices behind sliders; Loops figures are third-party.
- beehiiv, Kit, Canny, Linear, Featurebase, Cal.com show annual-billing prices only; month-to-month rates not published on the pages fetched.

## KQ3. Self-reported total monthly tooling bill of solo founders at $0-5k MRR

### Takeaway
Pre-revenue founders report $0-50/mo (free tiers + domain), rising to roughly $115-175/mo at $1-2k MRR and $400-450/mo at $5k MRR once Stripe fees, Vercel/Supabase Pro, Resend Pro, Sentry and a support tool are added. AI coding subscriptions add a further $20-60/mo in most 2025-26 reports. Blog "rule of thumb" ranges ($100-500/mo) are consistent with the itemised cases.

### Cited Findings
- $1K MRR itemised: $148.25/mo total (or ~$115 excluding boilerplate and Sentry); $5K MRR projection $400-450/mo (Stripe ~$220, Vercel $30-50, Supabase $30-40, Resend $20, Sentry $26, support ~$25, PostHog ~$50) — [Prompts to Product](https://www.promptstoproduct.com/saas-cost-at-1k-mrr)
- Pre-launch $41/mo (Vercel Pro 2 seats $40 + domain); launch ~$2K MRR $171/mo; growth ~$15K MRR $606/mo, "Stripe fees become the dominant cost" — [socialanimal.dev](https://socialanimal.dev/blog/saas-mvp-cost-2026/)
- Stage model: $0 at zero revenue, $73-120 at $1K-10K MRR, $200-500 at $10K+ MRR — [Superframeworks](https://superframeworks.com/articles/solopreneur-ai-stack-2026)
- "$0-50/month" full stack with light self-hosting; "$0-20/month before paying customers" — [Krispy blog](https://blog.krispyai.com/indie-hacker-stack-2026)
- "Under $20/mo before any revenue"; at $1K/mo "$30-50" (text) vs $89 (table); at $5K/mo $70 (infographic) vs $334 (table); figures internally inconsistent — [saasranger](https://saasranger.com/blog/indie-hacker-tool-stack-what-successful-solo-founders-actually-use/)
- Solo founder running 14 SaaS products: ~$15-25 domains + ~$0 hosting + $30-50 dev tools + $10-20 misc, i.e. roughly $55-95/mo total (snippet) — [Indie Hackers](https://www.indiehackers.com/post/the-real-monthly-cost-of-running-14-saas-products-solo-4611174aad)
- Rails founder, no managed platforms: ~$45/mo total (Jun 2025) — [dev.to](https://dev.to/untaught/how-i-run-my-saas-for-45month-without-supabase-vercel-or-firebase-just-rails-22pc)
- Rule-of-thumb blog claims: "total monthly SaaS bill for most indie hackers: $100 to $500"; another claims "$200-500/month on tooling before $200 MRR" (unsourced marketing copy) — [vibrantsnap](https://www.vibrantsnap.com/blog/essential-indie-hacker-tools-build-launch); [alexcloudstar](https://alexcloudstar.com/blog/saas-pricing-indie-hackers-2026/)
- Platform-vendor claim: "average solopreneur spends $147.83/mo on subscription software" from analysis of 138,000 users (vendor sells bundled tools; page returned 403 on fetch, methodology unverified) — [Mewayz](https://mewayz.com/ug/blog/the-solopreneur-tech-budget-2026-average-monthly-software-spend-breakdown-1)
- Indie/bootstrap MVP "$50 to $250 per month to run" — [wearefounders.uk](https://www.wearefounders.uk/how-much-does-it-cost-to-start-a-saas-in-2026/)
- Portfolio outlier: 35-app solo portfolio at $77K/mo estimated (by the article author, not the developer) at $1,250-1,500/mo infra plus ~$2,200 Stripe fees — [buildmvpfast](https://www.buildmvpfast.com/blog/solo-developer-35-micro-saas-apps-77k-month-portfolio-2026)
- Non-US VAT uplift: "Supabase, Vercel, Clerk all charge VAT on top. A $25/month plan becomes ~$30" — [Prompts to Product via search](https://www.promptstoproduct.com/saas-cost-at-1k-mrr)
- Older datapoints for contrast: 2022 waitlist startup $281/mo (Ahrefs $99, Intercom $89, Vercel $40) — [dev.to](https://dev.to/getwaitlist/my-frugal-indie-dev-startup-stack-40b7); Buttondown founder (c. 2019-21) $869/mo mostly Mailgun, Heroku, Stripe — [Indie Hackers](https://www.indiehackers.com/post/how-much-does-it-cost-to-run-your-side-project-6811b201e5)

### Inferences
- At $0-5k MRR, payment processing (Stripe 2.9% + 30c) is the single largest variable line from about $2k MRR onward and overtakes all fixed tooling by $5k MRR. Fixed SaaS tooling (excluding Stripe and AI subs) sits around $70-150/mo across the itemised 2025-26 cases.
- Blog totals are mostly vendor/affiliate content and are internally inconsistent (saasranger, tools8020); the two most carefully itemised sources (Prompts to Product, socialanimal.dev) agree within ~15% at the $1-2k MRR point ($148 vs $171).

### Gaps
- No survey-grade dataset of solo-founder tooling spend exists in the sources found; all totals are single-founder anecdotes or blog estimates.
- No Reddit or 2025-26 HN self-reports retrievable.

## KQ4. Which categories do founders call "must pay" vs "nice to have"?

### Takeaway
Sources consistently treat hosting, database/auth, payments, transactional email and (increasingly) AI coding tools as unavoidable paid lines, while analytics, error tracking, support chat, feedback, changelog, status page, link shortener and testimonials are kept on free tiers, self-hosted, or dropped. No formal survey exists; this is a pattern across cost posts.

### Cited Findings
- Core/"must" lines in every itemised 2025-26 breakdown: hosting (Vercel Pro), DB/auth (Supabase Pro), payments (Stripe fees), transactional email (Resend Pro), errors (Sentry) — [Prompts to Product](https://www.promptstoproduct.com/saas-cost-at-1k-mrr); [socialanimal.dev](https://socialanimal.dev/blog/saas-mvp-cost-2026/)
- "Cursor Pro at $20/month is worth paying from day one" — [vibrantsnap](https://www.vibrantsnap.com/blog/essential-indie-hacker-tools-build-launch)
- PostHog "has a free tier that almost any pre-revenue indie hacker can stay on indefinitely" (kept free, not paid) — [builtthisweek](https://www.builtthisweek.com/blog/indie-hacker-tools-2025)
- Analytics kept at $0 (PostHog Free) even at $1K MRR in the itemised case; support tool only added at the $5K MRR projection (~$25) — [Prompts to Product](https://www.promptstoproduct.com/saas-cost-at-1k-mrr)
- Krispy stack pairs every secondary category with a $0 self-hosted alternative (PostHog self-hosted, GlitchTip for errors, Chatwoot for support, Unleash for flags) and says the support-only stack can be "under $5/month" — [Krispy blog](https://blog.krispyai.com/indie-hacker-stack-2026)
- "Misc Productivity tools can add up to about $150 a month through many small $10-30 subscriptions" (tool-sprawl warning) and "a surprising number of common tools charge $50-200/month for features a solo developer could replace" — [MicroGaps](https://www.microgaps.com/blog/overpriced-saas-tools-solo-devs-can-replace)
- Founder replaced a $50/mo Reddit marketing tool stack with a free local desktop tool (snippet) — [Indie Hackers](https://www.indiehackers.com/post/i-killed-my-50-mo-reddit-marketing-stack-and-built-a-free-local-tool-e77a94445a)
- "How my SaaS saves $100 a month with home-grown solutions" (dev.to, replacing paid tools with built-in code) — [dev.to](https://dev.to/lunchbag/how-my-saas-saves-100-a-month-with-home-grown-solutions-211n)
- Cancellation rationale from a 2025 subscription-audit post: "a feature or two is not enough added value to earn the money" — [jeradtech Substack](https://jeradtech.substack.com/p/apps-and-subscriptions-im-not-renewing)
- PlanetScale "no longer indie-hacker-friendly because the free tier is gone"; Supabase free projects "pause after 1 week of inactivity" cited as friction points that trigger switching — [builtthisweek](https://www.builtthisweek.com/blog/indie-hacker-tools-2025)
- Vercel Hobby plan prohibits commercial use, forcing the $20 Pro upgrade; overage risk cited as reason to leave — [IH Vercel expensive](https://www.indiehackers.com/post/vercel-is-ridiculously-expensive-4d7bce8ca8)
- Older itemised stacks show Ahrefs ($99) and Intercom ($89) as the biggest discretionary lines, and these are absent from 2025-26 breakdowns — [dev.to getwaitlist](https://dev.to/getwaitlist/my-frugal-indie-dev-startup-stack-40b7)

### Inferences
- "Must pay" (appears as a paid line in nearly every 2025-26 breakdown): hosting, DB/auth, payments processing, transactional email, AI coding assistant, domain. "Pay once revenue justifies it": support chat, error tracking paid tier, newsletter tool over free cap. "Nice to have / almost never paid for by solo founders at <$5k MRR": changelog, feedback board, status page, link shortener, testimonial collection, screen recorder, social scheduler, forms, scheduling. The last group is exactly where incumbents charge $20-90/mo, suggesting a price-expectation gap (founders expect $0-10 or a one-off) rather than lack of need.
- Stated reasons to drop a tool: per-seat pricing on a one-person team, forced upgrade for a single feature (custom domain, remove branding), free tier removal, usage-based overage surprises.

### Gaps
- No survey or poll explicitly asking founders to rank must-pay vs nice-to-have was found; classification above is inferred from what appears (or not) in cost breakdowns.
- Could not access Reddit or X, where this kind of "what did you cancel" discussion is most common.
