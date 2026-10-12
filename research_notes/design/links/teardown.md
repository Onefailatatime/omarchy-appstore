# Link shortener + click analytics + link-in-bio: competitor teardown

Captured 2026-10-11 with headless Chromium (Playwright) at 1440px wide, full page. Firecrawl was out of credits, so the markdown copy and computed CSS values below were pulled directly from the live DOM. Screenshots live beside this file:

| Competitor | Home | Pricing |
|---|---|---|
| dub.co | `dub.co.png`, `dub.co-links.png` (the /links product page) | `dub.co-pricing.png` (Partners tab, default), `dub.co-pricing-links.png` (Links tab) |
| bitly.com | `bitly.com.png` | `bitly.com-pricing.png` |
| short.io | `short.io.png` | `short.io-pricing.png` |
| linktr.ee | `linktr.ee.png` | `linktr.ee-pricing.png` |
| bio.link | `bio.link.png` (pricing is a section on the home page) | n/a |
| sink.cool | `sink.cool.png`, `sink.cool-github.png` (README is the real marketing page) | no pricing, free self host |

Note: bio.link sits behind a Cloudflare bot check that fired on one attempt; the capture here came from a clean attempt and no challenge was bypassed. Bitly and Linktree captures include their cookie banners because nothing was clicked.

* * *

## 1. dub.co

**Hero headline:** "Turn clicks into revenue"
**Subheadline:** "Dub is the modern link attribution platform for short links, conversion tracking, and affiliate programs."
**Primary CTA:** "Start for free" (black pill button) with secondary "Get a demo" (white outline). Eyebrow pill: "Introducing our Startup Program".
**/links page hero:** "Short links with superpowers" / "The modern link management platform for entrepreneurs, creators, and growth teams."

**Section order (home):** nav, eyebrow pill, hero, three product chips (Affiliate Programs, Conversion Analytics, Short Links) that swap a large product screenshot, logo grid (Flow, Superhuman, Framer, Clay, Polymarket, Perplexity, Viktor, Buffer), manifesto text block with inline emoji icons ("Marketing isn't just about clicks. It's about outcomes."), Dub Links feature block, testimonial band (dotted background), Dub Analytics block ("Measure what matters") with a Sankey funnel demo, testimonial, integrations grid on a dot grid, Dub Partners block with payouts demo, testimonial, "Built to scale" with monospace live counters (links created, events tracked, revenue tracked), "Enterprise-grade link infrastructure", "Trusted by startups and enterprises", changelog ("We ship fast"), final CTA, footer with a "Compare" column (Bitly, Rebrandly, Short.io, Bl.ink).

**Visual system**
- Background: light. Body `#FAFAFA`, cards `#FFFFFF`, hairline borders `#E5E5E5`. Faint grid lines run down both sides of the content column, the whole page feels like it sits on graph paper.
- Text: `#0A0A0A` headings, `#737373` body grey, `#525252` secondary.
- Accents are tiny and product coded: blue `#2563EB` (analytics links), orange `#EA580C` (Dub Links), green `#16A34A` / mint `#DCFCE7` (conversion), purple `#581C87` (Partners). Stat counters render in orange monospace.
- Typography: Satoshi for display (48px, weight 500, tight tracking), Inter for body, GeistMono for numbers and URLs. Calm, editorial, very little bold.
- Radius: 8px on buttons, 12px on cards, 9999px on chips and pills.
- Illustration: none. Everything is a real product UI fragment at a slight tilt, often fading to white at the bottom. Light conic and radial gradients exist only inside tiny icon badges.
- Gradients: essentially none at page level. The Sankey funnel in the analytics demo is the one saturated moment (blue to purple to teal).

**Analytics rendering:** a three stat strip (Clicks 114,148 / Leads 2,235 / Sales $8,465) over a soft blue area chart with a hover tooltip, and a separate Sankey style funnel showing 100% to 36% to 1.3% in blue, violet and teal. Stats are tabs you click to change the chart.
**Link-in-bio rendering:** Dub does not have one. Closest thing is the domain cards (acme.link, refer.acme.com) with click counts and a Verified badge.

**Best visually:** the restrained, infrastructure-grade feel. Graph paper grid, monospace counters, and real UI fragments make it read as a developer tool with money behind it.
**Most generic:** the testimonial bands and logo grid are the standard YC SaaS pattern, and the page is extremely long (12,200px) with a lot of repeated "Explore X" button rows.

