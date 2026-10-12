# Feedback board + roadmap + changelog: competitor teardown

Date: 2026-10-11. Scope: canny.io, featurebase.app, headwayapp.co, getbeamer.com, fider.io, nolt.io.
Method: Firecrawl CLI was out of credits (and rate limited by sibling jobs), so every page was loaded in the built-in browser at a 1280x4800 viewport, computed styles were read from the DOM with JS, and the viewport screenshot was saved as PNG. Screenshots sit next to this file, named by domain (800x3000, top ~4800px of each homepage). Hex values below are converted from computed rgb() values, so they are exact. Pricing was read from each site's live pricing page on the same day.

Note on verbatim copy: where a competitor's own copy contains a dash, it has been replaced with a comma or colon here and marked [dash in original], because this file carries no dashes.

***

## canny.io

**Hero**
- Eyebrow (this is the actual h1, 14px, indigo): "AI-powered customer feedback platform"
- Headline (h2, 48px): "Build the features that close deals"
- Subheadline: "Canny uses AI to read every sales and support conversation and shows you what to build to retain customers and drive revenue growth"
- Primary CTA: "Get started free" (indigo filled, arrow glyph). Secondary: "Request a demo". Microcopy: "No credit card required".
- Hero right side: floating pill tags ("SALES CALL", "LIVE CHAT") drifting over an empty field, a lightweight animated motif.

**Section order**
1. Announcement bar (dark, "Canny MCP")
2. Hero (left aligned text, two CTAs)
3. Logo wall, "Trusted by both industry leaders and startups" (ahrefs, CircleCI, Hive, Axios, ClickUp, Harness, Strapi, Missive)
4. Tabbed feature switcher "Turn customer conversations into revenue" (Capture / Enrich / Organize / Prioritize / Close the loop), each with a product crop and a customer quote card
5. Full-bleed lavender testimonial band with a cutout portrait
6. "Built for the teams that drive revenue": four persona tiles (Product, Sales, CS, Marketing) beside floating mini UI cards arranged on a dotted orbit
7. "Turn feedback into customer insights that drive revenue": one wide chart card plus two half-width cards (lavender and sky blue) with hand-drawn style UI chips
8. "Make customers feel heard": four feature bullets plus stacked product cards
9. "The customer feedback platform behind thousands of revenue teams" (stats / customer stories)
10. "Works well with your existing workflow" (integrations)
11. "Here's why thousands of teams count on Canny" (review wall)
12. Final CTA "Start turning feedback into revenue today"
13. Footer (large, 5 columns)

**Visual system**
- Background: light, pure white #ffffff with pale lavender #f2f3ff and sky #cee7fe section cards
- Accent: indigo #525df9 (buttons, active tab, links), darker hover #414ce7; text near black #202020, grey #646464
- Typography: Inter everywhere, medium weight, tight tracking. Clean, corporate, geometric sans
- Radius: 12px buttons and cards, 6 to 8px on chips, pill 50px on tags
- Illustration: real product screenshots cropped into cards, plus flat line icons and "hand written" monospace chips (SALES CALL, in progress). Cutout photo of a customer in the testimonial band. No 3D
- Gradients: none in CSS. Flat colour bands only

**Best thing**: the tabbed Capture / Enrich / Organize / Prioritize / Close the loop switcher. It compresses the whole product story into one interactive strip and the pastel chips floating on an orbit (section 6) give the page a hand-made feel inside an otherwise corporate layout.

**Most generic**: Inter plus indigo plus white is the default 2024 B2B SaaS look; swap the logo and it could be any PLG tool.

**Pricing (canny.io/pricing)**
- Headline: "Canny costs less than building the wrong features". Yearly / Monthly toggle, 20% off yearly
- Free: $0, 25 tracked users, automatic feedback capture, unlimited feedback, 5 managers
- Pro: from $79/mo billed yearly, 100+ tracked users, PM integrations, advanced privacy, 10 managers. Marked "Most popular"
- Business: "Let's talk", 5,000+ tracked users, SSO, CRM integrations (HubSpot, Salesforce), custom roles
- Unit: "tracked user" (anyone who gave feedback). A slider from 25 to 5k+ changes the price live. Optional spend limit
- Gated upward: private boards, custom domains, remove branding, email whitelabel, automation rules, custom statuses, SOC 2, pay by invoice
- Long comparison table, then FAQ, then B2C and non-profit side notes

