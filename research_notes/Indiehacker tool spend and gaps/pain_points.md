# SaaS tools indie hackers and solo founders resent paying for (2025-2026): pain points, price-hike events, and open-source gaps

Research date: 2026-10-11. Method notes: Hacker News was queried directly via the Algolia API and individual threads were read; Reddit (reddit.com / old.reddit.com) and Indie Hackers (indiehackers.com) both block this agent's fetcher (HTTP 403 / blocked domain), so Reddit and IH sentiment below comes only via secondary write-ups that quote or link to those threads, and is flagged as such. GitHub issue pages for awesome-selfhosted returned 403/empty. The web-search budget ran out before Mailchimp, HubSpot, Buffer/Hypefury/Typefully, Senja and Canny could be covered in depth (see Gaps). Many pricing-comparison sources are vendor or competitor blogs; each is labelled where relevant.

Ranking of complaint categories by how often they recurred across the sources read (highest first):
1. Hosting / usage-based "denial-of-wallet" bills (Vercel dominates; also Cursor usage credits, Zapier task overages). Most dated incidents, most verbatim anger.
2. Price hikes with short notice that hit the smallest tiers hardest (Kit +34% Sept 2025; Figma up to +33% March 2025; Notion Business +33% 2025; Loom seat conversion + Jan 2026 hike; Cursor June 2025; Make Nov 2025).
3. Per-seat pricing that punishes 1-3 person teams (Figma Full seats, Loom viewer-to-paid-seat conversion, Zapier Team per-user, generic "seat-based pricing seems wrong").
4. Customer support / live chat (Intercom, Zendesk) called "very expensive", "constantly upsold", "prohibitive for small organizations".
5. Open-source rug-pulls removing the self-host escape hatch (Cal.com closed-source April 2026; Screen Studio lifetime licence removed Oct 2025).
6. Feature gating of branding removal / custom domain / A/B testing / AI behind higher tiers (Typeform, Tally, Kit, Notion, Loom, Figma).
7. Newsletter / email platforms (Kit, beehiiv, Mailchimp) -- strong but the only well-documented incident is Kit's.
8. Social scheduling (Buffer/Hypefury/Typefully), testimonials (Senja), feedback boards (Canny): complaints exist in aggregator reviews but no dated incident or strong primary quote was found (Gap).

---

## KQ1. Which named tools draw the most "too expensive for what it does" complaints from solo founders in 2025-2026?

### Takeaway
By volume and intensity of dated 2025-2026 complaints, the top targets are Vercel (surprise bandwidth/invocation bills), Cursor (June 2025 switch to usage credits), Intercom/Zendesk (per-seat plus per-resolution fees, "constantly upsold"), Zapier (task-based billing and overages), Kit (Sept 2025 hike at the 1k-subscriber tier), Figma (March 2025 seat restructure), Notion (AI folded into a $20 Business tier), and Loom (free seats converted to paid under Atlassian). Calendly, Typeform, Canny, Senja, Buffer-class tools generate "alternatives" content but few strong first-hand 2025-2026 quotes surfaced.

### Cited Findings

