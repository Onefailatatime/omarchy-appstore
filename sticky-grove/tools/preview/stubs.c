// Fakes for the hardware and network modules so the UI can run on a desktop.
#include <stdbool.h>
#include <stdint.h>
#include "board.h"
#include "display.h"
#include "imu.h"
void preview_rebind_buffer(void);
#include "net.h"
#include "nvs.h"
#include "nvs_flash.h"
#include "sht40.h"
#include "venice.h"

esp_err_t nvs_open(const char *ns, nvs_open_mode_t mode, nvs_handle_t *out) { return ESP_FAIL; }
esp_err_t nvs_get_blob(nvs_handle_t h, const char *k, void *o, size_t *l) { return ESP_FAIL; }
esp_err_t nvs_set_blob(nvs_handle_t h, const char *k, const void *d, size_t l) { return ESP_OK; }
esp_err_t nvs_commit(nvs_handle_t h) { return ESP_OK; }
void nvs_close(nvs_handle_t h) {}
esp_err_t nvs_flash_init(void) { return ESP_OK; }
esp_err_t nvs_flash_erase(void) { return ESP_OK; }

void board_init(board_button_cb_t cb) {}
i2c_master_bus_handle_t board_sensor_bus(void) { return NULL; }
void board_beep(uint32_t f, uint32_t ms) {}
int board_battery_percent(void) { return 83; }
bool board_on_usb_power(void) { return false; }
void board_power_off(void) {}
void board_deep_sleep(void) {}

void sht40_init(i2c_master_bus_handle_t bus) {}
bool sht40_read(float *c, float *h) { *c = 21.5f; *h = 44.0f; return true; }

void net_init(void) {}
void net_connect(void) {}
void net_apply_timezone(void) {}
net_state_t net_state(void) { return NET_CONNECTED; }
bool net_time_synced(void) { return true; }
const char *net_ip(void) { return "192.168.1.52"; }

bool venice_busy(void) { return false; }
bool venice_ask(const char *s, const char *u) { return false; }
bool venice_poll(char *r, int n, bool *ok) { return false; }

void display_request(display_refresh_t mode) {}
static display_rotation_t s_rot;
void display_set_rotation(display_rotation_t r)
{
    s_rot = r;
    bool portrait = r != ROT_LANDSCAPE;
    lv_display_set_resolution(lv_display_get_default(), portrait ? 480 : 800, portrait ? 800 : 480);
    preview_rebind_buffer();
}
display_rotation_t display_rotation(void) { return s_rot; }
void imu_init(i2c_master_bus_handle_t bus) {}
imu_orientation_t imu_orientation(void) { return IMU_UNKNOWN; }
void display_wait_idle(uint32_t ms) {}
void display_sleep(void) {}
