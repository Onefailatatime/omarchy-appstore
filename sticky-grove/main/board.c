#include "board.h"

#include "driver/gpio.h"
#include "driver/ledc.h"
#include "driver/rtc_io.h"
#include "esp_log.h"
#include "esp_rom_sys.h"
#include "esp_sleep.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "iot_button.h"
#include "button_gpio.h"
#include "pins.h"

static const char *TAG = "board";
static i2c_master_bus_handle_t s_bus;
static i2c_master_dev_handle_t s_gauge;
static board_button_cb_t s_on_button;

static void power_latch(bool on)
{
    gpio_hold_dis(PIN_POWER_HOLD);
    gpio_set_level(PIN_POWER_HOLD, on);
    gpio_set_level(PIN_POWER_LOCK, 0);
    esp_rom_delay_us(10);
    gpio_set_level(PIN_POWER_LOCK, 1);
    esp_rom_delay_us(10);
    gpio_set_level(PIN_POWER_LOCK, 0);
}

static void on_up(void *h, void *d)      { if (s_on_button) s_on_button(BOARD_BTN_UP); }
static void on_down(void *h, void *d)    { if (s_on_button) s_on_button(BOARD_BTN_DOWN); }
static void on_ai(void *h, void *d)      { if (s_on_button) s_on_button(BOARD_BTN_AI); }
static void on_ai_long(void *h, void *d) { if (s_on_button) s_on_button(BOARD_BTN_AI_LONG); }

static void button_init(int gpio, button_cb_t click, button_cb_t long_press)
{
    button_config_t cfg = { .long_press_time = 1500, .short_press_time = 150 };
    button_gpio_config_t io = { .gpio_num = gpio, .active_level = 0 };
    button_handle_t handle = NULL;
    if (iot_button_new_gpio_device(&cfg, &io, &handle) != ESP_OK) {
        ESP_LOGW(TAG, "button on GPIO%d failed", gpio);
        return;
    }
    iot_button_register_cb(handle, BUTTON_SINGLE_CLICK, NULL, click, NULL);
    if (long_press) {
        iot_button_register_cb(handle, BUTTON_LONG_PRESS_START, NULL, long_press, NULL);
    }
}

void board_init(board_button_cb_t on_button)
{
    s_on_button = on_button;

    gpio_config_t out = {
        .pin_bit_mask = (1ULL << PIN_POWER_HOLD) | (1ULL << PIN_POWER_LOCK) | (1ULL << PIN_BAT_CHG_EN),
        .mode = GPIO_MODE_OUTPUT,
    };
    gpio_config(&out);
    power_latch(true);
    gpio_set_level(PIN_BAT_CHG_EN, 0);   // allow charging

    gpio_config_t in = { .pin_bit_mask = 1ULL << PIN_EXTERNAL_POWER, .mode = GPIO_MODE_INPUT };
    gpio_config(&in);

    i2c_master_bus_config_t bus = {
        .i2c_port = I2C_NUM_1,
        .sda_io_num = PIN_SENSOR_SDA,
        .scl_io_num = PIN_SENSOR_SCL,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = 1,
    };
    ESP_ERROR_CHECK(i2c_new_master_bus(&bus, &s_bus));

    i2c_device_config_t gauge = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = BQ27220_ADDR,
        .scl_speed_hz = 100000,
    };
    if (i2c_master_probe(s_bus, BQ27220_ADDR, 50) == ESP_OK) {
        i2c_master_bus_add_device(s_bus, &gauge, &s_gauge);
    } else {
        ESP_LOGW(TAG, "battery gauge not found");
    }

    ledc_timer_config_t timer = {
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .timer_num = LEDC_TIMER_0,
        .duty_resolution = LEDC_TIMER_10_BIT,
        .freq_hz = 2000,
        .clk_cfg = LEDC_AUTO_CLK,
    };
    ledc_timer_config(&timer);
    ledc_channel_config_t ch = {
        .gpio_num = PIN_BUZZER,
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .channel = LEDC_CHANNEL_0,
        .timer_sel = LEDC_TIMER_0,
        .duty = 0,
    };
    ledc_channel_config(&ch);

    button_init(PIN_BTN_UP, on_up, NULL);
    button_init(PIN_BTN_DOWN, on_down, NULL);
    button_init(PIN_POWER_BTN, on_ai, on_ai_long);
}

i2c_master_bus_handle_t board_sensor_bus(void)
{
    return s_bus;
}

void board_beep(uint32_t freq_hz, uint32_t ms)
{
    ledc_set_freq(LEDC_LOW_SPEED_MODE, LEDC_TIMER_0, freq_hz);
    ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, 400);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
    vTaskDelay(pdMS_TO_TICKS(ms));
    ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, 0);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
}

int board_battery_percent(void)
{
    if (!s_gauge) {
        return -1;
    }
    const uint8_t reg = 0x2C;   // StateOfCharge
    uint8_t raw[2] = {0};
    if (i2c_master_transmit_receive(s_gauge, &reg, 1, raw, 2, 50) != ESP_OK) {
        return -1;
    }
    int percent = raw[0] | (raw[1] << 8);
    return percent > 100 ? 100 : percent;
}

bool board_on_usb_power(void)
{
    return gpio_get_level(PIN_EXTERNAL_POWER) != 0;
}

void board_power_off(void)
{
    ESP_LOGI(TAG, "power off");
    vTaskDelay(pdMS_TO_TICKS(100));
    power_latch(false);
    while (true) {
        vTaskDelay(portMAX_DELAY);
    }
}

void board_deep_sleep(void)
{
    ESP_LOGI(TAG, "deep sleep");
    const uint64_t wake_mask = (1ULL << PIN_POWER_BTN) | (1ULL << PIN_BTN_UP) | (1ULL << PIN_BTN_DOWN);
    const int wake_pins[] = { PIN_POWER_BTN, PIN_BTN_UP, PIN_BTN_DOWN };
    for (size_t i = 0; i < 3; i++) {
        rtc_gpio_init(wake_pins[i]);
        rtc_gpio_set_direction(wake_pins[i], RTC_GPIO_MODE_INPUT_ONLY);
        rtc_gpio_pulldown_dis(wake_pins[i]);
        rtc_gpio_pullup_en(wake_pins[i]);
    }
    esp_sleep_enable_ext1_wakeup_io(wake_mask, ESP_EXT1_WAKEUP_ANY_LOW);
    // Keep the power latch high while the core is asleep.
    gpio_hold_en(PIN_POWER_HOLD);
    gpio_deep_sleep_hold_en();
    esp_deep_sleep_start();
}
