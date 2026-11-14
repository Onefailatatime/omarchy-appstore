// SHT40 temperature and humidity sensor on the sensor bus.
#pragma once
#include <stdbool.h>
#include "driver/i2c_master.h"
void sht40_init(i2c_master_bus_handle_t bus);
bool sht40_read(float *celsius, float *humidity);
