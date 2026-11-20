#include "rtc_pcf8563.h"
#include "esp_log.h"
#include "pins.h"

static i2c_master_dev_handle_t s_dev;
static uint8_t bcd2bin(uint8_t v) { return (v >> 4) * 10 + (v & 0x0F); }
static uint8_t bin2bcd(uint8_t v) { return ((v / 10) << 4) | (v % 10); }

void rtc_clock_init(i2c_master_bus_handle_t bus)
{
    if (i2c_master_probe(bus, PCF8563_ADDR, 50) != ESP_OK) {
        ESP_LOGW("rtc", "PCF8563 not found");
        return;
    }
    i2c_device_config_t cfg = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = PCF8563_ADDR,
        .scl_speed_hz = 100000,
    };
    i2c_master_bus_add_device(bus, &cfg, &s_dev);
}

bool rtc_clock_read(struct tm *out)
{
    uint8_t reg = 0x02, r[7];
    if (!s_dev || i2c_master_transmit_receive(s_dev, &reg, 1, r, 7, 50) != ESP_OK || (r[0] & 0x80)) {
        return false;
    }
    out->tm_sec = bcd2bin(r[0] & 0x7F);
    out->tm_min = bcd2bin(r[1] & 0x7F);
    out->tm_hour = bcd2bin(r[2] & 0x3F);
    out->tm_mday = bcd2bin(r[3] & 0x3F);
    out->tm_wday = r[4] & 0x07;
    out->tm_mon = bcd2bin(r[5] & 0x1F) - 1;
    out->tm_year = bcd2bin(r[6]) + 100;   // chip counts from 2000
    out->tm_isdst = 0;
    return out->tm_year >= 124;
}

void rtc_clock_write(const struct tm *t)
{
    if (!s_dev) {
        return;
    }
    uint8_t w[8] = { 0x02, bin2bcd(t->tm_sec), bin2bcd(t->tm_min), bin2bcd(t->tm_hour),
                     bin2bcd(t->tm_mday), (uint8_t)t->tm_wday, bin2bcd(t->tm_mon + 1),
                     bin2bcd(t->tm_year - 100) };
    i2c_master_transmit(s_dev, w, sizeof(w), 50);
}
