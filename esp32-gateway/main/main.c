/*
 * main.c — HoxPi-ESP32: Hoval-CAN -> Modbus-TCP-Gateway (ESP-IDF >= 5.3)
 *
 * Ablauf: NVS/Netif/Event-Loop -> Laufzeit-Konfiguration (hoval_cfg: Kconfig-Defaults, NVS-Namespace "hoxpi"
 *         ueberschreibt Poll-Intervalle/Schreibfreigabe/Whitelist) -> Ethernet (RMII-PHY oder W5500-SPI, je Kconfig)
 *         -> auf IP warten -> Modbus-Slave (hoval_modbus.c) -> CAN (hoval_can.c) -> Statusseite (hoval_http.c :80)
 *         -> MQTT/Home Assistant (hoval_mqtt.c, nur mit HOXPI_MQTT_URI) -> OTA-Rollback-Wache (hoval_ota.c)
 *         -> Status-Task (Log alle 60 s).
 * Noch NICHT auf Hardware getestet (02.09.2026, kein Board). Pins in Kconfig.projbuild je Board.
 */
#include <string.h>
#include <inttypes.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_log.h"
#include "esp_err.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "esp_eth.h"
#include "esp_mac.h"
#include "esp_system.h"
#include "esp_timer.h"
#include "driver/spi_master.h"
#include "nvs_flash.h"
#include "sdkconfig.h"
#include "hoval_proto.h"
#include "hoval_can.h"
#include "hoval_modbus.h"
#include "hoval_cfg.h"
#include "hoval_http.h"
#include "hoval_mqtt.h"
#include "hoval_ota.h"

static const char *TAG = "hoxpi";
static EventGroupHandle_t s_ev;

static void cfg_warn(const char *msg, uint16_t reg) { ESP_LOGW(TAG, "%s: reg %u", msg, reg); }
#define EV_GOT_IP BIT0

static void on_got_ip(void *arg, esp_event_base_t base, int32_t id, void *data)
{
    (void)arg; (void)base; (void)id;
    const ip_event_got_ip_t *e = (const ip_event_got_ip_t *)data;
    ESP_LOGI(TAG, "IP: " IPSTR "  GW: " IPSTR, IP2STR(&e->ip_info.ip), IP2STR(&e->ip_info.gw));
    xEventGroupSetBits(s_ev, EV_GOT_IP);
}

static void on_eth(void *arg, esp_event_base_t base, int32_t id, void *data)
{
    (void)arg; (void)base; (void)data;
    switch (id) {
    case ETHERNET_EVENT_CONNECTED:    ESP_LOGI(TAG, "Ethernet Link up"); break;
    case ETHERNET_EVENT_DISCONNECTED: ESP_LOGW(TAG, "Ethernet Link down"); xEventGroupClearBits(s_ev, EV_GOT_IP); break;
    default: break;
    }
}

