// Ask Venice AI. The device's own lists ride along as context, and bullet
// answers can be dropped straight into the to-do list.
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "net.h"
#include "store.h"
#include "theme.h"
#include "ui.h"
#include "venice.h"

static lv_obj_t *s_input, *s_question, *s_answer, *s_status, *s_save_btn;
static lv_timer_t *s_poll;
static char s_reply[VENICE_REPLY_MAX];

static void build_context(char *out, size_t len)
{
    time_t now = time(NULL);
    struct tm t;
    localtime_r(&now, &t);
    char date[48];
    strftime(date, sizeof(date), "%A %B %d, %Y, %H:%M", &t);
    int n = snprintf(out, len,
        "You are Grove, a warm and brief helper living on a small e-paper display on the owner's wall. "
        "Reply in plain text under 80 words. No markdown headings, no emoji. "
        "When you list tasks, put each on its own line starting with '- '. "
        "The owner is building a business and wants her first five paying clients.\n"
        "Now: %s\nOpen to-dos:\n", date);
    for (int i = 0; i < g_data.todo_count && n < (int)len - 80; i++) {
        if (!g_data.todos[i].done) {
            n += snprintf(out + n, len - n, "- %s\n", g_data.todos[i].text);
        }
    }
    uint32_t today = day_index_tm(&t);
    n += snprintf(out + n, len - n, "Habits (streak, done today):\n");
    for (int i = 0; i < g_data.habit_count && n < (int)len - 80; i++) {
        n += snprintf(out + n, len - n, "- %s (%d, %s)\n", g_data.habits[i].name,
                      habit_streak(&g_data.habits[i], today),
                      habit_done_on(&g_data.habits[i], today) ? "yes" : "no");
    }
    if (g_data.note[0] && n < (int)len - 80) {
        snprintf(out + n, len - n, "Pinned note: %.200s\n", g_data.note);
    }
}

static int count_bullets(const char *text)
{
    int n = 0;
    for (const char *p = text; p && *p; p = strchr(p, '\n')) {
        if (*p == '\n') p++;
        if (p[0] == '-' && p[1] == ' ') n++;
    }
    return n;
}

static void save_bullets_cb(lv_event_t *e)
{
    int added = 0;
    for (const char *p = s_reply; p && *p; p = strchr(p, '\n')) {
        if (*p == '\n') p++;
        if (p[0] == '-' && p[1] == ' ') {
            char item[TODO_TEXT];
            const char *end = strchr(p, '\n');
            size_t n = end ? (size_t)(end - p - 2) : strlen(p + 2);
            if (n >= sizeof(item)) n = sizeof(item) - 1;
            memcpy(item, p + 2, n);
            item[n] = '\0';
            if (todo_add(item)) added++;
        }
    }
    store_save_data();
    lv_label_set_text_fmt(s_status, "Added %d to-do%s.", added, added == 1 ? "" : "s");
    lv_obj_add_flag(s_save_btn, LV_OBJ_FLAG_HIDDEN);
}

static void poll_cb(lv_timer_t *timer)
{
    bool ok;
    if (!venice_poll(s_reply, sizeof(s_reply), &ok)) {
        return;
    }
    lv_timer_delete(s_poll);
    s_poll = NULL;
    lv_label_set_text(s_answer, s_reply);
    lv_label_set_text(s_status, ok ? g_cfg.venice_model : "Something went wrong.");
    if (ok && count_bullets(s_reply) > 0) {
        lv_obj_remove_flag(s_save_btn, LV_OBJ_FLAG_HIDDEN);
    }
}

static void ask(const char *question)
{
    if (!question || !*question) {
        return;
    }
    if (!g_cfg.venice_key[0]) {
        lv_label_set_text(s_answer, "Add your Venice API key in Setup first.");
        return;
    }
    if (net_state() != NET_CONNECTED) {
        lv_label_set_text(s_answer, "Not online. Check Wi-Fi in Setup.");
        return;
    }
    static char context[1800];
    build_context(context, sizeof(context));
    if (!venice_ask(context, question)) {
        lv_label_set_text(s_answer, "Still thinking about the last one.");
        return;
    }
    lv_label_set_text(s_question, question);
    lv_label_set_text(s_answer, "Thinking...");
    lv_obj_add_flag(s_save_btn, LV_OBJ_FLAG_HIDDEN);
    lv_textarea_set_text(s_input, "");
    if (!s_poll) {
        s_poll = lv_timer_create(poll_cb, 300, NULL);
    }
}

