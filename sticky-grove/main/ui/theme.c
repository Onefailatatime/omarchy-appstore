#include "theme.h"
#include "src/themes/lv_theme_private.h"

static lv_style_t st_card, st_btn, st_btn_checked, st_cb_box, st_cb_checked,
                  st_ta, st_ta_cursor, st_kb, st_kb_item, st_kb_item_checked, st_cal_item,
                  st_dd_list, st_plain;
static lv_theme_t s_theme;

static void apply_cb(lv_theme_t *th, lv_obj_t *obj)
{
    if (lv_obj_check_type(obj, &lv_label_class)) {
        return;   // labels inherit font and colour, so checked buttons can invert them
    }
    lv_obj_add_style(obj, &st_plain, 0);
    if (lv_obj_get_parent(obj) == NULL) {
        return;   // screens and layers: ui_init paints the active screen white
    }
    if (lv_obj_check_type(obj, &lv_button_class)) {
        lv_obj_add_style(obj, &st_btn, 0);
        lv_obj_add_style(obj, &st_btn_checked, LV_STATE_CHECKED);
    } else if (lv_obj_check_type(obj, &lv_checkbox_class)) {
        lv_obj_add_style(obj, &st_cb_box, LV_PART_INDICATOR);
        lv_obj_add_style(obj, &st_cb_checked, LV_PART_INDICATOR | LV_STATE_CHECKED);
        lv_obj_set_style_pad_column(obj, 12, 0);
    } else if (lv_obj_check_type(obj, &lv_textarea_class)) {
        lv_obj_add_style(obj, &st_ta, 0);
        lv_obj_add_style(obj, &st_ta_cursor, LV_PART_CURSOR | LV_STATE_FOCUSED);
        lv_obj_set_style_anim_duration(obj, 0, LV_PART_CURSOR);   // no blinking on e-paper
    } else if (lv_obj_check_type(obj, &lv_keyboard_class)) {
        lv_obj_add_style(obj, &st_kb, 0);
        lv_obj_add_style(obj, &st_kb_item, LV_PART_ITEMS);
        lv_obj_add_style(obj, &st_kb_item_checked, LV_PART_ITEMS | LV_STATE_CHECKED);
    } else if (lv_obj_check_type(obj, &lv_calendar_class)) {
        lv_obj_add_style(obj, &st_card, 0);
        lv_obj_set_style_pad_all(obj, 6, 0);
    } else if (lv_obj_check_type(obj, &lv_buttonmatrix_class)) {
        lv_obj_add_style(obj, &st_cal_item, LV_PART_ITEMS);
        lv_obj_set_style_text_color(obj, COLOR_SHADE, LV_PART_ITEMS | LV_STATE_DISABLED);
    } else if (lv_obj_check_type(obj, &lv_dropdown_class)) {
        lv_obj_add_style(obj, &st_btn, 0);
    } else if (lv_obj_check_type(obj, &lv_dropdownlist_class)) {
        lv_obj_add_style(obj, &st_dd_list, 0);
        lv_obj_set_style_bg_color(obj, COLOR_INK, LV_PART_SELECTED | LV_STATE_CHECKED);
        lv_obj_set_style_text_color(obj, COLOR_PAPER, LV_PART_SELECTED | LV_STATE_CHECKED);
    }
}

