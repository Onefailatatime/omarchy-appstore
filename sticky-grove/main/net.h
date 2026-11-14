// Wi-Fi station plus NTP. Connects with the saved credentials, keeps the RTC in step.
#pragma once
#include <stdbool.h>

typedef enum { NET_IDLE, NET_CONNECTING, NET_CONNECTED, NET_FAILED } net_state_t;

void net_init(void);
void net_connect(void);        // (re)connect with g_cfg credentials
void net_apply_timezone(void);
net_state_t net_state(void);
bool net_time_synced(void);
const char *net_ip(void);
