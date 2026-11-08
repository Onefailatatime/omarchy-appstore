// Month view on the left, the chosen day's events on the right.
#include <time.h>
#include "store.h"
#include "theme.h"
#include "ui.h"

// Button-matrix control bits the calendar sets on today and on highlighted dates.
#define LV_CALENDAR_CTRL_TODAY     LV_BUTTONMATRIX_CTRL_CUSTOM_1
#define LV_CALENDAR_CTRL_HIGHLIGHT LV_BUTTONMATRIX_CTRL_CUSTOM_2

static lv_obj_t *s_calendar;
static lv_obj_t *s_day_title;
static lv_obj_t *s_events;
static lv_calendar_date_t s_selected;
static lv_calendar_date_t s_marks[EVENT_MAX];

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
        border->width = picked ? 3 : 2;
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
        lv_obj_t *row = lv_obj_create(s_events);
        lv_obj_remove_flag(row, LV_OBJ_FLAG_SCROLLABLE);
        lv_obj_set_size(row, LV_PCT(100), 44);
        lv_obj_t *text = theme_label(row, g_data.events[idx[i]].text, FONT_SMALL);
        lv_obj_set_width(text, 156);
        lv_label_set_long_mode(text, LV_LABEL_LONG_WRAP);
        lv_obj_align(text, LV_ALIGN_LEFT_MID, 0, 0);
        lv_obj_t *del = theme_button(row, LV_SYMBOL_CLOSE, delete_cb, (void *)(intptr_t)idx[i]);
        lv_obj_set_size(del, 40, 36);
        lv_obj_set_style_pad_all(del, 2, 0);
        lv_obj_set_style_text_font(del, FONT_SMALL, 0);
        lv_obj_align(del, LV_ALIGN_RIGHT_MID, 0, 0);
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
    time_t now = time(NULL);
    struct tm t;
    localtime_r(&now, &t);
    s_selected.year = t.tm_year + 1900;
    s_selected.month = t.tm_mon + 1;
    s_selected.day = t.tm_mday;

    s_calendar = lv_calendar_create(parent);
    lv_obj_set_size(s_calendar, 410, UI_CONTENT_H - 32);
    lv_obj_set_pos(s_calendar, 0, 0);
    lv_calendar_set_today_date(s_calendar, s_selected.year, s_selected.month, s_selected.day);
    lv_calendar_set_showed_date(s_calendar, s_selected.year, s_selected.month);
    lv_obj_t *header = lv_calendar_header_arrow_create(s_calendar);
    lv_obj_set_style_text_font(header, FONT_BODY, 0);
    lv_obj_add_event_cb(s_calendar, day_pressed, LV_EVENT_VALUE_CHANGED, NULL);
    lv_obj_add_event_cb(lv_calendar_get_btnmatrix(s_calendar), draw_day, LV_EVENT_DRAW_TASK_ADDED, NULL);
    mark_dates();

    lv_obj_t *pane = theme_card(parent, UI_CONTENT_W - 32 - 424, UI_CONTENT_H - 32);
    lv_obj_set_pos(pane, 424, 0);
    s_day_title = theme_label(pane, "", FONT_TITLE);
    lv_obj_t *add = theme_button(pane, LV_SYMBOL_PLUS, add_cb, NULL);
    lv_obj_set_size(add, 48, 44);
    lv_obj_set_style_pad_all(add, 4, 0);
    lv_obj_align(add, LV_ALIGN_TOP_RIGHT, 0, -4);
    s_events = theme_column(pane, LV_PCT(100), UI_CONTENT_H - 32 - 28 - 60);
    lv_obj_set_pos(s_events, 0, 52);
    lv_obj_set_style_pad_all(s_events, 0, 0);
    show_day();
}
