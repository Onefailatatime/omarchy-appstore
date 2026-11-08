// Habits: one row each with the last seven days, the streak and a Done button.
#include <time.h>
#include "store.h"
#include "theme.h"
#include "ui.h"

static lv_obj_t *s_list;
static uint32_t s_today;

static void rebuild(void);

static void done_cb(lv_event_t *e)
{
    habit_t *h = lv_event_get_user_data(e);
    habit_set(h, s_today, !habit_done_on(h, s_today));
    store_save_data();
    rebuild();
}

static void delete_cb(lv_event_t *e)
{
    habit_remove((int)(intptr_t)lv_event_get_user_data(e));
    store_save_data();
    rebuild();
}

static void added(lv_obj_t *ta, void *user_data)
{
    if (habit_add(lv_textarea_get_text(ta))) {
        store_save_data();
        rebuild();
    }
}

static void add_cb(lv_event_t *e)
{
    ui_prompt("New habit", "Something small, done daily", HABIT_TEXT - 1, added, NULL);
}

static void day_box(lv_obj_t *parent, int x, bool filled, bool today)
{
    lv_obj_t *b = lv_obj_create(parent);
    lv_obj_remove_flag(b, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(b, 26, 26);
    lv_obj_align(b, LV_ALIGN_LEFT_MID, x, 0);
    lv_obj_set_style_radius(b, 8, 0);
    lv_obj_set_style_border_color(b, COLOR_INK, 0);
    lv_obj_set_style_border_width(b, today ? 3 : 1, 0);
    lv_obj_set_style_bg_color(b, COLOR_INK, 0);
    lv_obj_set_style_bg_opa(b, filled ? LV_OPA_COVER : LV_OPA_TRANSP, 0);
}

static void rebuild(void)
{
    lv_obj_clean(s_list);
    for (int i = 0; i < g_data.habit_count; i++) {
        habit_t *h = &g_data.habits[i];
        lv_obj_t *row = theme_card(s_list, LV_PCT(100), 62);
        lv_obj_set_style_pad_ver(row, 6, 0);
        lv_obj_t *name = theme_label(row, h->name, FONT_BODY);
        lv_obj_align(name, LV_ALIGN_LEFT_MID, 0, 0);
        lv_obj_set_width(name, 170);
        lv_label_set_long_mode(name, LV_LABEL_LONG_DOT);
        for (int k = 6; k >= 0; k--) {
            day_box(row, 180 + (6 - k) * 32, habit_done_on(h, s_today - k), k == 0);
        }
        lv_obj_t *streak = lv_label_create(row);
        lv_obj_set_style_text_font(streak, FONT_SMALL, 0);
        int n = habit_streak(h, s_today);
        lv_label_set_text_fmt(streak, n == 1 ? "%d day" : "%d days", n);
        lv_obj_align(streak, LV_ALIGN_LEFT_MID, 412, 0);
        lv_obj_t *done = theme_button(row, habit_done_on(h, s_today) ? LV_SYMBOL_OK "  Done" : "Done",
                                      done_cb, h);
        lv_obj_set_size(done, 100, 42);
        lv_obj_set_style_pad_all(done, 4, 0);
        if (habit_done_on(h, s_today)) {
            lv_obj_add_state(done, LV_STATE_CHECKED);
        }
        lv_obj_align(done, LV_ALIGN_RIGHT_MID, -52, 0);
        lv_obj_t *del = theme_button(row, LV_SYMBOL_CLOSE, delete_cb, (void *)(intptr_t)i);
        lv_obj_set_size(del, 42, 42);
        lv_obj_set_style_pad_all(del, 4, 0);
        lv_obj_set_style_text_font(del, FONT_SMALL, 0);
        lv_obj_align(del, LV_ALIGN_RIGHT_MID, 0, 0);
    }
    if (g_data.habit_count == 0) {
        theme_label(s_list, "No habits yet. Tap Add and keep it tiny.", FONT_BODY);
    }
}

void page_habits_build(lv_obj_t *parent)
{
    time_t now = time(NULL);
    struct tm t;
    localtime_r(&now, &t);
    s_today = day_index_tm(&t);

    theme_title(parent, "Habits");
    lv_obj_t *add = theme_button(parent, LV_SYMBOL_PLUS "  Add", add_cb, NULL);
    lv_obj_align(add, LV_ALIGN_TOP_RIGHT, 0, 0);
    lv_obj_t *hint = theme_label(parent, "Last seven days, today on the right.", FONT_SMALL);
    lv_obj_set_pos(hint, 2, 44);

    s_list = theme_column(parent, UI_CONTENT_W - 32, UI_CONTENT_H - 32 - 72);
    lv_obj_set_pos(s_list, 0, 72);
    rebuild();
}
