#!/usr/bin/env python3
"""Build the Unofficial Omarchy App Store — a static package browser for the official repo.

Reads the pacman database from pkgs.omarchy.org (falling back to the cached
copy in data/), joins it with the omarchy-pkgs git history for first-added
dates and PKGBUILD locations, joins it with the curated data/categories.json,
and writes one self-contained page plus fonts to dist/. No framework, no
tracker. Remote profile images stay on their upstream hosts; the store serves
no packages itself and only prints the official install command.
"""

import datetime
import html
import io
import json
import pathlib
import re
import subprocess
import tarfile
import urllib.parse
import urllib.request
from compression import zstd  # stdlib since Python 3.14

import ads

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
DB_URL = "https://pkgs.omarchy.org/stable/x86_64/omarchy.db"
DB_CACHE = ROOT / "data" / "omarchy.db"
PKGS_REMOTE = "https://github.com/omacom/omarchy-pkgs"
PKGS_REPO = ROOT / "data" / "omarchy-pkgs"
CATEGORIES_FILE = ROOT / "data" / "categories.json"
ENRICHMENT_FILE = ROOT / "data" / "enrichment.json"
INDIE_FILE = ROOT / "data" / "indie.json"
AUTHORS_FILE = ROOT / "data" / "authors.json"
FALLBACK_CATEGORY = "Utilities"
NEW_ARRIVALS = 4
CONTACT_URL = "https://x.com/jessyka_boat"
X_DM_RECIPIENT_ID = "1400492097082327040"
SUGGEST_APP_URL = "https://x.com/messages/compose?" + urllib.parse.urlencode({
    "recipient_id": X_DM_RECIPIENT_ID,
    "text": (
        "Hi! I'd like to suggest an app for the Unofficial Omarchy App Store wishlist.\n\n"
        "App name: \n"
        "Official project URL: \n"
        "Why it would be useful on Omarchy: \n"
        "Current Linux or AUR availability: "
    ),
})
SITE_URL = "https://omarchyapps.com"
AD_FAQ = [
    ("How does the rotation work?", "The header and footer each show three sponsors at a time and rotate through every active sponsor in order, on a fixed timer. Every sponsor gets exactly the same screen time, there is no bidding for position. The starting order changes daily so nobody is permanently first or last."),
    ("How long does a sponsorship last?", "Paid spots bill every 90 days and renew until you cancel, so your ad stays up as long as you want it. Cancel from the Stripe receipt email and the ad runs to the end of the paid term."),
    ("How do I pay?", "By card through Stripe, from the button on each spot. It is a subscription that renews every 90 days. After paying, send your ad details and it goes live within one business day."),
    ("What is an app profile banner?", "Your banner on your app's own page, the highest intent spot on the site, seen by everyone who looks up that app. Only the app's own sponsor can buy it."),
    ("What is the lifetime pin?", "One sponsor, pinned permanently at the top of the homepage. It never rotates out and never expires. There is no listed price: message @jessyka_boat on X with your offer and we talk it through."),
    ("Does sponsoring affect my package's listing or rank?", "No. Listings come from the official repository and rankings come from reader votes. A sponsor unit is a separate, labelled ad."),
]
SITE_NAME = "Unofficial Omarchy App Store"
GUIDES = [
    {
        "slug": "omarchy-vs-macos-windows-ubuntu",
        "title": "Omarchy vs macOS, Windows 11 and Ubuntu: Which Fits You?",
        "description": "Compare Omarchy with macOS, Windows 11 and Ubuntu for development, gaming, creative work, hardware support, privacy and daily use.",
        "eyebrow": "Operating system comparison",
        "heading": "Omarchy vs <span>macOS, Windows & Ubuntu</span>",
        "tagline": "Four very different desktops, compared without pretending one is best for everyone.",
        "answer": "Choose Omarchy for a keyboard-first, highly curated Arch and Hyprland workflow; Ubuntu for a familiar, broadly documented Linux desktop; macOS for Apple hardware and Apple-only creative tools; or Windows 11 for the widest commercial software, peripheral and PC-gaming compatibility.",
        "faqs": [
            ("Is Omarchy easier than Ubuntu?", "Usually not for a Linux beginner. Omarchy is intentionally keyboard-first and terminal-heavy, while Ubuntu emphasizes a conventional graphical desktop and long-term support."),
            ("Can Omarchy replace macOS or Windows for development?", "For web, backend, terminal and many AI-assisted workflows, it can. Check any Apple-only, Windows-only, corporate VPN, anti-cheat or specialist hardware requirements before switching."),
            ("Is Omarchy based on Ubuntu?", "No. Omarchy is based on Arch Linux and uses Hyprland and Quickshell. Ubuntu is Debian-based and uses GNOME by default."),
        ],
    },
    {
        "slug": "free-notion-alternative-linux-slap-notes",
        "title": "Free Notion Alternative for Linux: Slap Notes Compared",
        "description": "Looking for a free Notion alternative on Linux? Compare Slap Notes with Notion, Obsidian and AppFlowy for local notes, blocks, links and privacy.",
        "eyebrow": "Linux notes comparison",
        "heading": "A free Notion alternative for Linux: <span>Slap Notes</span>",
        "tagline": "Local-first blocks, linked notes and an optional research agent—without requiring a cloud workspace.",
        "answer": "Slap Notes is a strong free Notion alternative for Linux users who want Notion-style blocks, Obsidian-style links and local storage in one native app. Choose Notion for polished cloud collaboration, Obsidian for a mature Markdown ecosystem, or AppFlowy for open-source databases and team features.",
        "faqs": [
            ("Is Slap Notes free?", "Yes. Slap Notes is a free, open-source project and the Omarchy package is listed as free software."),
            ("Does Notion have an official Linux desktop app?", "Notion currently documents desktop apps for macOS and Windows. Linux users can use Notion in a supported web browser."),
            ("Does Slap Notes require an account?", "No. Its public product page describes a local-first experience with no required account or sync service."),
        ],
    },
    {
        "slug": "free-video-editor-linux-omarchy",
        "title": "Free Video Editor for Linux: Omacut vs DaVinci Resolve",
        "description": "Need a free video editor on Linux? Learn when Omarchy-native Omacut is faster than DaVinci Resolve, Kdenlive or Final Cut Pro for simple video trimming.",
        "eyebrow": "Linux video editing guide",
        "heading": "A free video editor for Linux: <span>start with Omacut</span>",
        "tagline": "For a clean trim, a heavyweight timeline can be more tool than the job needs.",
        "answer": "Use Omacut when you only need to trim the beginning or end of a clip and export an MP4 quickly on Omarchy. Use Kdenlive or DaVinci Resolve for multitrack timelines, titles, effects and color work. Final Cut Pro is a Mac-only choice and does not run natively on Linux.",
        "faqs": [
            ("Is Omacut a full replacement for DaVinci Resolve?", "No. Omacut is deliberately a focused video trimmer. DaVinci Resolve is a full editing, color, audio and effects suite."),
            ("Can Final Cut Pro run on Linux?", "No native Linux version is offered. Apple's current system requirements specify macOS."),
            ("Is Omacut included with Omarchy?", "The official Omacut project says it is installed by default on new Omarchy installations from Quattro forward and is also available as the omacut package."),
        ],
    },
    {
        "slug": "best-apps-for-omarchy",
        "title": "Best Omarchy Apps to Install First: 12 Useful Picks",
        "description": "Start a new Omarchy setup with 12 useful apps for notes, files, themes, video, screenshots, gaming, remote access and developer work.",
        "eyebrow": "Starter app guide",
        "heading": "The best Omarchy apps to <span>install first</span>",
        "tagline": "A practical starter set chosen by job, not a pile of packages to install blindly.",
        "answer": "The best Omarchy apps are the ones that fill a real gap in your workflow. Start with a small set: LocalSend for transfers, Slap Notes for local knowledge, Strata for files, Aether for themes and Omacut for quick video trims—then add specialist tools only when you need them.",
        "faqs": [
            ("What should I install first on Omarchy?", "Start with one app for each recurring task you actually have. LocalSend, a notes app, a file manager and one creative tool make a useful first pass."),
            ("Are every one of these apps official Omarchy projects?", "No. The official repository includes a mix of Omarchy projects, upstream third-party software and independent community apps. Each profile links to its real project source."),
            ("Does this list automatically install anything?", "No. The guide only links to package profiles. You decide what to install and run the displayed Omarchy command yourself."),
        ],
    },
    {
        "slug": "how-to-install-apps-on-omarchy",
        "title": "How to Install Apps on Omarchy Safely",
        "description": "Learn how to install, inspect, update and remove apps on Omarchy using the official package repository, Arch packages and the AUR.",
        "eyebrow": "Omarchy package guide",
        "heading": "How to install apps on <span>Omarchy</span>",
        "tagline": "Use the official repository first, inspect unfamiliar software, and let Omarchy handle full-system updates.",
        "answer": "For an app in the official Omarchy package repository, use the profile's copyable omarchy pkg add command. For other software, check Omarchy's Install menu, Arch repositories and then the AUR. Review the source and permissions first, and use Omarchy's own update flow instead of a direct full pacman or yay upgrade.",
        "faqs": [
            ("What command installs a package from the Omarchy repository?", "Package profiles in this directory provide a copyable omarchy pkg add command using the exact current package name."),
            ("Can I use pacman and the AUR on Omarchy?", "Yes. Omarchy is Arch-based, and its manual points users to Arch packages and the AUR when needed. Full system updates should still go through Omarchy's update flow."),
            ("Does the Unofficial Omarchy App Store host packages?", "No. It is a directory. Install commands retrieve software through Omarchy and the configured package sources, not from this website."),
        ],
    },
    {
        "slug": "how-to-use-omarchy-zsh",
        "title": "omarchy-zsh on Omarchy: install, fzf keybindings, aliases & the chsh trap",
        "description": "Install omarchy-zsh on Omarchy the safe way (not chsh), learn the fzf keybindings and built-in aliases, and fix common issues like double inits and oh-my-zsh conflicts.",
        "eyebrow": "Omarchy shell guide",
        "heading": "omarchy-zsh on <span>Omarchy</span>",
        "tagline": "Zero-config Zsh with Omarchy's aliases — installed the safe way, not with chsh.",
        "answer": "Install omarchy-zsh with omarchy pkg add omarchy-zsh, then run omarchy-setup-zsh. Keep bash as your login shell — the setup auto-launches zsh from it. Do not use chsh: it breaks Omarchy's session startup.",
        "faqs": [
            ("How do I switch to zsh on Omarchy?", "Run omarchy pkg add omarchy-zsh, then omarchy-setup-zsh. Keep bash as your login shell — the setup makes zsh auto-launch from your ~/.bashrc. Do not use chsh; it breaks Omarchy's session startup."),
            ("Will it overwrite my .zshrc?", "The setup writes a small loader ~/.zshrc. If you already have one with real content, back it up first. Package updates never touch ~/.zshrc; everything system-owned lives under /usr/share/omarchy-zsh/."),
            ("omarchy-zsh vs oh-my-zsh?", "omarchy-zsh ports Omarchy's shared shell config to Zsh with fzf keybindings; it's small, fast, and Omarchy-aware. oh-my-zsh is a huge plugin framework — you can run it on Omarchy, but disable its duplicated inits and never define functions over omarchy's aliases."),
            ("Do my bash habits carry over?", "Mostly, yes. The aliases, functions, and env vars are the same ones Omarchy ships for bash, and the syntax is compatible. The prompt is starship in both."),
            ("How do I go back to plain bash?", "Remove the package with sudo pacman -R omarchy-zsh, then restore ~/.bashrc from a .bashrc.backup-* file or remove the exec zsh line."),
        ],
    },
    {
        "slug": "rustdesk-on-omarchy",
        "title": "How to Install & Use RustDesk on Omarchy (2026) — Free TeamViewer Alternative",
        "description": "Install RustDesk on Omarchy with one command. Free, open-source remote desktop: ID/password flow, unattended access, self-hosting, and fixes for the Wayland black-screen issue on Hyprland.",
        "eyebrow": "Remote desktop guide",
        "heading": "RustDesk on <span>Omarchy</span>",
        "tagline": "Free, open-source remote desktop — the $0 answer to TeamViewer's $50.90/mo.",
        "answer": "Install RustDesk with omarchy pkg add rustdesk, launch it, and connect with the 9-digit ID and password. No account, no payment. On Hyprland/Wayland, accept the screen-share prompt the first time.",
        "faqs": [
            ("Does RustDesk work on Omarchy/Wayland?", "Yes, with one caveat. Inside a logged-in Hyprland session, RustDesk captures via PipeWire and xdg-desktop-portal-hyprland — accept the screen-share prompt the first time and it works."),
            ("Is RustDesk really free?", "Yes. The client and self-hostable server are AGPL-3.0 open source and free forever. The paid product is RustDesk Server Pro for teams; core remote-desktop functionality is not gated."),
            ("RustDesk vs TeamViewer — which should I pick?", "Pick RustDesk for remote control, file transfer, and unattended access without a $50.90/mo bill. Pick TeamViewer for the enterprise admin console, compliance features, or third-party integrations."),
            ("Is RustDesk safe?", "Sessions are end-to-end encrypted and the code is open source. With a self-hosted server, sessions never pass through third-party infrastructure. Use a strong permanent password and keep RustDesk updated."),
        ],
    },
    {
        "slug": "flea-file-manager-omarchy",
        "title": "How to Install & Use Flea on Omarchy (2026)",
        "description": "Install Flea on Omarchy with one command. Keyboard-first file manager with Quick Look, undoable operations, and network shares. Setup, shortcuts, and real fixes from the issue tracker.",
        "eyebrow": "Omarchy file manager guide",
        "heading": "Flea on <span>Omarchy</span>",
        "tagline": "The keyboard-first file manager that feels like it belongs on Omarchy.",
        "answer": "Install Flea with omarchy pkg add flea, then make it your default with flea --default. You get Vim-style navigation, Space-bar Quick Look previews, undoable file operations, and network shares — all following your Omarchy theme.",
        "faqs": [
            ("Does Flea work on Omarchy?", "Yes — it's built exclusively for Omarchy. omarchy and quickshell are hard dependencies, and per the install docs it will not install on a plain Arch box. The Omarchy repo carries it as flea, and the AUR carries the faster-updating flea-bin."),
            ("Is Flea free?", "Yes. It's MIT-licensed open source. There's an optional GitHub Sponsors link and a Buy Me a Coffee page, but no paid tier, no trial, no feature gates."),
            ("How do I make Flea my default file manager?", "Run flea --default in a terminal inside your Omarchy session. It sets the inode/directory handler, routes Show-in-folder requests to Flea, and binds Super+Shift+F to it. Undo with flea --default off."),
            ("Can Flea replace the file Open/Save dialogs?", "Yes. flea --picker makes Flea answer the org.freedesktop.impl.portal.FileChooser contract, replacing the GTK Open/Save dialog in every portal-using app (including Flatpaks), then restart the portal: systemctl --user restart xdg-desktop-portal. Revert with flea --picker off."),
            ("How do I uninstall Flea cleanly?", "Run the integration undo first, then drop the package: flea --default off then omarchy pkg drop flea. Skipping the undo leaves stale per-user state (a D-Bus service file naming the removed binary, inode/directory handler lines, Hyprland keybinds)."),
        ],
    },
    {
        "slug": "omacut-video-editor-omarchy",
        "title": "How to Use omacut on Omarchy (2026): trim, split & export in minutes",
        "description": "omacut is Omarchy's dead-simple video trimmer (preinstalled on Quattro+). Open a video, drag the handles, split the middle, export an MP4 — plus shortcuts and fixes for AV1 black preview and export failures.",
        "eyebrow": "Omarchy video trimmer guide",
        "heading": "Use omacut on <span>Omarchy</span>",
        "tagline": "Open a video, cut the boring parts, export an MP4. That's the whole app.",
        "answer": "omacut ships by default on Omarchy 4.x (Quattro) and newer; older installs use omarchy pkg add omacut. Open a video with Ctrl+O, drag the start/end handles, double-click to split out middle sections, and export with Ctrl+S as an MP4.",
        "faqs": [
            ("Does omacut work on Omarchy?", "Yes — it's made for Omarchy. Written by DHH/omacom, it follows your theme's accent color, and it's installed by default in Omarchy from Quattro (v4.x) onward. Install manually with omarchy pkg add omacut on older installs."),
            ("Is omacut free?", "Yes, free and libre — MIT licensed, source on GitHub at omacom/omacut. No accounts, no watermarks, no upsells."),
            ("omacut vs LosslessCut — which should I use?", "omacut for speed and native Omarchy looks; it re-encodes, so exports are fast but not instant. LosslessCut for lossless (no re-encode) cuts that finish in seconds with zero quality loss — at the cost of an Electron app that doesn't match your theme. For cutting the dead air off a screen recording, omacut wins."),
            ("Can omacut cut the middle out of a video, or just the ends?", "The middle too. Double-click a clip to split it, drag the handles apart to remove the section between them, double-click the gap to join it back. Playback skips the gaps and exports the clips in order."),
            ("Why does my AV1 video show a black preview?", "That's a known Qt/ffmpeg hardware-decode issue fixed in omacut (Oct 2026) — update to the latest build. If it persists on unusual GPUs, run QT_FFMPEG_DECODING_HW_DEVICE_TYPES=vaapi,cuda omacut."),
        ],
    },
    {
        "slug": "sunshine-game-streaming-omarchy",
        "title": "How to Install & Use Sunshine on Omarchy (2026)",
        "description": "Install Sunshine on Omarchy and stream your games to any device with Moonlight. Pairing walkthrough, Hyprland capture-method fixes, and how it replaces NVIDIA GameStream.",
        "eyebrow": "Game streaming guide",
        "heading": "Sunshine on <span>Omarchy</span>",
        "tagline": "Turn your Omarchy PC into your own cloud-gaming server — free, no tiers.",
        "answer": "Install Sunshine with omarchy pkg add sunshine, open https://localhost:47990 to set credentials, and pair Moonlight on your phone, laptop, or Steam Deck with the one-time PIN. Your host's GPU encodes the stream in hardware.",
        "faqs": [
            ("Does Sunshine work on Omarchy/Hyprland?", "Yes — Omarchy is Arch-based, and the official docs cover Arch installs directly. On Hyprland (Wayland) prefer the KMS or PipeWire capture method; there are recent wlroots capture regressions (#5018), so if you get a black screen, switch capture methods in Configuration → Advanced first."),
            ("Is Sunshine free?", "Completely. It's free and open-source (LizardByte, GPL-licensed), with no paid tiers, no feature gates, no accounts, and no telemetry. Everything — hardware encoding, multi-client streaming, virtual displays, HDR — is in the same free build."),
            ("Sunshine vs Parsec — which should I use?", "For playing your own games remotely, Sunshine + Moonlight is free forever and matches Parsec's paid tiers on the features that matter (encoders, latency, gamepads). Pick Parsec if you want zero-config internet connectivity and session sharing — its $9.99/mo Warp buys convenience and relay infrastructure, not better streaming quality."),
            ("Do I need an NVIDIA GPU?", "No. Sunshine uses hardware encoding on AMD (VAAPI), Intel (VAAPI/QuickSync), and NVIDIA (NVENC) GPUs, with software x264/x265 as a fallback. This was NVIDIA GameStream's biggest limitation; Sunshine removed it."),
            ("Can I stream outside my home?", "Yes, two ways: forward the streaming ports on your router (TCP 47984, 47989, 48010; UDP 47998–48000, 48002, 48010), or install Tailscale on host and client and connect Moonlight to the host's Tailscale IP — no port forwarding, works behind CGNAT."),
        ],
    },
    {
        "slug": "hermes-desktop-omarchy",
        "title": "How to Install & Use Hermes Desktop on Omarchy (2026)",
        "description": "Install Hermes Desktop on Omarchy: the native GUI for Hermes Agent with memory, skills, scheduled tasks, and messaging integrations. Bring your own key, use Nous Portal's free tier, or run local models.",
        "eyebrow": "AI agent guide",
        "heading": "Hermes Desktop on <span>Omarchy</span>",
        "tagline": "A self-improving AI agent with a chat window — no terminal required.",
        "answer": "Install with omarchy pkg add hermes-desktop, pick Local mode in the first-run wizard, and connect a provider — an OpenRouter key, Nous Portal's free tier, or a local Ollama/LM Studio endpoint for $0. You get chat with memory, skills, scheduled tasks, and messaging gateways.",
        "faqs": [
            ("Does Hermes Desktop work on Omarchy?", "Yes — install with omarchy pkg add hermes-desktop. It's an Electron app (Linux AppImage/.deb/.rpm builds ship upstream), and the underlying Hermes Agent is a Unix-native Python tool, so Arch/Linux is its home turf."),
            ("Is Hermes Desktop free?", "Yes. The app is open-source under the MIT License. But it's a client, not a model — you supply the intelligence via your own provider key, a local model, or Nous Portal's free tier."),
            ("Do I need an API key?", "Not necessarily. You need a provider, but that can be a free one: Ollama or LM Studio running locally (no key at all), Nous Portal's free tier, or OpenRouter's free models. A paid key (OpenRouter/Anthropic/OpenAI/etc.) just buys you stronger models."),
            ("Can I run it against a remote Hermes server?", "Yes — the first-run wizard offers Remote mode (API URL + key). But know the caveat: in Remote mode several screens (Schedules, Skills, Gateway, Providers, Memory) are degraded or unavailable, and HTTPS remote sign-in has a known cookie bug (#996). Local mode is the smooth path."),
            ("Does it remember me across sessions?", "Yes — that's the headline feature. Persistent memory, session history with full-text search, and a skill system that distills repeated tasks into reusable knowledge. Check the Memory screen to see what it knows, and back it up from Settings before migrating machines."),
        ],
    },
    {
        "slug": "omawrite-writing-omarchy",
        "title": "Omawrite on Omarchy: Install, Shortcuts & Typora Alternative Guide",
        "description": "Omawrite is Omarchy's free default Markdown editor — a distraction-free, open-source Typora alternative. Install guide, keyboard shortcuts, real GitHub issues, and how to switch from Typora.",
        "eyebrow": "Omarchy writing guide",
        "heading": "Omawrite on <span>Omarchy</span>",
        "tagline": "The cleanest place to put words down on Omarchy — already installed.",
        "answer": "Omawrite ships by default on Omarchy 4.0 Quattro and newer; older installs use omarchy pkg add omawrite. Open it and write — Markdown syntax dims instead of shouting, drafts recover after crashes, and Pandoc covers the exports it skips.",
        "faqs": [
            ("Does Omawrite work on Omarchy?", "Yes — it's a first-class Omarchy citizen. It installs from the Omarchy package repository via omarchy pkg add omawrite and has been preinstalled on every fresh Omarchy install since version 4.0 Quattro. It's also in the AUR for other Arch-based systems."),
            ("Is Omawrite free?", "Yes, completely. It's MIT-licensed open source (omacom/omawrite), with the bundled IBM Plex Mono font under the SIL Open Font License. No trial, no paid tier, no account."),
            ("Omawrite vs Typora — which should I use?", "If you write Markdown and want zero friction, Omawrite — free, lighter, already installed, and Omarchy's chosen default. If you regularly export to Word/EPUB or live in custom themes, Typora's $14.99 buys you that. Most people can cover the export gap with Pandoc and keep the $14.99."),
            ("Does Omawrite have a preview mode?", "Not a side-by-side WYSIWYG preview — the editor is the view, with syntax dimmed rather than hidden. Print (Ctrl+P) renders real Markdown to PDF, which is the closest thing to a preview."),
            ("Will I lose my draft if it crashes?", "No — unsaved drafts are recovered after an abnormal exit, and the app warns you before an external edit to an open file can overwrite your work."),
        ],
    },
    {
        "slug": "strata-file-manager-omarchy",
        "title": "Strata on Omarchy: Install the Keyboard-First File Manager",
        "description": "Install Strata on Omarchy: the free keyboard-first GTK4 file manager with Miller columns, fuzzy search, and sandboxed previews. Setup, keybinds, fixes, and Strata vs flea compared.",
        "eyebrow": "Omarchy file manager guide",
        "heading": "Strata on <span>Omarchy</span>",
        "tagline": "Finder-style Miller columns with a preview engine that sandboxes everything.",
        "answer": "Install Strata with omarchy pkg add strata. You get navigable Miller columns, Ctrl+K fuzzy filename search that streams results while indexing, and rich previews rendered inside a Bubblewrap sandbox so untrusted files can't touch your system.",
        "faqs": [
            ("Does Strata work on Omarchy?", "Yes — Arch Linux and Omarchy are the project's primary supported environments, and Strata is explicitly designed for Omarchy. Requirements: glibc 2.39+ and GTK 4.12+. It follows the active Omarchy theme live (including Quattro), and the README documents Hyprland keybind overrides, udiskie encrypted-volume unlock, and SMB support via gvfs-smb."),
            ("Is Strata free?", "Yes. MIT-licensed, free and libre — no paid tiers, no feature gates. In-app updates are built in (on by default; disable in Settings → Updates)."),
            ("Strata vs flea?", "Both keyboard-first, both free, both on omarchyapps.com. Strata = Rust + GTK4, Miller columns, the richest preview engine, sandboxed parsers. flea = Rust + Quickshell, built Omarchy-first, leans into raw speed and native theme integration. Same price (zero). Columns and previews → Strata; Omarchy-native speedster → flea."),
            ("Why do some previews show 'Preview unavailable'?", "Almost always a missing sandbox dependency, not a Strata bug. Parser-backed previews require bubblewrap; video thumbnails need ffmpegthumbnailer/ffmpeg. Install the full runtime set (see the guide's first issue) and restart Strata. Strata fails closed by design — it will never run an untrusted parser unsandboxed just to show a thumbnail."),
            ("Can Strata replace Nautilus as my default file manager?", "Yes, two layers: Settings → General → Desktop integration sets Strata as the inode/directory handler and installs the FileManager1 D-Bus service. Then, on Lua-based Omarchy releases, override the stock Nautilus shortcuts (Super+Shift+F, Super+Alt+Shift+F) in ~/.config/hypr/bindings.lua — those user overrides survive Omarchy updates."),
        ],
    },
    {
        "slug": "claude-desktop-omarchy",
        "title": "Claude Desktop on Omarchy: Install & Setup Guide (2026)",
        "description": "Install Anthropic's official Claude Desktop Linux app on Omarchy. Setup, MCP connectors, Cowork VM troubleshooting, and the Hyprland login fix.",
        "eyebrow": "AI assistant guide",
        "heading": "Claude Desktop on <span>Omarchy</span>",
        "tagline": "Anthropic's official Linux app, repackaged for Arch — chat, MCP, and Cowork agents.",
        "answer": "Install with omarchy pkg add claude-desktop. The package repackages Anthropic's official Linux .deb (beta); the app binary is Anthropic's, the Arch packaging is community-maintained. Sign in via the claude.ai redirect, connect MCP servers for local file access, and use Cowork for autonomous agent tasks.",
        "faqs": [
            ("Is there an official Claude desktop app for Linux?", "Yes — since June 30, 2026, Anthropic ships a first-party Linux beta as a .deb (amd64 + arm64) from its own signed APT repository at downloads.claude.ai. It's a beta and it doesn't auto-update itself, but it's Anthropic's code, not a third-party port."),
            ("Is claude-desktop on Omarchy official?", "Half and half. The app binary is Anthropic's official Linux build, downloaded from Anthropic's own repository. But Anthropic doesn't ship an Arch package — the one omarchy pkg add installs is maintained by the Omarchy community in omarchy-pkgs, and Anthropic won't support issues with it. Report packaging problems to Omarchy, not Anthropic."),
            ("Is it free?", "The app is free to install and free to use with a free Claude account (no signed-out mode — you need an account). Capability limits follow your Claude plan: Free, Pro ($20/mo), Max, etc."),
            ("Does it work offline or run a model locally?", "No to both. Every message goes to Anthropic's servers. The virtual machine Cowork uses is a sandbox around what Claude can touch — it's not a local model."),
            ("Where do MCP settings live?", "~/.config/Claude/claude_desktop_config.json. Quit the app before editing it by hand."),
        ],
    },
    {
        "slug": "1password-omarchy",
        "title": "How to Install & Use 1Password on Omarchy (2026)",
        "description": "Install 1Password on Omarchy with one command. Setup, browser integration, real Linux fixes, and how it compares to free Bitwarden.",
        "eyebrow": "Password manager guide",
        "heading": "1Password on <span>Omarchy</span>",
        "tagline": "The polished commercial password manager — and the free Bitwarden alternative.",
        "answer": "Install with omarchy pkg add 1password. Sign in with your sign-in address, email, Secret Key, and master password. 1Password is paid (14-day trial, then Individual from $2.99/mo billed annually) — Bitwarden's free tier covers ~90% of the same ground.",
        "faqs": [
            ("Does 1Password work on Omarchy/Linux?", "Yes. 1Password ships an official Linux app (Electron frontend, Rust crypto core), and the AUR packages are maintained by 1Password themselves. Install with omarchy pkg add 1password. The main Linux-specific gotchas are browser sandboxing (use a native browser, not Flatpak/Snap) and Wayland clipboard quirks — both covered in the guide."),
            ("Is 1Password free?", "No. There is no free tier — just a 14-day trial. Individual starts at $2.99/mo billed annually (promotional rate for new signups; list price $3.99/mo after the March 2026 price increase), Families runs $4.99–$5.99/mo. If free matters, Bitwarden's free tier is the move."),
            ("1Password vs Bitwarden — which should I pick?", "Pick Bitwarden if price is the deciding factor: free, open source, self-hostable, and ~90% of the functionality. Pick 1Password if you want the most polished experience — best-in-class browser extension, passkeys, Watchtower health reports, and an SSH agent that just works — and you're fine paying ~$36–$48/yr for it."),
            ("Do I need the beta or the CLI?", "No. 1password (stable) is the right default. Grab 1password-beta if you're chasing a specific fix (clipboard and Wayland fixes often land there first). Grab 1password-cli if you want op in the terminal — pair it with the desktop app's CLI integration so you never manage session tokens by hand."),
            ("Which browsers work with 1Password on Omarchy?", "Chromium and Firefox, installed natively (not Flatpak/Snap), work out of the box with the official extension. Anything else (Vivaldi, Zen, Floorp) needs the /etc/1password/custom_allowed_browsers allowlist entry described in the guide."),
        ],
    },
    {
        "slug": "omadesign-omarchy",
        "title": "Omadesign on Omarchy: Install & Setup Guide (2026)",
        "description": "Install Omadesign, the free Linux design, paint, photo and motion app, on Omarchy. One-line install, theme integration, fixes, and why there is no package yet.",
        "eyebrow": "Creative suite guide",
        "search_terms": ["omadesign", "oma design", "affinity", "photoshop", "illustrator", "figma", "inkscape", "gimp", "krita"],
        "package_watch": {
            "app": "Omadesign",
            "names": ["omadesign", "omadesign-bin"],
            "fallback_cta": '<div><h2>Get Omadesign</h2><p>There is no package page on this site yet because there is no Omarchy package. The releases page has the tarballs, checksums and changelog.</p></div><a class="button" href="https://github.com/michaelmonetized/omadesign/releases" target="_blank" rel="noopener">Omadesign releases →</a>',
        },
        "heading": "Omadesign on <span>Omarchy</span>",
        "tagline": "A free, native, Omarchy-themed design, paint, photo and motion app. Alpha, and not in the package repo yet.",
        "answer": "Install with curl -fsSL https://omadesign.app/install | sh. The omadesign-bin package was merged into the Omarchy repo on October 11, 2026 but is on the edge ring only until the next release train promotes it to stable. Omadesign is free (MIT), follows your Omarchy theme and font, and updates itself from About > Update.",
        "faqs": [
            ("Does Omadesign work on Omarchy?", "Yes, it was built for it. The UI reads your Omarchy theme colors and font on launch and repaints when you switch themes. It runs natively on Wayland under Hyprland, on both x86_64 and Apple Silicon via Asahi. Expect a 4-core or sub-8 GB machine to feel slow."),
            ("Is Omadesign free?", "Completely, under the MIT license. No trial, no paid tier, no account for local work. The cloud sharing features need a sign-in but there is no published pricing for them."),
            ("Why isn't Omadesign in the Omarchy app store?", "Because it is not on the stable channel yet. The omadesign-bin package was merged into the official repo on October 11, 2026 and is live on the edge ring. Stable gets it with the next Omarchy release train, and this site lists stable."),
            ("Omadesign vs Inkscape, which should I pick?", "Inkscape if you need a specific SVG feature or you ship files to people on other tools. Omadesign if you want raster, photo and motion in the same window and prefer a native GUI over GTK3. Many people will keep both installed."),
            ("How do I update Omadesign?", "Omadesign > About > Update, which reruns the official installer and restarts with your documents open. Rerunning the curl one-liner does the same thing from a terminal. There is no pacman path."),
        ],
    },
]
FAQ = [
    ("What is the Unofficial Omarchy App Store?", "It is an independent, searchable directory of packages published by the official Omarchy package repository. It is not affiliated with or endorsed by Omarchy or Omacom."),
    ("How do I install an app on Omarchy?", "Open a package, review its requirements, then copy the displayed omarchy pkg add command into a terminal. Packages are downloaded from the official Omarchy repository, not from this site."),
    ("Does this site host or sell apps?", "No. The site hosts no packages and sells no software. It organizes public package information and links visitors to upstream projects and official PKGBUILDs."),
    ("How can a developer update or claim an app listing?", "Open the package and choose Claim this app. The X direct-message form asks for the developer's role, project URL, corrections, screenshots, and an optional demo video."),
    ("How do I request or vote for an app?", "Use Top Apps to upvote packages already in the repository. To suggest a missing project, use the homepage suggestion bar to send @jessyka_boat a direct message on X."),
    ("How do app upvotes work?", "Use the up-arrow button on any listed package. The public total is stored with this site and survives deployments. A secure anonymous browser cookie recognizes prior votes without requiring an account or email address."),
    ("How do I share a specific app?", "Use Share on any package card or profile. On supported devices it opens the system share sheet; otherwise it copies that app's permanent omarchyapps.com profile URL."),
    ("What does the Indie app sticker mean?", "It is a curated community label for an app or tool currently understood to be independently maintained. It is not an official Omarchy certification or endorsement, and developers can request a correction."),
    ("How can I prepare an app for Omarchy?", "Use the Develop for Omarchy checklist for packaging, permissions, checksums, desktop integration, clean-build testing, and pull-request preparation. Official repository guidance always takes precedence."),
]