void theme_init(lv_display_t *disp)
{
    lv_style_init(&st_plain);
    lv_style_set_text_color(&st_plain, COLOR_INK);
    lv_style_set_text_font(&st_plain, FONT_BODY);
    lv_style_set_outline_width(&st_plain, 0);
    lv_style_set_anim_duration(&st_plain, 0);

    lv_style_init(&st_card);
    lv_style_set_bg_color(&st_card, COLOR_PAPER);
    lv_style_set_bg_opa(&st_card, LV_OPA_COVER);
    lv_style_set_border_color(&st_card, COLOR_INK);
    lv_style_set_border_width(&st_card, 2);
    lv_style_set_radius(&st_card, 18);
    lv_style_set_pad_all(&st_card, 14);

    lv_style_init(&st_btn);
    lv_style_set_bg_color(&st_btn, COLOR_PAPER);
    lv_style_set_bg_opa(&st_btn, LV_OPA_COVER);
    lv_style_set_border_color(&st_btn, COLOR_INK);
    lv_style_set_border_width(&st_btn, 2);
    lv_style_set_radius(&st_btn, 14);
    lv_style_set_pad_hor(&st_btn, 16);
    lv_style_set_pad_ver(&st_btn, 10);

    lv_style_init(&st_btn_checked);
    lv_style_set_bg_color(&st_btn_checked, COLOR_INK);
    lv_style_set_text_color(&st_btn_checked, COLOR_PAPER);

    lv_style_init(&st_cb_box);
    lv_style_set_bg_color(&st_cb_box, COLOR_PAPER);
    lv_style_set_bg_opa(&st_cb_box, LV_OPA_COVER);
    lv_style_set_border_color(&st_cb_box, COLOR_INK);
    lv_style_set_border_width(&st_cb_box, 2);
    lv_style_set_radius(&st_cb_box, 8);
    lv_style_set_pad_all(&st_cb_box, 5);

    lv_style_init(&st_cb_checked);
    lv_style_set_bg_color(&st_cb_checked, COLOR_INK);
    lv_style_set_bg_image_src(&st_cb_checked, LV_SYMBOL_OK);
    lv_style_set_text_color(&st_cb_checked, COLOR_PAPER);
    lv_style_set_text_font(&st_cb_checked, FONT_SMALL);

    lv_style_init(&st_ta);
    lv_style_set_bg_color(&st_ta, COLOR_PAPER);
    lv_style_set_bg_opa(&st_ta, LV_OPA_COVER);
    lv_style_set_border_color(&st_ta, COLOR_INK);
    lv_style_set_border_width(&st_ta, 2);
    lv_style_set_radius(&st_ta, 12);
    lv_style_set_pad_all(&st_ta, 10);

    lv_style_init(&st_ta_cursor);
    lv_style_set_border_color(&st_ta_cursor, COLOR_INK);
    lv_style_set_border_width(&st_ta_cursor, 2);
    lv_style_set_border_side(&st_ta_cursor, LV_BORDER_SIDE_LEFT);

    lv_style_init(&st_kb);
    lv_style_set_bg_color(&st_kb, COLOR_PAPER);
    lv_style_set_bg_opa(&st_kb, LV_OPA_COVER);
    lv_style_set_border_color(&st_kb, COLOR_INK);
    lv_style_set_border_width(&st_kb, 2);
    lv_style_set_border_side(&st_kb, LV_BORDER_SIDE_TOP);
    lv_style_set_pad_all(&st_kb, 6);
    lv_style_set_pad_gap(&st_kb, 6);

    lv_style_init(&st_kb_item);
    lv_style_set_bg_color(&st_kb_item, COLOR_PAPER);
    lv_style_set_bg_opa(&st_kb_item, LV_OPA_COVER);
    lv_style_set_border_color(&st_kb_item, COLOR_INK);
    lv_style_set_border_width(&st_kb_item, 1);
    lv_style_set_radius(&st_kb_item, 8);
    lv_style_set_text_font(&st_kb_item, FONT_BODY);

    lv_style_init(&st_kb_item_checked);
    lv_style_set_bg_color(&st_kb_item_checked, COLOR_MIST);

    lv_style_init(&st_cal_item);
    lv_style_set_bg_color(&st_cal_item, COLOR_PAPER);
    lv_style_set_bg_opa(&st_cal_item, LV_OPA_COVER);
    lv_style_set_border_color(&st_cal_item, COLOR_PAPER);
    lv_style_set_border_width(&st_cal_item, 2);
    lv_style_set_radius(&st_cal_item, 10);
    lv_style_set_text_font(&st_cal_item, FONT_SMALL);

    lv_style_init(&st_dd_list);
    lv_style_set_bg_color(&st_dd_list, COLOR_PAPER);
    lv_style_set_bg_opa(&st_dd_list, LV_OPA_COVER);
    lv_style_set_border_color(&st_dd_list, COLOR_INK);
    lv_style_set_border_width(&st_dd_list, 2);
    lv_style_set_radius(&st_dd_list, 12);
    lv_style_set_pad_all(&st_dd_list, 8);
    lv_style_set_text_font(&st_dd_list, FONT_BODY);
    lv_style_set_max_height(&st_dd_list, 300);

    lv_theme_set_apply_cb(&s_theme, apply_cb);
    lv_display_set_theme(disp, &s_theme);
}

