# seeed_epaper

SSD1677 / UC8179 e-paper panel driver for ESP-IDF, taken from
[Lukilyy/reterminal-sticky-2048-eink-game](https://github.com/Lukilyy/reterminal-sticky-2048-eink-game)
(MIT). Only change here: the upstream `debug_logging` component is replaced by
the no-op macros in `app_debug_log.h`.

API used by this project: `seeed_epaper_new_panel`, `seeed_epaper_panel_prepare`,
`seeed_epaper_panel_write_bitmap` (GRAY8 input), `seeed_epaper_panel_write_bitmap_gray4`
(2 bpp input, 0 = white, 3 = black), `seeed_epaper_panel_commit`, `seeed_epaper_panel_sleep`.
