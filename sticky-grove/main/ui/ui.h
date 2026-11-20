// Screen shell: an Art Nouveau frame, page navigation, the page title in the
// card's name plaque, one page in the content area, and a shared keyboard.
// Landscape puts the navigation in a column on the left; portrait puts it in
// two rows under the content.
#pragma once

#include "board.h"
#include "display.h"
#include "lvgl.h"

typedef struct {
    bool portrait;
    int w, h;            // screen
    int cx, cy, cw, ch;  // content area inside the frame
    int inset;           // keep top-right buttons this far from the corner lily
} ui_layout_t;

typedef enum {
    PAGE_HOME, PAGE_TODO, PAGE_HABITS, PAGE_CALENDAR, PAGE_NOTE, PAGE_CHAT, PAGE_SETTINGS, PAGE_COUNT
} ui_page_t;

typedef void (*ui_keyboard_done_cb)(lv_obj_t *textarea, void *user_data);

void ui_init(void);
void ui_set_rotation(display_rotation_t rotation);   // rebuilds the shell and current page
const ui_layout_t *ui_layout(void);
void ui_show(ui_page_t page);
ui_page_t ui_current(void);
void ui_handle_button(board_button_t button);
void ui_minute_tick(void);
// Shows the keyboard for `ta`; `done` runs when the tick key is pressed.
void ui_keyboard_open(lv_obj_t *ta, ui_keyboard_done_cb done, void *user_data);
void ui_keyboard_close(void);
// Small popup used to add a line of text (new to-do, habit, event).
void ui_prompt(const char *title, const char *placeholder, int max_len, ui_keyboard_done_cb done, void *user_data);

// Page builders, one per file. Each draws into a blank content container.
void page_home_build(lv_obj_t *parent);
void page_home_minute(void);
void page_todo_build(lv_obj_t *parent);
void page_habits_build(lv_obj_t *parent);
void page_calendar_build(lv_obj_t *parent);
void page_note_build(lv_obj_t *parent);
void page_chat_build(lv_obj_t *parent);
void page_settings_build(lv_obj_t *parent);
