#pragma once
/* Stub der app_update-API (nur die hier benutzten Symbole, IDF 5.x) */
#include <stdint.h>
#include "esp_err.h"
typedef struct { int type; int subtype; uint32_t address; uint32_t size; char label[17]; } esp_partition_t;
typedef enum { ESP_OTA_IMG_NEW = 0, ESP_OTA_IMG_PENDING_VERIFY = 1, ESP_OTA_IMG_VALID = 2, ESP_OTA_IMG_INVALID = 3,
               ESP_OTA_IMG_ABORTED = 4, ESP_OTA_IMG_UNDEFINED = 0xFFFFFFFF } esp_ota_img_states_t;
const esp_partition_t *esp_ota_get_running_partition(void);
const esp_partition_t *esp_ota_get_boot_partition(void);
esp_err_t esp_ota_get_state_partition(const esp_partition_t *p, esp_ota_img_states_t *st);
esp_err_t esp_ota_mark_app_valid_cancel_rollback(void);
esp_err_t esp_ota_mark_app_invalid_rollback_and_reboot(void);
