// One pinned note. It shows on the dashboard.
#include <string.h>
#include "store.h"
#include "theme.h"
#include "ui.h"

static lv_obj_t *s_ta, *s_status;

static void save(void)
{
    strncpy(g_data.note, lv_textarea_get_text(s_ta), NOTE_TEXT - 1);
    g_data.note[NOTE_TEXT - 1] = '\0';
    store_save_data();
    lv_label_set_text(s_status, "Saved. It is pinned on Home.");
}

static void done(lv_obj_t *ta, void *user_data) { save(); }
static void save_cb(lv_event_t *e)              { save(); }

static void clear_cb(lv_event_t *e)
{
    lv_textarea_set_text(s_ta, "");
    save();
    lv_label_set_text(s_status, "Cleared.");
}

static void focus_cb(lv_event_t *e)
{
    ui_keyboard_open(s_ta, done, NULL);
}

void page_note_build(lv_obj_t *parent)
{
    const ui_layout_t *L = ui_layout();
    lv_obj_t *save_btn = theme_button(parent, "Save", save_cb, NULL);
    lv_obj_align(save_btn, LV_ALIGN_TOP_RIGHT, -L->inset, 0);
    lv_obj_t *clear = theme_button(parent, "Clear", clear_cb, NULL);
    lv_obj_align_to(clear, save_btn, LV_ALIGN_OUT_LEFT_MID, -8, 0);
    lv_obj_t *rose = theme_image(parent, &asset_rose);
    lv_obj_set_pos(rose, 0, -8);

    s_ta = lv_textarea_create(parent);
    lv_obj_set_size(s_ta, L->cw, L->portrait ? 300 : 170);
    lv_obj_set_pos(s_ta, 0, 44);
    lv_textarea_set_max_length(s_ta, NOTE_TEXT - 1);
    lv_textarea_set_placeholder_text(s_ta, "Tap here and write something kind to future you.");
    lv_textarea_set_text(s_ta, g_data.note);
    lv_obj_add_event_cb(s_ta, focus_cb, LV_EVENT_CLICKED, NULL);

    s_status = theme_label(parent, "Tap the note to edit. The tick key saves.", FONT_SMALL);
    lv_obj_set_pos(s_status, 0, L->portrait ? 352 : 222);
}