**Pricing (Dub Links tab, monthly):**
- Free: $0, 25 new links/mo, 1K tracked events/mo, 3 custom domains, 30-day analytics retention, QR codes, API access, AI assistant, 1 user.
- Pro: $30/mo, 1K links/mo, 50K events/mo, 1-year retention, free .link domain, folders, deep links.
- Business: $90/mo ("Best value"), 10K links/mo, 250K events/mo, 3-year retention, conversion tracking, A/B testing, webhooks, includes Dub Partners.
- Advanced: $300/mo, 50K links/mo, 1M events/mo, 5-year retention, elevated API limits.
- Enterprise: custom, unlimited, SAML/SSO, audit logs.
- Yearly toggle gives 10% off. Gated items: link volume, event volume, retention window, custom domain count (3 / 100 / 250 / unlimited), conversion tracking, A/B tests, SSO. QR codes are free on every tier. The Partners tab (default) hides prices behind a per-month figure that only renders client side.

* * *

## 2. bitly.com

**Hero headline:** "Understand what clicks with your audience"
**Subheadline:** "Bitly makes it easy to create, share, and track short links and QR Codes. Find what's resonating and scale it into bigger reach, more clicks, and more sales."
**Primary CTA:** "Sign up Free" (nav, white on navy) and "Get started for free" (navy button with arrow) throughout. The hero itself is a working shortener widget: "Shorten a long link / No credit card required / Paste your long link here".

**Section order:** announcement bar (peach), nav, hero on navy with the Short Link / QR Code tabbed shortener form, "Sign up for free. Your free plan includes:" strip with logos (Curology, Novasol, Rad Power Bikes, NYT, Smalls), "Link your marketing with Bitly" with three product cards (URL Shortener, QR Codes, Analytics), "Adopted and loved by millions" stat row (counters animate from 0, screenshot caught them at 0), customer quotes carousel on orange cards, "See how other businesses use Bitly" industry card carousel with line illustrations, "More than a link shortener" closing band on orange with a dashboard screenshot, footer.

**Visual system**
- Background: split. Navy hero `#031F39` then warm cream `#F6F4EF` body. Cards `#FFFFFD`.
- Accent: Bitly orange `#F36600`, with a darker rust `#943C01` for section eyebrow labels and a peach gradient `rgba(255,149,10,.6)` to `rgba(243,102,0,.6)` for banners and the Growth pricing card tint.
- Text: `#2F2E2D` body, navy `#031F39` headings.
- Typography: "Bitly Display" (custom grotesk) at 64px weight 500 for the H1. Friendly, rounded, approachable.
- Radius: 8px buttons, 24px cards. Everything is soft.
- Illustration: hand drawn two tone line illustrations with orange spot colour (people holding phones, QR codes), plus small sparkle and star glyphs scattered around headings.
- Gradients: yes, warm orange tints on banners and highlighted cards.

**Analytics rendering:** a blurred dashboard screenshot with an "Analyse with AI" sparkle pill floating on top. The analytics card itself shows tiny stat rows ("Total scans 1,200", "Weekly scan rate +23%" in green). The real dashboard appears only at the bottom of the pricing page.
**Link-in-bio rendering:** listed as a feature ("Link-in-bio") but not shown on the home page.

**Best visually:** the working shortener form inside the hero. The product is usable before you sign up, and the tabbed Short Link / QR Code card with its notch is a memorable shape.
**Most generic:** stock enterprise sections (industry carousel, "Adopted and loved by millions", cookie banner) and the blurred dashboard instead of a real one.

**Pricing (annual toggle default):**
- Free "With Ads": $0, 5 links/mo, 2 QR codes/mo, 2 landing pages, 3 custom back-halves/mo, unlimited clicks and scans.
- Core: $10/mo ($120/yr), 100 links/mo, 5 QR/mo, 30 days of click data, UTM builder, Bitly Assist AI.
- Growth: $29/mo ($348/yr, "Recommended"), 500 links/mo, 10 QR/mo, complimentary custom domain, branded links, 4 months of click data, bulk creation.
- Premium: $199/mo ($2,388/yr), 3,000 links/mo, 200 QR/mo, 1 year of click data, city and device level data, mobile deep linking.
- Enterprise: custom, SSO, 99.99% uptime, API and webhooks at volume.
- Gated items: link count (very low on Free), QR count, custom domain (Growth and up), analytics retention (30 days / 4 months / 1 year), city level geo (Premium), branding is removed via the custom domain. Annual saves "up to 34%".

