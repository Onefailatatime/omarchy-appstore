# Testimonial collection + wall of love: competitor teardown

Captured 2026-10-11 with Playwright (Chromium, 1440px viewport, full page). Firecrawl was out of credits, so every screenshot in this folder came from the local browser fallback. Files are named by domain: `<domain>.png` is the homepage, `<domain>-pricing.png` the pricing page, `<domain>-wall.png` the vendor's own public Wall of Love, and `*-wall-preview.png` a downscaled copy for quick viewing.

Trustmary note: the live site returned HTTP 522 (Cloudflare origin down) for the whole session, in both Playwright and the built-in browser. The homepage and pricing captures (`trustmary.com-wayback.png`, `trustmary.com-pricing-wayback.png`) come from Wayback Machine snapshots dated 2026-09-28 (home) and 2026-08-29 (pricing). Copy below is quoted from those snapshots.

Colour values marked "computed" were read from computed CSS on the page; others are read off the screenshot and are approximate.

House rule: no em or en dashes anywhere in this file. Two competitor headlines contain one in the original; the dash is replaced with a colon and flagged inline.

***

## 1. senja.io

**Hero headline (H1, verbatim):** "Meet Senja. The easiest way to gather customer testimonials and case studies, then share them everywhere to increase trust and sales."
The visual hero above the H1 is a large customer quote set as display text: "I've already seen a tangible impact on revenue and conversion by sharing more social proof." with the key phrase highlighted in lavender, attributed to Jay Clouse, Founder, Creator Science.
**Subheadline bullets:** "Collect text & video testimonials on autopilot, or import from 30+ platforms" / "Find the perfect one in seconds, from Slack or any browser tab" / "Turn it into a widget, video, image, popup, Wall of Love, or case study"
**Primary CTA:** "Start for free today" (nav: "Sign up for free"). Below it: five avatars, 5 gold stars, "loved by 20,000+ customers".

**Section order:**
1. Announcement bar (purple): "What's your Social Proof Score? Take the quiz"
2. Hero: quote as headline, product one-liner, 3 checkmarks, CTA, avatar row + stars
3. Logo strip (Webinar, Help Kit, FeedHive, Cal.com, pickupmusic) with a floating testimonial card overlapping the left edge
4. Two-card contrast: "You Without Social Proof" (red X list) vs "You With Social Proof" (green check list, lavender tint)
5. Collect: "Create a simple collection form in 30 seconds", 6 checks, orange gradient panel holding a collection form mockup
6. Find: "Where the f*ck is that screenshot?", dashboard screenshot
7. Share: "One testimonial, 12 ways to share it", tabbed demo (Social Videos, Widgets, Walls of Love, Popups, Testimonial Images, Video Hosting)
8. Thank: "Thank every customer like it's still day one"
9. Audience chips: "Whatever you make, Senja fits how you work" (Creators, Communities, SaaS, Agencies, Coaches...)
10. Trust: "We know testimonials drive trust, here's why people trust us"
11. Full-bleed purple CTA band: "Ready to boost your business with social proof?"
12. Footer with a row of hand-drawn purple doodles (speech bubble, star, play button, heart, card, gift)

Every section is punctuated by a single highlighted testimonial quote between blocks (yellow highlighter on the key phrase, small avatar, name).

