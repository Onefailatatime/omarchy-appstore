// Wi-Fi, Venice key and model, time zone, degrees, sleep timer, power.
#include <stdio.h>
#include <string.h>
#include "board.h"
#include "net.h"
#include "store.h"
#include "theme.h"
#include "ui.h"

static lv_obj_t *s_ssid, *s_pass, *s_key, *s_model, *s_net_status;

static void pull_fields(void)
{
    strncpy(g_cfg.wifi_ssid, lv_textarea_get_text(s_ssid), sizeof(g_cfg.wifi_ssid) - 1);
    strncpy(g_cfg.wifi_pass, lv_textarea_get_text(s_pass), sizeof(g_cfg.wifi_pass) - 1);
    strncpy(g_cfg.venice_key, lv_textarea_get_text(s_key), sizeof(g_cfg.venice_key) - 1);
    strncpy(g_cfg.venice_model, lv_textarea_get_text(s_model), sizeof(g_cfg.venice_model) - 1);
    store_save_config();
}

static void field_done(lv_obj_t *ta, void *user_data)
{
    pull_fields();
}

static void field_focus(lv_event_t *e)
{
    ui_keyboard_open(lv_event_get_target(e), field_done, NULL);
}

static void update_status(lv_timer_t *timer)
{
    const char *text;
    char buf[80];
    switch (net_state()) {
    case NET_CONNECTED:
        snprintf(buf, sizeof(buf), "Connected, %s%s", net_ip(), net_time_synced() ? ", clock set" : "");
        text = buf;
        break;
    case NET_CONNECTING: text = "Connecting..."; break;
    case NET_FAILED:     text = "Could not join. Check name and password."; break;
    default:             text = "Not configured."; break;
    }
    if (strcmp(lv_label_get_text(s_net_status), text) != 0) {
        lv_label_set_text(s_net_status, text);
    }
}

static void connect_cb(lv_event_t *e)
{
    pull_fields();
    net_connect();
    lv_label_set_text(s_net_status, "Connecting...");
}

static void tz_cb(lv_event_t *e)
{
    g_cfg.tz_index = lv_dropdown_get_selected(lv_event_get_target(e));
    store_save_config();
    net_apply_timezone();
}

static void units_cb(lv_event_t *e)
{
    g_cfg.fahrenheit = lv_dropdown_get_selected(lv_event_get_target(e)) == 0;
    store_save_config();
}

static const uint8_t kSleepMinutes[] = {0, 2, 5, 10, 30};

static void sleep_cb(lv_event_t *e)
{
    g_cfg.sleep_minutes = kSleepMinutes[lv_dropdown_get_selected(lv_event_get_target(e))];
    store_save_config();
}

static void off_cb(lv_event_t *e)
{
    store_save_data();
    display_sleep();
    board_power_off();
}

static void cleanup_cb(lv_event_t *e)
{
    lv_timer_delete(lv_event_get_user_data(e));
}

static lv_obj_t *field(lv_obj_t *parent, const char *label, const char *value, int max_len, int label_w)
{
    lv_obj_t *row = theme_row(parent, 38);
    lv_obj_t *l = theme_label(row, label, FONT_SMALL);
    lv_obj_align(l, LV_ALIGN_LEFT_MID, 0, 0);
    lv_obj_t *ta = lv_textarea_create(row);
    lv_textarea_set_one_line(ta, true);
    lv_textarea_set_max_length(ta, max_len);
    lv_textarea_set_text(ta, value);
    lv_obj_set_style_text_font(ta, FONT_SMALL, 0);
    lv_obj_set_size(ta, lv_obj_get_width(parent) - label_w - ui_layout()->inset, 32);
    lv_obj_align(ta, LV_ALIGN_LEFT_MID, label_w, 0);
    lv_obj_add_event_cb(ta, field_focus, LV_EVENT_CLICKED, NULL);
    return ta;
}

static lv_obj_t *choice(lv_obj_t *row, const char *label, int label_x, int x, int width,
                        const char *options, int selected, lv_event_cb_t cb)
{
    lv_obj_t *l = theme_label(row, label, FONT_SMALL);
    lv_obj_align(l, LV_ALIGN_LEFT_MID, label_x, 0);
    lv_obj_t *dd = lv_dropdown_create(row);
    lv_dropdown_set_options(dd, options);
    lv_dropdown_set_selected(dd, selected);
    lv_obj_set_size(dd, width, 32);
    lv_obj_align(dd, LV_ALIGN_LEFT_MID, x, 0);
    lv_obj_add_event_cb(dd, cb, LV_EVENT_VALUE_CHANGED, NULL);
    return dd;
}

