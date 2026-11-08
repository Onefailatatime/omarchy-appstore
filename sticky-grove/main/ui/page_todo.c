// To-do list: tick things off, add with the keyboard, sweep the done ones away.
#include "store.h"
#include "theme.h"
#include "ui.h"

static lv_obj_t *s_list;

static void rebuild(void);

static void toggle_cb(lv_event_t *e)
{
    todo_t *todo = lv_event_get_user_data(e);
    todo->done = lv_obj_has_state(lv_event_get_target(e), LV_STATE_CHECKED);
    store_save_data();
}

static void delete_cb(lv_event_t *e)
{
    todo_remove((int)(intptr_t)lv_event_get_user_data(e));
    store_save_data();
    rebuild();
}

static void added(lv_obj_t *ta, void *user_data)
{
    if (todo_add(lv_textarea_get_text(ta))) {
        store_save_data();
        rebuild();
    }
}

static void add_cb(lv_event_t *e)
{
    ui_prompt("New to-do", "What needs doing?", TODO_TEXT - 1, added, NULL);
}

static void clear_cb(lv_event_t *e)
{
    todo_clear_done();
    store_save_data();
    rebuild();
}

static void rebuild(void)
{
    lv_obj_clean(s_list);
    for (int i = 0; i < g_data.todo_count; i++) {
        lv_obj_t *row = lv_obj_create(s_list);
        lv_obj_remove_flag(row, LV_OBJ_FLAG_SCROLLABLE);
        lv_obj_set_size(row, LV_PCT(100), 48);
        lv_obj_t *cb = lv_checkbox_create(row);
        lv_checkbox_set_text(cb, g_data.todos[i].text);
        lv_obj_set_width(cb, 560);
        lv_obj_align(cb, LV_ALIGN_LEFT_MID, 0, 0);
        if (g_data.todos[i].done) {
            lv_obj_add_state(cb, LV_STATE_CHECKED);
            lv_obj_set_style_text_decor(cb, LV_TEXT_DECOR_STRIKETHROUGH, 0);
            lv_obj_set_style_text_color(cb, COLOR_SHADE, 0);
        }
        lv_obj_add_event_cb(cb, toggle_cb, LV_EVENT_VALUE_CHANGED, &g_data.todos[i]);
        lv_obj_t *del = theme_button(row, LV_SYMBOL_CLOSE, delete_cb, (void *)(intptr_t)i);
        lv_obj_set_size(del, 44, 40);
        lv_obj_set_style_pad_all(del, 4, 0);
        lv_obj_set_style_text_font(del, FONT_SMALL, 0);
        lv_obj_align(del, LV_ALIGN_RIGHT_MID, 0, 0);
    }
    if (g_data.todo_count == 0) {
        theme_label(s_list, "Nothing here. Tap Add to plant the first task.", FONT_BODY);
    }
}

void page_todo_build(lv_obj_t *parent)
{
    theme_title(parent, "To-do");
    lv_obj_t *add = theme_button(parent, LV_SYMBOL_PLUS "  Add", add_cb, NULL);
    lv_obj_align(add, LV_ALIGN_TOP_RIGHT, 0, 0);
    lv_obj_t *clear = theme_button(parent, "Clear done", clear_cb, NULL);
    lv_obj_align_to(clear, add, LV_ALIGN_OUT_LEFT_MID, -10, 0);

    s_list = theme_column(parent, UI_CONTENT_W - 32, UI_CONTENT_H - 32 - 58);
    lv_obj_set_pos(s_list, 0, 58);
    lv_obj_set_style_pad_row(s_list, 4, 0);
    rebuild();
}
