# Status page + uptime monitoring: competitor teardown

Captured 2026-10-12 with headless Chromium at 1440px (Firecrawl was out of credits, so screenshots were taken with Playwright). Full-page PNGs sit next to this file, one per domain, plus a `-pricing` PNG for each pricing page. Colour values were read from computed CSS on the live pages; where a site serves colours in lab() they are converted to the nearest hex.

Files:

- instatus.com.png, instatus.com-pricing.png
- openstatus.dev.png, openstatus.dev-pricing.png
- betterstack.com-uptime.png, betterstack.com-pricing.png
- uptimerobot.com.png, uptimerobot.com-pricing.png
- statuspage.io.png, statuspage.io-pricing.png
- hyperping.com.png, hyperping.com-pricing.png

---

## 1. Instatus (instatus.com)

**Hero**

- Headline: "GET READY FOR DOWNTIME"
- Subheadline: none. Three rotating lines under the hero: "Monitor your services", "Fix incidents with your team", "Share your status with customers"
- Primary CTA: "START FREE" (a second button reads "PLAY GAME", the hero is a retro arcade intro with "PRESS A TO GET STARTED" prompts)

**Section order**

1. Hero (animated arcade cinematic, headline fades in over a blue light streak)
2. Customer logos (Sketch, Dovetail, Airbyte, Harvard, Deno, Polymarket, Wistia, Modern Treasury)
3. 3D wireframe tunnel / screen frame transition
4. "GET ALERTED EVERYWHERE" with four product tabs (Check all your services, Track availability, Real-time alerts, Notify the right people) and an on-call schedule mock
5. "FIX INCIDENTS WITH YOUR TEAM" with an integrations browser (38 integrations grouped Monitoring / Notifications / Update your page / Metrics)
6. Incidents dashboard mock ("ADD A TEST INCIDENT")
7. "PUBLISH TO STATUS PAGE" with a $0/month callout
8. "CALCULATE YOUR SAVINGS" (replace Pingdom + PagerDuty + Atlassian Statuspage, interactive total bill)
9. "STAY AHEAD OF THE CRASH" closing CTA
10. Footer with a live "All systems operational" pill

**Visual system**

- Background: pure black #000000 with deep navy panels #131B2B and #02050D
- Accent: mint #BBFFF6 (nav active link, Sign up pill, headline glow), secondary teal #6FE4CB, alert red #DC2626
- Typography: Inter body, Soehne for the uppercase display headlines. Headlines are letter-spaced ALL CAPS which gives the arcade feel
- Corners: pill buttons (9999px), large 32px card radius, 8px inside dashboards
- Illustration: 3D cinematic (spinning crystal, light streak, wireframe tunnel), dark product screenshots, 49 gradient layers
- Gradients: heavy, used for glows and the hero light beam

**How the status page is rendered**

The homepage barely shows the status page itself. The product shots are the on-call schedule and incident list. The only status visual is the footer "All systems operational" dot. The arcade framing is the brand, not the uptime bar.

**Best**: the committed arcade cinematic. It is the only site in the category with a real idea and it makes the free tier feel like a game you start rather than a form you fill.

**Generic**: the feature tabs and the integrations grid are standard SaaS blocks once the animation stops, and the hero text is nearly unreadable until the animation finishes.

**Pricing** (instatus.com/pricing, "Use for free. Upgrade for hyper powers.", yearly toggle at 25% off)

- Starter: Free. 15 monitors, 2 min checks, email alerts, public page, 200 subscribers
- Pro: $20/month (read from page HTML). 50 monitors, 30 sec checks, email and SMS, 20 on-call members, 1+ custom domain, 5,000 subscribers
- Business: price is an animated JS counter and could not be read reliably from the capture. 1,000 monitors, SMS and calls, 50 on-call members, SAML SSO, all page types, 3+ custom domains, 25,000 subscribers
- Enterprise: contact. SCIM, priority support, 99.99% SLA, custom contracts
- Gated: check frequency, alert channels, on-call seats, SSO, page types, subscriber count. Free Pro for open source and non-profits on request.

---

