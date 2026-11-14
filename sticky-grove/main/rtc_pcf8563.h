// PCF8563 real-time clock on the sensor bus.
#pragma once
#include <stdbool.h>
#include <time.h>
#include "driver/i2c_master.h"
void rtc_clock_init(i2c_master_bus_handle_t bus);
bool rtc_clock_read(struct tm *out);          // false when the clock lost power
void rtc_clock_write(const struct tm *t);
