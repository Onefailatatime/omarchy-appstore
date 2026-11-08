// Everything the device remembers: to-dos, habits, events, the note and settings.
// Two NVS blobs, loaded once into the globals below and saved on change.
#pragma once

#include <stdbool.h>
#include <stdint.h>
#include <time.h>

#define TODO_MAX   20
#define TODO_TEXT  48
#define HABIT_MAX  6
#define HABIT_TEXT 24
#define EVENT_MAX  30
#define EVENT_TEXT 40
#define NOTE_TEXT  400

typedef struct { char text[TODO_TEXT]; bool done; } todo_t;
typedef struct {
    char name[HABIT_TEXT];
    uint32_t anchor_day;   // day index of bit 0
    uint32_t bits;         // bit k set = done on anchor_day + k
} habit_t;
typedef struct { uint16_t year; uint8_t month, day; char text[EVENT_TEXT]; } event_t;

typedef struct {
    uint32_t magic;
    uint8_t todo_count;
    todo_t todos[TODO_MAX];
    uint8_t habit_count;
    habit_t habits[HABIT_MAX];
    uint8_t event_count;
    event_t events[EVENT_MAX];
    char note[NOTE_TEXT];
} store_data_t;

typedef struct {
    uint32_t magic;
    char wifi_ssid[33];
    char wifi_pass[65];
    char venice_key[100];
    char venice_model[48];
    uint8_t tz_index;
    uint8_t sleep_minutes;   // idle time before deep sleep, 0 = never
    bool fahrenheit;
} store_config_t;

extern store_data_t g_data;
extern store_config_t g_cfg;

void store_init(void);
void store_save_data(void);
void store_save_config(void);

// Time zones offered in Settings.
extern const char *const store_tz_names[];
extern const char *const store_tz_posix[];
extern const int store_tz_count;

uint32_t day_index(int year, int month, int day);   // days since 1970-01-01
uint32_t day_index_tm(const struct tm *t);

bool todo_add(const char *text);
void todo_remove(int index);
void todo_clear_done(void);

bool habit_add(const char *name);
void habit_remove(int index);
bool habit_done_on(const habit_t *h, uint32_t day);
void habit_set(habit_t *h, uint32_t day, bool done);
int habit_streak(const habit_t *h, uint32_t today);

bool event_add(int year, int month, int day, const char *text);
void event_remove(int index);
int event_find(int year, int month, int day, int *indices, int max);   // sorted by insertion
int event_next(uint32_t today);                                        // index or -1