***

## featurebase.app

**Hero**
- Eyebrow pill: "We're hiring! Join our team"
- Headline (h1, 48px, medium weight): "Modern customer support & feedback platform"
- Subheadline: "Support your customers with AI, collect feedback, and announce product updates [dash in original] all with one tool"
- Primary CTA: "Get started - free" (white filled on black). Secondary: "Get a demo" (ghost)
- Below the hero: a five-tab product switcher (Support / Feedback / Help Center / Product Updates / Customers) driving a huge dark product screenshot with a purple glow behind it

**Section order**
1. Nav (dark, "Start for free" white button)
2. Centered hero
3. Tabbed product viewer, full width
4. Logo wall "Powering the world's leading startups and enterprises" (nature, Polymarket, Raycast, Elementor, n8n, OpenSea, Mercor, Instantly, beehiiv, Profound)
5. "Support your customers with AI": big screenshot card, then 3 feature columns (Omnichannel inbox / AI support agent / Workflows)
6. Testimonial card (Rize)
7. "Build better products with customer feedback": same screenshot plus 3 columns layout
8. "Connect with your favorite tools"
9. "Intelligent documentation for self-serve support" (same pattern)
10. "Keep users updated with product changelogs" (same pattern)
11. "Collaborate across teams to move fast" (Support / Product / GTM)
12. "The support & product platform for the next generation"
13. "Scale with security"
14. Final CTA "Start building products your users love"
15. Footer

**Visual system**
- Background: dark, near black #050608 with panel surfaces #101219 and #16181f, hairline borders at 5% white
- Accent: electric violet #7064f2 and purple #a855f7 glows; text #dee1ea, muted #b2b8cd
- Typography: Inter, medium weight headings, generous tracking. Neutral geometric sans
- Radius: 12 to 16px cards, 24px on large frames, 9999px pills, 6px on small controls
- Illustration: full dark-mode product screenshots in bordered frames, small line icons, radial violet glow behind the hero image. Dotted grid texture on the testimonial card
- Gradients: yes, 13 gradient backgrounds (radial glows and fade masks on screenshots)

**Best thing**: the dark product frame with a soft violet aurora behind it. The hero screenshot feels like a device sitting in a lit room, and the repeated "big screenshot, then three columns" rhythm is easy to scan.

**Most generic**: it is the Linear / Vercel dark template almost beat for beat (Inter, black, violet glow, hairline cards). Every section uses the same block so the page feels long and samey.

**Pricing (featurebase.app/pricing)**
- Headline: "Flexible plans that grow with you". Per seat, billed yearly, "Show features for: Helpdesk / Feedback" toggle. Feedback is bundled into every tier
- Free: 1 seat, live chat, unlimited conversations, inbox, mobile app, includes Feedback
- Growth: $29/seat/mo + $0.49 per AI resolution, AI agent, email, API/MCP/webhooks, integrations
- Professional: $59/seat/mo, Slack support, workflows, SLAs, Salesforce/HubSpot, multilingual, 20 Lite seats
- Enterprise: $99/seat/mo, multi-brand, SSO, custom admin roles, Azure DevOps, invoicing, 50 Lite seats
- Startup program: 86% off for companies under 2 years and under 6 people
- Interactive savings calculator vs Intercom / Zendesk / Freshdesk / Help Scout, then a long comparison table with animated odometer digits

***

## headwayapp.co

**Hero**
- Hidden h1 (nav label): "Headway - Changelog for your web-app"
- Visible headline (h2, large, navy): "Easiest way to keep your customers in the loop about your product."
- Subheadline: "Every update that you can share with your users, you should. They will love you for this, we promise."
- Primary CTA: "Create your changelog" (royal blue pill)

