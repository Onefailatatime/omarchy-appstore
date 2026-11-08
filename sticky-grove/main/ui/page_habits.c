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

static void day_box(lv_obj_t *parent, int x, int y, bool filled, bool today)
{
    lv_obj_t *b = lv_obj_create(parent);
    lv_obj_remove_flag(b, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(b, 20, 20);
    lv_obj_set_pos(b, x, y);
    lv_obj_set_style_radius(b, 5, 0);
    lv_obj_set_style_border_color(b, COLOR_INK, 0);
    lv_obj_set_style_border_width(b, today ? 2 : 1, 0);
    lv_obj_set_style_bg_color(b, COLOR_INK, 0);
    lv_obj_set_style_bg_opa(b, filled ? LV_OPA_COVER : LV_OPA_TRANSP, 0);
}

static void rebuild(void)
{
    const ui_layout_t *L = ui_layout();
    int w = L->cw;
    lv_obj_clean(s_list);
    for (int i = 0; i < g_data.habit_count; i++) {
        habit_t *h = &g_data.habits[i];
        bool done = habit_done_on(h, s_today);
        int streak = habit_streak(h, s_today);
        lv_obj_t *row = theme_row(s_list, L->portrait ? 66 : 48);
        lv_obj_t *name = theme_label(row, h->name, FONT_BODY);
        lv_obj_set_pos(name, 0, L->portrait ? 2 : 12);
        lv_obj_set_size(name, L->portrait ? w - 120 : 150, 22);
        lv_label_set_long_mode(name, LV_LABEL_LONG_DOT);
        lv_obj_t *count = lv_label_create(row);
        lv_obj_set_style_text_font(count, FONT_SMALL, 0);
        lv_label_set_text_fmt(count, streak == 1 ? "%d day" : "%d days", streak);
        int boxes_x = L->portrait ? 0 : 160;
        int boxes_y = L->portrait ? 34 : 14;
        for (int k = 6; k >= 0; k--) {
            day_box(row, boxes_x + (6 - k) * 24, boxes_y, habit_done_on(h, s_today - k), k == 0);
        }
        lv_obj_set_pos(count, L->portrait ? w - 112 : 336, L->portrait ? 4 : 14);
        lv_obj_t *btn = theme_button(row, done ? LV_SYMBOL_OK "  Done" : "Done", done_cb, h);
        lv_obj_set_size(btn, 84, 32);
        lv_obj_set_style_pad_all(btn, 4, 0);
        if (done) {
            lv_obj_add_state(btn, LV_STATE_CHECKED);
        }
        lv_obj_set_pos(btn, L->portrait ? 180 : w - 130, L->portrait ? 28 : 8);
        lv_obj_t *del = theme_button(row, LV_SYMBOL_CLOSE, delete_cb, (void *)(intptr_t)i);
        lv_obj_set_size(del, 36, 30);
        lv_obj_set_style_pad_all(del, 2, 0);
        lv_obj_set_style_text_font(del, &lv_font_montserrat_14, 0);
        lv_obj_set_pos(del, w - 36, L->portrait ? 0 : 9);
        theme_rule(row, 0, L->portrait ? 65 : 47, w);
    }
    if (g_data.habit_count == 0) {
        theme_label(s_list, "No habits yet. Tap Add and keep it tiny.", FONT_SMALL);
    }
}

void page_habits_build(lv_obj_t *parent)
{
    const ui_layout_t *L = ui_layout();
    time_t now = time(NULL);
    struct tm t;
    localtime_r(&now, &t);
    s_today = day_index_tm(&t);

    lv_obj_t *add = theme_button(parent, LV_SYMBOL_PLUS "  Add", add_cb, NULL);
    lv_obj_align(add, LV_ALIGN_TOP_RIGHT, -L->inset, 0);
    lv_obj_t *hint = theme_label(parent, "Seven days, today on the right.", FONT_SMALL);
    lv_obj_set_pos(hint, L->portrait ? 36 : 0, 10);   // clear of the portrait frame's lily

    s_list = theme_column(parent, L->cw, L->ch - 44);
    lv_obj_set_pos(s_list, 0, 44);
    rebuild();
}
