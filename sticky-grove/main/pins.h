// reTerminal Sticky GPIO map (Seeed hardware overview + community firmware).
#pragma once

#define PIN_POWER_BTN      4   // AI button, active low, also the deep-sleep wake pin
#define PIN_BTN_UP         5
#define PIN_BTN_DOWN       6
#define PIN_POWER_HOLD     45  // keep high or the board powers itself off
#define PIN_POWER_LOCK     46
#define PIN_BAT_CHG_EN     39  // active low
#define PIN_EXTERNAL_POWER 9   // high when USB power is present

#define PIN_SENSOR_SCL     0   // I2C1: BQ27220 gauge, PCF8563 RTC, SHT40, IMU
#define PIN_SENSOR_SDA     1
#define BQ27220_ADDR       0x55
#define PCF8563_ADDR       0x51
#define SHT40_ADDR         0x44

#define PIN_TOUCH_SCL      2   // I2C0: GT911
#define PIN_TOUCH_SDA      3
#define PIN_TOUCH_EN       42
#define PIN_TOUCH_INT      21
#define PIN_TOUCH_RST      41

#define PIN_EPD_MOSI       14  // SPI2: SSD1677, 800x480
#define PIN_EPD_CLK        13
#define PIN_EPD_CS         15
#define PIN_EPD_DC         16
#define PIN_EPD_RST        17
#define PIN_EPD_BUSY       18
#define PIN_EPD_EN         47

#define PIN_BUZZER         48

#define SCREEN_W           800
#define SCREEN_H           480

// The GT911 sensor is wired portrait (480 across, 800 down). Swap to land in
// landscape screen coordinates; flip these if touches land mirrored.
#define TOUCH_SWAP_XY      1
#define TOUCH_MIRROR_X     0
#define TOUCH_MIRROR_Y     0
