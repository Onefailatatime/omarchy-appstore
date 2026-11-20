#include "venice.h"

#include <stdlib.h>
#include <string.h>
#include "cJSON.h"
#include "esp_crt_bundle.h"
#include "esp_heap_caps.h"
#include "esp_http_client.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "store.h"

static const char *TAG = "venice";
#define URL "https://api.venice.ai/api/v1/chat/completions"
#define RESPONSE_MAX (16 * 1024)

static volatile bool s_busy, s_ready, s_ok;
static char s_reply[VENICE_REPLY_MAX];
static char *s_system, *s_user;

static void set_reply(bool ok, const char *text)
{
    strncpy(s_reply, text, sizeof(s_reply) - 1);
    s_reply[sizeof(s_reply) - 1] = '\0';
    s_ok = ok;
    s_ready = true;
}

// Drop a leading <think>...</think> block some models emit.
static const char *strip_thinking(const char *text)
{
    const char *open = strstr(text, "<think>");
    const char *close = strstr(text, "</think>");
    if (open && close && close > open) {
        text = close + 8;
        while (*text == '\n' || *text == ' ') text++;
    }
    return text;
}

static void request_task(void *arg)
{
    cJSON *root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "model", g_cfg.venice_model);
    cJSON *messages = cJSON_AddArrayToObject(root, "messages");
    cJSON *sys = cJSON_CreateObject();
    cJSON_AddStringToObject(sys, "role", "system");
    cJSON_AddStringToObject(sys, "content", s_system);
    cJSON_AddItemToArray(messages, sys);
    cJSON *usr = cJSON_CreateObject();
    cJSON_AddStringToObject(usr, "role", "user");
    cJSON_AddStringToObject(usr, "content", s_user);
    cJSON_AddItemToArray(messages, usr);
    cJSON_AddNumberToObject(root, "max_completion_tokens", 300);
    cJSON_AddNumberToObject(root, "temperature", 0.7);
    cJSON *vp = cJSON_AddObjectToObject(root, "venice_parameters");
    cJSON_AddBoolToObject(vp, "include_venice_system_prompt", false);
    cJSON_AddBoolToObject(vp, "strip_thinking_response", true);
    char *body = cJSON_PrintUnformatted(root);
    cJSON_Delete(root);

    char auth[128];
    snprintf(auth, sizeof(auth), "Bearer %s", g_cfg.venice_key);
    esp_http_client_config_t cfg = {
        .url = URL,
        .method = HTTP_METHOD_POST,
        .timeout_ms = 45000,
        .crt_bundle_attach = esp_crt_bundle_attach,
        .buffer_size = 2048,
        .buffer_size_tx = 2048,
    };
    esp_http_client_handle_t client = esp_http_client_init(&cfg);
    esp_http_client_set_header(client, "Content-Type", "application/json");
    esp_http_client_set_header(client, "Authorization", auth);

    char *response = heap_caps_malloc(RESPONSE_MAX, MALLOC_CAP_SPIRAM);
    int total = 0;
    esp_err_t err = esp_http_client_open(client, strlen(body));
    if (err == ESP_OK) {
        esp_http_client_write(client, body, strlen(body));
        esp_http_client_fetch_headers(client);
        while (total < RESPONSE_MAX - 1) {
            int n = esp_http_client_read(client, response + total, RESPONSE_MAX - 1 - total);
            if (n <= 0) break;
            total += n;
        }
        response[total] = '\0';
    }
    int status = esp_http_client_get_status_code(client);
    esp_http_client_cleanup(client);
    free(body);

    if (err != ESP_OK) {
        set_reply(false, "Could not reach Venice. Check Wi-Fi.");
    } else if (status != 200) {
        char msg[96];
        snprintf(msg, sizeof(msg), "Venice answered HTTP %d. Check the API key and model.", status);
        ESP_LOGW(TAG, "status %d: %.200s", status, response);
        set_reply(false, msg);
    } else {
        cJSON *json = cJSON_Parse(response);
        cJSON *choices = cJSON_GetObjectItem(json, "choices");
        cJSON *first = cJSON_GetArrayItem(choices, 0);
        cJSON *message = cJSON_GetObjectItem(first, "message");
        cJSON *content = cJSON_GetObjectItem(message, "content");
        if (cJSON_IsString(content)) {
            set_reply(true, strip_thinking(content->valuestring));
        } else {
            set_reply(false, "Venice sent an answer I could not read.");
        }
        cJSON_Delete(json);
    }
    free(response);
    free(s_system);
    free(s_user);
    s_system = s_user = NULL;
    s_busy = false;
    vTaskDelete(NULL);
}

bool venice_busy(void) { return s_busy; }

bool venice_ask(const char *system_prompt, const char *user_prompt)
{
    if (s_busy || !g_cfg.venice_key[0]) {
        return false;
    }
    s_busy = true;
    s_ready = false;
    s_system = strdup(system_prompt);
    s_user = strdup(user_prompt);
    if (xTaskCreate(request_task, "venice", 12288, NULL, 2, NULL) != pdPASS) {
        s_busy = false;
        return false;
    }
    return true;
}

bool venice_poll(char *reply, int reply_len, bool *ok)
{
    if (!s_ready) {
        return false;
    }
    s_ready = false;
    strncpy(reply, s_reply, reply_len - 1);
    reply[reply_len - 1] = '\0';
    *ok = s_ok;
    return true;
}