# Fixed order controls both the catalogue's section order and the category
# filter row. Deliberately not alphabetical: biggest/most-relevant first.
CATEGORY_ORDER = [
    "AI & Agents", "Developer Tools", "Terminal & Shell", "Themes & Desktop",
    "System & Drivers", "Gaming & Emulation", "Media & Creative",
    "Productivity & Notes", "Security & Privacy", "Browsers & Web",
    "Communication", "Utilities",
]
# One hue per category, from Tokyo Night's documented palette (omarchy.org's
# own root.css only wires up the subset it uses on the marketing page — the
# rest of the theme's colors are still Tokyo Night, not invented). Blue,
# green, terminal-white, and turquoise are reserved elsewhere (body text,
# data/versions, headings, hover) so no category may use them. Big categories
# get the most mutually distinct hues since they appear most often; small
# ones can sit closer together. Every place a hue appears, the category name
# is always printed alongside it — color is a support signal, never the only one.
CATEGORY_COLOR = {
    "System & Drivers": "41A6B5",     # deep teal — 34 pkgs, the largest hued bucket
    "Utilities": "565F89",            # comment grey — 31 pkgs, deliberately unfiled-looking
    "Gaming & Emulation": "F7768E",   # red
    "Themes & Desktop": "9D7CD8",     # purple
    "AI & Agents": "7DCFFF",          # cyan
    "Developer Tools": "E0AF68",      # yellow
    "Media & Creative": "73DACA",     # teal-green
    "Terminal & Shell": "0DB9D7",     # cyan-blue
    "Security & Privacy": "DB4B4B",   # deep red
    "Productivity & Notes": "BB9AF7", # magenta
    "Browsers & Web": "737AA2",       # muted slate — 2 pkgs
    "Communication": "A9B1D6",        # near-white muted — 1 pkg
}