**Section order**
1. Minimal nav (Pricing, Our changelog, centered logo, Your account)
2. Hero, left aligned, single CTA
3. Two-up demo panel: "Public changelog page" (browser mock with New / Fix / Bug tags) and "In-product widget" (badge with a red "2" counter), plus "Check out existing changelogs" links (Buffer, Honeycomb, Superhuman, Travis CI)
4. "But wait, there's more." Eight plain text feature blurbs in a 3 column grid (Custom branding, Integrations, Teams, Scheduled publishing, Privacy, Custom categories, Eyecatcher, Markdown editor)
5. Six testimonial cards with highlighter-marked phrases and tiny company logos
6. "Pricing." Two cards, Free and Pro, with floating confetti shapes behind Pro
7. Footer (address and legal only)

**Visual system**
- Background: light, white #ffffff with a faint grey #f6f7f8 panel band
- Accent: royal blue #0054ff on the CTA, navy text #131431 at 60 to 90% opacity, tag colours sky #1ed1f3 (New), blue (Fix), purple (Bug), red badge
- Typography: Graphik Web (humanist grotesque), 17px body, weight 400. Soft, friendly, almost editorial
- Radius: 50px pill buttons, 3 to 5px on tags and cards, 18px panels
- Illustration: schematic grey-bar wireframes of the product instead of real screenshots, one tiny flat people illustration, confetti dots and triangles behind the Pro card
- Gradients: none

**Best thing**: the marker-pen highlight inside testimonials (key phrase of each quote painted in pale blue) and the wireframe demo that shows the whole product in one glance without a screenshot. Also the shortest page in the set, which reads as confidence.

**Most generic**: the eight-blurb feature grid is just text; there is nothing to look at between the demo and the testimonials. The page has not changed in years.

**Pricing (on the homepage, /pricing is a 404)**
- Free: unlimited changelogs, public page customization, widget customization, custom categories, Eyecatcher
- Pro: $29/month: whitelabel, custom domain, all integrations, team management, search engine privacy, private changelog, scheduled publishing, plus all Free features
- Two tiers only, no per seat, no comparison table

***

## getbeamer.com

**Hero**
- Headline (h1, DM Serif Display, 56px): "A modern changelog for today's best-in-SaaS"
- Subheadline: "Inform and educate your customers with two-way communication that allows you to learn what customers love [dash in original] and what they need."
- Primary CTA: inline email capture with "START FOR FREE" (black, uppercase). Nav CTA also "START FOR FREE"
- Hero right: product crop "Collect new ideas" on a saffron yellow panel with orange ring doodles

**Section order**
1. Nav (black uppercase CTA, "Beamer by Userflow" lockup)
2. Hero with diagonal yellow wedge
3. "Why Beamer's customer communication platform?" four benefit tiles (Amplify reach, Increase engagement, Boost adoption, Improve satisfaction)
4. "Loved by 20,000+ product and marketing teams." logo wall
5. Alternating feature rows with eyebrow labels: CHANGELOG, IN-APP NOTIFICATIONS, NPS SURVEY, FEEDBACK, each with a wireframe illustration and an outlined orange "Learn about" button
6. Full-bleed yellow testimonial bands between feature rows (two of them, with headshot and logo)
7. Black stats band "POV: You're a Beamer customer" (520% ROI, 3x engagement, 40% churn reduction)
8. Black "Here's how easy it is to get started." three steps
9. "Get more out of your product releases." final CTA
10. Big footer with About / Products / Alternatives / How to / Resources / Docs
- Sticky vertical "Feedback" tab on the right edge (their own widget)