* * *

## 3. short.io

**Hero headline:** "URL shortener with QR codes" (the "QR codes" phrase is green and has a blinking cursor, implying a typewriter rotation).
**Subheadline:** eyebrow "Free plan available • No credit card required", then "Create branded short links with your custom domain or use ours. Free link shortener with detailed analytics, QR codes, and API. Track every click, run A/B tests, and optimize your campaigns."
**Primary CTA:** "Create free account" (green, arrow) with "View demo" (outline, play icon). Right column is a live "Shorten your link" card showing a monospace preview `https://ozl7di5.s.gy/my-link` with a Customize button.

**Section order:** nav, two column hero with shortener card, four icon value props (Free forever plan, Custom domain support, No credit card required, Rich analytics included), "Used by Fortune 500 companies and startups worldwide" industry strip with isometric icons, "Everything you need to manage links" six card feature grid (each card has a tinted mini illustration: sparkline, browser chrome, avatar cluster, QR, code block, tag rows), "See Short.io in action" numbered stepper with screenshot, "Connect with your favorite tools" 12 tile integration grid, "Built for every team" tabs (Marketing / Sales / Infrastructure) with an analytics mock, "Trusted at scale" stat strip (animated from 0), "Loved by teams worldwide" testimonial cards with gold stars, FAQ, "Ready to get started?" CTA, footer with 20+ language switcher.

**Visual system**
- Background: light. White `#FFFFFF` with pale slate `#F8FAFC` alternate bands.
- Accent: green `#1FB07E` on buttons, links, icons, checkmarks, and a 10% tint `rgba(31,176,126,.1)` for icon chips. Secondary pastel tints per card: mint, lavender `#EDE9FE`, peach, blue.
- Text: slate scale `#0F172A` headings, `#475569` / `#64748B` body. Tailwind slate, visibly.
- Typography: Plus Jakarta Sans everywhere, H1 56px weight 700, headings weight 700 to 800. Energetic, SaaS template feel.
- Radius: 8px buttons, 10px cards, 6px inputs.
- Illustration: small isometric 3D icons for industries, flat tinted UI mini mocks inside feature cards.
- Gradients: subtle 135deg green tint on chips only.

**Analytics rendering:** the "Marketing teams" tab shows a card with overlapping area curves in green, violet and blue, a donut "Clicks" chart, a city table (Singapore 8733, Columbus 6284 ...) and three KPI pills with green percentage deltas. Dense and very "dashboard template", but it does show geo and a donut at once.
**Link-in-bio rendering:** none. Short.io does not sell a bio page.

**Best visually:** the live shortener card with the monospace preview URL, and the pricing comparison table (search box, info tooltips, sticky plan columns, "Year 1" toggle on link automation). Clear, honest, dense.
**Most generic:** the whole page is a Tailwind SaaS template: green primary, slate greys, icon chips, six card grid, integrations grid, animated counters. Nothing is ownable.

**Pricing (monthly toggle default, annual saves 17%, 19 currencies):**
- Free: $0, 1 user, 5 custom domains, 1,000 branded links, 50,000 tracked clicks/mo, 10 MB storage, $1/mo AI usage.
- Hobby: $5/mo, 7 domains, 2,500 links, 100,000 clicks/mo, country targeting, referrer hiding.
- Pro: $18/mo, 10 domains, unlimited links and clicks, password protection, expiration, cloaking, click limit.
- Team: $48/mo ("Most popular"), unlimited users, 50 domains, city targeting, deep links, end to end encryption, 99.9% SLA.
- Enterprise: $148/mo, unlimited domains, multiple teams, SSO, raw export to S3, dedicated IP.
- Gated items: user seats, domain count, link count, tracked clicks, folders (3 / 5 / 10 / 100 / unlimited), targeting features, storage. Note that 5 custom domains on Free is the most generous domain allowance of the group.

* * *

## 4. linktr.ee

**Hero headline:** "A link in bio built for you."
**Subheadline:** "Join 70M+ people using Linktree for their link in bio. One link to help you share everything you create, curate and sell from your Instagram, TikTok, Twitter, YouTube and other social media profiles."
**Primary CTA:** "Get started for free" (dark green pill on lime) and "Sign up free" (ink pill in the floating nav).