def fetch_db() -> bytes:
    # pkgs.omarchy.org 403s the default Python-urllib agent; identify like a client.
    req = urllib.request.Request(DB_URL, headers={"User-Agent": "omarchy-appstore-build/1.0"})
    try:
        raw = urllib.request.urlopen(req, timeout=30).read()
        DB_CACHE.write_bytes(raw)
        print(f"db: fetched fresh ({len(raw):,} bytes)")
    except OSError as e:
        raw = DB_CACHE.read_bytes()
        print(f"db: offline ({e}); using cached copy")
    return raw


def sync_pkgbuilds() -> None:
    """Blob-less clone of omarchy-pkgs: ~3 MB, and its history is the only
    source of 'when was this package added' — the pacman db only knows last build."""
    try:
        if (PKGS_REPO / ".git").exists():
            subprocess.run(["git", "-C", str(PKGS_REPO), "pull", "--ff-only", "--quiet"], check=True, timeout=120)
        else:
            subprocess.run(["git", "clone", "--quiet", "--filter=blob:none", PKGS_REMOTE, str(PKGS_REPO)], check=True, timeout=300)
        print("omarchy-pkgs: synced")
    except (subprocess.SubprocessError, OSError) as e:
        print(f"omarchy-pkgs: offline ({e}); using checkout as-is")


