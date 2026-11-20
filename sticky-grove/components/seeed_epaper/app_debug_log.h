// Stub for the upstream debug-log component: this project does not trace the panel.
#pragma once
#include "esp_log.h"
#define APP_EPAPER_DEBUG_LOGE(tag, fmt, ...) do {} while (0)
#define APP_EPAPER_DEBUG_LOGW(tag, fmt, ...) do {} while (0)
#define APP_EPAPER_DEBUG_LOGI(tag, fmt, ...) do {} while (0)
#define APP_EPAPER_DEBUG_LOGD(tag, fmt, ...) do {} while (0)
