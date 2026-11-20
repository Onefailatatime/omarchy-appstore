#include "theme.h"
#include "src/themes/lv_theme_private.h"

static lv_style_t st_plain, st_btn, st_btn_checked, st_cb_box, st_cb_checked, st_ta, st_ta_cursor,
                  st_kb, st_kb_item, st_kb_item_checked, st_cal_item, st_dd_list, st_box;
static lv_theme_t s_theme;

static void apply_cb(lv_theme_t *th, lv_obj_t *obj)
{
    if (lv_obj_check_type(obj, &lv_label_class) || lv_obj_check_type(obj, &lv_image_class)) {
        return;   // labels inherit font and colour, so checked buttons can invert them
    }
    lv_obj_add_style(obj, &st_plain, 0);
    if (lv_obj_get_parent(obj) == NULL) {
        return;   // screens and layers: ui paints the active screen white
    }
    if (lv_obj_check_type(obj, &lv_button_class)) {
        lv_obj_add_style(obj, &st_btn, 0);
        lv_obj_add_style(obj, &st_btn_checked, LV_STATE_CHECKED);
    } else if (lv_obj_check_type(obj, &lv_checkbox_class)) {
        lv_obj_add_style(obj, &st_cb_box, LV_PART_INDICATOR);
        lv_obj_add_style(obj, &st_cb_checked, LV_PART_INDICATOR | LV_STATE_CHECKED);
        lv_obj_set_style_pad_column(obj, 10, 0);
        lv_obj_set_style_text_font(obj, FONT_SMALL, 0);
    } else if (lv_obj_check_type(obj, &lv_textarea_class)) {
        lv_obj_add_style(obj, &st_ta, 0);
        lv_obj_add_style(obj, &st_ta_cursor, LV_PART_CURSOR | LV_STATE_FOCUSED);
        lv_obj_set_style_anim_duration(obj, 0, LV_PART_CURSOR);   // no blinking on e-paper
    } else if (lv_obj_check_type(obj, &lv_keyboard_class)) {
        lv_obj_add_style(obj, &st_kb, 0);
        lv_obj_add_style(obj, &st_kb_item, LV_PART_ITEMS);
        lv_obj_add_style(obj, &st_kb_item_checked, LV_PART_ITEMS | LV_STATE_CHECKED);
    } else if (lv_obj_check_type(obj, &lv_buttonmatrix_class)) {
        lv_obj_add_style(obj, &st_cal_item, LV_PART_ITEMS);
        lv_obj_set_style_text_color(obj, COLOR_SHADE, LV_PART_ITEMS | LV_STATE_DISABLED);
    } else if (lv_obj_check_type(obj, &lv_dropdown_class)) {
        lv_obj_add_style(obj, &st_btn, 0);
        lv_obj_set_style_radius(obj, 6, 0);
        lv_obj_set_style_text_font(obj, FONT_SMALL, 0);
    } else if (lv_obj_check_type(obj, &lv_dropdownlist_class)) {
        lv_obj_add_style(obj, &st_dd_list, 0);
        lv_obj_set_style_bg_color(obj, COLOR_INK, LV_PART_SELECTED | LV_STATE_CHECKED);
        lv_obj_set_style_text_color(obj, COLOR_PAPER, LV_PART_SELECTED | LV_STATE_CHECKED);
    }
}

static void outline(lv_style_t *st, int radius)
{
    lv_style_init(st);
    lv_style_set_bg_color(st, COLOR_PAPER);
    lv_style_set_bg_opa(st, LV_OPA_COVER);
    lv_style_set_border_color(st, COLOR_INK);
    lv_style_set_border_width(st, 1);
    lv_style_set_radius(st, radius);
}