OMARCHY_PKGS_URLS = {"https://github.com/omacom-io/omarchy-pkgs", "https://github.com/omacom/omarchy-pkgs"}


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _related(pkgname: str, pkgbase: str, repo: str) -> bool:
    """A source array can carry a build-time toolchain download (a JDK, a
    vendored plugin) alongside the real project tarball — a bare 'found a
    github link' match can't tell those apart. Require the repo name to
    actually resemble the package before trusting it; a missed link is far
    cheaper than presenting a stranger's project as this one's."""
    r = _norm(repo)
    if not r:
        return False
    for cand in (pkgname, pkgbase):
        n = _norm(cand)
        n_stripped = re.sub(r"(bin|git|cli|dev)$", "", n)
        if n in r or r in n or (n_stripped and n_stripped in r):
            return True
    return False


def extract_github_repo(pkgbuild_text: str, pkg_url: str, pkgname: str = "", pkgbase: str = "") -> str | None:
    """Best-effort: find the package's own upstream GitHub repo (distinct from
    the omarchy-pkgs build recipe) by scanning PKGBUILD source=()/source_*=()
    arrays, substituting the PKGBUILD's own scalar variables (pkgname, pkgver,
    _appname, ...) where referenced. Returns None rather than guess wrong —
    a wrong link is worse than no link.

    Only worth attempting when the package's real homepage is NOT already a
    GitHub link: a source array often vendors a second, unrelated dependency
    from its own GitHub repo (e.g. omarchy-fish bundles fzf.fish, omarchy-zsh
    bundles omadots) — grabbing "the first github.com URL in source=" would
    silently present that unrelated project as if it were this one."""
    if pkg_url.startswith("https://github.com/"):
        return None
    scalars = {}
    for m in re.finditer(r"^(_?[a-zA-Z][\w]*)=(['\"]?)([^\n'\"]*)\2\s*$", pkgbuild_text, re.M):
        name, _, val = m.groups()
        if "(" not in val:
            scalars.setdefault(name, val)
    pm = re.search(r"^pkgname=([^\s(][^\n]*)", pkgbuild_text, re.M)
    if pm:
        scalars.setdefault("pkgname", pm.group(1).strip("'\""))

    def resolve(s: str) -> str:
        for _ in range(4):
            new = re.sub(r"\$\{?(\w+)\}?", lambda m: scalars.get(m.group(1), m.group(0)), s)
            if new == s:
                break
            s = new
        return s

    candidates = []
    for m in re.finditer(r"^source(?:_\w+)?=\(([^)]*)\)", pkgbuild_text, re.M | re.S):
        candidates.append(m.group(1))
    candidates.append(pkg_url or "")

    for block in candidates:
        for raw in re.findall(r"https://github\.com/[^\s'\")]+", block):
            resolved = resolve(raw)
            if "$" in resolved:
                continue
            m = re.match(r"https://github\.com/([\w.-]+)/([\w.-]+)", resolved)
            if not m:
                continue
            owner, repo = m.groups()
            repo = re.sub(r"\.git$", "", repo)
            url = f"https://github.com/{owner}/{repo}"
            if url in OMARCHY_PKGS_URLS:
                continue
            if not _related(pkgname, pkgbase, repo):
                continue
            return url
    return None


