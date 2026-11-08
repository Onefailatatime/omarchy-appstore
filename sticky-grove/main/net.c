#include "net.h"

#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include "esp_event.h"
#include "esp_log.h"
#include "esp_netif.h"
#include "esp_sntp.h"
#include "esp_timer.h"
#include "esp_wifi.h"
#include "rtc_pcf8563.h"
#include "store.h"

static const char *TAG = "net";
static net_state_t s_state = NET_IDLE;
static bool s_synced;
static char s_ip[16] = "";
static int s_retries;
static esp_timer_handle_t s_retry_timer;

static void retry_later(void *arg)
{
    s_retries = 0;
    s_state = NET_CONNECTING;
    esp_wifi_connect();
}

static void on_time_sync(struct timeval *tv)
{
    struct tm t;
    localtime_r(&tv->tv_sec, &t);
    rtc_clock_write(&t);
    s_synced = true;
    ESP_LOGI(TAG, "time synced");
}

static void on_event(void *arg, esp_event_base_t base, int32_t id, void *data)
{
    if (base == WIFI_EVENT && id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (base == WIFI_EVENT && id == WIFI_EVENT_STA_DISCONNECTED) {
        s_ip[0] = '\0';
        if (s_retries++ < 5) {
            s_state = NET_CONNECTING;
            esp_wifi_connect();
        } else {
            s_state = NET_FAILED;
            esp_timer_start_once(s_retry_timer, 60 * 1000 * 1000);   // try again in a minute
        }
    } else if (base == IP_EVENT && id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t *e = data;
        snprintf(s_ip, sizeof(s_ip), IPSTR, IP2STR(&e->ip_info.ip));
        s_retries = 0;
        s_state = NET_CONNECTED;
        if (!esp_sntp_enabled()) {
            esp_sntp_setoperatingmode(ESP_SNTP_OPMODE_POLL);
            esp_sntp_setservername(0, "pool.ntp.org");
            sntp_set_time_sync_notification_cb(on_time_sync);
            esp_sntp_init();
        }
    }
}

void net_apply_timezone(void)
{
    int i = g_cfg.tz_index < store_tz_count ? g_cfg.tz_index : 0;
    setenv("TZ", store_tz_posix[i], 1);
    tzset();
}

void net_init(void)
{
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    esp_event_handler_register(WIFI_EVENT, ESP_EVENT_ANY_ID, on_event, NULL);
    esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, on_event, NULL);
    const esp_timer_create_args_t retry = { .callback = retry_later, .name = "wifi_retry" };
    esp_timer_create(&retry, &s_retry_timer);
    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_ps(WIFI_PS_MAX_MODEM);
    if (g_cfg.wifi_ssid[0]) {
        net_connect();
    }
}

void net_connect(void)
{
    if (!g_cfg.wifi_ssid[0]) {
        s_state = NET_IDLE;
        return;
    }
    wifi_config_t wc = {0};
    strncpy((char *)wc.sta.ssid, g_cfg.wifi_ssid, sizeof(wc.sta.ssid));
    strncpy((char *)wc.sta.password, g_cfg.wifi_pass, sizeof(wc.sta.password));
    wc.sta.threshold.authmode = g_cfg.wifi_pass[0] ? WIFI_AUTH_WPA2_PSK : WIFI_AUTH_OPEN;
    esp_timer_stop(s_retry_timer);
    s_retries = 0;
    s_state = NET_CONNECTING;
    esp_wifi_stop();
    esp_wifi_set_config(WIFI_IF_STA, &wc);
    esp_wifi_start();
}

net_state_t net_state(void)  { return s_state; }
bool net_time_synced(void)   { return s_synced; }
const char *net_ip(void)     { return s_ip; }
