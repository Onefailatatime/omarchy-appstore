#include "ui.h"

#include "store.h"
#include "theme.h"

static lv_obj_t *s_content;
static lv_obj_t *s_nav[PAGE_COUNT];
static lv_obj_t *s_keyboard;
static lv_obj_t *s_prompt;
static ui_page_t s_page = PAGE_HOME;
static ui_keyboard_done_cb s_kb_done;
static void *s_kb_user;

static const char *const page_names[PAGE_COUNT] = {
    "Home", "To-do", "Habits", "Month", "Note", "Chat", "Setup",
};

static void nav_cb(lv_event_t *e)
{
    ui_show((ui_page_t)(intptr_t)lv_event_get_user_data(e));
}

static void keyboard_cb(lv_event_t *e)
{
    lv_obj_t *ta = lv_keyboard_get_textarea(s_keyboard);
    if (lv_event_get_code(e) == LV_EVENT_READY && s_kb_done) {
        ui_keyboard_done_cb done = s_kb_done;
        void *user = s_kb_user;
        ui_keyboard_close();
        done(ta, user);
        return;
    }
    ui_keyboard_close();
}

void ui_init(void)
{
    theme_init(lv_display_get_default());
    lv_obj_t *scr = lv_screen_active();
    lv_obj_remove_flag(scr, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_style_bg_color(scr, COLOR_PAPER, 0);
    lv_obj_set_style_bg_opa(scr, LV_OPA_COVER, 0);

    lv_obj_t *side = lv_obj_create(scr);
    lv_obj_remove_flag(side, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_size(side, UI_SIDEBAR_W, UI_CONTENT_H);
    lv_obj_set_pos(side, 0, 0);
    lv_obj_set_style_border_color(side, COLOR_INK, 0);
    lv_obj_set_style_border_width(side, 2, 0);
    lv_obj_set_style_border_side(side, LV_BORDER_SIDE_RIGHT, 0);
    lv_obj_set_style_pad_all(side, 8, 0);
    lv_obj_set_flex_flow(side, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_flex_align(side, LV_FLEX_ALIGN_START, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);
    lv_obj_set_style_pad_row(side, 6, 0);
    for (int i = 0; i < PAGE_COUNT; i++) {
        s_nav[i] = theme_button(side, page_names[i], nav_cb, (void *)(intptr_t)i);
        lv_obj_set_size(s_nav[i], 92, i == PAGE_SETTINGS ? 44 : 56);
        lv_obj_set_style_text_font(s_nav[i], i == PAGE_SETTINGS ? FONT_SMALL : FONT_BODY, 0);
        lv_obj_remove_flag(s_nav[i], LV_OBJ_FLAG_CHECKABLE);
    }

    s_content = lv_obj_create(scr);
    lv_obj_remove_flag(s_content, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_size(s_content, UI_CONTENT_W, UI_CONTENT_H);
    lv_obj_set_pos(s_content, UI_SIDEBAR_W, 0);
    lv_obj_set_style_pad_all(s_content, 16, 0);

    s_keyboard = lv_keyboard_create(lv_layer_top());
    lv_obj_set_size(s_keyboard, UI_CONTENT_W, 230);
    lv_obj_align(s_keyboard, LV_ALIGN_BOTTOM_RIGHT, 0, 0);
    lv_obj_add_event_cb(s_keyboard, keyboard_cb, LV_EVENT_READY, NULL);
    lv_obj_add_event_cb(s_keyboard, keyboard_cb, LV_EVENT_CANCEL, NULL);
    lv_obj_add_flag(s_keyboard, LV_OBJ_FLAG_HIDDEN);

    ui_show(g_cfg.wifi_ssid[0] ? PAGE_HOME : PAGE_SETTINGS);
}

void ui_show(ui_page_t page)
{
    ui_keyboard_close();
    if (s_prompt) {
        lv_obj_delete(s_prompt);
        s_prompt = NULL;
    }
    s_page = page;
    for (int i = 0; i < PAGE_COUNT; i++) {
        if (i == page) {
            lv_obj_add_state(s_nav[i], LV_STATE_CHECKED);
        } else {
            lv_obj_remove_state(s_nav[i], LV_STATE_CHECKED);
        }
    }
    lv_obj_clean(s_content);
    switch (page) {
    case PAGE_HOME:     page_home_build(s_content); break;
    case PAGE_TODO:     page_todo_build(s_content); break;
    case PAGE_HABITS:   page_habits_build(s_content); break;
    case PAGE_CALENDAR: page_calendar_build(s_content); break;
    case PAGE_NOTE:     page_note_build(s_content); break;
    case PAGE_CHAT:     page_chat_build(s_content); break;
    default:            page_settings_build(s_content); break;
    }
    display_request(page == PAGE_HOME ? DISPLAY_REFRESH_GRAY4 : DISPLAY_REFRESH_FULL);
}

ui_page_t ui_current(void)
{
    return s_page;
}

void ui_handle_button(board_button_t button)
{
    lv_display_trigger_activity(NULL);
    switch (button) {
    case BOARD_BTN_UP:   ui_show((s_page + PAGE_COUNT - 1) % PAGE_COUNT); break;
    case BOARD_BTN_DOWN: ui_show((s_page + 1) % PAGE_COUNT); break;
    case BOARD_BTN_AI:   ui_show(s_page == PAGE_CHAT ? PAGE_HOME : PAGE_CHAT); break;
    default: break;
    }
}

void ui_minute_tick(void)
{
    if (s_page == PAGE_HOME) {
        page_home_minute();
    }
}

void ui_keyboard_open(lv_obj_t *ta, ui_keyboard_done_cb done, void *user_data)
{
    s_kb_done = done;
    s_kb_user = user_data;
    lv_keyboard_set_textarea(s_keyboard, ta);
    lv_keyboard_set_mode(s_keyboard, LV_KEYBOARD_MODE_TEXT_LOWER);
    lv_obj_remove_flag(s_keyboard, LV_OBJ_FLAG_HIDDEN);
    lv_obj_scroll_to_view(ta, LV_ANIM_OFF);
    lv_obj_update_layout(ta);
    // The keyboard covers the bottom 230 px; scroll the field's list up if it sits under it.
    lv_area_t box;
    lv_obj_get_coords(ta, &box);
    int32_t limit = UI_CONTENT_H - 230 - 10;
    lv_obj_t *scroller = lv_obj_get_parent(ta);
    while (scroller && !lv_obj_has_flag(scroller, LV_OBJ_FLAG_SCROLLABLE)) {
        scroller = lv_obj_get_parent(scroller);
    }
    if (scroller && box.y2 > limit) {
        lv_obj_scroll_by_bounded(scroller, 0, limit - box.y2, LV_ANIM_OFF);
    }
}

void ui_keyboard_close(void)
{
    lv_keyboard_set_textarea(s_keyboard, NULL);
    lv_obj_add_flag(s_keyboard, LV_OBJ_FLAG_HIDDEN);
    s_kb_done = NULL;
}

static void prompt_done(lv_obj_t *ta, void *user_data)
{
    ui_keyboard_done_cb done = (ui_keyboard_done_cb)lv_obj_get_user_data(s_prompt);
    done(ta, user_data);
    lv_obj_delete(s_prompt);
    s_prompt = NULL;
}

static void prompt_cancel(lv_event_t *e)
{
    ui_keyboard_close();
    lv_obj_delete(s_prompt);
    s_prompt = NULL;
}

void ui_prompt(const char *title, const char *placeholder, int max_len, ui_keyboard_done_cb done, void *user_data)
{
    if (s_prompt) {
        lv_obj_delete(s_prompt);
    }
    s_prompt = theme_card(lv_layer_top(), UI_CONTENT_W - 40, 150);
    lv_obj_set_pos(s_prompt, UI_SIDEBAR_W + 20, 30);
    lv_obj_set_user_data(s_prompt, (void *)done);
    theme_label(s_prompt, title, FONT_TITLE);
    lv_obj_t *ta = lv_textarea_create(s_prompt);
    lv_textarea_set_one_line(ta, true);
    lv_textarea_set_max_length(ta, max_len);
    lv_textarea_set_placeholder_text(ta, placeholder);
    lv_obj_set_size(ta, UI_CONTENT_W - 200, 52);
    lv_obj_align(ta, LV_ALIGN_BOTTOM_LEFT, 0, 0);
    lv_obj_t *cancel = theme_button(s_prompt, "Cancel", prompt_cancel, NULL);
    lv_obj_align(cancel, LV_ALIGN_BOTTOM_RIGHT, 0, 0);
    ui_keyboard_open(ta, prompt_done, user_data);
}
