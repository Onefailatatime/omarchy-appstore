// Grove look: paper white, ink black, two greys, round corners, hand-cut shapes.
#pragma once
#include "lvgl.h"

#define FONT_SMALL (&lv_font_montserrat_16)
#define FONT_BODY  (&lv_font_montserrat_20)
#define FONT_TITLE (&lv_font_montserrat_28)
#define FONT_HERO  (&lv_font_montserrat_36)
#define FONT_CLOCK (&lv_font_montserrat_48)

#define COLOR_INK   lv_color_black()
#define COLOR_PAPER lv_color_white()
// Four-grey refreshes quantise to 0-63, 64-127, 128-191, 192-255; mono ones split at 128.
#define COLOR_SHADE lv_color_make(0x58, 0x58, 0x58)   // dark grey, reads black on mono pages
#define COLOR_MIST  lv_color_make(0xA0, 0xA0, 0xA0)   // light grey, reads white on mono pages

void theme_init(lv_display_t *disp);

lv_obj_t *theme_card(lv_obj_t *parent, int w, int h);
lv_obj_t *theme_button(lv_obj_t *parent, const char *text, lv_event_cb_t cb, void *user_data);
lv_obj_t *theme_label(lv_obj_t *parent, const char *text, const lv_font_t *font);
lv_obj_t *theme_title(lv_obj_t *parent, const char *text);   // page heading with a leaf mark
lv_obj_t *theme_column(lv_obj_t *parent, int w, int h);      // vertical flex list, scrollable
// Hills, clouds, a tree and a cottage across the bottom of `parent`.
void theme_scenery(lv_obj_t *parent, int y, int w, int h);
