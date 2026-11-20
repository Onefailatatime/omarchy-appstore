// Venice AI chat completions, one request at a time on a worker task.
#pragma once
#include <stdbool.h>

#define VENICE_REPLY_MAX 1200

bool venice_busy(void);
// Starts a request. Returns false when busy or no API key is set.
bool venice_ask(const char *system_prompt, const char *user_prompt);
// True once per finished request; copies the reply (or an error message) out.
bool venice_poll(char *reply, int reply_len, bool *ok);