static void send_cb(lv_event_t *e)          { ask(lv_textarea_get_text(s_input)); }
static void done(lv_obj_t *ta, void *user)  { ask(lv_textarea_get_text(ta)); }
static void focus_cb(lv_event_t *e)         { ui_keyboard_open(s_input, done, NULL); }
static void plan_cb(lv_event_t *e)
{
    ask("Look at my open to-dos and habits. Give me the three things to do today to get closer to paying clients, as '- ' bullets, then one short encouraging line.");
}
static void nudge_cb(lv_event_t *e)
{
    ask("Give me one gentle, specific nudge for the next hour based on my lists. Two sentences.");
}

static void cleanup_cb(lv_event_t *e)
{
    if (s_poll) {
        lv_timer_delete(s_poll);
        s_poll = NULL;
    }
}

void page_chat_build(lv_obj_t *parent)
{
    theme_title(parent, "Chat");
    s_status = theme_label(parent, g_cfg.venice_key[0] ? g_cfg.venice_model : "No API key yet", FONT_SMALL);
    lv_obj_align(s_status, LV_ALIGN_TOP_RIGHT, 0, 10);

    s_input = lv_textarea_create(parent);
    lv_textarea_set_one_line(s_input, true);
    lv_textarea_set_max_length(s_input, 200);
    lv_textarea_set_placeholder_text(s_input, "Ask anything...");
    lv_obj_set_size(s_input, 330, 50);
    lv_obj_set_pos(s_input, 0, 52);
    lv_obj_add_event_cb(s_input, focus_cb, LV_EVENT_CLICKED, NULL);
    lv_obj_t *send = theme_button(parent, "Ask", send_cb, NULL);
    lv_obj_set_pos(send, 340, 52);
    lv_obj_t *plan = theme_button(parent, "Plan my day", plan_cb, NULL);
    lv_obj_set_style_text_font(plan, FONT_SMALL, 0);
    lv_obj_set_pos(plan, 425, 52);
    lv_obj_t *nudge = theme_button(parent, "Nudge", nudge_cb, NULL);
    lv_obj_set_style_text_font(nudge, FONT_SMALL, 0);
    lv_obj_set_pos(nudge, 566, 52);

    lv_obj_t *card = theme_card(parent, UI_CONTENT_W - 32, UI_CONTENT_H - 32 - 114);
    lv_obj_set_pos(card, 0, 114);
    lv_obj_add_event_cb(card, cleanup_cb, LV_EVENT_DELETE, NULL);   // card dies with the page
    lv_obj_add_flag(card, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_scroll_dir(card, LV_DIR_VER);
    s_question = theme_label(card, "Tap the field, or try Plan my day.", FONT_SMALL);
    lv_obj_set_style_text_color(s_question, COLOR_SHADE, 0);
    lv_obj_set_width(s_question, LV_PCT(100));
    lv_label_set_long_mode(s_question, LV_LABEL_LONG_WRAP);
    s_answer = theme_label(card, "Grove knows your to-dos, habits and note, so ask about your day.", FONT_BODY);
    lv_obj_set_width(s_answer, LV_PCT(100));
    lv_label_set_long_mode(s_answer, LV_LABEL_LONG_WRAP);
    lv_obj_align_to(s_answer, s_question, LV_ALIGN_OUT_BOTTOM_LEFT, 0, 10);
    s_save_btn = theme_button(parent, "Add bullets to To-do", save_bullets_cb, NULL);
    lv_obj_set_style_text_font(s_save_btn, FONT_SMALL, 0);
    lv_obj_align(s_save_btn, LV_ALIGN_BOTTOM_RIGHT, -8, -8);
    lv_obj_add_flag(s_save_btn, LV_OBJ_FLAG_HIDDEN);

    // Coming back while an answer is pending, or after one landed unseen.
    bool ok;
    if (venice_busy()) {
        lv_label_set_text(s_answer, "Thinking...");
        s_poll = lv_timer_create(poll_cb, 300, NULL);
    } else if (venice_poll(s_reply, sizeof(s_reply), &ok)) {
        lv_label_set_text(s_answer, s_reply);
        if (ok && count_bullets(s_reply) > 0) {
            lv_obj_remove_flag(s_save_btn, LV_OBJ_FLAG_HIDDEN);
        }
    }
}
