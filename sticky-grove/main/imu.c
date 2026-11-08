#include "imu.h"

#include <stdlib.h>
#include "esp_log.h"
#include "pins.h"

static const char *TAG = "imu";
static i2c_master_dev_handle_t s_dev;

// Which accelerometer axis runs along the panel's long side, and which sign
// means the top edge of the landscape view points up. Flip these if the
// screen turns the wrong way; the boot log prints the raw axes to help.
#define IMU_LONG_AXIS   0     // 0 = X, 1 = Y
#define IMU_LONG_SIGN   1     // +1 or -1
#define IMU_SHORT_SIGN  1

void imu_init(i2c_master_bus_handle_t bus)
{
    const uint8_t addrs[] = { 0x6A, 0x6B };
    for (size_t i = 0; i < 2 && !s_dev; i++) {
        if (i2c_master_probe(bus, addrs[i], 50) != ESP_OK) {
            continue;
        }
        i2c_device_config_t cfg = {
            .dev_addr_length = I2C_ADDR_BIT_LEN_7,
            .device_address = addrs[i],
            .scl_speed_hz = 100000,
        };
        if (i2c_master_bus_add_device(bus, &cfg, &s_dev) != ESP_OK) {
            s_dev = NULL;
            continue;
        }
        const uint8_t ctrl1_xl[2] = { 0x10, 0x20 };   // accelerometer 26 Hz, +-2 g
        i2c_master_transmit(s_dev, ctrl1_xl, 2, 50);
        ESP_LOGI(TAG, "LSM6DS3 at 0x%02X", addrs[i]);
    }
    if (!s_dev) {
        ESP_LOGW(TAG, "motion sensor not found, staying landscape");
    }
}

imu_orientation_t imu_orientation(void)
{
    if (!s_dev) {
        return IMU_UNKNOWN;
    }
    const uint8_t reg = 0x28;   // OUTX_L_XL .. OUTZ_H_XL
    uint8_t r[6];
    if (i2c_master_transmit_receive(s_dev, &reg, 1, r, 6, 50) != ESP_OK) {
        return IMU_UNKNOWN;
    }
    int16_t a[3] = { (int16_t)(r[0] | r[1] << 8), (int16_t)(r[2] | r[3] << 8), (int16_t)(r[4] | r[5] << 8) };
    int along = a[IMU_LONG_AXIS] * IMU_LONG_SIGN;          // gravity along the long side
    int across = a[1 - IMU_LONG_AXIS] * IMU_SHORT_SIGN;    // gravity along the short side
    const int threshold = 9000;                            // about 0.55 g at 0.061 mg per LSB
    ESP_LOGD(TAG, "accel x=%d y=%d z=%d", a[0], a[1], a[2]);
    if (abs(along) > threshold && abs(along) > abs(across)) {
        return along > 0 ? IMU_PORTRAIT_CW : IMU_PORTRAIT_CCW;
    }
    if (abs(across) > threshold) {
        return IMU_LANDSCAPE;
    }
    return IMU_UNKNOWN;
}
