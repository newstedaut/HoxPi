#pragma once
#include <stdint.h>
#include "esp_err.h"
#include "esp_event.h"
#include "driver/spi_master.h"
typedef struct { int dummy; } eth_mac_config_t;
typedef struct { int phy_addr; int reset_gpio_num; } eth_phy_config_t;
typedef struct { struct { int mdc_num, mdio_num; } smi_gpio; } eth_esp32_emac_config_t;
typedef struct { int int_gpio_num; spi_host_device_t host; const spi_device_interface_config_t *dev; } eth_w5500_config_t;
typedef struct esp_eth_mac_s esp_eth_mac_t; typedef struct esp_eth_phy_s esp_eth_phy_t;
typedef struct { esp_eth_mac_t *mac; esp_eth_phy_t *phy; } esp_eth_config_t;
typedef void *esp_eth_handle_t;
extern esp_event_base_t ETH_EVENT;
enum { ETHERNET_EVENT_START, ETHERNET_EVENT_STOP, ETHERNET_EVENT_CONNECTED, ETHERNET_EVENT_DISCONNECTED };
typedef enum { ETH_CMD_G_MAC_ADDR, ETH_CMD_S_MAC_ADDR } esp_eth_io_cmd_t;
#define ETH_MAC_DEFAULT_CONFIG() { 0 }
#define ETH_PHY_DEFAULT_CONFIG() { 1, 5 }
#define ETH_ESP32_EMAC_DEFAULT_CONFIG() { { 23, 18 } }
#define ETH_W5500_DEFAULT_CONFIG(h, d) { 4, (h), (d) }
#define ETH_DEFAULT_CONFIG(m, p) { (m), (p) }
esp_eth_mac_t *esp_eth_mac_new_esp32(const eth_esp32_emac_config_t *e, const eth_mac_config_t *c);
esp_eth_phy_t *esp_eth_phy_new_lan87xx(const eth_phy_config_t *c);
esp_eth_mac_t *esp_eth_mac_new_w5500(const eth_w5500_config_t *w, const eth_mac_config_t *c);
esp_eth_phy_t *esp_eth_phy_new_w5500(const eth_phy_config_t *c);
esp_err_t esp_eth_driver_install(const esp_eth_config_t *c, esp_eth_handle_t *h);
esp_err_t esp_eth_ioctl(esp_eth_handle_t h, esp_eth_io_cmd_t cmd, void *data);
void *esp_eth_new_netif_glue(esp_eth_handle_t h);
esp_err_t esp_eth_start(esp_eth_handle_t h);