**Section order:** maroon announcement bar, floating white pill nav, lime hero with a photo of a creator holding a giant physical Linktree phone card ("Koy Sun. Lettering artist and illustrator."), royal blue band "Create and customize your Linktree in minutes" with a tilted phone mock and floating record / headphones / Spotify tile, maroon band "Share your Linktree anywhere you like!" with QR message, pale olive band "Analyze your audience and keep them engaged" with four bento stat tiles, "The only link in bio trusted by 70M+ musicians" (word rotates) with a creator avatar marquee (Selena Gomez, HBO, Comedy Central ...), three bento cards (Share every type of content / Sell products / Grow, own and engage), "The fast, friendly and powerful link in bio tool." with "Explore all plans", "As featured in..." press pills, big rounded photo with a pull quote, "Questions? Answered" FAQ, "Jumpstart your corner of the internet today" closing CTA, footer.

**Visual system**
- Background: full bleed colour bands, each section its own flat colour. Lime `#D2E823`, royal blue (approx `#2665D6`, read from the screenshot), maroon `#780016`, pale olive `#ECFEF2` / `#F3F3F1`, off white `#F3F3F1`.
- Text: ink `#1E2330`. Dark green `#254F1A` on lime, lime on blue, pink `#E9C0E9` on maroon. Every band has its own matched text colour.
- Typography: Linksans (custom), H1 80px weight 800, extremely tight. Loud and confident.
- Radius: 9999px on every button, 16px and 24px on cards, 32px on hero photo tiles.
- Illustration: none drawn. Photography of real creators, physical props, tilted phone mocks, product tiles.
- Gradients: none at all. Flat colour only.

**Analytics rendering:** the standout of the group. Four flat bento tiles in the olive band: olive tile with a lime line chart "43,500 Clicks", pink tile "643 Track Plays" with headphones icon, magenta tile "$2,362 Sales" with a dollar coin, navy tile with a flat globe and "New York, USA / 960 Visits". Each metric gets its own colour block instead of a shared chart.
**Link-in-bio rendering:** always inside a phone frame, tilted, surrounded by floating physical objects (vinyl, headphones) or shown as a printed physical card in a photo. The bio page is treated as a product you hold.

**Best visually:** the colour band rhythm plus the giant physical phone card prop. It owns lime the way Bitly owns orange.
**Most generic:** the FAQ and "As featured in" press pills, and the pricing page at 19,000px with a Kajabi monetization comparison table that reads like a different company wrote it.

**Pricing:**
- Free: $0 forever, unlimited basic links, email and phone sign ups.
- Starter: $6/mo billed annually or $8 monthly, personalized Linktree, unlimited featured links, basic analytics.
- Pro: $12/mo annually or $15 monthly ("Recommended", 7 day trial), remove Linktree branding, custom designs, sell with 0% fees, mailing list integrations.
- Premium: $30/mo annually or $35 monthly, link rules and routing, AI integrations, all time analytics, data export, social scheduling, Instagram auto replies.
- Agency or Enterprise: get in touch.
- Gated items: branding removal (Pro), analytics depth (basic / all time), routing and scheduling (Premium), data export (Premium). No custom domain or link limits are mentioned on the plan cards.

* * *

## 5. bio.link

**Hero headline:** "Your link-in-bio, now with a brain"
**Subheadline:** "Join 3M+ creators and brands using Bio Link. Add your links, share posts, send emails, and let AI greet and guide your visitors."
**Primary CTA:** a claim form: `bio.link/` input with placeholder "name" and a gradient button "Start 7-Days Free". Nav CTA is "Sign up" (black pill).