def pkgbuild_index() -> dict:
    """Map every pkgname and pkgbase in omarchy-pkgs to (directory, first-added
    timestamp, github repo url or None). Split packages (yaru-*,
    libretro-vice-*) live under one directory, so the directory — not
    pacman's %BASE% — is what a PKGBUILD link needs."""
    index = {}
    root = PKGS_REPO / "pkgbuilds"
    if not root.exists():
        return index
    for d in sorted(root.iterdir()):
        pkgbuild = d / "PKGBUILD"
        if not pkgbuild.exists():
            continue
        text = pkgbuild.read_text(encoding="utf-8", errors="replace")
        names = {d.name}
        for m in re.finditer(r"^pkg(?:name|base)=\(([^)]*)\)", text, re.M):
            names.update(n.strip("'\" ") for n in m.group(1).split())
        for m in re.finditer(r"^pkg(?:name|base)=([^\s(]+)", text, re.M):
            names.add(m.group(1).strip("'\""))
        um = re.search(r"^url=(['\"]?)([^\n'\"]*)\1", text, re.M)
        pkg_url = um.group(2) if um else ""
        bm = re.search(r"^pkgbase=([^\s(]+)", text, re.M)
        pkgbase = bm.group(1).strip("'\"") if bm else d.name
        github = extract_github_repo(text, pkg_url, pkgname=d.name, pkgbase=pkgbase)
        log = subprocess.run(
            ["git", "-C", str(PKGS_REPO), "log", "--diff-filter=A", "--format=%at", "--reverse", "--", f"pkgbuilds/{d.name}"],
            capture_output=True, text=True,
        ).stdout.split()
        added = int(log[0]) if log else 0
        for n in names:
            if n and not n.startswith("$"):
                index[n] = (d.name, added, github)
    return index


def parse_desc(text: str) -> dict:
    fields = {}
    for m in re.finditer(r"%(\w+)%\n((?:[^\n]+\n?)*)", text):
        fields[m.group(1)] = m.group(2).strip().split("\n")
    return fields


def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1000 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}".replace(".0 ", " ")
        n /= 1000
    return f"{n} GB"


def author_for(name: str, url: str, github: str, authors: dict) -> dict:
    """Resolve a public creator identity without guessing from package names."""
    override = authors.get("packages", {}).get(name)
    if override:
        return override
    for candidate in (github, url):
        parsed = urllib.parse.urlparse(candidate or "")
        if parsed.netloc.lower() not in ("github.com", "www.github.com"):
            continue
        owner = urllib.parse.unquote(parsed.path.strip("/").split("/", 1)[0])
        profile = authors.get("github_owners", {}).get(owner.lower())
        if profile:
            return profile
        if owner:
            return {"name": owner, "url": f"https://github.com/{urllib.parse.quote(owner)}"}
    return {}


def load_packages() -> list[dict]:
    raw = zstd.decompress(fetch_db())
    index = pkgbuild_index()
    categories = json.loads(CATEGORIES_FILE.read_text()) if CATEGORIES_FILE.exists() else {}
    enrichment = json.loads(ENRICHMENT_FILE.read_text()) if ENRICHMENT_FILE.exists() else {}
    indie = json.loads(INDIE_FILE.read_text()) if INDIE_FILE.exists() else {}
    authors = json.loads(AUTHORS_FILE.read_text()) if AUTHORS_FILE.exists() else {}
    pkgs = []
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        for member in tar.getmembers():
            if not member.name.endswith("/desc"):
                continue
            f = parse_desc(tar.extractfile(member).read().decode("utf-8"))
            name = f["NAME"][0]
            if name.endswith("-debug"):
                continue
            base = f.get("BASE", [name])[0]
            directory, added, github = index.get(name) or index.get(base) or (name, 0, None)
            url = f.get("URL", [""])[0]
            if url.startswith("http://www.nvidia.com"):
                url = "https://" + url.removeprefix("http://")
            if url in OMARCHY_PKGS_URLS:
                # Some PKGBUILDs default url= to the packaging repo itself when
                # the underlying project genuinely has no homepage of its own —
                # that's not "their site", so don't present it as one.
                url = ""
            if github == url:
                github = None  # nothing to add — the project's site already is its GitHub repo
            prof = enrichment.get(name, {})
            author = author_for(name, url, github or "", authors)
            pkgs.append({
                "name": name,
                "dir": directory,
                "version": f["VERSION"][0],
                "desc": f.get("DESC", [""])[0],
                "url": url,
                "github": github or "",
                "license": ", ".join(f.get("LICENSE", ["unknown"])),
                "csize": human_size(int(f["CSIZE"][0])),
                "isize": human_size(int(f["ISIZE"][0])),
                "built": int(f["BUILDDATE"][0]),
                "added": added,
                "deps": [re.split(r"[<>=]", d)[0] for d in f.get("DEPENDS", [])],
                "category": categories.get(name, FALLBACK_CATEGORY),
                "tagline": prof.get("tagline", ""),
                "full_desc": prof.get("description", ""),
                "pricing": prof.get("pricing", ""),
                "pricing_note": prof.get("pricing_note", ""),
                "requirements": prof.get("requirements", []),
                "screenshot_url": prof.get("screenshot_url", ""),
                "readme_screenshots": prof.get("readme_screenshots", []),
                "youtube_id": prof.get("youtube_id", ""),
                "youtube_title": prof.get("youtube_title", ""),
                "indie_note": indie.get(name, ""),
                "author_name": author.get("name", ""),
                "author_url": author.get("url", ""),
            })
    pkgs.sort(key=lambda p: p["name"])
    return pkgs


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def json_script(value: object) -> str:
    """Serialize JSON-LD without allowing a value to close its script tag."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def description_for(p: dict, limit: int = 158) -> str:
    text = re.sub(r"\s+", " ", p.get("full_desc") or p.get("desc") or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit - 1].rsplit(" ", 1)[0] + "…"


def claim_url(name: str) -> str:
    message = (
        f"Hi! I'd like to claim the {name} listing on the Unofficial Omarchy App Store.\n\n"
        "I can provide:\n- a correction or edit\n- screenshots of the app\n- a demo video\n\n"
        "Project URL: \nMy role with the app: "
    )
    return "https://x.com/messages/compose?" + urllib.parse.urlencode({
        "recipient_id": X_DM_RECIPIENT_ID,
        "text": message,
    })


def profile_images(p: dict) -> list[dict]:
    """Return at most four unique remote images for a profile.

    Curated media remains first. README media is a fallback only when the
    profile has no demo video, as requested; all URLs continue to point at the
    upstream host rather than being copied into this site.
    """
    images = []
    if p.get("screenshot_url"):
        images.append({
            "url": p["screenshot_url"],
            "source_url": p.get("github") or p.get("url") or "",
            "alt": f"{p['name']} app screenshot",
        })
    if not p.get("youtube_id"):
        images.extend(p.get("readme_screenshots") or [])
    unique = []
    seen = set()
    for image in images:
        url = image.get("url", "") if isinstance(image, dict) else ""
        if not url or url in seen:
            continue
        seen.add(url)
        unique.append(image)
    return unique[:4]


def card(p: dict, featured: bool = False) -> str:
    e = {k: html.escape(str(v)) for k, v in p.items() if isinstance(v, str)}
    built = datetime.date.fromtimestamp(p["built"]).isoformat()
    added_date = datetime.date.fromtimestamp(p["added"]) if p["added"] else None
    added = added_date.isoformat() if added_date else ""
    deps = html.escape(json.dumps(p["deps"]))
    reqs = html.escape(json.dumps(p["requirements"]))
    gallery = html.escape(json.dumps(profile_images(p)), quote=True)
    cat_slug = slug(p["category"])
    cls = f"card cat-{cat_slug} featured" if featured else f"card cat-{cat_slug}"
    if p.get("indie_note"):
        cls += " indie-app"
    footer = (
        f'<span class="card-facts"><span class="added">added {added_date.strftime("%b")} {added_date.day}</span><span class="size">{e["csize"]}</span></span>'
        if featured else
        f'<span class="card-facts"><span class="cat-dot" aria-hidden="true"></span><span class="size">{e["csize"]}</span></span>'
    )
    detail_url = f"apps/{slug(p['name'])}.html"
    share_url = f"{SITE_URL}/{detail_url}"
    indie_sticker = (f'<span class="indie-sticker card-sticker" title="{e["indie_note"]}">Indie app</span>'
                      if p.get("indie_note") else "")
    indie_line = f"  {indie_sticker}\n" if indie_sticker else ""
    byline = (f'<p class="byline">by <a href="{e["author_url"]}" target="_blank" '
              f'rel="author noopener">{e["author_name"]}</a></p>'
              if p.get("author_name") and p.get("author_url") else "")
    vote_button = (f'<button class="app-vote" type="button" data-vote-app="{e["name"]}" aria-pressed="false" '
                   f'aria-label="Upvote {e["name"]}"><span aria-hidden="true">▲</span> '
                   f'<span data-vote-count>0</span></button>')
    share_link = (f'<a class="app-share" href="{share_url}" data-share-app="{e["name"]}" '
                  f'data-share-title="{e["name"]} for Omarchy" data-share-url="{share_url}" '
                  f'aria-label="Share {e["name"]}">share</a>')
    return f"""<article class="{cls}" data-detail-url="{detail_url}"
  data-name="{e['name']}" data-dir="{e['dir']}" data-version="{e['version']}" data-desc="{e['desc']}"
  data-url="{e['url']}" data-github="{e['github']}" data-license="{e['license']}" data-csize="{e['csize']}" data-isize="{e['isize']}"
  data-built="{built}" data-built-ts="{p['built']}" data-added="{added}" data-added-ts="{p['added']}"
  data-deps="{deps}" data-category="{e['category']}" data-cat="{cat_slug}"
  data-tagline="{e['tagline']}" data-full-desc="{e['full_desc']}" data-pricing="{e['pricing']}"
  data-pricing-note="{e['pricing_note']}" data-reqs="{reqs}" data-gallery="{gallery}"
  data-indie-note="{e['indie_note']}"
  data-yt="{e['youtube_id']}" data-yt-title="{e['youtube_title']}">
  <header><h3><a href="{detail_url}">{e['name']}</a></h3><span class="ver">{e['version']}</span></header>
{indie_line}  {byline}
  <p class="card-description">{e['desc'] or '<em>No description provided.</em>'}</p>
  <footer>{footer}<span class="card-actions">{share_link}{vote_button}</span></footer>
