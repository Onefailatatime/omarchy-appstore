#include "store.h"

#include <string.h>
#include "esp_log.h"
#include "nvs.h"
#include "nvs_flash.h"

static const char *TAG = "store";
#define DATA_MAGIC 0x47524F31   // "GRO1"
#define CFG_MAGIC  0x47524332   // "GRC2"

store_data_t g_data;
store_config_t g_cfg;

const char *const store_tz_names[] = {
    "US Eastern", "US Central", "US Mountain", "US Pacific", "Alaska", "Hawaii",
    "UTC", "London", "Berlin / Paris", "Tokyo", "Sydney",
};
const char *const store_tz_posix[] = {
    "EST5EDT,M3.2.0,M11.1.0", "CST6CDT,M3.2.0,M11.1.0", "MST7MDT,M3.2.0,M11.1.0",
    "PST8PDT,M3.2.0,M11.1.0", "AKST9AKDT,M3.2.0,M11.1.0", "HST10",
    "UTC0", "GMT0BST,M3.5.0/1,M10.5.0", "CET-1CEST,M3.5.0,M10.5.0/3", "JST-9",
    "AEST-10AEDT,M10.1.0,M4.1.0/3",
};
const int store_tz_count = sizeof(store_tz_names) / sizeof(store_tz_names[0]);

static bool load_blob(const char *key, void *out, size_t len, uint32_t magic)
{
    nvs_handle_t h;
    if (nvs_open("grove", NVS_READONLY, &h) != ESP_OK) {
        return false;
    }
    size_t size = len;
    esp_err_t err = nvs_get_blob(h, key, out, &size);
    nvs_close(h);
    return err == ESP_OK && size == len && *(uint32_t *)out == magic;
}

static void save_blob(const char *key, const void *data, size_t len)
{
    nvs_handle_t h;
    if (nvs_open("grove", NVS_READWRITE, &h) != ESP_OK) {
        ESP_LOGE(TAG, "nvs open failed");
        return;
    }
    if (nvs_set_blob(h, key, data, len) == ESP_OK) {
        nvs_commit(h);
    }
    nvs_close(h);
}

void store_init(void)
{
    esp_err_t err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES || err == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        nvs_flash_erase();
        nvs_flash_init();
    }
    if (!load_blob("data", &g_data, sizeof(g_data), DATA_MAGIC)) {
        memset(&g_data, 0, sizeof(g_data));
        g_data.magic = DATA_MAGIC;
        todo_add("Reach out to one new lead");
        todo_add("Follow up with yesterday's contact");
        habit_add("Outreach");
        habit_add("Walk");
        habit_add("Water");
        strcpy(g_data.note, "Welcome to the grove.\nTap Note to write here.");
    }
    if (!load_blob("cfg", &g_cfg, sizeof(g_cfg), CFG_MAGIC)) {
        memset(&g_cfg, 0, sizeof(g_cfg));
        g_cfg.magic = CFG_MAGIC;
        strcpy(g_cfg.venice_model, "llama-3.3-70b");
        g_cfg.sleep_minutes = 5;
        g_cfg.fahrenheit = true;
    }
}

void store_save_data(void)   { save_blob("data", &g_data, sizeof(g_data)); }
void store_save_config(void) { save_blob("cfg", &g_cfg, sizeof(g_cfg)); }

// Howard Hinnant's days_from_civil.
uint32_t day_index(int y, int m, int d)
{
    y -= m <= 2;
    const int era = (y >= 0 ? y : y - 399) / 400;
    const unsigned yoe = (unsigned)(y - era * 400);
    const unsigned doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return (uint32_t)(era * 146097 + (int)doe - 719468);
}

uint32_t day_index_tm(const struct tm *t)
{
    return day_index(t->tm_year + 1900, t->tm_mon + 1, t->tm_mday);
}

static void copy_text(char *dst, size_t size, const char *src)
{
    strncpy(dst, src, size - 1);
    dst[size - 1] = '\0';
}