**Section order:** floating pill nav, two column hero with layered phone and card mocks (newsletter post, Spotify embed, post list), "Loved by top creators" avatar card marquee (Charly Mata, AC Milan, Flavia Gamonar ...), "Create your custom AI site in minutes" with a row of six themed phone mocks (Summer, Retro, Xmas, Basic, Rainy Night, Strawberry), "Engage every visitor. With AI, you can" with App / Website toggle and a phone on a pink to violet glow, "Next level features, unmatched value" feature list (custom domain, real time stats, embeds, multiple sites, email list, posts, QR), pricing block "All features, One simple plan" with a single gradient bordered card, testimonials grid with "+1.5 million users enjoy Bio Link" pill, "All you need, in one place" receipt style comparison (what you'd spend otherwise $84/mo vs $7.49/mo), FAQ "Got questions?", closing "Claim your bio link before it's taken" with the claim form again, footer.

**Visual system**
- Background: white, with a single large radial glow in coral to violet behind the AI section and the pricing card.
- Accent: brand gradient `#FF5858` to `#C058FF` at 126deg, used on the CTA button, the pricing card border and the glow. Spotify green `#1ED760` and blue `#007CF0` only inside embeds.
- Text: `#0D0D0D` ink, `#717171` grey, `#F4F4F4` surfaces, `#D9D9D9` borders.
- Typography: Inter Bold 72px H1, Inter throughout. Apple-ish, neutral.
- Radius: 9999px pills for buttons and eyebrow chips, 16 to 24px cards. Phones use real iPhone frames.
- Illustration: none. Six phone mocks with wildly different themes do the work, plus a "receipt" with torn paper edge and a tape strip for the price comparison.
- Gradients: yes, one brand gradient used sparingly and one big glow.

**Analytics rendering:** not shown as a visual. "Real time stats, track your site's performance" is a feature bullet only.
**Link-in-bio rendering:** the theme row is the signature: six phones side by side, each a complete different world (yellow retro buttons, cream serif, Christmas, glass dark, hot pink). Also layered cards floating out of a phone in the hero.

**Best visually:** the single plan pricing card with gradient border, and the receipt comparison that itemises what the bundle replaces. Simple, confident, slightly playful.
**Most generic:** the hero copy and Inter everything. Without the gradient it would be indistinguishable from any Apple style template.

**Pricing:** one plan. Free tier exists (implied by "Try for free" and the claim form) with Bio Link branding. Pro: $7.49/mo on the yearly toggle ("Save 50%", so roughly $15 monthly, the monthly figure was not captured). Pro includes unlimited sites and visitors, AI chat, custom domain, no branding / white label, posts and email list. Gated items: custom domain, branding removal, AI assistant, email list.

* * *

## 6. sink.cool (open source, Cloudflare native)

**Hero headline:** "Sink"
**Subheadline:** "A Simple / Speedy / Secure Link Shortener with Analytics, 100% run on Cloudflare."
**Primary CTA:** "Dashboard" (black pill) and "GitHub Repo" (ghost). Eyebrow pill: "Follow on X(Twitter)". Nav shows a live GitHub star count (7,206).

**Section order:** nav with docs, API reference, star badge, language and theme toggles; two column hero with a stock flat illustration (woman at a cafe with a giant phone, grey and black); two sponsor stickers (Cloudflare, Nuxt.js) in a sticker art style; "Features" 3x4 bordered grid (URL Shortening, Analytics, Serverless, Customizable Slug, AI Assistance, Link Control, Smart Routing, Social Preview, Near-real-time Analytics, QR Code, Import/Export, Multi-language); "Sink in Numbers" (stars, forks); "Loved by Users" masonry of embedded tweets (mostly Chinese language developer community); footer.
**GitHub README order:** badges, feature list, demo link, sibling versions (Sink on Cloudflare, Slite on Node/Docker), technologies (Nuxt, D1, KV, Analytics Engine, R2, Workers AI), roadmap, deployment, configuration, API, AI skills, MCP, FAQs, credits, license, sponsor.

**Visual system**
- Background: white (oklch 1 0 0) with a dark mode toggle. Zinc scale from shadcn: text `#18181B`, muted `#71717A`, borders `#E4E4E7`, surface `#FAFAFA`.
- Accent: none. Black buttons on white. The only colour on the page is in the sponsor stickers and the tweet avatars.
- Typography: IBM Plex Sans, H1 60px weight 500. Plain and technical.
- Radius: 32px pills on buttons, 16px cards, feature grid is a hairline bordered table with 0 radius cells.
- Illustration: one stock flat illustration, two sticker art logos. Mismatched styles.
- Gradients: none.

**Analytics rendering:** not shown on the site; described in text as "3D globe and event logs updated by periodic polling and client-side replay". Community tweets call the globe the special feature. The dashboard itself is behind the Dashboard login.
**Link-in-bio rendering:** none, Sink is shortener plus analytics only.

**Best visually:** the hairline bordered feature table and the live star badge in the nav. It is honest about being a dev tool and the tweet wall is real social proof.
**Most generic:** the shadcn default look with a stock illustration pasted into the hero. No product screenshot on the landing page at all, which for a tool whose signature is a 3D globe is a missed opportunity.

**Pricing:** none. Free, self hosted on Cloudflare Workers (D1, KV, Analytics Engine, R2 optional, Workers AI optional). Nothing is gated; limits are Cloudflare's own free tier limits.

* * *

## Cross competitor patterns worth noting

1. Every paid product gates the same four levers: link volume, analytics retention window, custom domain count, and branding removal. QR codes are free almost everywhere (Dub, Short.io, Sink) except Bitly which meters them.
2. Three of six put a working shortener or claim form in the hero (Bitly, Short.io, bio.link). The two that do not (Dub, Linktree) use a product screenshot instead.
3. Nobody in this set combines shortener analytics and a bio page in one visual. Dub and Short.io show charts, Linktree and bio.link show phones, never both.
4. Dark mode exists only on Sink. Every marketing page is light.
5. Monospace for URLs and counters shows up on Dub and Short.io and reads as developer credibility.
6. Animated counters that start at 0 (Bitly, Short.io) look broken in any static capture, including social previews.

* * *

## Mash-up design brief: Clickpath

Open source link shortener, click analytics and link-in-bio. Free self host on Cloudflare, $5/mo cloud. First audience: Omarchy and Linux developers. Must look distinct from Dub's black and white and from Bitly's orange.

### Positioning in one line
"Your links, your analytics, your page. One Worker, one repo, five dollars if you'd rather not run it."

### Visual direction: "terminal warmth"
Dark first (the only competitor that is dark is Sink, and it is dark only as a toggle). A deep ink background with a warm phosphor green accent and a soft amber secondary, so it reads as a well kept terminal rather than a neon dashboard. Hairline grid and monospace numerals borrowed from Dub, flat colour blocking borrowed from Linktree but pushed into dark tiles instead of pastel bands, and a working claim form in the hero borrowed from bio.link. No gradients on surfaces; the only glow is a soft radial behind the hero form.

### Palette
| Role | Hex | Use |
|---|---|---|
| Ink (page background) | `#0C1014` | body background, dark mode default |
| Panel | `#141A21` | cards, nav, pricing tiles |
| Hairline | `#223039` | borders, grid lines, dividers |
| Phosphor (primary accent) | `#5EE6A0` | primary buttons, live indicators, chart line, link hover |
| Amber (secondary accent) | `#F2B65A` | QR and "cloud" tier highlights, warnings, counter digits |
| Ice (tertiary) | `#7FB6F0` | geo and device breakdowns, secondary chart series |
| Fog (body text) | `#B8C4CC` | paragraph copy |
| Snow (headings) | `#F2F6F7` | headings, numerals |
| Paper (light mode background) | `#F5F3EE` | optional light theme, same accents darkened 15% |

Contrast notes: Phosphor on Ink is 11.8:1, Fog on Ink is 9.6:1, Amber on Ink is 10.4:1. All pass AA at small sizes. Do not use Phosphor on Paper for text; use `#1F8F5B` instead.

### Typography (Google Fonts only)
- **Display and headings:** Space Grotesk, weights 500 and 700. Geometric with a slight techno edge; separates cleanly from Satoshi (Dub), Bitly Display, Plus Jakarta (Short.io) and Linksans (Linktree). H1 at 64px / 1.05 line height, weight 700, tracking -0.02em.
- **Body, UI and numerals:** JetBrains Mono for every URL, counter, stat and table cell, and IBM Plex Sans for paragraphs. If a two font cap is enforced, drop Plex and set body in Space Grotesk 400 at 17px / 1.6, keeping JetBrains Mono for all data.

Rule: anything that is a URL, a number or a slug is monospace. Anything that is a sentence is not.

### Corner radius and surfaces
- Buttons 8px, inputs 8px, cards 12px, chips 9999px. No 24px plus "pillow" cards, that territory belongs to Bitly and Linktree.
- Cards are Panel on Ink with a 1px Hairline border, no drop shadows. Hover raises the border to Phosphor at 40% opacity.
- A 48px dot grid in Hairline sits behind hero and stat sections only.

### Hero layout
Two columns on desktop, stacked on mobile.
- Left: eyebrow chip "Open source · Cloudflare native · MIT", H1 "Short links, real numbers, your own page.", sub "Clickpath shortens, tracks and hosts your link-in-bio from one Cloudflare Worker. Self host for free or let us run it for $5 a month.", primary button "Deploy to Cloudflare" (Phosphor) and secondary ghost button "Try the cloud, $5/mo". Under the buttons, a one line install in monospace: `npx clickpath init` with a copy icon.
- Right: a single Panel card titled "Claim your path" containing a working form `clk.pt/` + slug input + "Shorten" button (bio.link's claim form crossed with Bitly's shortener). Below the form, three live rows: the resulting short URL in JetBrains Mono, a tiny 7 day sparkline in Phosphor, and a QR thumbnail in Amber on Ink. The card has a faint Phosphor radial glow behind it, the only glow on the page.

### Page sections in order (8)
1. **Hero** (above). One line of copy: "Short links, real numbers, your own page."
2. **Proof strip**: a hairline bordered row of four monospace counters that are real at render time (links served, clicks tracked, GitHub stars, Workers regions). Copy: "Running on 300+ Cloudflare edge locations since day one."
3. **Three product tiles** (Linktree bento, dark): Links / Analytics / Page, each a Panel tile with its own accent (Phosphor, Ice, Amber) and a real UI fragment. Copy: "Three tools that were always one job."
4. **Analytics showcase** (the signature card, see below). Copy: "Every click, where it came from, what device, in under a second."
5. **Link-in-bio showcase**: three phone frames side by side on Ink, each a different Clickpath theme (Omarchy Tokyo Night, Catppuccin, Paper), the middle one with a live click counter. Copy: "A page that looks like your terminal, or nothing like it."
6. **Self host vs cloud** comparison table in monospace with a Phosphor column for self host and an Amber column for cloud. Copy: "Same code either way. Pay us only if you'd rather not run it."
7. **Pricing**: two tiles only. Self host $0 (everything, your Cloudflare account, your limits) and Cloud $5/mo (hosted, custom domain, 3 year retention, backups, support), with a bio.link style receipt underneath showing what $5 replaces. Copy: "Five dollars. No seats, no link caps, no retention games."
8. **Developer footer block**: install snippet, API reference link, MCP server link, GitHub star button, Omarchy package line (`omarchy-pkg install clickpath`), then the FAQ as a plain monospace accordion. Copy: "Built for people who read the source."

### Signature analytics card treatment
A single Panel card, 12px radius, hairline border, with a 3 column header strip and a chart body.
- Header strip: three KPI cells divided by hairlines (Clicks, Unique, Top country). Numerals in JetBrains Mono 32px Snow, labels in 12px Fog uppercase with 0.08em tracking. The active cell gets a 2px Phosphor underline (Dub's tab strip idea).
- Chart body: one stepped area line in Phosphor with a 12% fill, no smoothing (stepped lines read as event logs, not marketing curves). Gridlines in Hairline, dashed. Hover tooltip is a Panel chip with monospace date and count.
- Right rail: a compact stacked bar for referrers in Ice and a device split as three monospace rows with inline bars. No donuts, no pie charts; those are Short.io's look.
- Live indicator: a 6px Phosphor dot with a slow pulse next to "live" in the header, matching Sink's near real time claim.
- A thin "event log" ticker runs along the bottom of the card: `12:04:31  DE  android  /launch` in monospace Fog, scrolling. This is the ownable detail: the card looks like a tail of a log file.
- Light theme variant swaps Ink for Paper and Phosphor for `#1F8F5B`.

### Three borrowed UI motifs (and from whom)
1. **Working form in the hero** from bio.link's `bio.link/name` claim form and Bitly's tabbed shortener. Clickpath puts a real shortener plus claim form in the hero card so the product is used before sign up.
2. **Hairline grid and monospace counters** from Dub's graph paper column edges and orange monospace "Built to scale" stats. Clickpath uses a Hairline dot grid behind hero and proof sections and JetBrains Mono for every counter, in Amber.
3. **Per metric colour tiles** from Linktree's four tile analytics bento (olive, pink, magenta, navy). Clickpath keeps the idea of one tile per metric but renders them as dark Panel tiles with a single accent each, so the bento reads as terminal panes rather than candy.

Honourable mention: the bio.link receipt with a torn edge is reused under pricing, redrawn as a monospace invoice block with a dashed border instead of a paper texture.

### What to avoid, explicitly
- No orange primary (Bitly), no black on white minimalism as the default theme (Dub, Sink), no lime (Linktree), no green on slate SaaS template (Short.io).
- No stock illustration (Sink), no blurred dashboard (Bitly), no counters that animate from zero.
- No gradients on buttons or cards. One radial glow behind the hero form, nothing else.
- No pie or donut charts anywhere.