## 2. openstatus (openstatus.dev)

**Hero**

- Headline: "Run status pages and incident response from Slack or your AI agent."
- Subheadline: "Open source status page, incident response and global uptime monitoring. When something breaks, your subscribers hear it first and your auditor gets the trail."
- Primary CTA: "Get started free" (secondary: "GitHub 9k+"; microcopy "Free to start, with a 14-day Starter trial and no card needed. Paid plans from $30/mo.")

**Section order**

1. Hero (text left, immediately followed by a full-width live status page mock for the fictional Pied Piper, mid-incident)
2. "Trusted by teams who ship transparency" logo grid (Cal.com, Documenso, Hanko, Superwall, Probo, Roundtable)
3. "One incident, start to finish": a six-step timeline (09:41 monitor catches it, 09:43 declare incident, 09:44 tell customers from Slack, 10:14 mitigate, 11:02 postmortem draft, +1 week record stays public, +6 months audit trail) each with a Slack or dashboard mock on the right
4. "In their words" two testimonials
5. "For humans and agents" (CLI, API, MCP server, Terraform)
6. "Flat pricing" plain table (Hobby $0, Starter $30, Pro $100, Scale $500)
7. "Get started"
8. FAQ (five questions)
9. Footer with light/dark/system toggle and a live "Operational" indicator

**Visual system**

- Background: white #FFFFFF, text near-black #0A0A0A, borders light grey #E5E5E5
- Accent: status green #22C55E, amber #F59E0B, blue #3B82F6, red #EF4444 (shadcn / Tailwind defaults)
- Typography: everything, including headlines, is Commit Mono. The whole site reads like a README
- Corners: none. Square boxes, 1px borders, table layouts. Zero gradients
- Illustration: no illustration at all, only mocked UI (Slack cards, postmortem doc, audit log) rendered as bordered boxes with real text

**How the status page is rendered**

The best in the set. A bordered card with a Degraded Performance banner (amber tint), then per-component rows: name, uptime percentage, and a 45-day bar of thin green rectangles with amber and red segments for degraded days, labelled "45 days ago" and "Today". Separate incident timeline uses a vertical rail with coloured dots per state (Resolved green, Monitoring blue, Identified amber, Investigating red) and timestamps.

**Best**: the timestamped incident narrative. Telling the product story as a clock (09:41 to six months later) is the strongest copy structure in the category and the mono type makes it feel honest.

**Generic**: the shadcn colour defaults and the plain white page make it look like every other open source dashboard; it has no brand colour of its own.

**Pricing** (openstatus.dev/pricing)

- Hobby: $0, 1 monitor, 1 status page, 10 min checks
- Starter: $30/mo, 20 monitors, 1 min checks, 1 status page, 20 components, custom domain, 6 regions per monitor, 3 months retention
- Pro: $100/mo, 50 monitors, 30 sec checks, 5 pages, 50 components, all 28 regions, custom theme, 12 months retention, audit log, private locations, OTel exporter
- Scale: $500/mo, 10 pages, 500 components, white label, email auth, IP restriction, 24 months retention
- Add-ons priced per month: extra status page $20, custom theme $20, white label $300, email auth $100, IP restriction $100, SSO $250, 10 extra monitors $15
- Unlimited team members on every plan. Enterprise is contact only. Self-host under AGPL-3.0.

---

## 3. Better Stack Uptime (betterstack.com/uptime)

**Hero**

- Headline: "The most reliable uptime monitoring"
- Subheadline: "Get 10 monitors, 10 heartbeats and a status page with 3-minute checks totally free."
- Primary CTA: "Get started in 30 seconds" (email field inline; "Looking for an enterprise solution? Book a demo")

**Section order**