</article>"""


GROUP_PREVIEW = 6  # cards shown per category until the reader asks for the rest


def nav_html(current_href: str) -> str:
    """The shared top bar, read from body.html so every page has one source."""
    body = (ROOT / "parts" / "body.html").read_text(encoding="utf-8")
    start = body.index('<header class="topbar">')
    bar = body[start:body.index("</header>", start) + len("</header>")].replace(' aria-current="page"', "")
    return bar.replace(f'href="{current_href}"', f'href="{current_href}" aria-current="page"', 1)


def group_section(category: str, pkgs: list[dict]) -> str:
    cat_slug = slug(category)
    cards = "\n".join(card(p) for p in pkgs)
    collapsed = len(pkgs) > GROUP_PREVIEW
    more = (f'  <button class="button ghost group-more" type="button" data-group-more aria-expanded="false">'
            f'Show all {len(pkgs)} {html.escape(category)} apps</button>\n') if collapsed else ""
    return f"""<section class="group cat-{cat_slug}{' collapsed' if collapsed else ''}" data-cat="{cat_slug}" data-preview="{GROUP_PREVIEW}">
  <h2><span class="dot" aria-hidden="true"></span>{html.escape(category)} <b>{len(pkgs)}</b></h2>
  <div class="grid">
{cards}
  </div>
{more}</section>"""


def leaderboard_row(p: dict) -> str:
    """Render one rankable app. Live vote totals and ordering are applied in
    the browser from the same persistent vote service used by the catalogue."""
    name = html.escape(p["name"])
    description = html.escape(p.get("desc") or "No description provided.")
    category = html.escape(p["category"])
    author = ""
    if p.get("author_name") and p.get("author_url"):
        author = (f'<span class="leader-author">by <a href="{html.escape(p["author_url"])}" '
                  f'target="_blank" rel="author noopener">{html.escape(p["author_name"])}</a></span>')
    indie = ('<span class="indie-sticker">Indie app</span>' if p.get("indie_note") else "")
    return f"""<article class="leader-row cat-{slug(p['category'])}" data-leader-app="{name}">
  <span class="leader-rank" data-leader-rank aria-label="Rank">—</span>
  <div class="leader-copy">
    <h2><a href="apps/{slug(p['name'])}.html">{name}</a></h2>
    <p>{description}</p>
    <div class="leader-meta"><span class="leader-category"><span class="dot" aria-hidden="true"></span>{category}</span>{author}{indie}</div>
  </div>
  <button class="button ghost app-vote leader-vote" type="button" data-vote-app="{name}" aria-pressed="false" aria-label="Upvote {name}"><span aria-hidden="true">▲</span> <span data-vote-count>0</span></button>
