# Ghostty on Omarchy — How-To Guide

> **VERIFY ON OMARCHY (Jessyka's pass):**
> - [ ] `omarchy pkg add ghostty` installs clean (package is `ghostty` 1.3.1-3 from pkgs.omarchy.org, split into `ghostty`, `ghostty-shell-integration`, `ghostty-terminfo`, `ghostty-nautilus`)
> - [ ] `omarchy default terminal ghostty` (or Setup > Defaults > Terminal) installs it if missing, copies the stock config to `~/.config/ghostty/config`, and writes `~/.config/xdg-terminals.list` so Super + Return opens Ghostty
> - [ ] First launch: window opens under Hyprland/Wayland with the current Omarchy theme colors and JetBrainsMono Nerd Font; no GTK header bar
> - [ ] Core workflow: open a tab (Ctrl + Shift + T), split below (Ctrl + Shift + E) and beside (Ctrl + Shift + O), move between splits (Ctrl + Alt + Arrows), reload config (Ctrl + Shift + ,)
> - [ ] Theme switch (Super + Ctrl + Shift + Space) recolors an open Ghostty window without a restart; font change (Style > Font) needs a restart as the manual warns
> - [ ] Claimed issues reproduced or confirmed: (1) `xterm-ghostty` unknown on a stock Debian/Ubuntu SSH host, (2) middle-click paste dead until `gtk-enable-primary-paste` is set, (3) Hyprland `exec, ghostty` keybind vs D-Bus activation on 1.3.1, (4) `--title nvim` ignored but `--title=nvim` works, (5) no OpenGL context on pre-GCN Radeon
> - [ ] Screenshots: fresh Ghostty under the default theme; a 2x2 split with a tab bar; `~/.config/ghostty/config` in nvim; the SSH terminfo error text; Setup > Defaults > Terminal menu

---

## Ghostty

**One-liner:** Ghostty is a GPU-rendered terminal with native tabs and splits, built by Mitchell Hashimoto (the HashiCorp founder), and it is the only terminal Omarchy ships a config for that gives you tabs and splits without tmux.

**TL;DR install:**
```bash
omarchy pkg add ghostty
```

That pulls the `ghostty` package from the Omarchy repo (an 18 MB download, built from the upstream 1.3.1 source with Zig 0.15.2) plus its terminfo and shell-integration subpackages. It does not make Ghostty your default terminal or copy Omarchy's tuned config. For that, run `omarchy default terminal ghostty` instead, or pick it from the Omarchy menu under Setup > Defaults > Terminal. Ghostty is free and MIT-licensed. There is no paid tier, no account, no telemetry.

One thing to know first: which terminal Omarchy ships by default has changed three times. Omarchy 3.0 shipped Alacritty, 3.2 switched to Ghostty, and 4.0 switched again to Foot. If you installed recently and Super + Return opens something without tabs, that is Foot, and this guide is how to swap it.

Profile page: [omarchyapps.com/apps/ghostty.html](https://omarchyapps.com/apps/ghostty.html)

## Getting started (5 minutes)

1. **Install and make it the default.** Run `omarchy default terminal ghostty` in whatever terminal you have. If Ghostty is missing, Omarchy opens a floating window, installs the package with sudo, copies its stock config to `~/.config/ghostty/`, and writes `com.mitchellh.ghostty.desktop` as the first line of `~/.config/xdg-terminals.list`. That file is what Super + Return reads, so the binding now opens Ghostty. You get a notification saying "Ghostty is now the default terminal." If you prefer the menu, it is Super + Alt + Space, then Setup > Defaults > Terminal.

2. **First launch.** Press Super + Return. You should see a plain window, no title bar, 14 px of padding, JetBrainsMono Nerd Font at 9 pt, and the colors of whatever Omarchy theme is active. There is no welcome screen. If you get a tiny or blank window instead, jump to the GPU issue below.

3. **The three things everyone needs to know.**
   - **Tabs and splits are built in.** Ctrl + Shift + T opens a tab, Ctrl + Shift + E splits below, Ctrl + Shift + O splits beside. Ctrl + Alt + Arrows moves between splits, Ctrl + Shift + Arrows moves between tabs, Alt + 1 through 9 jumps to a tab, and Ctrl + Shift + Enter zooms the current split to fill the window. Ctrl + Shift + W closes whichever one you are in.
   - **Config reloads live.** Ctrl + Shift + , reloads the config in place. Ctrl + , opens it in your editor. Most keys apply immediately, a few only apply to new tabs, and font changes need a full restart.
   - **The command palette.** Ctrl + Shift + P opens a VS Code style palette listing every action Ghostty can do. It is the fastest way to learn what else is bound.

4. **Where the config lives.** Ghostty reads `~/.config/ghostty/config`, a plain `key = value` file with `#` comments. Omarchy's copy is short and worth reading. The first line is `config-file = ?"~/.local/state/omarchy/current/theme/ghostty.conf"`, which pulls in a palette Omarchy regenerates from the active theme's `colors.toml` every time you switch themes. That is why theme changes recolor Ghostty instantly: Omarchy sends `SIGUSR2` to every running Ghostty process, which is its reload signal. Everything else in the file is yours to edit: font, padding, cursor, keybinds. The one line not to touch is `async-backend = epoll`, explained in the issues section.

5. **Check the Omarchy-specific keys.** Omarchy adds a few bindings on top of Ghostty's defaults. Shift + Enter and Alt + Shift + Enter are sent as CSI-u sequences so Claude Code, opencode, and tmux can tell them apart from Enter. Shift + Insert pastes and Ctrl + Insert copies. Super + Ctrl + Shift + Arrows resizes a split by 10 lines, add Alt for 100. The full list is in the Omarchy manual under Hotkeys > Ghostty Terminal.

## Common issues & fixes

**Problem: SSH into a server and you get "missing or unsuitable terminal: xterm-ghostty", or Backspace and arrow keys misbehave in `htop` or `vim`.**
Fix: Ghostty sets `TERM=xterm-ghostty`, and most servers have no terminfo entry by that name (newer ncurses ships one, but under `ghostty`, not `xterm-ghostty`). Omarchy's config already turns on `ssh-env`, which forwards `COLORTERM` and friends, but not the terminfo install. Three options, pick one:

```bash
# One session only
TERM=xterm-256color ssh user@host

# Permanent, per host, no root needed on the server
infocmp -x xterm-ghostty | ssh user@host -- tic -x -

# Permanent, every host, in ~/.ssh/config (needs OpenSSH 8.7 or newer)
Host *
  SetEnv TERM=xterm-256color
```

The `infocmp | tic` route keeps full Ghostty features like colored underlines. The `SetEnv` route is simplest but downgrades you on every host. There is also a built-in `ssh-terminfo` feature: change Omarchy's line to `shell-integration-features = no-cursor,ssh-env,ssh-terminfo` and Ghostty installs its terminfo on first connect and caches the result per host. It only works for `ssh` typed in an interactive shell, not from `scp`, `rsync`, `git`, scripts, or tools that call ssh themselves, and the remote needs `tic` installed. ([Ghostty docs: terminfo](https://ghostty.org/docs/help/terminfo), [Ghostty docs: SSH](https://ghostty.org/docs/features/ssh))

**Problem: Middle-click paste does nothing on Hyprland, even though selecting text works and Firefox pastes fine.**
Fix: Ghostty 1.3.0 started honoring the GTK setting `gtk-enable-primary-paste`, which defaults to off in current `gsettings-desktop-schemas`. Turn it on and restart Ghostty:

```bash
gsettings set org.gnome.desktop.interface gtk-enable-primary-paste true
```

Some people needed a full logout before it stuck. Check with `gsettings get org.gnome.desktop.interface gtk-enable-primary-paste`. Reported on Ghostty 1.3.1 under Hyprland, Niri, KDE and Sway. ([ghostty-org/ghostty discussion #12181](https://github.com/ghostty-org/ghostty/discussions/12181))

**Problem: A custom Hyprland keybind with `exec, ghostty` does nothing, but Ghostty opens fine from the launcher and from Super + Return.**
Fix: Since the 1.1.x tip builds, Ghostty registers a D-Bus service and a systemd user unit, and the bare binary launched from a compositor keybind can fail to spawn a window. Omarchy sidesteps this because Super + Return goes through `xdg-terminal-exec`, which uses the desktop entry. For your own bindings in `~/.config/hypr/bindings.lua`, either launch the same way Omarchy does with `omarchy-launch-terminal`, or activate the service directly:

```bash
gdbus call --session --dest com.mitchellh.ghostty --object-path /com/mitchellh/ghostty --method org.gtk.Actions.Activate new-window [] []
```

`ghostty --launched-from=desktop` also worked for the reporter. The D-Bus route cannot pass a command to run inside the new window, so `ghostty -e yazi` style bindings still need the binary. ([ghostty-org/ghostty discussion #7708](https://github.com/ghostty-org/ghostty/discussions/7708))

**Problem: `ghostty --title nvim -e nvim` logs "title: value required" and your Hyprland window rule never matches.**
Fix: Ghostty flags need an equals sign, unlike Kitty and Alacritty. Use `ghostty --title=nvim -e nvim`. Match it in Hyprland with `class:^(com.mitchellh.ghostty)$` plus `title:^(nvim)$`. You cannot set an arbitrary `--class` because GTK enforces application ID rules, so match on title. ([ghostty-org/ghostty discussion #8509](https://github.com/ghostty-org/ghostty/discussions/8509))

**Problem: Ghostty crashes on launch or shows a blank window on an older machine (ATI Radeon HD 5xxx, Lenovo X230 era Intel, some dual-GPU laptops).**
Fix: Ghostty needs a working OpenGL context and some legacy GPUs cannot provide one. Omarchy already handles the pre-GCN Radeon case: when it detects the `radeon` kernel driver at install time it swaps in Alacritty as the default terminal (merged January 2026). If you hit this on other hardware, the manual fix is one command:

```bash
omarchy default terminal alacritty
```

Launch `ghostty` from another terminal first and read the error. "Unable to acquire an OpenGL context" confirms it. ([basecamp/omarchy pull #3711](https://github.com/basecamp/omarchy/pull/3711), [basecamp/omarchy issue #4062](https://github.com/basecamp/omarchy/issues/4062))

**Problem: Ghostty feels sluggish, tabs stall, or `btop` shows high iowait with no disk activity.**
Fix: Already fixed in Omarchy's config via `async-backend = epoll`. Ghostty's default io_uring backend caused iowait spikes and window freezes on Hyprland for several users across 1.0.x and 1.1.x. If you wrote your own config from scratch and skipped that line, add it back and restart. ([ghostty-org/ghostty discussion #3224](https://github.com/ghostty-org/ghostty/discussions/3224))

## Good to know

**Pairs well with:**
- tmux ships with Omarchy, and Super + Alt + Return opens a session inside your default terminal. Use it when you need sessions that survive a closed window or follow you over SSH. Ghostty splits and tmux panes coexist fine.
- `omarchy pkg add yazi` gives you a file manager that uses Ghostty's Kitty graphics support to show image previews inline.

**If you hate this, try:** Foot, the current Omarchy default. Smaller, Wayland-only, no GPU requirement, no tabs or splits. Run `omarchy default terminal foot` and pair it with tmux.

**CLI pro tip:** `ghostty +show-config --default --docs | less` prints every option with its documentation, which beats searching the website. `ghostty +list-themes` previews all bundled themes in a picker, though on Omarchy the active theme overrides colors, so comment out the `config-file` line first if you want to try one. `ghostty +list-keybinds --default` dumps the full default keymap. `ghostty +validate-config` catches typos before you reload.

## Compare it

| | Ghostty | Foot | Kitty |
|---|---|---|---|
| Price | Free, MIT | Free, MIT | Free, GPL-3.0 |
| Best for | Tabs and splits without tmux, modern GPU, Omarchy theming out of the box | Old or low-power hardware, minimal footprint, tmux users | Image-heavy terminal apps, remote kittens, people who already have a kitty.conf |
| Omarchy install | `omarchy default terminal ghostty` | `omarchy default terminal foot` | `omarchy default terminal kitty` |

**One-line verdict:** Pick Ghostty if your machine is from this decade and you want tabs and splits without learning tmux; pick Foot if the laptop is old or you live in tmux anyway.

## FAQ

**Does Ghostty work on Omarchy and Hyprland?**
Yes, and it is one of the four terminals Omarchy officially supports with its own config, theme template, font switcher hook and reload signal. It is a GTK4 and libadwaita app running natively on Wayland, no XWayland involved. The one hardware caveat is that it needs OpenGL, so some pre-2012 GPUs cannot run it.

**Is Ghostty free?**
Completely. MIT license, no paid version, no account, nothing phones home.

**Ghostty vs Foot, which should I pick?**
Foot is what Omarchy 4 installs by default and it is fine if you use tmux for splits. Ghostty gives you tabs, splits, ligatures, image rendering and a command palette natively, at the cost of a heavier binary and a GPU requirement. If you pressed Super + Return, wanted a split, and found there was no keybind for one, that is your answer.

**Why does Super + Return still open Foot after I ran `omarchy pkg add ghostty`?**
Because `pkg add` only installs the package. The default terminal is whichever desktop entry is first in `~/.config/xdg-terminals.list`, and only `omarchy default terminal ghostty` (or the Setup > Defaults menu) rewrites that file. Run it once and you are done.

**Why does SSH into my server print "unknown terminal type xterm-ghostty"?**
Ghostty advertises its own terminfo name and the server has never heard of it. Copy the entry over once with `infocmp -x xterm-ghostty | ssh host -- tic -x -`, or set `SetEnv TERM=xterm-256color` in `~/.ssh/config` if you do not care about Ghostty-specific features on that host. Details and the built-in `ssh-terminfo` option are in the issues section above.

**Will Ghostty follow my Omarchy theme?**
Yes, automatically. Omarchy generates `~/.local/state/omarchy/current/theme/ghostty.conf` from each theme's `colors.toml` and the stock config includes it. Switching themes with Super + Ctrl + Shift + Space recolors open windows live. Changing the font via Style > Font edits your config but Ghostty needs a restart to pick it up, and Omarchy tells you so with a notification.