void theme_init(lv_display_t *disp)
{
    lv_style_init(&st_plain);
    lv_style_set_text_color(&st_plain, COLOR_INK);
    lv_style_set_text_font(&st_plain, FONT_BODY);
    lv_style_set_bg_opa(&st_plain, LV_OPA_TRANSP);
    lv_style_set_border_width(&st_plain, 0);
    lv_style_set_outline_width(&st_plain, 0);
    lv_style_set_pad_all(&st_plain, 0);
    lv_style_set_anim_duration(&st_plain, 0);

    outline(&st_btn, 20);
    lv_style_set_pad_hor(&st_btn, 14);
    lv_style_set_pad_ver(&st_btn, 7);
    lv_style_set_text_font(&st_btn, FONT_SMALL);

    lv_style_init(&st_btn_checked);
    lv_style_set_bg_color(&st_btn_checked, COLOR_INK);
    lv_style_set_text_color(&st_btn_checked, COLOR_PAPER);

    outline(&st_cb_box, 5);
    lv_style_set_pad_all(&st_cb_box, 3);

    lv_style_init(&st_cb_checked);
    lv_style_set_bg_color(&st_cb_checked, COLOR_INK);
    lv_style_set_bg_image_src(&st_cb_checked, LV_SYMBOL_OK);
    lv_style_set_text_color(&st_cb_checked, COLOR_PAPER);
    lv_style_set_text_font(&st_cb_checked, &lv_font_montserrat_14);

    outline(&st_ta, 6);
    lv_style_set_pad_all(&st_ta, 8);
    lv_style_set_text_font(&st_ta, FONT_BODY);

    lv_style_init(&st_ta_cursor);
    lv_style_set_border_color(&st_ta_cursor, COLOR_INK);
    lv_style_set_border_width(&st_ta_cursor, 2);
    lv_style_set_border_side(&st_ta_cursor, LV_BORDER_SIDE_LEFT);

    outline(&st_kb, 0);
    lv_style_set_border_side(&st_kb, LV_BORDER_SIDE_TOP);
    lv_style_set_pad_all(&st_kb, 6);
    lv_style_set_pad_gap(&st_kb, 6);

    outline(&st_kb_item, 8);
    lv_style_set_text_font(&st_kb_item, FONT_BODY);

    lv_style_init(&st_kb_item_checked);
    lv_style_set_bg_color(&st_kb_item_checked, COLOR_MIST);

    // Calendar days: white on white, the page's draw hook recolours today and event days.
    outline(&st_cal_item, 8);
    lv_style_set_border_color(&st_cal_item, COLOR_PAPER);
    lv_style_set_text_font(&st_cal_item, FONT_SMALL);

    outline(&st_dd_list, 6);
    lv_style_set_pad_all(&st_dd_list, 8);
    lv_style_set_text_font(&st_dd_list, FONT_SMALL);
    lv_style_set_max_height(&st_dd_list, 260);

    outline(&st_box, 4);
    lv_style_set_pad_all(&st_box, 10);

    lv_theme_set_apply_cb(&s_theme, apply_cb);
    lv_display_set_theme(disp, &s_theme);
}

lv_obj_t *theme_label(lv_obj_t *parent, const char *text, const lv_font_t *font)
{
    lv_obj_t *label = lv_label_create(parent);
    lv_label_set_text(label, text);
    lv_obj_set_style_text_font(label, font, 0);
    return label;
}

lv_obj_t *theme_button(lv_obj_t *parent, const char *text, lv_event_cb_t cb, void *user_data)
{
    lv_obj_t *btn = lv_button_create(parent);
    lv_obj_t *label = lv_label_create(btn);
    lv_label_set_text(label, text);
    lv_obj_center(label);
    if (cb) {
        lv_obj_add_event_cb(btn, cb, LV_EVENT_CLICKED, user_data);
    }
    return btn;
}

lv_obj_t *theme_image(lv_obj_t *parent, const lv_image_dsc_t *src)
{
    lv_obj_t *img = lv_image_create(parent);
    lv_image_set_src(img, src);
    lv_obj_remove_flag(img, LV_OBJ_FLAG_CLICKABLE);
    if (src->header.cf == LV_COLOR_FORMAT_A8) {
        lv_obj_set_style_image_recolor(img, COLOR_INK, 0);
        lv_obj_set_style_image_recolor_opa(img, LV_OPA_COVER, 0);
    }
    return img;
}

lv_obj_t *theme_rule(lv_obj_t *parent, int x, int y, int w)
{
    lv_obj_t *rule = lv_obj_create(parent);
    lv_obj_remove_flag(rule, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(rule, w, 1);
    lv_obj_set_pos(rule, x, y);
    lv_obj_set_style_bg_color(rule, COLOR_INK, 0);
    lv_obj_set_style_bg_opa(rule, LV_OPA_COVER, 0);
    return rule;
}

lv_obj_t *theme_row(lv_obj_t *parent, int h)
{
    lv_obj_t *row = lv_obj_create(parent);
    lv_obj_remove_flag(row, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_size(row, LV_PCT(100), h);
    return row;
}

lv_obj_t *theme_column(lv_obj_t *parent, int w, int h)
{
    lv_obj_t *col = lv_obj_create(parent);
    lv_obj_set_size(col, w, h);
    lv_obj_set_flex_flow(col, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_scrollbar_mode(col, LV_SCROLLBAR_MODE_OFF);
    lv_obj_set_scroll_dir(col, LV_DIR_VER);
    return col;
}

lv_obj_t *theme_box(lv_obj_t *parent, int w, int h)
{
    lv_obj_t *box = lv_obj_create(parent);
    lv_obj_add_style(box, &st_box, 0);
    lv_obj_remove_flag(box, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_scrollbar_mode(box, LV_SCROLLBAR_MODE_OFF);
    lv_obj_set_size(box, w, h);
    return box;
}
