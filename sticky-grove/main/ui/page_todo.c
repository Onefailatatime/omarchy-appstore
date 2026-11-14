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
        lv_obj_t *row = theme_row(s_list, 40);
        lv_obj_t *cb = lv_checkbox_create(row);
        lv_checkbox_set_text(cb, g_data.todos[i].text);
        lv_obj_set_width(cb, lv_obj_get_width(s_list) - 50);
        lv_obj_align(cb, LV_ALIGN_LEFT_MID, 0, 0);
        if (g_data.todos[i].done) {
            lv_obj_add_state(cb, LV_STATE_CHECKED);
            lv_obj_set_style_text_decor(cb, LV_TEXT_DECOR_STRIKETHROUGH, 0);
            lv_obj_set_style_text_color(cb, COLOR_SHADE, 0);
        }
        lv_obj_add_event_cb(cb, toggle_cb, LV_EVENT_VALUE_CHANGED, &g_data.todos[i]);
        lv_obj_t *del = theme_button(row, LV_SYMBOL_CLOSE, delete_cb, (void *)(intptr_t)i);
        lv_obj_set_size(del, 36, 30);
        lv_obj_set_style_pad_all(del, 2, 0);
        lv_obj_set_style_text_font(del, &lv_font_montserrat_14, 0);
        lv_obj_align(del, LV_ALIGN_RIGHT_MID, 0, 0);
        theme_rule(row, 0, 39, lv_obj_get_width(s_list));
    }
    if (g_data.todo_count == 0) {
        theme_label(s_list, "Nothing here. Tap Add to plant the first task.", FONT_SMALL);
    }
}

void page_todo_build(lv_obj_t *parent)
{
    const ui_layout_t *L = ui_layout();
    lv_obj_t *add = theme_button(parent, LV_SYMBOL_PLUS "  Add", add_cb, NULL);
    lv_obj_align(add, LV_ALIGN_TOP_RIGHT, -L->inset, 0);
    lv_obj_t *clear = theme_button(parent, "Clear done", clear_cb, NULL);
    lv_obj_align_to(clear, add, LV_ALIGN_OUT_LEFT_MID, -8, 0);
    if (!L->portrait) {   // no room beside the buttons when upright
        lv_obj_t *count = lv_label_create(parent);
        lv_obj_set_style_text_font(count, FONT_SMALL, 0);
        int open = 0;
        for (int i = 0; i < g_data.todo_count; i++) open += !g_data.todos[i].done;
        lv_label_set_text_fmt(count, "%d open", open);
        lv_obj_set_pos(count, 0, 10);
    }

    s_list = theme_column(parent, L->cw, L->ch - 44);
    lv_obj_set_pos(s_list, 0, 44);
    lv_obj_update_layout(s_list);
    rebuild();
}