**Visual system:**
- Background: white, alternating with very light grey (#F9FAFB-ish) bands; one full-bleed purple band.
- Accent: Senja purple #6701E6 (computed, `--color-senja`), darker #4901A4. Secondary: emerald green for checks (oklch 0.596 0.145 163), orange gradient panel (#FF8A3D to #FFB36B approx) behind the form demo, lavender #EDE4FF highlight on hero quote, yellow #FEF3C7 highlighter on inline quotes.
- Typography: DM Sans (body, computed), Bricolage Grotesque for headings (computed, 18 instances), Caveat (handwritten script) for section eyebrows like "Collect", "Find", "Share everywhere", "Thank".
- Corner radius: 8px dominant on cards and buttons, fully rounded pills for chips and avatars, 16px on larger panels.
- Illustration: hand-drawn purple line doodles (sparkle, speech bubble, gift, heart) placed in margins; product screenshots inside soft white frames.
- Gradients: yes, one orange gradient panel and 10 gradient elements total; used as a warm counterpoint to purple.

**Wall of love rendering (love.senja.io):**
- Dark mode wall: near-black background (#0A0A0A), two-column masonry of dark charcoal cards (#1A1A1A), 12px radius, no border.
- Each card: 36px avatar, name bold, role in muted grey, 5 gold stars row, body text with yellow highlighter on the key phrase, date in small grey, source badge (X or LinkedIn glyph) top-right.
- Video cards: 16:9 thumbnail with name and role overlaid bottom-left, play button bottom-right, stars overlaid.
- Purple CTA cards ("Testimonials made easy", "Sign up for free") are slotted into the masonry grid like testimonials.
- Filter pills above the wall: All Testimonials / Video / Love from SaaS / Love from creators / Love from Agencies / People who switched.
- Header is a mini landing: big quote, "Sign up. Free forever." button, and a stack of speech-bubble cards with 3px black outline, 24px radius, purple drop shadow (computed: border 3px solid rgb(0,0,0), radius 24px). This neo-brutalist bubble stack is unique to Senja.
- A floating "Collect testimonials with Senja" pill badge sits in the corner.

**Best visually:** the typographic hero. Leading with a real customer quote as the headline, with a highlighter stroke and an avatar, makes the product's output the first thing you see. Supporting that, the handwritten Caveat eyebrows and the margin doodles give it a warmth none of the others have.
**Most generic:** the alternating white/grey Tailwind band structure and the 8px radius cards; everything below the fold looks like every other SaaS page.

**Pricing page (senja.io/pricing):**
- Free: $0/month, "Free, forever". 15 video and text testimonials, collection form, invites and tracking, import from 18 platforms, testimonial analysis, case studies, Thank Yous, export, unlimited widgets (20+ templates), unlimited Walls of Love, Reels, widget analytics. Senja branding stays on.
- Starter: $29/month (yearly: 2 months free). Unlimited testimonials, 3 forms, 1 project, 2 seats, Spin the Wheel rewards, autosync, own branding (Brand Kit), custom domains, HD video exports, Pro widgets, Word of Mouth, Zapier, API and webhooks.
- Pro: $59/month. Unlimited forms, 5 projects (+$10 each), 5 seats (+$5 each), team access, rich snippets, translation into 20 languages.
- Gated: branding removal (Starter), custom domain (Starter), HD video (Starter), API (Starter), seats and rich snippets (Pro). Imports and unlimited widgets are free.
- Layout: Free plan as a full-width feature grid first, then two paid cards side by side, FAQ, purple CTA band.

***

## 2. testimonial.to

**Hero headline (verbatim):** "Capture, measure & showcase customer love" ("showcase customer love" in indigo-to-violet gradient text)
**Subheadline (verbatim):** "The fastest-growing teams turn customer love into their #1 growth channel. One platform that converts trust into revenue."
**Primary CTA:** "Start for Free" (arrow), secondary "Talk to us" with three avatars inside the button. Micro-copy: "Get started with free credits on us. See pricing."

**Section order:**
1. Nav (Customers, Features, Pricing, language picker)
2. Hero: centred headline, sub, two CTAs, then a row of product chips (Testimonials, NPS, Case Studies, Brand Monitor, Email Assistant), then an exploded collage of UI cards floating over a faint grid (inbox, NPS widget, case study, video card, email assistant)
3. "Trusted by 50,000+ businesses that value social proof" logo strip (Intuit, McKinsey, Superhuman, Acquire, Yoast)
4. Wavy divider into "Add testimonials to your website with no coding!" with a dark code card: "Try our sample embed code", 2 lines of script, buttons "Copy the code" (indigo) and "Live demo" (yellow)
5. "We started with Testimonial": feature card for the original product with sub-features and a carousel of app screenshots
6. "But we didn't stop there": 2x2 grid of product cards (Brand Monitor, Case Study, NPS, T.E.A Testimonial Email Assistant) plus a full-width MCP / AI Agents card, each tagged "Available in Ultimate"
7. "Integrate with any platform": 2x4 grid of white logo tiles (Webflow, Shopify, Carrd, WordPress, Kajabi, Bubble, Framer, Squarespace), "See all 100+ integrations"
8. Lavender CTA band: "Ready to turn customer love into growth?" with "Start for Free" and "Talk to us"
9. Footer with SOC 2 badge

**Visual system:**
- Background: white, with light lavender (#F5F3FF-ish) bands and a wave divider; the hero collage sits on a faint graph-paper grid.
- Accent: indigo #5D5DFF (computed button background rgb 93,93,255), gradient text from #5B4FE9 to violet; yellow #FEF3C7 highlighter (`--highlight-color`) on key phrases; orange CTA tiles inside the wall.
- Typography: Inter body (computed), Plus Jakarta Sans headings (computed), Inconsolata for the code block.
- Corner radius: 8px and 12px on cards, 16px on big panels, pill buttons (9999px), 50% avatars. Buttons 12px.
- Illustration: none; floating product-UI fragments do the work.
- Gradients: subtle (5 elements): gradient text in the headline, lavender wash behind CTA band.

**Wall of love rendering (testimonial.to/wall-of-love):**
- Light mode: white page, three-column masonry of white cards with 1px light grey border, 8px radius, no shadow.
- Card anatomy: avatar 36px, name bold, role grey, source icon top-right (LinkedIn blue square, X glyph, Product Hunt orange "P"), body text with yellow highlighter on key phrases, "Show more" link for long text, optional screenshot image attached below the text.
- Video cards: portrait or landscape thumbnail with indigo play button, name overlaid, and a quote strip in indigo beneath the video.
- Orange (#FF6B00-ish) CTA tiles "Sign up now and start collecting testimonials!" with a white "Sign up" button are inserted every ~8 cards.
- Stars appear only on cards that have ratings. No filter pills on the public wall.

**Best visually:** the exploded UI collage hero. Floating fragments of inbox, NPS, audio waveform, and video over a grid communicates "one platform, many surfaces" with no copy. The dark embed-code card with "Copy the code" and "Live demo" is also the most developer-friendly moment on any of the six sites.
**Most generic:** the integration logo grid and the lavender CTA band are stock SaaS; the 2x2 feature cards with "Learn more" arrows could be any product.

**Pricing page (testimonial.to/pricing):**
- Headline: "Turn happy customers into your best sales team". Toggle Billed Monthly / Billed Yearly (2 months off).
- Free: $0, forever. Unlimited X and LinkedIn imports, 2 video and 10 text testimonials total, public testimonial page, Wall of Love widgets, white-label widgets.
- Starter: $25/month ($300 billed annually). Unlimited text, 2 video total, social and review imports, white-label widgets, custom domain.
- Ultimate: $50/month per space ($600/yr), "Best value". Unlimited video, Brand Monitor 2,000 mentions, 1,000 automated invitations, eGift cards, Google rich snippets, REST API, MCP, webhooks, Zapier, team members, priority support.
- Ultimate +: $95/month per space ($1,140/yr). Case study collection, NPS surveys, AI video editor, Brand Monitor 5,000, 3,000 invitations, unlimited team, SOC 2.
- Enterprise: custom (SSO, PO/invoices, success manager).
- Gated: video count (free 2, unlimited only at Ultimate), custom domain (Starter), API/MCP (Ultimate), case studies and NPS (Ultimate +). White-label widgets are free, which is unusual.
- Layout: four cards in a row with the recommended one outlined in indigo, Enterprise as a slim full-width bar, logo strip, then a long comparison table grouped by product area.

***

## 3. famewall.io

**Hero headline (verbatim):** "Collect testimonials & reviews that keep selling for you on your website"
**Subheadline (verbatim):** "Collect text, video & audio testimonials with a simple link. Import the reviews you already have on 25+ platforms. Add everything to your website as widgets or a wall of love. No code, no developer - live in minutes."
**Primary CTA:** "Get started for FREE", micro-copy "It's 100% free to start. No credit card required!", secondary link "Or book a demo". Below: "Trusted by 10,000+ marketers, agencies & nonprofits" with an avatar row.

**Section order:**
1. Nav (Our Wall Of Love, Widgets Showcase, Features, Pricing, Blog, teal "Login in/Sign up")
2. Hero: centred headline, sub, CTA, avatar row, then a browser-framed interactive demo (Supademo) of the dashboard with a tooltip overlay
3. Three laurel-wreath testimonials (5 stars, quote, avatar, name, role)
4. "Trusted by 10,000+ businesses, from marketing teams to coaches & agencies" logo marquee (Compass, CIPR, AAHA, Chelmsford City Council, WES, WKAR)
5. "This is what testimonials do for your website": a before/after drag slider, "Without Famewall" vs "With Famewall", caption "Same website. Same traffic. More people saying yes."
6. Alternating feature rows (image left/right, teal gradient image frames): collect without chasing, video testimonials, widgets and wall of fame, import existing reviews, audio testimonials, set it and forget it
7. "Customers love us" with an AI Review Summary box, filter chips, and the embedded Famewall wall itself (video cards and text cards in masonry) with "Load more" and "Made with Famewall"
8. "What changed after they put their testimonials up?": three outcome cards
9. Agency panel: "Charge clients for testimonials. But run them all on Famewall at a flat rate."
10. "The testimonial tool that's easy for you & respects your time" dashboard shot
11. "Supports 40+ platforms you already use"
12. Share as page or video, "We care about you" founder note, FAQ, footer

**Visual system:**
- Background: white, with a teal-to-white radial gradient in the top-right corner of the hero and teal gradient image frames.
- Accent: teal/cyan #0891B2 (computed button rgb 8,145,178), darker #0E7490; indigo #4F46E5 for small eyebrow labels; gold stars.
- Typography: Lato (computed) throughout; headings in Lato bold, which reads a bit dated.
- Corner radius: 16px on image frames and cards (71 instances), 4px on buttons (unusually tight), 6px on small elements.
- Illustration: a small teal robot/wall mascot icon above section titles; laurel wreaths around hero testimonials; Supademo interactive embed.
- Gradients: 3 elements, teal and blue washes behind product screenshots.

**Wall of love rendering (wall.famewall.io/wall-of-love):**
- Light: faint graph-paper grid background, three-column masonry, white cards with 16px radius and a soft Material-style shadow (computed: rgba(60,64,67,0.3) 0 1px 2px).
- Video cards: full-bleed thumbnail with name and role overlaid bottom-right, play button bottom-left, "Made with Famewall" pill in the corner.
- Text cards: quote first, with yellow highlighter on key phrases, then 5 gold stars, date in small grey, avatar with name and role at the bottom (reverse of the usual order).
- Filter chips: All / Video Testimonials / Text Testimonials. Header has two buttons: "Send a Testimonial" (dark) and "Create your own wall of love" (teal).
- Source badges are shown on imported items (LinkedIn), otherwise none.

**Best visually:** the before/after drag slider ("Drag the slider. Same site. The only change is proof on the page.") is the clearest argument for the category on any of the six sites, and the laurel-wreath testimonial trio has personality.
**Most generic:** the long alternating image-left/image-right feature rows with a blue gradient frame; it is the default Tailwind marketing page and goes on for ~8,000px.

**Pricing page (famewall.io/pricing):**
- Headline: "Simple pricing to turn what customers say into your marketing engine". Monthly/Yearly toggle, 20% off yearly. Five cards in a row.
- Free: $0. 10 testimonials, 1 published wall, 1 collection page, 1 brand page, 1 video, 1 audio, SD video download, unlimited widget types, social proof avatars, 3rd party reviews. Struck-through: custom domain, Zapier, webhooks, API, custom branding, white label embeds, HD video.
- Standard: $12/month ($149/yr). Unlimited testimonials, 4 walls, 6 video, 6 audio, 2 min recording, HD downloads, 4 custom domains, translation, review schema, Zapier, webhooks, Make, Slack/Discord, API, white label embeds, custom branding, AI review summary.
- Professional: $25/month ($299/yr). 15 walls, unlimited video and audio, 3 min recording, 3 team members, 10 custom domains, AI Composer.
- Business: $80/month ($959/yr). Unlimited walls, 10 team members, 5 min recording, unlimited custom domains, dedicated onboarding.
- Agency: $125/month ($1,499/yr). Unlimited client workspaces, unlimited team, one console, full white-label.
- Gated: custom domain, branding removal, HD video, API and integrations (all Standard); video count (6 on Standard, unlimited from Professional); team seats; white label and client workspaces (Agency).
- Layout: five cards, "Trusted by" logo strip, then a full comparison table.

***

## 4. shoutout.io

**Hero headline (verbatim):** "Stop wasting traffic. Improve your conversion rate with testimonials." ("conversion rate" in red-orange)
**Subheadline (verbatim):** "Collect, manage, and showcase customer testimonials that build trust and drive conversions. Turn your happy customers into your best marketing team."
**Primary CTA:** "View Pricing" (large red-orange gradient button; nav button is "Get Shoutout"). Above the headline: a pill "Re-launch offer: $100 off lifetime access". Below: "5.0", "4000+ walls of love", "7-day money back guarantee", "Founded in 2020", "Newly acquired in 2025", Tiny Startups "#1 Product of the Week" and Product Hunt "#3 Product of the Day" badges, then small logos (SPI, Kit, Lovable, Notion).

**Section order:**
1. Nav (About, Blog, Use Cases, Features, Pricing, Wall of Love, Sign In, red "Get Shoutout")
2. Hero: left-aligned copy and CTA; right side a white card stack showing a video testimonial card and an X-post card, "Powered by Shoutout" footer, soft red glow blobs behind
3. "The Power of Social Proof": two cards, "Without Social Proof" (red X list) vs "With Social Proof" (green check list, warm tint)
4. "Why Pay More Every Year?": price ladder comparing Shoutout $199 once vs Senja $590/yr, Testimonial.to $400/yr, Framewall $299/yr, Shapo $290/yr, with "197% more expensive" badges
5. "Hey, we're Kyle & Mitya": founder note with two avatars
6. "Add testimonials to your website": a carousel of three X-post cards inside a glowing frame
7. Pricing inline: "Lifetime access. One-time Payment." Monthly vs Pay Once cards, FAQ accordion, one testimonial quote
8. "Loved by thousands of businesses" / "See Shoutout in action": the real Shoutout wall (video cards and X cards, three-column masonry)
9. "Integrate with any platform": 2x4 logo tiles
10. "By The Numbers": conversion calculator panel (Typical Digital Product vs After Adding Testimonials, +15% Monthly Revenue) and four stat tiles ("92% Read Reviews", "5x More Likely"...)
11. Founder video ("A quick word from Kyle, co-owner of Shoutout")
12. "Everything you need to collect & showcase testimonials": three feature tiles and two feature rows
13. Customer Success Stories, big FAQ (15 questions), final CTA

**Visual system:**
- Background: white with cream (#FFFAEB) tints and a warm off-white section; red-orange radial glow blobs behind the hero cards and the wall carousel.
- Accent: red-orange #F23118 (computed `--primary: 7 89% 52%`), accent #FF5A2E (`--accent: 14 100% 57%`), warm brown ink #30251D (rgb 48,37,29) for headings and #847062 for body, green checks.
- Typography: system UI sans (computed `ui-sans-serif`), no custom font loaded; headings are heavy and tight.
- Corner radius: 8px cards, 9999px pills (36 instances), 6px buttons.
- Illustration: emoji used as icons in buttons and eyebrows ("💰 View Pricing", "⚡ Get Shoutout"), Product Hunt and Tiny Startups badges.
- Gradients: heavy (21 elements): red-orange button gradients and several radial glow blobs.

**Wall of love rendering (homepage #testimonials and the carousel):**
- Light: three-column masonry of white cards, 1px light border, 8px radius, no shadow.
- Cards reproduce the X post faithfully: avatar, name, @handle, X glyph top-right, post body with @mentions and links in red-orange, attached screenshot image, heart count and date in the footer. LinkedIn and plain cards drop the handle.
- Video cards: landscape thumbnail with native video controls, name and role header, date below.
- "Made with Shoutout" badge bottom-right. Carousel version (section 6) shows three cards with arrows and a glowing frame.

**Best visually:** the X-post fidelity in the wall. Shoutout cards look exactly like the tweets they came from, which is the most trustworthy rendering in the set, and the "Why Pay More Every Year?" ladder is a bold, scannable comparison block.
**Most generic:** system font, emoji-as-icons, and the stock 2x4 "Integrate with any platform" tile grid (near-identical to testimonial.to's); the page is also very long (17,700px) with three FAQ blocks.

**Pricing page (shoutout.io/pricing):**
- Headline: "Lifetime access. One-time Payment." Sub: "No monthly fees. 100% money back guarantee within 7-days."
- Monthly: $15/month (struck $29, "48% OFF"). Up to 3 websites/projects, unlimited video and text, unlimited embeds, unlimited published walls, custom branding, remove Shoutout branding, cancel anytime.
- Pay Once: $199 one-time (struck $299, "33% OFF", "Most Popular"). Same limits, remove branding is +$50 one-time, includes 2 years of updates.
- Gated: nothing by feature except branding removal on lifetime (+$50); the limit is 3 projects. No free tier.
- Layout: two cards, five-question FAQ, one testimonial, footer. Shortest pricing page of the six.

***

## 5. trustmary.com (Wayback snapshots, live site down)

**Hero headline (verbatim, en dash in the original replaced with a colon):** "Turn customer feedback into visibility: let AI sell for you"
Eyebrow: "AI VISIBILITY THROUGH CUSTOMER EXPERIENCE"
**Subheadline (verbatim):** "Start with a free AI visibility baseline report. It shows how often ChatGPT, Gemini, Claude and Google AI Overviews recommend your business today."
**Primary CTA:** "Order the free report" (yellow pill). Checks: "How often each model mentions you", "Which competitors come up and why", "Recommended actions in priority order", "Free, and the report is yours to keep". Trust row: Secure, GDPR compliant, Made in Finland. Nav CTAs: "Book a demo", "Start for free".

**Section order:**
1. Hero: two-column, serif headline left, image/report preview right, on cream
2. Full-bleed yellow band: "More mentions in AI, better conversion on your site"
3. "TRUSTED BY 1800+ COMPANIES ALL OVER THE WORLD" logo strip
4. Stats grid: "AI search is already the start of the buying journey" (50%, 70%, 44%, 60-65%, 300%, 2x) with sources line
5. "A typical customer buying journey with AI": three yellow step tiles
6. "Three stages, three kinds of question": three columns
7. "What are the answers built from?": three content types, cream band
8. "Which sources sit behind the content?": six-cell source matrix with one cream highlighted cell
9. "Why is Trustmary such a strong source?": comparison table Trustmary vs Review sites
10. "How does Trustmary work?": Collect / Understand / Show, three columns with yellow pill CTAs
11. "What is the Trustmary profile page?": three pastel cards (lilac, mint, lavender) with circular icons
12. "Openness and authentic customer data..." text block plus two stat cards (41.76%, +90%)
13. Full-bleed yellow band: "Trustmary benefits", six benefit tiles with circular icons
14. "Case studies show real life results": tabs and four case cards
15. "What kind of companies is Trustmary for?": three pastel audience cards
16. Inline pricing: "AI visibility from EUR 1,990 a year" four tiers
17. Integrations, "We are here to help!" support block, final CTA, mission statement, footer

**Visual system:**
- Background: cream #FFF9E5 (computed rgb 255,249,229) and white, with full-bleed marigold bands.
- Accent: marigold yellow #FFC907 (computed rgb 255,201,7); pastel card tints lilac #F4F0FF, mint #EEF7F3, lavender #F4F6FC; deep purple #3D2277, forest #144C46, navy #1D3A6D for icon circles; ink #2A2A2A.
- Typography: Instrument Serif for headings (computed on H1), a geometric sans (DM Sans-like) for body. The serif gives it an editorial, Scandinavian feel.
- Corner radius: 16px on cards (44 instances), 25px pills on buttons, 8px minor.
- Illustration: none; circular icon badges and flat colour tiles carry the page.
- Gradients: none visible. Flat colour blocks throughout.

**Wall of love rendering:** Trustmary does not lead with a wall. Its widgets are review carousels and star-rating bars (Google-style), and its public artifact is a "Review Page" / AI-optimised profile page rather than a masonry wall. The homepage snapshot shows no testimonial wall at all; social proof appears as stat tiles, logos, and case-study cards. Treat Trustmary as the "review platform + NPS survey" end of the category, not the wall-of-love end.

**Best visually:** the colour system. Cream, marigold and three pastel tints with a serif display face is the most distinctive and least "SaaS template" palette of the six, and the full-bleed yellow bands make the long page scannable.
**Most generic:** the sheer density of stat grids and three-column explainer blocks; by the sixth three-column section the rhythm is monotonous, and the page has no product UI at all.

**Pricing page (trustmary.com/pricing, Wayback 2026-08-29):**
- Toggle "Pay annually, save -14%" / "Pay monthly", currency picker.
- Solo: free. 5 monthly survey responses, 200 monthly widget views. Import reviews, add reviews to website, collect feedback and reviews, Review Page. "Start for free, no credit card required".
- Build Your Plan: from $26/month. 10 responses, 5,000 widget views, auto-import, schema markup.
- Starter: $203/month ("Recommended"). 10 responses, 5,000 views, 3 review connections, custom surveys, analytics, premium support.
- Business: $463/month. 50 responses, 25,000 views, 10 review connections, lead generation, whitelabel, premium integrations.
- Add-ons (per month, billed annually): AI Visibility Profile Page +$197, Review Connections +$10, Whitelabel +$19, Custom surveys +$10, Premium Integrations +$98, Lead generation forms +$29, Analytics +$59, Experiments +$29, Premium Support +$98, HR package +$59, Review Translations +$10, Onboarding package $990 one-off.
- The newer homepage snapshot (2026-09-28) lists annual EUR tiers instead: AI Visibility EUR 1,990/yr, Starter EUR 2,990/yr, Business EUR 5,590/yr, Enterprise EUR 9,990/yr. Pricing appears to be mid-transition.
- Gated: metered on widget views and survey responses rather than features; whitelabel, imports (connections), and translations are paid add-ons. Video is not a headline feature.
- Layout: free Solo as a slim bar on top, three cards with the middle one raised, "View add-ons" expander into a 4x3 add-on grid, FAQ.

***

## 6. vouchfor.com

Note: Vouch has pivoted away from customer testimonials. The site now sells employee-story video for Employer Brand and Internal Comms teams. It is included for its visual system, which is the most "warm editorial" of the six, but it no longer has a wall-of-love product.

**Hero headline (verbatim):** "Your employees have great stories. Give them the tools to tell them."
**Subheadline (verbatim, em dash in the original replaced with a colon):** "The platform Employer Brand and Internal Comms teams use to collect, edit and share employee content: with AI that does the heavy lifting."
**Primary CTA:** "Book a demo" (slate pill), secondary "Take a 5-min tour". Nav: "Book a demo", "Sign in".

**Section order:**
1. Nav with mega-menus (Products, Teams, Pricing, Customers, Resources); a top ticker of three blog headlines
2. Hero: centred serif headline, sub, two pill CTAs, then a dark-framed product video (library grid of employee videos)
3. "Trusted by 1,000+ people teams globally" logo marquee (Culture Amp, Marstons, MongoDB, Warner Bros Discovery, NRMA, GoDaddy)
4. "Why teams choose Vouch": four image tiles on sand with short copy
5. Full-width customer quote on a pale green wave background with a portrait video (Jackie Denner, MongoDB)
6. "Vouch platform overview": sticky-scroll product chapters (Content, Advocacy, Recruiter) with serif headlines, lots of whitespace
7. "Introducing Ask Vouch": AI section
8. "Built for the teams doing the work": two audience columns
9. "Explore our insights & updates": blog cards
10. "Ready to make employee stories work harder?" CTA, footer

**Visual system:**
- Background: cream #F9F6F1 (computed body rgb 249,246,241), sand #F3ECE2 tiles, pale green #EEF3F0 wave section.
- Accent: slate blue #44607B (computed `--swatch--brand`), hover navy #001D39, amber #F7B139 (tertiary button), ink #212121, muted #64748B.
- Typography: Martina Plantijn (serif, computed) for headings, Inter Variable for body. Serif headings at large sizes with tight leading.
- Corner radius: 16px on cards and video frames, full pill (1440px) on buttons, 8px minor.
- Illustration: small line glyphs (sun, compass, grid) as section markers; portrait photography of real employees.
- Gradients: almost none (2); flat cream surfaces and a soft wave shape.

**Wall of love rendering:** none on the current site. Testimonials appear as a single full-bleed quote with a portrait video and a three-up quote row on the pricing page (serif quote, name, role, company logo). Historically Vouch rendered video testimonials in a rounded-portrait "Vouch player" carousel; that is gone from the marketing site.

**Best visually:** the warm editorial typography. Serif display headlines on cream with slate pill buttons reads like a magazine, not a dashboard, and the big single-quote-plus-portrait section is a more dignified testimonial treatment than any masonry wall here.
**Most generic:** the sticky-scroll "platform overview" chapters with enormous empty space, and the blog-card section; both are Webflow template moves.

**Pricing page (vouchfor.com/pricing):**
- Headline: "Loved by talent teams of all sizes". No public prices anywhere.
- Vouch Content (base, "Recommended"): unlimited video collection and creation, basic templates, enterprise security (SSO, SOC 2, GDPR, CCPA, HIPAA), 5 admin seats. CTA "Get Started".
- "Build Your Plan" add-on modules: Employee Advocacy (New), Recruiter Enablement (tiered), Ask Vouch (AI editing and MCP), Custom Brand Kits. CTAs "Chat to the team", "See it in action", "Explore options".
- Gated: everything beyond the base is sales-led; branding is sold as "Custom Brand Kits".
- Layout: one wide slate-blue header card, three add-on cards with coloured top-left glyphs, a brand-kit bar, FAQ, three customer quotes, CTA.

***

## Cross-competitor patterns worth knowing

- Five of six use a white page with one accent colour and Tailwind-era 8px to 16px radii. Only Trustmary (cream + marigold, serif) and Vouch (cream + slate, serif) break the pattern, and both are the most memorable.
- Every wall of love is a masonry grid of cards with avatar, name, role, star row, highlighted phrase, date, and a source glyph (X, LinkedIn, Product Hunt, G2, Google). Video cards use a thumbnail with name overlaid and a play button. CTA tiles inserted into the grid (Senja purple, testimonial.to orange) are a conversion trick worth copying.
- Yellow highlighter on the key phrase of a quote appears on Senja, testimonial.to, Famewall, and Shoutout. It is now a category convention, so Kudowall should do it in a non-yellow colour or do it differently.
- "Without X / With X" two-card contrast appears on Senja and Shoutout almost identically.
- Free tiers cap testimonials (Senja 15, testimonial.to 10 text + 2 video, Famewall 10, Trustmary 5 responses/month). Branding removal is the universal paid gate ($12 to $29/month, or Shoutout +$50 once). Custom domain is the second gate. Video count is the third.
- Embed story is told with a dark code card (testimonial.to) or logo tile grids (testimonial.to, Shoutout, Famewall). Nobody shows the widget in multiple visual themes side by side.

***

## Mash-up design brief: Kudowall

Product: open-source testimonial collection and wall-of-love widget. Free self-host, $7/month cloud. First audience: Omarchy and Linux developers who ship side projects; the wall widget itself has to look great on any founder's marketing site, so the site should be lighter and warmer than typical dev-tool black-and-neon.

### Positioning line
"Collect kudos. Pin them on your wall. Own the whole thing." Kudowall is the only tool in this set where the wall is yours: self-host it, theme it, and never pay for branding removal.

### Palette

| Token | Hex | Use |
|---|---|---|
| Paper | #FBF7F0 | Page background. Warm off-white, close to Vouch cream but a touch brighter |
| Card | #FFFFFF | Testimonial cards and panels |
| Ink | #1C1A17 | Headlines, body on paper |
| Muted | #6B645C | Roles, dates, secondary copy |
| Line | #E7DFD3 | 1.5px card borders and dividers, warm grey not cool grey |
| Moss | #2E6B4E | Primary accent: buttons, links, source chips, section eyebrows |
| Moss deep | #1F4D37 | Button hover, dark CTA band |
| Apricot | #F6A96B | Highlighter stroke on key phrases, secondary CTA, hero accent |
| Apricot wash | #FDE9D6 | Highlighter fill behind text, soft tints on contrast cards |
| Star | #F5B301 | Star rows only; never used elsewhere so stars stay recognisable |
| Mint wash | #DCEFE4 | "With Kudowall" card tint, success states |
| Terminal | #14201A | Dark code card and dark wall theme background, moss-tinted black rather than pure black |

Why: no competitor owns green. Senja purple, testimonial.to indigo, Famewall teal, Shoutout red-orange, Trustmary yellow, Vouch slate. Moss on warm paper reads "grown, trusted, open source" and sits well on both a founder's SaaS page and a Linux user's site. Apricot replaces the category's yellow highlighter so Kudowall quotes are recognisable at a glance.

### Typography (Google Fonts)

- Headings: **Fraunces** (variable, use the "soft" optical axis at display sizes, weight 600, tight leading). Gives the warm editorial feel of Trustmary and Vouch without copying Instrument Serif or Martina Plantijn.
- Body and UI: **Instrument Sans** (400 and 500, with tabular numerals for dates and counts). Clean, slightly narrow, friendlier than Inter and not DM Sans (Senja).
- Code snippets use the system monospace stack, styled in the Terminal card; no third web font.

### Hero layout

Two-column on desktop, stacked on mobile.
- Left (55%): eyebrow in small caps moss "Open source. Self-host free." Headline in Fraunces, 64px: "Put the nice things people say to work." Sub in Instrument Sans 20px: "Collect testimonials with one link, import the ones you already have from X, LinkedIn, G2 and GitHub, and pin them on a wall that matches your site. Host it yourself for free, or let us run it for $7 a month." Two CTAs side by side: moss pill "Start on cloud, $7/mo" and outlined pill "Self-host it (free)". Beneath: a Terminal card with a single install line (`npx kudowall init` or the Docker one-liner), copy button, and the GitHub star count as a live chip.
- Right (45%): a real, live Kudowall wall at reduced scale, three columns of kudo cards gently drifting upward in a slow marquee, with one card lifted and tilted 2 degrees as if just pinned. An apricot "pinned" tack dot on the lifted card. This is the Senja move (product output as the hero) crossed with testimonial.to's floating collage, but using the actual widget rather than a mockup.
- Background: paper, with a faint 24px dot grid (not a line grid, to avoid Famewall and testimonial.to) fading out below the fold.

### Page sections in order

1. **Hero** as above. "Put the nice things people say to work."
2. **Walls in the wild**: horizontal marquee of six real Kudowalls embedded on real founder sites, each in a tiny browser frame, in six different themes. "One widget, six sites, zero of them look like a template."
3. **Collect**: split row, left copy, right a collection-form card in Apricot wash. "Send one link. Get text, video, or a voice note back. No login for your customer, ever."
4. **Import what you already have**: a row of source chips (X, LinkedIn, G2, Product Hunt, GitHub issues, App Store, Google) feeding into one card. "Paste a tweet URL or a G2 link and the card is built for you, with the source badge intact."
5. **Show it off**: the signature section. A Kudowall on the left and a theme switcher on the right (Paper, Terminal, Omarchy Tokyo Night, Catppuccin, your own CSS). Below it the before/after slider. "Drag the handle. Same page, same traffic, now with proof next to the button."
6. **Embed anywhere**: Terminal card with the three-line embed, tabs for Script tag, React, Astro, Hugo, WordPress. "Three lines, any stack, no build step. Under 12 KB."
7. **Self-host or cloud**: two pricing cards only. Free self-host (everything, forever, MIT) and Cloud $7/month (we host, back up, serve video, custom domain, same features). A line underneath, in the Shoutout spirit but without naming competitors: "No branding fee. No per-wall cap. No video tier." Then a small "What the others charge for" list: branding removal, custom domain, HD video, API, with moss checks on both Kudowall columns.
8. **Our own wall + FAQ + final CTA**: Kudowall's wall of kudos from early users and contributors (a GitHub contributor card is a kudo card too), six FAQs (self-host requirements, data export, video storage, license, does it work on static sites, can I remove the badge: yes), then a moss-deep full-bleed band: "Pin your first kudo in five minutes." with both CTAs.

### Signature wall-of-love card treatment ("kudo card")

- Card: #FFFFFF on Paper, 14px radius, 1.5px Line border, plus a hard offset shadow 3px 3px 0 #E7DFD3 (a softened nod to Senja's 3px-outlined bubbles without the black). On hover the card lifts 2px and the shadow goes apricot. In the Terminal theme the card is #1B2A22 with a 1px #2E6B4E border and no shadow.
- Top row: 36px avatar with a 2px Paper ring, name in Instrument Sans 500, role and company in Muted 13px. Top-right: a 22px circular source chip in moss outline with the platform glyph (X, LinkedIn, G2, GitHub, Product Hunt, Google, Email). Imported posts keep their original handle and date.
- Stars: 5 x 14px in Star gold, only when a rating exists; never fake a 5-star row.
- Body: Instrument Sans 15px/1.5, with the key phrase marked in Apricot wash with a slightly rotated (minus 1 degree) highlighter block so it reads hand-marked rather than a CSS mark tag. The author or owner picks the phrase; it is also the line used in the compact widget.
- Footer: date in tabular numerals, an optional tiny "Verified" moss check with tooltip (collected via Kudowall link or imported from a public URL), and, in free self-host, no badge at all. Cloud shows a small "kudowall" wordmark in Muted that the user can turn off.
- Video kudo: 4:5 thumbnail with 14px radius, name and role in a Paper-coloured pill bottom-left, moss play button bottom-right, the chosen quote line beneath the video in Fraunces italic 17px.
- Pinned card: any card can be "pinned" by the owner; pinned cards get an apricot tack dot top-left and sit first in the grid. This is the Kudowall-only motif that ties the name to the visual.
- Grid: CSS masonry, 3 columns desktop, 2 tablet, 1 mobile, 16px gap, with an optional CTA card (Moss deep, Paper text) slotted in every ninth position, like Senja's and testimonial.to's inserted sign-up tiles.

### Three UI motifs borrowed, and from whom

1. **Quote-as-headline hero with hand-marked highlight, from Senja.** Senja opens with a real customer quote in display type with a highlighter stroke, and uses handwritten Caveat eyebrows and margin doodles. Kudowall borrows the highlight stroke (in apricot, rotated minus 1 degree) and the warm hand-drawn feel, but keeps the real wall as the hero visual instead of a quote.
2. **Before/after drag slider, from Famewall.** "Without Famewall / With Famewall" with the caption "Same website. Same traffic. More people saying yes." is the clearest category argument in the set. Kudowall reuses the mechanic in section 5 with a moss handle and the caption "Same page, same traffic, now with proof next to the button."
3. **Dark embed-code card with Copy and Live demo buttons, from testimonial.to.** Its "Try our sample embed code" card with a copy button and a yellow "Live demo" button is the only developer-native moment across all six sites. Kudowall makes it the Terminal card in the hero and again in section 6, with framework tabs and the live GitHub star chip.

Honourable mention: Shoutout's "Why Pay More Every Year?" price ladder is the model for section 7's "What the others charge for" list, without naming competitors on the page.

### Things to avoid (seen too often across the six)
- Alternating white/grey band layout with image-left/image-right feature rows (Famewall, Senja, Shoutout).
- The 2x4 white logo-tile integration grid (testimonial.to, Shoutout).
- Yellow highlighter (four of six); use apricot.
- Emoji as icons (Shoutout); use 1.5px moss line glyphs.
- A page longer than ~7,000px at 1440 wide; Famewall and Shoutout are 18,000px and fatigue sets in halfway.
