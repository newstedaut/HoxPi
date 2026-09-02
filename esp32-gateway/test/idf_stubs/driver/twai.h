#pragma once
#include <stdint.h>
#include "esp_err.h"
typedef enum { TWAI_MODE_NORMAL, TWAI_MODE_NO_ACK, TWAI_MODE_LISTEN_ONLY } twai_mode_t;
typedef enum { TWAI_STATE_STOPPED, TWAI_STATE_RUNNING, TWAI_STATE_BUS_OFF, TWAI_STATE_RECOVERING } twai_state_t;
typedef struct { twai_mode_t mode; int tx_io, rx_io; uint32_t tx_queue_len, rx_queue_len; } twai_general_config_t;
typedef struct { int dummy; } twai_timing_config_t;
typedef struct { int dummy; } twai_filter_config_t;
typedef struct {
    union { struct { uint32_t extd: 1; uint32_t rtr: 1; uint32_t ss: 1; uint32_t self: 1; uint32_t dlc_non_comp: 1; uint32_t reserved: 27; }; uint32_t flags; };
    uint32_t identifier; uint8_t data_length_code; uint8_t data[8];
} twai_message_t;
typedef struct { twai_state_t state; uint32_t msgs_to_tx, msgs_to_rx, tx_error_counter, rx_error_counter, tx_failed_count, rx_missed_count, rx_overrun_count, arb_lost_count, bus_error_count; } twai_status_info_t;
#define TWAI_GENERAL_CONFIG_DEFAULT(tx, rx, m) { (m), (tx), (rx), 5, 5 }
#define TWAI_TIMING_CONFIG_50KBITS() { 0 }
#define TWAI_FILTER_CONFIG_ACCEPT_ALL() { 0 }
esp_err_t twai_driver_install(const twai_general_config_t *g, const twai_timing_config_t *t, const twai_filter_config_t *f);
esp_err_t twai_start(void);
esp_err_t twai_receive(twai_message_t *m, uint32_t ticks);
esp_err_t twai_transmit(const twai_message_t *m, uint32_t ticks);
esp_err_t twai_get_status_info(twai_status_info_t *s);
esp_err_t twai_initiate_recovery(void);
