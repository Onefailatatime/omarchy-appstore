// LSM6DS3TR-C motion sensor, used only to tell which way up the Sticky hangs.
#pragma once
#include "driver/i2c_master.h"

typedef enum {
    IMU_UNKNOWN = 0,      // flat on a table, or no sensor
    IMU_LANDSCAPE,
    IMU_PORTRAIT_CW,      // landscape top edge now on the right
    IMU_PORTRAIT_CCW,     // landscape top edge now on the left
} imu_orientation_t;

void imu_init(i2c_master_bus_handle_t bus);
imu_orientation_t imu_orientation(void);