1. Hero (centered text, email capture, large dark dashboard screenshot with glow)
2. "Relied on by the world's best engineering teams" logo marquee (Brave, NordVPN, Unicef, Decathlon, Raycast)
3. "Best-in-class uptime monitoring. No false positives." bento grid (Traceroute and MTR, Screenshots and error logs, Playwright transaction monitoring, SSL to domain expiration, 30s checks, Cron monitoring)
4. "A lot more than uptime monitoring. Batteries included." (incident merging, escalations, unlimited voice calls)
5. "Elegant status page" (status.yourdomain.com, share updates, subscribe to updates)
6. "Save big with Better Stack" comparison card: PagerDuty + Pingdom + Statuspage.io $673/mo vs Better Stack $269/mo
7. "Don't just take our word for it" Twitter testimonial masonry
8. "Get started in 30 seconds" closing CTA
9. Footer (large platform sitemap)

**Visual system**

- Background: near-black navy #0B0C14, cards #1F2433 and #0F101A
- Text: cool off-white #C9D3EE, muted #939DB8, dim #646E87
- Accent: indigo #7C87F7 (buttons #5B63D3, highlights #98A4F7)
- Typography: Helvetica Now Display for headlines, Helvetica Now Text for body. Tight, Swiss, corporate
- Corners: 8px and 16px cards, pill buttons, 6px inner elements
- Illustration: dark product screenshots with a soft indigo glow behind them, bento cards with miniature UI vignettes, 19 gradient layers (mostly edge glows and dotted light fields)

**How the status page is rendered**

A small dark status page screenshot inside the "Elegant status page" block: an "All services are online" header and a list of components with green bars. It is the generic Better Stack status page look (dark card, green dot rows). Not a hero element.

**Best**: the bento grid of miniature UI vignettes. Each card contains a real product fragment (traceroute output, error 502 timeline, Playwright logo) so the grid is informative rather than decorative.

**Generic**: the hero. Centered headline, email field, glowing dashboard screenshot and a logo marquee is the exact template of every dark SaaS site in 2025.

**Pricing** (betterstack.com/pricing, 60-day money-back guarantee, annual gets ~2 months free)

- Free: $0, 10 monitors and heartbeats, 1 status page, Slack and email alerts, plus telemetry allowances
- Responder license: $34/month monthly or $29 annual, per responder. Unlocks incident management, on-call, unlimited phone call and SMS alerts
- Non-responder team members: $0
- Status page add-ons: extra public page $15/mo, custom CSS and JS $15/page, white label $250/page, password auth $50/page, IP allowlisting $250
- Slack and Teams advanced workflows: $9 per responder
- AI SRE: consumption based
- Gated: phone call alerts, on-call, white label, page auth, and everything telemetry is a separate consumption meter. Pricing page is a very long per-product matrix, not a three-card layout.

---

## 4. UptimeRobot (uptimerobot.com)

**Hero**

- Headline: "Meet the #1 uptime monitoring service."
- Subheadline: four check-marked bullets: "50 monitors for free", "20+ integrations", "Real-time alerts, web & mobile", "Public status pages"
- Primary CTA: "Start monitoring for free" (inline email field; badge above headline: "Over 3.4M+ users trust UptimeRobot.")

**Section order**

1. Hero (centered, email capture, dark dashboard screenshot)
2. Logo marquee (n8n, Canva, OVHcloud, Akamai, Atlassian, GitHub, Slack, Siemens, Intel, IBM, BBC)
3. "Catch downtime before your users do." six icon cards (Website, Keyword, Ping, Port, Cron job, DNS record monitoring)
4. "Need more than 500 monitors? Book an Enterprise demo." banner
5. "Trusted by over 3.2M+ developers and teams." with 4.7 star rating and case study carousel
6. "Real-time status pages for your website, API, or service." with a tilted 3D status page render
7. "Start monitoring in seconds. Seriously." dashboard card
8. "Deep insights. Full control. Zero blind spots." accordion feature list with screenshot
9. Integrations card and mobile app card (two-up)
10. FAQ (nine questions)
11. "Start monitoring in 30 seconds." closing CTA
12. Footer

**Visual system**

- Background: dark slate #111821, cards #131B25 and #1C2634, borders #2D3540
- Text: #E2E8F0, muted #A0ADC0 and #72849E
- Accent: bright green #3BD671 used for headline keyword, buttons, check marks, icon glows, and every status indicator
- Typography: Plus Jakarta Sans for headlines, Inter for body. Friendly, rounded, slightly consumer
- Corners: very rounded, 24px and 32px cards, pill buttons, 8px inner
- Illustration: dark product screenshots, line icons with concentric green radial glows behind them, a tilted isometric status page, 18 gradient layers