/* ---- Ethernet: zwei Varianten ---- */
static esp_netif_t *eth_start(void)
{
    eth_mac_config_t mac_config = ETH_MAC_DEFAULT_CONFIG();
    eth_phy_config_t phy_config = ETH_PHY_DEFAULT_CONFIG();
    esp_eth_mac_t *mac = NULL; esp_eth_phy_t *phy = NULL;

#if CONFIG_HOXPI_ETH_RMII
    /* ESP32 (classic) mit internem EMAC + LAN87xx-PHY, z. B. Olimex ESP32-EVB (PHY-Adr 0, MDC 23, MDIO 18) */
    phy_config.phy_addr = CONFIG_HOXPI_ETH_PHY_ADDR;
    phy_config.reset_gpio_num = CONFIG_HOXPI_ETH_PHY_RST_GPIO;
    eth_esp32_emac_config_t emac = ETH_ESP32_EMAC_DEFAULT_CONFIG();
    emac.smi_gpio.mdc_num  = CONFIG_HOXPI_ETH_MDC_GPIO;    /* IDF >= 5.3 (vorher smi_mdc_gpio_num) */
    emac.smi_gpio.mdio_num = CONFIG_HOXPI_ETH_MDIO_GPIO;
    mac = esp_eth_mac_new_esp32(&emac, &mac_config);
    phy = esp_eth_phy_new_lan87xx(&phy_config);
#else
    /* W5500 an SPI (ESP32-S3-Boards, z. B. Waveshare ESP32-S3-POE-ETH) */
    spi_bus_config_t bus = { .miso_io_num = CONFIG_HOXPI_W5500_MISO, .mosi_io_num = CONFIG_HOXPI_W5500_MOSI,
                             .sclk_io_num = CONFIG_HOXPI_W5500_SCLK, .quadwp_io_num = -1, .quadhd_io_num = -1 };
    ESP_ERROR_CHECK(spi_bus_initialize(SPI2_HOST, &bus, SPI_DMA_CH_AUTO));
    spi_device_interface_config_t dev = { .command_bits = 16, .address_bits = 8, .mode = 0,
                                          .clock_speed_hz = 20 * 1000 * 1000, .spics_io_num = CONFIG_HOXPI_W5500_CS, .queue_size = 20 };
    eth_w5500_config_t w5500 = ETH_W5500_DEFAULT_CONFIG(SPI2_HOST, &dev);
    w5500.int_gpio_num = CONFIG_HOXPI_W5500_INT;
    phy_config.phy_addr = -1;
    phy_config.reset_gpio_num = CONFIG_HOXPI_W5500_RST;
    mac = esp_eth_mac_new_w5500(&w5500, &mac_config);
    phy = esp_eth_phy_new_w5500(&phy_config);
#endif
    esp_eth_config_t cfg = ETH_DEFAULT_CONFIG(mac, phy);
    esp_eth_handle_t h = NULL;
    ESP_ERROR_CHECK(esp_eth_driver_install(&cfg, &h));
#if !CONFIG_HOXPI_ETH_RMII
    uint8_t macaddr[6]; ESP_ERROR_CHECK(esp_read_mac(macaddr, ESP_MAC_ETH));   /* W5500 hat keine eigene MAC */
    ESP_ERROR_CHECK(esp_eth_ioctl(h, ETH_CMD_S_MAC_ADDR, macaddr));
#endif
    esp_netif_config_t ncfg = ESP_NETIF_DEFAULT_ETH();
    esp_netif_t *netif = esp_netif_new(&ncfg);
    ESP_ERROR_CHECK(esp_netif_attach(netif, esp_eth_new_netif_glue(h)));
    ESP_ERROR_CHECK(esp_event_handler_register(ETH_EVENT, ESP_EVENT_ANY_ID, &on_eth, NULL));
    ESP_ERROR_CHECK(esp_event_handler_register(IP_EVENT, IP_EVENT_ETH_GOT_IP, &on_got_ip, NULL));
    ESP_ERROR_CHECK(esp_eth_start(h));
    return netif;
}

/* ---- Status alle 60 s; Stale-Warnung wenn > 10 min kein Datenpunkt ---- */
static void status_task(void *arg)
{
    (void)arg;
    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(60000));
        const hc_stats_t *s = hc_stats();
        uint16_t st = 0, err = 0, aussen = 0;
        hm_read(1501, &st); hm_read(1534, &err); hm_read(1477, &aussen);
        uint32_t age_s = s->last_rx_ms ? (uint32_t)(esp_timer_get_time() / 1000 - s->last_rx_ms) / 1000 : 0;
        ESP_LOGI(TAG, "CAN rx=%" PRIu32 " msgs=%" PRIu32 " dec=%" PRIu32 " tx=%" PRIu32 " txerr=%" PRIu32 " busoff=%" PRIu32
                 " | 1501=%u 1534=%u 1477=%d | letzter DP vor %" PRIu32 " s | heap %" PRIu32,
                 s->rx_frames, s->rx_msgs, s->decoded, s->tx_frames, s->tx_errors, s->bus_off,
                 st, err, (int16_t)aussen, age_s, (uint32_t)esp_get_free_heap_size());
        if (s->last_rx_ms && age_s > 600) ESP_LOGW(TAG, "STALE: seit %" PRIu32 " s keine Hoval-Antwort (CAN-Kabel? Regler aus?)", age_s);
    }
}

