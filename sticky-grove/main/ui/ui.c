#include "ui.h"

#include "store.h"
#include "theme.h"

// Frame interiors measured from the artwork at panel size.
static const ui_layout_t kLandscape = { false, 800, 480, 176, 84, 548, 286, 28 };
static const ui_layout_t kPortrait  = { true,  480, 800,  80, 98, 320, 392, 24 };

static const char *const kNav[PAGE_COUNT]   = { "Home", "To-do", "Habits", "Month", "Note", "Oracle", "Setup" };
static const char *const kTitle[PAGE_COUNT] = { "Home", "To-do", "Habits", "The Month", "The Note", "The Oracle", "Setup" };

static const ui_layout_t *L = &kLandscape;
static lv_obj_t *s_content, *s_title, *s_keyboard, *s_prompt;
static lv_obj_t *s_nav[PAGE_COUNT], *s_nav_mark[PAGE_COUNT];
static ui_page_t s_page = PAGE_HOME;
static ui_keyboard_done_cb s_kb_done;
static void *s_kb_user;

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

static lv_obj_t *nav_item(lv_obj_t *parent, int page, int x, int y, int w)
{
    lv_obj_t *btn = lv_button_create(parent);
    lv_obj_set_style_border_width(btn, 0, 0);
    lv_obj_set_style_bg_opa(btn, LV_OPA_TRANSP, 0);
    lv_obj_set_style_bg_opa(btn, LV_OPA_TRANSP, LV_STATE_CHECKED);
    lv_obj_set_style_text_color(btn, COLOR_INK, LV_STATE_CHECKED);
    lv_obj_set_style_pad_all(btn, 0, 0);
    lv_obj_set_size(btn, w, 28);
    lv_obj_set_pos(btn, x, y);
    lv_obj_add_event_cb(btn, nav_cb, LV_EVENT_CLICKED, (void *)(intptr_t)page);
    lv_obj_t *label = theme_label(btn, kNav[page], FONT_DECO_S);
    if (L->portrait) {
        // No room for a star: the chosen page is underlined instead.
        lv_obj_set_style_text_decor(btn, LV_TEXT_DECOR_UNDERLINE, LV_STATE_CHECKED);
        lv_obj_center(label);
        s_nav_mark[page] = NULL;
    } else {
        s_nav_mark[page] = theme_image(btn, &asset_star_s);
        lv_obj_align(s_nav_mark[page], LV_ALIGN_LEFT_MID, 0, 0);
        lv_obj_align(label, LV_ALIGN_LEFT_MID, 24, 0);
    }
    return btn;
}

static void build_shell(void)
{
    lv_obj_t *scr = lv_screen_active();
    lv_obj_clean(scr);
    lv_obj_clean(lv_layer_top());
    s_prompt = NULL;
    lv_obj_remove_flag(scr, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_style_bg_color(scr, COLOR_PAPER, 0);
    lv_obj_set_style_bg_opa(scr, LV_OPA_COVER, 0);

    theme_image(scr, L->portrait ? &asset_frame_port : &asset_frame_land);

    if (L->portrait) {
        // Three rows of names under the content, above the poppies.
        int y = L->cy + L->ch + 8;
        int w = L->cw / 3;
        for (int i = 0; i < PAGE_COUNT; i++) {
            int row = i / 3, col = i % 3;
            int x = row == 2 ? L->cx + w : L->cx + col * w;   // "Setup" sits alone, centred
            s_nav[i] = nav_item(scr, i, x, y + row * 28, w);
        }
    } else {
        // Between the top and bottom lilies on the left.
        for (int i = 0; i < PAGE_COUNT; i++) {
            s_nav[i] = nav_item(scr, i, 62, 132 + i * 28, 110);
        }
    }

    s_content = lv_obj_create(scr);
    lv_obj_remove_flag(s_content, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_size(s_content, L->cw, L->ch);
    lv_obj_set_pos(s_content, L->cx, L->cy);

    // The card's name plaque, between the two bottom crescents.
    s_title = theme_label(scr, "", FONT_DECO);
    lv_obj_align(s_title, LV_ALIGN_BOTTOM_MID, 0, L->portrait ? -92 : -72);

    s_keyboard = lv_keyboard_create(lv_layer_top());
    lv_obj_set_size(s_keyboard, L->w - 40, 230);
    lv_obj_align(s_keyboard, LV_ALIGN_BOTTOM_MID, 0, -10);
    lv_obj_add_event_cb(s_keyboard, keyboard_cb, LV_EVENT_READY, NULL);
    lv_obj_add_event_cb(s_keyboard, keyboard_cb, LV_EVENT_CANCEL, NULL);
    lv_obj_add_flag(s_keyboard, LV_OBJ_FLAG_HIDDEN);
}

void ui_init(void)
{
    theme_init(lv_display_get_default());
    L = display_rotation() == ROT_LANDSCAPE ? &kLandscape : &kPortrait;
    build_shell();
    ui_show(g_cfg.wifi_ssid[0] ? PAGE_HOME : PAGE_SETTINGS);
}

void ui_set_rotation(display_rotation_t rotation)
{
    display_set_rotation(rotation);
    L = rotation == ROT_LANDSCAPE ? &kLandscape : &kPortrait;
    build_shell();
    ui_show(s_page);
}

const ui_layout_t *ui_layout(void)
{
    return L;
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
        if (s_nav_mark[i]) {
            if (i == page) {
                lv_obj_remove_flag(s_nav_mark[i], LV_OBJ_FLAG_HIDDEN);
            } else {
                lv_obj_add_flag(s_nav_mark[i], LV_OBJ_FLAG_HIDDEN);
            }
        }
    }
    lv_label_set_text(s_title, kTitle[page]);
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
    // The keyboard covers the bottom 240 px; scroll the field's list up if it sits under it.
    lv_area_t box;
    lv_obj_get_coords(ta, &box);
    int32_t limit = L->h - 240 - 10;
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
    s_prompt = theme_box(lv_layer_top(), L->cw, 122);
    lv_obj_set_pos(s_prompt, L->cx, L->cy);
    lv_obj_set_user_data(s_prompt, (void *)done);
    theme_label(s_prompt, title, FONT_DECO_S);
    lv_obj_t *ta = lv_textarea_create(s_prompt);
    lv_textarea_set_one_line(ta, true);
    lv_textarea_set_max_length(ta, max_len);
    lv_textarea_set_placeholder_text(ta, placeholder);
    lv_obj_set_size(ta, L->cw - 20 - 96, 44);
    lv_obj_align(ta, LV_ALIGN_BOTTOM_LEFT, 0, 0);
    lv_obj_t *cancel = theme_button(s_prompt, "Cancel", prompt_cancel, NULL);
    lv_obj_align(cancel, LV_ALIGN_BOTTOM_RIGHT, 0, -4);
    ui_keyboard_open(ta, prompt_done, user_data);
}