**How the status page is rendered**

A tilted perspective render of a dark status page: "All systems operational" header and a stack of components each with a row of bright green ticks. The bars are shown as a decorative texture, not readable. Elsewhere the dashboard shows small green bars for "Last 24 hours".

**Best**: the single-accent discipline. One green against slate, repeated on icons, ticks, buttons and the headline keyword, makes the whole page feel like one product.

**Generic**: everything else. The six icon cards, logo marquee, testimonial carousel and FAQ are the stock enterprise SaaS stack with no surprises.

**Pricing** (uptimerobot.com/pricing, "Unmatched affordability. Exceptional monitoring.", annual saves ~15%)

- Free: $0, 50 monitors, 5 min interval, basic status pages, 5 integrations, 3 months retention
- Solo: $12/mo annual ($13 monthly), 10 monitors, 60 sec interval, 3 status pages with own domain, 12 months retention
- Team: $39/mo annual ($46 monthly), most popular, 100 monitors, 30 sec interval, 3 seats, 100 status pages white-label, webhook, Zapier, PagerDuty
- Scale: $79/mo annual ($98 monthly), 200 or 500 monitors, 15 sec interval, 5 seats, unlimited status pages
- Enterprise: contact
- Gated: interval, seats ($15 to $19 per extra login seat), SMS and call credits, white label, password pages, status page analytics, retention. Offers a machine-readable pricing page for AI agents.

---

## 5. Atlassian Statuspage (atlassian.com/software/statuspage)

**Hero**

- Headline: "Build trust with every incident"
- Subheadline: "Easily communicate real-time status to your users, just like DigitalOcean and Dropbox."
- Primary CTA: "Get it free" (secondary: "See how" video link)

**Section order**

1. Hero (centered text, two real customer status page screenshots side by side: DigitalOcean and Dropbox)
2. "SUPPORT & IT TEAMS: Eliminate duplicate support tickets & clunky email lists" (flat illustration, hot air balloons)
3. "DEVOPS & IT TEAMS: Display the status of each part of your service" (status page screenshot with uptime bars)
4. "Statuspage is the communication piece of your incident management process" (grey band, hub-and-spoke illustration)
5. "INCIDENT RESPONSE TEAMS: Level-up your incident communication" (illustration)
6. "MARKETING & SALES TEAMS: Showcase reliability" (Uptime Showcase screenshot)
7. "Trusted by thousands of companies" video testimonial
8. "Pricing that scales with you as you grow" (inline pricing with Public / Private / Audience-specific tabs)
9. Atlassian corporate footer

**Visual system**

- Background: white #FFFFFF with light grey bands #F4F5F7
- Text: Atlassian navy #091E42, secondary #42526E
- Accent: Atlassian blue #0052CC (buttons, links), yellow #FFAB00 (illustration and cookie banner), green in the status screenshots
- Typography: Charlie Display headlines, Charlie Text body. Clean, corporate, slightly rounded
- Corners: tiny, 3px and 4px. Zero gradients
- Illustration: flat vector Atlassian house style (people, balloons, clouds, giant check marks in green and yellow), plus real customer screenshots

**How the status page is rendered**

The classic: a white card, a full-width green "All Systems Operational" banner, then component rows with a name, a 90-day bar of thin green ticks, and "Operational" in green on the right. The DigitalOcean example adds an incident history list with dated entries. This is the format every other product copies.

**Best**: leading with real customer status pages in the hero. Showing DigitalOcean and Dropbox instantly answers "what will mine look like" and borrows their credibility.

**Generic**: the flat illustrations are interchangeable with every other Atlassian product page and date the site; the page has no motion and no developer signal at all.

**Pricing** (atlassian.com/software/statuspage/pricing, "No minimum contracts, no sign-up fees, no cancellation fees")

Public page tab:

- Free: 100 subscribers, 25 components, 2 team members, 2 metrics, email, Slack and Teams notifications, REST API
- Hobby: $29/mo, 250 subscribers, 5 team members, 5 metrics, basic customization, custom domain
- Startup: $99/mo, 1,000 subscribers, 10 members, 10 metrics, SMS and webhook notifications, custom CSS, SSO
- Business: $399/mo, 5,000 subscribers, 25 members, custom CSS/HTML/JS, component subscriptions, RBAC
- Enterprise: $1,499/mo, 25,000 subscribers, 50 members, purchase orders

Private page and Audience-specific page tabs have separate ladders (Starter, Growth, Corporate, Enterprise). Gated: subscribers, team members, metrics, SMS, custom code, SSO, RBAC.

---

## 6. Hyperping (hyperping.com)

**Hero**

- Headline: "Show uptime. Catch downtime."
- Subheadline: "Monitoring, status pages and on-call in one simple platform."
- Primary CTA: "Get started" (secondary: "Sign up with Google"; microcopy "20 monitors free. No credit card required."; a "New: Ask Hyperping, the AI that investigates" pill above the headline)

**Section order**

1. Hero (left-aligned text, two overlapping product screenshots on the right: monitors list and a status page, on a dotted world map)
2. "Trusted by teams that put uptime first." logo grid (Alma, Pitch, Silverfort, Beatport, EF, Higgsfield, Havas, Slite, Husqvarna, Oxford)
3. "We're on watch" live counter ticker (checks run today, active monitors, outages caught, alerts sent, heartbeats received, live status pages) with rolling digits
4. "Uptime, status pages and on-call. One platform. Know before your customers do." bento grid of seven feature cards each with a mini UI vignette (Uptime, Server, Browser checks with Playwright code, Cron, Notification channels, SSL, On-call calendar)
5. "Status pages. For your customers. And your team." (public page mock and private SSO login mock)
6. "Powering businesses of all sizes." case study carousel (big orange Alma card)
7. "Monitoring from 18 locations worldwide." stats row (18 locations, 30s checks, 99.99%, SSO, SLA, Audit logs) plus "Verified alerts" integration icons
8. "Real status pages, in production." gallery of four real customer status pages (Pitch, Slite, Beatport, ClearShot X)
9. "What teams say about Hyperping." testimonials
10. "An investigator on every incident." AI section
11. "For developers" (a few lines of code, monitoring as code, your AI in the loop)
12. "Three tools. One better bill." tool mix comparison
13. FAQ (nine questions)
14. "Stay ahead of downtime." closing CTA, footer

**Visual system**

- Background: near-black #0A0A0B, cards #1E1F21, hairline borders
- Text: white and white at 60% opacity, light #EDF1EF
- Accent: mint green #5DD6AD (status, headline second line, logo), soft lavender #B8ACF4 (code and secondary highlights), secondary green #8BD9B0
- Typography: Manrope for headlines, Inter body, SF Mono for code. Calm and precise
- Corners: small, 6px and 8px, status page previews with 10px top corners. 25 gradient layers used subtly for card tops and the map
- Illustration: product screenshots, miniature UI vignettes inside cards, dotted world map, real photography in case studies

**How the status page is rendered**

Shown three times: in the hero (dark "acme" page with "All systems operational" and green tick bars), in the feature card (a small "All systems operational 99.98%" chip with a row of green ticks), and as a gallery of four real production status pages in light and dark themes with 90-day bars. The gallery is the signature move.

**Best**: the live "We're on watch" counter strip and the real status page gallery. Both prove the product is running right now, which is the whole point of an uptime tool.

**Generic**: the bento grid and the dark card system are very close to Better Stack and Linear; without the green it would be hard to tell them apart.

**Pricing** (hyperping.com/pricing, "Peace of mind. At every stage.", yearly gets 2 months free)

