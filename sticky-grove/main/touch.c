#include "touch.h"

#include "driver/gpio.h"
#include "driver/i2c_master.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "pins.h"

static const char *TAG = "touch";
#define REG_STATUS 0x814E
#define REG_POINTS 0x8150
#define REG_RES    0x8146
#define SENSOR_W   480   // sensor orientation, see TOUCH_SWAP_XY
#define SENSOR_H   800

static i2c_master_bus_handle_t s_bus;
static i2c_master_dev_handle_t s_dev;
static uint16_t s_max_x = SENSOR_W, s_max_y = SENSOR_H;

static bool reg_read(uint16_t reg, uint8_t *buf, size_t len)
{
    uint8_t addr[2] = { reg >> 8, reg & 0xFF };
    return i2c_master_transmit_receive(s_dev, addr, 2, buf, len, 20) == ESP_OK;
}

static bool reg_write8(uint16_t reg, uint8_t value)
{
    uint8_t payload[3] = { reg >> 8, reg & 0xFF, value };
    return i2c_master_transmit(s_dev, payload, 3, 20) == ESP_OK;
}

// Address select happens on the reset edge: INT low -> 0x5D, INT high -> 0x14.
static bool reset_to(uint8_t address)
{
    gpio_set_direction(PIN_TOUCH_INT, GPIO_MODE_OUTPUT);
    gpio_set_direction(PIN_TOUCH_RST, GPIO_MODE_OUTPUT);
    gpio_set_level(PIN_TOUCH_RST, 0);
    gpio_set_level(PIN_TOUCH_INT, address == 0x14);
    vTaskDelay(pdMS_TO_TICKS(20));
    gpio_set_level(PIN_TOUCH_RST, 1);
    vTaskDelay(pdMS_TO_TICKS(20));
    gpio_set_direction(PIN_TOUCH_INT, GPIO_MODE_INPUT);
    vTaskDelay(pdMS_TO_TICKS(80));
    if (i2c_master_probe(s_bus, address, 20) != ESP_OK) {
        return false;
    }
    i2c_device_config_t cfg = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = address,
        .scl_speed_hz = 100000,
    };
    if (i2c_master_bus_add_device(s_bus, &cfg, &s_dev) != ESP_OK) {
        return false;
    }
    uint8_t id[4];
    if (!reg_read(0x8140, id, 4)) {
        i2c_master_bus_rm_device(s_dev);
        s_dev = NULL;
        return false;
    }
    return true;
}

static void read_cb(lv_indev_t *indev, lv_indev_data_t *data)
{
    static lv_point_t last;
    data->state = LV_INDEV_STATE_RELEASED;
    data->point = last;
    uint8_t status = 0;
    if (!s_dev || !reg_read(REG_STATUS, &status, 1) || !(status & 0x80)) {
        return;
    }
    uint8_t count = status & 0x0F;
    if (count >= 1 && count <= 5) {
        uint8_t raw[8];
        if (reg_read(REG_POINTS, raw, 8)) {
            uint32_t sx = raw[0] | (raw[1] << 8);
            uint32_t sy = raw[2] | (raw[3] << 8);
            int32_t x = sx * (SENSOR_W - 1) / s_max_x;
            int32_t y = sy * (SENSOR_H - 1) / s_max_y;
#if TOUCH_SWAP_XY
            int32_t t = x; x = y; y = t;
#endif
#if TOUCH_MIRROR_X
            x = SCREEN_W - 1 - x;
#endif
#if TOUCH_MIRROR_Y
            y = SCREEN_H - 1 - y;
#endif
            last.x = LV_CLAMP(0, x, SCREEN_W - 1);
            last.y = LV_CLAMP(0, y, SCREEN_H - 1);
            data->point = last;
            data->state = LV_INDEV_STATE_PRESSED;
        }
    }
    reg_write8(REG_STATUS, 0);
}

lv_indev_t *touch_init(void)
{
    gpio_config_t en = { .pin_bit_mask = 1ULL << PIN_TOUCH_EN, .mode = GPIO_MODE_OUTPUT };
    gpio_config(&en);
    gpio_set_level(PIN_TOUCH_EN, 1);
    vTaskDelay(pdMS_TO_TICKS(250));

    i2c_master_bus_config_t bus = {
        .i2c_port = I2C_NUM_0,
        .sda_io_num = PIN_TOUCH_SDA,
        .scl_io_num = PIN_TOUCH_SCL,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = 1,
    };
    ESP_ERROR_CHECK(i2c_new_master_bus(&bus, &s_bus));

    bool ok = false;
    for (int attempt = 0; attempt < 3 && !ok; attempt++) {
        ok = reset_to(0x14) || reset_to(0x5D);
    }
    if (!ok) {
        ESP_LOGE(TAG, "GT911 not found");
    } else {
        uint8_t res[4];
        if (reg_read(REG_RES, res, 4)) {
            uint16_t x = res[0] | (res[1] << 8), y = res[2] | (res[3] << 8);
            if (x) s_max_x = x;
            if (y) s_max_y = y;
        }
        reg_write8(REG_STATUS, 0);
        ESP_LOGI(TAG, "GT911 ready, sensor %ux%u", s_max_x, s_max_y);
    }

    lv_indev_t *indev = lv_indev_create();
    lv_indev_set_type(indev, LV_INDEV_TYPE_POINTER);
    lv_indev_set_read_cb(indev, read_cb);
    return indev;
}
