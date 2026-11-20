// Month view with the chosen day's events beside it (landscape) or under it (portrait).
#include <time.h>
#include "store.h"
#include "theme.h"
#include "ui.h"

// Button-matrix control bits the calendar sets on today and on highlighted dates.
#define LV_CALENDAR_CTRL_TODAY     LV_BUTTONMATRIX_CTRL_CUSTOM_1
#define LV_CALENDAR_CTRL_HIGHLIGHT LV_BUTTONMATRIX_CTRL_CUSTOM_2

static lv_obj_t *s_calendar, *s_day_title, *s_events;
static lv_calendar_date_t s_selected;
static lv_calendar_date_t s_marks[EVENT_MAX];
static int s_pane_w;

static const char *const kMonths[] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};

static void mark_dates(void)
{
    for (int i = 0; i < g_data.event_count; i++) {
        s_marks[i].year = g_data.events[i].year;
        s_marks[i].month = g_data.events[i].month;
        s_marks[i].day = g_data.events[i].day;
    }
    lv_calendar_set_highlighted_dates(s_calendar, s_marks, g_data.event_count);
}

// Paint today solid ink, event days with an ink ring, the tapped day with a thick ring.
static void draw_day(lv_event_t *e)
{
    lv_obj_t *btnm = lv_event_get_current_target(e);
    lv_draw_task_t *task = lv_event_get_param(e);
    lv_draw_dsc_base_t *base = lv_draw_task_get_draw_dsc(task);
    if (base->part != LV_PART_ITEMS || base->id1 < 7 ||
        lv_buttonmatrix_has_button_ctrl(btnm, base->id1, LV_BUTTONMATRIX_CTRL_DISABLED)) {
        return;
    }
    bool today = lv_buttonmatrix_has_button_ctrl(btnm, base->id1, LV_CALENDAR_CTRL_TODAY);
    bool marked = lv_buttonmatrix_has_button_ctrl(btnm, base->id1, LV_CALENDAR_CTRL_HIGHLIGHT);
    bool picked = lv_buttonmatrix_get_selected_button(btnm) == (uint32_t)base->id1;
    lv_draw_fill_dsc_t *fill = lv_draw_task_get_fill_dsc(task);
    lv_draw_border_dsc_t *border = lv_draw_task_get_border_dsc(task);
    lv_draw_label_dsc_t *label = lv_draw_task_get_label_dsc(task);
    if (fill) {
        fill->color = today ? COLOR_INK : COLOR_PAPER;
        fill->opa = LV_OPA_COVER;
    }
    if (border) {
        border->color = (marked || picked) ? COLOR_INK : COLOR_PAPER;
        border->opa = LV_OPA_COVER;
        border->width = picked ? 2 : 1;
    }
    if (label && today) {
        label->color = COLOR_PAPER;
    }
}

static void show_day(void);

static void delete_cb(lv_event_t *e)
{
    event_remove((int)(intptr_t)lv_event_get_user_data(e));
    store_save_data();
    mark_dates();
    show_day();
}

static void added(lv_obj_t *ta, void *user_data)
{
    if (event_add(s_selected.year, s_selected.month, s_selected.day, lv_textarea_get_text(ta))) {
        store_save_data();
        mark_dates();
        show_day();
    }
}

static void add_cb(lv_event_t *e)
{
    ui_prompt("New event", "What is happening?", EVENT_TEXT - 1, added, NULL);
}

static void show_day(void)
{
    lv_label_set_text_fmt(s_day_title, "%s %d", kMonths[s_selected.month - 1], s_selected.day);
    lv_obj_clean(s_events);
    int idx[EVENT_MAX];
    int n = event_find(s_selected.year, s_selected.month, s_selected.day, idx, EVENT_MAX);
    for (int i = 0; i < n; i++) {
        lv_obj_t *row = theme_row(s_events, 36);
        lv_obj_t *text = theme_label(row, g_data.events[idx[i]].text, FONT_SMALL);
        lv_obj_set_size(text, s_pane_w - 44, 20);
        lv_label_set_long_mode(text, LV_LABEL_LONG_DOT);
        lv_obj_align(text, LV_ALIGN_LEFT_MID, 0, 0);
        lv_obj_t *del = theme_button(row, LV_SYMBOL_CLOSE, delete_cb, (void *)(intptr_t)idx[i]);
        lv_obj_set_size(del, 36, 28);
        lv_obj_set_style_pad_all(del, 2, 0);
        lv_obj_set_style_text_font(del, &lv_font_montserrat_14, 0);
        lv_obj_align(del, LV_ALIGN_RIGHT_MID, 0, 0);
        theme_rule(row, 0, 35, s_pane_w);
    }
    if (n == 0) {
        theme_label(s_events, "Nothing planned.", FONT_SMALL);
    }
}

static void day_pressed(lv_event_t *e)
{
    lv_calendar_date_t d;
    if (lv_calendar_get_pressed_date(s_calendar, &d)) {
        s_selected = d;
        show_day();
    }
}

void page_calendar_build(lv_obj_t *parent)
{
    const ui_layout_t *L = ui_layout();
    time_t now = time(NULL);
    struct tm t;
    localtime_r(&now, &t);
    s_selected.year = t.tm_year + 1900;
    s_selected.month = t.tm_mon + 1;
    s_selected.day = t.tm_mday;

    int cal_w = L->portrait ? L->cw : 330;
    int cal_h = L->portrait ? 290 : L->ch;
    s_calendar = lv_calendar_create(parent);
    lv_obj_set_size(s_calendar, cal_w, cal_h);
    lv_obj_set_pos(s_calendar, 0, 0);
    lv_calendar_set_today_date(s_calendar, s_selected.year, s_selected.month, s_selected.day);
    lv_calendar_set_showed_date(s_calendar, s_selected.year, s_selected.month);
    lv_obj_t *header = lv_calendar_header_arrow_create(s_calendar);
    lv_obj_set_style_text_font(header, FONT_DECO_S, 0);
    lv_obj_add_event_cb(s_calendar, day_pressed, LV_EVENT_VALUE_CHANGED, NULL);
    lv_obj_add_event_cb(lv_calendar_get_btnmatrix(s_calendar), draw_day, LV_EVENT_DRAW_TASK_ADDED, NULL);
    mark_dates();

    int px = L->portrait ? 0 : cal_w + 16;
    int py = L->portrait ? cal_h + 8 : 0;
    s_pane_w = L->portrait ? L->cw : L->cw - px;
    int pane_h = L->portrait ? L->ch - py : L->ch;
    theme_rule(parent, px, py + 36, s_pane_w);
    s_day_title = theme_label(parent, "", FONT_DECO_S);
    lv_obj_set_pos(s_day_title, px, py + 4);
    lv_obj_t *add = theme_button(parent, LV_SYMBOL_PLUS "  Add", add_cb, NULL);
    lv_obj_set_size(add, 80, 30);
    lv_obj_set_style_pad_all(add, 3, 0);
    lv_obj_set_pos(add, px + s_pane_w - 80 - (L->portrait ? 0 : L->inset), py);
    s_events = theme_column(parent, s_pane_w, pane_h - 44);
    lv_obj_set_pos(s_events, px, py + 44);
    show_day();
}
