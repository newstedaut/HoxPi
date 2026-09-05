#pragma once
/* Stub der esp_http_server-API (nur die hier benutzten Symbole, IDF 5.x) */
#include <stddef.h>
#include <stdint.h>
#include "esp_err.h"
typedef void *httpd_handle_t;
typedef enum { HTTP_GET = 1, HTTP_POST = 3 } httpd_method_t;
typedef struct httpd_req { size_t content_len; void *user_ctx; } httpd_req_t;
typedef struct {
    const char *uri; httpd_method_t method; esp_err_t (*handler)(httpd_req_t *r); void *user_ctx;
} httpd_uri_t;
typedef struct { uint16_t server_port; uint16_t max_uri_handlers; int lru_purge_enable; int stack_size; } httpd_config_t;
#define HTTPD_DEFAULT_CONFIG() (httpd_config_t){ .server_port = 80, .max_uri_handlers = 8, .lru_purge_enable = 0, .stack_size = 4096 }
#define HTTPD_RESP_USE_STRLEN (-1)
esp_err_t httpd_start(httpd_handle_t *h, const httpd_config_t *c);
esp_err_t httpd_register_uri_handler(httpd_handle_t h, const httpd_uri_t *u);
esp_err_t httpd_resp_set_status(httpd_req_t *r, const char *s);
esp_err_t httpd_resp_set_type(httpd_req_t *r, const char *t);
esp_err_t httpd_resp_set_hdr(httpd_req_t *r, const char *k, const char *v);
esp_err_t httpd_resp_send(httpd_req_t *r, const char *buf, ssize_t len);
int       httpd_req_recv(httpd_req_t *r, char *buf, size_t len);
esp_err_t httpd_req_get_hdr_value_str(httpd_req_t *r, const char *k, char *out, size_t cap);
esp_err_t httpd_req_get_url_query_str(httpd_req_t *r, char *out, size_t cap);
esp_err_t httpd_query_key_value(const char *q, const char *k, char *out, size_t cap);