</article>"""



def fill_package_watch(guide, body, pkgs):
    """Guides for apps not yet in the Omarchy repo carry __PKG_CTA__ and __PKG_NOTE__
    markers. Once any of the watched package names appears in the catalogue, the
    twice-daily rebuild links the guide to that package page without a manual edit."""
    watch = guide.get("package_watch")
    if not watch:
        return body
    found = next((p for p in pkgs if p["name"] in watch["names"]), None)
    if found:
        name = found["name"]
        cta = (f'<div><h2>Open the {html.escape(watch["app"])} package</h2><p>It is in the official Omarchy repo now. '
               f'See the live version, requirements, source and exact install command.</p></div>'
               f'<a class="button" href="/apps/{slug(name)}.html">View {html.escape(watch["app"])} →</a>')
        note = (f'<p><strong>Update:</strong> {html.escape(watch["app"])} landed in the official Omarchy package repo as '
                f'<code>{html.escape(name)}</code>. <code>omarchy pkg add {html.escape(name)}</code> now works and is the '
                f'better route, since it updates with everything else. See the <a href="/apps/{slug(name)}.html">package page</a>. '
                f'The notes below about the missing package are kept for people on older installs.</p>')
    else:
        cta = watch["fallback_cta"]
        note = ""
    return body.replace("__PKG_CTA__", cta).replace("__PKG_NOTE__", note)

def render_app_page(template: str, css: str, p: dict, synced: str, app_banners: dict | None = None) -> str:
    canonical = f"{SITE_URL}/apps/{slug(p['name'])}.html"
    desc = description_for(p)
    project_url = p.get("url") or p.get("github") or f"https://github.com/omacom/omarchy-pkgs/tree/master/pkgbuilds/{urllib.parse.quote(p['dir'])}"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareApplication",
                "@id": canonical + "#app",
                "name": p["name"],
                "description": p.get("full_desc") or p.get("desc") or "Omarchy package",
                "applicationCategory": p["category"],
                "operatingSystem": "Omarchy Linux",
                "softwareVersion": p["version"],
                "license": p["license"],
                "url": canonical,
                "sameAs": project_url,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": SITE_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": p["name"], "item": canonical},
                ],
            },
        ],
    }
    images = profile_images(p)
    if images:
        schema["@graph"][0]["screenshot"] = [image["url"] for image in images]
    if p.get("pricing") in ("free", "free-libre"):
        schema["@graph"][0]["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    reqs = "".join(f"<li>{html.escape(str(r))}</li>" for r in p.get("requirements", []))
    links = []
    if p.get("url"):
        links.append(f'<a class="button ghost" href="{html.escape(p["url"])}" target="_blank" rel="noopener">Project site ↗</a>')
    if p.get("github"):
        links.append(f'<a class="button ghost" href="{html.escape(p["github"])}" target="_blank" rel="noopener">GitHub ↗</a>')
    links.append(f'<a class="button ghost" href="https://github.com/omacom/omarchy-pkgs/tree/master/pkgbuilds/{urllib.parse.quote(p["dir"])}" target="_blank" rel="noopener">PKGBUILD ↗</a>')
    gallery = ""
    if images:
        tiles = "".join(
            f'<a class="shot-wrap" href="{html.escape(image["url"])}" target="_blank" rel="noopener" '
            f'aria-label="Open full-size {html.escape(image.get("alt") or p["name"] + " screenshot")}">'
            f'<img src="{html.escape(image["url"])}" alt="{html.escape(image.get("alt") or p["name"] + " screenshot")}" '
            f'loading="lazy" decoding="async" referrerpolicy="no-referrer"></a>'
            for image in images
        )
        source_url = next((image.get("source_url") for image in images if image.get("source_url")), "")
        source = (f'<p class="media-source">Loaded from the upstream project · '
                  f'<a href="{html.escape(source_url)}" target="_blank" rel="noopener">View upstream source ↗</a></p>'
                  if source_url else '<p class="media-source">Loaded directly from the upstream project.</p>')
        gallery = f'<section class="project-media"><h2>Project screenshots</h2><div class="shot-gallery">{tiles}</div>{source}</section>'
    video = (f'<p><a class="button ghost" href="https://www.youtube.com/watch?v={html.escape(p["youtube_id"])}" target="_blank" rel="noopener">Watch: {html.escape(p["youtube_title"] or p["name"] + " demo")} ↗</a></p>' if p.get("youtube_id") else "")
    pricing = p.get("pricing_note") or p.get("pricing") or "Check the project site for current pricing."
    indie_sticker = (f'<span class="indie-sticker" title="{html.escape(p["indie_note"])}">Indie app</span>'
                      if p.get("indie_note") else "")
    author = (f'by <a href="{html.escape(p["author_url"])}" target="_blank" '
              f'rel="author noopener">{html.escape(p["author_name"])}</a>'
              if p.get("author_name") and p.get("author_url") else "")
    replacements = {
        "__STYLE__": css,
        "__SITE_URL__": SITE_URL,
        "__CANONICAL__": canonical,
        "__SHARE_URL__": canonical,
        "__NAME__": html.escape(p["name"]),
        "__VERSION__": html.escape(p["version"]),
        "__CATEGORY__": html.escape(p["category"]),
        "__DESCRIPTION__": html.escape(desc),
        "__FULL_DESCRIPTION__": html.escape(p.get("full_desc") or p.get("desc") or "No description provided."),
        "__INSTALL_COMMAND__": html.escape("omarchy pkg add " + p["name"]),
        "__LICENSE__": html.escape(p["license"]),
        "__DOWNLOAD_SIZE__": html.escape(p["csize"]),
        "__INSTALLED_SIZE__": html.escape(p["isize"]),
        "__PRICING__": html.escape(pricing),
        "__INDIE_STICKER__": indie_sticker,
        "__AUTHOR__": author,
        "__REQUIREMENTS__": reqs or "<li>No special requirements documented.</li>",
        "__SCREENSHOT__": gallery,
        "__APP_BANNER__": ads.render_app_banner(app_banners or {}, slug(p["name"])),
        "__VIDEO__": video,
        "__LINKS__": "".join(links),
        "__CLAIM_URL__": html.escape(claim_url(p["name"])),
        "__STRUCTURED_DATA__": json_script(schema),
        "__SYNCED__": synced,
    }
    page = template
    for key, value in replacements.items():
        page = page.replace(key, value)
    return page


def main() -> None:
    sync_pkgbuilds()
    pkgs = load_packages()
    missing_authors = [p["name"] for p in pkgs if not p.get("author_name") or not p.get("author_url")]
    if missing_authors:
        print("missing public author attribution for: " + ", ".join(missing_authors))
    synced = datetime.date.today().isoformat()
    functions_dir = ROOT / "src"
    functions_dir.mkdir(parents=True, exist_ok=True)
    (functions_dir / "app-names.mjs").write_text(
        "export default " + json.dumps([p["name"] for p in pkgs], ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )

    newest = sorted((p for p in pkgs if p["added"]), key=lambda p: (-p["added"], p["name"]))[:NEW_ARRIVALS]
    newest_names = {p["name"] for p in newest}

    # Arrivals get their own featured card up top; skip them in the catalogue
    # below so nobody sees the same package twice on one page.
    by_cat: dict[str, list[dict]] = {c: [] for c in CATEGORY_ORDER}
    for p in pkgs:
        if p["name"] in newest_names:
            continue
        by_cat.setdefault(p["category"], []).append(p)
    groups = "\n".join(group_section(c, by_cat[c]) for c in CATEGORY_ORDER if by_cat.get(c))

    chips = "\n".join(
        f'<button class="chip cat-{slug(c)}" type="button" data-cat="{slug(c)}" aria-pressed="false">'
        f'<span class="dot" aria-hidden="true"></span>{html.escape(c)} <b>{len(by_cat.get(c, []))}</b></button>'
        for c in CATEGORY_ORDER if by_cat.get(c)
    )
    legend = " · ".join(
        f'<span class="cat-{slug(c)}"><span class="dot" aria-hidden="true"></span>{html.escape(c)}</span>'
        for c in CATEGORY_ORDER if by_cat.get(c)
    )
    cat_vars = "\n".join(f".cat-{slug(c)} {{ --cat: #{h}; }}" for c, h in CATEGORY_COLOR.items())

    body = (ROOT / "parts" / "body.html").read_text(encoding="utf-8")
    css = (ROOT / "parts" / "style.css").read_text(encoding="utf-8")
    faq_html = "\n".join(
        f"    <details><summary>{html.escape(question)}</summary><p>{html.escape(answer)}</p></details>"
        for question, answer in FAQ
    )
    homepage_schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": SITE_NAME, "alternateName": "Omarchy Apps", "description": "Searchable community directory of packages in the official Omarchy repository."},
            {"@type": "CollectionPage", "@id": SITE_URL + "/#webpage", "url": SITE_URL + "/", "name": SITE_NAME, "isPartOf": {"@id": SITE_URL + "/#website"}, "mainEntity": {"@type": "ItemList", "numberOfItems": len(pkgs), "itemListElement": [
                {"@type": "ListItem", "position": i, "url": f"{SITE_URL}/apps/{slug(p['name'])}.html", "name": p["name"]}
                for i, p in enumerate(pkgs, 1)
            ]}},
            {"@type": "FAQPage", "@id": SITE_URL + "/#faq", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in FAQ
            ]},
        ],
    }
    sponsor = ads.load()
    ad_slots = ads.render_homepage(sponsor)
    app_banners = ads.active_banners((sponsor.get("app_banners") or {}).get("banners") or {})
    guide_results = "\n".join(
        f'<a href="/{g["slug"]}.html" hidden data-hay="{html.escape(" ".join([g["title"], g["description"], g["eyebrow"], g["slug"].replace("-", " "), " ".join(g.get("search_terms", []))]))}">'
        f'<strong>{html.escape(g["title"])}</strong><span>{html.escape(g["eyebrow"])}</span></a>'
        for g in GUIDES
    )
    page = (body
            .replace("__AD_HEADER__", ad_slots["__AD_HEADER__"])
            .replace("__AD_FOOTER__", ad_slots["__AD_FOOTER__"])
            .replace("__AD_LIFETIME__", ad_slots["__AD_LIFETIME__"])
            .replace("__NEW__", "\n".join(card(p, featured=True) for p in newest))
            .replace("__TICKER__", html.escape(("Just landed: " + ", ".join(p["name"] for p in newest[:3])) if newest else f"{len(pkgs)} packages, synced {synced}"))
            .replace("__GROUPS__", groups)
            .replace("__GUIDE_RESULTS__", guide_results)
            .replace("__CHIPS__", chips)
            .replace("__LEGEND__", legend)
            .replace("__COUNT__", str(len(pkgs)))
            .replace("__CATCOUNT__", str(len(CATEGORY_ORDER)))
            .replace("__NEWCOUNT__", str(len(newest)))
            .replace("__SYNCED__", synced)
            .replace("__SITE_URL__", SITE_URL)
            .replace("__FAQ__", faq_html)
            .replace("__STRUCTURED_DATA__", json_script(homepage_schema))
            .replace("__CONTACT__", html.escape(CONTACT_URL))
            .replace("__SUGGEST_APP_URL__", html.escape(SUGGEST_APP_URL))
            .replace("__X_DM_RECIPIENT__", X_DM_RECIPIENT_ID)
            .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
    DIST.mkdir(exist_ok=True)
    (DIST / "index.html").write_text(page, encoding="utf-8")
    leaderboard_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Top Omarchy Apps — Community Leaderboard",
        "description": "Live community ranking of apps in the official Omarchy package repository, ordered by votes on the Unofficial Omarchy App Store.",
        "url": SITE_URL + "/leaderboard.html",
        "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": SITE_URL + "/"},
    }
    leaderboard = ((ROOT / "parts" / "leaderboard.html").read_text(encoding="utf-8")
                   .replace("__COUNT__", str(len(pkgs)))
                   .replace("__LEADER_ROWS__", "\n".join(leaderboard_row(p) for p in pkgs))
                   .replace("__STRUCTURED_DATA__", json_script(leaderboard_schema))
                   .replace("__SYNCED__", synced)
                   .replace("__SITE_URL__", SITE_URL)
                   .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
    (DIST / "leaderboard.html").write_text(leaderboard, encoding="utf-8")
    develop = ((ROOT / "parts" / "develop.html").read_text(encoding="utf-8")
               .replace("__SYNCED__", synced)
               .replace("__SITE_URL__", SITE_URL)
               .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
    (DIST / "develop.html").write_text(develop, encoding="utf-8")
    # The checklist is emailed to newsletter subscribers, not published as a file.
    develop_md = ((ROOT / "resources" / "develop-for-omarchy.md").read_text(encoding="utf-8")
                  .replace("__SYNCED__", synced))
    (functions_dir / "checklist.mjs").write_text(
        "export default " + json.dumps(develop_md, ensure_ascii=False) + ";\n", encoding="utf-8")
    terms = ((ROOT / "parts" / "terms.html").read_text(encoding="utf-8")
             .replace("__SYNCED__", synced)
             .replace("__SITE_URL__", SITE_URL)
             .replace("__CONTACT__", html.escape(CONTACT_URL))
             .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
    (DIST / "terms.html").write_text(terms, encoding="utf-8")
    fonts = DIST / "fonts"
    fonts.mkdir(exist_ok=True)
    for f in (ROOT / "assets" / "fonts").glob("*.woff2"):
        (fonts / f.name).write_bytes(f.read_bytes())
    images = DIST / "images"
    images.mkdir(exist_ok=True)
    for f in (ROOT / "assets" / "images").glob("*"):
        if f.is_file():
            (images / f.name).write_bytes(f.read_bytes())
    (DIST / "favicon.ico").write_bytes((ROOT / "assets" / "images" / "favicon.ico").read_bytes())
    (DIST / "newsletter.js").write_text((ROOT / "assets" / "newsletter.js").read_text(encoding="utf-8"), encoding="utf-8")
    (DIST / "ads.js").write_text((ROOT / "assets" / "ads.js").read_text(encoding="utf-8"), encoding="utf-8")
    (DIST / "votes.js").write_text((ROOT / "assets" / "votes.js").read_text(encoding="utf-8"), encoding="utf-8")
    (DIST / "home-leaders.js").write_text((ROOT / "assets" / "home-leaders.js").read_text(encoding="utf-8"), encoding="utf-8")
    (DIST / "hero-field.js").write_text((ROOT / "assets" / "hero-field.js").read_text(encoding="utf-8"), encoding="utf-8")
    (DIST / "leaderboard.js").write_text((ROOT / "assets" / "leaderboard.js").read_text(encoding="utf-8"), encoding="utf-8")
    (DIST / "share.js").write_text((ROOT / "assets" / "share.js").read_text(encoding="utf-8"), encoding="utf-8")
    about = ((ROOT / "parts" / "about.html").read_text(encoding="utf-8")
             .replace("__SYNCED__", synced)
             .replace("__CONTACT__", html.escape(CONTACT_URL))
             .replace("__SITE_URL__", SITE_URL)
             .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
    (DIST / "about.html").write_text(about, encoding="utf-8")

    ad_faq_html = "\n".join(
        f"    <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in AD_FAQ
    )
    advertise_schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": SITE_URL + "/advertise.html", "url": SITE_URL + "/advertise.html",
             "name": "Advertise on Omarchy Apps", "isPartOf": {"@id": SITE_URL + "/#website"},
             "description": "Sponsor the Unofficial Omarchy App Store: header and footer rotations plus app profile banners. Flat monthly rates on 90-day terms, fair rotation for every sponsor.",
             "dateModified": synced},
            {"@type": "FAQPage", "@id": SITE_URL + "/advertise.html#faq", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in AD_FAQ
            ]},
        ],
    }
    advertise = ((ROOT / "parts" / "advertise.html").read_text(encoding="utf-8")
                 .replace("__AD_SLOTS__", ads.render_slot_cards(sponsor))
                 .replace("__AD_FAQ__", ad_faq_html)
                 .replace("__STRUCTURED_DATA__", json_script(advertise_schema))
                 .replace("__CONTACT_DM__", html.escape(ads.dm_url("Hi! I have a question about sponsoring omarchyapps.com.")))
                 .replace("__COUNT__", str(len(pkgs)))
                 .replace("__SYNCED__", synced)
                 .replace("__CONTACT__", html.escape(CONTACT_URL))
                 .replace("__SITE_URL__", SITE_URL)
                 .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
    (DIST / "advertise.html").write_text(advertise, encoding="utf-8")

    guide_cards = "\n".join(
        f'<a class="guide-card" href="/{g["slug"]}.html"><p class="eyebrow">{html.escape(g["eyebrow"])}</p>'
        f'<strong>{html.escape(g["title"])}</strong><span>{html.escape(g["description"])}</span></a>'
        for g in GUIDES
    )
    guides_schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Omarchy Guides",
                     "url": SITE_URL + "/guides.html", "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": SITE_URL + "/"},
                     "hasPart": [{"@type": "Article", "name": g["title"], "url": f"{SITE_URL}/{g['slug']}.html"} for g in GUIDES]}
    guides_index = ((ROOT / "parts" / "guides.html").read_text(encoding="utf-8")
                    .replace("__NAV__", nav_html("guides.html"))
                    .replace("__GUIDE_CARDS__", guide_cards)
                    .replace("__GUIDE_COUNT__", str(len(GUIDES)))
                    .replace("__STRUCTURED_DATA__", json_script(guides_schema))
                    .replace("__SYNCED__", synced)
                    .replace("__CONTACT__", html.escape(CONTACT_URL))
                    .replace("__SITE_URL__", SITE_URL)
                    .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
    (DIST / "guides.html").write_text(guides_index, encoding="utf-8")

    guide_template = (ROOT / "parts" / "guide.html").read_text(encoding="utf-8")
    for guide in GUIDES:
        guide_url = f"{SITE_URL}/{guide['slug']}.html"
        related = "\n".join(
            f'<a class="related-guide" href="/{item["slug"]}.html"><strong>{html.escape(item["title"])}</strong><span>{html.escape(item["description"])}</span></a>'
            for item in GUIDES if item["slug"] != guide["slug"]
        )
        guide_schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "@id": guide_url + "#article",
                    "headline": guide["title"],
                    "description": guide["description"],
                    "url": guide_url,
                    "dateModified": synced,
                    "author": {"@type": "Person", "name": "Jessyka", "url": SITE_URL + "/about.html"},
                    "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL + "/"},
                    "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": SITE_URL + "/"},
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
                        {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE_URL + "/#guides"},
                        {"@type": "ListItem", "position": 3, "name": guide["title"], "item": guide_url},
                    ],
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
                        for question, answer in guide["faqs"]
                    ],
                },
            ],
        }
        guide_body = (ROOT / "parts" / "guides" / f"{guide['slug']}.html").read_text(encoding="utf-8")
        guide_body = fill_package_watch(guide, guide_body, pkgs)
        guide_page = (guide_template
                      .replace("__TITLE__", html.escape(guide["title"]))
                      .replace("__DESCRIPTION__", html.escape(guide["description"]))
                      .replace("__SLUG__", guide["slug"])
                      .replace("__EYEBROW__", html.escape(guide["eyebrow"]))
                      .replace("__HEADING__", guide["heading"])
                      .replace("__TAGLINE__", html.escape(guide["tagline"]))
                      .replace("__ANSWER__", html.escape(guide["answer"]))
                      .replace("__BODY__", guide_body)
                      .replace("__RELATED_GUIDES__", related)
                      .replace("__STRUCTURED_DATA__", json_script(guide_schema))
                      .replace("__SYNCED__", synced)
                      .replace("__SITE_URL__", SITE_URL)
                      .replace("__STYLE__", css.replace("__CATVARS__", cat_vars)))
        (DIST / f"{guide['slug']}.html").write_text(guide_page, encoding="utf-8")

    apps_dir = DIST / "apps"
    apps_dir.mkdir(exist_ok=True)
    for old in apps_dir.glob("*.html"):
        old.unlink()
    app_template = (ROOT / "parts" / "app.html").read_text(encoding="utf-8")
    resolved_css = css.replace("__CATVARS__", cat_vars).replace("url(fonts/", "url(../fonts/")
    for p in pkgs:
        (apps_dir / f"{slug(p['name'])}.html").write_text(
            render_app_page(app_template, resolved_css, p, synced, app_banners), encoding="utf-8"
        )

    sitemap_urls = [SITE_URL + "/", SITE_URL + "/leaderboard.html", SITE_URL + "/develop.html", SITE_URL + "/about.html", SITE_URL + "/advertise.html", SITE_URL + "/guides.html", SITE_URL + "/terms.html"]
    sitemap_urls.extend(f"{SITE_URL}/{guide['slug']}.html" for guide in GUIDES)
    sitemap_urls.extend(f"{SITE_URL}/apps/{slug(p['name'])}.html" for p in pkgs)
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap.extend(f"  <url><loc>{url}</loc><lastmod>{synced}</lastmod></url>" for url in sitemap_urls)
    sitemap.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8"
    )
    (DIST / "_headers").write_text(
        (ROOT / "resources" / "netlify-headers").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (DIST / "llms.txt").write_text(
        f"# {SITE_NAME}\n\n"
        "> An independent directory of packages published by the official Omarchy package repository.\n\n"
        f"Canonical site: {SITE_URL}/\n\n"
        "This site is unofficial and is not affiliated with or endorsed by Omarchy, Omacom, or DHH. "
        "It does not host packages. Package facts are refreshed from pkgs.omarchy.org, and official upstream sources take precedence.\n\n"
        "## Main pages\n"
        f"- [Browse packages]({SITE_URL}/)\n"
        f"- [Top apps leaderboard]({SITE_URL}/leaderboard.html)\n"
        f"- [Develop for Omarchy]({SITE_URL}/develop.html)\n"
        f"- [About]({SITE_URL}/about.html)\n"
        f"- [Guides]({SITE_URL}/guides.html)\n"
        f"- [Advertise]({SITE_URL}/advertise.html)\n"
        f"- [Terms of Use]({SITE_URL}/terms.html)\n\n"
        "## Guides and comparisons\n"
        + "".join(f"- [{guide['title']}]({SITE_URL}/{guide['slug']}.html)\n" for guide in GUIDES)
        + "\n"
        "Contact: https://x.com/jessyka_boat\n", encoding="utf-8"
    )

    unresolved = [p["name"] for p in pkgs if not p["added"]]
    uncategorized = [p["name"] for p in pkgs if p["category"] == FALLBACK_CATEGORY and p["name"] not in json.loads(CATEGORIES_FILE.read_text() or "{}")]
    print(f"dist/index.html  {len(page):,} bytes · {len(pkgs)} packages · synced {synced}")
    print(f"dist/leaderboard.html {len(leaderboard):,} bytes · live Top 25 community ranking")
    print(f"dist/develop.html {len(develop):,} bytes · public packaging checklist")
    print(f"src/checklist.mjs {len(develop_md):,} bytes · checklist emailed to subscribers")
    print(f"dist/terms.html   {len(terms):,} bytes · terms of use")
    print(f"dist/about.html   {len(about):,} bytes · project and builder bio")
    print(f"dist/advertise.html {len(advertise):,} bytes · sponsor products (rotations + app banners)")
    print(f"dist/guides       {len(GUIDES)} search-focused editorial guides")
    print(f"dist/apps/        {len(pkgs)} crawlable package pages")
    print(f"dist/sitemap.xml  {len(sitemap_urls)} canonical URLs")
    print("new arrivals:    " + ", ".join(f"{p['name']} ({datetime.date.fromtimestamp(p['added'])})" for p in newest))
    if unresolved:
        print(f"no git history for {len(unresolved)}: {', '.join(unresolved)}")
    if not CATEGORIES_FILE.exists():
        print("categories:      data/categories.json missing — everything filed under Utilities")
    elif uncategorized:
        print(f"uncategorized (fell back to Utilities): {', '.join(uncategorized)}")


if __name__ == "__main__":
    main()
