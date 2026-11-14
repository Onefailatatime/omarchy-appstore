// Sticky Grove: a calm dashboard, to-dos, habits, calendar, note and an AI chat
// for the Seeed reTerminal Sticky e-paper display.
#include <sys/time.h>
#include <time.h>
#include "board.h"
#include "display.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "assets.h"
#include "imu.h"
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/task.h"
#include "lvgl.h"
#include "net.h"
#include "rtc_pcf8563.h"
#include "sht40.h"
#include "store.h"
#include "touch.h"
#include "ui/ui.h"
#include "venice.h"

static const char *TAG = "grove";
static QueueHandle_t s_buttons;

static void on_button(board_button_t button)
{
    xQueueSend(s_buttons, &button, 0);
}

static uint32_t tick_ms(void)
{
    return (uint32_t)(esp_timer_get_time() / 1000);
}

static display_rotation_t rotation_from(imu_orientation_t o)
{
    switch (o) {
    case IMU_PORTRAIT_CW:  return ROT_PORTRAIT_CW;
    case IMU_PORTRAIT_CCW: return ROT_PORTRAIT_CCW;
    case IMU_LANDSCAPE:    return ROT_LANDSCAPE;
    default:               return display_rotation();   // flat: keep what we have
    }
}

// Turn the UI once the sensor has reported the same new way up twice in a row.
static void follow_orientation(void)
{
    static display_rotation_t candidate;
    static int votes;
    display_rotation_t seen = rotation_from(imu_orientation());
    if (seen == display_rotation()) {
        votes = 0;
        return;
    }
    if (seen != candidate) {
        candidate = seen;
        votes = 1;
        return;
    }
    if (++votes >= 2) {
        votes = 0;
        ESP_LOGI(TAG, "turning to %s", seen == ROT_LANDSCAPE ? "landscape" : "portrait");
        ui_set_rotation(seen);
    }
}

static void settle_and_sleep(void)
{
    // Leave the dashboard on the wall, let the panel finish drawing, then sleep.
    ui_show(PAGE_HOME);
    uint32_t until = tick_ms() + 5000;
    while (tick_ms() < until) {
        lv_timer_handler();
        vTaskDelay(pdMS_TO_TICKS(20));
    }
    display_wait_idle(8000);
    display_sleep();
    board_deep_sleep();
}

void app_main(void)
{
    s_buttons = xQueueCreate(8, sizeof(board_button_t));
    board_init(on_button);
    store_init();
    net_apply_timezone();
    rtc_clock_init(board_sensor_bus());
    sht40_init(board_sensor_bus());
    imu_init(board_sensor_bus());
    assets_init();

    struct tm t;
    if (rtc_clock_read(&t)) {
        struct timeval tv = { .tv_sec = mktime(&t) };
        settimeofday(&tv, NULL);
    } else {
        ESP_LOGW(TAG, "RTC time not valid, waiting for NTP");
    }

    lv_init();
    lv_tick_set_cb(tick_ms);
    display_init();
    touch_init();
    display_set_rotation(rotation_from(imu_orientation()));
    ui_init();
    net_init();

    time_t last_minute = time(NULL) / 60;
    uint32_t last_imu = 0;
    while (true) {
        uint32_t wait = lv_timer_handler();
        board_button_t button;
        while (xQueueReceive(s_buttons, &button, 0) == pdTRUE) {
            if (button == BOARD_BTN_AI_LONG) {
                board_beep(1200, 80);
                store_save_data();
                display_wait_idle(8000);
                display_sleep();
                board_power_off();
            }
            ui_handle_button(button);
        }
        time_t minute = time(NULL) / 60;
        if (minute != last_minute) {
            last_minute = minute;
            ui_minute_tick();
        }
        if (tick_ms() - last_imu > 1500) {
            last_imu = tick_ms();
            follow_orientation();
        }
        uint32_t idle_ms = lv_display_get_inactive_time(NULL);
        if (g_cfg.sleep_minutes && !board_on_usb_power() && !venice_busy() &&
            idle_ms > (uint32_t)g_cfg.sleep_minutes * 60000u) {
            settle_and_sleep();
        }
        vTaskDelay(pdMS_TO_TICKS(wait < 5 ? 5 : (wait > 50 ? 50 : wait)));
    }
}
