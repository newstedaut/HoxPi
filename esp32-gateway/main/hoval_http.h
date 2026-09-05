/* hoval_http.h — kleine Status-/Konfigseite (esp_http_server), Gegenstueck zum HoxPi-Dashboard
 *
 *   GET  /               HTML-Minimalseite (liest /status per fetch, zeigt Kernwerte + Konfig)
 *   GET  /status         JSON: Laufzeit, CAN-Zaehler, stale, Modbus, Tabelle, Konfig, Kernregister
 *   GET  /config         JSON: Poll-Werte, Schreibfreigabe, Whitelist, Herkunft (NVS/Kompilat)
 *   POST /config         JSON-Body {"poll_wez":60,"poll_hv":5,"poll_delay":100,"wr_en":1,
 *                        "whitelist":"1490,1497"} -> pruefen, live anwenden, im NVS sichern.
 *                        Poll-Werte/Whitelist wirken sofort; wr_en erst nach Neustart (Modbus-Slave
 *                        uebernimmt die Freigabe beim Start) -> Antwort "restart_required":true.
 *   POST /config/reset   NVS-Namespace loeschen -> naechster Start mit Kompilat-Defaults
 *   POST /restart        Neustart
 *   GET  /ota            Update-Zustand: Partition, App-Version, pending_verify, letzter Lauf (hoval_ota.h)
 *   POST /ota            {"url":"https://host/hoxpi_esp32.bin"} -> Update in die inaktive OTA-Partition,
 *                        Neustart, Rollback wenn das neue Image keinen CAN-Datenpunkt dekodiert (202 Accepted)
 *   GET  /register?reg=N JSON zu einem Register (Tabellenzeile + Rohwort, seen)
 *
 * Schreibende Aufrufe (POST) verlangen den Header  X-Token: <CONFIG_HOXPI_HTTP_TOKEN>.
 * Ist das Token leer (Default), sind alle POST-Routen gesperrt (403) - wie bei HoxPi, wo das
 * Dashboard ohne Login nur liest. Kein TLS: nur im eigenen LAN betreiben.
 */
#ifndef HOVAL_HTTP_H
#define HOVAL_HTTP_H
#include <stdbool.h>
#include <stdint.h>

/* Server starten. modbus_write_effective = Schreibpfad, wie beim Start an hm_start() uebergeben. */
bool hh_start(bool modbus_write_effective);

#endif