**Visual system**
- Background: light, white with saffron #ffcb1f and orange #ff8b00 bands, pale blue grey #deecef and #f6fafb panels, black #1c1e21 bands
- Accent: orange #ff8b00 on outlined buttons and eyebrows, yellow #ffcb1f; body text #1c1e21
- Typography: DM Serif Display for headlines (high contrast serif, bold) with Lato for body. The only serif in the set
- Radius: small, 4 to 5px on buttons, 8 to 12px cards, circles on avatars
- Illustration: grey wireframe browser mocks in a blue grey card, orange line doodles (rings and scribbles) over the yellow panels, flat yellow icons
- Gradients: none

**Best thing**: the serif headline against saffron and black bands. It is the only site that does not look like a software template, and the alternating yellow / white / black rhythm makes a long page feel paced.

**Most generic**: the grey wireframe placeholders stand in for product shots so you never see the actual changelog, and the "520% ROI" black stat band is boilerplate.

**Pricing (getbeamer.com/pricing)**
- Headline "Pricing & Plans". Monthly / Annual toggle
- Free: $0, under 1,000 MAU, 1 teammate, Beamer branding, 1 language
- Starter: $59/mo ($49 annual), 5,000 MAU, in-app and standalone changelog, boosted announcements, analytics
- Pro: $119/mo ($99 annual), 10,000 MAU, dedicated inbox, comments and reactions, basic segmentation. "Most popular"
- Scale: $299/mo ($249 annual), 50,000 MAU, advanced segmentation, user activities, staging account
- Custom: get in touch
- Unit: Monthly Active Users. Feedback board and roadmap are a $99/mo add-on (Free tier of the add-on is public only; Pro add-on gets private boards, priority score, moderation). NPS is another $99/mo add-on
- Gated upward: custom domain and CSS at Pro, SSO / audit logs / SOC2 at Scale, custom sender domain at Pro
- Comparison table, add-on cards, cross-sell block for Userflow onboarding, FAQ

***

## fider.io

**Hero**
- Eyebrow pill: "#1 Product Feedback Tool"
- Headline (h1, Unigeo, 64px, bold): "Wanna Manage All Those Feature Requests Properly?"
- Subheadline: "Give your customers a place to submit feedback, create feature requests, and vote on your product direction. Fider is all your product feedback in one place. Like your to-do list, but crowdsourced from the people who use your product."
- Primary CTA: "Get Started For Free" (mustard yellow, black outline, hard shadow). Nav CTA: "Sign up - it's free"

**Section order**
1. Nav (Home, Pricing, Blog, yellow sign up)
2. Hero on a pink field with blue and yellow diagonal wedges, blobby outlined shapes and a paper plane doodle
3. "All Your Product Feedback In One Place": centered copy with an underlined phrase, a yellow CTA, a cutout photo of a person giving two thumbs up over a blue blob
4. Beige testimonial band with a hand-drawn yellow ticket graphic (Joel Bethke, Security Analyst)
5. Four alternating "how it works" steps, each with a big headline, a product crop and a yellow "Get Fider For Free" button (Create your board / Add ideas / Let the voting commence / Sit back)
6. "Don't take our word for it" three quote cards with hard black shadows (rendered three times in the DOM, a carousel)
7. "Take the next step" final CTA with "Full access / No credit card / Cancel anytime"
8. FAQ accordion (7 questions, including "How much does Fider cost?" and "I could just use a spreadsheet right?")
9. Footer

**Visual system**
- Background: light, white with a bubblegum pink hero, cream #f9f5f2 bands, beige #f1ebe4
- Accent: mustard #f7cb45 (buttons), navy #001125 text, black outlines, pastel pink / sky / lemon blobs
- Typography: Unigeo (chunky geometric display) for headlines, Poppins for body. Playful, rounded, loud
- Radius: 8px buttons, 12 to 24px cards, 1000px pills
- Illustration: memphis style blobs with black outlines, diagonal colour wedges, cutout photos, hard offset drop shadows on cards. Emoji in body copy. A few real product crops
- Gradients: 6 (soft fades on the blobs)

**Best thing**: a genuinely different mood. The pink / mustard / outlined-blob language plus the black hard shadows make it the most memorable homepage in the set, and the four-step walkthrough is clear.

