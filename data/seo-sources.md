# SEO page sources (checked 2026-10-15 PT)

Every fact on the programmatic pages comes from `data/seo-facts.json`, which stores the source URL next to each claim. Page text is generated from that file only. Catalogue pages (categories, apps list, app pages) use the package data from pkgs.omarchy.org plus this site's own categories and enrichment files.

## Omarchy (official)
- https://omarchy.org/ : default editor Neovim, default terminal Foot, Steam/RetroArch, Windows VM.
- https://omarchy.org/manual/ : based on Arch, Hyprland, Quickshell.
- https://omarchy.org/manual/getting-started/ : ISO install, full-disk or free-space install, encryption by default, Secure Boot/TPM off.
- https://omarchy.org/manual/security/ : firewall defaults (LocalSend 53317 only, SSH off), Arch core/extra/multilib plus the Omarchy Package Repository, optional AUR.
- https://omarchy.org/manual/updates/ : rolling, stable channel one month behind on the Arch mirror.
- https://omarchy.org/manual/system-snapshots/ : snapshot on every Omarchy update, Limine.
- https://omarchy.org/manual/other-packages/ : `omarchy pkg add`.
- https://omarchy.org/manual/gaming/ : Steam, Lutris, Battle.net, Heroic install routes.
- https://omarchy.org/manual/development-tools/ : Docker (sudo by default, Sudoless Docker option), Install > Editor (Zed and others).
- https://omarchy.org/manual/commercial-apps-services/ : Tailscale, Bitwarden (Install > Service).
- https://omarchy.org/manual/browsers/ : Install > Browser, Setup > Defaults > Browser, `omarchy default browser firefox`.
- https://omarchy.org/manual/web-apps/ : Zoom and Discord preinstalled web apps, Remove > Web App.

## Other distros (official sites only)
- Ubuntu: https://ubuntu.com/about/release-cycle (six-month releases, LTS every two years with 5 years of standard security maintenance, deb plus snap), https://ubuntu.com/desktop (Ubuntu Pro free on up to 5 machines).
- CachyOS: https://cachyos.org/ (Arch base, rolling, x86-64-v3/v4/Zen4 with LTO, PGO/BOLT, linux-cachyos schedulers, Calamares and CLI installers, 17+ desktops).
- Arch Linux: https://archlinux.org/ (pacman, x86-64 repos, community repo/AUR), https://wiki.archlinux.org/title/Arch_Linux (independent, rolling, general purpose).
- Fedora: https://fedoraproject.org/workstation/ (GNOME Workstation, KDE Plasma edition, Atomic Silverblue/Kinoite, Koji builds RPMs).
- Linux Mint: https://linuxmint.com/about.php (Debian and Ubuntu base, about 30,000 packages, conservative updates, Cinnamon/MATE/Xfce, LTS-only since 2014).
- Pop!_OS: https://system76.com/pop/ (System76, auto-tiling, full-disk encryption, Ubuntu-compatible tools).
- Bazzite: https://bazzite.gg/ (Universal Blue, Fedora Kinoite/Silverblue, image-based rollback, Secure Boot, SELinux, LUKS, Steam and Lutris preinstalled, HDR/VRR).

## Skipped (not verifiable from official sources, or out of scope)
- Install guides for VS Code, Cursor, Spotify, Dropbox, Minecraft, Google Chrome, Brave: these are packages in the Omarchy repo, so they already have app pages.
- Install guides for Apple Music, iMessage, DaVinci Resolve, Obsidian, AppImage/Flatpak: the Omarchy manual gives no install route (Obsidian ships preinstalled, see /manual/guis/). No page.
- Fedora release cadence and default package manager name; Pop!_OS base distro and desktop name; Ubuntu default desktop: not stated on the pages fetched, so not claimed.
- Any "faster", "better" or "best" claims, benchmark numbers, and hardware requirements: not claimed.
- Display names for apps ("Aether" vs "aether"): the repo data has only package names, so titles use the real package name.
- aggregateRating from votes: votes are not ratings, so no rating schema.
