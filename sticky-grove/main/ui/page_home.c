// Dashboard: the Moon figure beside the day, clock, room climate, today's
// to-dos, habit dots, the next event and the pinned note.
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "board.h"
#include "net.h"
#include "sht40.h"
#include "store.h"
#include "theme.h"
#include "ui.h"

static lv_obj_t *s_clock;
static int s_shown_minute = -1;

static const char *const kDays[] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
static const char *const kMonths[] = {"January", "February", "March", "April", "May", "June", "July",
                                      "August", "September", "October", "November", "December"};

static void set_clock(const struct tm *t)
{
    int hour = t->tm_hour % 12 ? t->tm_hour % 12 : 12;
    lv_label_set_text_fmt(s_clock, "%d:%02d %s", hour, t->tm_min, t->tm_hour < 12 ? "am" : "pm");
    s_shown_minute = t->tm_min;
}

static void todo_toggle(lv_event_t *e)
{
    todo_t *todo = lv_event_get_user_data(e);
    todo->done = lv_obj_has_state(lv_event_get_target(e), LV_STATE_CHECKED);
    store_save_data();
    display_request(DISPLAY_REFRESH_GRAY4);
}

static void dot(lv_obj_t *parent, int x, int y, bool filled, bool today)
{
    lv_obj_t *d = lv_obj_create(parent);
    lv_obj_remove_flag(d, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(d, 12, 12);
    lv_obj_set_pos(d, x, y);
    lv_obj_set_style_radius(d, LV_RADIUS_CIRCLE, 0);
    lv_obj_set_style_border_color(d, COLOR_INK, 0);
    lv_obj_set_style_border_width(d, today ? 2 : 1, 0);
    lv_obj_set_style_bg_color(d, COLOR_INK, 0);
    lv_obj_set_style_bg_opa(d, filled ? LV_OPA_COVER : LV_OPA_TRANSP, 0);
}

static lv_obj_t *small(lv_obj_t *parent, const char *text, int x, int y, int w)
{
    lv_obj_t *l = theme_label(parent, text, FONT_SMALL);
    lv_obj_set_pos(l, x, y);
    if (w > 0) {
        lv_obj_set_width(l, w);
        lv_label_set_long_mode(l, LV_LABEL_LONG_DOT);
    }
    return l;
}

// The lists under the header: to-dos, habits, note. Returns nothing; fills y..ch.
static void lists(lv_obj_t *parent, int x, int y, int w, int h, uint32_t today, int max_habits)
{
    theme_rule(parent, x, y, w);
    y += 6;
    small(parent, "Today", x, y, 0);
    int next = event_next(today);
    if (next >= 0) {
        const event_t *e = &g_data.events[next];
        uint32_t d = day_index(e->year, e->month, e->day);
        lv_obj_t *up = lv_label_create(parent);
        lv_obj_set_style_text_font(up, FONT_SMALL, 0);
        if (d == today) {
            lv_label_set_text_fmt(up, "Today: %s", e->text);
        } else if (d == today + 1) {
            lv_label_set_text_fmt(up, "Tomorrow: %s", e->text);
        } else {
            lv_label_set_text_fmt(up, "%.3s %d: %s", kMonths[e->month - 1], e->day, e->text);
        }
        lv_obj_set_width(up, w - 70);
        lv_label_set_long_mode(up, LV_LABEL_LONG_DOT);
        lv_obj_set_style_text_align(up, LV_TEXT_ALIGN_RIGHT, 0);
        lv_obj_set_pos(up, x + 70, y);
    }
    y += 22;
    int shown = 0;
    for (int i = 0; i < g_data.todo_count && shown < 3; i++) {
        if (g_data.todos[i].done) continue;
        lv_obj_t *cb = lv_checkbox_create(parent);
        lv_checkbox_set_text(cb, g_data.todos[i].text);
        lv_obj_set_width(cb, w);
        lv_obj_set_pos(cb, x, y);
        lv_obj_add_event_cb(cb, todo_toggle, LV_EVENT_VALUE_CHANGED, &g_data.todos[i]);
        y += 22;
        shown++;
    }
    if (shown == 0) {
        small(parent, "All clear. Enjoy the quiet.", x, y, 0);
        y += 22;
    }
    y += 4;
    theme_rule(parent, x, y, w);
    y += 6;
    for (int i = 0; i < g_data.habit_count && i < max_habits; i++) {
        const habit_t *hb = &g_data.habits[i];
        small(parent, hb->name, x, y, w - 120);
        for (int k = 6; k >= 0; k--) {
            dot(parent, x + w - 100 + (6 - k) * 14, y + 3, habit_done_on(hb, today - k), k == 0);
        }
        y += 20;
    }
    if (g_data.habit_count == 0) {
        small(parent, "Add a habit to start a streak.", x, y, 0);
        y += 20;
    }
    y += 2;
    theme_rule(parent, x, y, w);
    y += 6;
    lv_obj_t *note = theme_label(parent, g_data.note[0] ? g_data.note : "Nothing pinned.", FONT_SMALL);
    lv_obj_set_pos(note, x, y);
    lv_obj_set_size(note, w, h - y > 16 ? h - y : 16);
    lv_label_set_long_mode(note, LV_LABEL_LONG_WRAP);
}

void page_home_build(lv_obj_t *parent)
{
    const ui_layout_t *L = ui_layout();
    time_t now = time(NULL);
    struct tm t;
    localtime_r(&now, &t);
    bool time_known = t.tm_year >= 124;
    uint32_t today = day_index_tm(&t);

    char status[96] = "";
    float c, h;
    if (sht40_read(&c, &h)) {
        snprintf(status, sizeof(status), g_cfg.fahrenheit ? "%.0f F, %.0f%% humidity" : "%.0f C, %.0f%% humidity",
                 g_cfg.fahrenheit ? c * 9 / 5 + 32 : c, h);
    }
    char power[48] = "";
    int battery = board_battery_percent();
    if (battery >= 0) {
        snprintf(power, sizeof(power), "Battery %d%%%s", battery, board_on_usb_power() ? ", charging" : "");
    }
    if (net_state() != NET_CONNECTED) {
        strlcat(power, power[0] ? ", offline" : "Offline", sizeof(power));
    }
    const char *weekday = time_known ? kDays[t.tm_wday] : "Hello";
    char date[40];
    if (time_known) {
        snprintf(date, sizeof(date), "%s %d", kMonths[t.tm_mon], t.tm_mday);
    } else {
        snprintf(date, sizeof(date), "Clock not set. Join Wi-Fi in Setup.");
    }

    if (L->portrait) {
        lv_obj_t *fig = theme_image(parent, &asset_figure_s);
        lv_obj_set_pos(fig, 0, 0);
        int x0 = 146, iw = L->cw - 146;
        lv_obj_t *day = theme_label(parent, weekday, FONT_DECO_S);
        lv_obj_set_pos(day, x0, 0);
        small(parent, date, x0, 28, iw);
        s_clock = theme_label(parent, "--:--", FONT_DECO);
        lv_obj_set_pos(s_clock, x0, 52);
        small(parent, status, x0, 96, iw);
        small(parent, power, x0, 116, iw);
        lists(parent, 0, 204, L->cw, L->ch, today, 2);
    } else {
        lv_obj_t *fig = theme_image(parent, &asset_figure_l);
        lv_obj_set_pos(fig, 0, 0);
        int x0 = 204, iw = L->cw - 204;
        lv_obj_t *day = theme_label(parent, weekday, FONT_DECO);
        lv_obj_set_pos(day, x0, 0);
        s_clock = theme_label(parent, "--:--", FONT_DECO_L);
        lv_obj_align(s_clock, LV_ALIGN_TOP_RIGHT, -L->inset, -6);
        small(parent, date, x0, 36, iw);
        char line[150];
        snprintf(line, sizeof(line), "%s%s%s", status, status[0] && power[0] ? "   " : "", power);
        small(parent, line, x0, 56, iw);
        lists(parent, x0, 76, iw, L->ch, today, 3);
    }
    if (time_known) {
        set_clock(&t);
    }
}

void page_home_minute(void)
{
    time_t now = time(NULL);
    struct tm t;
    localtime_r(&now, &t);
    // A grey refresh flashes the whole panel, so the clock only moves every five minutes.
    if (t.tm_year >= 124 && t.tm_min % 5 == 0 && t.tm_min != s_shown_minute) {
        set_clock(&t);
        display_request(DISPLAY_REFRESH_GRAY4);
    }
}
