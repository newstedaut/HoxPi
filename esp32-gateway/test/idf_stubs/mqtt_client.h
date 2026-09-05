#pragma once
/* Stub der esp-mqtt-API (nur die hier benutzten Symbole, ESP-IDF 5.3) */
#include <stdint.h>
#include <stddef.h>
#include "esp_err.h"
#include "esp_event.h"
typedef struct esp_mqtt_client *esp_mqtt_client_handle_t;
typedef enum { MQTT_EVENT_ANY = -1, MQTT_EVENT_ERROR = 0, MQTT_EVENT_CONNECTED, MQTT_EVENT_DISCONNECTED, MQTT_EVENT_SUBSCRIBED,
               MQTT_EVENT_UNSUBSCRIBED, MQTT_EVENT_PUBLISHED, MQTT_EVENT_DATA, MQTT_EVENT_BEFORE_CONNECT, MQTT_EVENT_DELETED } esp_mqtt_event_id_t;
typedef struct { int error_type; int esp_tls_last_esp_err; int connect_return_code; } esp_mqtt_error_codes_t;
typedef struct {
    esp_mqtt_event_id_t event_id; esp_mqtt_client_handle_t client;
    char *data; int data_len; int total_data_len; int current_data_offset;
    char *topic; int topic_len; int msg_id; int session_present; esp_mqtt_error_codes_t *error_handle; bool retain; int qos; bool dup;
} esp_mqtt_event_t;
typedef esp_mqtt_event_t *esp_mqtt_event_handle_t;
typedef struct {
    struct { struct { const char *uri; const char *hostname; int port; } address; } broker;
    struct { const char *username; const char *client_id; struct { const char *password; } authentication; } credentials;
    struct { struct { const char *topic; const char *msg; int msg_len; int qos; int retain; } last_will;
             int keepalive; bool disable_clean_session; } session;
    struct { int reconnect_timeout_ms; int timeout_ms; } network;
} esp_mqtt_client_config_t;
esp_mqtt_client_handle_t esp_mqtt_client_init(const esp_mqtt_client_config_t *c);
esp_err_t esp_mqtt_client_register_event(esp_mqtt_client_handle_t c, esp_mqtt_event_id_t e, esp_event_handler_t h, void *arg);
esp_err_t esp_mqtt_client_start(esp_mqtt_client_handle_t c);
int esp_mqtt_client_publish(esp_mqtt_client_handle_t c, const char *topic, const char *data, int len, int qos, int retain);
int esp_mqtt_client_subscribe(esp_mqtt_client_handle_t c, const char *topic, int qos);