**Most generic**: the copy ("Wanna...", "Yes yes yes", emoji) and the stock cutout photo tip it into cheap. The open-source angle, which is Fider's real differentiator, is not on the homepage at all.

**Pricing (fider.io/pricing)**
- Headline: "Fider is Free". Two cards only
- Free: $0, unlimited users and members, fair-use cap of 250 feedback items, customization, multiple languages, integrations
- Pro: $25 USD/month, content moderation, unlimited feedback items, SEO indexing, billed month to month
- Self-hosting (open source, MIT) is not mentioned on the marketing pricing page; the hosted product is the only story
- FAQ repeated from the homepage

***

## nolt.io

**Hero**
- Eyebrow: "Rated 4.9/5 on Capterra and G2"
- Headline (h1, Source Sans Pro, 45px, medium): "Manage feedback from idea to release"
- Subheadline: "Nolt is a beautiful, collaborative place for all your user requests. Collect feedback, plan work and keep users in the loop. Starting at just $29/month."
- Four coloured anchor pills under the sub: Feedback (red), Kanban (violet), Roadmap (amber), Changelog (green)
- Primary CTA: "Get started for free" (white pill on dark). Nav CTA: "Create a Nolt Board"

**Section order**
1. Nav with a light / dark theme switch
2. Centered hero on a dark field with a warm orange-to-magenta radial glow top left
3. Logo marquee "Nolt powers user research at thousands of companies around the globe" (Meetup, UptimeRobot, Cisco, Gumroad, Replo, Weglot, Facepunch, Plausible)
4. Four product chapters, each colour coded and separated by a small squiggle arrow: Feedback board (red header card), Kanban view (violet), Roadmap (amber), Changelog (green). Each chapter is a centered product screenshot with six annotated mini-screenshots around it, joined by hand-drawn arrows and handwritten-style labels
5. "Integrate with apps you already use" (logo rows, GraphQL API and MCP server mention)
6. "See our wall of love" testimonial grid (Gumroad, Pointz, Kommodo)
7. Footer with "Made in Canada & Switzerland"

**Visual system**
- Background: dark by default, near black #030a12 with a warm radial gradient (orange #e0a84e into magenta #5a0d56) fading from the top left corner. Light theme available (body bg #f6f6f6)
- Accent: a four colour status set, red #e85c58 (feedback), violet #7b63e6 (kanban), amber #e0a84e (roadmap), green #35b074 (changelog). Text #ffffff and grey #b8b8b8
- Typography: Source Sans Pro headings, system sans body. Neutral, slightly dated, but the handwritten annotation labels add character
- Radius: 36px pill buttons, 12 to 15px cards, 5px on small controls
- Illustration: real product screenshots (the dark board UI), annotated with hand-drawn arrows and callouts like a whiteboard; 149 images on the page. Flat squiggle dividers
- Gradients: 6, the hero glow and section fades

**Best thing**: the annotated product chapters. One screenshot in the middle, six zoomed mini-shots around it with hand-drawn arrows, one colour per product area. It teaches the product without a single paragraph of feature copy and the colour coding carries from the hero pills down the whole page.

**Most generic**: the hero itself (centered text, rating badge, white pill button on a dark glow) is the stock dark SaaS opener, and the heavy scroll-in fades leave the page blank until you scroll.

**Pricing (nolt.io/pricing)**
- Headline: "Simple flat-rate pricing". All plans include unlimited users, content and admins. Europe / Global region toggle, Annual / Monthly toggle (annual saves over 20%)
- Essential: $29/month ($348 annual), 1 board, custom fields and statuses, private boards, roadmap, JWT SSO, Slack / Discord / GitHub / Trello, analytics integrations
- Pro: $69/month ($828 annual), 5 boards, password protected boards, domain restriction, moderation and profanity filters, Zapier / Make, Intercom / Teams, Jira / Linear / monday / Asana, export APIs. "Most popular"
- Enterprise: custom, unlimited boards, AI moderation, SAML / OIDC, SCIM, invoicing, SLA, priority support
- Unit: boards, not seats or users. No free tier; a 10 day Pro trial, no card
- FAQ (6 questions), logo wall, no comparison table

