#pragma once
#include <stdint.h>
#include <stddef.h>
#include "esp_err.h"
typedef enum { MB_PARAM_HOLDING, MB_PARAM_INPUT, MB_PARAM_COIL, MB_PARAM_DISCRETE } mb_param_type_t;
typedef enum { MB_IPV4, MB_IPV6 } mb_tcp_addr_type_t;
typedef enum { MB_MODE_RTU, MB_MODE_ASCII, MB_MODE_TCP } mb_mode_type_t;
typedef struct { mb_mode_type_t ip_mode; uint16_t ip_port; mb_tcp_addr_type_t ip_addr_type; void *ip_addr; void *ip_netif_ptr; } mb_communication_info_t;
typedef struct { uint16_t start_offset; mb_param_type_t type; void *address; size_t size; } mb_register_area_descriptors_t;
typedef uint32_t mb_event_group_t;
#define MB_EVENT_HOLDING_REG_WR 0x08u
#define MB_EVENT_HOLDING_REG_RD 0x04u
typedef struct { uint32_t time_stamp; uint16_t mb_offset; mb_event_group_t type; uint8_t *address; size_t size; } mb_param_info_t;
esp_err_t mbc_slave_init_tcp(void **h);
esp_err_t mbc_slave_setup(void *c);
esp_err_t mbc_slave_set_descriptor(mb_register_area_descriptors_t d);
esp_err_t mbc_slave_start(void);
mb_event_group_t mbc_slave_check_event(mb_event_group_t g);
esp_err_t mbc_slave_get_param_info(mb_param_info_t *i, uint32_t ticks);
