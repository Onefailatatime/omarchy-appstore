# Paid developer-founder tools that are Mac-only or weak on Linux, and what Linux/Hyprland/Omarchy users say they are missing (2025-2026)

Research date: 2026-10-11/12. All GitHub star counts were pulled live from the GitHub API on 2026-10-12 unless another date is given. Pricing was read from the vendors' own pages on 2026-10-11. Web search budget was exhausted before Reddit/X could be mined directly; see Gaps in each section.

Status legend used throughout: **[WAYLAND OK]** = exists and works on Wayland/Hyprland; **[X11 ONLY / PORTAL-DEPENDENT]** = exists but X11-only or only via xdg-desktop-portal with caveats; **[NONE]** = no Linux equivalent found.

---

## Key Question 1: Which Mac-only paid productivity/founder tools are asked for on Linux, and what do they cost?

### Takeaway
The incumbents cluster into three price bands: ~$100-350/yr subscriptions (Screen Studio $108/yr, Raycast Pro $96/yr, CleanShot Pro $120/yr, Rize $120-480/yr, Setapp $180/yr, Kaleidoscope ~$96/yr), $35-130 one-time (CleanShot Basic $35, Xnapper ~$30, Typora $15, TablePlus $99-129, Proxyman $89-99) and app-store one-offs ($10-50). Of the list, Screen Studio, CleanShot X, Xnapper, Shottr, Timing, Bartender, Kaleidoscope, Things, Bear and Rocket Typist are macOS-only; Raycast, Rize and Tower are Mac+Windows (Rize says Linux is "coming soon"); TablePlus, Proxyman and Cap already ship Linux builds.

### Cited Findings