- Free: 20 monitors, 5 min checks, 1 server agent, 1 basic status page, 1 seat
- Essentials: $24/mo yearly ($290 billed yearly), 3 seats (+$7 each), 50 monitors, 3 browser checks, 1 status page with custom domain, 100 subscribers, on-call, phone alerts, all integrations
- Pro: $74/mo yearly ($890), 10 seats (+$9), 250 monitors, 10 browser checks, 3 public or private pages, 1,000 subscribers, SMS subscribers, multilingual, SAML SSO
- Business: $249/mo yearly ($2,990), 20 seats (+$12), 1,000 monitors, 10 pages, unlimited subscribers, white label, audit logs
- Enterprise: custom
- Logs are metered at $0.25/GB over the included volume. AI included on every paid plan.
- Gated: seats, monitors, status page count, subscribers, white label, SSO.

---

## Cross-site patterns worth knowing

- Five of six are dark. Only openstatus and Statuspage are light. Dark + one green is the category default (UptimeRobot #3BD671, Hyperping #5DD6AD, Instatus mint #BBFFF6). Better Stack is the one dark site using indigo instead of green.
- Every site shows the same uptime bar: thin vertical green ticks, 45 to 90 days, amber and red segments for incidents, "Today" on the right.
- Every site has a logo wall in slot two. Every dark site uses a glowing product screenshot in the hero.
- The two strongest copy devices are openstatus's clock timeline and Better Stack's "replace three tools" bill comparison.
- The free tiers are generous (10 to 50 monitors). $5/mo would be the cheapest paid cloud plan in the category by a wide margin; the next cheapest is UptimeRobot Solo at $12.

---

## Mash-up design brief: Pulsepage

Pulsepage is open source, free to self-host, $5/mo on the hosted cloud. First audience is Omarchy and Linux developers, so the site should feel like a well-kept terminal, not a SaaS funnel. Dark, but warm and high-contrast, so it sits away from omarchy.org (black and mono) and from Shiplog (Tokyo Night blues and purples).

### Direction in one line

A warm, amber-lit dark theme with terminal honesty: one accent, square-ish geometry, mono type for anything that is data, and a status bar you can actually read.

### Palette

| Role | Hex | Notes |
|---|---|---|
| Page background | #141210 | warm near-black, brown undertone, never pure black |
| Surface / card | #1E1A16 | one step lighter, cards get a 1px border instead of a shadow |
| Border | #342D27 | hairline, warm |
| Text primary | #F3EBDD | parchment off-white, high contrast on #141210 (ratio above 14:1) |
| Text secondary | #A89C8C | warm grey for labels and microcopy |
| Accent (brand) | #FFB454 | amber. Buttons, headline keyword, cursor, links |
| Accent pressed | #E09A3A | hover and active states |
| Up | #9CE37D | warm lime for operational ticks |
| Degraded | #FFB454 | the brand amber doubles as degraded, so an incident literally lights the page in brand colour |
| Down | #FF6B57 | coral red, warm not cool |
| Maintenance | #7FB5FF | the only cool colour, used sparingly so it reads as "scheduled, not broken" |

Rule: no gradients except a single amber radial glow behind the hero status card at 12% opacity. No indigo, no mint, no Tokyo Night blue.

### Typography (Google Fonts)

- Display and headings: **Bricolage Grotesque** (weights 600 and 800, slightly condensed with optical sizing; it is characterful without being quirky)
- Body, UI, data, code: **JetBrains Mono** (400 and 500). Everything that is a number, a timestamp, a percentage or a hostname is set in mono, which is where the developer-native feel comes from

Body paragraphs can also sit in JetBrains Mono at 15px with 1.6 line height, openstatus-style, to keep the two-font rule strict.

### Hero layout

Two columns on desktop, stacked on mobile.

- Left: a small amber "prompt" label (`$ pulsepage init`) in mono, then the headline in Bricolage Grotesque 800 at 64px, then a one-sentence sub, then two buttons: amber filled "Self-host for free" and outlined "Cloud for $5/mo". Under the buttons a mono line: "AGPL. One binary. Runs on a Raspberry Pi or Cloudflare."
- Right: a live, real Pulsepage status card (not a screenshot) for status.pulsepage.dev itself, showing three components with 90-day bars, one with a degraded day, and a breathing amber dot in the corner labelled "live". This borrows Statuspage's "show the real thing in the hero" and Hyperping's "it is running right now" proof.
- Headline copy: "Your status page. Your server. Your rules."
- Sub copy: "Open source uptime monitoring and status pages for people who read logs. Self-host in one command, or let us run it for five dollars a month."

### Page sections in order

1. **Hero**: "Your status page. Your server. Your rules." with the live status card.
2. **Install strip**: a single copyable command block (`curl -fsSL get.pulsepage.dev | sh` or the `pacman`/`yay` line for Omarchy) with a "or sign up for cloud" link. Replaces the logo wall; Pulsepage has no logos yet and a command is more credible to this audience.
3. **The incident, by the clock**: five rows with mono timestamps down a left rail (03:12 check fails from two regions, 03:13 you get the ping, 03:14 one command posts the incident, 03:40 resolved, 90 days later the bar still shows the dent). Each row has a small UI vignette. Borrowed from openstatus.
4. **Feature grid**: six bordered cards, no icons with glows, each card holds a real fragment: HTTP and TCP checks, cron heartbeats, SSL expiry countdown, Slack and Matrix and ntfy alerts, a config file in TOML, a `pulsepage status` CLI output. Copy: "Everything you need to know your thing is up. Nothing you need a sales call for."
5. **Self-host vs cloud**: two cards side by side. Self-host: $0, your box, your data, you run updates. Cloud: $5/mo, we run it, custom domain, email subscribers, global check regions. Copy: "Same code either way. Pick who babysits it." Borrowed from Better Stack's bill comparison card, repointed at a hosting decision instead of competitor prices.
6. **Status pages in the wild**: gallery of four real pages running on Pulsepage in both light and dark themes. Copy: "Pages people actually ship." Borrowed from Hyperping.
7. **Pricing**: a plain mono table, three rows (Self-host $0, Cloud $5/mo, Cloud Team $15/mo if a second tier is ever needed), no feature matrix, openstatus style.
8. **FAQ and footer**: six questions (self-host requirements, data ownership, migration from Statuspage and UptimeRobot, license, what $5 covers, Omarchy install), then a footer whose last line is the live "all systems operational" indicator rendered in the same tick style as the product.

### Signature uptime bar treatment

- 90 ticks, each 4px wide and 28px tall with 2px gaps and 1px corner radius. Up ticks are #9CE37D at 85% opacity; the most recent tick is 100% opacity and pulses slowly (2.4s ease) to show the page is live. This is the "pulse" in Pulsepage.
- Degraded ticks are amber #FFB454, down ticks are coral #FF6B57 and grow to 32px tall so incidents physically stick out of the row, which no competitor does.
- Under each bar a mono caption: `99.97%  ·  90d  ·  2 incidents` on the left and `today` on the right. Hover on a tick shows a mono tooltip with the date and downtime minutes.
- On the marketing site the same bar is reused as a decorative divider between sections at 20% opacity, so the product's signature glyph becomes the page rhythm.
- Overall status banner is not a full-width green block (Statuspage, Hyperping); it is a single amber-bordered line with a text label in mono: `[ ok ] all systems operational` or `[ !! ] degraded: api`.

### Three borrowed UI motifs

1. **openstatus: the timestamped incident rail.** Mono timestamps down a thin left line, each with a UI vignette, telling one incident from first failed check to the postmortem. Pulsepage runs it warmer and shorter (five beats, not seven).
2. **Hyperping: proof it is running.** The live counter strip ("checks run today", rolling digits) and the gallery of real production status pages. Pulsepage uses one live counter (total checks across cloud, updating in view) under the install strip, and the gallery as section six.
3. **Better Stack: the comparison card.** Two cards with a highlighted winner. Pulsepage uses it for Self-host vs Cloud so the $5 price is framed as "someone else babysits it" rather than as a feature upsell.

### Things to avoid, learned from the teardown

- No logo wall in slot two, no testimonial masonry, no icon cards with radial glows (UptimeRobot), no 3D cinematic (Instatus).
- No shadcn default green/amber/red; the warm variants above are deliberate.
- No per-seat or per-feature add-on pricing matrix. Two prices, one table.
