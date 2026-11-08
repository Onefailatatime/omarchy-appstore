// Tarot card look: ink on paper, hairline rules, Art Nouveau lettering and ornaments.
#pragma once
#include "assets.h"
#include "lvgl.h"

LV_FONT_DECLARE(eagle_22)
LV_FONT_DECLARE(eagle_30)
LV_FONT_DECLARE(eagle_40)

#define FONT_SMALL  (&lv_font_montserrat_16)
#define FONT_BODY   (&lv_font_montserrat_18)
#define FONT_BIG    (&lv_font_montserrat_28)
#define FONT_DECO_S (&eagle_22)   // navigation, small headings
#define FONT_DECO   (&eagle_30)   // card titles
#define FONT_DECO_L (&eagle_40)   // the clock

#define COLOR_INK   lv_color_black()
#define COLOR_PAPER lv_color_white()
// Four-grey refreshes quantise to 0-63, 64-127, 128-191, 192-255; mono ones split at 128.
#define COLOR_SHADE lv_color_make(0x58, 0x58, 0x58)   // dark grey, reads black on mono pages
#define COLOR_MIST  lv_color_make(0xA0, 0xA0, 0xA0)   // light grey, reads white on mono pages

void theme_init(lv_display_t *disp);

lv_obj_t *theme_label(lv_obj_t *parent, const char *text, const lv_font_t *font);
lv_obj_t *theme_button(lv_obj_t *parent, const char *text, lv_event_cb_t cb, void *user_data);
lv_obj_t *theme_image(lv_obj_t *parent, const lv_image_dsc_t *src);   // ink-coloured artwork
lv_obj_t *theme_rule(lv_obj_t *parent, int x, int y, int w);          // one-pixel hairline
lv_obj_t *theme_row(lv_obj_t *parent, int h);                         // invisible full-width row
lv_obj_t *theme_column(lv_obj_t *parent, int w, int h);               // vertical list, scrollable
lv_obj_t *theme_box(lv_obj_t *parent, int w, int h);                  // hairline-bordered panel
