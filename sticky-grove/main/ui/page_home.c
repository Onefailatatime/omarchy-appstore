// Dashboard: date and clock, room climate, today's to-dos, habit dots, the note,
// the next calendar event, and the grove along the bottom.
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
    lv_obj_set_size(d, 14, 14);
    lv_obj_set_pos(d, x, y);
    lv_obj_set_style_radius(d, LV_RADIUS_CIRCLE, 0);
    lv_obj_set_style_border_color(d, COLOR_INK, 0);
    lv_obj_set_style_border_width(d, today ? 2 : 1, 0);
    lv_obj_set_style_bg_color(d, COLOR_INK, 0);
    lv_obj_set_style_bg_opa(d, filled ? LV_OPA_COVER : LV_OPA_TRANSP, 0);
}

void page_home_build(lv_obj_t *parent)
{
    time_t now = time(NULL);
    struct tm t;
    localtime_r(&now, &t);
    bool time_known = t.tm_year >= 124;
    uint32_t today = day_index_tm(&t);

    lv_obj_t *day = theme_label(parent, time_known ? kDays[t.tm_wday] : "Hello", FONT_HERO);
    lv_obj_set_pos(day, 0, 0);
    lv_obj_t *date = lv_label_create(parent);
    if (time_known) {
        lv_label_set_text_fmt(date, "%s %d", kMonths[t.tm_mon], t.tm_mday);
    } else {
        lv_label_set_text(date, "Clock not set yet. Connect Wi-Fi in Setup.");
    }
    lv_obj_set_pos(date, 2, 42);

    s_clock = theme_label(parent, "", FONT_CLOCK);
    lv_obj_align(s_clock, LV_ALIGN_TOP_RIGHT, 0, -6);
    if (time_known) {
        set_clock(&t);
    } else {
        lv_label_set_text(s_clock, "--:--");
    }

    // Status line: climate, battery, network, next event.
    char status[160] = "";
    float c, h;
    if (sht40_read(&c, &h)) {
        if (g_cfg.fahrenheit) {
            snprintf(status, sizeof(status), "%.0f F  %.0f%% humidity", c * 9 / 5 + 32, h);
        } else {
            snprintf(status, sizeof(status), "%.0f C  %.0f%% humidity", c, h);
        }
    }
    int battery = board_battery_percent();
    if (battery >= 0) {
        snprintf(status + strlen(status), sizeof(status) - strlen(status), "   Battery %d%%%s",
                 battery, board_on_usb_power() ? " (charging)" : "");
    }
    if (net_state() != NET_CONNECTED) {
        snprintf(status + strlen(status), sizeof(status) - strlen(status), "   Offline");
    }
    lv_obj_t *status_label = theme_label(parent, status, FONT_SMALL);
    lv_obj_set_pos(status_label, 2, 76);

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
            lv_label_set_text_fmt(up, "%s %d: %s", kMonths[e->month - 1], e->day, e->text);
        }
        lv_obj_set_width(up, 300);
        lv_label_set_long_mode(up, LV_LABEL_LONG_DOT);
        lv_obj_align(up, LV_ALIGN_TOP_RIGHT, 0, 78);
        lv_obj_set_style_text_align(up, LV_TEXT_ALIGN_RIGHT, 0);
    }

    // Three cards.
    const int top = 108, height = 206;
    lv_obj_t *todo_card = theme_card(parent, 300, height);
    lv_obj_set_pos(todo_card, 0, top);
    theme_label(todo_card, "Today", FONT_SMALL);
    int shown = 0, y = 28;
    for (int i = 0; i < g_data.todo_count && shown < 4; i++) {
        if (g_data.todos[i].done) continue;
        lv_obj_t *cb = lv_checkbox_create(todo_card);
        lv_checkbox_set_text(cb, g_data.todos[i].text);
        lv_obj_set_style_text_font(cb, FONT_SMALL, 0);
        lv_obj_set_width(cb, 272);
        lv_obj_set_pos(cb, 0, y);
        lv_obj_add_event_cb(cb, todo_toggle, LV_EVENT_VALUE_CHANGED, &g_data.todos[i]);
        y += 38;
        shown++;
    }
    if (shown == 0) {
        lv_obj_t *empty = theme_label(todo_card, "All clear. Enjoy the quiet.", FONT_SMALL);
        lv_obj_set_pos(empty, 0, 32);
    }

    lv_obj_t *habit_card = theme_card(parent, 186, height);
    lv_obj_set_pos(habit_card, 310, top);
    theme_label(habit_card, "Habits", FONT_SMALL);
    y = 30;
    for (int i = 0; i < g_data.habit_count && i < 5; i++) {
        const habit_t *hb = &g_data.habits[i];
        lv_obj_t *name = theme_label(habit_card, hb->name, FONT_SMALL);
        lv_obj_set_pos(name, 0, y);
        lv_obj_set_size(name, 58, 20);
        lv_label_set_long_mode(name, LV_LABEL_LONG_DOT);
        for (int k = 6; k >= 0; k--) {
            dot(habit_card, 62 + (6 - k) * 14, y + 2, habit_done_on(hb, today - k), k == 0);
        }
        y += 32;
    }
    if (g_data.habit_count == 0) {
        lv_obj_t *empty = theme_label(habit_card, "Add a habit to\nstart a streak.", FONT_SMALL);
        lv_obj_set_pos(empty, 0, 32);
    }

    lv_obj_t *note_card = theme_card(parent, 152, height);
    lv_obj_set_pos(note_card, 506, top);
    theme_label(note_card, "Note", FONT_SMALL);
    lv_obj_t *note = theme_label(note_card, g_data.note[0] ? g_data.note : "Nothing pinned.", FONT_SMALL);
    lv_obj_set_pos(note, 0, 28);
    lv_obj_set_width(note, 124);
    lv_obj_set_height(note, 150);
    lv_label_set_long_mode(note, LV_LABEL_LONG_WRAP);

    theme_scenery(parent, 324, UI_CONTENT_W - 32, 124);
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