void page_settings_build(lv_obj_t *parent)
{
    const ui_layout_t *L = ui_layout();
    const int label_w = L->portrait ? 80 : 110;
    const int left = L->portrait ? 30 : 0;   // clear of the portrait frame's lily
    lv_obj_t *col = theme_column(parent, L->cw - left, L->ch);
    lv_obj_set_pos(col, left, 0);
    lv_obj_remove_flag(col, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_style_pad_row(col, 2, 0);
    lv_obj_update_layout(col);

    s_ssid = field(col, L->portrait ? "Wi-Fi" : "Wi-Fi name", g_cfg.wifi_ssid, 32, label_w);
    s_pass = field(col, "Password", g_cfg.wifi_pass, 64, label_w);
    lv_obj_t *r = theme_row(col, 36);
    lv_obj_t *connect = theme_button(r, "Connect", connect_cb, NULL);
    lv_obj_set_style_pad_ver(connect, 4, 0);
    lv_obj_align(connect, LV_ALIGN_LEFT_MID, label_w, 0);
    if (L->portrait) {
        s_net_status = theme_label(theme_row(col, 24), "", FONT_SMALL);
        lv_obj_set_width(s_net_status, L->cw - left);
    } else {
        s_net_status = theme_label(r, "", FONT_SMALL);
        lv_obj_align(s_net_status, LV_ALIGN_LEFT_MID, label_w + 108, 0);
        lv_obj_set_width(s_net_status, L->cw - left - label_w - 108);
    }
    lv_label_set_long_mode(s_net_status, LV_LABEL_LONG_DOT);
    lv_timer_t *timer = lv_timer_create(update_status, 1000, NULL);
    update_status(timer);
    lv_obj_add_event_cb(col, cleanup_cb, LV_EVENT_DELETE, timer);   // col dies with the page

    s_key = field(col, L->portrait ? "Key" : "Venice key", g_cfg.venice_key, sizeof(g_cfg.venice_key) - 1, label_w);
    s_model = field(col, "Model", g_cfg.venice_model, sizeof(g_cfg.venice_model) - 1, label_w);

    char tz_options[400] = "";
    for (int i = 0; i < store_tz_count; i++) {
        strlcat(tz_options, store_tz_names[i], sizeof(tz_options));
        if (i < store_tz_count - 1) strlcat(tz_options, "\n", sizeof(tz_options));
    }
    int sleep_index = 2;
    for (int i = 0; i < 5; i++) {
        if (kSleepMinutes[i] == g_cfg.sleep_minutes) sleep_index = i;
    }
    const char *sleep_options = "Never\n2 min\n5 min\n10 min\n30 min";
    if (L->portrait) {
        choice(theme_row(col, 38), "Time zone", 0, label_w, L->cw - left - label_w, tz_options, g_cfg.tz_index, tz_cb);
        choice(theme_row(col, 38), "Degrees", 0, label_w, 90, "F\nC", g_cfg.fahrenheit ? 0 : 1, units_cb);
        choice(theme_row(col, 38), "Sleep", 0, label_w, 140, sleep_options, sleep_index, sleep_cb);
    } else {
        r = theme_row(col, 38);
        choice(r, "Time zone", 0, label_w, 150, tz_options, g_cfg.tz_index, tz_cb);
        choice(r, "Degrees", 272, 342, 64, "F\nC", g_cfg.fahrenheit ? 0 : 1, units_cb);
        choice(r, "Sleep", 418, 470, L->cw - 470, sleep_options, sleep_index, sleep_cb);
    }

    r = theme_row(col, 34);
    char about[96];
    int battery = board_battery_percent();
    if (battery >= 0) {
        snprintf(about, sizeof(about), L->portrait ? "Grove 1.1, battery %d%%" : "Grove 1.1   Battery %d%%   Sleeps on battery only", battery);
    } else {
        snprintf(about, sizeof(about), L->portrait ? "Grove 1.1" : "Grove 1.1   Sleeps on battery only");
    }
    lv_obj_t *l = theme_label(r, about, FONT_SMALL);
    lv_obj_align(l, LV_ALIGN_LEFT_MID, 0, 0);
    lv_obj_set_size(l, L->cw - left - 110, 20);
    lv_label_set_long_mode(l, LV_LABEL_LONG_DOT);
    lv_obj_t *off = theme_button(r, "Power off", off_cb, NULL);
    lv_obj_set_style_pad_ver(off, 4, 0);
    lv_obj_align(off, LV_ALIGN_RIGHT_MID, 0, 0);
}