bool todo_add(const char *text)
{
    if (g_data.todo_count >= TODO_MAX || !text || !*text) {
        return false;
    }
    todo_t *t = &g_data.todos[g_data.todo_count++];
    copy_text(t->text, TODO_TEXT, text);
    t->done = false;
    return true;
}

void todo_remove(int index)
{
    if (index < 0 || index >= g_data.todo_count) {
        return;
    }
    memmove(&g_data.todos[index], &g_data.todos[index + 1],
            (g_data.todo_count - index - 1) * sizeof(todo_t));
    g_data.todo_count--;
}

void todo_clear_done(void)
{
    for (int i = g_data.todo_count - 1; i >= 0; i--) {
        if (g_data.todos[i].done) {
            todo_remove(i);
        }
    }
}

bool habit_add(const char *name)
{
    if (g_data.habit_count >= HABIT_MAX || !name || !*name) {
        return false;
    }
    habit_t *h = &g_data.habits[g_data.habit_count++];
    copy_text(h->name, HABIT_TEXT, name);
    h->anchor_day = 0;
    h->bits = 0;
    return true;
}

void habit_remove(int index)
{
    if (index < 0 || index >= g_data.habit_count) {
        return;
    }
    memmove(&g_data.habits[index], &g_data.habits[index + 1],
            (g_data.habit_count - index - 1) * sizeof(habit_t));
    g_data.habit_count--;
}

bool habit_done_on(const habit_t *h, uint32_t day)
{
    if (day < h->anchor_day || day - h->anchor_day >= 32) {
        return false;
    }
    return (h->bits >> (day - h->anchor_day)) & 1;
}

void habit_set(habit_t *h, uint32_t day, bool done)
{
    if (h->anchor_day == 0 || h->bits == 0) {
        h->anchor_day = day;
    }
    if (day < h->anchor_day) {
        return;   // older than the window we keep
    }
    uint32_t offset = day - h->anchor_day;
    if (offset >= 32) {
        uint32_t shift = offset - 31;
        h->bits = shift >= 32 ? 0 : h->bits >> shift;
        h->anchor_day += shift;
        offset = 31;
    }
    if (done) {
        h->bits |= 1u << offset;
    } else {
        h->bits &= ~(1u << offset);
    }
}

int habit_streak(const habit_t *h, uint32_t today)
{
    int streak = 0;
    uint32_t day = habit_done_on(h, today) ? today : today - 1;
    while (habit_done_on(h, day)) {
        streak++;
        day--;
    }
    return streak;
}

bool event_add(int year, int month, int day, const char *text)
{
    if (g_data.event_count >= EVENT_MAX || !text || !*text) {
        return false;
    }
    event_t *e = &g_data.events[g_data.event_count++];
    e->year = year;
    e->month = month;
    e->day = day;
    copy_text(e->text, EVENT_TEXT, text);
    return true;
}

void event_remove(int index)
{
    if (index < 0 || index >= g_data.event_count) {
        return;
    }
    memmove(&g_data.events[index], &g_data.events[index + 1],
            (g_data.event_count - index - 1) * sizeof(event_t));
    g_data.event_count--;
}

int event_find(int year, int month, int day, int *indices, int max)
{
    int n = 0;
    for (int i = 0; i < g_data.event_count && n < max; i++) {
        const event_t *e = &g_data.events[i];
        if (e->year == year && e->month == month && e->day == day) {
            indices[n++] = i;
        }
    }
    return n;
}

int event_next(uint32_t today)
{
    int best = -1;
    uint32_t best_day = 0;
    for (int i = 0; i < g_data.event_count; i++) {
        const event_t *e = &g_data.events[i];
        uint32_t d = day_index(e->year, e->month, e->day);
        if (d >= today && (best < 0 || d < best_day)) {
            best = i;
            best_day = d;
        }
    }
    return best;
}
