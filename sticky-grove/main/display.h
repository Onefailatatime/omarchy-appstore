// E-paper panel behind an LVGL display. LVGL renders into a full RGB565 frame;
// every finished frame is turned to grey and pushed by a refresh task.
#pragma once

#include "lvgl.h"

typedef enum {
    DISPLAY_REFRESH_PARTIAL = 0,  // quick, black and white, no flash
    DISPLAY_REFRESH_FULL,         // black and white with a clean flash
    DISPLAY_REFRESH_GRAY4,        // four grey levels, slowest; used for the dashboard
} display_refresh_t;

lv_display_t *display_init(void);
// Mode for the next pushed frame. Stronger modes win until the frame is shown.
void display_request(display_refresh_t mode);
// Blocks until no frame is being pushed, or the timeout passes.
void display_wait_idle(uint32_t timeout_ms);
void display_sleep(void);