lv_obj_t *theme_card(lv_obj_t *parent, int w, int h)
{
    lv_obj_t *card = lv_obj_create(parent);
    lv_obj_add_style(card, &st_card, 0);
    lv_obj_set_size(card, w, h);
    lv_obj_set_scrollbar_mode(card, LV_SCROLLBAR_MODE_OFF);
    lv_obj_remove_flag(card, LV_OBJ_FLAG_SCROLLABLE);
    return card;
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

lv_obj_t *theme_label(lv_obj_t *parent, const char *text, const lv_font_t *font)
{
    lv_obj_t *label = lv_label_create(parent);
    lv_label_set_text(label, text);
    lv_obj_set_style_text_font(label, font, 0);
    return label;
}

static lv_obj_t *circle(lv_obj_t *parent, int x, int y, int d, lv_color_t color)
{
    lv_obj_t *c = lv_obj_create(parent);
    lv_obj_remove_flag(c, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(c, d, d);
    lv_obj_set_pos(c, x, y);
    lv_obj_set_style_radius(c, LV_RADIUS_CIRCLE, 0);
    lv_obj_set_style_bg_color(c, color, 0);
    lv_obj_set_style_bg_opa(c, LV_OPA_COVER, 0);
    lv_obj_set_style_border_width(c, 0, 0);
    return c;
}

lv_obj_t *theme_title(lv_obj_t *parent, const char *text)
{
    lv_obj_t *row = lv_obj_create(parent);
    lv_obj_remove_flag(row, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(row, LV_SIZE_CONTENT, 40);
    lv_obj_t *leaf = circle(row, 2, 9, 20, COLOR_INK);
    lv_obj_set_style_radius(leaf, 8, 0);
    lv_obj_set_style_transform_pivot_x(leaf, 10, 0);
    lv_obj_set_style_transform_pivot_y(leaf, 10, 0);
    lv_obj_set_style_transform_rotation(leaf, 450, 0);
    lv_obj_t *label = theme_label(row, text, FONT_TITLE);
    lv_obj_set_pos(label, 34, 2);
    return row;
}

lv_obj_t *theme_column(lv_obj_t *parent, int w, int h)
{
    lv_obj_t *col = lv_obj_create(parent);
    lv_obj_set_size(col, w, h);
    lv_obj_set_flex_flow(col, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_style_pad_row(col, 8, 0);
    lv_obj_set_scrollbar_mode(col, LV_SCROLLBAR_MODE_OFF);
    lv_obj_set_scroll_dir(col, LV_DIR_VER);
    return col;
}

static void line(lv_obj_t *parent, lv_point_precise_t *pts, int n, int width, lv_color_t color)
{
    lv_obj_t *l = lv_line_create(parent);
    lv_line_set_points(l, pts, n);
    lv_obj_set_style_line_width(l, width, 0);
    lv_obj_set_style_line_color(l, color, 0);
    lv_obj_set_style_line_rounded(l, true, 0);
}

static void cloud(lv_obj_t *parent, int x, int y, int scale)
{
    circle(parent, x, y + scale / 2, scale, COLOR_MIST);
    circle(parent, x + scale / 2, y, scale + scale / 3, COLOR_MIST);
    circle(parent, x + scale + scale / 4, y + scale / 3, scale, COLOR_MIST);
    lv_obj_t *base = lv_obj_create(parent);
    lv_obj_remove_flag(base, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(base, scale * 2 + scale / 4, scale / 2);
    lv_obj_set_pos(base, x, y + scale);
    lv_obj_set_style_radius(base, scale / 4, 0);
    lv_obj_set_style_bg_color(base, COLOR_MIST, 0);
    lv_obj_set_style_bg_opa(base, LV_OPA_COVER, 0);
    lv_obj_set_style_border_width(base, 0, 0);
}

void theme_scenery(lv_obj_t *parent, int y, int w, int h)
{
    lv_obj_t *land = lv_obj_create(parent);
    lv_obj_remove_flag(land, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(land, w, h);
    lv_obj_set_pos(land, 0, y);
    lv_obj_set_style_pad_all(land, 0, 0);
    lv_obj_set_style_border_width(land, 0, 0);
    lv_obj_set_style_bg_opa(land, LV_OPA_TRANSP, 0);

    cloud(land, 40, 4, 22);
    cloud(land, w - 170, 10, 16);

    // Rolling hills: large circles pushed below the ground line.
    circle(land, -120, h - 70, 460, COLOR_MIST);
    circle(land, w - 360, h - 58, 520, COLOR_MIST);
    circle(land, w / 2 - 180, h - 40, 380, COLOR_SHADE);

    // Cottage on the middle hill.
    int hx = w / 2 - 40, hy = h - 62;
    lv_obj_t *house = lv_obj_create(land);
    lv_obj_remove_flag(house, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(house, 44, 34);
    lv_obj_set_pos(house, hx, hy);
    lv_obj_set_style_bg_color(house, COLOR_PAPER, 0);
    lv_obj_set_style_bg_opa(house, LV_OPA_COVER, 0);
    lv_obj_set_style_border_color(house, COLOR_INK, 0);
    lv_obj_set_style_border_width(house, 2, 0);
    lv_obj_set_style_radius(house, 4, 0);
    static lv_point_precise_t roof[3];
    roof[0] = (lv_point_precise_t){hx - 6, hy + 2};
    roof[1] = (lv_point_precise_t){hx + 22, hy - 18};
    roof[2] = (lv_point_precise_t){hx + 50, hy + 2};
    line(land, roof, 3, 3, COLOR_INK);
    lv_obj_t *door = lv_obj_create(land);
    lv_obj_remove_flag(door, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(door, 10, 16);
    lv_obj_set_pos(door, hx + 17, hy + 18);
    lv_obj_set_style_bg_color(door, COLOR_INK, 0);
    lv_obj_set_style_bg_opa(door, LV_OPA_COVER, 0);
    lv_obj_set_style_border_width(door, 0, 0);
    lv_obj_set_style_radius(door, 4, 0);

    // A round tree to the left and a sapling to the right.
    lv_obj_t *trunk = lv_obj_create(land);
    lv_obj_remove_flag(trunk, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(trunk, 8, 40);
    lv_obj_set_pos(trunk, 96, h - 60);
    lv_obj_set_style_bg_color(trunk, COLOR_INK, 0);
    lv_obj_set_style_bg_opa(trunk, LV_OPA_COVER, 0);
    lv_obj_set_style_border_width(trunk, 0, 0);
    circle(land, 70, h - 110, 60, COLOR_SHADE);
    circle(land, 60, h - 86, 40, COLOR_SHADE);
    circle(land, 104, h - 90, 44, COLOR_SHADE);
    circle(land, w - 90, h - 54, 26, COLOR_INK);
    lv_obj_t *stem = lv_obj_create(land);
    lv_obj_remove_flag(stem, LV_OBJ_FLAG_SCROLLABLE | LV_OBJ_FLAG_CLICKABLE);
    lv_obj_set_size(stem, 4, 22);
    lv_obj_set_pos(stem, w - 79, h - 34);
    lv_obj_set_style_bg_color(stem, COLOR_INK, 0);
    lv_obj_set_style_bg_opa(stem, LV_OPA_COVER, 0);
    lv_obj_set_style_border_width(stem, 0, 0);

    // Grass tufts and two birds.
    static lv_point_precise_t grass[6][3];
    const int gx[6] = {30, 180, 250, 420, 520, 600};
    for (int i = 0; i < 6; i++) {
        grass[i][0] = (lv_point_precise_t){gx[i], h - 6};
        grass[i][1] = (lv_point_precise_t){gx[i] + 5, h - 18};
        grass[i][2] = (lv_point_precise_t){gx[i] + 10, h - 6};
        line(land, grass[i], 3, 2, COLOR_INK);
    }
    static lv_point_precise_t birds[2][3];
    const int bx[2] = {w / 2 + 120, w / 2 + 150};
    for (int i = 0; i < 2; i++) {
        birds[i][0] = (lv_point_precise_t){bx[i], 20 + i * 8};
        birds[i][1] = (lv_point_precise_t){bx[i] + 7, 14 + i * 8};
        birds[i][2] = (lv_point_precise_t){bx[i] + 14, 20 + i * 8};
        line(land, birds[i], 3, 2, COLOR_INK);
    }
}
