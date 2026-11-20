#include "sht40.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "pins.h"

static i2c_master_dev_handle_t s_dev;

void sht40_init(i2c_master_bus_handle_t bus)
{
    if (i2c_master_probe(bus, SHT40_ADDR, 50) != ESP_OK) {
        ESP_LOGW("sht40", "not found");
        return;
    }
    i2c_device_config_t cfg = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = SHT40_ADDR,
        .scl_speed_hz = 100000,
    };
    i2c_master_bus_add_device(bus, &cfg, &s_dev);
}

bool sht40_read(float *celsius, float *humidity)
{
    const uint8_t cmd = 0xFD;   // high precision measurement
    uint8_t r[6];
    if (!s_dev || i2c_master_transmit(s_dev, &cmd, 1, 50) != ESP_OK) {
        return false;
    }
    vTaskDelay(pdMS_TO_TICKS(12));
    if (i2c_master_receive(s_dev, r, 6, 50) != ESP_OK) {
        return false;
    }
    float t = ((r[0] << 8) | r[1]) / 65535.0f;
    float h = ((r[3] << 8) | r[4]) / 65535.0f;
    *celsius = -45.0f + 175.0f * t;
    *humidity = -6.0f + 125.0f * h;
    if (*humidity < 0) *humidity = 0;
    if (*humidity > 100) *humidity = 100;
    return true;
}
