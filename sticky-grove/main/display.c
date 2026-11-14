#include "display.h"

#include <string.h>
#include "driver/spi_master.h"
#include "epaper_panel.h"
#include "esp_heap_caps.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/task.h"
#include "pins.h"

static const char *TAG = "display";
#define PIXELS ((size_t)SCREEN_W * SCREEN_H)
#define PARTIALS_BEFORE_FULL 10

static seeed_epaper_panel_handle_t s_panel;
static lv_display_t *s_disp;
static uint16_t *s_rgb;      // LVGL draw buffer, logical orientation
static uint8_t *s_gray8;     // panel orientation frame handed to the refresh task
static uint8_t *s_gray2;     // packed 2 bpp copy for GRAY4 refreshes
static SemaphoreHandle_t s_frame_lock;
static TaskHandle_t s_task;
static portMUX_TYPE s_lock = portMUX_INITIALIZER_UNLOCKED;
static volatile display_refresh_t s_requested = DISPLAY_REFRESH_PARTIAL;
static display_rotation_t s_rotation = ROT_LANDSCAPE;
static bool s_need_full = true;   // first frame, and the frame after a GRAY4 pass
static int s_partials;
static volatile bool s_pushing;

static inline uint8_t luma(uint16_t p)
{
    uint32_t r = (p >> 11) & 0x1F, g = (p >> 5) & 0x3F, b = p & 0x1F;
    return (uint8_t)((r * 255 / 31 * 77 + g * 255 / 63 * 151 + b * 255 / 31 * 28) >> 8);
}

// Logical frame -> panel frame. Portrait frames are 480 wide and 800 tall.
static void rgb_to_gray(void)
{
    if (s_rotation == ROT_LANDSCAPE) {
        for (size_t i = 0; i < PIXELS; i++) {
            s_gray8[i] = luma(s_rgb[i]);
        }
        return;
    }
    for (int y = 0; y < SCREEN_W; y++) {          // logical rows, 800 of them
        for (int x = 0; x < SCREEN_H; x++) {      // logical columns, 480 of them
            int px, py;
            if (s_rotation == ROT_PORTRAIT_CW) {
                px = y;
                py = SCREEN_H - 1 - x;
            } else {
                px = SCREEN_W - 1 - y;
                py = x;
            }
            s_gray8[py * SCREEN_W + px] = luma(s_rgb[y * SCREEN_H + x]);
        }
    }
}

static void gray_to_2bpp(void)
{
    for (size_t i = 0; i < PIXELS; i += 4) {
        uint8_t byte = 0;
        for (int k = 0; k < 4; k++) {
            uint8_t level = 3 - (s_gray8[i + k] >> 6);   // 0 white .. 3 black
            byte |= level << (6 - 2 * k);
        }
        s_gray2[i / 4] = byte;
    }
}

static void push_frame(display_refresh_t mode)
{
    const seeed_epaper_area_t full = {0, 0, SCREEN_W, SCREEN_H};
    esp_err_t err;
    xSemaphoreTake(s_frame_lock, portMAX_DELAY);
    if (mode == DISPLAY_REFRESH_GRAY4) {
        gray_to_2bpp();
        err = seeed_epaper_panel_write_bitmap_gray4(s_panel, &full, s_gray2, SCREEN_W / 4);
    } else {
        seeed_epaper_refresh_mode_t m = mode == DISPLAY_REFRESH_FULL ? SEEED_EPAPER_REFRESH_FULL
                                                                      : SEEED_EPAPER_REFRESH_PARTIAL;
        err = seeed_epaper_panel_prepare(s_panel, m);
        if (err == ESP_OK) {
            err = seeed_epaper_panel_write_bitmap(s_panel, &full, s_gray8, SCREEN_W,
                                                  SEEED_EPAPER_PIXEL_FORMAT_GRAY8, m);
        }
    }
    xSemaphoreGive(s_frame_lock);
    if (err == ESP_OK) {
        seeed_epaper_refresh_mode_t m = mode == DISPLAY_REFRESH_GRAY4 ? SEEED_EPAPER_REFRESH_GRAY4
                                      : mode == DISPLAY_REFRESH_FULL ? SEEED_EPAPER_REFRESH_FULL
                                                                     : SEEED_EPAPER_REFRESH_PARTIAL;
        err = seeed_epaper_panel_commit(s_panel, &full, m);
    }
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "refresh failed: %s", esp_err_to_name(err));
    }
}