**Screen recording / demo video**
- Screen Studio: $9/mo billed yearly ($108/yr, "Save 69%") or $29/mo monthly; one-time licenses "no longer sold to new customers"; macOS 13.1+ only; FAQ: "No, and there are no near-future plans to add Windows support"; Linux not mentioned at all — [screen.studio](https://screen.studio/)
- Cap (open-source Loom alternative): Free tier; Desktop License $29/license/yr or $58 one-time lifetime (commercial rights, unlimited local recording); Cap Pro $12/user/mo or $8.16/mo annual; downloads listed for "macOS, Windows & Linux" — [cap.so/pricing](https://cap.so/pricing). Linux download formats: .deb (default button), AppImage, .rpm, Arch/Pacman; no Flatpak or AUR listed; Windows still labelled "Beta" — [cap.so/download](https://cap.so/download)

**Screenshots / annotation**
- CleanShot X: Basic $35 one-time (Mac app + 1 yr updates, optional $19/yr renewal, 1 GB cloud); Pro $10/user/mo billed annually (unlimited cloud, custom domain, SSO/SCIM); macOS 13+ only; "No Windows version, and none is planned" — [cleanshot.com/pricing](https://cleanshot.com/pricing)
- Xnapper: third-party listings give Base $29.99 (1 device), Personal $54.99, Standard $79.99, pay-once with 1 year of updates; macOS 10.15+; also on Setapp. Official site did not resolve (DNS failure 2026-10-11), so prices are from reviews — [The Sweet Bits](https://thesweetbits.com/tools/xnapper/); [Toolradar](https://toolradar.com/tools/xnapper); a $5 AppSumo code deal was reported by [Dave Swift](https://daveswift.com/xnapper/)
- Shottr: "Name your price, or enter $0 to get Shottr for free"; macOS Catalina 10.15+ only; current version v1.9.3 — [shottr.cc](https://shottr.cc/)

**Launcher**
- Raycast: Free; Pro $10/mo or $96/yr; Plus $20/mo or $192/yr; Max $50/mo or $480/yr; Teams Pro $15/user/mo; platforms shown: macOS, Windows, iOS; Linux not mentioned — [raycast.com/pricing](https://www.raycast.com/pricing)

**Time tracking / focus**
- Rize: Basic $9.99/mo, Pro $23.99/mo, Max $39.99/mo (annual billing shown; monthly $12.99-39.99); Team $39.99/seat/mo or $29.99 annual; macOS 10.14.6+ and Windows 10+; page states "Support for Linux will be coming soon" — [rize.io/pricing](https://rize.io/pricing)
- Timing: Professional (1 Mac) $10/mo lowest listed figure; Connect (3 Macs, "AI-powered workflows and teams") $168/yr highest listed; macOS only; not on the Mac App Store because sandboxing would limit tracking — [timingapp.com/pricing](https://timingapp.com/pricing)

**Notes / tasks / calendar**
- Craft: Free (1,500 blocks); Plus $6.4/mo yearly or $8/mo monthly; Family $12/$15; Team $50/mo (10 accounts); syncs "across iPhone, iPad, Mac, and web" — no Linux/Windows native app — [craft.do/pricing](https://www.craft.do/pricing)
- Things: Mac, iPhone/Watch, iPad, Vision Pro only; prices set in USD via App Store, not displayed on the site — [culturedcode.com/things/pricing](https://culturedcode.com/things/pricing/)
- Rocket Typist (text expander): Pro USD 19.95 on Mac (body text says $19.99), $9.99 on iPhone/iPad; macOS 14+/iOS 16+; included with Setapp — [witt-software.com/rockettypist](https://witt-software.com/rockettypist/)

**Menu bar / utilities / bundles**
- Bartender: macOS only (Bartender 7 for macOS 27, Bartender 6 for macOS 26); models listed: one-time purchase, Pro yearly, "Mega Supporter" lifetime; prices did not render ("Loading price") — [macbartender.com](https://www.macbartender.com/)
- Setapp: $14.99/mo (1 Mac), $18.99/mo (Mac + 4 iOS), $22.99/mo Power User (4 Macs + 4 iOS); "hundreds of high-quality apps"; macOS + iOS only — [setapp.com/pricing](https://setapp.com/pricing)

**Dev tools**
- Tower (Git GUI): Basic $69/yr (~$5.75/mo), Pro $129/yr (~$10.75/mo), Enterprise $149/yr; "All plans include versions for Mac and Windows"; Linux not mentioned — [git-tower.com/pricing](https://www.git-tower.com/pricing)
- Kaleidoscope (diff/merge): subscription "starting at $8/month", 7-day trial; macOS Sequoia 15+ only — [kaleidoscope.app](https://kaleidoscope.app/)
- TablePlus: Basic $99 (1 device), Standard $129 (was $198, 2 devices), Team $79/seat (3+ seats); perpetual with 1 yr updates; macOS 12+, Windows (.NET 4.8), iOS, and a Linux version with its own GitHub issue tracker — [tableplus.com/pricing](https://tableplus.com/pricing)
- Proxyman: Standard $89 perpetual (1 seat, "one Mac, Windows, or Linux device"), Personal $99 (2 seats + mobile), Team $99/seat/yr or $12/seat/mo; Linux supported — [proxyman.com/pricing](https://proxyman.com/pricing)

**Dictation (bonus, highly relevant to Omarchy)**
- Superwhisper: Free tier; Pro (price did not render cleanly, shows monthly/yearly/lifetime options); platform list on homepage says "Available on Mac, Windows, iOS and Android" with no Linux mention — [superwhisper.com](https://superwhisper.com/). Contradiction: the Omarchy manual states "On fresh installs, Superwhisper is the default dictation backend" and Omarchy's base package list contains `superwhisper-bin` (x86_64 only) — [Omarchy manual, Text Extraction & Dictation](https://github.com/omacom/omarchy/blob/master/manual/11-text-extraction-dictation.md); [install/omarchy-x86_64-only.packages](https://raw.githubusercontent.com/omacom/omarchy/master/install/omarchy-x86_64-only.packages)

**Demand signals from Linux users (what was reachable without Reddit/X)**
- Cap GitHub issue #609 "[Question] Will there be a Linux version for this screen recorder" opened 2025-06-09, still open, 15 reactions; #1671 "cap.so for linux" (2026-03-19, 10 reactions) closed after maintainer richiemcilroy wrote on 2026-06-24 "we're currently testing out the Linux release ... Should hopefully have it fully live in 0.5.2 today"; users on 2026-06-12 and 06-24 reported the Linux download buttons "none of them work" — [#609](https://github.com/CapSoftware/Cap/issues/609); [#1671](https://github.com/CapSoftware/Cap/issues/1671)
- Raycast-compatible Linux clones have real traction: Vicinae 10,227 stars (GPL-3.0, "compatible with the Raycast ecosystem", v0.29.1 released 2026-09-30, sponsors Depot and CodeRabbit) — [github.com/vicinaehq/vicinae](https://github.com/vicinaehq/vicinae); Flare (ByteAtATime/flare, formerly raycast-linux) 1,519 stars, v0.1.0 2025-07-29, **archived** (last push 2026-01-17) — [github.com/ByteAtATime/flare](https://github.com/ByteAtATime/flare)
- An Omarchy issue asked to "Use Vicinae as default menu handler" (#1982, 2025-09-26, 52 reactions, 33 comments); DHH replied 2026-02-01 "I remain happy with Walker for Omarchy, but feel free to replace any part of the system as you see fit" — [#1982](https://github.com/omacom/omarchy/issues/1982)
- AlternativeTo maintains a dedicated "Raycast for Linux" alternatives page and lists Vicinae and Flare as the main options — [alternativeto.net/software/raycast-for-linux](https://www.alternativeto.net/software/raycast-for-linux/)
- Two paid, proprietary, Linux-only Screen Studio clones launched in 2026 (Hosaka Studio, Screenix) — see KQ2; their existence is itself evidence of demand founders are betting on.

### Inferences
- The Mac tools with zero Linux path are precisely the "polish" layer: Screen Studio, CleanShot X, Xnapper, Shottr, Bartender, Timing, Kaleidoscope, Things, Bear, Craft, Setapp. Dev-infrastructure tools (TablePlus, Proxyman, Zed, Warp, Cap) have already crossed to Linux, so the remaining gap is design-forward utilities, not dev tooling.
- Rize's "Linux coming soon" and Cap's slow Linux rollout (issue open since June 2025, downloads broken as of June 2026, Wayland fixes still in open PRs in Oct 2026) show incumbents treat Linux as a late, low-priority port rather than a first-class target.
- Typical willingness-to-pay anchors for a Linux-native equivalent, based on incumbents: $35-60 one-time for screenshot tooling, $9-12/mo or $58-108/yr for recording, $96/yr for a launcher.

### Gaps
- Bear Pro price (bear.app/pricing returned 404), Things prices (App Store only), Bartender prices (did not render), Paw/RapidAPI and Notion Calendar pricing/platforms were not fetched. Rocket Typist/Timing/Bartender being Mac-only is confirmed; exact Bartender pricing is not.
- No direct Reddit or X thread quotes ("I'd pay for Screen Studio on Linux") could be captured: the web-search budget ran out and old.reddit.com fetches are blocked in this environment. The Indie Hackers thread "Linux users, have you ever paid for apps on Linux?" (2022) returned HTTP 403; a search snippet said one commenter would pay for a lifetime license but otherwise use OBS/Peek — [indiehackers.com](https://www.indiehackers.com/post/linux-users-have-you-ever-paid-for-apps-on-linux-f726f86e00) (unverified content).

---

## Key Question 2: Screen recording and demo videos on Wayland — Cap, Kooha, OBS, wf-recorder, wl-screenrec, GPU Screen Recorder, Peek; does anything do Screen-Studio-style auto-zoom and padding?

### Takeaway
Raw capture on Wayland/Hyprland is solved (gpu-screen-recorder ships in Omarchy's base package set; OBS, Kooha, wf-recorder, wl-screenrec all work), but the Screen-Studio layer (auto-zoom on click, cursor smoothing, padded backgrounds, one-click polished export) exists on Linux only as (a) OpenScreen, a 7-month-old MIT project at 4.1k stars whose click effects require evdev/input-group hacks and whose Hyprland cursor-tracking PR was closed unmerged, (b) two small paid proprietary apps (Hosaka Studio, Screenix) and (c) Cap, whose Wayland window/display recording is still being fixed in an open PR as of 2026-10-05.

### Cited Findings

**Raw recorders — [WAYLAND OK]**
- OBS Studio: 77,337 stars, pushed 2026-10-10 — [github.com/obsproject/obs-studio](https://github.com/obsproject/obs-studio). Wayland capture via PipeWire landed in OBS 27 — [It's FOSS](https://itsfoss.com/obs-studio-25-release/). A community "Hyprland OBS Zoom To Mouse + Follow Script" exists because the generic zoom script did not work on Hyprland — [OBS forum](https://obsproject.com/forum/threads/hyprland-obs-zoom-to-mouse-follow-script.188472/)
- Kooha (GNOME, portal-based): 3,530 stars; latest release v2.3.2 2026-06-05 — [github.com/SeaDve/Kooha](https://github.com/SeaDve/Kooha); in Arch `extra` as 2.3.2 (updated 2026-07-17) — [archlinux.org](https://archlinux.org/packages/search/json/?name=kooha). No zoom/padding features.
- gpu-screen-recorder: Arch `extra` 6.1.3, updated 2026-09-23, "A shadowplay-like screen recorder for Linux. The fastest screen recorder for Linux" — [archlinux.org](https://archlinux.org/packages/search/json/?name=gpu-screen-recorder). It is in Omarchy's core pacstrap list (`gpu-screen-recorder`) — [install/omarchy-base.packages](https://raw.githubusercontent.com/omacom/omarchy/master/install/omarchy-base.packages). A Lemmy thread on Wayland single-window capture says it "works amazingly well" and notes Hyprland needs xdg-desktop-portal-hyprland — [feddit.it](https://feddit.it/post/9626943)
- wf-recorder (wlroots): 1,318 stars; v0.6.0 released 2025-10-17; last push 2026-04-12 — [github.com/ammen99/wf-recorder](https://github.com/ammen99/wf-recorder)
- wl-screenrec (wlroots, hardware encoding): 630 stars; v0.3.1 2026-08-10; repo now at rosalyntg/wl-screenrec — [github.com/russelltg/wl-screenrec](https://github.com/russelltg/wl-screenrec)
- record-ui-git (AUR, July 2026): "Rust/GTK4 screen recorder for Hyprland (wf-recorder UI; binary: hyprcap)" — [aur.archlinux.org/packages/record-ui-git](https://aur.archlinux.org/packages/record-ui-git)
- Peek (GIF recorder): 10,549 stars but **archived** (last push 2025-09-24) — [github.com/phw/peek](https://github.com/phw/peek) — effectively [NONE] going forward.

**Cap on Linux — [PORTAL-DEPENDENT, Wayland incomplete]**
- Cap: 23,221 stars; latest release cap-v0.6.0 2026-09-15 — [github.com/CapSoftware/Cap](https://github.com/CapSoftware/Cap)
- Tracking issue #1553 "Linux Desktop App support and build pipeline" opened 2026-01-26, still open — [#1553](https://github.com/CapSoftware/Cap/issues/1553)
- PR #2420 "feat(linux): enable Wayland window/display recording with PipeWire cursor metadata and evdev clicks" opened 2026-10-05, **open, not merged**; adds DMA-BUF sync, PipeWire window-size negotiation, evdev click capture; tested on KDE Plasma 6 Wayland; automated review flagged that "clean capture is disabled for Wayland display and area recordings, so the app's own windows may appear in recordings" and X11 clicks may be dropped — [#2420](https://github.com/CapSoftware/Cap/pull/2420)
- Cap's download page gives no Linux beta label or Wayland/X11 note — [cap.so/download](https://cap.so/download)

**Screen-Studio-style auto-zoom on Linux**
- OpenScreen (getopenscreen/openscreen): 4,065 stars, repo created 2026-03-14, v2.0.0 released 2026-10-03, MIT; features auto/manual zoom with easing, cursor smoothing and click effects, wallpaper/gradient backgrounds, webcam overlay; Linux .deb/.rpm/.pacman/AppImage/Nix. Linux caveats: native capture needs xdg-desktop-portal + PipeWire or it "falls back to browser capture with fewer capabilities"; click effects need evdev read access via udev rule or `input` group, otherwise "cursor samples are recorded as moves only"; Hyprland not mentioned — [github.com/getopenscreen/openscreen](https://github.com/getopenscreen/openscreen). PR #157 "Hyprland cursor tracking for Linux recordings" was closed, not merged — [#157](https://github.com/getopenscreen/openscreen/pull/157). Status: [PORTAL-DEPENDENT].
- Hosaka Studio (paid, Linux-only): Free 7-day trial; Pro $39 one-time (1 yr updates); Lifetime $79; 3 machine activations; X11 and Wayland; "Flatpak has limited support on wlroots compositors" (Sway, Hyprland named); native packages for Arch, Debian, Ubuntu, Fedora; site lists AI background removal, webcam bubble, Whisper transcription, YouTube/S3/R2 publishing — [hosaka.studio](https://hosaka.studio/). AlternativeTo (added 2026-02-23) describes it as auto-zooming on click, Pay-once, $39-79 — [alternativeto.net](https://alternativeto.net/software/hosaka-studio/about). Note: the official site text fetched did not mention auto-zoom; the AlternativeTo listing and a Product Hunt post do. Status: [WAYLAND OK with wlroots/Flatpak caveat].
- Screenix (paid, Linux-only): $39/yr, $59 lifetime, Team $80/seat/yr (min 2); "Recorded clicks drive automatic zooms and smooth cursor motion"; FAQ explicitly lists Arch with KDE Plasma, **Hyprland**, GNOME or Cinnamon; capture via portal on Wayland — [screenix.studio](https://screenix.studio/). AUR `screenix-bin` 1.8.2-2, 1 vote, popularity 0.0, last modified 2026-10-05 — [AUR RPC](https://aur.archlinux.org/rpc/v5/info?arg[]=screenix-bin). Status: [WAYLAND OK], negligible adoption so far.
- Beam ("an alternative to Screen Studio ... Windows/Mac/Linux"): 52 stars, pushed 2026-10-11 — [github.com/BeamRecorder/Beam](https://github.com/BeamRecorder/Beam). ferricast ("Linux-only GNOME app alternative to Screen Studio"): 0 stars — [github.com/AlexPiquard/ferricast](https://github.com/AlexPiquard/ferricast)
- ScreenArc (paid, proprietary, Linux auto-zoom) and ClickZoom (€8.50 one-time, adds zoom animations at click points) appear in AlternativeTo listings; not independently verified — [alternativeto.net/software/screenarc](https://alternativeto.net/software/screenarc/?p=4)
- Omarchy's own video tool, omacut (86 stars, v0.5.0 2026-10-03, MIT, Qt Quick + ffmpeg), is "A dead-simple video trimmer" — trim/split/export only, no recording or zoom — [github.com/omacom/omacut](https://github.com/omacom/omacut)

### Inferences
- Nobody on Linux has shipped the combination Screen Studio sells: reliable Wayland capture + auto-zoom + cursor smoothing + padded export + share link, with Hyprland as a first-class target. OpenScreen is closest in features but depends on evdev workarounds and has no Hyprland cursor tracking; Screenix is closest in Hyprland support but has one AUR vote.
- gpu-screen-recorder being in Omarchy's base install means every Omarchy user already has a capable raw recorder; the gap is the post-production/presentation layer, which could sit on top of gpu-screen-recorder output.
- Price anchors set by the Linux-native entrants are $39-59 one-time or $39/yr, well under Screen Studio's $108/yr.

### Gaps
- No usage/revenue numbers exist for Hosaka Studio or Screenix (neither site states customer counts).
- Kooha and wf-recorder "last release" dates are confirmed; gpu-screen-recorder's upstream (git.dec05eba.com) was not fetched, only its Arch package date.
- Whether Cap's Linux build works on Hyprland specifically is not documented; PR #2420 was tested only on KDE Plasma 6.

---

## Key Question 3: Screenshots and annotation on Wayland — Satty, Swappy, Flameshot, grim/slurp, ksnip; what do they lack versus CleanShot X?

### Takeaway
Hyprland screenshotting is a pipeline of CLI pieces (grim + slurp + satty/swappy) rather than an app; Omarchy answered this in Aug 2026 by shipping its own Shottr-inspired tool, Omasnap (562 stars, in the base install), which covers region/window/scrolling capture, OCR, vector annotations, backdrops and pins, but has no recording, no cloud upload/share links, and no history/cloud library, the features CleanShot Pro charges $10/mo for.

### Cited Findings
- Hyprland wiki's canonical recommendations: grim + swappy (keybind example), Satty ("inspired by swappy and Flameshot, and an almost drop-in replacement for swappy"), and Flameshot, which "on Wayland ... depends on desktop portal support for capture" — [wiki.hypr.land](https://wiki.hypr.land/Useful-Utilities/Screenshots-and-Recording/)
- Satty: 2,448 stars (repo now Satty-org/Satty), v0.22.0 released 2026-08-03, pushed 2026-10-11 — [github.com/gabm/satty](https://github.com/gabm/satty). [WAYLAND OK], annotation only (no capture; needs grim/slurp).
- Swappy: 1,508 stars, "A Wayland native snapshot editing tool, inspired by Snappy on macOS", last push 2025-12-16 — [github.com/jtheoof/swappy](https://github.com/jtheoof/swappy). [WAYLAND OK], slow-moving.
- Flameshot: 31,159 stars, v14.0.0 released 2026-06-19 — [github.com/flameshot-org/flameshot](https://github.com/flameshot-org/flameshot). [PORTAL-DEPENDENT] on Wayland per the Hyprland wiki.
- grim: 1,003 stars on the GitHub mirror, **archived** there (last push 2022-03-30) — [github.com/emersion/grim](https://github.com/emersion/grim); it is still in Omarchy's base packages alongside `slurp` — [omarchy-base.packages](https://raw.githubusercontent.com/omacom/omarchy/master/install/omarchy-base.packages)
- ksnip: 3,357 stars, pushed 2026-10-01 — [github.com/ksnip/ksnip](https://github.com/ksnip/ksnip)
- Hyprshot: 884 stars, last push 2024-07-29 — [github.com/Gustash/Hyprshot](https://github.com/Gustash/Hyprshot)
- Omasnap (omacom/omasnap, created 2026-08-10): 562 stars, 67 forks, MIT, v1.21.0 released 2026-09-20; "Native Wayland screenshot and annotation editor for Omarchy and Hyprland"; README names Shottr ("fast region/window capture, OCR, and polished backdrops"), Satty and Flameshot as inspirations; features: smart selection, region/window/fullscreen/scrolling capture (`omasnap --scroll`, manual or automatic stitching), OCR via Tesseract (`O` key), movable vector layers (arrows, shapes, freehand, highlighter, numbered markers, text, redaction), gradient backdrops and drop shadows, pinned floating captures on every workspace, last-five recents; **not mentioned: screen recording, cloud upload or share links** — [github.com/omacom/omasnap](https://github.com/omacom/omasnap). It is in Omarchy's core package list — [omarchy-base.packages](https://raw.githubusercontent.com/omacom/omarchy/master/install/omarchy-base.packages). The repo also exists under Tobi Lütke's account (tobi/omasnap) — [github.com/tobi/omasnap](https://github.com/tobi/omasnap)
- Omarchy also bundles Tesseract OCR for `Super + Ctrl + PrtScr` text extraction — [manual/11-text-extraction-dictation.md](https://github.com/omacom/omarchy/blob/master/manual/11-text-extraction-dictation.md)
- A May 2025 r/hyprland thread asked for Spectacle-like "freeze the screen and draw shapes and arrows"; replies were grim + slurp + satty and grimblast `--freeze` piped to satty — [redlib mirror of r/hyprland](https://redlib.ssps.io/r/hyprland/comments/1kcfpg9/screen_shoot_tool_for_hyprland) (mirror unreachable at time of writing; content from search snippet)
- CleanShot X features paid for in the Pro tier: unlimited cloud storage, custom domain/branding, advanced sharing and security, team management, SSO/SCIM — [cleanshot.com/pricing](https://cleanshot.com/pricing)

### Inferences
- Versus CleanShot X, the Wayland stack lacks: (1) instant share links / cloud library, (2) screen recording + GIF in the same tool, (3) a capture history browser, (4) team/branding features. Omasnap closed the local-capture and annotation gap in Aug-Sep 2026 but explicitly stays local-only (clipboard, PNG, pins).
- Since Omasnap is default and MIT, a paid Omarchy-targeted screenshot app would need to compete on the cloud/share/recording layer rather than on capture or annotation.

### Gaps
- No user-count data for Satty/Swappy beyond stars; no Reddit quotes comparing them to CleanShot could be captured (search budget exhausted, Reddit fetch blocked).
- Whether Omasnap has a roadmap for recording or upload is not stated in the README.

---

## Key Question 4: What does the Omarchy community say it wants added or wishes existed, and what shows up in "omarchy pkg" requests?

### Takeaway
Omarchy's GitHub Discussions are dominated by compositor/session requests (Niri support 46 votes, save/restore Hyprland sessions 31, vim window navigation 26, multiple users 40) and default-app swaps (Hermes Desktop 36, Zen browser theming 41, Zathura PDF 9), not by requests for Mac-style productivity apps; instead the Omacom org has been building its own replacements (omasnap, omawrite, omacut, omacalc, hype, signed) and in Sep 2026 registered wecanfixeverything.com with the slogan "every missing app, every incompatibility, every paper cut", signalling that app gaps are being tackled in-house.

### Cited Findings
- Top Discussions overall (votes/comments): "Password auth failing randomly on Lock Screen" 101/183; "Bring back bare mode/minimal install request" 68/20; "Omarchy + Niri => Ochiri?" 46/15; "Please reconsider removing the Suspend menu option" 45/21; "Using Firefox as the WebApp Browser" 41/50; "Zen browser theme integration?" 41/10; "Support Multiple Users" 40/15; "Add Hermes and Hermes Desktop as pre-installed defaults" 36/1 (2026-08-19); "Arch + Hyprland with Omarchy on MacBooks" 36/73; "Installing Omarchy in a VM on an M* Mac" 29/108 — [github.com/omacom/omarchy/discussions?sort=top](https://github.com/omacom/omarchy/discussions?discussions_q=sort%3Atop)
- Top open "Ideas": Niri 46; Firefox webapp 41; Zen theme 41; Multiple users 40; Hermes defaults 36; Save/Restore hyprland sessions 31; VI(M) keybindings for windows 26; restart with saved apps 22; "Show the keyboard shortcuts when you don't use them" 19 (2026-08-31); "Optional Default Apps" 17; bluetui 16; 802.1x WiFi 16; VPN settings in network menu 14; battery charge threshold 14; Google Drive in file manager 13; Vimium default 10; Howdy face unlock 9; Zathura default PDF 9; "Guide: Using Apple apps on Linux" 8. The reviewer found "No listed request explicitly asks for a screenshot, screen recording, launcher, notes, calendar, time tracking, or clipboard tool" — [Ideas category sorted by top](https://github.com/omacom/omarchy/discussions/categories/ideas?discussions_q=is%3Aopen+category%3AIdeas+sort%3Atop)
- Most-reacted issues/PRs (reactions): Omarchy Quattro release PR 272; "Code of conduct?" 204; "Omarchy goes Quickshell" 154 (2026-05-15); Omarchy 3.4.0 148; "Use NetworkManager instead of systemd-networkd" 137 (102 comments); aarch64 support 109; "Switch default terminal to Ghostty" 96; "GPU passthrough and Windows VM with Looking Glass" 61; "Use Vicinae as default menu handler" 52 — [GitHub issue search](https://api.github.com/search/issues?q=repo:omacom/omarchy+request+OR+wish+OR+add&sort=reactions). Total issues+PRs in the repo: 8,563 as of 2026-10-12 (same query).
- Omarchy's Install menu (`Super + Alt + Space` > Install) offers categories Editor (VSCode, Cursor, Zed, Sublime Text, Helix), Package, AUR, Development, Terminal (Ghostty, Foot, Kitty; Alacritty default), AI (incl. Voxtype dictation), Gaming (Steam, RetroArch, Lutris, Heroic), Web App, Windows VM, Style; the CLI equivalent is `omarchy pkg add [package]` / `omarchy pkg drop` — [Omarchy manual](https://learn.omacom.io/2/the-omarchy-manual); [Other Packages](https://learn.omacom.io/2/the-omarchy-manual/66/other-packages.md)
- The manual's "Commercial" page lists 1Password (`Super + Shift + /`), Typora ("15-day free trial, then a one-time $15 cost", `Super + Shift + W`), Spotify, Dropbox, Tailscale and NordVPN, and states Omarchy is "mostly focused on free, open source software but ... not religious about it. Sometimes the best solution is a commercial offering" — [manual/commercial](https://learn.omacom.io/2/the-omarchy-manual/61/commercial)
- Superwhisper is the default dictation backend on fresh installs, with Voxtype as the open-source alternative selectable via Setup > Defaults > Dictation — [manual/11-text-extraction-dictation.md](https://github.com/omacom/omarchy/blob/master/manual/11-text-extraction-dictation.md)
- In-house Omacom apps now in the base install or org (stars, created): aether theming 752 (2025-10); omasnap 562 (2026-08); omawrite "The essence of writing" 262 (2026-06); gliff 191 (2026-09); hype "Simple Markdown presentations with a visual slide editor" 72 (2026-09); omacut video trimmer 86 (2026-06); monologue 53 (2026-09); herdr "the runtime your coding agents live on" 28 (2026-08); omacalc 21 (2026-08); omarchy-plugin-marketplace 347 (2026-07); try-omarchy 2,568 (2026-08-23); try-omarchy-windows 607 (2026-08-28); wecanfixeverything 23 (2026-08-31) — [GitHub API, orgs/omacom/repos](https://api.github.com/orgs/omacom/repos?per_page=100)
- On 2026-10-11 Omarchy replaced Xournal++ with "Signed, Omacom's PDF signing app" in the base packages (PR #14999) — [commits on omarchy-base.packages](https://github.com/omacom/omarchy/commits/master/install/omarchy-base.packages)
- wecanfixeverything.com is a one-page Cloudflare Worker pointing at omarchy.org with the slogan "we can fix ~~some things~~ **everything** / every missing app, every incompatibility, every paper cut" — [github.com/omacom/wecanfixeverything](https://github.com/omacom/wecanfixeverything)
- Omarchy ran "The first plugin competition" (announced 2026-08-19, winners 2026-08-28) — [omarchy.org/news](https://omarchy.org/news)
- Omarchy team page: "most of Omarchy happens in the Discord and on GitHub" (questions, themes, plugins, PRs) — [us.omarchy.org/teams](https://us.omarchy.org/teams/)
- Base package list (full pacstrap set, 2026-10-12) includes: chromium, docker, nvim, obsidian, libreoffice-fresh, localsend, pinta, evince, mpv, imv, nautilus, lazygit, btop, fzf, ripgrep, grim, slurp, gpu-screen-recorder, hyprpicker, omasnap, omacut, omawrite, omacalc, hype, monologue, signed, superwhisper-bin, quickshell, tesseract, wl-clipboard — [omarchy-base.packages](https://raw.githubusercontent.com/omacom/omarchy/master/install/omarchy-base.packages)

### Inferences
- The community's loudest asks are system-level (compositor, sessions, networking, multi-user), which suggests that by late 2026 the app layer is perceived as "handled by Omacom" rather than something users lobby for publicly. The Omacom org's app cadence (a new in-house app roughly every 2-4 weeks since June 2026) means any third-party tool risks being out-built by a free default.
- The "Commercial" manual page and the Superwhisper default are strong evidence the Omarchy project itself endorses paid software where it is best-in-class; a paid Linux-native tool is culturally acceptable in this distro.
- Package requests are not tracked as issues: `omarchy pkg add` wraps pacman/yay directly, so "what people install" is invisible publicly; only default-app proposals surface in Discussions.

### Gaps
- Omarchy Discord content (reported >6,000 members Aug 2025) was not accessible; it is where per-app requests likely live. No Omarchy Discourse forum was found.
- X posts by DHH about specific missing apps could not be searched (search budget exhausted). DHH's 2025 "All in on Omarchy" post names no missing apps, only battery life and lack of vendor support — [world.hey.com/dhh](https://world.hey.com/dhh/all-in-on-omarchy-68162450)
- The GitHub Discussions list only shows titles; discussion bodies were not read, so some "Ideas" may contain app asks not visible from titles.

---

## Key Question 5: Numbers on Omarchy adoption and the Hyprland user base

### Takeaway
Omarchy went from ~27.1k GitHub stars (2026-08-21) to 44,609 (2026-10-12), reported 100,000 ISO downloads in one week (2026-08-28) and 200,000 Quattro ISO downloads in 18 days (2026-09-02), and claims via 1Password telemetry to be the #2 Linux distro on weekdays and #1 on weekends; the Omacom Foundation behind it has raised well over $13M from tech founders and corporations. Hyprland itself has 38,843 stars and roughly 12.6% of window-manager installs among ~30k voluntary Arch pkgstats submitters (Dec 2025), statistically tied with i3 and Sway.

### Cited Findings

**Omarchy**
- GitHub: omacom/omarchy 44,609 stars, repo created 2025-06-01, pushed 2026-10-12 — [GitHub API](https://api.github.com/repos/omacom/omarchy); ossinsight showed 44,452 stars and 5,343 forks a day earlier — [ossinsight.io](https://ossinsight.io/analyze/omacom/omarchy); star-history snapshot: 27.1k stars on 2026-08-21, trended 12 days with best rank #2 on 2026-08-16 — [star-history.com](https://www.star-history.com/basecamp/omarchy)
- Discord: "over 6,000 members" and "over 100,000 unique visitors in the last month" to the website as of 2025-08-25 (Omarchy 2.0, ~2 months old) — [Lunduke](https://lunduke.substack.com/p/omarchy-20-the-arch-based-hyprland)
- 2026-08-28: "100,000 Omarchy ISO downloads in the past week", nearly one petabyte served in seven days — [omarchy.org/news](https://omarchy.org/news/2026/08/100000-downloads-in-a-week/)
- 2026-09-02: "Two hundred thousand ISO downloads of Omarchy Quattro in just 18 days"; one download every ~8 seconds on average; peak 1,165 ISOs in one hour; downloads from 215 countries/territories; "Over half the downloads come from outside the top five countries"; US 28%; Iceland, Norway, Denmark download at more than twice the US per-capita rate; figures are "completed-download equivalents" from Omarchy's own servers, before de-duplicating repeat use; projection of millionth Quattro ISO by Nov 4 described by DHH as extrapolating "wildly" — [omarchy.org/news](https://omarchy.org/news/2026/09/quattro-crosses-200000-iso-downloads)
- Same post: 1Password's data on which Linux distros its users run puts Omarchy "#2 on weekdays, ahead of Fedora" and "#1" on weekends — [omarchy.org/news](https://omarchy.org/news/2026/09/quattro-crosses-200000-iso-downloads) (self-reported, not independently verified)
- 37signals: "over the next three years ... switching everyone on their Ops and Ruby programming teams" to Omarchy, on Framework and Beelink hardware; HEY test suite "almost twice as fast" on a Framework Desktop than an M4 Max — [world.hey.com/dhh](https://world.hey.com/dhh/all-in-on-omarchy-68162450) (2025-08-09); [The New Stack](https://thenewstack.io/what-is-omarchy-linux-and-why-is-37signals-moving-to-it/)
- Omacom Foundation timeline from omarchy.org/news: launched 2026-08-21 (post title "launches with $23.5 million", URL slug says "8-million"; a secondary source reports eight Founding Patrons and $8M at launch, later twelve patrons and ~$18.5M after DigitalOcean joined 2026-09-09); "funding hits $10m" 2026-08-24; "$12.6 million" total when 1Password and 37signals each pledged $100,000/yr for three years (2026-08-31); "reaches $13M with four Distinguished Patrons" 2026-09-02; DigitalOcean $3M (2026-09-09); Alibaba Cloud $3M (2026-09-22); SpaceXAI $1.5M in Grok tokens (2026-10-08); $1.8M in tokens from AI labs (2026-09-03); $100,000 HackerOne bug bounty (2026-10-02) — [omarchy.org/news](https://omarchy.org/news); [1Password/37signals post](https://omarchy.org/news/2026/08/1password-and-37signals-become-distinguished-corporate-patrons/); [OpenReplay blog summary of pledges](https://blog.openreplay.com/omarchy-linux-foundation-pledges/)
- Open (individual) patronage: "more than $120,000" from 826 patrons as of 2026-09-17, up from "roughly $60,000 from nearly 500 donors" ten days earlier — [omarchy.org/news](https://omarchy.org/news/2026/09/brian-cartmell-and-american-cloud-join-as-open-patronage-doubles/)
- Omacom Foundation hired full-time staff: outfoxxed (Quickshell creator) as Head of Omarchy Shell (2026-09-09), kernel dev Krzysztof Wilczyński (2026-09-03), Emir Beganović Head of Infrastructure (2026-09-10); ThePrimeagen joined Omarchy Core (2026-09-26) — [omarchy.org/news](https://omarchy.org/news)
- Mac reach: try-omarchy ("Run Omarchy on MacOS without any setup", 2,568 stars, created 2026-08-23); omarchy-mac 1,936 stars; "Introducing Omarchy M" (Apple M-series) 2026-09-11 — [GitHub API](https://api.github.com/orgs/omacom/repos?per_page=100); [omarchy.org/news](https://omarchy.org/news)

**Hyprland**
- hyprwm/Hyprland 38,843 stars, pushed 2026-10-09; latest release v0.56.2 2026-08-05 — [GitHub API](https://api.github.com/repos/hyprwm/Hyprland)
- Arch pkgstats (Dec 2025 snapshot): among window managers i3 12.75%, Hyprland 12.58%, Sway 12.43%, "effectively tied", together over one-third of reported WM installs; DE share KDE Plasma 38.36%, GNOME 19.84%, XFCE 10.73%; dataset is voluntary submissions — [Linuxiac](https://linuxiac.com/which-desktop-environment-do-arch-linux-users-prefer/); a pkgstats trend tracker puts the sample at ~30K+ submissions and ranks Hyprland 4th fastest-growing package (+1.44 points/month) — [piefed post](https://piefed.nullspace.lol/post/244036); primary source [pkgstats.archlinux.de](https://pkgstats.archlinux.de/)
- Omacom Foundation becomes Hyprland's exclusive sponsor for three years (option for two more) from 2026-10-10; Hyprperks "will be released for free, and the paid subscriptions will end" — [omarchy.org/news](https://omarchy.org/news/2026/08/omacom-foundation-to-be-exclusive-hyprland-sponsor/); hypr.land footer now lists Omarchy as "Exclusive sponsor" — [hypr.land/news](https://hypr.land/news/)

**Linux desktop context**
- StatCounter June 2026: Linux 4.39% of worldwide desktop OS usage; a reported July 2026 North America figure of 10.65% is disputed because of a 9.24% "Unknown" bucket — [Linuxiac](https://linuxiac.com/linux-desktop-market-share-surpasses-10-in-north-america/); [It's FOSS market share report](https://itsfoss.com/linux-market-share/)
- Stack Overflow 2022: Linux primary OS for 40.23% of respondents — [Slashdot summary](https://linux.slashdot.org/story/22/12/25/0114237/stack-overflow-survey-finds-more-developers-now-use-linux-than-macos)

### Inferences
- Stars grew ~17.5k (65%) in the seven weeks between 2026-08-21 and 2026-10-12, coinciding with Quattro and the Foundation launch; the ISO figures (200k in 18 days) imply the installed base is plausibly in the low-to-mid hundreds of thousands by Oct 2026 even after heavy de-duplication, but no install telemetry exists.
- The 1Password ranking is the single best proxy for *paying-user* composition: 1Password is a paid product, and Omarchy ranking #1-2 among its Linux users implies Omarchy users are disproportionately people who already pay for software.

### Gaps
- No independent install count; all download figures are Omarchy's own. No X follower counts for @omarchy or DHH were retrievable (search budget).
- GitHub stargazer timestamps could not be paged (API returned 404 for the star+json endpoint), so no month-by-month star curve beyond the two snapshots above.
- No Hyprland-wide user estimate exists beyond Arch pkgstats shares; Hyprperks subscriber counts were never published.

---

## Key Question 6: Do Linux desktop users pay for software? Evidence from Linux-first paid apps and the Omarchy demographic

### Takeaway
Direct Linux-only revenue data is scarce, but the Omarchy ecosystem shows unusually strong pay signals: the distro ships paid defaults (1Password, Typora at $15, Superwhisper, Spotify) and says it is "not religious" about FOSS; 826 individuals gave >$120k (~$145 average) to the Foundation in about three weeks; Hyprland users were sold a €5/mo perks tier for a year; and two founders launched paid, Linux-only Screen Studio clones in 2026. The weak signal is adoption of those paid clones (Screenix has 1 AUR vote).

### Cited Findings
- Omarchy manual "Commercial" page lists 1Password, Typora ($15 one-time after 15-day trial), Spotify, Dropbox, Tailscale, NordVPN and says "Sometimes the best solution is a commercial offering, and that's fine" — [learn.omacom.io](https://learn.omacom.io/2/the-omarchy-manual/61/commercial)
- Omarchy Install > Editor menu includes Cursor and Sublime Text (both paid) alongside VSCode, Zed, Helix — [Omarchy manual](https://learn.omacom.io/2/the-omarchy-manual)
- Superwhisper (a paid dictation app that until recently listed only Mac/Windows/iOS/Android) is Omarchy's default dictation backend and is packaged as `superwhisper-bin` — [manual](https://github.com/omacom/omarchy/blob/master/manual/11-text-extraction-dictation.md); [superwhisper.com](https://superwhisper.com/)
- 1Password's own distro telemetry ranks Omarchy #2 (weekdays) / #1 (weekends) among its Linux users — [omarchy.org/news](https://omarchy.org/news/2026/09/quattro-crosses-200000-iso-downloads); 1Password also pledged $100,000/yr for three years to the Foundation — [omarchy.org/news](https://omarchy.org/news/2026/08/1password-and-37signals-become-distinguished-corporate-patrons/)
- Open patronage: 826 individual donors, >$120,000, as of 2026-09-17 (≈$145/donor), doubling in ten days — [omarchy.org/news](https://omarchy.org/news/2026/09/brian-cartmell-and-american-cloud-join-as-open-patronage-doubles/)
- Hyprperks: €5/month plus tax, launched 2025-07-28 (GA), perks = member forum, premium dotfiles, support; It's FOSS author said €5 "is hard for many people to afford" and asked for yearly/lifetime options — [Phoronix](https://www.phoronix.com/news/Hyprland-Hyprperks); [It's FOSS](https://itsfoss.com/news/hyprland-premium); [hypr.land/news/hyprperks](https://hypr.land/news/hyprperks). Paid subscriptions end when Omacom's exclusive sponsorship starts 2026-10-10 — [omarchy.org/news](https://omarchy.org/news/2026/08/omacom-foundation-to-be-exclusive-hyprland-sponsor/)
- Paid Linux-only apps launched 2026: Hosaka Studio ($39/$79 one-time) — [hosaka.studio](https://hosaka.studio/); Screenix ($39/yr, $59 lifetime, $80/seat teams) — [screenix.studio](https://screenix.studio/); Screenix AUR package has 1 vote, popularity 0.0 (2026-10-05) — [AUR](https://aur.archlinux.org/rpc/v5/info?arg[]=screenix-bin)
- Cross-platform paid dev tools price Linux identically: Zed Pro $10/mo (cut from $20 in May 2026; Business $30/seat) — [CostBench](https://costbench.com/software/ai-coding-assistants/zed-ai/); Warp Build $20/mo with Linux in the free tier — [It's FOSS](https://itsfoss.com/news/warp.md); TablePlus and Proxyman sell perpetual licenses valid on Linux — [tableplus.com](https://tableplus.com/pricing); [proxyman.com](https://proxyman.com/pricing)
- Historical: Humble Indie Bundle (2011) average payment Linux $10.79 vs Mac $6.15 vs Windows $3.83 — [Revert to Saved](https://reverttosaved.com/2011/07/27/humble-indie-bundle-shows-mac-linux-and-window-user-thinking-regarding-software-pricing/); a 2013 indie game dev reported Mac+Linux as 18% of direct revenue — [GamingOnLinux](https://www.gamingonlinux.com/2013/03/the-developers-or-defenders-quest-show-off-linux-sales/page=1/)
- Omarchy demographic: created by DHH for 37signals' Ruby and Ops teams; 37signals is moving those teams off Macs over three years — [world.hey.com/dhh](https://world.hey.com/dhh/all-in-on-omarchy-68162450); Omarchy ships Rails-adjacent defaults (ruby, mise, docker, postgresql-libs, mariadb-libs, lazygit) — [omarchy-base.packages](https://raw.githubusercontent.com/omacom/omarchy/master/install/omarchy-base.packages); try-omarchy for macOS (2,568 stars) and "Omarchy M" target existing Mac owners — [GitHub API](https://api.github.com/orgs/omacom/repos?per_page=100); [omarchy.org/news](https://omarchy.org/news/2026/09/introducing-omarchy-m/)

### Inferences
- Omarchy's audience skews toward ex-Mac professional developers who already hold 1Password, Spotify, Typora and Cursor subscriptions; the distro normalises paying for best-in-class tools, so a $30-60 one-time or ~$5-9/mo Linux-native utility is within established norms for this group.
- The gap between demand signals (foundation donations, Hyprperks uptake, Cap Linux issue traffic) and actual uptake of the two paid Screen Studio clones suggests distribution, not willingness to pay, is the bottleneck: tools not in Omarchy's menus or AUR-with-votes stay invisible.
- A tool that ships via `omarchy pkg add` / AUR with an Omarchy theme hook (as Omasnap, omacut and Aether do) is more likely to be adopted than a Flatpak, given Hosaka's own "limited Flatpak support on wlroots" caveat.

### Gaps
- No revenue or Linux-share numbers from Zed, Warp, Sublime, Typora, Insomnia or Beeper were found; none publish per-OS breakdowns.
- Hyprperks subscriber count was never disclosed.
- Indie Hackers "have you ever paid for apps on Linux" thread (2022) could not be read (HTTP 403).
- No 2025-2026 survey specifically on Linux users' willingness to pay for desktop software was located before the search budget ran out.