***

## Cross-cutting observations

- Three light sites (Canny, Headway, Beamer, Fider) and two dark (Featurebase, Nolt). Only Beamer uses a serif. Only Fider uses outlines and hard shadows. Nobody uses a monospace face as a brand element, which is an open lane for a developer-first product.
- Every site shows the product either as a real screenshot (Canny, Featurebase, Nolt) or as a grey wireframe (Headway, Beamer). Nolt is the only one that annotates the screenshot.
- Pricing units differ everywhere: tracked users (Canny), seats (Featurebase), MAU (Beamer), boards (Nolt), feedback items (Fider), flat (Headway). Two tier pricing (Headway, Fider) reads as the most honest.
- No competitor leads with self-hosting, a CLI, or an API on the homepage, even Fider which is open source. The whole category speaks to PMs and marketers, not to the developer who will actually wire it up.
- Logo walls appear on 4 of 6 pages directly under the hero. Testimonials appear on all 6.

***

## Mash-up design brief: Shiplog

**Positioning line**: Shiplog is the feedback board, public roadmap and changelog you can `git clone`. Free to self-host, $9/mo cloud. First audience: Omarchy and Linux developers who already live in a terminal and a tiling window manager. The page must feel like a tool they would install, not a SaaS they would be sold.

**Mood**: a well-lit terminal. Tokyo Night adjacent, but shifted warm and anchored on orange and teal instead of omarchy.org's blue #7aa2f7 and green #9ece6a. Where omarchy.org uses JetBrains Mono and the stock #1a1b26 base, Shiplog uses a deeper ink base, a different mono, and a serif-free grotesque with real personality.

### Palette (hex)

| Token | Hex | Use |
|-|-|-|
| ink | #13141c | page background (deeper and slightly bluer than #1a1b26, so it reads as its own thing next to omarchy.org) |
| panel | #1c1e2b | cards, code blocks, changelog entries |
| line | #2c3045 | hairline borders, table rules |
| fog | #9aa3c0 | secondary text |
| paper | #e6e9f5 | primary text |
| ember | #ff9e64 | primary accent: CTAs, links, active tab, cursor (the Tokyo Night orange, used as the hero colour rather than the blue) |
| tide | #73daca | "shipped" status, success, changelog "New" tag |
| plum | #bb9af7 | "planned" status, roadmap column headers |
| rose | #f7768e | "bug" tag and destructive states only |
| lemon | #e0af68 | "in progress" status |

Status set (plum / lemon / tide / rose) is the Nolt idea of one colour per product area, folded into the roadmap columns so the colour coding is meaningful rather than decorative. Ember is the only colour allowed on buttons.

Light mode is not required for launch; the board itself ships with both themes, the marketing page is dark only.

### Fonts (Google Fonts)

- **Bricolage Grotesque** for headlines and body. Variable optical size: use the display axis tight and heavy at 56 to 72px for the hero, normal at 16 to 18px for body. It is a grotesque with a visible personality (narrow counters, slightly quirky g and a), so it reads as crafted rather than as Inter.
- **Geist Mono** for everything a developer would type or read in a terminal: eyebrow labels, the install command, changelog version tags, roadmap status chips, pricing numbers, footer. Mono carries the brand; it is the one typographic move nobody in the set makes.

### Hero layout

Two columns on desktop, stacked on mobile.

Left (55%): Geist Mono eyebrow `$ shiplog init` with a blinking ember cursor. Headline in Bricolage, 64px, paper: "Ship it. Log it. Let them vote." Sub in fog, 18px: "A feedback board, public roadmap and changelog in one binary. Self-host it for free, or let us run it for $9 a month." Primary CTA, ember filled, 8px radius, mono label: `curl -fsSL get.shiplog.dev | sh` rendered as a copyable command block with a copy icon; secondary ghost button "Try the cloud demo". Microcopy under it in mono: "MIT licensed. No tracked users, no MAU, no seats."