static void refresh_task(void *arg)
{
    while (true) {
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        vTaskDelay(pdMS_TO_TICKS(120));   // coalesce bursts such as typing
        taskENTER_CRITICAL(&s_lock);
        display_refresh_t mode = s_requested;
        s_requested = DISPLAY_REFRESH_PARTIAL;
        taskEXIT_CRITICAL(&s_lock);
        if (s_need_full && mode == DISPLAY_REFRESH_PARTIAL) {
            mode = DISPLAY_REFRESH_FULL;
        }
        if (mode == DISPLAY_REFRESH_PARTIAL && ++s_partials >= PARTIALS_BEFORE_FULL) {
            mode = DISPLAY_REFRESH_FULL;
        }
        if (mode != DISPLAY_REFRESH_PARTIAL) {
            s_partials = 0;
        }
        s_need_full = mode == DISPLAY_REFRESH_GRAY4;
        s_pushing = true;
        push_frame(mode);
        s_pushing = false;
    }
}

static void flush_cb(lv_display_t *disp, const lv_area_t *area, uint8_t *px_map)
{
    if (lv_display_flush_is_last(disp)) {
        xSemaphoreTake(s_frame_lock, portMAX_DELAY);
        rgb_to_gray();
        xSemaphoreGive(s_frame_lock);
        s_pushing = true;
        xTaskNotifyGive(s_task);
    }
    lv_display_flush_ready(disp);
}

lv_display_t *display_init(void)
{
    spi_bus_config_t bus = {
        .mosi_io_num = PIN_EPD_MOSI,
        .miso_io_num = -1,
        .sclk_io_num = PIN_EPD_CLK,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = SCREEN_W * SCREEN_H / 8,
    };
    ESP_ERROR_CHECK(spi_bus_initialize(SPI2_HOST, &bus, SPI_DMA_CH_AUTO));
    spi_device_interface_config_t dev = {
        .clock_speed_hz = 10 * 1000 * 1000,
        .mode = 0,
        .spics_io_num = PIN_EPD_CS,
        .queue_size = 1,
    };
    spi_device_handle_t spi;
    ESP_ERROR_CHECK(spi_bus_add_device(SPI2_HOST, &dev, &spi));

    seeed_epaper_panel_config_t cfg = {
        .spi_handle = spi,
        .pin_dc = PIN_EPD_DC,
        .pin_rst = PIN_EPD_RST,
        .pin_busy = PIN_EPD_BUSY,
        .pin_enable = PIN_EPD_EN,
        .busy_timeout_ms = 10000,
        .reset_low_ms = 10,
        .reset_high_ms = 10,
        .busy_level = 1,
        .enable_level = 1,
        .mirror_x = true,
    };
    ESP_ERROR_CHECK(seeed_epaper_new_panel(SEEED_EPAPER_PANEL_SSD1677, &cfg, &s_panel));

    s_rgb = heap_caps_malloc(PIXELS * 2, MALLOC_CAP_SPIRAM);
    s_gray8 = heap_caps_malloc(PIXELS, MALLOC_CAP_SPIRAM);
    s_gray2 = heap_caps_malloc(PIXELS / 4, MALLOC_CAP_SPIRAM);
    assert(s_rgb && s_gray8 && s_gray2);
    memset(s_rgb, 0xFF, PIXELS * 2);
    s_frame_lock = xSemaphoreCreateMutex();
    xTaskCreate(refresh_task, "epaper", 4096, NULL, 3, &s_task);

    s_disp = lv_display_create(SCREEN_W, SCREEN_H);
    lv_display_set_color_format(s_disp, LV_COLOR_FORMAT_RGB565);
    lv_display_set_buffers(s_disp, s_rgb, NULL, PIXELS * 2, LV_DISPLAY_RENDER_MODE_DIRECT);
    lv_display_set_flush_cb(s_disp, flush_cb);
    return s_disp;
}

void display_request(display_refresh_t mode)
{
    taskENTER_CRITICAL(&s_lock);
    if (mode > s_requested) {
        s_requested = mode;
    }
    taskEXIT_CRITICAL(&s_lock);
}

void display_set_rotation(display_rotation_t rotation)
{
    if (rotation == s_rotation) {
        return;
    }
    s_rotation = rotation;
    bool portrait = rotation != ROT_LANDSCAPE;
    lv_display_set_resolution(s_disp, portrait ? SCREEN_H : SCREEN_W, portrait ? SCREEN_W : SCREEN_H);
    // Same bytes, new row length: re-register the buffer so LVGL recomputes its stride.
    lv_display_set_buffers(s_disp, s_rgb, NULL, PIXELS * 2, LV_DISPLAY_RENDER_MODE_DIRECT);
}

display_rotation_t display_rotation(void)
{
    return s_rotation;
}

void display_wait_idle(uint32_t timeout_ms)
{
    TickType_t until = xTaskGetTickCount() + pdMS_TO_TICKS(timeout_ms);
    while (s_pushing && xTaskGetTickCount() < until) {
        vTaskDelay(pdMS_TO_TICKS(20));
    }
}

void display_sleep(void)
{
    xSemaphoreTake(s_frame_lock, portMAX_DELAY);
    seeed_epaper_panel_sleep(s_panel);
    xSemaphoreGive(s_frame_lock);
}
