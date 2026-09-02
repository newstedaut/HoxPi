#pragma once
#include <stdint.h>
#include "esp_err.h"
#include "esp_event.h"
typedef struct esp_netif_obj esp_netif_t;
typedef struct { uint32_t addr; } esp_ip4_addr_t;
typedef struct { esp_ip4_addr_t ip, netmask, gw; } esp_netif_ip_info_t;
typedef struct { esp_netif_t *esp_netif; esp_netif_ip_info_t ip_info; } ip_event_got_ip_t;
typedef struct { int dummy; } esp_netif_config_t;
extern esp_event_base_t IP_EVENT;
enum { IP_EVENT_STA_GOT_IP, IP_EVENT_ETH_GOT_IP };
#define IPSTR "%d.%d.%d.%d"
#define IP2STR(a) (int)((a)->addr & 0xff), (int)(((a)->addr >> 8) & 0xff), (int)(((a)->addr >> 16) & 0xff), (int)(((a)->addr >> 24) & 0xff)
#define ESP_NETIF_DEFAULT_ETH() { 0 }
esp_err_t esp_netif_init(void);
esp_netif_t *esp_netif_new(const esp_netif_config_t *c);
esp_err_t esp_netif_attach(esp_netif_t *n, void *glue);
