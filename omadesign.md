# Omadesign on Omarchy — How-To Guide

> **VERIFY ON OMARCHY (Jessyka's pass):**
> - [ ] There is NO `omarchy pkg add omadesign` yet. Confirm `pacman -Ss omadesign` returns nothing and that omarchy-pkgs PR #343 (`omadesign-bin` 0.0.4alpha, opened Sep 7 2026) is still unmerged and stale against upstream 0.6.3
> - [ ] `curl -fsSL https://omadesign.app/install | sh` completes, prints "omadesign 0.6.3 is installed", and `~/.local/bin/omadesign --version` works
> - [ ] Desktop entry appears in Walker (Super + Space) after install, no logout needed
> - [ ] First launch: welcome screen renders under Hyprland/Wayland in the current Omarchy theme colors and font
> - [ ] Core workflow: new Vector document, draw a rectangle (R), add text (T), export PNG and SVG; open a JPEG in Photo mode and export; About > Update shows the current version
> - [ ] Claimed issues reproduced or confirmed: (1) theme switch does not recolor an already-open window on builds before 0.6.0, (2) fcitx5 input and Ctrl+C/V on Hyprland before 0.6.2, (3) sluggish UI on a 4-core / under-8 GB box, (4) no package route, maintainer declined AUR
> - [ ] Screenshots: welcome screen in Tokyo Night; Design workspace with a gradient fill; Photo mode with a RAW open; About > Update dialog; the install command running in Ghostty

---

## Omadesign

**One-liner:** Omadesign is a free, native Linux creative suite (vector design, layout, pixel painting, RAW photo development and motion in one app) written in Rust and built to follow your Omarchy theme and font out of the box.

**TL;DR install:**
```bash
curl -fsSL https://omadesign.app/install | sh
```

That is the only supported install route as of October 2026. The script picks your architecture, downloads the 0.6.3 release tarball from GitHub, verifies its SHA-256 and unpacks into `~/.local`. Nothing touches `/usr` and no sudo is needed. Omadesign is free and MIT-licensed with no paid tier. Cloud features (shared projects, team review) need an account, but every editing feature works offline without one.

The honest caveat up front: `omarchy pkg add omadesign-bin` only works on the edge channel for now. The package was merged into the official Omarchy repo on October 11, 2026, but new packages land on the edge ring first and only reach stable when the next Omarchy release train promotes them. Until then the curl one-liner is the route for everyone on stable. Read the script first if you want; it is 62 lines, and the SHA-256 check happens before anything is extracted. Second caveat: the project moves fast (0.6.0 to 0.6.3 in one month) and this guide is written against 0.6.3.

## Getting started (5 minutes)

1. **Install.** Run the command above in a terminal. You need `curl`, `tar` and `sha256sum`, all of which Omarchy ships. It downloads about 39 MB on x86_64 (36 MB on ARM64, which covers Apple Silicon under Asahi). The last line should read "omadesign 0.6.3 is installed". If `omadesign --version` says command not found, open a new terminal; Omarchy puts `~/.local/bin` on your PATH but existing shells will not see it. To pin a version, set `OMADESIGN_TAG=v0.6.2` before the command. To install somewhere else, set `OMADESIGN_INSTALL_PREFIX`.

2. **First launch.** Hit Super + Space and type "oma", or run `omadesign`. You land on a welcome screen that scans your home directory for existing `.oma` projects (it skips hidden folders, Trash and symlinks) and offers +Vector and +Layout buttons that open the template picker. The window is already in your Omarchy palette and font. There is no light/dark toggle because it just mirrors whatever theme is active.

3. **The three things everyone needs to know.**
   - **Modes, not separate apps.** The centered buttons across the top switch between Vector, Raster, Layout, Photo, Motion and Agent, all on one document and one layer stack. Press R for rectangle, P for pen, T for type, B for brush, C for crop. F1 opens the full shortcut list and Ctrl + / toggles a shortcut overlay for the current tool.
   - **It opens and exports the files you already have.** Import covers PSD/PSB, GIMP XCF, PDF, Illustrator (PDF-compatible), OpenRaster, SVG and camera RAW (DNG, CR2/CR3, NEF, ARW, RAF). Export covers layered PSD, PDF, OpenRaster, 16-bit PNG/TIFF, JPEG, SVG, animated SVG, Lottie and responsive HTML. The limits are real and documented: PSD text and smart objects come in as flattened pixels, there is no writer for AI or XCF, and PDF export turns text into outlines. The [format guide](https://omadesign.app/docs/formats/) lists every one.
   - **Updates happen inside the app.** Omadesign > About > Update checks the release channel, downloads the new build with the same installer, snapshots your open documents and restarts with them open. There is no `pacman -Syu` path, so this menu is how you stay current.

4. **Where its config lives.**
   - Preferences: `~/.config/omadesign/`
   - Crash recovery swap files: `~/.local/share/omadesign/<id>.oma.swp`, written after about a second idle and deleted on save
   - Binary and desktop entry: `~/.local/bin/omadesign` and `~/.local/share/applications/`
   - Theme: read on launch from `~/.local/state/omarchy/current/theme/colors.toml`, falling back to `~/.config/omarchy/themes/<current>/colors.toml`, then a built-in Catppuccin
   - Font: whatever `omarchy font current` returns, then fontconfig sans-serif. Override with `OMADESIGN_FONT=/path/to/font.ttf`
   - Projects are plain folders. A folder counts as a project when it holds `.omacolors`, `.omatype` or an `.omabrand/` directory. Photo edits sit next to the original as `photo.jpg.omaphoto`.

5. **Try the terminal side.** `omadesign --inspect artwork.psd` prints a file's structure without opening the UI, and `omadesign --convert artwork.afdesign --output artwork.oma` converts between any supported pair. `omadesign --agent-docs manual` dumps the whole manual as text, which is handy to feed Claude Code when you want it to script something.

## Common issues & fixes

**Problem: `omarchy pkg add omadesign` says "target not found", and the app is missing from omarchyapps.com.**
Fix: There is no package, and that is not a mistake on your end. The developer submitted `omadesign-bin` to the official Omarchy package repo on September 7, 2026. The PR passed CI and a maintainer gave it the build-approved label, but it has not been reviewed or merged since, and it is still pinned to 0.0.4alpha while upstream is on 0.6.3. A separate request for an AUR package was closed as not planned, with the maintainer saying installation "stays the home-directory installer / release archives." So the curl one-liner is the only route, and no `pacman`, `yay` or `omarchy pkg add` command will work until that PR is rebased and merged. If you refuse to pipe to sh, download the tarball and checksum from the [GitHub releases page](https://github.com/michaelmonetized/omadesign/releases), verify with `sha256sum -c`, extract, and run the `install.sh` inside. That is exactly what the one-liner does. ([omacom/omarchy-pkgs pull #343](https://github.com/omacom/omarchy-pkgs/pull/343), [michaelmonetized/omadesign issue #73](https://github.com/michaelmonetized/omadesign/issues/73))

**Problem: You switch Omarchy themes and Omadesign keeps the old colors.**
Fix: Builds before 0.6.0 read the palette once at startup and cached it, so the window stayed stale until a restart. The maintainer shipped a file watcher in the 0.6.0 replacement bundles. Check Omadesign > About; if you are on 0.5.x, run the install one-liner again or use About > Update. On a current build, a theme switch repaints live. ([michaelmonetized/omadesign issue #133](https://github.com/michaelmonetized/omadesign/issues/133))

**Problem: Ctrl + C / Ctrl + V do nothing, and fcitx5 cannot type CJK into a text box, on Hyprland.**
Fix: Before 0.6.2 the app never activated the Wayland text-input protocol, so the input method never received keystrokes and the clipboard sat on the wrong path. Fixed in 0.6.2 (verified by the maintainer under Sway with fcitx5 and Rime, reported originally on Hyprland 0.56). Update via About > Update. Omarchy ships fcitx5 by default, so this one bit Omarchy users specifically. ([michaelmonetized/omadesign issue #83](https://github.com/michaelmonetized/omadesign/issues/83))

**Problem: Typing and brush strokes lag badly, or motion playback stutters on a bigger comp.**
Fix: Two separate things. Motion playback on complex compositions was fixed upstream at the end of September 2026, so update first. The lag is hardware. The maintainer's own benchmark ran the same build on three machines: a 4-core AMD thin client with under 6 GB RAM saw 90 ms median keystroke latency with half-second stalls, while an 8 GB Intel laptop sat at 35 ms and an M1 Pro at 21 ms. The provisional guidance is 8 GB RAM minimum, 16 GB recommended, and four cores is not enough. A dedicated GPU is not needed; AI features (background removal, upscaling) run on the CPU. ([issue #177](https://github.com/michaelmonetized/omadesign/issues/177), [issue #158 benchmark](https://github.com/michaelmonetized/omadesign/issues/158))

**Problem: Affinity files will not open.**
Fix: Affinity import goes through an optional GPL-licensed bridge that is not bundled. Run `./scripts/setup-affinity-import.sh` from a source checkout once; it needs Inkscape's Python modules plus the Python `zstandard`, `Pillow` and `numpy` packages. Even then, adjustments, live effects and edit history do not survive, and multi-spread documents can fail. ([Omadesign format guide](https://omadesign.app/docs/formats/))

## Good to know

**Pairs well with:**
- `omarchy pkg add inkscape` if you need a mature SVG editor for the pieces Omadesign still approximates (mesh gradients, complex text on import).
- `omarchy pkg add gimp` for the XCF round trip. Omadesign reads XCF but cannot write it, so export OpenRaster and open that in GIMP.
- `omarchy pkg add darktable` if you do serious RAW work. Omadesign's Photo mode covers develop, crop and presets; Darktable covers everything else.

**If you hate this, try:** Inkscape plus GIMP plus Darktable, the three separate tools Omadesign is trying to replace. All are one `omarchy pkg add` away from the Arch repos, all are mature, none follow your theme.

**CLI pro tip:** `omadesign --agent-skill` prints a ready-made skill file describing the app's CLI and document format. Drop it in `.claude/skills/` and Claude Code can batch-convert and inspect your files without you opening the UI.

## Compare it

| | Omadesign | Inkscape + GIMP | Krita |
|---|---|---|---|
| Price | Free, MIT | Free, GPL | Free, GPL |
| Best for | One app for vector, layout, photo and motion that matches your Omarchy theme; alpha-stage | Battle-tested vector and raster editing with huge plugin ecosystems | Digital painting and illustration, brush engine nobody else matches |
| Omarchy install | `curl -fsSL https://omadesign.app/install \| sh` | `omarchy pkg add inkscape gimp` | `omarchy pkg add krita` |

**One-line verdict:** Use Omadesign if you want one themed app and can live with alpha software; use Inkscape and GIMP if a format detail matters for client work; use Krita if you mostly paint.

## FAQ

**Does Omadesign work on Omarchy?**
Yes, it was built for it. The UI reads your Omarchy theme colors and font on launch and repaints when you switch themes. It runs natively on Wayland under Hyprland, on both x86_64 and Apple Silicon via Asahi. Expect a 4-core or sub-8 GB machine to feel slow.

**Is it free?**
Completely, under the MIT license. No trial, no paid tier, no account for local work. The cloud sharing features need a sign-in but there is no published pricing for them.

**Why isn't it in the Omarchy app store?**
Because it is not in the Omarchy package repo. The maintainer distributes only through the home-directory installer and declined an AUR package. A community PR to omarchy-pkgs exists but is stale. Until a package lands, omarchyapps.com has no profile page for it and `omarchy pkg add omadesign` will fail.

**Omadesign vs Inkscape, which should I pick?**
Inkscape if you need a specific SVG feature or you ship files to people on other tools; it is the safer bet for anything client-facing. Omadesign if you want raster, photo and motion in the same window and prefer a native GUI over GTK3. Many people will keep both installed.

**How do I update it?**
Omadesign > About > Update, which reruns the official installer and restarts with your documents open. Rerunning the curl one-liner does the same thing from a terminal. There is no pacman path.

**My theme change didn't apply. Is that a bug?**
Only on builds before 0.6.0. Check About for the version and update. If you are on 0.6.x and it still does not repaint, confirm that `~/.local/state/omarchy/current/theme/colors.toml` exists, since that is the file it watches.
