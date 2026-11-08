// Power, buttons, buzzer, battery gauge and the shared sensor I2C bus.
#pragma once

#include <stdbool.h>
#include <stdint.h>
#include "driver/i2c_master.h"

typedef enum {
    BOARD_BTN_NONE = 0,
    BOARD_BTN_UP,
    BOARD_BTN_DOWN,
    BOARD_BTN_AI,
    BOARD_BTN_AI_LONG,
} board_button_t;

typedef void (*board_button_cb_t)(board_button_t button);

void board_init(board_button_cb_t on_button);
i2c_master_bus_handle_t board_sensor_bus(void);
void board_beep(uint32_t freq_hz, uint32_t ms);
int board_battery_percent(void);      // -1 when the gauge is missing
bool board_on_usb_power(void);
void board_power_off(void);           // cuts the power latch, does not return
void board_deep_sleep(void);          // wakes on any of the three buttons
