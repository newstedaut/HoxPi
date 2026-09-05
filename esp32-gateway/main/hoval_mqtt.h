/* hoval_mqtt.h — MQTT/Home-Assistant-Anbindung (esp-mqtt), Topics/Payloads aus hoval_ha.[ch]
 *
 *   hoval/<key>/state (retain)      Sensoren, COP, freigegebene Steuerungen
 *   hoval/<key>/set                 Kommando HA -> Gateway -> hm_write() (gleicher Pruefpfad wie Modbus)
 *   hoval/bridge/status             online / offline (LWT)
 *   hoval/stale/..., hoval/kuehl_wartet/...  binary_sensors (state + attr)
 *   homeassistant/.../hoxpi/<key>/config  Auto-Discovery (retain), bei Whitelist-Aenderung erneuert
 *
 * Aus, wenn CONFIG_HOXPI_MQTT_URI leer ist. Kein TLS erzwungen (mqtt:// im LAN; mqtts:// braucht Zertifikat-Konfig).
 */
#ifndef HOVAL_MQTT_H
#define HOVAL_MQTT_H
#include <stdbool.h>
#include <stdint.h>

typedef struct { bool connected; uint32_t pub_ok, pub_fail, cmd_ok, cmd_rej; } hmq_stats_t;

bool hmq_enabled(void);        /* URI konfiguriert? */
bool hmq_start(void);          /* Client + Task starten; false = aus oder Fehler (Gateway laeuft weiter) */
void hmq_stats(hmq_stats_t *s);

#endif