Right (45%): a live, real Shiplog board (not a screenshot, an embedded iframe or a static HTML replica) showing three roadmap columns with plum / lemon / tide headers and vote counters that tick when hovered. Panel #1c1e2b, 12px radius, 1px line border. Behind it, a very faint ember radial glow at 8% opacity bleeding off the top right, which is the Featurebase aurora turned down to a whisper.

No logo wall under the hero. Replace it with a single mono line: "Running on 1,200 self-hosted instances and the Omarchy package feed." (number to be verified before launch).

### Page sections, in order

1. **Hero** (above). One line: Ship it. Log it. Let them vote.
2. **Install strip**: three tabs in mono, `omarchy-pkg`, `docker`, `cloud`, each revealing one command. "One command on Omarchy, one container anywhere else, or zero commands on cloud."
3. **The loop, annotated**: Nolt-style chapter. One real board screenshot centered with four annotated callouts on hand-drawn ember arrows: vote, merge duplicates, move to Shipped, auto-post to changelog. "Feedback comes in, a roadmap column moves, the changelog writes itself."
4. **Three products, three colours**: three panels side by side, Board (plum header), Roadmap (lemon header), Changelog (tide header), each with a four-bullet mono list of what it does. "Board, roadmap, changelog. Same database, same URL, same theme as your app."
5. **Built for people who read man pages**: a 2x3 grid of panels with mono titles: `config.toml`, `GitHub + GitLab issues sync`, `Markdown everywhere`, `OIDC / GitHub login`, `JSON API + webhooks`, `Theme = your terminal colours (Tokyo Night, Catppuccin, Gruvbox shipped)`. "Everything is a file, a flag or an endpoint. Nothing is a sales call."
6. **Changelog, eating its own dog food**: Shiplog's real changelog rendered inline, three entries, tide "New" and rose "Fix" tags, version numbers in mono. "This section is our own changelog widget. Click any entry to see the board post it closed."
7. **Pricing**: two cards only, Headway style. Self-host: $0, everything, forever, MIT. Cloud: $9/mo flat, unlimited boards, users and admins, custom domain, backups, email digests. No comparison table. "Two prices. The second one exists so you do not have to run Postgres."
8. **Wall of commits**: testimonials formatted as git log entries in mono (`author`, `date`, one quoted line), 6 of them, with Headway's highlighter treatment in ember at 20% opacity on the key phrase. "What people say after they stopped paying per seat."
9. **Footer**: source link, docs, package feed status, Omarchy badge, licence. Mono, small, line rule above.

(That is 8 content sections plus the footer.)

### Three UI motifs borrowed, with attribution

1. **Annotated product screenshot with hand-drawn arrows and mini callouts** (from nolt.io, product chapters). Used once in section 3 instead of four times, with ember arrows on the ink background so it reads as marker on a dark whiteboard.
2. **Highlighter-marked key phrase inside testimonials** (from headwayapp.co). Reused in section 8 with ember at low opacity behind mono text so quotes scan in two seconds.
3. **Tabbed product switcher driving one framed panel** (from canny.io's Capture / Enrich / Organize strip, and featurebase.app's five-tab viewer). Used for the install strip in section 2, but the tabs switch commands rather than screenshots, which keeps the pattern while making it developer-native.

Also borrowed in spirit, not form: Beamer's confidence in a non-default typeface (serif there, Bricolage plus mono here) and Fider's hard-edged shapes, reduced to 1px line borders and 8px radii rather than blobs.

### What to avoid, so it stays distinct

- No Inter, no violet glow at full strength, no logo wall under the hero (Featurebase, Canny).
- No blue #7aa2f7 as the primary accent and no JetBrains Mono, both of which are omarchy.org's signature.
- No grey wireframe placeholders (Headway, Beamer); every product image is a real board.
- No "Most popular" badge, no slider, no MAU or seat language anywhere on the page.
- No dashes in any copy.
