// Renders each page to out/<page>.pgm the way the panel would show it:
// four greys for Home, pure black and white for every other page.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include "assets.h"
#include "lvgl.h"
#include "store.h"
#include "ui/ui.h"

#define W 800
#define H 480
static uint16_t frame[W * H];
static int cur_w = W, cur_h = H;
static uint32_t ticks;

static uint32_t tick_cb(void) { return ticks; }

void preview_rebind_buffer(void)
{
    lv_display_set_buffers(lv_display_get_default(), frame, NULL, sizeof(frame), LV_DISPLAY_RENDER_MODE_DIRECT);
}

static void flush_cb(lv_display_t *d, const lv_area_t *a, uint8_t *px)
{
    lv_display_flush_ready(d);
}

static void save(const char *name, bool gray4)
{
    char path[128];
    snprintf(path, sizeof(path), "out/%s.pgm", name);
    FILE *f = fopen(path, "wb");
    fprintf(f, "P5\n%d %d\n255\n", cur_w, cur_h);
    for (int i = 0; i < cur_w * cur_h; i++) {
        uint16_t p = frame[i];
        uint32_t r = (p >> 11) & 0x1F, g = (p >> 5) & 0x3F, b = p & 0x1F;
        uint8_t gray = (r * 255 / 31 * 77 + g * 255 / 63 * 151 + b * 255 / 31 * 28) >> 8;
        uint8_t shown = gray4 ? (uint8_t)((gray >> 6) * 85) : (gray >= 128 ? 255 : 0);
        fputc(shown, f);
    }
    fclose(f);
    printf("wrote %s\n", path);
}

static void settle(void)
{
    for (int i = 0; i < 10; i++) {
        ticks += 50;
        lv_timer_handler();
    }
}

int main(void)
{
    mkdir("out", 0755);
    setenv("TZ", "EST5EDT,M3.2.0,M11.1.0", 1);
    tzset();
    lv_init();
    lv_tick_set_cb(tick_cb);
    lv_display_t *disp = lv_display_create(W, H);
    lv_display_set_color_format(disp, LV_COLOR_FORMAT_RGB565);
    lv_display_set_buffers(disp, frame, NULL, sizeof(frame), LV_DISPLAY_RENDER_MODE_DIRECT);
    lv_display_set_flush_cb(disp, flush_cb);

    assets_init();
    store_init();
    strcpy(g_cfg.wifi_ssid, "HomeWifi");
    strcpy(g_cfg.venice_key, "vn_demo");
    todo_add("Send proposal to Maya");
    todo_add("Post the case study");
    g_data.todos[1].done = true;
    time_t now = time(NULL);
    struct tm t;
    localtime_r(&now, &t);
    uint32_t today = day_index_tm(&t);
    for (int k = 1; k <= 4; k++) habit_set(&g_data.habits[0], today - k, true);
    habit_set(&g_data.habits[1], today, true);
    habit_set(&g_data.habits[1], today - 1, true);
    habit_set(&g_data.habits[2], today - 2, true);
    event_add(t.tm_year + 1900, t.tm_mon + 1, t.tm_mday, "Call with Sam, 3 pm");
    event_add(t.tm_year + 1900, t.tm_mon + 1, t.tm_mday < 20 ? t.tm_mday + 6 : 2, "Invoice due");
    strcpy(g_data.note, "Five clients by spring.\nOne kind email a day.");

    ui_init();
    const char *names[PAGE_COUNT] = {"home", "todo", "habits", "calendar", "note", "chat", "settings"};
    for (int p = 0; p < PAGE_COUNT; p++) {
        ui_show(p);
        settle();
        save(names[p], p == PAGE_HOME);
    }
    ui_show(PAGE_TODO);
    settle();
    ui_prompt("New to-do", "What needs doing?", TODO_TEXT - 1, NULL, NULL);
    settle();
    save("todo_keyboard", false);

    // The same pages held upright.
    ui_set_rotation(ROT_PORTRAIT_CW);
    cur_w = H;
    cur_h = W;
    for (int p = 0; p < PAGE_COUNT; p++) {
        char name[32];
        snprintf(name, sizeof(name), "portrait_%s", names[p]);
        ui_show(p);
        settle();
        save(name, p == PAGE_HOME);
    }
    return 0;
}