void app_main(void)
{
    ESP_LOGI(TAG, "HoxPi-ESP32 Gateway, %u Register, %u Modbus-Bereiche, Whitelist %u",
             hp_regs_count, hp_areas_count, hp_whitelist_count);
    esp_err_t r = nvs_flash_init();
    if (r == ESP_ERR_NVS_NO_FREE_PAGES || r == ESP_ERR_NVS_NEW_VERSION_FOUND) { ESP_ERROR_CHECK(nvs_flash_erase()); r = nvs_flash_init(); }
    ESP_ERROR_CHECK(r);
    hota_log_boot();

    /* Laufzeit-Konfiguration: Kconfig-Defaults, dann NVS drueber, dann Whitelist einhaengen */
    hcfg_defaults(hcfg_mut(), CONFIG_HOXPI_POLL_INTERVAL_S, CONFIG_HOXPI_POLL_HV_INTERVAL_S,
                  CONFIG_HOXPI_POLL_DELAY_MS, CONFIG_HOXPI_ENABLE_WRITE);
    hcfg_nvs_load(hcfg_mut());
    size_t dropped = hcfg_apply(hcfg_mut(), cfg_warn);
    {
        uint16_t wn = 0; hp_whitelist_active(&wn);
        const hcfg_t *c = hcfg_get();
        ESP_LOGI(TAG, "Konfig: Poll WEZ %u s, HV %u s, Abstand %u ms, Schreiben %s, Whitelist %u Register (%s%s), NVS-Quellen 0x%02x",
                 c->poll_wez_s, c->poll_hv_s, c->poll_delay_ms, c->enable_write ? "AN" : "AUS", wn,
                 c->wl_override ? "NVS" : "Kompilat", dropped ? ", Eintraege verworfen" : "", c->from_nvs);
    }

    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    s_ev = xEventGroupCreate();

    esp_netif_t *netif = eth_start();
    ESP_LOGI(TAG, "warte auf IP (DHCP) ...");
    xEventGroupWaitBits(s_ev, EV_GOT_IP, pdFALSE, pdTRUE, portMAX_DELAY);

    if (!hm_start(netif, hcfg_get()->enable_write)) { ESP_LOGE(TAG, "Modbus-Start fehlgeschlagen - Neustart in 10 s"); vTaskDelay(pdMS_TO_TICKS(10000)); esp_restart(); }
    if (!hc_start(hm_store))                          { ESP_LOGE(TAG, "CAN-Start fehlgeschlagen - Neustart in 10 s");    vTaskDelay(pdMS_TO_TICKS(10000)); esp_restart(); }
    if (!hh_start(hcfg_get()->enable_write))         ESP_LOGW(TAG, "Statusseite nicht gestartet (Gateway laeuft ohne HTTP weiter)");
    if (hmq_enabled() && !hmq_start())               ESP_LOGW(TAG, "MQTT nicht gestartet (Gateway laeuft ohne MQTT weiter)");
    hota_watch();                                    /* nur nach einem Update aktiv: bestaetigt das Image beim ersten CAN-Datenpunkt */
    xTaskCreate(status_task, "hoxpi_status", 3072, NULL, 2, NULL);
    ESP_LOGI(TAG, "bereit: Loxone kann Modbus-TCP :%d lesen (Templates wie HoxPi)", CONFIG_HOXPI_MODBUS_PORT);
}