Vercel (hosting; usage pricing)
- Indie Hackers founder of MDX.one reported a Vercel bill of around $1.8k, about 5.6 TB of bandwidth at peak, moved duration-heavy API calls to Cloudflare Workers, and closed signups because they "couldn't afford the bill to keep growing" (paraphrase from search snippet; IH page itself returned 403) -- [Indie Hackers: Huge Vercel costs and rebrand to Feather](https://www.indiehackers.com/product/mdx-one/huge-vercel-costs-and-rebrand-to-feather--Myc071NF66jYxLB2yED)
- Vercel community, 17 June 2026: Pro-plan user hit by DDoS, >2 TB egress. Verbatim: "This caused my June invoice to spike from my usual $20-60 to $231.71." Support reportedly called usage charges "non-refundable"; poster "since added Cloudflare and enabled Spend Management, but the existing charges remain." -- [Vercel Community](https://community.vercel.com/t/ddos-attack-caused-170-in-extra-charges-support-refuses-refund/44044)
- HN, Sept 2026, "Zuck's bot increased our Vercel bill 10x" (7 pts, 7 comments): Meta's `meta-externalagent/1.1` crawler made >1M requests to a preview deployment; author says Vercel declined to ease the bill. Comments: speedgoose: "you realised that you are vulnerable to denial of wallet attacks without loosing that much money."; raunaksingwi: "Nobody should be able to make so many calls to your site that it results in 10x higher bill on your side."; author Marciok: "Vercel 'lets it sleep through' since they make money on these calls." -- [HN 49732873](https://news.ycombinator.com/item?id=49732873)
- X post surfaced on HN, 28 July 2025: "My vercel bill jumped from $300 a month to $3550 this month" -- [HN 44712921 linking to X](https://twitter.com/_mattwelter/status/1949850488654143932)
- Older but canonical: Cara (artist social app) hit with a $96k Vercel bill, June 2024 -- [HN 40612981 / X](https://twitter.com/zemotion/status/1798558292681343039); "Ask HN: Why is Vercel so expensive?" 1 April 2024 (12 pts, 23 comments), commenters moving to "cloud flare pages and workers" (moomoo11) and "a dockerized container to my VPS" (vunderba) -- [HN 39898391](https://news.ycombinator.com/item?id=39898391)
- Secondary blogs disagree on Vercel overage: one says $0.15/GB beyond 1 TB, others say $40 per additional 100 GB (a ~2.7x discrepancy; verify on vercel.com/pricing) -- [DeployWise](https://deploywise.dev/blog/vercel-billing-too-expensive); [ServerCompass](https://servercompass.app/blog/vercel-pricing-explained-hidden-costs)
- A self-hosting guide puts a solo founder's tool bill at "$110 and $250 per month once a second Vercel seat is added" (vendor-leaning source) -- [Cloudzy](https://cloudzy.com/blog/best-self-hosted-stack-indie-hackers/)

Cursor (AI IDE; usage credits)
- June 2025: Pro ($20/mo) moved from a fixed fast-request allowance to a $20 usage credit pool plus "unlimited" Auto; "unlimited" applied to Auto only. TechCrunch 7 July 2025: Cursor apologised for unclear changes. -- [TechCrunch via HN 44496285](https://techcrunch.com/2025/07/07/cursor-apologizes-for-unclear-pricing-changes-that-upset-users/); [Simon Willison 5 July 2025](https://simonwillison.net/2025/Jul/5/cursor-clarifying-our-pricing/)
- Timeline write-up: refunds "for the most egregious cases"; "One team's $7,000 annual subscription was reportedly depleted in a single day of normal usage"; some users reported daily charges of $10-$20; r/cursor user 'eraoul' went "from evangelist to recommending Claude Code and Windsurf"; alternatives named: Claude Code, Windsurf, Continue.dev. No hard cancellation counts anywhere. -- [WeAreFounders timeline](https://www.wearefounders.uk/cursors-pricing-disaster-the-full-timeline-of-how-an-ai-coding-darling-burned-its-most-loyal-users/)
- HN comment, 2 Jan 2026 (brettgriffin, quoting an article on solo dev usage costs): "is there a 'solo dev building absurdly large systems' discount tier I'm missing?" -- [HN 46467738](https://news.ycombinator.com/item?id=46467738)
- May 2026: plans restructured to Hobby / Individual $20 / Teams $40 per user / Enterprise; June 2026 "Cursor cuts prices, adds enterprise spend controls amid 'tokenomics' reckoning" -- [The New Stack via HN 48430227](https://thenewstack.io/cursor-pricing-token-billing/)

Intercom / Zendesk (support chat; per-seat + per-resolution)
- HN 13 Oct 2025 (rhubarbtree, "Ask HN: What are you working on?"): Intercom "is also very expensive and constantly upsold, despite being rubbish"; says Chatwoot "haven't done a great job" as the OSS alternative -- [HN 45565815](https://news.ycombinator.com/item?id=45565815)
- HN 28 Feb 2026, Show HN Opencom (open-source Intercom alternative): built because of Intercom's "complex and expensive pricing model or their frequent layout and UX changes" (jackjayd) -- [HN 47194407](https://news.ycombinator.com/item?id=47194407)
- HN 15 June 2026 on Salesforce acquiring Fin/Intercom (jmuguy): "for a product like Intercom, that is very expensive, they get eaten alive by smaller SaaS + in-house AI agent." -- [HN 48541316](https://news.ycombinator.com/item?id=48541316)
- Show HN Libredesk, 24 Feb 2025 (376 pts, 75 comments): author: "I built this because I wanted a truly open and self-hosted alternative to platforms like Chatwoot, Intercom, and Zendesk." Commenter OldMatey: Zendesk is "SO expensive and the pricing tiers and cost structures are prohibitive for many small organizations"; teruakohatu: paid options "had high costs even on the most basic plans." -- [HN 43158166](https://news.ycombinator.com/item?id=43158166)
- Intercom pricing structure (vendor/competitor sources): Essential $29/seat/mo annual or $39 monthly, plus $0.99 per Fin AI resolution; Spur (competitor) claims most businesses end up at "$600-2,000+ monthly" with add-ons -- [Voiceflow](https://www.voiceflow.com/articles/intercom-pricing); [Spur (competitor)](https://www.spurnow.com/blogs/intercom-pricing); Capterra reviewer: "its pricing is very high so that for early startups it is very hard to afford it" -- [Capterra](https://capterra.com/p/134347/Intercom/pricing/)
- Older (approx. 2023) Indie Hackers thread comment: Intercom "far too expensive for simple chat", Chatwoot works instead (via search snippet; IH blocked) -- [IH: Which SaaS do you pay for](https://www.indiehackers.com/post/which-saas-do-you-pay-for-as-an-indie-hacker-131cca2b19)

Zapier / Make (automation; task pricing)
- HN 2 Dec 2025 (cv_h): "Zapier is cloud-only and expensive at scale." -- [HN 46121394](https://news.ycombinator.com/item?id=46121394)
- Consultant note (Rafal Fila, 14 client accounts): 9 of 14 clients exceeded their task allocation within three months; overage billed at ~1.25x base task rate; Professional from $29.99/mo monthly or ~$19.99 annual, Team ~$69/user/mo annual (as of July 2026) -- [AutomationAtlas](https://automationatlas.io/answers/zapier-pricing-changes-2025-2026/)
- Anecdote (low-authority blog): a Professional plan "$49/month for 2,000 tasks rose to $249/month" after adding AI actions and a premium app -- [Neura.market](https://www.neura.market/blog/zapier-pricing-2026-is-it-still-worth-it-a-forward-looking-analysis)
- Make raised prices Nov 2025: "was $9/$16/$29/$59, now $12/$21/$38" (comparison-site claim) -- [Cut The SaaS](https://cut-the-saas.com/guides/make-vs-zapier-vs-n8n)
- n8n self-hosted Community Edition is free; cloud $20-$50/mo -- [ShippedSolo](https://shippedsolo.com/blog/zapier-vs-make-vs-n8n/)

Kit (formerly ConvertKit; newsletters)
- Price rise 8 Sept 2025: Creator plan at 1,000 subs $29 -> $39 (+34%); 10k tier $119 -> $139; existing accounts billed new price from first bill after 15 Oct 2025; free plan to 10k subs unchanged. Competitor EmailOctopus: "It for sure is going to hit many small creators and businesses who are working on a tight budget." -- [EmailOctopus (competitor), 9 Sept 2025](https://emailoctopus.com/blog/kit-formerly-convertkit-price-hike); [PassiveKit price history](https://www.passivekit.com/?p=629)
- beehiiv (competitor): "The September 2025 price increase stung", "around 35% across the board" -- [beehiiv blog](https://www.beehiiv.com/blog/best-kit-alternatives-for-growing-your-audience)
- Kit charges 3.5% + $0.30 on digital product sales on all plans including free (vendor-leaning source; verify) -- [TheFrontKit](https://thefrontkit.com/blogs/convertkit-alternatives-2026)
- beehiiv's own pain points: Scale plan ($99/mo) "can feel steep for early-stage newsletters"; "You even have to be on a more expensive plan to get priority support" (creator quote) -- [Dev.to beehiiv alternatives](https://dev.to/onsen/beehiiv-alternatives-competitors-2026-42lo); [Skipblast newsletter](https://skipblast.beehiiv.com/p/going)

Figma (design; seats)
- March 2025 restructure to Full/Dev/Collab/View seats; Professional $15/mo -> Full seat $20/mo ($16 annual); Organization $45 -> $55; Dev/Collab seats exclude Figma Design so design access forces a Full seat -- [PixelFounder, 13 Dec 2024](https://pixelfounder.substack.com/p/navigating-figmas-new-pricing-landscape); [UserJot](https://userjot.com/blog/figma-pricing-2025-plans-seats-costs-explained)
- Reddit quote relayed by a secondary source (could not verify on Reddit): "I love Figma but holy shit does their pricing strategy suck. 22% raise is SIGNIFICANT money." -- [via search summary of SaaS CRM Review / Pricing SaaS newsletter](https://newsletter.pricingsaas.com/p/inside-figmas-pricing-evolution)

Notion (docs; AI bundling)
- May/June 2025: AI add-on discontinued and bundled into Business at $20/user/mo (Business "33% increase from $15 -> $20"); Plus users get a 20-response one-time AI trial; sources conflict on effective date (June vs 13 Aug 2025) -- [SaaS Price Pulse](https://www.saaspricepulse.com/blog/notion-pricing-history); [Docsie comparison](https://www.docsie.io/solutions/vs/notion-vs-readme-pricing/)
- HN 28 Sept 2026 (baxtr, general): "The whole notion of seat-based pricing seems wrong to me as well." -- [HN 49876704](https://news.ycombinator.com/item?id=49876704)

Loom (async video; seats)
- Atlassian integration eliminated the free "Creator Lite" seat; those users auto-converted to paid Creator seats ($15-$24/user/mo); "A workspace with 10 recorders and 90 watchers used to pay for 10 seats. It now pays for 100." Free Starter plan remains (25 recordings, 5-min cap). A LinkedIn CS leader cancelled Loom over it (no verbatim). -- [SaaStr](https://saastr.com/atlassian-just-deleted-looms-free-seats-it-was-also-looms-distribution)
- 27 Jan 2026: top plan $15 -> $20/user/mo (+33.3%) per tracker; other sources list $18/$24 monthly -- [CostBench](https://costbench.com/changelog/loom-price-increase-2026-01/)

Screen Studio (screen recording; licence model)
- 1 Oct 2025: $229 lifetime licence (1 yr updates) removed for new buyers; subscription only (~$9/mo annual, $20-29 monthly). Founder said the $229 tier "was a mistake with low adoption" and the team is bootstrapped, five people. "Some users described the move as misleading." Alternatives users pointed to: Cap (OSS), Screenity (OSS), Screen Sage, Canvid (lifetime). -- [AlternativeTo news, 1 Oct 2025](https://alternativeto.net/news/2025/10/screen-studio-has-removed-their-non-subscription-licensing-options-for-new-customers/)

Framer (site builder)
- 9 Oct 2025 repricing: Basic $15 -> $10 but pages 1,000 -> 30; Pro $30; Scale $200 -> $100; Mini and Launch plans dropped. Reddit r/framer thread "Searching for Framer Alternatives after recent Price Changes": author with ~15 clients said "with the new pricing structure their costs will increase something like 400%." (relayed by a vendor blog; Reddit not directly verified) -- [Awesomic](https://www.awesomic.com/blog/framer-alternatives); [Reddit thread URL](https://www.reddit.com/r/framer/comments/1odbsyj/searching_for_framer_alternatives_after_recent/)

General SaaS fatigue (HN)
- "Ask HN: The Future of SaaS", 17 Apr 2025 (zer8k): "I, personally, am so sick of everything being a subscription"; "SaaS vendors to me are without a doubt vultures." -- [HN 43717288](https://news.ycombinator.com/item?id=43717288)
- HN "AI is killing B2B SaaS" (2026): a commenter said one vendor quadrupled prices after acquisition; another described a licence raising price 5-10% yearly (anecdotes) -- [HN 46888441](https://news.ycombinator.com/item?id=46888441)

### Inferences
- Solo-founder resentment clusters on tools whose bill can move without the founder doing anything: metered hosting (Vercel), metered AI (Cursor), metered automation (Zapier), and seat conversions (Loom, Figma). Flat-fee tools (Carrd $19/yr) attract almost no complaints.
- Intercom-class support tooling is the category with the most explicit "built an OSS alternative because of price" launches on HN in 2025-2026 (Libredesk Feb 2025, Opencom Feb 2026), and the most explicit dissatisfaction with the existing OSS option (Chatwoot).
- The enterprise vs solo split: Vercel's "low/mid five figures" enterprise plans and Figma Organization annual-only are enterprise complaints; the $20->$231 DDoS invoice, Kit $29->$39, Framer 15-client agency, and Loom 10/90 seat example are small-operator complaints.

### Gaps
- Reddit (r/selfhosted, r/SaaS, r/indiehackers, r/microsaas) and Indie Hackers are blocked for this fetcher; all Reddit/IH material here is second-hand.
- No strong 2025-2026 first-hand complaints were found for Calendly, Typeform, Canny, Senja, Buffer, Hypefury, Typefully, Carrd, Webflow, Mailchimp or HubSpot; the HN comment search for "Calendly Typeform expensive" (2025+) returned zero hits. Search budget ran out before targeted searches on Mailchimp/HubSpot/Buffer/Senja/Canny.
- No X/Twitter sentiment was retrievable beyond two Vercel-bill posts that were submitted to HN.

---

## KQ2. Which price-hike or plan-change events in 2024-2026 caused visible migration to alternatives?

### Takeaway
The best-documented migration-causing events are: Cursor's June 2025 usage-credit switch (users publicly moving to Claude Code / Windsurf; CEO apology), Kit's 8 Sept 2025 hike (an ecosystem of "leave Kit" content from beehiiv/EmailOctopus/MailerLite), Cal.com going closed source 15 Apr 2026 (self-hosters announcing migration in a 391-point HN thread), Screen Studio dropping lifetime licences (Oct 2025; users naming Cap/Screenity), Figma's March 2025 seat restructure, Loom's seat conversion and Jan 2026 hike, Notion's 2025 AI bundling, Framer's Oct 2025 repricing, and Make's Nov 2025 increase. Hard migration numbers do not exist for any of them.

### Cited Findings
- Cursor, June 2025 -> apology 7 July 2025 -> Teams pricing change 15 Sept 2025 -> May 2026 restructure -> June 2026 price cuts and spend controls -- [TechCrunch](https://techcrunch.com/2025/07/07/cursor-apologizes-for-unclear-pricing-changes-that-upset-users/); [Cursor Aug 2025 pricing post](https://cursor.com/en/blog/aug-2025-pricing); [The New Stack June 2026](https://thenewstack.io/cursor-pricing-token-billing/); migration targets Claude Code, Windsurf, Continue.dev -- [WeAreFounders](https://www.wearefounders.uk/cursors-pricing-disaster-the-full-timeline-of-how-an-ai-coding-darling-burned-its-most-loyal-users/)
- Kit, 8 Sept 2025, existing users had ~36-38 days before new price applied (15 Oct 2025); "many users criticized the short transition window" -- [EmailOctopus](https://emailoctopus.com/blog/kit-formerly-convertkit-price-hike); [PassiveKit](https://www.passivekit.com/?p=629)
- Cal.com, 15 Apr 2026: LICENSE replaced in commit "feat: Cal.diy - community-driven MIT-licensed fork", repo renamed calcom/cal.diy; Cal.diy lost Teams, Organizations, Workflows, Insights, SSO/SAML; README: "strictly recommended for personal, non-production use". HN thread 391 pts / 317 comments. opem: "For real, one of the reasons I use cal.com is because it's open source. Time to migrate."; lrvick: "Same. I expect in a misguided effort to save customers, they are going to lose a lot more."; gouthamve: "I feel like this is more a business decision than a security decision."; fhn: "Blaming AI is just an excuse to close source." Thunderbird Appointment's lead (ryanleesipes): "Our scheduling tool, Thunderbird Appointment, will always be open source." -- [HN 47780456](https://news.ycombinator.com/item?id=47780456); [Cal.com announcement](https://cal.com/blog/cal-com-goes-closed-source-why); [It's FOSS](https://itsfoss.com/news/cal-com-goes-proprietary.md); [Implicator.ai, 15 Apr 2026](https://www.implicator.ai/cal-com-goes-private-as-self-hosted-calendly-choices-narrow-in-2026/)
- Secondary coverage claims "the r/selfhosted thread is full of people asking for alternatives" (unverified; Reddit blocked) and quotes a self-hoster: "using opensource as GTM strategy, to get developer contribution, traction and then say fuckoff" -- [WhyOps](https://whyops.com/blog/cal-com-closed-source); [Sacra](https://sacra.com/chat/h/f931b58f-990b-4e26-913c-65f99df50172/)
- Screen Studio, 1 Oct 2025, lifetime licence removed; alternatives named by users: Cap, Screenity, Screen Sage, Canvid -- [AlternativeTo](https://alternativeto.net/news/2025/10/screen-studio-has-removed-their-non-subscription-licensing-options-for-new-customers/)
- Figma, 11 March 2025 seat restructure; "forum and G2 feedback shows real frustration, especially from smaller teams who don't use FigJam or Slides" -- [Pricing SaaS newsletter](https://newsletter.pricingsaas.com/p/inside-figmas-pricing-evolution); [UserJot](https://userjot.com/blog/figma-pricing-2025-plans-seats-costs-explained)
- Loom: Creator Lite seat removal (2025) and 27 Jan 2026 +33% on top plan -- [SaaStr](https://saastr.com/atlassian-just-deleted-looms-free-seats-it-was-also-looms-distribution); [CostBench](https://costbench.com/changelog/loom-price-increase-2026-01/)
- Notion: AI bundled into Business $20/user, 2025 (effective date disputed) -- [SaaS Price Pulse](https://www.saaspricepulse.com/blog/notion-pricing-history)
- Framer 9 Oct 2025 repricing; June 2026 Scale retired, editor seats $40 -> $20 (single-source claim) -- [Oma-kase](https://www.oma-kase.com/blog/framer-vs-webflow-pricing-2026-guide); [Awesomic](https://www.awesomic.com/blog/framer-alternatives)
- Make.com Nov 2025 increase ($9/$16/$29 -> $12/$21/$38) -- [Cut The SaaS](https://cut-the-saas.com/guides/make-vs-zapier-vs-n8n)
- Zapier: AI steps, code and SDK now follow task-based pricing; one site claims AI steps charged as tasks from 15 June 2026 (unconfirmed on Zapier's materials) -- [Zapier pricing](https://zapier.com/pricing); [AutomationAtlas](https://automationatlas.io/answers/zapier-pricing-changes-2025-2026/)
- Vercel: not a price hike but a steady drumbeat of bill-shock posts (June 2024 Cara $96k; July 2025 $300->$3550; June 2026 DDoS $231; Sept 2026 Meta crawler 10x) -- see KQ1 citations.

### Inferences
- Migration is most visible when (a) the change hits the entry tier and (b) a credible OSS or cheaper substitute already exists (Cursor -> Claude Code; Kit -> beehiiv/MailerLite; Screen Studio -> Cap). Where no substitute exists (Figma), complaints do not become migration.
- Cal.com is unique: the event removed the alternative rather than raising a price, which is why the thread is dominated by "where do we go now" rather than "cancel".

### Gaps
- No source gives churn or migration counts for any event; all "exodus" language is journalistic.
- Cursor's exact June 2025 change date (16 June is widely repeated but not confirmed in the primary sources read).

---

## KQ3. Most-upvoted "is there a self-hosted alternative to X" requests on r/selfhosted and HN in 2025-2026, and which still have no good answer?

### Takeaway
On HN (Algolia, 2025-2026), the loudest "alternative to" signals are Show HN launches of OSS alternatives rather than asks: Files.md (Obsidian, 730 pts), Pangolin (Cloudflare Tunnels, 500), Libredesk (Intercom/Zendesk, 376), Omni (workplace search, 177), AgenticSeek (cloud AI, 122), plus ZaneOps/DockerHoster (Vercel). Explicit Ask HNs are small (European Vercel/Cloudflare alternative 13 pts; Confluence for small dev teams; Jsonbin.io; MinIO; FOSS Merge/Paragon/Unified; Clay.com). Categories still called unsolved: a production-grade self-hosted Calendly after Cal.com closed (Easy!Appointments is the fallback), a satisfying OSS Intercom (Chatwoot criticised; Libredesk/Opencom new), and self-hosted outbound email (universally "not worth it"). r/selfhosted could not be read directly.

### Cited Findings
HN Show HN launches that explicitly target a paid tool (points / comments / date):
- Files.md, "Open-source alternative to Obsidian", 730 / 356, 18 May 2026 -- [HN 48179677](https://news.ycombinator.com/item?id=48179677)
- Pangolin, "Open source alternative to Cloudflare Tunnels", 500 / 125, 10 July 2025 -- [HN 44526015](https://news.ycombinator.com/item?id=44526015)
- Libredesk, open-source customer support desk vs Chatwoot/Intercom/Zendesk, 376 / 75, 24 Feb 2025 -- [HN 43158166](https://news.ycombinator.com/item?id=43158166)
- Omni, open-source workplace search and chat on Postgres, 177 / 42, 2 March 2026 -- [HN 47215427](https://news.ycombinator.com/item?id=47215427)
- AgenticSeek, "Self-hosted alternative to cloud-based AI tools", 122 / 18, 26 Apr 2025 -- [HN 43805457](https://news.ycombinator.com/item?id=43805457)
- Hopp, "open-source alternative to expensive pair programming apps", 39 / 17, 1 Sept 2025 -- [HN 45092967](https://news.ycombinator.com/item?id=45092967)
- Wakana, open source alternative to Wakatime, 42 / 23, 25 March 2025 -- [HN 43469783](https://news.ycombinator.com/item?id=43469783)
- Opencom, "full Intercom alternative, open-source", 28 Feb 2026 -- [HN 47194407](https://news.ycombinator.com/item?id=47194407)
- ZaneOps "self-hosted alternative to Vercel, Heroku and Render" (Feb 2025, 7 pts; Mar 2026, 4 pts); DockerHoster "self-hosted alternative to Vercel" (Jan 2026); Baserow 2.0 vs Airtable (Nov 2025); Planly vs Jira/Asana (Aug 2026); NoteDiscovery vs Notion/Obsidian (Nov 2025); Whook vs Hookdeck/webhook.site (Jan 2026); Eigen vs Google Workspace (Oct 2026); Flowctl open-source workflow automation (Dec 2025) -- [HN Algolia query "self-hosted alternative" 2025+](https://hn.algolia.com/api/v1/search?query=%22self-hosted%20alternative%22&tags=story&numericFilters=created_at_i%3E1735689600)
Explicit Ask HN requests 2025-2026 (all low-vote):
- "Ask HN: European alternative to Vercel/Cloudflare for hosting", 13 / 20, 27 Jan 2026 -- [HN 46781700](https://news.ycombinator.com/item?id=46781700)
- "Ask HN: Is there a good open-source alternative to Adobe Acrobat?", 9 / 9, 26 Jan 2026 -- [HN 46764607](https://news.ycombinator.com/item?id=46764607)
- "Ask HN: Self Hostable Alternative to Jsonbin.io?", 8 / 1, 2 Nov 2025 -- [HN 45793606](https://news.ycombinator.com/item?id=45793606)
- "Ask HN: What's a modern alternative to Confluence for small dev teams?", 5 / 8, 11 Sept 2025 -- [HN 45214077](https://news.ycombinator.com/item?id=45214077)
- "Ask HN: Is there any good open-source alternative to MinIO?", 4 / 5, 1 May 2026 -- [HN 47977081](https://news.ycombinator.com/item?id=47977081)
- "Where Is the FOSS Alternative to Merge, Paragon, Unified, etc." (unified API integrations), 3 / 2, 9 Apr 2025 -- [HN 43636469](https://news.ycombinator.com/item?id=43636469)
- "Interest in an open-source alternative to Clay.com for data enrichment?", 1 / 3, 21 Apr 2025 -- [HN 43756298](https://news.ycombinator.com/item?id=43756298)
- "Ask HN: Any interest in a 5x cheaper alternative to Fly.io for containers?", 3 / 2, 24 May 2025 -- [HN 44080015](https://news.ycombinator.com/item?id=44080015)
- "Open source alternative to Lovable, Bolt and v0", 3 / 0, 29 Aug 2025 -- [HN 45067304](https://news.ycombinator.com/item?id=45067304)
Still no good answer:
- Scheduling after Cal.com: Cal.diy "recommended for personal, non-production use"; Easy!Appointments "won't match Cal.com's polish" and "lacks the same slick routing, analytics, and enterprise authentication"; Nextcloud is "a lot of plumbing for one faucet"; Thunderbird Appointment hosted option is waitlist-only ("Hardly a terrific experience" -- jen729w) -- [Implicator.ai](https://www.implicator.ai/cal-com-goes-private-as-self-hosted-calendly-choices-narrow-in-2026/); [HN 47780456](https://news.ycombinator.com/item?id=47780456)
- Support desk: Chatwoot "haven't done a great job" (rhubarbtree, Oct 2025) -- [HN 45565815](https://news.ycombinator.com/item?id=45565815)
- Outbound email: see KQ4.

### Inferences
- The HN community's demand signal has shifted from "ask for" to "ship" an alternative; the Show HN titles are a better proxy for pain than Ask HNs.
- The categories with the biggest OSS gaps for solo founders are exactly the ones with heavy ops burden (email sending, scheduling with calendar sync, support inbox with multi-channel), which is why hosted OSS (PostHog Cloud, n8n Cloud, Plausible Cloud) thrives.

### Gaps
- r/selfhosted top request threads 2025-2026 could not be retrieved (reddit.com blocked). The awesome-selfhosted issue tracker returned 403 / "0 results". alternativeto.net request lists were not reachable within budget.
- Nothing retrieved on self-hosted alternatives to Loom, Typeform, Senja or Canny specifically for 2025-2026 (Cap/Screenity were named only in the Screen Studio context).

---

## KQ4. What stops founders from self-hosting, and what makes them pay for a hosted version of an OSS tool anyway?

### Takeaway
Time is the universal blocker ("If I spend 15 mins of time every month extra self hosting then it's immediately not worth it"), followed by email deliverability (near-unanimous "not worth it"), and ops complexity for heavy stacks (PostHog). People pay hosted-OSS vendors for DB migrations, backups, uptime, and to keep the project sustainable, not for features.

### Cited Findings
Time / maintenance
- jaccola, HN 2 Feb 2026: "If I spend 15 mins of time every month extra self hosting then it's immediately not worth it." -- [HN 46850994](https://news.ycombinator.com/item?id=46850994)
- seec, HN "Why Self-Host?" 10 Oct 2025: "you have to pay with your time, which is not worth it for most"; "install open-source stuff with a docker image and god knows how many configuration steps and gotchas"; "people just say fuck it and pay someone else" -- [HN 45538496](https://news.ycombinator.com/item?id=45538496)
- fodkodrasz, 24 July 2026: "I contemplated self-hosting before, but realized it is not worth the hassle" -- [HN 49031792](https://news.ycombinator.com/item?id=49031792)
- kaydub, 6 Sept 2026: "It's not worth dealing with the headaches of managing things myself." -- [HN 49590493](https://news.ycombinator.com/item?id=49590493)
- ownagefool, 23 May 2025, on managed Postgres: "it's not worth my time." -- [HN 44072674](https://news.ycombinator.com/item?id=44072674)
- tallanvor, 20 Oct 2025 ("What I Self Host"): "it's just not worth it until I actually have the time to spare." -- [HN 45646623](https://news.ycombinator.com/item?id=45646623)
Email deliverability
- tcdent, 5 Oct 2026: "self-hosting your own outbound email is not worth it" -- [HN 49966767](https://news.ycombinator.com/item?id=49966767)
- sshprotocol, 17 Aug 2026 ("Self hosted email continues to steeply decline"): "it's not worth it to me, especially since using / sending email is mandatory for doing most things." -- [HN 49333022](https://news.ycombinator.com/item?id=49333022)
- LoganDark and sandeepkd, 24 July 2026 ("Self-host your mail server"): "It's just not worth it."; "its not worth it unless you are doing it as a business." -- [HN 49040114](https://news.ycombinator.com/item?id=49040114); [HN 49041232](https://news.ycombinator.com/item?id=49041232)
- Guide: deliverability is "the single hardest part of self-hosting"; even with perfect SPF/DKIM/DMARC/rDNS "your IP will likely be viewed with suspicion by major providers like Gmail and Microsoft" -- [Elementor guide](https://elementor.com/blog/how-to-host-your-own-email-server/); startup account of being blocked by a major German provider despite a reputable ESP and dedicated IP -- [Feedbagel](https://feedbagel.com/post/why-self-hosting-email-is-problematic-a-startups-experience-with-email-deliverab)
Ops weight of specific OSS tools
- PostHog self-host runs ClickHouse + Kafka + Postgres + Redis, "7+ services", 8 GB VPS practical minimum; "PostHog is refreshingly honest about this: for most teams, they will tell you Cloud is the right answer" -- [Databuddy](https://www.databuddy.cc/blog/best-self-hosted-web-analytics-developers-2026); [use-apify PostHog guide](https://use-apify.com/docs/self-hosted/analytics/posthog)
- Umami (app + Postgres) ~400 MB idle vs Plausible (app + Postgres + ClickHouse) ~1.8 GB -- [use-apify Plausible vs Umami](https://use-apify.com/blog/plausible-vs-umami-2026)
- n8n: self-host free, "No per-execution fees"; cloud "handles updates, backups, and uptime so your team does not have to" -- [LowCode Agency](https://www.lowcode.agency/blog/n8n-self-hosted-vs-cloud)
Why people pay for hosted OSS
- nh2 (Libredesk thread, Feb 2025): "the hosted version takes care of DB migration and backups for them."; "A lot of people will be happy to pay for the convenience of hosted."; aarreedd: "Happy to pay a bit to keep the project sustainable." -- [HN 43158166](https://news.ycombinator.com/item?id=43158166)
- Hyvor Relay: self-hosted AGPL free, planned cloud tier EUR 30/mo for 300k emails (listing may be stale) -- [OpenAlternative](https://openalternative.co/hyvor-relay)
Why people self-host anyway
- ur-whale, 9 Oct 2026: "Self-hosting is, for most enterprises, absolutely not about economics but rather about data confidentiality." (enterprise, not solo) -- [HN 50017353](https://news.ycombinator.com/item?id=50017353)
- Gitea guide lists "no surprise pricing changes" as a reason to self-host -- [DevToolPicks](https://devtoolpicks.com/blog/best-github-alternatives-indie-hackers-2026)
- minraws, 15 Aug 2026 (Cloudflare outage thread): "you might be better off self hosting, even in this ram apocalypse." -- [HN 49311238](https://news.ycombinator.com/item?id=49311238)

### Inferences
- The willingness-to-pay for hosted OSS is an ops-insurance payment: founders pay for backups, migrations and uptime, which suggests a hosted-OSS product for solo founders should price like insurance (flat, low, no seats), not like the incumbent SaaS.
- Anything that sends email (newsletters, transactional, support replies) is the one category where even self-hosting enthusiasts tell solo founders to pay.

### Gaps
- No quantitative survey of founders' self-host vs pay decisions found; all evidence is anecdotal HN comments.

---

## KQ5. What features do people want that incumbents gate behind expensive tiers?

### Takeaway
The recurring gated items are: branding removal and custom domains (Typeform: branding on Plus+, custom domain Enterprise-only; Tally: Pro; Carrd: Pro), A/B testing and referral programmes (Kit: Creator Pro), AI features (Notion: Business $20; Loom: Business + AI $24), full design access and monthly billing (Figma: Full seat; Organization annual-only), priority support (beehiiv higher plan), premium app connectors and AI steps (Zapier), and spend caps / flat-rate CDN protection against bill spikes (Vercel, only added after incidents).

### Cited Findings
- Typeform: "With a Plus or higher account you can remove all Typeform branding"; favicon and email legal disclaimer cannot be removed; custom domain: "if you're on an Enterprise plan, you can create a custom domain" -- [Typeform help](https://TYPEFORM.COM/help/a/remove-typeform-branding-360029262372/)
- Tally: "With Tally Pro, you can remove all Tally branding" -- [Tally help](https://tally.so/help/remove-tally-branding)
- Carrd: Pro from $19/yr includes custom domains and no branding; sources conflict on whether a $9/yr Pro Lite covers custom domains -- [Carrd Pro](https://carrd.co/pro); [Unilink Carrd pricing](https://www.unilink.us/blog/carrd-pricing-2026)
- Kit: referral system and full-email A/B testing in Creator Pro ($79/mo at 1k subs), not Creator ($39) -- [Skillscouter](https://skillscouter.com/kit-review/); [PassiveKit](https://www.passivekit.com/?p=629)
- Kit free plan: platform controls a paid recommendation spot and keeps the revenue (creator complaint) -- [Skipblast](https://skipblast.beehiiv.com/p/going)
- Notion: full AI only in Business $20/user; Plus gets 20-response trial -- [SaaS Price Pulse](https://www.saaspricepulse.com/blog/notion-pricing-history)
- Loom: most AI features only on Business + AI $24/seat -- [SaaStr](https://saastr.com/atlassian-just-deleted-looms-free-seats-it-was-also-looms-distribution)
- Figma: Dev/Collab seats exclude Figma Design; Organization/Enterprise "killed monthly billing" -- [UserJot](https://userjot.com/blog/figma-pricing-2025-plans-seats-costs-explained); the Professional-to-Organization gap ($15 -> $55/seat) called "the biggest pain point" -- [Pricing SaaS newsletter](https://newsletter.pricingsaas.com/p/inside-figmas-pricing-evolution)
- beehiiv: priority support only on more expensive plan (creator quote) -- [Skipblast](https://skipblast.beehiiv.com/p/going)
- Zapier: premium apps "$20-50/month per app on lower tiers" (comparison-site claim); AI steps billed as tasks -- [Neura.market](https://www.neura.market/blog/zapier-pricing-2026-is-it-still-worth-it-a-forward-looking-analysis); [Zapier pricing](https://zapier.com/pricing)
- Intercom: proactive messaging $99/mo add-on, $0.99 per AI resolution (competitor source) -- [Spur](https://www.spurnow.com/blogs/intercom-pricing)
- Vercel: Spend Management exists but did not reduce already-incurred charges; "a new flat rate CDN option that protects against temporary spikes" promised by staff Sept 2026 -- [Vercel Community](https://community.vercel.com/t/ddos-attack-caused-170-in-extra-charges-support-refuses-refund/44044)
- Free tiers break at the second person: IH commenter observed most SaaS free tiers "become too limited once a second person joins the team" (via search snippet; IH blocked) -- [IH thread](https://www.indiehackers.com/post/which-saas-do-you-pay-for-as-an-indie-hacker-131cca2b19)

### Inferences
- For a solo founder the gated features that matter are cosmetic/ownership ones (custom domain, no branding, export) and bill-safety ones (hard spend caps). An OSS or flat-fee tool that ships those at the base tier directly addresses the recurring complaint.
- "AI as the new upsell lever" (Notion, Loom, Intercom Fin, Zapier AI tasks, Cursor credits) is the 2025-2026 pattern replacing the older "seats as the upsell lever".

### Gaps
- No Calendly branding/custom-domain gating evidence surfaced. No Senja, Canny, Buffer/Hypefury/Typefully, Webflow, Mailchimp or HubSpot gating evidence beyond generic aggregator pages. Search budget was exhausted before these could be covered.
