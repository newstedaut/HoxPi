#pragma once
/* Stub: esp_http_client_config_t (nur die hier benutzten Felder, IDF 5.x) */
#include <stdbool.h>
#include "esp_err.h"
typedef struct {
    const char *url; const char *cert_pem; int timeout_ms; bool keep_alive_enable;
    bool skip_cert_common_name_check; esp_err_t (*crt_bundle_attach)(void *conf);
} esp_http_client_config_t;
